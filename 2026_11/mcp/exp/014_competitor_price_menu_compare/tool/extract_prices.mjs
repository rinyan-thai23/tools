// サイトの文章から「メニュー名＋価格」を取り出す（費用0）。同じ行か、次の2行以内にある価格を、メニュー名と対応づける。
// 使い方：node extract_prices.mjs <shops.json> <sites_dir> <出力.json>
import fs from 'node:fs';
const [shopsF, dir, out] = process.argv.slice(2);
const shops = JSON.parse(fs.readFileSync(shopsF, 'utf8')).items;
const MENU = {
  'カット': /カット|CUT|Cut/, 'カラー': /カラー|COLOR|Color|白髪染め/, 'パーマ': /パーマ|PERM|Perm/,
  '縮毛矯正': /縮毛矯正|ストレート|STRAIGHT/, 'トリートメント': /トリートメント|TREATMENT|髪質改善/, 'ヘッドスパ': /ヘッドスパ|スパ|SPA/, 'ブリーチ': /ブリーチ|BLEACH/,
};
const PRICE = /[¥￥]\s?([0-9][0-9,]{2,6})|([0-9][0-9,]{2,6})\s?円/g;
const prices = s => [...s.matchAll(PRICE)].map(m => +(m[1] || m[2]).replace(/,/g, '')).filter(v => v >= 500 && v <= 80000);
const res = [];
for (const sh of shops) {
  const f = `${dir}/${sh.cid}.txt`; if (!fs.existsSync(f)) continue;
  const lines = fs.readFileSync(f, 'utf8').split('\n'); const found = {}, evid = {};
  lines.forEach((l, i) => {
    for (const [name, re] of Object.entries(MENU)) {
      if (!re.test(l)) continue;
      let p = prices(l);
      if (!p.length) for (const k of [1, 2]) { const nx = lines[i + k] || ''; if (Object.values(MENU).some(r => r.test(nx)) && k === 2) break; const q = prices(nx); if (q.length) { p = q; break; } }
      if (p.length) { const v = Math.min(...p); if (!(name in found) || v < found[name]) { found[name] = v; evid[name] = (l + ' ' + (lines[i + 1] || '')).slice(0, 70); } }
    }
  });
  res.push({店: sh.title, サイト: sh.domain, 価格表記の数: prices(lines.join('\n')).length, 取れたメニュー: found, 根拠の行: evid});
}
fs.writeFileSync(out, JSON.stringify(res, null, 1));
for (const r of res) console.log(r.店.slice(0, 16).padEnd(18), String(r.価格表記の数).padStart(3), JSON.stringify(r.取れたメニュー));
