// 画面の共通部品（文言・キー欄・国言語・表・CSV）
import { getCreds, setCreds, clearCreds } from './api.js';
import { markdownToHtml } from './markdown.js';

export const lang = document.documentElement.lang || 'ja';
let L = {};
export const t = (k, v = {}) => (L[k] || k).replace(/\{(\w+)\}/g, (_, n) => v[n] ?? '');

const getJson = (u) => fetch(u).then((r) => r.json());
export async function init() {
  L = await getJson(`/locales/${lang}.json`);
  window.__L = L;
  document.querySelectorAll('[data-i18n]').forEach((el) => (el.textContent = t(el.dataset.i18n)));
  const cfg = await getJson('/shared/site-config.json');
  renderKeyBox(document.getElementById('keybox'), cfg.referral_url);
}

// 説明ページ用：data-referral の付いたリンクに紹介リンクを入れる
export async function referralLinks() {
  const cfg = await getJson('/shared/site-config.json');
  document.querySelectorAll('a[data-referral]').forEach((a) => {
    a.href = cfg.referral_url || 'https://dataforseo.com/';
    if (cfg.referral_url) { a.rel = 'noopener sponsored'; a.after(document.createTextNode(lang === 'ja' ? ' （紹介リンクです）' : lang === 'zh-TW' ? '（推薦連結）' : lang === 'vi' ? ' (liên kết giới thiệu)' : ' (referral link)')); }
  });
}

function renderKeyBox(box, referral) {
  const draw = () => {
    const c = getCreds();
    box.innerHTML = `
      <details ${c ? '' : 'open'}>
        <summary>${t('key.title')} <span class="badge ${c ? 'on' : 'off'}">${c ? '● ' + t('key.set') : '○ ' + t('key.unset')}</span></summary>
        <label>${t('key.login')}<input id="k-login" type="email" autocomplete="username" value="${c ? c.login : ''}"></label>
        <label>${t('key.password')}<input id="k-pass" type="password" autocomplete="current-password" value="${c ? c.password : ''}"></label>
        <p class="note">${t('key.note')}</p>
        <button id="k-save">${t('key.save')}</button>
        <button id="k-clear" class="sub">${t('key.clear')}</button>
        <p class="note"><a href="${referral || 'https://dataforseo.com/'}" target="_blank" rel="noopener${referral ? ' sponsored' : ''}">${t('key.create')}</a>${referral ? ' （' + t('key.referral') + '）' : ''} ／ <a href="/dfs-${lang === 'ja' ? 'ja' : 'en'}.html">${t('key.about')}</a></p>
      </details>`;
    box.querySelector('#k-save').onclick = () => {
      setCreds(box.querySelector('#k-login').value.trim(), box.querySelector('#k-pass').value.trim());
      draw();
    };
    box.querySelector('#k-clear').onclick = () => { clearCreds(); draw(); };
  };
  draw();
}

// 国と言語の選択欄。一覧は markets.generated.json（scripts/gen-markets.mjs が、DataForSEOの無料の一覧から作る）。
// 名前は Intl.DisplayNames で、ISOコード／言語コードから画面の言語で作る（訳を手で書かない）。初期値は、画面の言語の国と言語（markets.json の defaults）。
const FAM = [['serp/youtube/', 'yt'], ['serp/', 'serp'], ['keywords_data/google_ads/', 'ads'], ['keywords_data/google_trends/', 'gt'], ['keywords_data/dataforseo_trends/', 'dt'], ['dataforseo_labs/', 'labs'], ['ai_optimization/ai_keyword_data/', 'aikw'], ['ai_optimization/', 'llm']];
export async function fillMarkets(countrySel, langSel, endpoint = '') {
  const [g, d] = await Promise.all([getJson('/shared/markets.generated.json'), getJson('/shared/markets.json')]);
  const fam = (FAM.find(([p]) => endpoint.startsWith(p)) || [0, 'serp'])[1];
  const dflt = d.defaults[lang] || d.defaults.en;
  const dn = (type) => { try { return new Intl.DisplayNames([lang], { type }); } catch { return null; } };
  const rn = dn('region'), ln = dn('language');
  const norm = (c) => String(c).replace('_', '-');
  const cname = (code) => { const [iso, en] = g.countries[code] || ['', String(code)]; try { return (iso && rn && rn.of(iso)) || en; } catch { return en; } };
  const lname = (code) => { try { const n = ln && ln.of(norm(code)); if (n && n !== norm(code)) return n; } catch { /* 予備へ */ } return g.langNames[code] || code; };
  const sorted = (codes, name, first) => [...codes].sort((a, b) => (String(a) === String(first) ? -1 : String(b) === String(first) ? 1 : name(a).localeCompare(name(b), lang)));
  const opt = (codes, name, sel) => codes.map((c) => `<option value="${c}" ${String(c) === String(sel) ? 'selected' : ''}>${name(c)}</option>`).join('');
  const pick = (list) => list.find((c) => norm(c) === dflt.language) || list.find((c) => norm(c) === 'en') || list[0]; // 言語の初期値：画面の言語 → 英語 → 先頭
  const langsOf = (country) => (country != null && g.perCountry[fam] && g.perCountry[fam][country]) || g.langs[fam] || [];
  const fillLangs = () => {
    if (!langSel) return;
    const list = langsOf(countrySel ? countrySel.value : null), prev = langSel.value;
    const first = pick(list);
    langSel.innerHTML = opt(sorted(list, lname, first), lname, list.includes(prev) ? prev : first);
  };
  if (countrySel) {
    const codes = g.fam[fam] || [];
    const first = codes.includes(dflt.country) ? dflt.country : (codes.includes(2840) ? 2840 : codes[0]);
    countrySel.innerHTML = opt(sorted(codes, cname, first), cname, first);
    countrySel.addEventListener('change', fillLangs);
  }
  fillLangs();
}

const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

// cols: [{key, label, link?}]  rows: [{...}]
// opts.rowCopy(i, btn)：行ごとのコピーボタンを付ける。行が PAGE 件を超えるときは、絞り込み・並べ替え・「さらに表示」を付ける（CSV・コピーは全行）
const PAGE = 100;
const cellHtml = (c, r) => (c.type === 'image_auth' && r[c.key] ? `<a href="${esc(r[c.key])}" target="_blank" rel="noopener">${esc(r[c.key])}</a><br><img data-auth-src="${esc(r[c.key])}" alt="" class="shot">` : c.type === 'image' && r[c.key] ? `<img src="${esc(r[c.key])}" alt="" loading="lazy" referrerpolicy="no-referrer" class="thumb">` : c.link && r[c.key] ? `<a href="${esc(r[c.key])}" target="_blank" rel="noopener">${esc(r[c.key])}</a>` : esc(r[c.key]));
export function renderTable(el, cols, rows, opts = {}) {
  if (!rows.length) { el.innerHTML = `<p>${t('ui.empty')}</p>`; return; }
  const big = rows.length > PAGE;
  const st = { q: '', sort: null, dir: 1, shown: PAGE };
  const num = (v) => { const n = parseFloat(String(v ?? '').replace(/,/g, '')); return Number.isFinite(n) && /^[-+]?[\d,.]+/.test(String(v ?? '').trim()) ? n : null; };
  const view = () => {
    let L = rows.map((r, i) => [r, i]);
    if (st.q) { const q = st.q.toLowerCase(); L = L.filter(([r]) => cols.some((c) => String(r[c.key] ?? '').toLowerCase().includes(q))); }
    if (st.sort != null) {
      const k = cols[st.sort].key, allNum = L.every(([r]) => r[k] == null || r[k] === '' || num(r[k]) != null);
      L = [...L].sort((x, y) => { const a = x[0][k], b = y[0][k]; if (a == null || a === '') return 1; if (b == null || b === '') return -1; return (allNum ? num(a) - num(b) : String(a).localeCompare(String(b), lang)) * st.dir; });
    }
    return L;
  };
  const draw = () => {
    const L = view(), vis = L.slice(0, st.shown);
    const head = cols.map((c, j) => `<th${big ? ` data-j="${j}" class="sortable"` : ''}>${c.label}${st.sort === j ? (st.dir > 0 ? ' ▲' : ' ▼') : ''}</th>`).join('') + (opts.rowCopy ? '<th></th>' : '');
    const body = vis.map(([r, i]) => `<tr>${cols.map((c) => `<td>${cellHtml(c, r)}</td>`).join('')}${opts.rowCopy ? `<td><button type="button" class="sub rowcopy" data-i="${i}">${t('ui.copy_row')}</button></td>` : ''}</tr>`).join('');
    const bar = big ? `<div class="tbar"><input type="search" class="tfilter" placeholder="${t('ui.table_filter')}" value="${esc(st.q)}"> <span class="note">${t('ui.table_shown', { total: L.length === rows.length ? rows.length : `${L.length}/${rows.length}`, shown: vis.length })}</span>${vis.length < L.length ? ` <button type="button" class="sub tmore">${t('ui.table_more', { n: Math.min(PAGE, L.length - vis.length) })}</button> <button type="button" class="sub tall">${t('ui.table_all')}</button>` : ''}</div>` : '';
    el.innerHTML = `${bar}<div class="scroll"><table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table></div>`;
    if (big) {
      const f = el.querySelector('.tfilter');
      f.oninput = () => { st.q = f.value.trim(); st.shown = PAGE; const pos = f.selectionStart; draw(); const nf = el.querySelector('.tfilter'); nf.focus(); nf.setSelectionRange(pos, pos); };
      el.querySelectorAll('th.sortable').forEach((th) => (th.onclick = () => { const j = +th.dataset.j; st.dir = st.sort === j ? -st.dir : 1; st.sort = j; draw(); }));
      const m = el.querySelector('.tmore'); if (m) m.onclick = () => { st.shown += PAGE; draw(); };
      const a = el.querySelector('.tall'); if (a) a.onclick = () => { st.shown = rows.length; draw(); };
    }
    if (opts.rowCopy) el.querySelectorAll('button.rowcopy').forEach((b) => (b.onclick = () => opts.rowCopy(+b.dataset.i, b)));
  };
  draw();
}

// DataForSEO の画像（スクショ）は、まず直接読み込む。だめなら、キーを付けて取りに行く（ブラウザの制限で取れないこともある）。取れなければ、リンクだけが残る
export async function loadAuthImages(el) {
  const c = getCreds();
  for (const img of el.querySelectorAll('img[data-auth-src]')) {
    const u = img.dataset.authSrc;
    const viaFetch = async () => { // 直接開けないときは、キーを付けて取りに行く
      try {
        const h = u.startsWith('https://api.dataforseo.com/') && c ? { Authorization: 'Basic ' + btoa(c.login + ':' + c.password) } : {};
        const res = await fetch(u, { headers: h });
        if (!res.ok) throw 0;
        img.onerror = () => img.remove();
        img.src = URL.createObjectURL(await res.blob());
      } catch { img.remove(); }
    };
    img.onerror = viaFetch;
    img.referrerPolicy = 'no-referrer';
    img.src = u;
  }
}


// 折れ線グラフ（外部ライブラリなし）。spec = { x: 横軸の列, y: [縦軸の列, ...] }。値が数字の行だけ描く
export function renderChart(el, cols, rows, spec) {
  if (spec.type === 'bar') return renderBars(el, cols, rows, spec);
  const ys = (spec.y || []).map((k) => cols.find((c) => c.key === k)).filter(Boolean);
  const src = spec.reverse ? [...rows].reverse() : rows; // 新しい順の表は、古い順に並べ直して描く
  const pts = src.map((r) => ({ x: String(r[spec.x] ?? ''), v: ys.map((c) => (typeof r[c.key] === 'number' ? r[c.key] : null)) }));
  if (pts.length < 2 || !ys.length) return;
  const W = 640, H = 240, L = 48, R = 12, T = 12, B = 30;
  const max = Math.max(1, ...pts.flatMap((p) => p.v.filter((v) => v != null)));
  const nice = (m) => { const e = 10 ** Math.floor(Math.log10(m)); const f = m / e; return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 5 ? 5 : 10) * e; };
  const top = nice(max);
  const short = (v) => (v >= 1e6 ? +(v / 1e6).toFixed(1) + 'M' : v >= 1e3 ? +(v / 1e3).toFixed(1) + 'K' : String(Math.round(v))); // 軸の目盛りは短く（26M など）
  const X = (i) => L + ((W - L - R) * i) / (pts.length - 1), Y = (v) => T + (H - T - B) * (1 - v / top);
  const colors = ['var(--chart-1, #2563eb)', 'var(--chart-2, #dc2626)', 'var(--chart-3, #059669)'];
  const grid = [0, 0.25, 0.5, 0.75, 1].map((g) => `<line x1="${L}" x2="${W - R}" y1="${Y(top * g)}" y2="${Y(top * g)}" stroke="currentColor" opacity=".15"/><text x="${L - 6}" y="${Y(top * g) + 4}" text-anchor="end" font-size="11" fill="currentColor" opacity=".7">${short(top * g)}</text>`).join('');
  const label = (p) => p.x.slice(0, 10);
  const idx = [0, Math.floor((pts.length - 1) / 2), pts.length - 1];
  const xl = idx.map((i, n) => `<text x="${X(i)}" y="${H - 8}" text-anchor="${n === 0 ? 'start' : n === 2 ? 'end' : 'middle'}" font-size="11" fill="currentColor" opacity=".7">${esc(label(pts[i]))}</text>`).join('');
  const lines = ys.map((c, k) => {
    const d = pts.map((p, i) => (p.v[k] == null ? '' : `${i && pts[i - 1].v[k] != null ? 'L' : 'M'}${X(i).toFixed(1)},${Y(p.v[k]).toFixed(1)}`)).join(' ');
    const dots = pts.map((p, i) => (p.v[k] == null ? '' : `<circle cx="${X(i).toFixed(1)}" cy="${Y(p.v[k]).toFixed(1)}" r="${pts.length > 60 ? 1.5 : 3}" fill="${colors[k % 3]}"><title>${esc(p.x)}：${p.v[k]}</title></circle>`)).join('');
    return `<path d="${d}" fill="none" stroke="${colors[k % 3]}" stroke-width="2"/>${dots}`;
  }).join('');
  const legend = ys.length > 1 ? `<p class="note">${ys.map((c, k) => `<span style="color:${colors[k % 3]}">●</span> ${esc(c.label)}`).join('　')}</p>` : '';
  el.insertAdjacentHTML('afterbegin', `<div class="chart"><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(ys.map((c) => c.label).join(', '))}" width="100%">${grid}${xl}${lines}</svg>${legend}</div>`);
}

// 横向きの棒グラフ。spec = { x: 名前の列, y: [値の列], sort: 'desc'（任意：値の大きい順に並べる） }
function renderBars(el, cols, rows, spec) {
  const c = cols.find((k) => k.key === spec.y?.[0]);
  let list = rows.filter((r) => typeof r[spec.y[0]] === 'number').map((r) => ({ n: String(r[spec.x] ?? ''), v: r[spec.y[0]] }));
  if (!c || !list.length) return;
  if (spec.sort === 'desc') list = [...list].sort((a, b) => b.v - a.v);
  const max = Math.max(1, ...list.map((p) => p.v));
  const LW = 120, W = 640, RH = 22, H = list.length * RH + 6;
  const body = list.map((p, i) => {
    const y = 3 + i * RH, w = Math.max(1, ((W - LW - 44) * p.v) / max);
    return `<text x="${LW - 6}" y="${y + 15}" text-anchor="end" font-size="12" fill="currentColor">${esc(p.n)}</text><rect x="${LW}" y="${y + 3}" width="${w.toFixed(1)}" height="${RH - 8}" rx="2" fill="var(--chart-1, #2563eb)"><title>${esc(p.n)}：${p.v}</title></rect><text x="${LW + w + 5}" y="${y + 15}" font-size="11" fill="currentColor" opacity=".7">${p.v}</text>`;
  }).join('');
  el.insertAdjacentHTML('afterbegin', `<div class="chart"><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(c.label)}" width="100%">${body}</svg></div>`);
}

export function downloadCsv(name, cols, rows, more = []) {
  const q = (v) => '"' + String(v ?? '').replace(/"/g, '""') + '"';
  const block = (cs, rs) => [cs.map((c) => q(c.label)).join(','), ...rs.map((r) => cs.map((c) => q(r[c.key])).join(','))];
  const text = [...block(cols, rows), ...more.flatMap((m) => ['', q(m.title), ...block(m.cols, m.rows)])].join('\r\n'); // 2つ目以降の表も、空行をはさんで続ける
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob(['﻿' + text], { type: 'text/csv;charset=utf-8' }));
  a.download = name; a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}

// 表をタブ区切りの文字にする（表計算に貼れる形。2つ目以降の表も、空行をはさんで続ける）
export function tableToTsv(cols, rows, more = []) {
  const c = (v) => String(v ?? '').replace(/[\t\r\n]+/g, ' ').trim();
  const block = (cs, rs) => [cs.map((x) => c(x.label)).join('\t'), ...rs.map((r) => cs.map((x) => c(r[x.key])).join('\t'))];
  return [...block(cols, rows), ...more.flatMap((m) => ['', c(m.title), ...block(m.cols, m.rows)])].join('\n');
}

// クリップボードにコピー（使えないブラウザでは、選択してコピーする方法に切り替える）
export async function copyText(text) {
  try { await navigator.clipboard.writeText(text); return true; } catch { /* 下へ */ }
  try {
    const ta = document.createElement('textarea');
    ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select();
    const ok = document.execCommand('copy'); ta.remove(); return ok;
  } catch { return false; }
}

export const fmtDate = (d) => d.toLocaleString(lang);

// 取得中の表示：動くバー＋経過時間＋目安。終わったら stop() で止めて、かかった秒数を返す
export function startProgress(el, etaText) {
  const t0 = Date.now();
  el.className = 'progress';
  el.setAttribute('role', 'status');
  el.innerHTML = `<div class="bar"><i></i></div><div><span class="state">${t('ui.loading')}</span> ／ ${t('ui.elapsed')}: <b class="sec">0</b>${t('ui.sec')} ／ ${etaText}</div>`;
  const sec = el.querySelector('.sec');
  const timer = setInterval(() => (sec.textContent = Math.floor((Date.now() - t0) / 1000)), 500);
  return {
    retry: (n) => (el.querySelector('.state').textContent = t('ui.retrying', { n })),
    stop: () => { clearInterval(timer); el.className = ''; el.innerHTML = ''; return Math.round((Date.now() - t0) / 100) / 10; },
  };
}

// 文章で返るツール用：回答文（Markdown）を安全に整形して表示
export function renderAnswer(el, label, markdown) {
  el.innerHTML = markdown ? `<h2 class="sub-title">${esc(label)}</h2><div class="answer">${markdownToHtml(markdown)}</div>` : '';
}
