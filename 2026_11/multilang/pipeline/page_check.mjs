import http from 'node:http';
import { pathToFileURL } from 'node:url';
import { execSync } from 'node:child_process';
const { chromium } = await import(pathToFileURL(execSync('npm root -g').toString().trim() + '/playwright/index.mjs').href);
const mod = await import(pathToFileURL('/home/user/tools/dist/worker.js').href + '?' + Date.now());
const srv = http.createServer(async (q, s) => { const r = await mod.default.fetch(new Request('http://localhost:8788' + q.url)); s.writeHead(r.status, Object.fromEntries(r.headers)); s.end(Buffer.from(await r.arrayBuffer())); }).listen(8788);
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 390, height: 800 }, deviceScaleFactor: 1 });
const errs = []; p.on('pageerror', (e) => errs.push(e.message)); p.on('console', (m) => m.type() === 'error' && errs.push(m.text()));
for (const u of ['/C24/vi/', '/C24/ja/', '/vi/']) {
  await p.goto('http://localhost:8788' + u); await p.waitForTimeout(1200);
  const info = await p.evaluate(() => ({ lang: document.documentElement.lang, h1: document.querySelector('h1')?.textContent, c: [...document.querySelectorAll('#country option')].map((o) => o.textContent + (o.selected ? '*' : '')), l: [...document.querySelectorAll('#language option')].map((o) => o.textContent + (o.selected ? '*' : '')), rows: document.querySelectorAll('table tbody tr').length, run: document.getElementById('run')?.textContent, notice: document.body.innerText.includes('bản mẫu'), ai: document.querySelector('#ai-box textarea')?.value.slice(0, 120) }));
  console.log(u, JSON.stringify(info));
}
await p.goto('http://localhost:8788/C24/vi/'); await p.waitForTimeout(1200);
await p.screenshot({ path: '/tmp/claude-0/-home-user-tools/2ca120b9-7712-5745-afca-83eac98dbbdc/scratchpad/vi_c24.png', fullPage: false });
console.log('errors', errs);
await b.close(); srv.close();
