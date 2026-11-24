// 結果の取り出し（tool.js とチェック用スクリプトで共用。画面にもNodeにも依存しない）
export const get = (o, path) => path.split('.').reduce((a, k) => (a == null ? a : a[k]), o);
export const transforms = {
  strip_www: (v) => String(v ?? '').replace(/^www\./, ''),
  date: (v) => String(v ?? '').slice(0, 10), // "2026-11-22 04:50:16 +00:00" → "2026-11-22"
  mmss: (v) => { if (v == null || v === '') return ''; const s = Math.floor(+v); const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), x = s % 60; return (h ? h + ':' + String(m).padStart(2, '0') : m) + ':' + String(x).padStart(2, '0'); }, // 秒 → "3:25"
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
export const extractAnswer = (cfg, task) => (cfg.result.answer ? get(task, cfg.result.answer.markdown) || '' : '');

export function extractRows(cfg, task) {
  const r = cfg.result;
  return (get(task, r.items) || [])
    .filter((it) => Object.entries(r.where || {}).every(([k, v]) => (Array.isArray(v) ? v.includes(it[k]) : it[k] === v)))
    .map((it) => Object.fromEntries(r.columns.map((c) => {
      const v = pick(it, c.from || c.key);
      return [c.key, c.transform ? transforms[c.transform](v) : v];
    })));
}
