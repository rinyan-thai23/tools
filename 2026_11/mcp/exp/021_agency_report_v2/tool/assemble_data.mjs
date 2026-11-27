// 5つの部品（地図・口コミ・競合の口コミ・サイトとのズレ・近所の料金）の結果を、1店ぶんの診断データに集める。費用0。
// 各欄に「状態」を付ける：自動（数字が取れた）／取れなかった（理由つき）。AIが読む文章は、このデータを見て書く。
import fs from 'node:fs';
const E = new URL('../../', import.meta.url).pathname;
const J = f => { try { return JSON.parse(fs.readFileSync(E + f, 'utf8')); } catch { return null; } };
const rev = (s, n) => ({取得件数: s.取得件数, 平均の星: s.平均の星, 星の分布: s.星の分布, 時期別: s.時期別の平均の星, 返信: s.返信.全体, 低評価への返信: s.返信.低評価_星1_2});
const comp = ['1482945000160954991', '2484419894226796327', '5534021639072604399', '9239448775594595470'].map(c => J(`015_competitor_review_reading/data/${c}_stats.json`)).filter(Boolean);
const prices = J('014_competitor_price_menu_compare/data/coverage_gym.json') && {note: '近所の料金は014の表（AIが読んだ5店）を参照'};
const shops = {
  A: {
    名前: 'A店（口コミ18件・星3.7）',
    地図: {状態: '自動', ...J('002_meo_agency_diagnosis_maker/sample_output/kokubunji_auto/diagnosis.json')},
    口コミ: {状態: '自動', ...rev(J('011_review_reading_report/data/newi_stats.json'))},
    競合の口コミ: {状態: '自動', 店数: 4},
    サイトとのズレ: {状態: '取れなかった', 理由: '公式サイトがなく、予約ポータルのページのみ（ポータルは規約確認が必要なので読まない）'},
    近所の料金: {状態: '一部だけ', 理由: 'この店の料金は取れない（ポータルのみ）。近所の競合5店の料金は取れた（014）'},
  },
  B: {
    名前: 'B店（口コミ113件・星4.9）',
    地図: {状態: '自動', ...J('002_meo_agency_diagnosis_maker/sample_output/ratio_auto/diagnosis.json')},
    口コミ: {状態: '自動', ...rev(J('015_competitor_review_reading/data/5534021639072604399_stats.json'))},
    サイトとのズレ: {状態: '自動', ...J('017_review_vs_website_gap/data/ratio_gap.json')},
    近所の料金: {状態: '自動', 自店: {カット: 7300, カラー: '7,590円〜', 縮毛矯正: 15300}, 近所の幅: {カット: '4,400〜7,700円', 縮毛矯正: '15,300〜35,200円'}},
  },
};
fs.writeFileSync(new URL('../data/report_data.json', import.meta.url), JSON.stringify({shops, 競合4店の平均: {直近6か月の口コミ数: comp.map(s => s.時期別の平均の星['直近6か月']?.件数)}}, null, 1));
const brief = s => Object.fromEntries(Object.entries(s).map(([k, v]) => [k, typeof v === 'object' && v ? (v.状態 ?? '') + (v.理由 ? '：' + v.理由 : '') : v]));
console.log(JSON.stringify({A: brief(shops.A), B: brief(shops.B)}, null, 1));
console.log('A 地図', JSON.stringify(shops.A.地図.counts), '中心', shops.A.地図.center_rank, '／ B 地図', JSON.stringify(shops.B.地図.counts), '中心', shops.B.地図.center_rank);
console.log('A 口コミ', JSON.stringify(shops.A.口コミ.時期別), '返信', shops.A.口コミ.返信);
console.log('B 口コミ', shops.B.口コミ.取得件数, shops.B.口コミ.平均の星, shops.B.口コミ.返信, JSON.stringify(shops.B.口コミ.時期別));
