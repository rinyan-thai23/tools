// 全ツール共通の動き。ツールごとの違いは site/Cxx/tool.json に書く。
import { callApi, getApi, ApiError } from '/shared/api.js';
import { extractRows, extractAnswer, extractExtra, parseVideoId } from '/shared/rows.js';
import { init, t, fillMarkets, renderTable, renderAnswer, downloadCsv, fmtDate, startProgress } from '/shared/ui.js';

const id = document.body.dataset.tool;
const cfg = await fetch(`/${id}/tool.json`).then((r) => r.json());
const key = id.toLowerCase();
const $ = (x) => document.getElementById(x);
let cols = [], rows = [], lookupMap = null; // lookupMap：番号→名前（result.lookup があるツールだけ）

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
  for (const x of extractExtra(cfg, task)) {
    if (!x.rows.length) continue;
    const d = document.createElement('div');
    $('result').appendChild(d);
    renderTable(d, x.columns.map((c) => ({ key: c.key, label: t(c.label), link: c.link, type: c.type })), x.rows);
    if (x.title) d.insertAdjacentHTML('afterbegin', `<h2 class="sub-title">${t(x.title)}</h2>`);
  }
  $('meta').textContent = meta;
  $('csv').hidden = !rows.length;
}

function params() {
  const p = { ...(cfg.params || {}) };
  for (const i of cfg.inputs) {
    const v = $('in-' + i.id).value.trim();
    if (i.wrap === 'lines') { // 改行（と、読点・カンマ）で区切って、複数のキーワードにする
      const list = v.split(/[\n,、]+/).map((x) => x.trim()).filter(Boolean);
      if (!list.length) throw new ApiError('bad_input');
      p[i.param] = i.max ? list.slice(0, i.max) : list;
    } else if (i.wrap === 'array') p[i.param] = [v];
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
$('run').onclick = run;
$('sample').onclick = sample;
$('csv').onclick = () => downloadCsv(cfg.csv || `${id}.csv`, cols, rows);
await sample();
