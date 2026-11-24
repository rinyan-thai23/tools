// site/ の全ファイルを1つの Worker に埋め込む → dist/worker.js
import { readdirSync, readFileSync, writeFileSync, mkdirSync, statSync } from 'node:fs';
import { join, extname } from 'node:path';

const types = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.svg': 'image/svg+xml', '.xml': 'application/xml; charset=utf-8', '.png': 'image/png', '.txt': 'text/plain; charset=utf-8',
};
const files = {};
const walk = (d, base = '') => {
  for (const n of readdirSync(d)) {
    if (n.startsWith('.')) continue;
    const p = join(d, n), u = base + '/' + n;
    if (statSync(p).isDirectory()) walk(p, u);
    else files[u] = { type: types[extname(n)] || 'application/octet-stream', body: readFileSync(p).toString('base64') };
  }
};
walk('site');

// SITE_URL の置換（site/shared/site-config.json の site_url）
const siteUrl = JSON.parse(readFileSync('site/shared/site-config.json', 'utf8')).site_url.replace(/\/$/, '');
for (const [u, f] of Object.entries(files)) {
  if (/\.(html|xml|txt)$/.test(u)) f.body = Buffer.from(Buffer.from(f.body, 'base64').toString('utf8').replaceAll('{{SITE_URL}}', siteUrl)).toString('base64');
}
// sitemap.xml と robots.txt を自動生成
const pages = Object.keys(files).filter((u) => u.endsWith('.html')).map((u) => u.replace(/index\.html$/, ''));
const b64 = (x) => Buffer.from(x).toString('base64');
files['/sitemap.xml'] = { type: types['.xml'], body: b64(`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${pages.map((u) => `<url><loc>${siteUrl}${u}</loc></url>`).join('\n')}\n</urlset>\n`) };
files['/robots.txt'] = { type: types['.txt'], body: b64(`User-agent: *\nAllow: /\nSitemap: ${siteUrl}/sitemap.xml\n`) };

const code = `const FILES = ${JSON.stringify(files)};
const dec = (b) => Uint8Array.from(atob(b), (c) => c.charCodeAt(0));
export default {
  fetch(req) {
    let p = decodeURIComponent(new URL(req.url).pathname);
    if (!FILES[p] && !p.endsWith('/') && FILES[p + '/index.html']) return Response.redirect(new URL(p + '/', req.url).href, 301);
    if (p.endsWith('/')) p += 'index.html';
    const f = FILES[p];
    if (!f) return new Response('Not found', { status: 404 });
    return new Response(dec(f.body), { headers: { 'content-type': f.type, 'cache-control': 'public, max-age=300' } });
  },
};
`;
mkdirSync('dist', { recursive: true });
writeFileSync('dist/worker.js', code);
console.log('files:', Object.keys(files).length, 'bytes:', code.length);
