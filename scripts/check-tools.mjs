// 品質ゲート①：全ツールを同じ基準で機械チェックする。1つでも失敗したら終了コード1。
//   node scripts/check-tools.mjs            全ツール
//   node scripts/check-tools.mjs C02 C03    指定したツールだけ（類似チェックは全ツールと比べる）
import { readdirSync, readFileSync, existsSync } from 'node:fs';
import { extractRows, extractAnswer } from '../site/shared/rows.js';

const read = (p) => readFileSync(p, 'utf8');
const json = (p) => JSON.parse(read(p));
const langs = json('scripts/langs.json').map((l) => l.code);
const whoMap = json('scripts/who-map.json');
const locales = Object.fromEntries(langs.map((l) => [l, json(`site/locales/${l}.json`)]));

// TSV
const [head, ...lines] = read('2026_11/tools_simple.tsv').trim().split('\n').map((l) => l.split('\t'));
const tsv = Object.fromEntries(lines.map((c) => [c[0], Object.fromEntries(head.map((h, i) => [h, c[i] ?? '']))]));

const allIds = readdirSync('site').filter((n) => /^[A-Z]\d+$/.test(n) && existsSync(`site/${n}/tool.json`)).sort();
const only = process.argv.slice(2);
const ids = only.length ? only : allIds;

// ---- 基準値（C01 を基準に決めた。下げない）
const MIN_TEXT = { default: 1100 }; // 本文の文字数（タグを除く）。英語は単語数で見る
const MIN_EN_WORDS = 380;
const MAX_SIMILARITY = 0.5;       // 他ツールの本文との類似度の上限
const BAD_WORDS = /TODO|TBD|lorem|ipsum|XXX|ここに|〇〇|◯◯|FIXME|サンプルテキスト/i;

const text = (html) => html.replace(/<script[\s\S]*?<\/script>/g, '').replace(/<[^>]+>/g, ' ').replace(/&[a-z]+;/g, ' ').replace(/\s+/g, ' ').trim();
const shingles = (s, n = 8) => { const x = s.replace(/\s/g, ''); const set = new Set(); for (let i = 0; i + n <= x.length; i++) set.add(x.slice(i, i + n)); return set; };
const jaccard = (a, b) => { let i = 0; for (const x of a) if (b.has(x)) i++; return i / (a.size + b.size - i || 1); };

const contentOf = (id, l) => (existsSync(`site/${id}/_content.${l}.html`) ? read(`site/${id}/_content.${l}.html`) : null);
const shingleCache = {};
const shOf = (id, l) => (shingleCache[`${id}.${l}`] ||= shingles(text(contentOf(id, l) || '')));

let failed = 0;
const report = [];

// 全言語で、文言のキーが同じか（共通の文言の翻訳漏れを防ぐ）
{
  const E = [];
  for (const l of langs) for (const key of Object.keys(locales[langs[0]])) {
    if (/^c\d+\./.test(key)) continue; // ツール固有はツールごとに見る
    if (!locales[l][key]) E.push(`[${l}] locales に共通の文言「${key}」がない`);
  }
  if (E.length) { failed++; report.push(['(共通の文言)', E, []]); }
}
for (const id of ids) {
  const E = [], W = [];
  const k = id.toLowerCase();
  let cfg;
  try { cfg = json(`site/${id}/tool.json`); } catch (e) { report.push([id, ['tool.json が読めない: ' + e.message], []]); failed++; continue; }

  // 1) tool.json の必須項目
  for (const f of ['endpoint', 'who', 'inputs', 'result']) if (!cfg[f]) E.push(`tool.json に ${f} がない`);
  if (!cfg.result?.items || !cfg.result?.columns?.length) E.push('result.items / result.columns がない');
  if (cfg.endpoint && /^\/|^https?:/.test(cfg.endpoint)) E.push('endpoint は serp/... の形で書く（先頭に / や https を付けない）');

  // 2) TSV との一致（TSVにない・段が違うものは作らない）
  const row = tsv[id];
  if (!row) E.push('TSV に該当行がない');
  else {
    if (!row['段'].startsWith('1')) E.push(`TSV の段が「${row['段']}」。このツールは作らない決まり`);
    if (whoMap[row['誰の']] !== cfg.who) E.push(`who が TSV と違う（TSV: ${row['誰の']} → ${whoMap[row['誰の']]}、tool.json: ${cfg.who}）`);
    if (cfg.endpoint && !row['エンドポイント'].startsWith(cfg.endpoint.replace(/\/live\/advanced$/, '')) && row['エンドポイント'] !== cfg.endpoint)
      W.push(`endpoint が TSV と違う可能性（TSV: ${row['エンドポイント']}）`);
    const n = row['表示する項目'].split('・').length;
    if (cfg.result?.columns && cfg.result.columns.length !== n) W.push(`列の数が TSV の「表示する項目」(${n}個) と違う（${cfg.result.columns.length}個）。意図したものか確認`);
  }

  // 3) sample.json は実データで、画面に出せること
  try {
    const s = json(`site/${id}/sample.json`);
    if (!s.fetched_at) E.push('sample.json に fetched_at がない');
    if (!s.keyword && !s.inputs) E.push('sample.json に keyword（または inputs）がない');
    const rows = extractRows(cfg, s.tasks?.[0] || {});
    if (rows.length < (cfg.min_sample_rows ?? 3)) E.push(`サンプルの行が少ない（${rows.length}行）。実データを取り直すか、tool.json の result を見直す`);
    for (const c of cfg.result.columns) if (!rows.some((r) => r[c.key] !== undefined && r[c.key] !== null && r[c.key] !== '')) E.push(`サンプルで列「${c.key}」が全部空。取り出し方（from）が違う可能性`);
    if (cfg.result?.answer && !(extractAnswer(cfg, s.tasks?.[0] || {}).length > 100)) E.push('サンプルに回答文がない/短い（result.answer.markdown の場所を確認）');
    if (typeof s.tasks?.[0]?.cost !== 'number') W.push('sample.json に cost がない（実データのまま残すのが望ましい）');
  } catch (e) { E.push('sample.json が読めない/ない'); }

  // 4) 出典メモ（比較表の根拠）
  if (!existsSync(`site/${id}/_sources.md`)) E.push('_sources.md がない（比較表に書いた他社の料金・機能の出典URLと確認日を残す）');
  else {
    const src = read(`site/${id}/_sources.md`);
    if ((src.match(/https?:\/\//g) || []).length < 3) E.push('_sources.md に出典URLが3つ未満');
    if (!/確認日|checked/i.test(src)) E.push('_sources.md に確認日がない');
  }

  // 5) 言語ごと：文言・本文
  for (const l of langs) {
    const L = locales[l];
    const content = contentOf(id, l);
    if (content === null) { E.push(`[${l}] _content.${l}.html がない（全ツール、全対応言語でそろえる）`); continue; }
    const need = [`${k}.name`, `${k}.desc`, `${k}.price`, `${k}.eta`, `${k}.title`, `${k}.meta`, `who.${cfg.who}`,
      ...(cfg.inputs || []).map((i) => i.label), ...(cfg.result?.columns || []).map((c) => c.label), ...(cfg.count ? [cfg.count.label] : []), ...[...(cfg.result?.columns || []), ...(cfg.result?.extra || []).flatMap((x) => x.columns)].flatMap((c) => [c.label, ...Object.values(c.labels || {})])];
    for (const key of need) if (!L[key]) E.push(`[${l}] locales に「${key}」がない`);
    if (L[`${k}.meta`] && L[`${k}.meta`].length > 200) W.push(`[${l}] meta が長い（${L[`${k}.meta`].length}文字）。検索結果で切れる`);
    if (L[`${k}.title`] && L[`${k}.title`].length > 70) W.push(`[${l}] title が長い（${L[`${k}.title`].length}文字）`);
    if (row && l === 'ja') {
      const price = (row['1回の$料金'].match(/\$[\d.]+/) || [])[0];
      if (price && !(L[`${k}.price`] || '').includes(price)) W.push(`[ja] 料金表記に TSV の ${price} が入っていない`);
    }
    // 本文
    const t = text(content);
    if (!/<section class="seo">/.test(content)) E.push(`[${l}] 本文が <section class="seo"> で囲まれていない`);
    if (l === 'en' ? t.split(' ').length < MIN_EN_WORDS : t.length < MIN_TEXT.default) E.push(`[${l}] 本文が短い（${l === 'en' ? t.split(' ').length + ' words' : t.length + '文字'}）`);
    if (!/<table/.test(content) || (content.match(/<tr/g) || []).length < 4) E.push(`[${l}] 比較表がない、または行が少ない（見出し＋3行以上）`);
    if ((content.match(/<h2/g) || []).length < 4) E.push(`[${l}] 見出し(h2)が4つ未満（比較・メリット・向かない場面・FAQ）`);
    if ((content.match(/<details/g) || []).length < 4) E.push(`[${l}] FAQ(details)が4つ未満`);
    if (!/class="me"/.test(content)) E.push(`[${l}] 比較表に「このツール」の行（class="me"）がない`);
    if (!/class="asof"/.test(content)) E.push(`[${l}] 「○年○月時点」の注記（class="asof"）がない`);
    if (!/2026/.test(t)) E.push(`[${l}] 本文に調べた年月がない`);
    if (!/(向いていない|向かない|not the right fit|When it is not)/i.test(content)) E.push(`[${l}] 「向いていない場面」がない`);
    if (BAD_WORDS.test(content) || BAD_WORDS.test(JSON.stringify(L).includes(`"${k}.`) ? need.map((x) => L[x] || '').join(' ') : '')) E.push(`[${l}] 仮の文言（TODO/〇〇 など）が残っている`);
    if (/最安|業界No|必ず|絶対|圧倒的|革命/.test(content)) E.push(`[${l}] 言い切り・誇大表現がある（最安・必ず・絶対 など）`);
    // 類似度（使い回しの検出）
    for (const other of allIds) {
      if (other === id || !contentOf(other, l)) continue;
      const sim = jaccard(shOf(id, l), shOf(other, l));
      if (sim > MAX_SIMILARITY) E.push(`[${l}] 本文が ${other} と似すぎ（類似度 ${sim.toFixed(2)}）。使い回さず、このツールの「誰の」に合わせて書く`);
      else if (sim > MAX_SIMILARITY * 0.8) W.push(`[${l}] 本文が ${other} とやや似ている（${sim.toFixed(2)}）`);
    }
  }
  if (E.length) failed++;
  report.push([id, E, W]);
}

for (const [id, E, W] of report) {
  console.log(`${E.length ? '✗' : '✓'} ${id}${E.length ? ` — ${E.length}件の失敗` : ''}${W.length ? `（注意 ${W.length}件）` : ''}`);
  for (const e of E) console.log('    ✗ ' + e);
  for (const w of W) console.log('    ! ' + w);
}
console.log(`\n${report.length - failed}/${report.length} ツールが合格`);
process.exit(failed ? 1 : 0);
