// 比較ボードの表（HTML）を、集計データから作る。支店は記号（A〜）に伏せる。注意の印は、ルールで付ける（ルールは下に書いた通り）。
import fs from 'node:fs';
const d = JSON.parse(fs.readFileSync(new URL('../data/anytime_west_tokyo_board.json', import.meta.url), 'utf8'));
const T = d.table.map(r => {
  const last6 = parseInt(String(r.直近6か月の口コミ数), 10);   // 「4（30件中）」＝最新30件のうち、6か月以内が4件。30なら「30件以上」（最新30件がすべて6か月以内）
  const flags = [];
  if (r.評価 < 3.9) flags.push('評価が低い（3.9未満）');
  if (r.星1と2の割合_新しい順 >= 0.2) flags.push('星1〜2が2割以上');
  if (r.星1と2の件数 >= 3 && (r.星1と2_返信率 ?? 1) < 0.5) flags.push('低評価への返信が半分未満');
  if (r.順位_お店の場所 == null || r.順位_お店の場所 >= 7) flags.push('お店の場所でも7位以下');
  if (last6 <= 7) flags.push('口コミが増えるのが遅い（6か月で7件以下）');
  return {...r, last6, flags};
}).sort((a, b) => b.flags.length - a.flags.length || a.評価 - b.評価);
const L = i => String.fromCharCode(65 + i);
const cls = (bad) => bad ? ' class="bad"' : '';
const rows = T.map((r, i) => `<tr><td><b>${L(i)}</b></td><td class="n"${cls(r.評価 < 3.9)}>${r.評価}<span class="m">（${r.口コミ数}件）</span></td><td class="n"${cls(r.順位_お店の場所 == null || r.順位_お店の場所 >= 7)}>${r.順位_お店の場所 ?? '圏外'}位</td><td class="n"${cls(r.last6 <= 7)}>${r.last6 >= 30 ? '30件以上' : r.last6 + '件'}</td><td class="n"${cls(r.星1と2の割合_新しい順 >= 0.2)}>${Math.round(r.星1と2の割合_新しい順 * 100)}%</td><td class="n"${cls(r.星1と2の件数 >= 3 && (r.星1と2_返信率 ?? 1) < 0.5)}>${r.星1と2_返信率 == null ? '—' : Math.round(r.星1と2_返信率 * 100) + '%'}<span class="m">（${r.星1と2の件数}件中）</span></td><td class="n"><b>${r.flags.length}</b></td></tr>`).join('');
fs.writeFileSync(new URL('../data/table_rows.html', import.meta.url), rows);
fs.writeFileSync(new URL('../data/board_ranked.json', import.meta.url), JSON.stringify(T.map((r, i) => ({記号: L(i), 店名: r.店名, 評価: r.評価, 口コミ数: r.口コミ数, 場所での順位: r.順位_お店の場所, 直近6か月: r.直近6か月の口コミ数, 星1と2の割合: r.星1と2の割合_新しい順, 低評価への返信率: r.星1と2_返信率, 低評価件数: r.星1と2の件数, 注意の印: r.flags})), null, 1));
console.log(T.slice(0, 8).map((r, i) => `${L(i)} ${r.店名.slice(10, 22)} 印${r.flags.length}: ${r.flags.join('／')}`).join('\n'));
console.log('印が0の支店', T.filter(r => !r.flags.length).length, '／', T.length);
