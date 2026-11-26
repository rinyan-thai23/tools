// 複数の店の口コミを、まとめて取る（Google Reviews・非同期）。0件で返ったら、並び順を変えてやり直す。
// 使い方：NODE_USE_ENV_PROXY=1 node fetch_many.mjs <店リスト.json> <1店あたりの件数> <出力フォルダ>
// 料金：10件あたり約$0.00075（0件で返っても請求される）
import fs from 'node:fs';
import path from 'node:path';
import {connect} from '../../../lib/mcp.mjs';
const [listFile, depth, outDir] = [process.argv[2], +process.argv[3] || 100, process.argv[4]];
fs.mkdirSync(outDir, {recursive: true});
const shops = JSON.parse(fs.readFileSync(listFile, 'utf8'));
const mcp = await connect();
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function one(shop, sort) {
  const post = await mcp.api('/v3/business_data/google/reviews/task_post', [{cid: shop.cid, location_code: 2392, language_code: 'ja', depth, sort_by: sort}]);
  const id = post.tasks?.[0]?.id; if (!id) return null;
  for (let i = 0; i < 45; i++) {
    await sleep(4000);
    const r = await mcp.api(`/v3/business_data/google/reviews/task_get/${id}`, undefined, {method: 'GET'});
    const t = r.tasks?.[0];
    if (t?.status_code === 20000) return {id, sort, res: r};
    if (t && ![20100, 40601, 40602].includes(t.status_code)) return {id, sort, res: r};
  }
  return null;
}
const log = [];
for (const shop of shops) {
  let got = null;
  for (const sort of ['newest', 'relevant']) {
    const r = await one(shop, sort);
    const n = r?.res?.tasks?.[0]?.result?.[0]?.items_count || 0;
    log.push({店: shop.title, 並び順: sort, 件数: n});
    if (n > 0) { got = r; break; }
  }
  if (got) fs.writeFileSync(path.join(outDir, shop.cid + '_raw.json'), JSON.stringify({shop, sort: got.sort, depth, result: got.res}));
}
console.log(JSON.stringify(log, null, 1), '\n費用の合計', mcp.cost.toFixed(4), '／呼び出し', mcp.calls);
await mcp.close();
