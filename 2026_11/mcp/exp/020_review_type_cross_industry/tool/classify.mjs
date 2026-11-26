// 不満の「型」を、辞書で全件に自動で振り分ける（費用0）。読み取り（人／AI）で見つけた型を辞書にしたもの。
// 使い方：node classify.mjs <_reviews.json> <業種キー(dental|hair|chiro)> <出力.json> [確認用に表示する件数]
import fs from 'node:fs';
const [file, ind, out, show] = [process.argv[2], process.argv[3], process.argv[4], +process.argv[5] || 0];
const tax = JSON.parse(fs.readFileSync(new URL('./taxonomy.json', import.meta.url), 'utf8'))[ind];
const re = Object.fromEntries(Object.entries(tax).map(([k, v]) => [k, new RegExp(v)]));
const d = JSON.parse(fs.readFileSync(file, 'utf8'));
const low = d.reviews.filter(x => x.star <= 2 && x.text);
const labeled = low.map(x => ({text: x.text, labels: Object.keys(re).filter(k => re[k].test(x.text))}));
const n = labeled.length, none = labeled.filter(x => !x.labels.length).length;
const share = Object.fromEntries(Object.keys(re).map(k => [k, +(labeled.filter(x => x.labels.includes(k)).length / n).toFixed(2)]));
const res = {業種: ind, 星1と2の本文件数: n, どの型にも入らない: +(none / n).toFixed(2), 型ごとの割合: share};
fs.writeFileSync(out, JSON.stringify({...res, 分類結果: labeled.map(x => ({labels: x.labels, text: x.text.slice(0, 120)}))}, null, 1));
console.log(JSON.stringify(res, null, 1));
if (show) { let s = 12345; const rnd = () => (s = (s * 1103515245 + 12345) % 2147483648) / 2147483648; const a = [...labeled]; console.log('--- 確認用の抽出（無作為）'); for (let i = 0; i < Math.min(show, a.length); i++) { const x = a.splice(Math.floor(rnd() * a.length), 1)[0]; console.log(`[${x.labels.join('／') || '（なし）'}] ${x.text.replace(/\s+/g, ' ').slice(0, 85)}`); } }
