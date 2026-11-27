// 複数店舗（同じチェーンの支店）の比較ボード。本部向け：「どの店が負けているか」を1表で。
// 流れ：①支店のリスト（business_listings・店名で絞る）②各支店の口コミ（新しい順N件＋評価の低い順M件・並列）③各支店の場所で検索したときの順位 ④集計
// 使い方：NODE_USE_ENV_PROXY=1 node board.mjs <設定.json>
import fs from 'node:fs';
import path from 'node:path';
import {connect} from '../../../lib/mcp.mjs';
const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const out = path.resolve(path.dirname(process.argv[2]), '../data');
const mcp = await connect(); const sleep = ms => new Promise(r => setTimeout(r, ms));
// ① 支店のリスト
let branches;
if (cfg.discover === 'maps') { // 地図検索で、近くの支店を集める（店名にスペースがあっても拾える。1回$0.002）
  const mr = await mcp.api('/v3/serp/google/maps/live/advanced', [{keyword: cfg.title, location_coordinate: cfg.center_xy + ',13z', language_code: 'ja', depth: cfg.limit}]);
  branches = (mr.tasks?.[0]?.result?.[0]?.items || []).filter(i => i.cid && (i.original_title || i.title || '').replace(/[\s　]/g, '').includes((cfg.title_must || cfg.title).replace(/[\s　]/g, '')) && (i.rating?.votes_count || 0) >= (cfg.min_votes ?? 10))
    .map(i => ({cid: i.cid, 店名: i.original_title || i.title, 住所: i.address, 緯度: i.latitude, 経度: i.longitude, 評価: i.rating?.value, 口コミ数: i.rating?.votes_count}));
} else {
  const lr = await mcp.api('/v3/business_data/business_listings/search/live', [{...(cfg.categories ? {categories: cfg.categories} : {}), title: cfg.title, location_coordinate: cfg.center, limit: cfg.limit,
    filters: [['rating.votes_count', '>=', cfg.min_votes ?? 10], 'and', ['address_info.country_code', '=', 'JP']], order_by: ['rating.votes_count,desc']}]);
  branches = (lr.tasks?.[0]?.result?.[0]?.items || []).filter(i => i.cid && (i.original_title || i.title || '').includes(cfg.title_must || cfg.title))
    .map(i => ({cid: i.cid, 店名: i.original_title || i.title, 住所: i.address, 緯度: i.latitude, 経度: i.longitude, 評価: i.rating?.value, 口コミ数: i.rating?.votes_count}));
}
// ② 口コミ（並列）
async function fetchAll(jobs) {
  const posted = [];
  for (const j of jobs) { const p = await mcp.api('/v3/business_data/google/reviews/task_post', [{cid: j.cid, location_code: 2392, language_code: 'ja', depth: j.depth, sort_by: j.sort}]); posted.push({...j, id: p.tasks?.[0]?.id, done: null}); }
  for (let round = 0; round < 80 && posted.some(p => p.id && !p.done); round++) { await sleep(3000);
    for (const p of posted.filter(p => p.id && !p.done)) { const g = await mcp.api(`/v3/business_data/google/reviews/task_get/${p.id}`, undefined, {method: 'GET'}); const t = g.tasks?.[0];
      if (t?.status_code === 20000) p.done = t.result?.[0] || {items: []}; else if (t && ![20100, 40601, 40602].includes(t.status_code)) p.done = {items: []}; } }
  return posted;
}
const jobs = branches.flatMap(b => [{cid: b.cid, sort: 'newest', depth: cfg.newest}, {cid: b.cid, sort: 'lowest_rating', depth: cfg.lowest}]);
let res = await fetchAll(jobs);
const empty = res.filter(r => !(r.done?.items?.length)); let retried = empty.length;
if (empty.length) { const again = await fetchAll(empty.map(e => ({cid: e.cid, sort: e.sort === 'newest' ? 'relevant' : e.sort, depth: e.depth}))); empty.forEach((e, i) => { if (again[i].done?.items?.length) e.done = again[i].done; }); }
// ③ 各支店の場所で検索したときの順位（その支店は、自分の場所で何位か）
const door = {};
for (const b of branches) {
  const d = await mcp.api('/v3/serp/google/maps/live/advanced', [{keyword: cfg.door_keyword, location_coordinate: `${b.緯度},${b.経度},15z`, language_code: 'ja', depth: 20}]);
  const it = d.tasks?.[0]?.result?.[0]?.items || []; const me = it.find(x => x.cid === b.cid);
  door[b.cid] = me ? me.rank_group : null;
}
// ④ 集計
const now = new Date('2026-11-27T00:00:00Z'), months = t => (now - new Date(t)) / (1000 * 60 * 60 * 24 * 30.4);
const re = Object.fromEntries(Object.entries(cfg.topics).map(([k, v]) => [k, new RegExp(v)]));
const table = branches.map(b => {
  const rv = res.filter(r => r.cid === b.cid).flatMap(r => (r.done?.items || []).map(x => ({via: r.sort, star: x.rating?.value, text: (x.review_text || '').trim(), time: x.timestamp, replied: !!x.owner_answer})));
  const seen = new Set(), u = rv.filter(x => { const k = x.time + x.text.slice(0, 20) + x.star; if (seen.has(k)) return false; seen.add(k); return true; });
  const nw = u.filter(x => x.via === 'newest'), low = u.filter(x => x.star <= 2);
  const last6 = nw.filter(x => months(x.time) <= 6).length;
  const topics = Object.fromEntries(Object.keys(re).map(k => [k, low.filter(x => re[k].test(x.text)).length]));
  return {...b, 順位_お店の場所: door[b.cid], 新しい順の件数: nw.length, 直近6か月の口コミ数: nw.length >= cfg.newest ? `${last6}（${cfg.newest}件中）` : last6, 星1と2の割合_新しい順: nw.length ? +(nw.filter(x => x.star <= 2).length / nw.length).toFixed(2) : null, 星1と2_返信率: low.length ? +(low.filter(x => x.replied).length / low.length).toFixed(2) : null, 星1と2の件数: low.length, 低評価の話題: topics, 低評価の本文: low.filter(x => x.text).map(x => x.text.replace(/\s+/g, ' ').slice(0, 140))};
});
fs.writeFileSync(path.join(out, cfg.name + '_board.json'), JSON.stringify({cfg, retried, cost: mcp.cost, 呼び出し: mcp.calls, table}, null, 1));
console.log('支店', branches.length, '費用', mcp.cost.toFixed(4), 'やり直し', retried);
for (const r of table) console.log(`${r.店名.slice(0, 18).padEnd(20)} 評価${r.評価} (${r.口コミ数}件) 場所で${r.順位_お店の場所 ?? '圏外'}位 6か月${r.直近6か月の口コミ数} 星1-2:${r.星1と2の割合_新しい順} 返信:${r.星1と2_返信率} 低評価${r.星1と2の件数}件`);
await mcp.close();
