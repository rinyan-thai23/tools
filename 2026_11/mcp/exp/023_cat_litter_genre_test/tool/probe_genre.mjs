// ジャンルの「取れる量」だけ測る。使い方：NODE_USE_ENV_PROXY=1 node probe_genre.mjs "<キーワード>" <出力名>
// Amazon商品検索 → Googleショッピング商品検索 → 口コミが多いものから最大3商品の口コミ（各40件）。費用の目安 約$0.01
import fs from 'node:fs'; import path from 'node:path';
import {connect} from '../../../lib/mcp.mjs';
const [kw, name] = [process.argv[2], process.argv[3] || 'genre'];
const out = path.resolve(path.dirname(process.argv[1]), '../data');
const m = await connect(); const sleep = ms => new Promise(r => setTimeout(r, ms));
const wait = async p => { for (let i = 0; i < 40; i++) { await sleep(3000); const g = await m.api(p, undefined, {method: 'GET'}); const t = g.tasks?.[0]; if (t?.status_code === 20000) return t.result?.[0]; if (t && ![20100, 40601, 40602].includes(t.status_code)) return null; } return null; };
// 1) Amazon
const a = await m.api('/v3/merchant/amazon/products/live/advanced', [{keyword: kw, location_code: 2392, language_code: 'ja_JP', depth: 100}]);
const ai = (a.tasks?.[0]?.result?.[0]?.items || []).filter(i => i.data_asin);
// 2) Google ショッピング
const p = await m.api('/v3/merchant/google/products/task_post', [{keyword: kw, location_code: 2392, language_code: 'ja', depth: 100}]);
const gr = await wait(`/v3/merchant/google/products/task_get/advanced/${p.tasks[0].id}`);
const gi = (gr?.items || []).filter(i => i.title);
const withG = gi.filter(i => i.gid), withVotes = gi.filter(i => i.product_rating?.votes_count > 0);
// 3) 口コミ（votes多い順に最大3商品）
const targets = withG.filter(i => i.product_rating?.votes_count > 0).sort((x, y) => y.product_rating.votes_count - x.product_rating.votes_count).slice(0, 3);
const revs = [];
for (const t of targets) { const rp = await m.api('/v3/merchant/google/reviews/task_post', [{gid: t.gid, location_code: 2392, language_code: 'ja', depth: 40}]);
  const r = rp.tasks?.[0]?.id ? await wait(`/v3/merchant/google/reviews/task_get/advanced/${rp.tasks[0].id}`) : null;
  revs.push({title: t.title, votes: t.product_rating.votes_count, got: r?.items?.length ?? 0, total: r?.reviews_count ?? null, sources: [...new Set((r?.items || []).map(x => x.provided_by))], items: r?.items || []}); }
fs.writeFileSync(path.join(out, name + '_raw.json'), JSON.stringify({kw, amazon: ai, google: gi, reviews: revs}));
const med = x => x.length ? x.sort((p, q) => p - q)[Math.floor(x.length / 2)] : null;
const sum = {キーワード: kw, 費用USD: +m.cost.toFixed(4),
  amazon: {商品数: ai.length, 販売数の目安あり: ai.filter(i => i.bought_past_month).length, 星の中央値: med(ai.map(i => i.rating?.value).filter(Boolean)), ベストセラー: ai.filter(i => i.is_best_seller).length, 価格の中央値: med(ai.map(i => i.price_from).filter(Boolean))},
  google: {商品数: gi.length, gidあり: withG.length, 口コミ数あり: withVotes.length, 口コミ合計: withVotes.reduce((s, i) => s + i.product_rating.votes_count, 0)},
  口コミ取得: revs.map(r => ({商品: r.title.slice(0, 28), 総数: r.total, 取れた: r.got, 提供元: r.sources}))};
fs.writeFileSync(path.join(out, name + '_summary.json'), JSON.stringify(sum, null, 1)); console.log(JSON.stringify(sum, null, 1)); await m.close();
