// 近所の店のリストと公式サイトのアドレスを取る（business_listings/search・1回$0.012＋1件$0.00036）。
// 使い方：NODE_USE_ENV_PROXY=1 node list_shops.mjs <カテゴリ> <緯度,経度,半径km> <件数> <出力.json>
import fs from 'node:fs';
import {connect} from '../../../lib/mcp.mjs';
const [cat, center, limit, out] = [process.argv[2], process.argv[3], +process.argv[4], process.argv[5]];
const mcp = await connect();
const r = await mcp.api('/v3/business_data/business_listings/search/live', [{categories: [cat], location_coordinate: center, limit,
  filters: [['rating.value', '>=', 4], 'and', ['rating.votes_count', '>=', 20], 'and', ['address_info.country_code', '=', 'JP']], order_by: ['rating.votes_count,desc']}]);
const x = r.tasks?.[0]?.result?.[0];
const items = (x?.items || []).map(i => ({cid: i.cid, title: i.original_title || i.title, url: i.url, domain: i.domain, rating: i.rating?.value, votes: i.rating?.votes_count, price_level: i.price_level, address: i.address, phone: i.phone}));
fs.writeFileSync(out, JSON.stringify({total_count: x?.total_count, cost: r.cost, items}, null, 1));
console.log('総数', x?.total_count, '取得', items.length, '費用', r.cost, '／ サイトあり', items.filter(i => i.url).length);
await mcp.close();
