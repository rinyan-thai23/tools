// 国と言語の一覧を、DataForSEOの無料の一覧（$0）から作る。ときどき手で1回だけ実行する。
//   node scripts/gen-markets.mjs
// 出力：site/shared/markets.generated.json（国コード・ISO・APIの系統ごとの対応・言語）
// 名前（日本語・英語など）は入れない。画面側が Intl.DisplayNames で、ISOコード／言語コードから作る。
import { execFileSync } from 'node:child_process';
import { mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const dir = mkdtempSync(join(tmpdir(), 'mk-'));
const get = (path) => {
  const f = join(dir, path.replace(/\//g, '_') + '.json');
  execFileSync('curl', ['-s', '--fail', '-m', '300', `https://api.dataforseo.com/v3/${path}`, '-o', f]); // 認証はプロキシが付ける（無料）
  const d = JSON.parse(readFileSync(f, 'utf8'));
  if (d.status_code !== 20000 || d.cost) throw new Error(`${path}: ${d.status_code} cost=${d.cost}`);
  return d.tasks[0].result;
};
const countries = {}; // code -> [ISO, 英語名]
const fam = {};       // 系統 -> [国コード]
const addLoc = (name, rows, all = false) => { // all：Labs系は全部が国
  const cs = rows.filter((x) => all || !x.location_code_parent); // 親が無い行＝国・地域（台湾・香港・バミューダなどは Region で返る）
  fam[name] = cs.map((x) => x.location_code).sort((a, b) => a - b);
  for (const x of cs) if (!countries[x.location_code] || (!countries[x.location_code][0] && x.country_iso_code)) countries[x.location_code] = [x.country_iso_code || '', x.location_name];
};
addLoc('serp', get('serp/google/locations'));
addLoc('yt', get('serp/youtube/locations'));
addLoc('ads', get('keywords_data/google_ads/locations'));
addLoc('gt', get('keywords_data/google_trends/locations'));
addLoc('dt', get('keywords_data/dataforseo_trends/locations'));
addLoc('llm', get('ai_optimization/chat_gpt/llm_scraper/locations'));
const perCountry = {}; // 国ごとに言語が決まっている系統
for (const [name, path] of [['labs', 'dataforseo_labs/locations_and_languages'], ['aikw', 'ai_optimization/ai_keyword_data/locations_and_languages']]) {
  const rows = get(path);
  addLoc(name, rows, true);
  perCountry[name] = Object.fromEntries(rows.map((x) => [x.location_code, x.available_languages.map((l) => l.language_code)]));
}
for (const c of Object.values(countries)) if (!c[0]) console.warn('ISOなし:', c[1]); // 画面では英語名を使う
const langNames = {}; // 英語名（Intl が知らない言語のときの予備）
const langs = {};     // 系統 -> [言語コード]（全国共通の系統）
for (const [name, path] of [['serp', 'serp/google/languages'], ['yt', 'serp/youtube/languages'], ['ads', 'keywords_data/google_ads/languages'], ['gt', 'keywords_data/google_trends/languages'], ['llm', 'ai_optimization/chat_gpt/llm_scraper/languages']]) {
  const r = get(path);
  langs[name] = r.map((x) => x.language_code);
  for (const x of r) langNames[x.language_code] ||= x.language_name;
}
for (const name of Object.keys(perCountry)) {
  langs[name] = [...new Set(Object.values(perCountry[name]).flat())].sort();
  for (const x of get(name === 'labs' ? 'dataforseo_labs/locations_and_languages' : 'ai_optimization/ai_keyword_data/locations_and_languages')) for (const l of x.available_languages) langNames[l.language_code] ||= l.language_name;
}
const out = { generated: new Date().toISOString().slice(0, 10), countries, fam, langs, perCountry, langNames };
writeFileSync('site/shared/markets.generated.json', JSON.stringify(out) + '\n');
console.log('countries', Object.keys(countries).length, Object.fromEntries(Object.entries(fam).map(([k, v]) => [k, v.length])), Object.fromEntries(Object.entries(langs).map(([k, v]) => [k, v.length])));
