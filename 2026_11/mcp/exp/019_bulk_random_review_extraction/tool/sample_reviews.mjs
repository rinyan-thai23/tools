// 小さな実測：地域×業種から、店を準無作為に選び、各店の口コミを取る。
// 使い方：NODE_USE_ENV_PROXY=1 node sample_reviews.mjs <設定.json>
// 設定例：{"name":"tokyo_dentist","categories":["dentist"],"center":"35.68,139.76,20","min_votes":10,"pool":30,"pick":10,"per_shop":10,"seed":7}
// 費用：総数確認 $0.012／回 ＋ 店リスト $0.012+$0.00036×件 ＋ 口コミ $0.00075×(件数/10)×店数
import fs from 'node:fs';
import path from 'node:path';
import {connect} from '../../../lib/mcp.mjs';
const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const out = path.resolve(path.dirname(process.argv[2]), '../data');
const mcp = await connect();
const sleep = ms => new Promise(r => setTimeout(r, ms));
// 乱数（シード固定で再現できる）
// mulberry32（初期値が小さくても偏らない乱数）。最初の版は線形合同法で、シード7だと最初の値が0に近く、offsetが0になった（バグ）
let s = (cfg.seed || 1) >>> 0; const rnd = () => { s = (s + 0x6D2B79F5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
const log = {設定: cfg, 手順: []};
const filters = [['rating.value', '>=', 4], 'and', ['rating.votes_count', '>=', cfg.min_votes || 10]];
const base = {categories: cfg.categories, location_coordinate: cfg.center, filters, order_by: ['rating.votes_count,desc']};
const t0 = Date.now();
// 1. 総数の確認（limit=1）
const probe = await mcp.api('/v3/business_data/business_listings/search/live', [{...base, limit: 1}]);
const pr = probe.tasks?.[0]?.result?.[0];
log.手順.push({内容: '総数の確認', status: probe.tasks?.[0]?.status_code, total_count: pr?.total_count, items_count: pr?.items_count, 費用: probe.cost});
const total = pr?.total_count || 0;
if (!total) { console.log(JSON.stringify(log, null, 1)); fs.writeFileSync(path.join(out, cfg.name + '_log.json'), JSON.stringify(log, null, 1)); await mcp.close(); process.exit(0); }
// 2. ランダムな位置から店を取る
const maxOff = Math.max(0, Math.min(total, 10000) - cfg.pool);
const offset = Math.floor(rnd() * (maxOff + 1));
const lst = await mcp.api('/v3/business_data/business_listings/search/live', [{...base, limit: cfg.pool, offset}]);
const items = lst.tasks?.[0]?.result?.[0]?.items || [];
log.手順.push({内容: '店リスト', offset, 取得件数: items.length, 費用: lst.cost, 総数: total});
fs.writeFileSync(path.join(out, cfg.name + '_listing_raw.json'), JSON.stringify({offset, total, items}));
// 3. 間引き（ランダムに pick 店）
const pool = items.filter(i => i.cid || i.place_id);
const picked = []; while (picked.length < Math.min(cfg.pick, pool.length)) { const k = Math.floor(rnd() * pool.length); picked.push(pool.splice(k, 1)[0]); }
// 4. 口コミ（全店の依頼を先に出して、まとめて結果を待つ＝並列）
const t1 = Date.now();
const posted = [];
for (const it of picked) {
  const post = await mcp.api('/v3/business_data/google/reviews/task_post', [{cid: it.cid, location_code: 2392, language_code: 'ja', depth: cfg.per_shop, sort_by: 'newest'}]);
  posted.push({it, id: post.tasks?.[0]?.id, done: null, secs: null});
}
for (let round = 0; round < 60 && posted.some(p => p.id && !p.done); round++) {
  await sleep(3000);
  for (const p of posted.filter(p => p.id && !p.done)) {
    const g = await mcp.api(`/v3/business_data/google/reviews/task_get/${p.id}`, undefined, {method: 'GET'}); const t = g.tasks?.[0];
    if (t?.status_code === 20000) { p.done = t.result?.[0] || {items: []}; p.secs = Math.round((Date.now() - t1) / 1000); }
    else if (t && ![20100, 40601, 40602].includes(t.status_code)) { p.done = {items: []}; p.secs = Math.round((Date.now() - t1) / 1000); }
  }
}
const shops = posted.map(p => { const rv = p.done?.items || []; const it = p.it;
  return {店: it.title, cid: it.cid, 住所: it.address, 評価: it.rating?.value, 口コミ総数: it.rating?.votes_count, 取得件数: rv.length, 秒: p.secs, reviews: rv.map(x => ({star: x.rating?.value, text: x.review_text, time: x.timestamp, replied: !!x.owner_answer}))}; });
const all = shops.flatMap(x => x.reviews);
log.手順.push({内容: '口コミ取得（並列）', 店数: shops.length, 全店がそろうまでの秒: Math.max(...shops.map(x => x.秒 || 0)), 取得件数: all.length, 失敗した店: shops.filter(x => !x.取得件数).length});
log.集計 = {口コミ件数: all.length, 本文なし割合: all.length ? +(all.filter(x => !(x.text || '').trim()).length / all.length).toFixed(2) : null, 星4以上の割合: all.length ? +(all.filter(x => x.star >= 4).length / all.length).toFixed(2) : null, 店ごとの秒: shops.map(x => x.秒)};
log.費用の合計 = +mcp.cost.toFixed(4); log.呼び出し回数 = mcp.calls; log.かかった秒 = Math.round((Date.now() - t0) / 1000);
fs.writeFileSync(path.join(out, cfg.name + '_sample.json'), JSON.stringify({shops}));
fs.writeFileSync(path.join(out, cfg.name + '_log.json'), JSON.stringify(log, null, 1));
console.log(JSON.stringify({...log, 設定: undefined}, null, 1));
await mcp.close();
