// 業種ごとの「料金が取れた店の割合」を数える（費用0）。料金表記＝¥・円つきの数字（業種ごとの妥当な範囲）で3つ以上。
// 使い方：node coverage.mjs <店リスト.json> <サイトのフォルダ> <最小金額> <最大金額>
import fs from 'node:fs';
const [shopsF, dir, lo, hi] = [process.argv[2], process.argv[3], +process.argv[4], +process.argv[5]];
const shops = JSON.parse(fs.readFileSync(shopsF, 'utf8')).items;
const PRICE = /[¥￥]\s?([0-9][0-9,]{2,6})|([0-9][0-9,]{2,6})\s?円/g;
let withUrl = 0, got = 0, rendered = 0, rows = [];
for (const sh of shops) {
  if (!sh.url) continue; withUrl++;
  const f = `${dir}/${sh.cid}.txt`; if (!fs.existsSync(f)) { rows.push({店: sh.title, 文字: null, 価格表記: null}); continue; }
  const t = fs.readFileSync(f, 'utf8'); rendered++;
  const n = [...t.matchAll(PRICE)].map(m => +(m[1] || m[2]).replace(/,/g, '')).filter(v => v >= lo && v <= hi).length;
  if (n >= 3) got++;
  rows.push({店: sh.title.slice(0, 20), サイト: sh.domain, 文字: t.length, 価格表記: n});
}
console.log(JSON.stringify({店数: shops.length, サイトあり: withUrl, 表示できた: rendered, 料金が取れた: got, 割合_サイトあり中: +(got / withUrl).toFixed(2), 割合_全体中: +(got / shops.length).toFixed(2)}));
fs.writeFileSync(process.argv[5 + 1] || '/dev/null', JSON.stringify(rows, null, 1));
