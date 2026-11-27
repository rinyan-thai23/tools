// 月1の通信簿：前回と今回の格子（002/004と同じ形）を比べ、ゆれの範囲を「変化なし」と言い切る。
// 使い方：node card.mjs <runs.json> <前回の番号> <今回の番号>  （費用0・保存データだけ使う）
import fs from 'node:fs';
const [f, ia, ib] = [process.argv[2], +process.argv[3] || 0, +process.argv[4] || 1];
const d = JSON.parse(fs.readFileSync(f, 'utf8')); const A = d.runs[ia].g, B = d.runs[ib].g;
const cid = d.runs[0].g.cells.flatMap(c => c.items).find(i => i.title === d.shop)?.cid ?? d.runs[0].g.cells.flatMap(c => c.items).find(i => d.shop.startsWith(i.title.slice(0, 5)))?.cid;
const rk = (g, c) => g.cells.find(x => x.r === c.r && x.q === c.q).items.find(i => i.cid === cid)?.rank ?? null;
const stat = g => { const rs = g.cells.map(c => rk(g, c)); const inn = rs.filter(Boolean).sort((a, b) => a - b);
  return {top3: rs.filter(r => r && r <= 3).length, top10: rs.filter(r => r && r <= 10).length, out: rs.filter(r => !r).length, median: inn.length ? inn[Math.floor(inn.length / 2)] : null, n: rs.length}; };
const a = stat(A), b = stat(B);
// ゆれの許容（004で測った：同条件でも順位は平均1.7〜2.4ずれ、件数は数セルずれる）
const TOL_CELLS = 3, TOL_RANK = 2;
const judge = (x, y, tol) => Math.abs(y - x) <= tol ? '変化なし（ゆれの範囲）' : (y > x ? '増えた' : '減った');
const rows = [
  ['上位3位に入る地点', a.top3, b.top3, judge(a.top3, b.top3, TOL_CELLS)],
  ['上位10位に入る地点', a.top10, b.top10, judge(a.top10, b.top10, TOL_CELLS)],
  ['圏外（20位まで見て出ない）の地点', a.out, b.out, judge(a.out, b.out, TOL_CELLS)],
  ['順位の中央値', a.median, b.median, a.median == null || b.median == null ? '—' : Math.abs(a.median - b.median) <= TOL_RANK ? '変化なし（ゆれの範囲）' : (b.median < a.median ? '良くなった' : '悪くなった')]];
const out = {shop: d.shop, keyword: d.keyword, cells: a.n, 前回: d.runs[ia].label, 今回: d.runs[ib].label, rows};
fs.writeFileSync(new URL('../data/card_' + ia + ib + '.json', import.meta.url), JSON.stringify(out, null, 1));
console.log(JSON.stringify(out, null, 1));
