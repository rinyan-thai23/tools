// 総数の確認だけ（limit=1・約$0.012/回）。カテゴリ名や地域の候補を比べる。
import {connect} from '../../../lib/mcp.mjs';
const [cats, center] = [process.argv[2].split(','), process.argv[3]];
const mcp = await connect();
const r = await mcp.api('/v3/business_data/business_listings/search/live', [{categories: cats, location_coordinate: center, filters: [['rating.value', '>=', 4], 'and', ['rating.votes_count', '>=', 10]], limit: 1}]);
const t = r.tasks?.[0], x = t?.result?.[0];
console.log(cats.join('+'), center, '→', t?.status_code, t?.status_message, '総数', x?.total_count, '費用', r.cost, JSON.stringify(x?.items?.[0] || {}).slice(0, 600));
await mcp.close();
