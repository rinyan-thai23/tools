// 結果の取り出し（tool.js とチェック用スクリプトで共用。画面にもNodeにも依存しない）
export const get = (o, path) => path.split('.').reduce((a, k) => (a == null ? a : a[k]), o);
export const transforms = {
  strip_www: (v) => String(v ?? '').replace(/^www\./, ''),
  date: (v) => String(v ?? '').slice(0, 10), // "2026-11-22 04:50:16 +00:00" → "2026-11-22"
  mmss: (v) => { if (v == null || v === '') return ''; const s = Math.floor(+v); const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), x = s % 60; return (h ? h + ':' + String(m).padStart(2, '0') : m) + ':' + String(x).padStart(2, '0'); }, // 秒 → "3:25"
  monthly: (v) => (Array.isArray(v) ? v.map((m) => m.search_volume ?? '').join(' / ') : ''), // 月別の配列 → "2900 / 3600 / …"（新しい月から）
  slash: (v) => (Array.isArray(v) ? v.join(' / ') : String(v ?? '')), // [45, 36] → "45 / 36"
  round0: (v) => (typeof v === 'number' ? Math.round(v) : v),
  round2: (v) => (typeof v === 'number' ? Math.round(v * 100) / 100 : v),
  ids: (v) => (Array.isArray(v) ? v.map((a) => a.advertiser_id).join(', ') : String(v ?? '')), // 広告主IDの配列 → "AR..., AR..."
};

// 動画URL（watch?v= / youtu.be / shorts / embed）か動画IDから、11文字の動画IDを取り出す。取れなければ null
export function parseVideoId(s) {
  const v = String(s ?? '').trim();
  if (/^[\w-]{11}$/.test(v)) return v;
  const m = v.match(/(?:[?&]v=|youtu\.be\/|\/shorts\/|\/embed\/|\/live\/)([\w-]{11})/);
  return m ? m[1] : null;
}

// from が配列なら、最初に値がある項目を使う
const pick = (it, from) => { for (const f of [].concat(from)) { const v = get(it, f); if (v != null && v !== '') return v; } return undefined; };

// 文章で返ってくるツール（AIモードなど）：回答文をそのまま取り出す
//   answer.markdown = 回答文の場所 ／ answer.sections = true なら、LLMの message の sections の text をつなぐ
export const extractAnswer = (cfg, task) => {
  const a = cfg.result.answer;
  if (!a) return '';
  if (a.sections) {
    return (get(task, a.items || 'result.0.items') || []).filter((it) => it.type === 'message')
      .flatMap((it) => (it.sections || []).map((s) => s.text)).filter(Boolean).join('\n\n');
  }
  return get(task, a.markdown) || '';
};

// 1つの表の行を取り出す。spec = { items, where, flatten, unique, columns }
//   flatten: 配列の入れ子を平らにする（例 ["sections","annotations"]）／ unique: 同じ値の行を1つにする項目
export function rowsOf(spec, task) {
  let list = (get(task, spec.items) || []).filter((it) => Object.entries(spec.where || {}).every(([k, v]) => (Array.isArray(v) ? v.includes(it[k]) : it[k] === v)));
  for (const k of spec.flatten || []) list = list.flatMap((it) => it[k] || []);
  let rows = list.map((it) => Object.fromEntries(spec.columns.map((c) => {
    if (c.join) return [c.key, c.join.map((k) => { const v = get(it, k); return typeof v === 'number' && v < 10 ? String(v).padStart(2, '0') : v; }).join(c.sep ?? '-')];
    const v = pick(it, c.from || c.key);
    return [c.key, c.transform ? transforms[c.transform](v) : v];
  })));
  if (spec.unique) { const seen = new Set(); rows = rows.filter((r) => { const k = r[spec.unique]; if (!k || seen.has(k)) return false; seen.add(k); return true; }); }
  return rows;
}

export function extractRows(cfg, task) {
  const r = cfg.result;
  if (r.answer_only) return [{ answer: extractAnswer(cfg, task) }]; // 回答文だけのツール：CSVは回答文1行
  return rowsOf(r, task);
}
export const extractExtra = (cfg, task) => (cfg.result.extra || []).map((x) => ({ ...x, rows: rowsOf(x, task) }));
