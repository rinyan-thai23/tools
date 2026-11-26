// HTMLから「見える文章」だけを取り出す（script・style・SVG・コメント・タグを除く）。費用0。
// 使い方：node extract_text.mjs <in.html> <out.txt>
import fs from 'node:fs';
let h = fs.readFileSync(process.argv[2], 'utf8');
h = h.replace(/<!--[\s\S]*?-->/g, ' ').replace(/<(script|style|svg|noscript|template)[\s\S]*?<\/\1>/gi, ' ')
  .replace(/<(br|\/p|\/div|\/li|\/h[1-6]|\/tr|\/section)[^>]*>/gi, '\n').replace(/<[^>]+>/g, ' ')
  .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(+n));
const lines = h.split('\n').map(l => l.replace(/[ \t　]+/g, ' ').trim()).filter(l => l.length >= 2);
const uniq = [...new Set(lines)];
fs.writeFileSync(process.argv[3], uniq.join('\n'));
console.log(process.argv[2].split('/').pop(), '→ 行数', uniq.length, '文字数', uniq.join('').length);
