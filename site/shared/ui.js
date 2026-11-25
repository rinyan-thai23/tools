// 画面の共通部品（文言・キー欄・国言語・表・CSV）
import { getCreds, setCreds, clearCreds } from './api.js';
import { markdownToHtml } from './markdown.js';

export const lang = document.documentElement.lang || 'ja';
let L = {};
export const t = (k, v = {}) => (L[k] || k).replace(/\{(\w+)\}/g, (_, n) => v[n] ?? '');

const getJson = (u) => fetch(u).then((r) => r.json());
export async function init() {
  L = await getJson(`/locales/${lang}.json`);
  document.querySelectorAll('[data-i18n]').forEach((el) => (el.textContent = t(el.dataset.i18n)));
  const cfg = await getJson('/shared/site-config.json');
  renderKeyBox(document.getElementById('keybox'), cfg.referral_url);
}

// 説明ページ用：data-referral の付いたリンクに紹介リンクを入れる
export async function referralLinks() {
  const cfg = await getJson('/shared/site-config.json');
  document.querySelectorAll('a[data-referral]').forEach((a) => {
    a.href = cfg.referral_url || 'https://dataforseo.com/';
    if (cfg.referral_url) { a.rel = 'noopener sponsored'; a.after(document.createTextNode(lang === 'ja' ? ' （紹介リンクです）' : lang === 'zh-TW' ? '（推薦連結）' : ' (referral link)')); }
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

export async function fillMarkets(countrySel, langSel, allowed) {
  const m = await getJson('/shared/markets.json');
  if (allowed) m.countries = m.countries.filter((c) => allowed.includes(c.code)); // そのAPIが対応している国だけ
  const opt = (a, d) => a.map((x) => `<option value="${x.code}" ${x.code === d ? 'selected' : ''}>${x[lang] || x.en}</option>`).join('');
  if (countrySel) countrySel.innerHTML = opt(m.countries, allowed && !allowed.includes((m.defaults[lang] || m.defaults.en).country) ? allowed[0] : (m.defaults[lang] || m.defaults.en).country);
  if (langSel) langSel.innerHTML = opt(m.languages, (m.defaults[lang] || m.defaults.en).language);
}

const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

// cols: [{key, label, link?}]  rows: [{...}]
export function renderTable(el, cols, rows) {
  if (!rows.length) { el.innerHTML = `<p>${t('ui.empty')}</p>`; return; }
  el.innerHTML = `<div class="scroll"><table><thead><tr>${cols.map((c) => `<th>${c.label}</th>`).join('')}</tr></thead><tbody>${rows
    .map((r) => `<tr>${cols.map((c) => `<td>${c.type === 'image_auth' && r[c.key] ? `<a href="${esc(r[c.key])}" target="_blank" rel="noopener">${esc(r[c.key])}</a><br><img data-auth-src="${esc(r[c.key])}" alt="" class="shot">` : c.type === 'image' && r[c.key] ? `<img src="${esc(r[c.key])}" alt="" loading="lazy" referrerpolicy="no-referrer" class="thumb">` : c.link && r[c.key] ? `<a href="${esc(r[c.key])}" target="_blank" rel="noopener">${esc(r[c.key])}</a>` : esc(r[c.key])}</td>`).join('')}</tr>`)
    .join('')}</tbody></table></div>`;
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

export function downloadCsv(name, cols, rows, more = []) {
  const q = (v) => '"' + String(v ?? '').replace(/"/g, '""') + '"';
  const block = (cs, rs) => [cs.map((c) => q(c.label)).join(','), ...rs.map((r) => cs.map((c) => q(r[c.key])).join(','))];
  const text = [...block(cols, rows), ...more.flatMap((m) => ['', q(m.title), ...block(m.cols, m.rows)])].join('\r\n'); // 2つ目以降の表も、空行をはさんで続ける
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob(['﻿' + text], { type: 'text/csv;charset=utf-8' }));
  a.download = name; a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
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
