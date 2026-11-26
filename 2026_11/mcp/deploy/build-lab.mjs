// lab.byokkit.com 用のビルド。mcp/ の資料を静的ページにして、1つのWorkerに埋め込む。
// 使い方：cd 2026_11/mcp && node deploy/build-lab.mjs   → deploy/dist/worker.js ができる
// 検索エンジンには出さない：全ページに noindex の meta、全応答に X-Robots-Tag、/robots.txt は全拒否。
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {marked} from 'marked';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const dist = path.join(here, 'dist');
fs.mkdirSync(dist, {recursive: true});

const ASSETS = {}; // urlpath -> {ct, text?, b64?}
const TYPES = {'.html': 'text/html', '.json': 'application/json', '.txt': 'text/plain', '.md': 'text/plain', '.mjs': 'text/plain', '.css': 'text/css', '.png': 'image/png', '.tsv': 'text/plain'};
const isText = ct => /^(text\/|application\/json)/.test(ct);
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
const NOINDEX = '<meta name="robots" content="noindex, nofollow, noarchive">';

function put(urlpath, content, ext) {
  const ct = TYPES[ext] || 'application/octet-stream';
  const full = isText(ct) ? ct + '; charset=utf-8' : ct;
  ASSETS[urlpath] = isText(ct) ? {ct: full, text: content.toString()} : {ct: full, b64: Buffer.from(content).toString('base64')};
}
// 既存のHTML（<head>のない断片）に、doctype・文字コード・noindexを付けて公開する
function putHtml(urlpath, srcFile) {
  let h = fs.readFileSync(srcFile, 'utf8');
  if (!/^\s*<!doctype/i.test(h)) h = `<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">${NOINDEX}<style>body{margin:0}img{max-width:100%}</style>\n` + h;
  else h = h.replace(/<head>/i, '<head>' + NOINDEX);
  put(urlpath, h, '.html');
}
function putFile(urlpath, srcFile) {
  const ext = path.extname(srcFile).toLowerCase();
  if (ext === '.html') return putHtml(urlpath, srcFile);
  put(urlpath, fs.readFileSync(srcFile), ext);
}
function walk(dir, skip = () => false) {
  const out = [];
  for (const n of fs.readdirSync(dir).sort()) {
    const p = path.join(dir, n);
    if (skip(p, n)) continue;
    if (fs.statSync(p).isDirectory()) out.push(...walk(p, skip)); else out.push(p);
  }
  return out;
}
const kb = n => n < 1024 ? n + ' B' : (n / 1024).toFixed(n < 10240 ? 1 : 0) + ' KB';

// ---------- 共通の見た目 ----------
const CSS = `
:root{--bg:#f7f6f2;--panel:#fff;--fg:#1d2433;--muted:#5d6678;--line:#e1ded5;--accent:#183a6b;--accent-soft:#e6ecf5;--hot:#d9541e;--hot-soft:#fbe9df;--ok:#2a7a4f;--font:'Noto Sans JP','Hiragino Sans','Yu Gothic',system-ui,sans-serif}
@media (prefers-color-scheme:dark){:root{--bg:#12161e;--panel:#1a202b;--fg:#e8ebf1;--muted:#9aa4b6;--line:#2a3342;--accent:#8db4ee;--accent-soft:#1e2a40;--hot:#ff8a55;--hot-soft:#3a2a20;--ok:#6cc79a;color-scheme:dark}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--font);line-height:1.85;font-size:15.5px;padding:0 max(16px,env(safe-area-inset-right,0px)) 64px max(16px,env(safe-area-inset-left,0px))}
.top{max-width:900px;margin:0 auto;padding:14px 0;display:flex;gap:14px;flex-wrap:wrap;align-items:center;border-bottom:1px solid var(--line);font-size:.85rem}
.top a{color:var(--accent);text-decoration:none}.top .sp{flex:1}
.tag{border:1px solid var(--hot);color:var(--hot);border-radius:4px;padding:0 8px;font-size:.78rem}
main{max-width:900px;margin:0 auto;padding-top:24px;min-width:0}
h1{font-size:1.7rem;line-height:1.4;font-weight:900;margin:0 0 14px;text-wrap:balance}
h2{font-size:1.25rem;font-weight:900;margin:34px 0 10px;padding-bottom:6px;border-bottom:2px solid var(--accent);text-wrap:balance}
h3{font-size:1.05rem;margin:22px 0 6px}
p{margin:0 0 12px}ul,ol{margin:0 0 12px;padding-left:1.4em}li{margin-bottom:4px}
a{color:var(--accent)}code{background:var(--accent-soft);padding:1px 6px;border-radius:4px;font-size:.86em;overflow-wrap:anywhere}
pre{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:12px;overflow-x:auto}pre code{background:none;padding:0}
blockquote{margin:0 0 12px;padding:8px 14px;border-left:4px solid var(--accent);background:var(--accent-soft)}
.tw{overflow-x:auto;background:var(--panel);border:1px solid var(--line);border-radius:8px;margin:0 0 14px}
table{border-collapse:collapse;width:100%;min-width:560px;font-size:.88rem}th,td{padding:8px 10px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
th{background:var(--accent-soft);white-space:nowrap}tr:last-child td{border-bottom:0}
.note{background:var(--hot-soft);border:1px dashed var(--hot);border-radius:8px;padding:10px 14px;font-size:.88rem;margin:0 0 18px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:14px 0}
.card{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:12px 14px}.card b{display:block;font-size:1.5rem;font-variant-numeric:tabular-nums}.card span{color:var(--muted);font-size:.82rem}
.btns{display:flex;flex-wrap:wrap;gap:10px;margin:14px 0 8px}
.btn{display:inline-block;background:var(--accent);color:var(--bg);text-decoration:none;border-radius:8px;padding:9px 16px;font-weight:700;font-size:.92rem}
.btn.sub{background:var(--panel);color:var(--accent);border:1px solid var(--accent)}
.ok{color:var(--ok);font-weight:700}.hold{color:var(--hot);font-weight:700}
.files{font-size:.88rem}.files li{overflow-wrap:anywhere}.files .sz{color:var(--muted);margin-left:6px}
.pn{display:flex;justify-content:space-between;gap:12px;margin-top:40px;padding-top:14px;border-top:1px solid var(--line);font-size:.9rem}
`;
const FONT = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap">';
function shell({title, body, crumbs = ''}) {
  return `<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">${NOINDEX}<title>${esc(title)}</title>${FONT}<style>${CSS}</style></head><body>
<nav class="top"><a href="/"><b>MCP実験室</b></a>${crumbs}<span class="sp"></span><a href="/ideas/">アイデア帳</a><a href="/patterns/">型の判断</a><a href="/about/">進め方</a><span class="tag">社内用・検索に出しません</span></nav>
<main>${body}</main></body></html>`;
}
const md = s => marked.parse(s, {gfm: true}).replace(/<table>/g, '<div class="tw"><table>').replace(/<\/table>/g, '</table></div>');

// ---------- 台帳 ----------
const rows = fs.readFileSync(path.join(root, 'INDEX.tsv'), 'utf8').trim().split('\n').map(l => l.split('\t'));
const head = rows[0], data = rows.slice(1).map(r => Object.fromEntries(head.map((h, i) => [h, r[i] ?? ''])));
const NAMES = {
  '000': 'ドメイン診断（簡易コンサル）とMCPの比較', '001': '場所ごとの順位マップ診断（店主向け）', '002': 'MEO診断メーカー（制作会社・代行向け）',
  '003': 'AI概要への掲載チェック', '004': '順位のノイズ測定', '005': '店の特定の改善', '006': '複数店舗の比較ボード', '007': '既存ツールとの違いの整理',
  '008': '担当者がいない会社の月1通信簿', '009': '店舗向けマップ月次通信簿', '010': '開業前の商圏競合調査', '011': '口コミ読解レポート', '012': '営業提案書の下書き', '013': '士業向け「探されている言葉」の地図', '014': '近所の競合の料金・メニュー比較', '015': '競合の口コミから「選ばれる理由・嫌われる理由」を読む', '016': '業種×街の「不満・期待」調査レポート', '017': '口コミとHPのズレ診断（旧：口コミから作るHP素材）', '018': '多言語の口コミ（インバウンドの声）', '019': '大量・無作為の口コミ抽出（見積り）', '020': '3業種の口コミ不満マップ（歯科・美容室・整骨院）'};

// ---------- 事例ページ ----------
const cases = []; // {id, dir, readme, files:[{url,label,size}], extra}
const exp = path.join(root, 'exp');
for (const d of fs.readdirSync(exp).sort()) {
  const m = d.match(/^(\d{3})_/); if (!m) continue;
  const dir = path.join(exp, d);
  const files = walk(dir, (p, n) => n === 'README.md' && path.dirname(p) === dir || n === '_template.html' || n === 'node_modules');
  cases.push({id: m[1], dir, readme: fs.readFileSync(path.join(dir, 'README.md'), 'utf8'), files, base: dir});
}
// 000：最初の実験（ドメイン診断とMCP比較）は mcp/ 直下にある
{
  const files = [path.join(root, 'khansei_report.html'), path.join(root, 'khansei_report.md'), ...walk(path.join(root, 'data', 'site01'))];
  const readme = `# 000 ドメイン診断（簡易コンサル）と、公式MCPの比較\n\n- 日付：2026-11-26　／　実費：約 **$0.1**　／　状態：完了（簡易コンサルとして通用）\n- 一言：中小企業のドメイン1つについて、検索データ5本（全体の強さ・順位つきキーワード・ページ別・競合・同業との差）を、公式MCPで取り、AIが分析レポートを書いた。\n\n## 誰の、どんな悩みか\n「うちのサイトは、ネットでどう見えているか」を知りたい社長・士業。調査は安く速くできる時代になったが、価値は「次に何をするか」を決めることにある。\n\n## 読む順番\n1. まず **[レポート本体（図つき）](/c/000/report/)** を読む。これが1枚の診断資料\n2. 下の「MCPの実験メモ」を読む（公式MCPを使って分かったこと）\n\n---\n\n` + fs.readFileSync(path.join(root, 'mcp_test.md'), 'utf8').replace(/^# .*\n/, '## MCPの実験メモ\n')
    .replace(/## 結果メモ（khansei[^\n]*/, '## 結果メモ（対象サイトのA〜E 実行）').replace('## 追加テスト：AI概要への掲載（LLM Mentions・対象サイト、2026-11-26）', '## 追加テスト：AI概要への掲載（→ 003へ）');
  cases.unshift({id: '000', dir: root, readme, files, base: root, special: true});
}
const url0 = c => `/c/${c.id}/`;
const idsWithPage = new Set(cases.map(c => c.id));

for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  // ファイルを公開（base からの相対パスで）
  const list = [];
  for (const f of c.files) {
    let rel = path.relative(c.base, f).split(path.sep).join('/');
    if (c.id === '000') { rel = rel.startsWith('data/site01/') ? 'data/' + rel.slice('data/site01/'.length) : rel; if (rel === 'khansei_report.html') rel = 'report/index.html'; }
    const u = url0(c) + rel;
    putFile(u, f);
    list.push({u: u.endsWith('/index.html') ? u.slice(0, -10) : u, rel, size: fs.statSync(f).size});
  }
  // 「見る・開く」ボタン（LP・見本・レポートがあれば先頭に出す）
  const btn = [];
  const has = r => list.find(x => x.rel === r);
  if (has('report/index.html')) btn.push(`<a class="btn" href="${has('report/index.html').u}">診断レポートを開く</a>`);
  if (has('lp/index.html')) btn.push(`<a class="btn" href="${has('lp/index.html').u}">LP（見本）を開く</a>`);
  if (has('sample_output/diagnosis.html')) btn.push(`<a class="btn sub" href="${has('sample_output/diagnosis.html').u}">診断書の見本を開く</a>`);
  // ファイル一覧（フォルダごと）
  const groups = {};
  for (const x of list) { const g = x.rel.includes('/') ? x.rel.slice(0, x.rel.lastIndexOf('/')) : '（直下）'; (groups[g] ||= []).push(x); }
  const filesHtml = '<h2>成果物・生データの一覧</h2><p class="note">店名つきの生データも含まれます。検索エンジンには出しませんが、URLを知っている人は開けます。</p>' +
    Object.entries(groups).map(([g, xs]) => `<h3>${esc(g)}</h3><ul class="files">${xs.map(x => `<li><a href="${x.u}">${esc(x.rel.split('/').pop())}</a><span class="sz">${kb(x.size)}</span></li>`).join('')}</ul>`).join('');
  const prev = cases[i - 1], next = cases[i + 1];
  const pn = `<div class="pn"><span>${prev ? `← <a href="${url0(prev)}">${prev.id} ${esc(NAMES[prev.id])}</a>` : ''}</span><span>${next ? `<a href="${url0(next)}">${next.id} ${esc(NAMES[next.id])}</a> →` : ''}</span></div>`;
  const row0 = data.find(d => d.id === c.id); const row = row0 && {...row0, '誰の': row0['who(誰の)'], '何を解決': row0['solves(何を解決)'], '区分': row0['区分(データ)']};
  const body = (btn.length ? `<div class="btns">${btn.join('')}</div>` : '') + md(c.readme) +
    (row ? `<h2>台帳での評価</h2><div class="tw"><table><tbody>${['誰の', '何を解決', '区分', '判定', '合計/21', 'メモ'].map(k => row[k] !== undefined ? `<tr><th>${k}</th><td>${esc(row[k])}</td></tr>` : '').join('')}</tbody></table></div>` : '') +
    filesHtml + pn;
  const title = `${c.id} ${NAMES[c.id]}`;
  put(url0(c) + 'index.html', shell({title, body, crumbs: `<span>／</span><span>${esc(title)}</span>`}), '.html');
}

// ---------- 全体の目次 ----------
const stat = v => /^(採用|候補|見本完了|見積り完了|実測完了)/.test(v) ? `<span class="ok">${esc(v)}</span>` : v ? `<span class="hold">${esc(v)}</span>` : '';
const tbl = `<div class="tw"><table style="min-width:1100px"><thead><tr><th>ID</th><th>案</th><th>誰の</th><th>何を解決できるか</th><th>形・売り先</th><th>データの区分</th><th>費用(USD)</th><th>状態</th></tr></thead><tbody>${data.map(r => {
  const nm = esc(NAMES[r.id] || r.slug);
  return `<tr><td>${r.id}</td><td>${idsWithPage.has(r.id) ? `<a href="/c/${r.id}/">${nm}</a>` : nm}</td><td>${esc(r['who(誰の)'])}</td><td>${esc(r['solves(何を解決)'])}</td><td>${esc(r['tags(形・売り先)'])}</td><td>${esc(r['区分(データ)'])}</td><td>${esc(r['原価USD'])}</td><td>${stat(r['判定'])}</td></tr>`;
}).join('')}</tbody></table></div>`;
const indexBody = `
<h1>MCP実験室：レポート型の事業案を、まず20本試す</h1>
<p>「誰を喜ばせるか」から考えて、DataForSEOのデータで作れる<b>レポート型の事業案</b>を、実際にAPIを叩いて試す場所です。まず20本で区切り、そのあと既存ツールの公開とじっくりした検討に移ります。1つの案は、<b>1ページに全部入っています</b>（誰のため・何をどうしたか・費用・結果・弱点・LP・生データ）。</p>
<p class="note">このサイトは検索エンジンに出さない設定です（noindex）。パスワードはないので、URLを知っている人は開けます。実在の店名・会社名つきのデータを含みます。</p>
<div class="cards">
 <div class="card"><b>${data.filter(r => ['000', '001', '002', '003', '004', '007', '011', '013', '015', '016', '017', '019', '020'].includes(r.id)).length} / 20案</b><span>実験を終えた案（目標20）（${data.filter(r => r['判定'] === '構想').length}案が構想中）</span></div>
 <div class="card"><b>約$1.71</b><span>ここまでの実費合計（約255円）</span></div>
 <div class="card"><b>約$0.054</b><span>診断1回の原価（約8円）</span></div>
 <div class="card"><b>0人</b><span>外の人の反応（これから）</span></div>
</div>
<h2>案の一覧</h2>${tbl}
<p style="font-size:.85rem;color:var(--muted)">点数は、AIによる暫定の自己採点（21点満点）。採用は、外の人の反応で決めます。実費は、API料金のみ（Claudeの利用料は含みません）。</p>
<h2>まず読む順番（全体像をつかむ）</h2>
<ol>
 <li><a href="/ideas/"><b>アイデア帳</b></a>：需要から考えた新しい案（008〜013）と、毎回の「強引チェック」。いちばん新しい考え方はここ</li>
 <li><a href="/patterns/"><b>型の判断</b></a>：成り立ちそうな型と、そうでない型（根拠つき）。ここだけ読めば全体の結論が分かります</li>
 <li><a href="/c/002/"><b>002 MEO診断メーカー</b></a>：いま一番進んでいる案（道具・見本・LP・激戦区の確認）</li>
 <li><a href="/c/001/"><b>001 順位マップ診断</b></a>：002の元になった、店主向けの案</li>
 <li><a href="/c/000/"><b>000 ドメイン診断</b></a>：最初の実験。簡易コンサルとして通用した例</li>
 <li><a href="/about/"><b>進め方</b></a>：100本から10本を選ぶ決まりと、採用の基準</li>
</ol>`;
put('/index.html', shell({title: 'MCP実験室', body: indexBody}), '.html');
put('/about/index.html', shell({title: '進め方', body: md(fs.readFileSync(path.join(root, 'README.md'), 'utf8')), crumbs: '<span>／</span><span>進め方</span>'}), '.html');
put('/ideas/index.html', shell({title: 'アイデア帳', body: md(fs.readFileSync(path.join(root, 'IDEAS.md'), 'utf8')), crumbs: '<span>／</span><span>アイデア帳</span>'}), '.html');
put('/patterns/index.html', shell({title: '型の判断', body: md(fs.readFileSync(path.join(root, 'PATTERNS.md'), 'utf8')), crumbs: '<span>／</span><span>型の判断</span>'}), '.html');
put('/robots.txt', 'User-agent: *\nDisallow: /\n', '.txt');

// ---------- Worker ----------
const worker = `// 自動生成（deploy/build-lab.mjs）。lab.byokkit.com：社内用・検索に出さない。
const A = ${JSON.stringify(ASSETS)};
const H = {'X-Robots-Tag': 'noindex, nofollow, noarchive', 'Referrer-Policy': 'no-referrer', 'X-Content-Type-Options': 'nosniff', 'Cache-Control': 'public, max-age=60'};
const bin = b64 => Uint8Array.from(atob(b64), c => c.charCodeAt(0));
export default {
  async fetch(req) {
    const u = new URL(req.url);
    let p; try { p = decodeURIComponent(u.pathname); } catch { return new Response('bad request', {status: 400, headers: H}); }
    if (p.endsWith('/')) p += 'index.html';
    let a = A[p];
    if (!a && !/\\.[a-z0-9]+$/i.test(p) && A[p + '/index.html']) return Response.redirect(u.origin + u.pathname + '/', 301);
    if (!a) return new Response('見つかりません', {status: 404, headers: {...H, 'Content-Type': 'text/plain; charset=utf-8'}});
    return new Response(req.method === 'HEAD' ? null : (a.text !== undefined ? a.text : bin(a.b64)), {headers: {...H, 'Content-Type': a.ct}});
  }
};
`;
fs.writeFileSync(path.join(dist, 'worker.js'), worker);
const total = Object.values(ASSETS).reduce((s, a) => s + (a.text ? Buffer.byteLength(a.text) : a.b64.length), 0);
console.log('ページ・ファイル数', Object.keys(ASSETS).length, '／ 埋め込み合計', kb(total), '／ worker.js', kb(Buffer.byteLength(worker)));
