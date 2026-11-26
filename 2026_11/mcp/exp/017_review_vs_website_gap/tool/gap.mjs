// 口コミ（お客さんの言葉）と、サイト（お店の言葉）のズレを集計する。費用0。
// 使い方：node gap.mjs <口コミ原本.json(015形式)> <サイト文章.txt> <出力.json>
// 出力：話題ごとに「高評価の口コミで出る割合」「サイトに出る回数」→ ズレの種類
import fs from 'node:fs';
const TOPICS = {
  'カウンセリング・相談': /カウンセリング|ヒアリング|相談|悩み/,
  '希望を汲み取る・イメージ通り': /汲み|イメージ|希望|要望|理想/,
  '似合わせ・提案': /似合|提案|アドバイス/,
  'カットの技術': /カット|切って|上手|技術|うまい/,
  '髪質改善・縮毛矯正': /髪質改善|縮毛|トリートメント|ツヤ|うねり|クセ/,
  'カラー・白髪': /カラー|ブリーチ|白髪/,
  'ショート・ボブ': /ショート|ボブ/,
  '丁寧・安心・親切': /丁寧|安心|親切|優しい|気遣い/,
  '話しやすい・居心地': /話しやすい|雰囲気|居心地|落ち着|リラックス|気さく/,
  'マンツーマン・1対1': /マンツーマン|1対1|一対一|プライベート/,
  '個室・半個室': /個室/,
  '清潔・きれい': /清潔|綺麗|きれい/,
  '駅近・通いやすさ': /駅|アクセス|通いやすい|立地/,
  '予約の取りやすさ・当日': /当日|急(な|に)|取りやすい|予約が取れ/,
  '料金・コスパ': /料金|価格|値段|お得|リーズナブル|コスパ|安い/,
  'リピート・長く通う': /通って|リピート|長年|毎回|ずっと|年以上/,
};
const items = JSON.parse(fs.readFileSync(process.argv[2], 'utf8')).result.tasks[0].result[0].items;
const hi = items.filter(i => i.rating?.value >= 4 && (i.review_text || '').trim().length >= 10);
const hp = fs.readFileSync(process.argv[3], 'utf8');
const rows = Object.entries(TOPICS).map(([k, re]) => {
  const gre = new RegExp(re.source, 'g');
  const rs = hi.filter(i => re.test(i.review_text)).length / hi.length;
  const hc = (hp.match(gre) || []).length;
  const kind = rs >= 0.15 && hc === 0 ? '口コミで多いのに、サイトに無い' : rs >= 0.15 && hc <= 2 ? '口コミで多いが、サイトでは薄い' : rs < 0.04 && hc >= 3 ? 'サイトで推しているが、口コミに出ない' : '';
  return {話題: k, 口コミで出る割合: +rs.toFixed(2), サイトに出る回数: hc, ズレ: kind};
});
const out = {高評価の本文件数: hi.length, サイトの文字数: hp.length, 話題別: rows, ズレだけ: rows.filter(r => r.ズレ)};
fs.writeFileSync(process.argv[4], JSON.stringify(out, null, 1));
console.log(JSON.stringify({高評価の本文: hi.length, サイト文字数: hp.length, ズレだけ: out.ズレだけ}, null, 1));
