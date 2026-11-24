// 全ツール共通の動き。ツールごとの違いは site/Cxx/tool.json に書く。
import { callApi, getApi, ApiError } from '/shared/api.js';
import { extractRows, extractAnswer, extractExtra, parseVideoId, parseDomain } from '/shared/rows.js';
import { init, t, fillMarkets, renderTable, renderAnswer, loadAuthImages, downloadCsv, fmtDate, startProgress } from '/shared/ui.js';

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

function show(task, meta) {
  cols = cfg.result.columns.map((c) => ({ key: c.key, label: t(c.label), link: c.link, type: c.type }));
  rows = extractRows(cfg, task);
  // 番号を名前に引く（無料の参照データ）。lookup.column の値を「名前（番号）」にする
  if (cfg.result.lookup && lookupMap) rows.forEach((r) => { const n = lookupMap[r[cfg.result.lookup.column]]; if (n) r[cfg.result.lookup.column] = `${n}（${r[cfg.result.lookup.column]}）`; });
  // 値の読み替え（例：informational → 情報を調べる）。columns[].labels = { 元の値: 文言のキー }
  for (const c of cfg.result.columns) if (c.labels) rows.forEach((r) => { if (c.labels[r[c.key]]) r[c.key] = t(c.labels[r[c.key]]); });
  renderAnswer($('answer'), cfg.result.answer ? t(cfg.result.answer.label) : '', extractAnswer(cfg, task));
  if (cfg.result.answer_only) $('result').innerHTML = '';
  else {
    renderTable($('result'), cols, rows);
    if (cfg.result.title && rows.length) $('result').insertAdjacentHTML('afterbegin', `<h2 class="sub-title">${t(cfg.result.title)}</h2>`);
  }
  // 2つ目以降の表（result.extra）
  more = [];
  for (const x of extractExtra(cfg, task)) {
    if (!x.rows.length) continue;
    const d = document.createElement('div');
    $('result').appendChild(d);
    x.columns.forEach((c) => { if (c.labels) x.rows.forEach((r) => { if (c.labels[r[c.key]]) r[c.key] = t(c.labels[r[c.key]]); }); });
    const xc = x.columns.map((c) => ({ key: c.key, label: t(c.label), link: c.link, type: c.type }));
    more.push({ title: x.title ? t(x.title) : '', cols: xc, rows: x.rows });
    renderTable(d, xc, x.rows);
    if (x.title) d.insertAdjacentHTML('afterbegin', `<h2 class="sub-title">${t(x.title)}</h2>`);
  }
  loadAuthImages($('result'));
  $('meta').textContent = meta;
  $('csv').hidden = !rows.length;
}

function params() {
  const p = { ...(cfg.params || {}) };
  // 実行日から決める日付（date_from：11か月前の月初＝いまの月を入れて12か月分）
  if (cfg.params_dynamic?.date_from === 'months_ago_11') { const d = new Date(); d.setDate(1); d.setMonth(d.getMonth() - 11); p.date_from = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-01`; }
  const nd = new Date(); nd.setDate(nd.getDate() + (((6 - nd.getDay() + 7) % 7) || 7)); // 次の土曜（今日が土曜なら、来週の土曜）
  const ymd = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  if (cfg.params_dynamic?.check_in === 'next_saturday') { p.check_in = ymd(nd); nd.setDate(nd.getDate() + 1); p.check_out = ymd(nd); } // 次の土曜・1泊
  for (const i of cfg.inputs) {
    let v = $('in-' + i.id).value.trim();
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
  if (cfg.markets === true) p.language_code = $('language').value;
  if (cfg.markets === 'language') for (const k of cfg.language_params || ['language_code']) p[k] = $('language').value;
  if (cfg.count) p[cfg.count.param] = +$('count').value;
  return p;
}

async function run() {
  $('answer').innerHTML = ''; $('result').innerHTML = ''; $('meta').textContent = ''; $('csv').hidden = true;
  $('msg').textContent = '';
  $('run').disabled = true;
  const pg = startProgress($('msg'), t(`${key}.eta`));
  try {
    if (cfg.inputs.some((i) => i.transform === 'technology')) await loadTech();
    const { task, cost, time } = await callApi(cfg.endpoint, params(), { onRetry: pg.retry });
    if (cfg.result.lookup) { const lk = await getApi(cfg.result.lookup.endpoint); lookupMap = lk ? Object.fromEntries((lk.result || []).map((x) => [x[cfg.result.lookup.key], x[cfg.result.lookup.value]])) : null; }
    const took = pg.stop();
    show(task, `${t('ui.cost')}: $${cost} ／ ${t('ui.took')}: ${took}${t('ui.sec')} ／ ${t('ui.fetched')}: ${fmtDate(time)}`);
  } catch (e) {
    pg.stop();
    $('msg').className = 'err';
    $('msg').textContent = t('err.' + (e instanceof ApiError ? e.key : 'other'));
  } finally { $('run').disabled = false; }
}

async function sample() {
  const s = await fetch(`/${id}/sample.json`).then((r) => r.json());
  if (s.inputs) for (const [k, v] of Object.entries(s.inputs)) $('in-' + k).value = v; // 入力が複数あるツール
  else if (cfg.inputs.length) $('in-' + cfg.inputs[0].id).value = s.keyword;
  lookupMap = s.tasks[0].lookup || null;
  $('msg').className = 'banner';
  $('msg').textContent = t('ui.sample_notice', { date: s.fetched_at });
  show(s.tasks[0], '');
}

await init();
if (cfg.markets) await fillMarkets($('country'), $('language')); // 'country' / 'language' のときは、ない方は null
if (cfg.inputs.some((i) => i.transform === 'technology')) loadTech().catch(() => {});
$('run').onclick = run;
$('sample').onclick = sample;
$('csv').onclick = () => downloadCsv(cfg.csv || `${id}.csv`, cols, rows, more);
await sample();
