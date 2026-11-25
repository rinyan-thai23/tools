// 全ツール共通の動き。ツールごとの違いは site/Cxx/tool.json に書く。
import { callApi, getApi, ApiError } from '/shared/api.js';
import { extractRows, extractAnswer, extractExtra, parseVideoId, parseDomain } from '/shared/rows.js';
import { init, t, fillMarkets, renderTable, renderAnswer, renderChart, loadAuthImages, downloadCsv, fmtDate, startProgress, tableToTsv, copyText } from '/shared/ui.js';

const id = document.body.dataset.tool;
const cfg = await fetch(`/${id}/tool.json`).then((r) => r.json());
const key = id.toLowerCase();
const $ = (x) => document.getElementById(x);
let techNames = []; // 技術名の一覧（無料）。C75 のように transform: technology の入力があるツールだけ使う
async function loadTech() {
  if (techNames.length) return;
  const tk = await getApi('domain_analytics/technologies/technologies');
  try { techNames = tk ? tk.result[0].groups.flatMap((g) => g.categories.flatMap((c) => c.technologies)) : []; } catch { techNames = []; }
  const dl = document.querySelector('datalist');
  if (dl) dl.innerHTML = [...new Set(techNames.map((n) => n.trim()))].map((n) => `<option value="${n.replace(/"/g, '&quot;')}">`).join('');
}
let cols = [], rows = [], more = [], lookupMap = null; // lookupMap：番号→名前（result.lookup があるツールだけ）

function prepRows(task, now) { // 1回の結果から、表の行を作る（番号→名前、値の読み替えまで）
  const rs = extractRows(cfg, task, { now });
  if (cfg.result.lookup && lookupMap) rs.forEach((r) => { const n = lookupMap[r[cfg.result.lookup.column]]; if (n) r[cfg.result.lookup.column] = `${n}（${r[cfg.result.lookup.column]}）`; });
  for (const c of cfg.result.columns) if (c.labels) rs.forEach((r) => { if (c.labels[r[c.key]]) r[c.key] = t(c.labels[r[c.key]]); });
  return rs;
}
// task：1回の結果。multi：複数入力のとき [{ input, task }]（入力ごとの結果を、「入力」の列を付けて1つの表にする）
function show(task, meta, now, multi) {
  const items = multi || [{ input: null, task }];
  const tag = (it, r) => (multi ? { __in: it.input, ...r } : r);
  cols = cfg.result.columns.map((c) => ({ key: c.key, label: t(c.label), link: c.link, type: c.type }));
  if (multi) cols.unshift({ key: '__in', label: t('ui.multi_input') });
  rows = items.flatMap((it) => prepRows(it.task, now).map((r) => tag(it, r)));
  answerMd = items.map((it) => { const a = extractAnswer(cfg, it.task) || ''; return multi && a ? `### ${it.input}\n${a}` : a; }).filter(Boolean).join('\n\n');
  renderAnswer($('answer'), cfg.result.answer ? t(cfg.result.answer.label) : '', answerMd);
  if (cfg.result.answer_only) $('result').innerHTML = '';
  else {
    renderTable($('result'), cols, rows, cfg.copy ? { rowCopy: rowCopyHandler } : {});
    if (!multi && cfg.result.chart && rows.length && (!cfg.result.chart.single || new Set(rows.map((r) => r[cfg.result.chart.single])).size === 1)) { const ch = document.createElement('div'); $('result').prepend(ch); renderChart(ch, cols, rows, cfg.result.chart); } // 表の上にグラフ（tool.json の result.chart）。複数入力のときは出さない
    if (cfg.result.title && rows.length) $('result').insertAdjacentHTML('afterbegin', `<h2 class="sub-title">${t(cfg.result.title)}</h2>`);
  }
  // 2つ目以降の表（result.extra）
  more = [];
  const nex = (cfg.result.extra || []).length;
  for (let k = 0; k < nex; k++) {
    const parts = items.map((it) => ({ it, x: extractExtra(cfg, it.task)[k] }));
    const x = parts[0].x; const xrows = parts.flatMap(({ it, x: y }) => y.rows.map((r) => tag(it, r)));
    if (!xrows.length) continue;
    const d = document.createElement('div');
    $('result').appendChild(d);
    x.columns.forEach((c) => { if (c.labels) xrows.forEach((r) => { if (c.labels[r[c.key]]) r[c.key] = t(c.labels[r[c.key]]); }); });
    const xc = x.columns.map((c) => ({ key: c.key, label: t(c.label), link: c.link, type: c.type }));
    if (multi) xc.unshift({ key: '__in', label: t('ui.multi_input') });
    more.push({ title: x.title ? t(x.title) : '', cols: xc, rows: xrows });
    renderTable(d, xc, xrows);
    if (!multi && x.chart) { const ch = document.createElement('div'); d.prepend(ch); renderChart(ch, xc, xrows, x.chart); } // 2つ目以降の表にも、グラフを付けられる
    if (x.title) d.insertAdjacentHTML('afterbegin', `<h2 class="sub-title">${t(x.title)}</h2>`);
  }
  loadAuthImages($('result'));
  $('meta').textContent = meta;
  $('csv').hidden = !rows.length;
  $('copy').hidden = !(cfg.copy && rows.length);
  renderAiBox();
}

function params(ov) {
  const p = { ...(cfg.params || {}) };
  // 実行日から決める日付（date_from：11か月前の月初＝いまの月を入れて12か月分）
  const mago = /^months_ago_(\d+)$/.exec(cfg.params_dynamic?.date_from || '');
  if (mago) { const d = new Date(); d.setDate(1); d.setMonth(d.getMonth() - +mago[1]); p.date_from = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-01`; }
  const nd = new Date(); nd.setDate(nd.getDate() + (((6 - nd.getDay() + 7) % 7) || 7)); // 次の土曜（今日が土曜なら、来週の土曜）
  const ymd = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  if (cfg.params_dynamic?.check_in === 'next_saturday') { p.check_in = ymd(nd); nd.setDate(nd.getDate() + 1); p.check_out = ymd(nd); } // 次の土曜・1泊
  for (const i of cfg.inputs) {
    let v = (ov && ov[i.id] != null ? ov[i.id] : $('in-' + i.id).value).trim();
    if (i.transform === 'domain') { v = parseDomain(v); if (!v) throw new ApiError('bad_input'); }
    if (i.transform === 'technology') { // 技術名は大文字小文字を区別するので、一覧から正しい書き方に直す（一覧にない名前は、料金がかかる前にエラー）
      if (!techNames.length) throw new ApiError('tech_list'); // 一覧が取れていないときは、料金がかかる呼び出しをしない
      const hit = techNames.find((n) => n.trim().toLowerCase() === v.toLowerCase());
      if (!hit) throw new ApiError('bad_technology');
      v = hit;
    }
    if (i.wrap === 'lines') { // 改行（と、読点・カンマ）で区切って、複数のキーワードにする
      const list = v.split(/[\n,、]+/).map((x) => x.trim()).filter(Boolean);
      if (!list.length) throw new ApiError('bad_input');
      p[i.param] = i.max ? list.slice(0, i.max) : list;
    } else if (i.wrap === 'array') p[i.param] = [v];
    else if (i.wrap === 'filter_eq') p[i.param] = [i.field, '=', v]; // 例：filters: ["domain","=","example.com"]
    else if (i.param.includes('.')) { const [a, b] = i.param.split('.'); (p[a] ||= {})[b] = v; } // 例：pages.1 → {pages:{"1": 値}}
    else if (i.transform === 'video_id') { const vid = parseVideoId(v); if (!vid) throw new ApiError('bad_video'); p[i.param] = vid; } else p[i.param] = v;
  }
  // markets: true=国と言語／"country"=国だけ／"language"=言語だけ（language_params に送り先の項目名）
  if (cfg.markets === true || cfg.markets === 'country') p.location_code = +$('country').value;
  const lc = (l) => (/^keywords_data\/google_ads\//.test(cfg.endpoint) && l === 'zh-TW' ? 'zh_TW' : l); // Google広告のAPIは zh_TW（アンダースコア）
  if (cfg.markets === true) p.language_code = lc($('language').value);
  if (cfg.markets === 'language') for (const k of cfg.language_params || ['language_code']) p[k] = lc($('language').value);
  if (cfg.count) p[cfg.count.param] = +$('count').value;
  return p;
}

// 件数が多いとき、APIの上限（1回ぶん）ごとに分けて、順に送る。結果は1つにまとめ、料金は合計する（tool.json の chunk）
async function sendAll(p, pg) {
  const c = cfg.chunk, list = c && p[c.param];
  if (!c || !Array.isArray(list) || list.length <= c.size) return callApi(cfg.endpoint, p, { onRetry: pg.retry });
  const parts = [];
  for (let i = 0; i < list.length; i += c.size) parts.push(list.slice(i, i + c.size));
  let first = null, cost = 0, result = [], time;
  for (let n = 0; n < parts.length; n++) {
    if (n) await new Promise((r) => setTimeout(r, 1500)); // 続けて送りすぎない
    $('msg').textContent = t('ui.chunk_progress', { n: n + 1, m: parts.length });
    const r = await callApi(cfg.endpoint, { ...p, [c.param]: parts[n] }, { onRetry: pg.retry });
    first ||= r.task; cost += r.cost || 0; time = r.time; result = result.concat(r.task.result || []);
  }
  if (c.merge_items) result = [{ ...(result[0] || {}), items: result.flatMap((x) => x.items || []), items_count: result.reduce((a, x) => a + (x.items_count || (x.items || []).length), 0) }]; // 結果が result[0].items に入る型は、items をつなげる
  return { task: { ...first, result }, cost: Math.round(cost * 1e6) / 1e6, time };
}

// ---- コピー・AI分析プロンプト（tool.json の copy: true のツールだけ。プロンプトの文は、ロケールの <id>.ai_prompt）
let dataDate = '', answerMd = '';
const selText = (id) => { const e = $(id); return e && e.selectedOptions && e.selectedOptions[0] ? e.selectedOptions[0].textContent : ''; };
const MAX_CHARS = 120000;
function aiData() { // AIに渡すデータの文字。答え（文章）があれば先頭に付ける。大きすぎるときは、先頭の行だけにする
  const make = (keep) => {
    const tbl = rows.length ? tableToTsv(cols, keep == null ? rows : rows.slice(0, keep), keep == null ? more : []) : '';
    if (!answerMd) return tbl;
    if (cfg.result.answer_only) return answerMd;
    return `${t('ui.ai_answer_head')}\n${answerMd}\n\n${t('ui.ai_refs_head')}\n${tbl}`;
  };
  let text = make(null), n = rows.length, truncated = false;
  if (text.length > MAX_CHARS) {
    let keep = rows.length; while (keep > 1 && make(keep).length > MAX_CHARS) keep = Math.floor(keep * 0.9);
    text = make(keep); n = keep; truncated = true;
  }
  return { text, n, truncated };
}
// ---- 前回のデータ（このブラウザの localStorage に保存。比較プロンプト用）
const hash = (str) => { let h = 5381; for (let i = 0; i < str.length; i++) h = ((h << 5) + h + str.charCodeAt(i)) | 0; return (h >>> 0).toString(36); };
const prevKey = () => `dfs_prev:${id}:${lang()}:${hash(cfg.inputs.map((i) => $('in-' + i.id).value.trim()).join('\n') + '|' + ($('country') ? $('country').value : '') + '|' + ($('language') ? $('language').value : ''))}`;
const lang = () => document.documentElement.lang;
function readPrev() { try { return JSON.parse(localStorage.getItem(prevKey()) || 'null'); } catch { return null; } }
function writePrev() { try { const d = aiData(); if (d.text.length < 400000) localStorage.setItem(prevKey(), JSON.stringify({ date: dataDate, text: d.text, n: d.n })); } catch { /* 保存できなくても、そのまま */ } }
let prevRec = null, isSample = true;
function renderAiBox() {
  const box = $('ai-box');
  if (!cfg.copy || !(rows.length || answerMd) || !(`${key}.ai_prompt` in L())) { box.hidden = true; box.innerHTML = ''; return; }
  const d = aiData();
  const hasDiff = `${key}.ai_prompt_diff` in L();
  const vars = { date: dataDate, country: selText('country'), language: selText('language'), n: rows.length };
  const marker = t('ui.ai_data_here'), pmarker = t('ui.ai_prev_here');
  const text = (mode) => (mode === 'diff'
    ? t(`${key}.ai_prompt_diff`, { ...vars, data: marker, prev_data: pmarker, prev_date: prevRec ? prevRec.date : '', prev_n: prevRec ? prevRec.n : '' })
    : t(`${key}.ai_prompt`, { ...vars, data: marker }));
  box.hidden = false;
  box.innerHTML = `<details><summary>${t('ui.ai_title')}</summary>
    <p class="note">${t('ui.ai_note')}</p>
    ${hasDiff ? `<p><button id="ai-m-analyze" class="sub">${t('ui.ai_mode_analyze')}</button> <button id="ai-m-diff" class="sub">${t('ui.ai_mode_diff')}</button></p><p id="ai-prev-note" class="note"></p>` : ''}
    <textarea id="ai-text" rows="16" spellcheck="false"></textarea>
    <p class="note">${t('ui.ai_size', { n: d.n, k: d.text.length.toLocaleString() })}${d.truncated ? ' ' + t('ui.ai_trunc', { n: d.n }) : ''}</p>
    <button id="ai-copy-prompt" class="sub">${t('ui.ai_copy_prompt')}</button>
    <button id="ai-copy-all">${t('ui.ai_copy_all')}</button>
    <span id="ai-msg" class="note" role="status"></span></details>`;
  const ta = $('ai-text'); let mode = 'analyze'; ta.value = text(mode);
  const setMode = (m) => {
    mode = m; ta.value = text(m);
    $('ai-m-analyze').classList.toggle('sub', m !== 'analyze'); $('ai-m-diff').classList.toggle('sub', m !== 'diff');
    $('ai-prev-note').textContent = m === 'diff' ? (prevRec ? t('ui.ai_prev_saved', { date: prevRec.date }) : t('ui.ai_prev_none')) : '';
  };
  if (hasDiff) { $('ai-m-analyze').onclick = () => setMode('analyze'); $('ai-m-diff').onclick = () => setMode('diff'); setMode('analyze'); }
  const say = (ok) => { $('ai-msg').textContent = ok ? t('ui.copied') : t('ui.copy_failed'); setTimeout(() => ($('ai-msg').textContent = ''), 2500); };
  $('ai-copy-prompt').onclick = async () => say(await copyText(ta.value));
  $('ai-copy-all').onclick = async () => { // マーカーの場所にデータを入れる（消されていたら、最後に付ける）
    let v = ta.value;
    if (mode === 'diff' && prevRec) v = v.split(pmarker).join(prevRec.text);
    const full = v.includes(marker) ? v.split(marker).join(d.text) : v + '\n\n' + d.text;
    say(await copyText(full));
  };
}
// ---- 表の行ごとのコピー（見出し＋その行を、タブ区切りで）
async function rowCopyHandler(i, b) {
  const ok = await copyText(tableToTsv(cols, [rows[i]]));
  b.textContent = ok ? t('ui.copied') : t('ui.copy_failed'); setTimeout(() => (b.textContent = t('ui.copy_row')), 1500);
}
// ---- 入力を共有するURL（入力・国・言語だけ。APIキーは入れない）
const SHARE_MAX = 4000;
function shareUrl() {
  const q = new URLSearchParams();
  cfg.inputs.forEach((i) => { const v = $('in-' + i.id).value.trim(); if (v) q.set('i_' + i.id, v); });
  if ($('country')) q.set('country', $('country').value); if ($('language')) q.set('language', $('language').value);
  if ($('count')) q.set('count', $('count').value);
  return `${location.origin}${location.pathname}?${q.toString()}`;
}
function applyShared() { // URLに入力があれば、入力欄に入れる（自動では実行しない）
  const q = new URLSearchParams(location.search); let any = false;
  cfg.inputs.forEach((i) => { if (q.has('i_' + i.id)) { $('in-' + i.id).value = q.get('i_' + i.id); any = true; } });
  if (!any) return false;
  if ($('country') && q.get('country')) $('country').value = q.get('country');
  if ($('language') && q.get('language')) $('language').value = q.get('language');
  if ($('count') && q.get('count')) $('count').value = q.get('count');
  document.querySelectorAll('[id^=in-]').forEach((e) => e.dispatchEvent(new Event('input')));
  $('msg').className = 'banner'; $('msg').textContent = t('ui.shared_notice');
  return true;
}
const L = () => window.__L || {};
// ---- 複数入力（tool.json の multi: { input, max, unit_cost, parallel, confirm_over }）
const multiLines = () => {
  const m = cfg.multi; const seen = new Set();
  return $('in-' + m.input).value.split('\n').map((x) => x.trim()).filter((x) => x && !seen.has(x) && seen.add(x)).slice(0, m.max);
};
async function runMulti(lines, pg) {
  const m = cfg.multi, est = (lines.length * m.unit_cost).toFixed(3);
  if (lines.length > (m.confirm_over ?? 10) && !window.confirm(t('ui.multi_confirm', { n: lines.length, cost: est }))) { pg.stop(); return; }
  const results = [], errs = []; let done = 0, cost = 0, time = new Date(), fatal = null;
  const next = (() => { let i = 0; return () => (i < lines.length && !fatal ? i++ : -1); })();
  const worker = async () => {
    for (let i = next(); i >= 0; i = next()) {
      try {
        const r = await sendAll(params({ [m.input]: lines[i] }), { retry: pg.retry });
        results[i] = { input: lines[i], task: r.task }; cost += r.cost || 0; time = r.time || time;
      } catch (e) {
        const k = e instanceof ApiError ? e.key : 'other';
        if (['nokey', '40100', '40210'].includes(k)) { fatal = e; return; } // キー・残高の問題は、続けても同じ。止める
        errs.push({ input: lines[i], key: k });
      }
      done++; $('msg').textContent = t('ui.multi_progress', { n: done, m: lines.length });
    }
  };
  await Promise.all(Array.from({ length: Math.min(m.parallel || 2, lines.length) }, worker));
  const took = pg.stop();
  const ok = results.filter(Boolean);
  if (fatal && !ok.length) throw fatal;
  dataDate = new Date().toISOString().slice(0, 10); isSample = false; prevRec = null;
  show(null, `${t('ui.cost')}: $${Math.round(cost * 1e6) / 1e6} ／ ${t('ui.took')}: ${took}${t('ui.sec')} ／ ${t('ui.fetched')}: ${fmtDate(time)}`, undefined, ok);
  if (errs.length || fatal) { $('msg').className = 'err'; $('msg').textContent = t('ui.multi_failed', { n: errs.length + (fatal ? lines.length - done : 0), list: errs.map((e) => e.input).slice(0, 5).join(', ') }); }
}
async function run() {
  $('answer').innerHTML = ''; $('result').innerHTML = ''; $('meta').textContent = ''; $('csv').hidden = true; $('copy').hidden = true; $('ai-box').hidden = true;
  $('msg').textContent = '';
  $('run').disabled = true;
  const pg = startProgress($('msg'), t(`${key}.eta`));
  try {
    if (cfg.inputs.some((i) => i.transform === 'technology')) await loadTech();
    if (cfg.multi) { // 複数入力：1行ごとに1回ずつ送る
      const lines = multiLines();
      if (lines.length > 1) { await runMulti(lines, pg); return; }
    }
    let { task, cost, time } = await sendAll(params(cfg.multi ? { [cfg.multi.input]: multiLines()[0] ?? '' } : undefined), pg);
    if (cfg.result.lookup) { const lk = await getApi(cfg.result.lookup.endpoint); lookupMap = lk ? Object.fromEntries((lk.result || []).map((x) => [x[cfg.result.lookup.key], x[cfg.result.lookup.value]])) : null; }
    const took = pg.stop();
    dataDate = new Date().toISOString().slice(0, 10);
    isSample = false; prevRec = cfg.copy ? readPrev() : null;
    show(task, `${t('ui.cost')}: $${cost} ／ ${t('ui.took')}: ${took}${t('ui.sec')} ／ ${t('ui.fetched')}: ${fmtDate(time)}`);
    if (cfg.copy) writePrev();
  } catch (e) {
    pg.stop();
    $('msg').className = 'err';
    $('msg').textContent = t('err.' + (e instanceof ApiError ? e.key : 'other'));
  } finally { $('run').disabled = false; }
}

async function sample() {
  const sl = (cfg.sample_langs || []).includes(document.documentElement.lang) ? `sample.${document.documentElement.lang}.json` : 'sample.json'; // 言語ごとの専用サンプル（tool.json の sample_langs に書いた言語だけ）
  const r = await fetch(`/${id}/${sl}`);
  const s = await r.json();
  if (s.multi && cfg.multi && sl === 'sample.json') { // 複数入力のサンプル（3件）：入力欄に3件を入れ、「入力」の列つきの表で見せる
    $('in-' + cfg.multi.input).value = s.multi.map((m) => m.input).join('\n');
    document.querySelectorAll('[id^=in-]').forEach((e) => e.dispatchEvent(new Event('input')));
    $('msg').className = 'banner'; $('msg').textContent = t('ui.sample_notice', { date: s.fetched_at });
    dataDate = s.fetched_at; show(null, '', new Date(`${s.fetched_at}-15`), s.multi); return;
  }
  if (s.inputs) for (const [k, v] of Object.entries(s.inputs)) $('in-' + k).value = v; // 入力が複数あるツール
  else if (cfg.inputs.length) $('in-' + cfg.inputs[0].id).value = s.keyword;
  document.querySelectorAll('[id^=in-]').forEach((e) => e.dispatchEvent(new Event('input'))); // 語数の表示などを更新
  lookupMap = s.tasks[0].lookup || null;
  $('msg').className = 'banner';
  $('msg').textContent = t('ui.sample_notice', { date: s.fetched_at });
  dataDate = s.fetched_at;
  show(s.tasks[0], '', new Date(`${s.fetched_at}-15`)); // サンプルは、取った月を「今月」として扱う
}

await init();
(() => { // 「取得できる量と料金の目安」を、数段階の表で見せる（ロケールの <id>.steps = [[量, 料金, 使いどころ], ...]）
  const rowsS = (window.__L || {})[`${key}.steps`]; if (!Array.isArray(rowsS) || !rowsS.length) return;
  const esc = (x) => String(x).replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
  $('steps').innerHTML = `<details open><summary>${t('ui.steps_title')}</summary><div class="scroll"><table class="steps"><thead><tr><th>${t('ui.steps_amount')}</th><th>${t('ui.steps_cost')}</th><th>${t('ui.steps_use')}</th></tr></thead><tbody>${rowsS.map((r) => `<tr>${r.map((c) => `<td>${esc(c)}</td>`).join('')}</tr>`).join('')}</tbody></table></div></details>`;
})();
if (cfg.markets) await fillMarkets($('country'), $('language'), cfg.country_codes); // 'country' / 'language' のときは、ない方は null
if (cfg.inputs.some((i) => i.transform === 'technology')) loadTech().catch(() => {});
if (cfg.chunk) { // 入力した語数と、送る回数・料金の目安を、その場で見せる
  const ta = $('in-' + cfg.chunk.input), nt = $('chunk-note');
  const upd = () => {
    const n = ta.value.split(/[\n,、]+/).map((x) => x.trim()).filter(Boolean).length, c = cfg.chunk;
    if (!n) { nt.textContent = ''; return; }
    const used = Math.min(n, c.max), calls = Math.ceil(used / c.size), cost = (c.per_item != null ? calls * c.base + used * c.per_item : calls * c.unit_cost).toFixed(c.per_item != null ? 3 : 2); // 1回の基本料金＋1語ごと（per_item）の型と、1回いくらの型
    nt.textContent = (n > c.max ? t('ui.chunk_over', { max: c.max }) + ' ' : '') + (calls > 1 ? t('ui.chunk_multi', { n: used, calls, cost }) : t('ui.chunk_one', { n: used, cost }));
  };
  ta.addEventListener('input', upd); upd();
}
if (cfg.multi) { // 入力した件数と、料金の目安を、その場で見せる
  const ta = $('in-' + cfg.multi.input), nt = $('multi-note');
  const upd = () => {
    const all = ta.value.split('\n').map((x) => x.trim()).filter(Boolean).length, n = multiLines().length;
    if (!all) { nt.textContent = ''; return; }
    nt.textContent = (all > cfg.multi.max ? t('ui.multi_over', { max: cfg.multi.max }) + ' ' : '') + (n > 1 ? t('ui.multi_note', { n, cost: (n * cfg.multi.unit_cost).toFixed(3) }) : t('ui.multi_one'));
  };
  ta.addEventListener('input', upd); upd();
}
$('run').onclick = run;
$('copy').onclick = async () => { const ok = await copyText(tableToTsv(cols, rows, more)); $('copy-msg').textContent = ok ? t('ui.copied') : t('ui.copy_failed'); setTimeout(() => ($('copy-msg').textContent = ''), 2500); };
$('csv').onclick = () => downloadCsv(cfg.csv || `${id}.csv`, cols, rows, more);
const shared = cfg.copy && applyShared();
if (cfg.copy) { const sb = $('share'); sb.hidden = false; sb.onclick = async () => { const u = shareUrl(); if (u.length > SHARE_MAX) { $('copy-msg').textContent = t('ui.share_too_long'); return; } const ok = await copyText(u); $('copy-msg').textContent = ok ? t('ui.share_copied') : t('ui.copy_failed'); setTimeout(() => ($('copy-msg').textContent = ''), 3500); }; }
if (!shared) await sample();
