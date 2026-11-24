// 画面の共通部品（文言・キー欄・国言語・表・CSV）
import { getCreds, setCreds, clearCreds } from './api.js';

export const lang = document.documentElement.lang === 'en' ? 'en' : 'ja';
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
    if (cfg.referral_url) { a.rel = 'noopener sponsored'; a.after(document.createTextNode(lang === 'ja' ? ' （紹介リンクです）' : ' (referral link)')); }
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
        <p class="note"><a href="${referral || 'https://dataforseo.com/'}" target="_blank" rel="noopener${referral ? ' sponsored' : ''}">${t('key.create')}</a>${referral ? ' （' + t('key.referral') + '）' : ''} ／ <a href="/dfs-${lang}.html">${t('key.about')}</a></p>
      </details>`;
    box.querySelector('#k-save').onclick = () => {
      setCreds(box.querySelector('#k-login').value.trim(), box.querySelector('#k-pass').value.trim());
      draw();
    };
    box.querySelector('#k-clear').onclick = () => { clearCreds(); draw(); };
  };
  draw();
}

export async function fillMarkets(countrySel, langSel) {
  const m = await getJson('/shared/markets.json');
  const opt = (a, d) => a.map((x) => `<option value="${x.code}" ${x.code === d ? 'selected' : ''}>${x[lang]}</option>`).join('');
  countrySel.innerHTML = opt(m.countries, m.defaults[lang].country);
  langSel.innerHTML = opt(m.languages, m.defaults[lang].language);
}

const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

// cols: [{key, label, link?}]  rows: [{...}]
export function renderTable(el, cols, rows) {
  if (!rows.length) { el.innerHTML = `<p>${t('ui.empty')}</p>`; return; }
  el.innerHTML = `<div class="scroll"><table><thead><tr>${cols.map((c) => `<th>${c.label}</th>`).join('')}</tr></thead><tbody>${rows
    .map((r) => `<tr>${cols.map((c) => `<td>${c.link && r[c.key] ? `<a href="${esc(r[c.key])}" target="_blank" rel="noopener">${esc(r[c.key])}</a>` : esc(r[c.key])}</td>`).join('')}</tr>`)
    .join('')}</tbody></table></div>`;
}

export function downloadCsv(name, cols, rows) {
  const q = (v) => '"' + String(v ?? '').replace(/"/g, '""') + '"';
  const text = [cols.map((c) => q(c.label)).join(','), ...rows.map((r) => cols.map((c) => q(r[c.key])).join(','))].join('\r\n');
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob(['﻿' + text], { type: 'text/csv;charset=utf-8' }));
  a.download = name; a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}

export const fmtDate = (d) => d.toLocaleString(lang === 'ja' ? 'ja-JP' : 'en-US');
