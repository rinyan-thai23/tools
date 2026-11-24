// DataForSEO 呼び出しとエラー処理。各ツールでは書かない。
const KEY = 'dfs_creds';
const BASE = 'https://api.dataforseo.com/v3/';

export function getCreds() {
  try { return JSON.parse(localStorage.getItem(KEY) || 'null'); } catch { return null; }
}
export function setCreds(login, password) {
  try { localStorage.setItem(KEY, JSON.stringify({ login, password })); } catch {}
}
export function clearCreds() {
  try { localStorage.removeItem(KEY); } catch {}
}

export class ApiError extends Error {
  constructor(key) { super(key); this.key = key; }
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function extraParams(path, body) {
  const p = { ...body };
  if (path.startsWith('serp/google/organic/')) { p.resolve_goto_urls = true; p.resolve_poisoned_results = true; }
  else if (/^serp\/google\/(news|local_finder|search_by_image)\//.test(path)) p.resolve_goto_urls = true;
  return p;
}

// path 例: 'serp/google/organic/live/advanced'。body は1タスク分のオブジェクト。
// 戻り値: { task, cost, time }。失敗時は ApiError(key) → locale の err.<key>
export async function callApi(path, body, { onRetry } = {}) {
  const c = getCreds();
  if (!c || !c.login || !c.password) throw new ApiError('nokey');
  const auth = 'Basic ' + btoa(c.login + ':' + c.password);
  let lastErr = 'busy';
  for (let i = 0; i < 3; i++) {
    const ctl = new AbortController();
    const timer = setTimeout(() => ctl.abort(), 300000);
    try {
      const res = await fetch(BASE + path, {
        method: 'POST', signal: ctl.signal,
        headers: { Authorization: auth, 'Content-Type': 'application/json' },
        body: JSON.stringify([extraParams(path, body)]),
      });
      const json = await res.json();
      const task = json.tasks && json.tasks[0];
      const code = (task && task.status_code) || json.status_code;
      if (code === 20000 && task) return { task, cost: task.cost, time: new Date() };
      if (code === 40100) throw new ApiError('40100');
      if (code === 40210) throw new ApiError('40210');
      if (code === 40207) throw new ApiError('40207');
      if (code === 40102) throw new ApiError('40102');
      if (code === 40101 || code === 40103 || code === 50301) { lastErr = 'busy'; if (i < 2 && onRetry) onRetry(i + 2); await sleep(1500 * (i + 1)); continue; }
      throw new ApiError('other');
    } catch (e) {
      if (e instanceof ApiError) throw e;
      lastErr = 'busy';
      if (i < 2 && onRetry) onRetry(i + 2);
      await sleep(1500 * (i + 1));
    } finally { clearTimeout(timer); }
  }
  throw new ApiError(lastErr);
}

// 無料の参照データ（GET）を取る。失敗したら null（呼び出し側は、なくても表示できるようにする）
export async function getApi(path) {
  const c = getCreds();
  if (!c || !c.login || !c.password) return null;
  try {
    const res = await fetch(BASE + path, { headers: { Authorization: 'Basic ' + btoa(c.login + ':' + c.password) } });
    const json = await res.json();
    const task = json.tasks && json.tasks[0];
    return task && task.status_code === 20000 ? task : null;
  } catch { return null; }
}
