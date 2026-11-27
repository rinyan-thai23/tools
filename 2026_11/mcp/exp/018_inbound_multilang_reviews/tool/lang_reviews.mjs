// インバウンド：外国語の口コミが、どれくらいあるか。言語別の件数・星・話題を集計する。
// 流れ：①地図検索で、観光地の店を選ぶ（口コミ数が多い順）②各店の口コミ（新しい順N件・言語つき）③言語別に集計
// 使い方：NODE_USE_ENV_PROXY=1 node lang_reviews.mjs <設定.json>
import fs from 'node:fs';
import path from 'node:path';
import {connect} from '../../../lib/mcp.mjs';
const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const out = path.resolve(path.dirname(process.argv[2]), '../data');
const mcp = await connect(); const sleep = ms => new Promise(r => setTimeout(r, ms));
const mr = await mcp.api('/v3/serp/google/maps/live/advanced', [{keyword: cfg.keyword, location_coordinate: cfg.center + ',15z', language_code: 'ja', depth: 20}]);
const shops = (mr.tasks?.[0]?.result?.[0]?.items || []).filter(i => i.cid && (i.rating?.votes_count || 0) >= cfg.min_votes).sort((a, b) => b.rating.votes_count - a.rating.votes_count).slice(0, cfg.pick)
  .map(i => ({cid: i.cid, 店名: i.original_title || i.title, 評価: i.rating?.value, 口コミ数: i.rating?.votes_count, 住所: i.address}));
const posted = [];
for (const s of shops) { const p = await mcp.api('/v3/business_data/google/reviews/task_post', [{cid: s.cid, location_code: 2392, language_code: cfg.review_language || 'ja', depth: cfg.depth, sort_by: 'newest'}]); posted.push({s, id: p.tasks?.[0]?.id, done: null}); }
for (let r = 0; r < 80 && posted.some(p => p.id && !p.done); r++) { await sleep(3000);
  for (const p of posted.filter(p => p.id && !p.done)) { const g = await mcp.api(`/v3/business_data/google/reviews/task_get/${p.id}`, undefined, {method: 'GET'}); const t = g.tasks?.[0];
    if (t?.status_code === 20000) p.done = t.result?.[0] || {items: []}; else if (t && ![20100, 40601, 40602].includes(t.status_code)) p.done = {items: []}; } }
const all = [];
for (const p of posted) for (const x of p.done?.items || []) all.push({shop: p.s.店名, lang: x.original_language || '不明', star: x.rating?.value, text: (x.review_text || '').trim(), original: (x.original_review_text || '').trim(), time: x.timestamp, replied: !!x.owner_answer});
fs.writeFileSync(path.join(out, cfg.name + '_reviews.json'), JSON.stringify({shops, reviews: all}));
const by = {}; for (const r of all) { (by[r.lang] ||= []).push(r); }
const avg = a => a.length ? +(a.reduce((s, x) => s + x.star, 0) / a.length).toFixed(2) : null;
const summary = {店数: shops.length, 口コミ件数: all.length, 費用: +mcp.cost.toFixed(4), 言語別: Object.entries(by).sort((a, b) => b[1].length - a[1].length).map(([l, a]) => ({言語: l, 件数: a.length, 割合: +(a.length / all.length).toFixed(2), 平均の星: avg(a), 本文あり: a.filter(x => x.text || x.original).length}))};
fs.writeFileSync(path.join(out, cfg.name + '_summary.json'), JSON.stringify(summary, null, 1));
console.log(shops.map(s => `${s.店名.slice(0, 16)}｜評価${s.評価}（${s.口コミ数}件）`).join('\n'));
console.log(JSON.stringify(summary, null, 1));
await mcp.close();
