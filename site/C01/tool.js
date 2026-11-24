// C01: serp/google/organic/live/advanced
import { callApi, ApiError } from '/shared/api.js';
import { init, t, fillMarkets, renderTable, downloadCsv, fmtDate, startProgress } from '/shared/ui.js';

const $ = (id) => document.getElementById(id);
let cols = [], rows = [];

const toRows = (task) =>
  ((task.result && task.result[0] && task.result[0].items) || [])
    .filter((i) => i.type === 'organic')
    .map((i) => ({ rank: i.rank_group, title: i.title, url: i.url, domain: (i.domain || '').replace(/^www\./, '') }));

function show(task, metaHtml) {
  cols = [
    { key: 'rank', label: t('c01.col.rank') },
    { key: 'title', label: t('c01.col.title') },
    { key: 'url', label: t('c01.col.url'), link: true },
    { key: 'domain', label: t('c01.col.domain') },
  ];
  rows = toRows(task);
  renderTable($('result'), cols, rows);
  $('meta').textContent = metaHtml;
  $('csv').hidden = !rows.length;
}

async function run() {
  $('result').innerHTML = ''; $('meta').textContent = ''; $('csv').hidden = true;
  $('msg').textContent = '';
  $('run').disabled = true;
  const pg = startProgress($('msg'), t('c01.eta'));
  try {
    const { task, cost, time } = await callApi('serp/google/organic/live/advanced', {
      keyword: $('kw').value.trim(), location_code: +$('country').value, language_code: $('language').value, depth: +$('count').value,
    }, { onRetry: pg.retry });
    const took = pg.stop();
    show(task, `${t('ui.cost')}: $${cost} ／ ${t('ui.took')}: ${took}${t('ui.sec')} ／ ${t('ui.fetched')}: ${fmtDate(time)}`);
  } catch (e) {
    pg.stop();
    $('msg').className = 'err';
    $('msg').textContent = t('err.' + (e instanceof ApiError ? e.key : 'other'));
  } finally { $('run').disabled = false; }
}

async function sample() {
  const s = await fetch('../sample.json').then((r) => r.json());
  $('kw').value = s.keyword;
  $('msg').className = 'banner';
  $('msg').textContent = t('ui.sample_notice', { date: s.fetched_at });
  show(s.tasks[0], '');
}

await init();
await fillMarkets($('country'), $('language'));
$('run').onclick = run;
$('sample').onclick = sample;
await sample();
$('csv').onclick = () => downloadCsv('C01.csv', cols, rows);
