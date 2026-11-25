# 記事用の全データ表（articles/_inc/*.html）と、ダウンロード用CSV（site/articles/data/*.csv）を、保存済みの生データから作る
import json, csv, html, io
R = '/home/user/tools/'
D = R + '2026_11/articles/data/'
INC = R + 'articles/_inc/'
OUT = R + 'site/articles/data/'
e = html.escape
def load(f):
    return json.load(open(D + f, encoding='utf-8'))['tasks'][0]['result']
def months(rows):
    ms = {}
    for r in rows:
        for m in (r.get('monthly_searches') or []):
            ms[(m['year'], m['month'])] = 1
    return sorted(ms)  # 古い月から
def monthly_map(r):
    return {(m['year'], m['month']): m['search_volume'] for m in (r.get('monthly_searches') or [])}
def num(v, f='{:,}'):
    return '' if v is None else f.format(v)
def cell_vol(v):
    return '空欄' if v is None else f'{v:,}'
def write_csv(name, header, rows):
    with open(OUT + name, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)
def c24_table(rows, ms):
    head = ['キーワード', '月間検索数', '競合度(0-100)', '競合ラベル', 'CPC(USD)', '入札額・下限(USD)', '入札額・上限(USD)'] + [f'{y}-{m:02d}' for y, m in ms]
    tr = []
    csvrows = []
    for r in rows:
        mm = monthly_map(r)
        cells = [r['keyword'], r['search_volume'], r['competition_index'], r['competition'], r['cpc'], r['low_top_of_page_bid'], r['high_top_of_page_bid']] + [mm.get(k) for k in ms]
        csvrows.append(['' if c is None else c for c in cells])
        tds = [e(r['keyword']), cell_vol(r['search_volume']), num(r['competition_index']), e(r['competition'] or ''), num(r['cpc'], '{}'), num(r['low_top_of_page_bid'], '{}'), num(r['high_top_of_page_bid'], '{}')] + [num(mm.get(k)) for k in ms]
        tr.append('<tr>' + ''.join(f'<td>{t}</td>' for t in tds) + '</tr>')
    th = ''.join(f'<th>{e(h)}</th>' for h in head)
    return f'<div class="scroll"><table class="data">\n<thead><tr>{th}</tr></thead>\n<tbody>\n' + '\n'.join(tr) + '\n</tbody></table></div>', head, csvrows

# --- 538語
r538 = load('C24_538_2026-11-25.json'); ms = months(r538)
t, head, rows = c24_table(r538, ms)
write_csv('c24-538-keywords-2026-11-25.csv', head, rows)
open(INC + 'table538.html', 'w', encoding='utf-8').write(t)
empties = [r['keyword'] for r in r538 if r['search_volume'] is None]
open(INC + 'empties.html', 'w', encoding='utf-8').write('<ol class="cols">\n' + '\n'.join(f'<li>{e(k)}</li>' for k in empties) + '\n</ol>')
# 数字あり 202語（検索数の多い順）
withv = sorted([r for r in r538 if r['search_volume'] is not None], key=lambda r: -r['search_volume'])
open(INC + 'volumes_sorted.html', 'w', encoding='utf-8').write('<div class="scroll"><table class="data">\n<thead><tr><th>順位</th><th>キーワード</th><th>月間検索数</th></tr></thead>\n<tbody>\n' + '\n'.join(f'<tr><td>{i}</td><td>{e(r["keyword"])}</td><td>{r["search_volume"]:,}</td></tr>' for i, r in enumerate(withv, 1)) + '\n</tbody></table></div>')
vals = sorted(r['search_volume'] for r in withv)
print('538:', len(r538), 'empty', len(empties), 'values', len(vals), 'median', vals[len(vals) // 2], 'max', vals[-1], 'months', ms[0], ms[-1])
b = {'10以下': 0, '20〜90': 0, '100〜990': 0, '1,000以上': 0}
for v in vals:
    b['10以下' if v <= 10 else '20〜90' if v < 100 else '100〜990' if v < 1000 else '1,000以上'] += 1
print(b)
# --- 1,200語
r1200 = load('C24_1199_part1_2026-11-25.json') + load('C24_1199_part2_2026-11-25.json')
ms2 = months(r1200)
t2, head2, rows2 = c24_table(r1200, ms2)
write_csv('c24-1200-keywords-2026-11-25.csv', head2, rows2)
open(INC + 'table1200.html', 'w', encoding='utf-8').write(t2)
nv = sum(1 for r in r1200 if r['search_volume'] is not None)
print('1200:', len(r1200), 'values', nv, 'empty', len(r1200) - nv)
# --- 10語の比較
raw = open(D + 'KeywordPlanner_stats_2026-11-25.csv', 'rb').read().decode('utf-16')
kp = {}
rd = list(csv.reader(io.StringIO(raw), delimiter='\t'))
hdr = [i for i, x in enumerate(rd) if x and x[0] == 'Keyword'][0]
H = rd[hdr]
for x in rd[hdr + 1:]:
    if len(x) > 7 and x[0] and x[2] == '':
        kp[x[0]] = dict(zip(H, x))
open(OUT + 'keyword-planner-stats-2026-11-25.csv', 'w', encoding='utf-8-sig', newline='').write(raw.replace('\t', ',') if False else '')
with open(OUT + 'keyword-planner-stats-2026-11-25.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    for x in rd:
        if x: w.writerow(x)
a = load('C24_10words_2026-11-25.json'); bsp = load('C24_10words_kpspelling_2026-11-25.json')
amap = {r['keyword']: r for r in a}; bmap = {r['keyword']: r for r in bsp}
order = list(bmap)  # キーワードプランナーの表示どおり（スペース入り）
orig = ["meo 対策", "serp 分析", "キーワードプランナー", "キーワード 検索ボリューム", "検索順位 チェック", "検索結果 上位 調べる", "検索ボリューム 調べる", "SERP 分析", "検索ボリューム 推移", "検索ボリューム 一括", "検索意図 調べる"]
same = True
for k, r in bmap.items():
    o = [x for x in a if x['keyword'].replace(' ', '').lower() == k.replace(' ', '').lower()]
    assert len(o) == 1, k
    if o[0]['search_volume'] != r['search_volume'] or o[0]['competition_index'] != r['competition_index']: same = False
print('spacing identical:', same)
def kpv(k):
    v = kp.get(k, {}).get('Avg. monthly searches', '')
    return float(v) if v not in ('', None) else None
rows4 = []; tr = []
for k in ['meo 対策', 'serp 分析', 'キーワード プランナー', 'キーワード 検索 ボリューム', '検索 ボリューム 一括', '検索 ボリューム 推移', '検索 ボリューム 調べる', '検索 順位 チェック', '検索 意図 調べる', '検索 結果 上位 調べる']:
    c = bmap[k]; p = kp.get(k, {})
    mm = monthly_map(c)
    kv = kpv(k)
    row = [k, int(kv) if kv is not None else '', p.get('Competition', ''), p.get('Competition (indexed value)', ''), p.get('Top of page bid (low range)', ''), p.get('Top of page bid (high range)', ''), p.get('Three month change', ''), p.get('YoY change', ''),
           c['search_volume'] if c['search_volume'] is not None else '', c['competition_index'] if c['competition_index'] is not None else '', c['competition'] or '', c['cpc'] if c['cpc'] is not None else '', c['low_top_of_page_bid'] if c['low_top_of_page_bid'] is not None else '', c['high_top_of_page_bid'] if c['high_top_of_page_bid'] is not None else ''] + [mm.get(m, '') for m in ms]
    rows4.append(row)
head4 = ['キーワード', 'KP:月間検索数', 'KP:競合性', 'KP:競合性(指数)', 'KP:入札額・低(THB)', 'KP:入札額・高(THB)', 'KP:3か月の変化', 'KP:前年比', 'C24:月間検索数', 'C24:競合度(0-100)', 'C24:競合ラベル', 'C24:CPC(USD)', 'C24:入札額・下限(USD)', 'C24:入札額・上限(USD)'] + [f'C24:{y}-{m:02d}' for y, m in ms]
write_csv('keyword-planner-vs-c24-10words-2026-11-25.csv', head4, rows4)
th = ''.join(f'<th>{e(h)}</th>' for h in head4)
def show(v):
    return '空欄' if v == '' else (f'{v:,}' if isinstance(v, int) else e(str(v)))
for r in rows4:
    tr.append('<tr>' + ''.join(f'<td>{show(v) if i in (1, 8) else e(str(v))}</td>' for i, v in enumerate(r)) + '</tr>')
open(INC + 'table10.html', 'w', encoding='utf-8').write(f'<div class="scroll"><table class="data">\n<thead><tr>{th}</tr></thead>\n<tbody>\n' + '\n'.join(tr) + '\n</tbody></table></div>')
print('kp rows', len(kp), 'months', ms[0], ms[-1])
