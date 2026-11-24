// 結果の取り出し（tool.js とチェック用スクリプトで共用。画面にもNodeにも依存しない）
export const get = (o, path) => path.split('.').reduce((a, k) => (a == null ? a : a[k]), o);
export const transforms = {
  strip_www: (v) => String(v ?? '').replace(/^www\./, ''),
  date: (v) => String(v ?? '').slice(0, 10), // "2026-11-22 04:50:16 +00:00" → "2026-11-22"
};

// 文章で返ってくるツール（AIモードなど）：回答文をそのまま取り出す
export const extractAnswer = (cfg, task) => (cfg.result.answer ? get(task, cfg.result.answer.markdown) || '' : '');

export function extractRows(cfg, task) {
  const r = cfg.result;
  return (get(task, r.items) || [])
    .filter((it) => Object.entries(r.where || {}).every(([k, v]) => it[k] === v))
    .map((it) => Object.fromEntries(r.columns.map((c) => {
      const v = get(it, c.from || c.key);
      return [c.key, c.transform ? transforms[c.transform](v) : v];
    })));
}
