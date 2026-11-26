// 順位のゆれを測る：002で取った格子と、同じ条件（同じ地点・同じ言葉）で取り直して、地点ごとに比べる。
// 使い方：NODE_USE_ENV_PROXY=1 node noise.mjs <002のdata/xxx.json> <取り直す回数> <出力名>
// 費用：1回の取り直しあたり $0.05（25地点）
import fs from 'node:fs';
import path from 'node:path';
import {connect} from '../../../lib/mcp.mjs';
import {runGrid} from '../../../lib/grid.mjs';
const [src, reps, name] = [process.argv[2], +process.argv[3] || 1, process.argv[4] || 'run'];
const base = JSON.parse(fs.readFileSync(src, 'utf8'));
const g0 = base.g, shop = base.shop;
const mcp = await connect();
const runs = [{label: 'A（以前に取ったもの）', g: g0, fetched: 'earlier'}];
for (let i = 0; i < reps; i++) {
  const g = await runGrid(mcp, {keyword: g0.keyword, lat: g0.center[0], lng: g0.center[1], n: g0.n, scale: (g0.step_m / 111000) / 0.005});
  runs.push({label: 'BCDEFG'[i] + '（取り直し' + (i + 1) + '回目）', g, fetched: new Date().toISOString()});
}
const cost = mcp.cost; await mcp.close();
fs.writeFileSync(path.resolve(path.dirname(process.argv[1]), '../data', name + '_runs.json'), JSON.stringify({shop: shop.title, keyword: g0.keyword, step_m: g0.step_m, cost, runs}));

const rankOf = (g, c) => { const cell = g.cells.find(x => x.r === c.r && x.q === c.q); return cell.items.find(i => i.cid === shop.cid)?.rank ?? null; };
const top3 = (g, c) => new Set(g.cells.find(x => x.r === c.r && x.q === c.q).items.slice(0, 3).map(i => i.cid));
const lists = (g, c) => g.cells.find(x => x.r === c.r && x.q === c.q).items.map(i => i.cid);
function pair(a, b) {
  let same = 0, both = 0, absd = 0, oneOut = 0, maxd = 0, j = 0, tot = 0, ovl = 0, within2 = 0;
  for (const c of g0.cells) {
    tot++;
    const ra = rankOf(a.g, c), rb = rankOf(b.g, c);
    if (ra === rb) same++;
    if (ra && rb) { both++; absd += Math.abs(ra - rb); maxd = Math.max(maxd, Math.abs(ra - rb)); if (Math.abs(ra - rb) <= 2) within2++; }
    else if (ra || rb) oneOut++;
    const A = top3(a.g, c), B = top3(b.g, c); j += [...A].filter(x => B.has(x)).length / 3;
    const la = lists(a.g, c).slice(0, 10), lb = new Set(lists(b.g, c).slice(0, 10)); ovl += la.filter(x => lb.has(x)).length / 10;
  }
  return {地点数: tot, 順位が全く同じ: same, 両方に出ている地点: both, 差が2位以内: within2, 平均の差: both ? +(absd / both).toFixed(2) : null, 最大の差: maxd, 片方だけ圏外: oneOut, 上位3店の一致率: +(j / tot).toFixed(2), 上位10店の一致率: +(ovl / tot).toFixed(2)};
}
const sum = g => { const rs = g0.cells.map(c => rankOf(g, c)); return {'3位以内': rs.filter(r => r && r <= 3).length, '10位以内': rs.filter(r => r && r <= 10).length, '圏外': rs.filter(r => !r).length}; };
const out = {店: shop.title, 費用: +cost.toFixed(3), 各回の集計: runs.map(r => ({回: r.label, ...sum(r.g)})), 比較: []};
for (let i = 0; i < runs.length; i++) for (let k = i + 1; k < runs.length; k++) out.比較.push({組: runs[i].label.slice(0, 1) + 'と' + runs[k].label.slice(0, 1), ...pair(runs[i], runs[k])});
fs.writeFileSync(path.resolve(path.dirname(process.argv[1]), '../data', name + '_summary.json'), JSON.stringify(out, null, 1));
console.log(JSON.stringify(out, null, 1));
