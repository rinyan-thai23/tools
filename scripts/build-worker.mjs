// site/ の全ファイルを1つの Worker に埋め込む → dist/worker.js
import { readdirSync, readFileSync, writeFileSync, mkdirSync, statSync } from 'node:fs';
import { join, extname } from 'node:path';

const types = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.txt': 'text/plain; charset=utf-8',
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
