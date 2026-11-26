// 013：士業（例：税理士）のお客さんが「探している言葉」を集めて、月間検索数つきで並べる。
// 使い方：NODE_USE_ENV_PROXY=1 node keyword_map.mjs <設定.json>
// 費用の目安：Labs keyword_ideas は 1回 $0.01 ＋ 1件あたり 約$0.0001（実測で確認）
import fs from 'node:fs';
import path from 'node:path';
import {connect} from '../../../lib/mcp.mjs';
const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const out = path.resolve(path.dirname(process.argv[2]), '../data');
const mcp = await connect();
const r = await mcp.api('/v3/dataforseo_labs/google/keyword_ideas/live', [{keywords: cfg.seeds, location_code: 2392, language_code: 'ja', limit: cfg.limit || 300,
  filters: [['keyword_info.search_volume', '>=', cfg.min_volume || 50]], order_by: ['keyword_info.search_volume,desc']}]);
const t = r.tasks?.[0], x = t?.result?.[0];
fs.writeFileSync(path.join(out, cfg.name + '_raw.json'), JSON.stringify(r)); // 生データを先に保存（取り出し方を間違えても、お金を無駄にしない）
const g = i => i.keyword_data || i;
const items = (x?.items || []).map(i => ({keyword: g(i).keyword, volume: g(i).keyword_info?.search_volume, cpc: g(i).keyword_info?.cpc, competition: g(i).keyword_info?.competition_level, intent: g(i).search_intent_info?.main_intent}));
fs.writeFileSync(path.join(out, cfg.name + '_keywords.json'), JSON.stringify({seeds: cfg.seeds, total_count: x?.total_count, cost: r.cost, items}));
console.log(JSON.stringify({status: t?.status_code, message: t?.status_message, total_count: x?.total_count, 取得: items.length, 費用: r.cost, 先頭: items.slice(0, 5)}, null, 1));
await mcp.close();
