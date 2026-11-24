// 品質ゲート②：ビルドした dist/worker.js をブラウザで開いて、全ツール×全言語を動かして確かめる。
//   node scripts/smoke.mjs [C02 C03 ...]
// 見るもの：エラーなし／サンプルが表示される（3行以上）／見出し・料金・目安が出ている／CSVが落ちる（BOM付き）／スマホ幅で横にはみ出さない
import http from 'node:http';
import { readdirSync, readFileSync, existsSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import { execSync } from 'node:child_process';

let chromium;
try { ({ chromium } = await import('playwright')); }
catch { ({ chromium } = await import(pathToFileURL(execSync('npm root -g').toString().trim() + '/playwright/index.mjs').href)); }

const langs = JSON.parse(readFileSync('scripts/langs.json', 'utf8')).map((l) => l.code);
const only = process.argv.slice(2);
const ids = (only.length ? only : readdirSync('site').filter((n) => /^[A-Z]\d+$/.test(n) && existsSync(`site/${n}/tool.json`))).sort();

const mod = await import(pathToFileURL(process.cwd() + '/dist/worker.js').href + '?' + Date.now());
const srv = http.createServer(async (q, s) => {
  const r = await mod.default.fetch(new Request('http://localhost:8787' + q.url));
  s.writeHead(r.status, Object.fromEntries(r.headers));
  s.end(Buffer.from(await r.arrayBuffer()));
}).listen(8787);

const browser = await chromium.launch();
let bad = 0;
for (const id of ids) for (const l of langs) {
  const url = `http://localhost:8787/${id}/${l}/`;
  const E = [];
  const ctx = await browser.newContext({ viewport: { width: 390, height: 800 }, acceptDownloads: true });
  const p = await ctx.newPage();
  p.on('pageerror', (e) => E.push('JSエラー: ' + e.message));
  p.on('console', (m) => m.type() === 'error' && E.push('console.error: ' + m.text()));
  p.on('requestfailed', (r) => E.push('読み込み失敗: ' + r.url()));
  try {
    const res = await p.goto(url);
    if (res.status() !== 200) E.push('HTTP ' + res.status());
    await p.waitForSelector('#result table', { timeout: 8000 }).catch(() => E.push('サンプルの表が出ない'));
    const n = await p.$$eval('#result tbody tr', (r) => r.length).catch(() => 0);
    const cfg = JSON.parse(readFileSync(`site/${id}/tool.json`, 'utf8'));
    if (n < (cfg.min_sample_rows ?? 3)) E.push(`サンプルの行が少ない（${n}）`);
    if (cfg.result.answer && !(await p.$('#answer .answer p'))) E.push('回答文が表示されない');
    if (cfg.result.columns.some((c) => c.type === 'image') && !(await p.$('#result img.thumb'))) E.push('画像が表示されない');
    for (const sel of ['h1', 'title', '#run', '#sample']) {
      const t = (await p.textContent(sel).catch(() => '')) || '';
      if (!t.trim()) E.push(`${sel} が空`);
    }
    const price = (await p.textContent('.note[data-i18n$=".price"]').catch(() => '')) || '';
    if (!/\$/.test(price)) E.push('料金の目安が出ていない');
    if (!(await p.$('#msg.banner'))) E.push('「これはサンプルです」の帯が出ていない');
    // 文言キーがそのまま出ていないか（翻訳漏れ）
    const raw = await p.$$eval('body *', (els) => els.filter((e) => e.children.length === 0 && !e.closest('#result') && /^(ui|key|err|site|who|c\d+)\.[a-z0-9_.]+$/.test(e.textContent.trim())).map((e) => e.textContent.trim()));
    if (raw.length) E.push('文言キーがそのまま表示: ' + raw.slice(0, 3).join(', '));
    // CSV
    const [dl] = await Promise.all([p.waitForEvent('download', { timeout: 5000 }).catch(() => null), p.click('#csv').catch(() => {})]);
    if (!dl) E.push('CSVが落ちない');
    else {
      const buf = readFileSync(await dl.path());
      if (!(buf[0] === 0xef && buf[1] === 0xbb && buf[2] === 0xbf)) E.push('CSVにBOMがない');
      if (buf.toString('utf8').split('\r\n').length < (cfg.min_sample_rows ?? 3) + 1) E.push('CSVの行が少ない');
    }
    // スマホ幅ではみ出さない
    const over = await p.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    if (over > 1) E.push(`スマホ幅で横にはみ出す（${over}px）`);
  } catch (e) { E.push('例外: ' + e.message.split('\n')[0]); }
  await ctx.close();
  const ok = E.filter(Boolean).length === 0;
  if (!ok) bad++;
  console.log(`${ok ? '✓' : '✗'} ${id}/${l}`);
  for (const e of E.filter(Boolean)) console.log('    ✗ ' + e);
}
await browser.close();
srv.close();
console.log(`\n${ids.length * langs.length - bad}/${ids.length * langs.length} ページが合格`);
process.exit(bad ? 1 : 0);
