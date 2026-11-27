// 店の特定のテスト。曖昧なケース（チェーン・同名・名前だけ）と、ヒントで解決できるケースを比べる。
import fs from 'node:fs';
import {connect} from '../../../lib/mcp.mjs';
import {identifyShop} from '../../../lib/identify.mjs';
const cases = [
  {名前: '一意な名前（ヒントなし）', q: {query: 'newi国分寺'}},
  {名前: 'チェーン（ヒントなし）', q: {query: 'エニタイムフィットネス'}},
  {名前: 'チェーン＋住所のヒント', q: {query: 'エニタイムフィットネス 国分寺', address_hint: '国分寺'}},
  {名前: 'よくある名前（ヒントなし）', q: {query: 'ミント歯科'}},
  {名前: 'よくある名前＋住所のヒント', q: {query: 'ミント歯科 江古田', address_hint: '練馬'}},
];
const mcp = await connect(); const out = [];
for (const c of cases) {
  const r = await identifyShop(mcp, c.q);
  out.push({ケース: c.名前, 入力: c.q, 確信度: r.confidence, 理由: r.reason, 選ばれた店: r.shop?.original_title || r.shop?.title, 住所: r.shop?.address, 候補: r.candidates.map(x => `${x.点}点 ${x.店名}（${(x.住所 || '').slice(0, 24)}）`)});
}
fs.writeFileSync(new URL('../data/test_results.json', import.meta.url), JSON.stringify({cost: mcp.cost, out}, null, 1));
for (const o of out) console.log(`■ ${o.ケース}\n   → ${o.確信度}｜${o.理由}\n   選ばれた：${o.選ばれた店}｜${(o.住所 || '').slice(0, 30)}\n   候補：${o.候補.slice(0, 3).join(' ／ ')}`);
console.log('費用', mcp.cost.toFixed(4));
await mcp.close();
