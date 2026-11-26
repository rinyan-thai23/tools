// 取れた言葉を、関連語で絞り、表記ゆれ（空白・全角）をそろえて、グループごとに月間検索数を足す。費用0。
// 使い方：node cluster.mjs <_keywords.json> <出力.json>
import fs from 'node:fs';
const d = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const norm = k => (k || '').replace(/[\s　]+/g, '').toLowerCase();
const GROUPS = [  // 先に当たったグループに入れる
  ['確定申告・医療費控除・e-Tax', /確定申告|医療費控除|e-?tax|申告書|作成コーナー|ふるさと納税/],
  ['相続・贈与', /相続|贈与|遺産/],
  ['インボイス・消費税', /インボイス|適格請求書|消費税|消費\s*税/],
  ['個人事業・開業・経費', /個人事業|開業|青色|経費|フリーランス/],
  ['法人化・会社設立・決算', /法人化|法人成|会社設立|決算|法人税/],
  ['年末調整・源泉・給与', /年末調整|源泉|給与/],
  ['税理士を探す・比べる', /税理士|会計士|顧問/],
];
const rel = new RegExp(GROUPS.map(g => g[1].source).join('|'));
const seen = new Map();
for (const i of d.items) { const k = norm(i.keyword); if (!k || !rel.test(i.keyword)) continue; const cur = seen.get(k); if (!cur || i.volume > cur.volume) seen.set(k, i); }
const out = GROUPS.map(([name, re]) => ({name, items: []}));
for (const i of seen.values()) { const gi = GROUPS.findIndex(g => g[1].test(i.keyword)); out[gi].items.push(i); }
const res = out.map(g => ({グループ: g.name, 語数: g.items.length, 月間検索数の合計: g.items.reduce((s, x) => s + (x.volume || 0), 0), 代表: g.items.sort((a, b) => b.volume - a.volume).slice(0, 4).map(x => `${x.keyword}(${x.volume})`)}));
const stat = {取得語数: d.items.length, 関連語: [...seen.values()].length, 関連語の割合: +([...seen.values()].length / d.items.length).toFixed(2)};
fs.writeFileSync(process.argv[3], JSON.stringify({stat, res}, null, 1));
console.log(JSON.stringify({stat, res}, null, 1));
