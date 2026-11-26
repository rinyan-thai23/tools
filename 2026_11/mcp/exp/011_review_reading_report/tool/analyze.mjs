// 口コミの集計（お金がかからない部分）。星の分布・時期別の平均・返信率・話題（キーワードの数え方は下に書いた通り）。
// 文章の読み取り（話題のまとめ・返信の下書き）は、このあとAI（Claude）が口コミ本文を読んで行う。
// 使い方：node analyze.mjs <取得ファイル.json> <出力.json>
import fs from 'node:fs';
const raw = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const items = raw.result.tasks[0].result[0].items;
const now = new Date('2026-11-26T00:00:00Z');
const months = i => (now - new Date(i.timestamp)) / (1000 * 60 * 60 * 24 * 30.4);
const avg = a => a.length ? +(a.reduce((s, x) => s + x, 0) / a.length).toFixed(2) : null;
const star = i => i.rating?.value;
const bucket = m => m <= 6 ? '直近6か月' : m <= 12 ? '6か月〜1年' : m <= 24 ? '1〜2年' : '2年より前';
const periods = {};
for (const i of items) { const b = bucket(months(i)); (periods[b] ||= []).push(star(i)); }
const TOPICS = {  // キーワードで数える（1件が複数の話題に入ることがある）
  '費用・自費診療の勧め': /自費|自由診療|セラミック|ジルコニア|高額|万円|保険|料金|値段|お金/,
  '痛み・処置の腕': /痛|麻酔|抜歯|根管|削|仕上が|下手|切られ|バサバサ|カット/,
  '受付・接客・説明': /受付|対応|態度|説明|不親切|高圧|不快|スタッフ|接客|丁寧|優しい/,
  '予約・時間・会計': /予約|待た|遅れ|時間|支払|会計|キャンセル/,
  '清潔・内装・個室': /綺麗|きれい|清潔|個室|半個室|店内|雰囲気/,
};
const topics = {};
for (const [k, re] of Object.entries(TOPICS)) {
  const hit = items.filter(i => re.test(i.review_text || ''));
  topics[k] = {全体: hit.length, 低評価_星1_2: hit.filter(i => star(i) <= 2).length, 高評価_星4_5: hit.filter(i => star(i) >= 4).length};
}
const low = items.filter(i => star(i) <= 2);
const out = {
  取得件数: items.length, 平均の星: avg(items.map(star)),
  星の分布: Object.fromEntries([1, 2, 3, 4, 5].map(n => [n + '星', items.filter(i => star(i) === n).length])),
  本文なし: items.filter(i => !(i.review_text || '').trim()).length,
  時期別の平均の星: Object.fromEntries(Object.entries(periods).map(([k, v]) => [k, {件数: v.length, 平均: avg(v)}])),
  返信: {全体: items.filter(i => i.owner_answer).length + '/' + items.length, 低評価_星1_2: low.filter(i => i.owner_answer).length + '/' + low.length,
    未返信の低評価: low.filter(i => !i.owner_answer).map(i => ({星: star(i), いつ: i.time_ago, 本文あり: !!(i.review_text || '').trim()}))},
  話題: topics,
  注意: '話題はキーワードで数えた目安。1件が複数の話題に入る。'
};
fs.writeFileSync(process.argv[3], JSON.stringify(out, null, 1));
console.log(JSON.stringify(out, null, 1));
