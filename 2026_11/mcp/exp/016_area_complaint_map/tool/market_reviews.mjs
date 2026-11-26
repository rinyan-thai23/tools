// 「業種×街」の口コミを、自動で集めて集計する（016）。人が手でやると回らない部分を、1コマンドにしたもの。
// 流れ：①総数の確認 ②小さなかたまりをランダムな位置から複数回取って店を選ぶ ③各店の口コミ（新しい順＋評価の低い順）を並列で取る
//       ④集計（星・本文なし・返信率・話題）⑤AIが読むための「読み取りパケット」を作る
// 使い方：NODE_USE_ENV_PROXY=1 node market_reviews.mjs <設定.json>
import fs from 'node:fs';
import path from 'node:path';
import {connect} from '../../../lib/mcp.mjs';
const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const out = path.resolve(path.dirname(process.argv[2]), '../data');
const mcp = await connect(); const sleep = ms => new Promise(r => setTimeout(r, ms));
let s = (cfg.seed ?? Date.now()) >>> 0; const rnd = () => { s = (s + 0x6D2B79F5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
const filters = [['rating.value', '>=', cfg.min_rating ?? 4], 'and', ['rating.votes_count', '>=', cfg.min_votes ?? 10], 'and', ['address_info.country_code', '=', 'JP']];
const base = {categories: cfg.categories, location_coordinate: cfg.center, filters, order_by: ['rating.votes_count,desc']};
const log = {設定: cfg, 手順: []}; const t0 = Date.now();
const probe = await mcp.api('/v3/business_data/business_listings/search/live', [{...base, limit: 1}]);
const total = probe.tasks?.[0]?.result?.[0]?.total_count || 0; log.手順.push({内容: '総数', total});
// ② 小さなかたまり×複数回（人気の似た店ばかりになるのを避ける）
const used = new Set(), shops = [], offsets = [];
for (let b = 0; b < cfg.blocks; b++) {
  const off = Math.floor(rnd() * Math.max(1, Math.min(total, 10000) - cfg.block_size)); offsets.push(off);
  const r = await mcp.api('/v3/business_data/business_listings/search/live', [{...base, limit: cfg.block_size, offset: off}]);
  for (const it of r.tasks?.[0]?.result?.[0]?.items || []) if (it.cid && !used.has(it.cid)) { used.add(it.cid); shops.push({cid: it.cid, title: it.original_title || it.title, address: it.address, rating: it.rating?.value, votes: it.rating?.votes_count}); }
}
log.手順.push({内容: '店の選定', offsets, 店数: shops.length});
// ③ 口コミ（並列）
async function fetchAll(jobs) {
  const posted = [];
  for (const j of jobs) { const p = await mcp.api('/v3/business_data/google/reviews/task_post', [{cid: j.cid, location_code: 2392, language_code: 'ja', depth: j.depth, sort_by: j.sort}]); posted.push({...j, id: p.tasks?.[0]?.id, done: null}); }
  for (let round = 0; round < 80 && posted.some(p => p.id && !p.done); round++) {
    await sleep(3000);
    for (const p of posted.filter(p => p.id && !p.done)) { const g = await mcp.api(`/v3/business_data/google/reviews/task_get/${p.id}`, undefined, {method: 'GET'}); const t = g.tasks?.[0];
      if (t?.status_code === 20000) p.done = t.result?.[0] || {items: []}; else if (t && ![20100, 40601, 40602].includes(t.status_code)) p.done = {items: []}; }
  }
  return posted;
}
const jobs = shops.flatMap(sh => [{cid: sh.cid, sort: 'newest', depth: cfg.newest}, {cid: sh.cid, sort: 'lowest_rating', depth: cfg.lowest}]);
const res = await fetchAll(jobs);
let retried = 0; const empty = res.filter(r => !(r.done?.items?.length)); // 0件で返ったものは、並び順を変えてやり直す
if (empty.length) { retried = empty.length; const again = await fetchAll(empty.map(e => ({cid: e.cid, sort: e.sort === 'newest' ? 'relevant' : e.sort, depth: e.depth}))); empty.forEach((e, i) => { if (again[i].done?.items?.length) e.done = again[i].done; }); }
const rv = [];
for (const r of res) { const sh = shops.find(x => x.cid === r.cid); for (const x of r.done?.items || []) rv.push({cid: r.cid, shop: sh.title, via: r.sort, star: x.rating?.value, text: (x.review_text || '').trim(), time: x.timestamp, replied: !!x.owner_answer}); }
// 重複（同じ口コミが新しい順と低い順の両方に出る）を除く
const seen = new Set(), uniq = []; for (const x of rv) { const k = x.cid + '|' + x.time + '|' + x.text.slice(0, 30) + '|' + x.star; if (!seen.has(k)) { seen.add(k); uniq.push(x); } }
fs.writeFileSync(path.join(out, cfg.name + '_reviews.json'), JSON.stringify({shops, reviews: uniq}));
// ④ 集計
const TOP = cfg.topics; const re = Object.fromEntries(Object.entries(TOP).map(([k, v]) => [k, new RegExp(v)]));
const newest = uniq.filter(x => x.via === 'newest'); const low = uniq.filter(x => x.star <= 2), hi = uniq.filter(x => x.star >= 4);
const lowT = low.filter(x => x.text), hiT = hi.filter(x => x.text);
const share = (arr, r) => arr.length ? +(arr.filter(x => r.test(x.text)).length / arr.length).toFixed(2) : null;
const stats = {
  店数: shops.length, 口コミ件数: uniq.length, 費用: +mcp.cost.toFixed(4), 呼び出し: mcp.calls, やり直し: retried, 秒: Math.round((Date.now() - t0) / 1000),
  新しい順だけで見た星の分布: Object.fromEntries([1, 2, 3, 4, 5].map(n => [n, newest.filter(x => x.star === n).length])),
  新しい順_星1と2の割合: newest.length ? +(newest.filter(x => x.star <= 2).length / newest.length).toFixed(3) : null,
  新しい順_本文なしの割合: newest.length ? +(newest.filter(x => !x.text).length / newest.length).toFixed(2) : null,
  星1と2_件数: low.length, 星1と2_本文あり: lowT.length, 星1と2_返信率: low.length ? +(low.filter(x => x.replied).length / low.length).toFixed(2) : null,
  話題の割合: Object.fromEntries(Object.keys(re).map(k => [k, {星1と2の本文: share(lowT, re[k]), 星4と5の本文: share(hiT, re[k])}])),
  店ごとの星1と2の割合_新しい順: Object.fromEntries(shops.map(sh => { const n = newest.filter(x => x.cid === sh.cid); return [sh.title.slice(0, 14), n.length ? +(n.filter(x => x.star <= 2).length / n.length).toFixed(2) : null]; })),
};
fs.writeFileSync(path.join(out, cfg.name + '_stats.json'), JSON.stringify(stats, null, 1));
// ⑤ 読み取りパケット（AIがここを読んで、不満・期待の型をまとめる）
const pick = (arr, n) => { const a = [...arr]; const o = []; while (o.length < n && a.length) o.push(a.splice(Math.floor(rnd() * a.length), 1)[0]); return o; };
const lowSamp = pick(lowT.filter(x => x.text.length >= 30), cfg.read_low ?? 50), hiSamp = pick(hiT.filter(x => x.text.length >= 30), cfg.read_high ?? 20);
const fmt = x => `[星${x.star}] ${x.text.replace(/\s+/g, ' ').slice(0, 170)}`;
fs.writeFileSync(path.join(out, cfg.name + '_reading_packet.md'), `# 読み取りパケット（${cfg.name}）\n\n## 星1〜2（${lowSamp.length}件を無作為に抽出／全${lowT.length}件）\n${lowSamp.map(fmt).join('\n')}\n\n## 星4〜5（${hiSamp.length}件を無作為に抽出／全${hiT.length}件）\n${hiSamp.map(fmt).join('\n')}\n`);
console.log(JSON.stringify({...stats, 店ごとの星1と2の割合_新しい順: undefined}, null, 1));
await mcp.close();
