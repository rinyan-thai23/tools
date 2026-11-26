// 口コミを取る（Google Reviews・非同期）。依頼(task_post)→結果(task_get)の2段。料金は「10件ごと」。
// 使い方：NODE_USE_ENV_PROXY=1 node fetch_reviews.mjs <cid> <件数> <出力ファイル> [newest|lowest_rating|highest_rating|relevant]
import fs from 'node:fs';
import {connect} from '../../../lib/mcp.mjs';
const [cid, depth, out, sort = 'newest'] = [process.argv[2], +process.argv[3] || 20, process.argv[4], process.argv[5]];
const mcp = await connect();
const post = await mcp.api('/v3/business_data/google/reviews/task_post', [{cid, location_code: 2392, language_code: 'ja', depth, sort_by: sort}]);
const tk = post.tasks?.[0];
if (tk?.status_code !== 20100) { console.error('依頼に失敗', tk?.status_code, tk?.status_message); await mcp.close(); process.exit(1); }
const id = tk.id; console.log('依頼完了 id', id, '費用', post.cost);
let res;
for (let i = 0; i < 40; i++) {
  await new Promise(r => setTimeout(r, 4000));
  res = await mcp.api(`/v3/business_data/google/reviews/task_get/${id}`, undefined, {method: 'GET'});
  const t = res.tasks?.[0];
  if (t?.status_code === 20000) break;
  if (t && t.status_code !== 40602) { console.log('状態', t.status_code, t.status_message); if (![20100, 40601, 40602].includes(t.status_code)) break; }
}
const r = res?.tasks?.[0]?.result?.[0];
console.log('取得件数', r?.items_count, '／全体の口コミ数', r?.reviews_count, '／評価', r?.rating?.value, '／費用の合計', mcp.cost);
fs.writeFileSync(out, JSON.stringify({cid, sort, depth, cost: mcp.cost, task_id: id, result: res}, null, 1));
await mcp.close();
