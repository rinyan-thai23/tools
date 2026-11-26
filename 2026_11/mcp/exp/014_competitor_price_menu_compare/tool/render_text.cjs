// ブラウザ（Playwright・無料）でページを表示して、見える文章を取り出す。同じサイト内のリンクを最大 N ページ たどる。
// 使い方：node render_text.cjs <URL> <出力.txt> [最大ページ数=5]
const {chromium} = require('playwright'); const fs = require('fs');
(async () => {
  const [url, out, maxp] = [process.argv[2], process.argv[3], +process.argv[4] || 5];
  const b = await chromium.launch(); const ctx = await b.newContext({userAgent: 'Mozilla/5.0 (compatible; research-bot)', locale: 'ja-JP'});
  const origin = new URL(url).origin; const seen = new Set(), queue = [url], texts = [];
  while (queue.length && seen.size < maxp) {
    const u = queue.shift(); if (seen.has(u)) continue; seen.add(u);
    const p = await ctx.newPage();
    try {
      await p.goto(u, {waitUntil: 'networkidle', timeout: 30000}).catch(() => {}); await p.waitForTimeout(1200);
      const t = await p.evaluate(() => document.body.innerText || '');
      texts.push(`### ${u}\n${t}`);
      const links = await p.evaluate(() => [...document.querySelectorAll('a[href]')].map(a => ({h: a.href, t: (a.innerText || a.getAttribute('aria-label') || '').trim()})));
      // 「料金・メニュー・価格・Price」のリンクを、先にたどる（料金のページに着くため）
      const PRI = /料金|メニュー|価格|price|menu|コース|system/i;
      for (const {h, t: lt} of links) { try { const x = new URL(h); x.hash = ''; if (x.origin === origin && !/\.(jpg|png|pdf|zip)$/i.test(x.pathname) && !seen.has(x.href) && !queue.includes(x.href)) { if (PRI.test(lt) || PRI.test(x.pathname)) queue.unshift(x.href); else queue.push(x.href); } } catch {} }
    } catch (e) { texts.push(`### ${u}\n（取得失敗：${e.message.slice(0, 60)}）`); }
    await p.close();
  }
  await b.close();
  const all = texts.join('\n\n').split('\n').map(l => l.replace(/[ \t　]+/g, ' ').trim()).filter(Boolean);
  fs.writeFileSync(out, [...new Set(all)].join('\n'));
  console.log(out.split('/').pop(), 'ページ', seen.size, '文字数', all.join('').length);
})();
