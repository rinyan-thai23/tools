// 全ツール共通の動き。ツールごとの違いは site/Cxx/tool.json に書く。
import { callApi, ApiError } from '/shared/api.js';
import { init, t, fillMarkets, renderTable, downloadCsv, fmtDate, startProgress } from '/shared/ui.js';

const id = document.body.dataset.tool;
const cfg = await fetch(`/${id}/tool.json`).then((r) => r.json());
const key = id.toLowerCase();
const $ = (x) => document.getElementById(x);
const get = (o, path) => path.split('.').reduce((a, k) => (a == null ? a : a[k]), o);
const transforms = { strip_www: (v) => String(v ?? '').replace(/^www\./, '') };

let cols = [], rows = [];

function toRows(task) {
  const r = cfg.result;
  return (get(task, r.items) || [])
    .filter((it) => Object.entries(r.where || {}).every(([k, v]) => it[k] === v))
    .map((it) => Object.fromEntries(r.columns.map((c) => {
      const v = get(it, c.from || c.key);
      return [c.key, c.transform ? transforms[c.transform](v) : v];
    })));
}

function show(task, meta) {
  cols = cfg.result.columns.map((c) => ({ key: c.key, label: t(c.label), link: c.link }));
  rows = toRows(task);
  renderTable($('result'), cols, rows);
  $('meta').textContent = meta;
  $('csv').hidden = !rows.length;
}

function params() {
  const p = { ...(cfg.params || {}) };
  for (const i of cfg.inputs) p[i.param] = $('in-' + i.id).value.trim();
  if (cfg.markets) { p.location_code = +$('country').value; p.language_code = $('language').value; }
  if (cfg.count) p[cfg.count.param] = +$('count').value;
  return p;
}

async function run() {
  $('result').innerHTML = ''; $('meta').textContent = ''; $('csv').hidden = true;
  $('msg').textContent = '';
  $('run').disabled = true;
  const pg = startProgress($('msg'), t(`${key}.eta`));
  try {
    const { task, cost, time } = await callApi(cfg.endpoint, params(), { onRetry: pg.retry });
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
  $('in-' + cfg.inputs[0].id).value = s.keyword;
  $('msg').className = 'banner';
  $('msg').textContent = t('ui.sample_notice', { date: s.fetched_at });
  show(s.tasks[0], '');
}

await init();
if (cfg.markets) await fillMarkets($('country'), $('language'));
$('run').onclick = run;
$('sample').onclick = sample;
$('csv').onclick = () => downloadCsv(cfg.csv || `${id}.csv`, cols, rows);
await sample();
