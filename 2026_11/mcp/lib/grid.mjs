// Googleマップの「場所ごと順位」を取る。1点 $0.002。
// 例: node lib/grid.mjs --keyword ラーメン --lat 35.7057 --lng 139.6497 --n 5 --out out.json
import fs from 'node:fs';
import {connect} from './mcp.mjs';

export function cellsAround(lat0, lng0, n = 5, dlat = 0.005, dlng = 0.0062) {
  const h = (n - 1) / 2, cells = [];
  for (let r = 0; r < n; r++) for (let q = 0; q < n; q++)
    cells.push({r, q, lat: +(lat0 + (h - r) * dlat).toFixed(5), lng: +(lng0 + (q - h) * dlng).toFixed(5)}); // r=0 が北
  return cells;
}
const slim = x => ({rank: x.rank_group, title: x.title, cid: x.cid, rating: x.rating?.value ?? null, votes: x.rating?.votes_count ?? null,
  lat: x.latitude, lng: x.longitude, cat: x.category, claimed: x.is_claimed, photos: x.total_photos ?? null});

export async function runGrid(mcp, {keyword, lat, lng, n = 5, depth = 20, conc = 5, scale = 1}) {
  const dlat = 0.005 * scale, dlng = 0.0062 * scale;
  const cells = cellsAround(lat, lng, n, dlat, dlng), out = [];
  let i = 0;
  const worker = async () => { while (i < cells.length) { const c = cells[i++];
    const d = await mcp.api('/v3/serp/google/maps/live/advanced', [{keyword, location_coordinate: `${c.lat},${c.lng},15z`, language_code: 'ja', depth}]);
    const tk = d.tasks?.[0];
    out.push({...c, status: tk?.status_code, items: (tk?.result?.[0]?.items || []).map(slim)}); } };
  await Promise.all(Array.from({length: conc}, worker));
  out.sort((a, b) => a.r - b.r || a.q - b.q);
  return {keyword, center: [lat, lng], n, step_m: Math.round(dlat * 111000), cells: out};
}

if (process.argv[1] && process.argv[1].endsWith('grid.mjs')) {
  const a = Object.fromEntries(process.argv.slice(2).reduce((m, v, k, arr) => v.startsWith('--') ? [...m, [v.slice(2), arr[k + 1]]] : m, []));
  const mcp = await connect();
  const g = await runGrid(mcp, {keyword: a.keyword, lat: +a.lat, lng: +a.lng, n: +(a.n || 5)});
  g.cost = mcp.cost; fs.writeFileSync(a.out || 'grid.json', JSON.stringify(g));
  console.log('cells', g.cells.length, 'cost', g.cost.toFixed(3), 'errors', g.cells.filter(c => c.status !== 20000).length);
  await mcp.close();
}
