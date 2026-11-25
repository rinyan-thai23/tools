// site/ をもとに、ページを自動生成して、全ファイルを1つの Worker に埋め込む → dist/worker.js
//   ・site/Cxx/tool.json がある → /Cxx/<言語>/ のページを言語ごとに生成
//   ・トップページ（/ と /en/ など）を「誰の」ごとに分けて生成
//   ・ヘッダー・フッター・紹介リンク・確認タグを差し込み、sitemap.xml と robots.txt を生成
import { readdirSync, readFileSync, writeFileSync, mkdirSync, statSync, existsSync } from 'node:fs';
import { join, extname } from 'node:path';

const read = (p) => readFileSync(p, 'utf8');
const b64 = (x) => Buffer.from(x).toString('base64');
const unb64 = (x) => Buffer.from(x, 'base64').toString('utf8');
const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

const types = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.svg': 'image/svg+xml', '.xml': 'application/xml; charset=utf-8', '.png': 'image/png', '.csv': 'text/csv; charset=utf-8', '.txt': 'text/plain; charset=utf-8',
};

// ---------- 1. site/ のファイルを集める（. や _ で始まるファイルは公開しない）
const files = {};
const walk = (d, base = '') => {
  for (const n of readdirSync(d)) {
    if (n.startsWith('.') || n.startsWith('_')) continue;
    const p = join(d, n), u = base + '/' + n;
    if (statSync(p).isDirectory()) walk(p, u);
    else files[u] = { type: types[extname(n)] || 'application/octet-stream', body: readFileSync(p).toString('base64') };
  }
};
walk('site');
const addPage = (url, html) => { files[url] = { type: types['.html'], body: b64(html) }; };

const cfg = JSON.parse(read('site/shared/site-config.json'));
const siteUrl = cfg.site_url.replace(/\/$/, '');

// ---------- 2. 言語とロケール
const langs = JSON.parse(read('scripts/langs.json')); // [{code, label}]
const locales = {};
for (const { code } of langs) {
  const p = `site/locales/${code}.json`;
  if (existsSync(p)) locales[code] = JSON.parse(read(p));
}
const topPath = (l) => (l === 'ja' ? '/' : `/${l}/`);
const render = (tpl, vars) => tpl.replace(/\{\{(\w+)\}\}/g, (m, k) => (k in vars ? vars[k] : m));

// ---------- 3. ツール一覧（site/Cxx/tool.json）
const toolIds = readdirSync('site').filter((n) => /^[A-Z]\d+$/.test(n) && existsSync(`site/${n}/tool.json`)).sort();
const tools = toolIds.map((id) => ({ ...JSON.parse(read(`site/${id}/tool.json`)), id }));
// 公開できる言語 = ロケールがあり、そのツールの本文ファイルがある
const langsOf = (id) => langs.filter(({ code }) => locales[code] && existsSync(`site/${id}/_content.${code}.html`));

// ---------- 4. ツールのページを生成
const toolTpl = read('scripts/templates/tool.html');
for (const tool of tools) {
  const id = tool.id, k = id.toLowerCase();
  const avail = langsOf(id);
  const alt = avail.map(({ code }) => `<link rel="alternate" hreflang="${code}" href="{{SITE_URL}}/${id}/${code}/">`).join('\n')
    + `\n<link rel="alternate" hreflang="x-default" href="{{SITE_URL}}/${id}/${(avail.find((a) => a.code === 'en') || avail[0]).code}/">`;
  for (const { code: l } of avail) {
    const L = locales[l];
    const T = (key) => esc(L[key] ?? '');
    const inputs = tool.inputs.map((i) => `<label><span data-i18n="${i.label}">${T(i.label)}</span>${i.select ? `<select id="in-${i.id}">${i.select.map((o) => `<option value="${esc(o.value)}" data-i18n="${o.label}">${T(o.label)}</option>`).join('')}</select>` : i.multiline ? `<textarea id="in-${i.id}" rows="4"></textarea>` : `<input id="in-${i.id}" type="text"${i.datalist ? ` list="dl-${i.id}"` : ''}>${i.datalist ? `<datalist id="dl-${i.id}"></datalist>` : ''}`}</label>`).join('\n');
    const chunkNote = tool.chunk ? '<p class="note" id="chunk-note"></p>' : '';
    const cSel = `<label><span data-i18n="ui.country">${T('ui.country')}</span><select id="country"></select></label>`;
    const lSel = `<label><span data-i18n="ui.language">${T('ui.language')}</span><select id="language"></select></label>`;
    const markets = tool.markets === 'country' ? cSel : tool.markets === 'language' ? lSel : tool.markets ? `<div class="row">\n  ${cSel}\n  ${lSel}\n</div>` : '';
    const count = tool.count
      ? `<label><span data-i18n="${tool.count.label}">${T(tool.count.label)}</span><select id="count">${tool.count.options.map((o) => `<option>${o}</option>`).join('')}</select></label>`
      : '';
    const slow = tool.slow_search ? `<p class="note" data-i18n="ui.slow_search">${T('ui.slow_search')}</p>` : '';
    const switcher = avail.filter((a) => a.code !== l).map((a) => `<a href="/${id}/${a.code}/">${esc(a.label)}</a>`).join(' ');
    const html = render(toolTpl, {
      LANG: l, ID: id, TITLE: T(`${k}.title`), META: T(`${k}.meta`), ALT: alt, CANON: `{{SITE_URL}}/${id}/${l}/`,
      SWITCH: switcher, TOP: topPath(l), TOPLABEL: T('ui.top'),
      NAME_KEY: `${k}.name`, NAME: T(`${k}.name`), DESC_KEY: `${k}.desc`, DESC: T(`${k}.desc`),
      PRICE_KEY: `${k}.price`, PRICE: T(`${k}.price`), INPUTS: inputs + chunkNote, MARKETS: markets, COUNT: count, SLOW: slow,
      RUN: T('ui.run'), SAMPLE: T('ui.sample'), CSV: T('ui.csv'), CONTENT: read(`site/${id}/_content.${l}.html`),
    });
    addPage(`/${id}/${l}/index.html`, html);
  }
}

// ---------- 5. トップページ（言語ごと・「誰の」ごとにツールを並べる）
const indexTpl = read('scripts/templates/index.html');
const indexLangs = langs.filter(({ code }) => locales[code] && tools.some((t) => langsOf(t.id).some((a) => a.code === code)));
const indexAlt = indexLangs.map(({ code }) => `<link rel="alternate" hreflang="${code}" href="{{SITE_URL}}${topPath(code)}">`).join('\n')
  + `\n<link rel="alternate" hreflang="x-default" href="{{SITE_URL}}${topPath((indexLangs.find((a) => a.code === 'en') || indexLangs[0]).code)}">`;
for (const { code: l } of indexLangs) {
  const L = locales[l];
  const groups = {};
  for (const t of tools) if (langsOf(t.id).some((a) => a.code === l)) (groups[t.who] ||= []).push(t);
  const list = Object.entries(groups).map(([who, ts]) =>
    `<h3>${esc(L[`who.${who}`] ?? who)}</h3>\n<ul class="tools">\n${ts.map((t) => `  <li><strong>${t.id}</strong> <a href="/${t.id}/${l}/">${esc(L[`${t.id.toLowerCase()}.name`])}</a><br><span class="note">${esc(L[`${t.id.toLowerCase()}.desc`])}</span></li>`).join('\n')}\n</ul>`).join('\n');
  const switcher = indexLangs.filter((a) => a.code !== l).map((a) => `<a href="${topPath(a.code)}">${esc(a.label)}</a>`).join(' ');
  // トップページの「このサイトでできること」（機能別の説明と、ツールへのリンク）。言語ごとに scripts/index-categories.json に書いた分だけ出す
  const catAll = existsSync('scripts/index-categories.json') ? JSON.parse(read('scripts/index-categories.json')) : {};
  const cat = catAll[l];
  const descs = existsSync('scripts/index-descriptions.json') ? (JSON.parse(read('scripts/index-descriptions.json'))[l] || {}) : {}; // トップの詳しい説明（キーワード入り）
  const introTop = cat ? `<p class="intro-lead"><strong>${esc(cat.intro)}</strong></p>` : '';
  const intro = cat ? `<section class="intro">\n<h2>${esc(cat.title)}</h2>\n${cat.sections.map((sec) => {
    const items = sec.tools.filter((id) => langsOf(id).some((a) => a.code === l)).map((id) => `  <li><small class="tid">${id}</small> <a href="/${id}/${l}/">${esc((cat.titled || []).includes(id) ? L[`${id.toLowerCase()}.title`] : L[`${id.toLowerCase()}.name`])}</a><br><span class="note">${esc(descs[id] ?? L[`${id.toLowerCase()}.desc`])}</span></li>`);
    return items.length ? `<h3>${esc(sec.title)}</h3>\n<p>${esc(sec.text)}</p>\n<ul class="tools">\n${items.join('\n')}\n</ul>` : '';
  }).join('\n')}\n</section>` : '';
  const aboutLang = l === 'ja' ? 'ja' : l === 'zh-TW' ? 'zh-TW' : 'en';
  addPage(topPath(l) + 'index.html', render(indexTpl, {
    LANG: l, TITLE: esc(L['site.index_title']), META: esc(L['site.index_meta']), ALT: indexAlt, CANON: `{{SITE_URL}}${topPath(l)}`,
    SWITCH: switcher, H1: esc(L['site.title']).replace('DataForSEO', '<a data-referral href="https://dataforseo.com/" target="_blank" rel="noopener">DataForSEO</a>'), LEAD: esc(L['site.lead']), TOOLS_TITLE: cat ? '' : esc(L['site.tools']),
    LIST: cat ? '' : list, INTRO_TOP: introTop, INTRO: intro, ABOUT: `<a href="/dfs-${aboutLang}.html">${esc(L['key.about'])}</a>`,
  }).replace('<h2 id="tools"></h2>\n', ''));
}

// ---------- 5b. 記事（日本語のみ）：articles/index.json と articles/<slug>.html から /articles/ を生成
if (existsSync('articles/index.json')) {
  const arts = JSON.parse(read('articles/index.json'));
  const LJ = locales.ja || {};
  const tname = (id) => LJ[`${id.toLowerCase()}.name`] || id;
  const tdesc = (id) => LJ[`${id.toLowerCase()}.desc`] || '';
  const byTool = {};
  for (const a of arts) (byTool[a.tool] ||= []).push(a);
  const toolIdsWithArts = Object.keys(byTool).sort();
  const nav = toolIdsWithArts.map((id) => `<a href="#t-${id}">${id} ${esc(tname(id))}（${byTool[id].length}本）</a>`).join(' ／ ');
  const list = toolIdsWithArts.map((id) => `<section id="t-${id}">\n<h2><small class="tid">${id}</small> ${esc(tname(id))}</h2>\n<p class="note">対象ツール：<a href="/${id}/ja/">${esc(tname(id))}</a>｜${esc(tdesc(id))}</p>\n<ul class="tools">\n${byTool[id].map((a) => `<li><a href="/articles/${a.slug}/">${esc(a.title)}</a><br><span class="note">${esc(a.description)}（${esc(a.date)}）</span></li>`).join('\n')}\n</ul>\n</section>`);
  const shell = (title, desc, canon, body) => `<!doctype html>\n<html lang="ja">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>${esc(title)}</title>\n<meta name="description" content="${esc(desc)}">\n<link rel="canonical" href="{{SITE_URL}}${canon}">\n<meta property="og:title" content="${esc(title)}">\n<meta property="og:description" content="${esc(desc)}">\n<link rel="stylesheet" href="/shared/style.css">\n</head>\n<body>\n<!--SITE_HEADER-->\n${body}\n<!--SITE_FOOTER-->\n</body>\n</html>\n`;
  addPage('/articles/index.html', shell('記事一覧｜DataForSEO 1機能ツール集', 'ツールで実際に調べたデータをそのまま載せた記事の一覧です。', '/articles/', `<p><a href="/">← ツール一覧</a></p>\n<h1>記事一覧</h1>\n<p>ツールを実際に使って調べたデータを、そのまま載せた記事です。ツールごとに並べています。</p>\n<p class="note">${nav}</p>\n${list.join('\n')}`));
  for (const a of arts) {
    const body = read(`articles/${a.slug}.html`).replace(/<!--include:(\w+)-->/g, (m, n) => read(`articles/_inc/${n}.html`));
    const others = arts.filter((x) => x.slug !== a.slug).map((x) => `<li><a href="/articles/${x.slug}/">${esc(x.title)}</a></li>`).join('\n');
    addPage(`/articles/${a.slug}/index.html`, shell(`${a.title}｜DataForSEO 1機能ツール集`, a.description, `/articles/${a.slug}/`,
      `<p><a href="/articles/">← 記事一覧</a></p>\n<article>\n<h1>${esc(a.title)}</h1>\n<p class="note">${esc(a.date)} ／ 運営者：Hideaki Takahashi ／ </p>\n<p class="box">この記事のツール：<strong><a href="/${a.tool}/ja/">${a.tool} ${esc(tname(a.tool))}</a></strong><br><span class="note">${esc(tdesc(a.tool))}</span></p>\n${body}\n<h2>関連する記事</h2>\n<ul>\n${others}\n</ul>\n<p><a href="/about/">運営者について</a></p>\n</article>`));
  }
  // ツールページ（日本語）の下に「関連記事」
  for (const t of tools) {
    const rel = arts.filter((a) => a.tool === t.id);
    const u = `/${t.id}/ja/index.html`;
    if (!rel.length || !files[u]) continue;
    const block = `<section class="seo">\n<h2>このツールの関連記事</h2>\n<ul>\n${rel.map((a) => `<li><a href="/articles/${a.slug}/">${esc(a.title)}</a></li>`).join('\n')}\n</ul>\n</section>\n`;
    files[u].body = b64(unb64(files[u].body).replace('<!--SITE_FOOTER-->', block + '<!--SITE_FOOTER-->'));
  }
}

// ---------- 6. ヘッダー・フッター・確認タグ・紹介リンクの差し込み
const refUrl = cfg.referral_url || 'https://dataforseo.com/';
const noteText = { ja: ' （紹介リンクです）', en: ' (referral link)', 'zh-TW': '（推薦連結）' };
const part = (n, l) => read(existsSync(`scripts/partials/${n}.${l}.html`) ? `scripts/partials/${n}.${l}.html` : `scripts/partials/${n}.en.html`);
for (const [u, f] of Object.entries(files)) {
  if (!u.endsWith('.html')) continue;
  let h = unb64(f.body);
  if (!h.includes('<!--SITE_')) continue;
  const l = (h.match(/<html lang="([\w-]+)"/) || [])[1] || 'ja';
  h = h.replace('<!--SITE_HEADER-->', part('header', l)).replace('<!--SITE_FOOTER-->', part('footer', l));
  h = h.replace('<!--SITE_VERIFY-->', cfg.google_site_verification ? `<meta name="google-site-verification" content="${cfg.google_site_verification}">` : '');
  h = h.replaceAll('{{REFERRAL_URL}}', refUrl)
    .replaceAll('{{REFERRAL_REL}}', cfg.referral_url ? 'noopener sponsored' : 'noopener')
    .replaceAll('{{REFERRAL_NOTE}}', cfg.referral_url ? (noteText[l] || noteText.en) : '');
  f.body = b64(h);
}

// ---------- 7. SITE_URL の置換
for (const f of Object.values(files)) {
  if (f.type.startsWith('text/html')) f.body = b64(unb64(f.body).replaceAll('{{SITE_URL}}', siteUrl));
}

// ---------- 8. sitemap.xml と robots.txt（noindex のページは載せない）
const pages = Object.keys(files)
  .filter((u) => u.endsWith('.html') && !unb64(files[u].body).includes('noindex'))
  .map((u) => u.replace(/index\.html$/, ''));
files['/sitemap.xml'] = { type: types['.xml'], body: b64(`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${pages.map((u) => `<url><loc>${siteUrl}${u}</loc></url>`).join('\n')}\n</urlset>\n`) };
files['/robots.txt'] = { type: types['.txt'], body: b64(`User-agent: *\nAllow: /\nSitemap: ${siteUrl}/sitemap.xml\n`) };

// ---------- 9. Worker を書き出す
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
console.log('tools:', tools.map((t) => t.id).join(','), '| files:', Object.keys(files).length, '| bytes:', code.length);
