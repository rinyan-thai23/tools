# C01記事用: 保存済みの生データから全データ表(articles/_inc)とCSV(site/articles/data)を作り、数える
import json, csv, html, glob, collections, re, sys
R = '/home/user/tools/'; D = R + '2026_11/articles/data/'; INC = R + 'articles/_inc/'; OUT = R + 'site/articles/data/'
e = html.escape
DATE = sys.argv[1] if len(sys.argv) > 1 else '2026-11-25'
def res(f):
    return json.load(open(D + f, encoding='utf-8'))['tasks'][0]['result'][0]
def wcsv(name, head, rows):
    with open(OUT + name, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f); w.writerow(head); w.writerows(rows)
def tbl(head, rows, cls='data'):
    return f'<div class="scroll"><table class="{cls}">\n<thead><tr>' + ''.join(f'<th>{e(h)}</th>' for h in head) + '</tr></thead>\n<tbody>\n' + '\n'.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '\n</tbody></table></div>'
# ---- 記事1: 上位100件
r = res(f'C01_blog100_{DATE}.json')
org = [i for i in r['items'] if i['type'] == 'organic']
head = ['順位', '全体の位置(rank_absolute)', 'タイトル', 'URL', 'ドメイン', '説明文']
rows = [[i['rank_group'], i['rank_absolute'], i['title'] or '', i['url'] or '', i['domain'] or '', i.get('description') or ''] for i in org]
wcsv(f'c01-blog-100-{DATE}.csv', head, rows)
open(INC + 'c01_table100.html', 'w', encoding='utf-8').write(tbl(head, [[c if isinstance(c, int) else e(str(c)) for c in x] for x in rows]))
print('100:', len(org), 'types', dict(collections.Counter(i['type'] for i in r['items'])))
# ---- 記事3: 数える
titles = [i['title'] or '' for i in org]
L = [len(t) for t in titles]
IST = lambda t: ('...' in t) or ('…' in t)
trunc = sum(1 for t in titles if IST(t))
st = {
 '件数': len(titles), '省略(…)で終わる': trunc,
 '【】を含む': sum('【' in t for t in titles), '年号(20xx)を含む': sum(bool(re.search(r'20\d\d', t)) for t in titles),
 '「初心者」を含む': sum('初心者' in t for t in titles), '「始め方」を含む': sum('始め方' in t for t in titles), '「ブログ」を含む': sum('ブログ' in t for t in titles),
 '「完全」を含む': sum('完全' in t for t in titles), '「おすすめ」を含む': sum('おすすめ' in t for t in titles), '「無料」を含む': sum('無料' in t for t in titles),
 '最短': min(L), '最長': max(L), '中央値': sorted(L)[len(L) // 2], '平均': round(sum(L) / len(L), 1)}
print(st)
# 省略されていないタイトルだけの文字数
NT = [t for t in titles if not IST(t)]
L2 = [len(t) for t in NT]
NTC = {k: sum(1 for t in NT if f(t)) for k, f in {'【】': lambda t: '【' in t, '年号': lambda t: bool(re.search(r'20\d\d', t)), '初心者': lambda t: '初心者' in t, '始め方': lambda t: '始め方' in t, 'ブログ': lambda t: 'ブログ' in t, '完全': lambda t: '完全' in t, '無料': lambda t: '無料' in t, 'おすすめ': lambda t: 'おすすめ' in t}.items()}
print('NTC', NTC)
print('non-trunc', len(L2), min(L2), max(L2), sorted(L2)[len(L2) // 2])
bins = collections.Counter()
for n in L: bins[(n // 10) * 10] += 1
dom = collections.Counter(i['domain'] for i in org)
print('domains', len(dom), dom.most_common(12))
open(INC + 'c01_stats.json', 'w', encoding='utf-8').write(json.dumps({'st': st, 'bins': sorted(bins.items()), 'dom': dom.most_common(), 'nontrunc': [len(L2), min(L2), max(L2), sorted(L2)[len(L2) // 2]], 'ntc': NTC, 'nbins': sorted(collections.Counter((n // 10) * 10 for n in L2).items()), 'avg_nt': round(sum(L2) / len(L2), 1)}, ensure_ascii=False))
# 全タイトルの文字数つき表
head3 = ['順位', 'タイトル', '文字数', '省略(…)']
rows3 = [[i['rank_group'], e(i['title'] or ''), len(i['title'] or ''), '○' if IST(i['title'] or '') else ''] for i in org]
open(INC + 'c01_titles.html', 'w', encoding='utf-8').write(tbl(head3, rows3))
open(INC + 'c01_domains.html', 'w', encoding='utf-8').write(tbl(['ドメイン', '上位100件に出た回数'], [[e(d), n] for d, n in dom.most_common()]))
wcsv(f'c01-blog-100-domains-{DATE}.csv', ['ドメイン', '回数'], dom.most_common())
# ---- 記事2: 20語
files = sorted(glob.glob(D + f'C01_kw*_{DATE}.json'))
allrows = []; summ = []; types = collections.Counter()
for f in files:
    j = json.load(open(f, encoding='utf-8'))['tasks'][0]; x = j['result'][0]
    kw = x['keyword']; its = x['items']
    c = collections.Counter(i['type'] for i in its); types.update(c.keys())
    summ.append((kw, len(its), c))
    for i in its:
        allrows.append([kw, i['rank_absolute'], i['rank_group'], i['type'], i.get('title') or '', i.get('url') or '', i.get('domain') or ''])
tl = sorted(types, key=lambda t: (-types[t], t))
print('kw files', len(files), 'types', dict(types))
head2 = ['キーワード', '全項目数'] + tl
rows2 = [[e(k), n] + [c.get(t, 0) for t in tl] for k, n, c in summ]
# 青いリンクの本数と、それ以外の項目の数
open(INC + 'c01_types.html', 'w', encoding='utf-8').write(tbl(head2, rows2))
wcsv(f'c01-20keywords-types-{DATE}.csv', ['キーワード', '全項目数'] + tl, [[k, n] + [c.get(t, 0) for t in tl] for k, n, c in summ])
head2b = ['キーワード', '全体の位置', '順位(種類内)', '種類', 'タイトル', 'URL', 'ドメイン']
wcsv(f'c01-20keywords-items-{DATE}.csv', head2b, allrows)
open(INC + 'c01_items.html', 'w', encoding='utf-8').write(tbl(head2b, [[e(str(c)) for c in x] for x in allrows]))
json.dump([[k, n, dict(c)] for k, n, c in summ], open(INC + 'c01_types.json', 'w', encoding='utf-8'), ensure_ascii=False)
