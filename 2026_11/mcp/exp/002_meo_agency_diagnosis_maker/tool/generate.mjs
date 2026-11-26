// MEO診断メーカー：店名とキーワードから、1枚の「見え方診断」HTMLを作る。
// 使い方：NODE_USE_ENV_PROXY=1 node generate.mjs config.json
// config 例は config.sample.json。費用の目安：検索1回＋25地点＝約 $0.052（約8円）
import fs from 'node:fs';
import path from 'node:path';
import {connect} from '../../../lib/mcp.mjs';
import {runGrid} from '../../../lib/grid.mjs';

const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const outDir = path.resolve(path.dirname(process.argv[2]), cfg.out_dir || 'out');
fs.mkdirSync(outDir, {recursive: true});
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
const med = a => { a = a.filter(x => x != null).sort((x, y) => x - y); if (!a.length) return null; const m = a.length >> 1; return a.length % 2 ? a[m] : (a[m - 1] + a[m]) / 2; };

// 取得結果は data/ に保存。2回目以降（文面やルールの調整）は、保存分を使うので無料。
const cachePath = path.resolve(path.dirname(process.argv[2]), '../data', (cfg.slug || 'run') + '.json');
let shop, g, cost = 0, calls = 0;
if (fs.existsSync(cachePath) && !process.argv.includes('--refetch')) {
  ({shop, g, cost, calls} = JSON.parse(fs.readFileSync(cachePath, 'utf8')));
  console.log('保存済みデータを使用（費用0）');
} else {
  const mcp = await connect();
  // 1. 店を探す（全国検索。店名＋地名で入れる）
  const find = await mcp.api('/v3/serp/google/maps/live/advanced', [{keyword: cfg.shop_query, location_code: 2392, language_code: 'ja', depth: 5}]);
  shop = find.tasks?.[0]?.result?.[0]?.items?.[0];
  if (!shop) { console.error('店が見つかりませんでした'); process.exit(1); }
  // 2. 格子の間隔を決める。'auto'：お店の場所で検索した上位20店が広がる距離（20位までの距離）の半分を間隔にする（+$0.002）
  let scale = cfg.step_scale || 1, r20 = null;
  if (cfg.step_scale === 'auto') {
    const pr = await mcp.api('/v3/serp/google/maps/live/advanced', [{keyword: cfg.keyword, location_coordinate: `${shop.latitude},${shop.longitude},15z`, language_code: 'ja', depth: 20}]);
    const ds = (pr.tasks?.[0]?.result?.[0]?.items || []).filter(i => i.latitude).map(i => Math.hypot((i.latitude - shop.latitude) * 111000, (i.longitude - shop.longitude) * 90000)).sort((a, b) => a - b);
    r20 = ds.length ? Math.round(ds[ds.length - 1]) : 1100;
    scale = Math.min(2, Math.max(0.1, +(r20 / 2 / 550).toFixed(2)));
    console.log(`上位20店の広がり ${r20}m → 格子の間隔 約${Math.round(550 * scale)}m`);
  }
  // 3. 店のまわりで順位を取る
  g = await runGrid(mcp, {keyword: cfg.keyword, lat: shop.latitude, lng: shop.longitude, n: cfg.grid || 5, scale});
  g.r20 = r20;
  cost = mcp.cost; calls = mcp.calls; await mcp.close();
  fs.mkdirSync(path.dirname(cachePath), {recursive: true});
  fs.writeFileSync(cachePath, JSON.stringify({shop, g, cost, calls}));
}
console.log('対象の店:', shop.title, '/', shop.address);

// 4. 集計
const n = g.n, mat = Array.from({length: n}, () => Array(n).fill(null));
const top = new Map();
for (const c of g.cells) {
  const me = c.items.find(i => i.cid === shop.cid); mat[c.r][c.q] = me ? me.rank : null;
  for (const i of c.items.slice(0, 3)) if (i.cid !== shop.cid) top.set(i.cid, i);
}
const flat = mat.flat(), total = flat.length;
const cnt3 = flat.filter(v => v && v <= 3).length, cnt10 = flat.filter(v => v && v <= 10).length, cntOut = flat.filter(v => !v).length;
const h = (n - 1) / 2, centerRank = Number.isInteger(h) ? mat[h][h] : null;
// 比べる相手：お店の位置（マップの中心）で3位以内に入れていない時は、その場所で上にいる店。入れている時は、この地域で3位以内に入った店
const centerCell = g.cells.find(c => c.r === h && c.q === h);
const atDoor = centerCell ? centerCell.items.filter(i => i.cid !== shop.cid).slice(0, 3) : [];
const useDoor = (centerRank == null || centerRank > 3) && atDoor.length >= 3;
const tops = useDoor ? atDoor : [...top.values()];
const topLabel = useDoor ? 'お店の場所（マップの中心）で上位3位に出る店' : `この地域のどこかの地点で3位以内に入った他のお店（${tops.length}店）`;
const t = {rating: +(tops.reduce((s, i) => s + (i.rating || 0), 0) / (tops.filter(i => i.rating).length || 1)).toFixed(2), votes: med(tops.map(i => i.votes)), photos: med(tops.map(i => i.photos))};
const me = {rating: shop.rating?.value ?? null, votes: shop.rating?.votes_count ?? null, photos: shop.total_photos ?? null};
const profile = [
  ['オーナー確認（ビジネスの所有者確認）', shop.is_claimed === true],
  ['電話番号の登録', !!shop.phone], ['ホームページの登録', !!shop.url], ['営業時間の登録', !!shop.work_hours],
  ['追加カテゴリの登録', (shop.additional_categories || []).length > 0],
];
// 5. 次の一手（差がいちばん大きい項目を1つ。ルールはここに書いてある）
let next;
if (shop.is_claimed === false) next = 'Googleに「このお店のオーナー」として登録（確認）を済ませる。ここが未完了だと、情報の追加ができません。';
else if (me.votes != null && t.votes && me.votes < t.votes * 0.5) next = `お客さんに口コミをお願いする紙（QRコード）を、会計のそばに置く。いまの${me.votes}件を、上位店の中央値${t.votes}件に近づけるのが最初の目標です。`;
else if (me.photos != null && t.photos && me.photos < t.photos * 0.5) next = `写真を増やす。外観・内観・メニュー（商品）の3種類を、月に5枚ずつ追加。いまの${me.photos}枚に対して、上位店の中央値は${t.photos}枚です。`;
else if (me.rating != null && t.rating && me.rating <= t.rating - 0.4) next = `評価（星）の差を縮める。星1〜2の口コミを読み、共通の不満を1つ見つけて、返信で丁寧に対応する。いまの${me.rating}に対して、上位店の平均は${t.rating}です。`;
else if (centerRank != null && centerRank > 3) next = `お店の場所でも${centerRank}位です。まず、この場所で上にいる3店（上の比較）との差を、口コミの中身・写真・プロフィールの説明文で1つ見つけ、そこから手を付ける。`;
else if (profile.some(p => !p[1])) next = `未登録の項目（${profile.filter(p => !p[1]).map(p => p[0]).join('・')}）を埋める。`;
else next = '今回の診断では、上位店との大きな差は見つかりませんでした。口コミへの返信を全件に1〜2行ずつ返しながら、口コミを少しずつ増やすのが、次の一手です。';

const mask = !!cfg.mask, shopName = mask ? 'お客さまの店舗（例）' : shop.title, agency = cfg.agency || {name: '（会社名）', contact: ''};
const area = cfg.area_label || (shop.address_info?.city || '');
const cell = v => { const c = v == null ? 'r0' : v <= 3 ? 'r1' : v <= 10 ? 'r2' : 'r3'; return `<div class="cell ${c}">${v == null ? '圏外' : v}</div>`; };
const html = `<title>${esc(shopName)}さま Googleマップ見え方診断</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap">
<style>
:root{--bg:#f7f6f2;--panel:#fff;--fg:#1d2433;--muted:#5d6678;--line:#e1ded5;--accent:#183a6b;--hot:#d9541e;--hot-soft:#fbe9df;--accent-soft:#e6ecf5;
--c1:#183a6b;--c1t:#fff;--c2:#5d86bd;--c2t:#fff;--c3:#c3d3e8;--c3t:#1d2433;--c0:#ecebe6;--c0t:#8a8f9b;--font:'Noto Sans JP','Hiragino Sans',system-ui,sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#12161e;--panel:#1a202b;--fg:#e8ebf1;--muted:#9aa4b6;--line:#2a3342;--accent:#8db4ee;--hot:#ff8a55;--hot-soft:#3a2a20;--accent-soft:#1e2a40;--c1:#8db4ee;--c1t:#0f1626;--c2:#4a6fa5;--c2t:#fff;--c3:#2b3b57;--c3t:#e8ebf1;--c0:#222a38;--c0t:#7b8496;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#12161e;--panel:#1a202b;--fg:#e8ebf1;--muted:#9aa4b6;--line:#2a3342;--accent:#8db4ee;--hot:#ff8a55;--hot-soft:#3a2a20;--accent-soft:#1e2a40;--c1:#8db4ee;--c1t:#0f1626;--c2:#4a6fa5;--c2t:#fff;--c3:#2b3b57;--c3t:#e8ebf1;--c0:#222a38;--c0t:#7b8496;color-scheme:dark}
body{background:var(--bg);color:var(--fg);font-family:var(--font);line-height:1.8;font-size:15px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:28px 48px}
main{max-width:720px;margin:0 auto;display:flex;flex-direction:column;gap:22px}
h1{font-size:1.5rem;line-height:1.4;font-weight:900;margin:0;text-wrap:balance} h2{font-size:1.1rem;margin:0 0 8px;font-weight:900}
p{margin:0 0 8px}.m{color:var(--muted);font-size:.82rem}
.sum{background:var(--accent-soft);border-left:4px solid var(--accent);padding:12px 14px;border-radius:0 6px 6px 0}
.map{display:grid;grid-template-columns:repeat(${n},1fr);gap:4px;max-width:420px}
.cell{aspect-ratio:1;display:flex;align-items:center;justify-content:center;border-radius:6px;font-weight:900;font-size:1.1rem;font-variant-numeric:tabular-nums}
.r1{background:var(--c1);color:var(--c1t)}.r2{background:var(--c2);color:var(--c2t)}.r3{background:var(--c3);color:var(--c3t)}.r0{background:var(--c0);color:var(--c0t);font-weight:500;font-size:.75rem}
.legend{display:flex;flex-wrap:wrap;gap:10px;font-size:.78rem;color:var(--muted);margin-top:6px}.legend i{width:13px;height:13px;border-radius:3px;display:inline-block;vertical-align:-2px;margin-right:4px}
.cmp{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:12px;min-width:0}.card .k{font-size:.78rem;color:var(--muted)}.card .v{font-size:1.4rem;font-weight:900;font-variant-numeric:tabular-nums}
.card.gap .v{color:var(--hot)}
ul.chk{list-style:none;padding:0;margin:0;display:grid;gap:4px}ul.chk li{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:6px 10px;display:flex;justify-content:space-between;gap:8px}
.ok{color:var(--accent);font-weight:700}.ng{color:var(--hot);font-weight:700}
.next{background:var(--hot-soft);border:1px solid var(--hot);border-radius:8px;padding:12px 14px}
footer{border-top:1px solid var(--line);padding-top:12px}
</style>
<main>
<header><p class="m">${esc(agency.name)} ／ 診断日 ${esc(new Date().toISOString().slice(0, 10))} ／ 検索キーワード「${esc(cfg.keyword)}」</p>
<h1>${esc(shopName)}さま<br>Googleマップ見え方診断</h1></header>
<section class="sum"><p><b>${esc(shopName)}は、お店のまわり${total}地点（約${(g.step_m || 550) * (n - 1)}m四方）のうち、3位以内が${cnt3}地点、10位以内が${cnt10}地点、圏外（21位以下）が${cntOut}地点でした。</b></p>
<p style="margin:0 0 4px">お店の場所（マップの中心）では<b>${centerRank ? centerRank + '位' : '圏外'}</b>です。</p><p class="m" style="margin:0">「${esc(cfg.keyword)}」と検索した人に、場所ごとにどう見えるかを調べました。</p></section>
<section><h2>場所ごとの順位</h2>
<div class="map" role="img" aria-label="場所ごとの順位マップ">${mat.map(r => r.map(cell).join('')).join('')}</div>
<div class="legend"><span><i style="background:var(--c1)"></i>1〜3位</span><span><i style="background:var(--c2)"></i>4〜10位</span><span><i style="background:var(--c3)"></i>11〜20位</span><span><i style="background:var(--c0)"></i>圏外</span></div>
<p class="m" style="margin-top:6px">上が北。1マス約${g.step_m || 550}m。お店はマップの中心です。</p></section>
<section><h2>上位の店と比べると</h2>
<div class="cmp">
<div class="card${me.votes != null && t.votes && me.votes < t.votes * .5 ? ' gap' : ''}"><div class="k">口コミの数</div><div class="v">${me.votes ?? '—'}件</div><div class="m">上位店の中央値 ${t.votes ?? '—'}件</div></div>
<div class="card${me.photos != null && t.photos && me.photos < t.photos * .5 ? ' gap' : ''}"><div class="k">写真の数</div><div class="v">${me.photos ?? '—'}枚</div><div class="m">上位店の中央値 ${t.photos ?? '—'}枚</div></div>
<div class="card"><div class="k">評価（星）</div><div class="v">${me.rating ?? '—'}</div><div class="m">上位店の平均 ${t.rating}</div></div>
</div><p class="m" style="margin-top:6px">上位店＝${topLabel}。</p></section>
<section><h2>プロフィールの基本項目</h2><ul class="chk">${profile.map(p => `<li><span>${p[0]}</span><span class="${p[1] ? 'ok' : 'ng'}">${p[1] ? '登録あり' : '未登録'}</span></li>`).join('')}</ul></section>
<section class="next"><p style="margin:0"><b>次の一手（まず1つ）</b></p><p style="margin:0">${esc(next)}</p></section>
<footer><p class="m">この診断は、Googleマップの検索結果を機械で取得した目安です。人や時間によって表示は変わります。順位の上昇を保証するものではありません。口コミの買い取り・自作自演はGoogleの規約違反です。</p>
<p class="m">${esc(agency.name)} ${esc(agency.contact || '')}</p></footer>
</main>`;
fs.writeFileSync(path.join(outDir, 'diagnosis.html'), html);
fs.writeFileSync(path.join(outDir, 'diagnosis.json'), JSON.stringify({shop: {title: mask ? '(masked)' : shop.title, rating: me.rating, votes: me.votes, photos: me.photos, profile: Object.fromEntries(profile)}, keyword: cfg.keyword, grid: mat, counts: {total, top3: cnt3, top10: cnt10, out: cntOut}, top_shops: {n: tops.length, ...t}, next, cost_usd: +cost.toFixed(4), calls, center_rank: centerRank, benchmark: useDoor ? 'door_top3' : 'area_top3'}, null, 1));
console.log(JSON.stringify({shop: shop.title, counts: {total, top3: cnt3, top10: cnt10, out: cntOut}, me, top: t, next, cost: +cost.toFixed(4), calls, center_rank: centerRank, benchmark: useDoor ? 'door_top3' : 'area_top3'}, null, 1));
