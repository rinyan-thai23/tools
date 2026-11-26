import json,html
exec(open('gen_tables.py').read().split("json.dump")[0]) if False else None
import runpy
g=runpy.run_path('gen_tables.py')
rows=g['rows']; months=g['months']; ORDER=g['ORDER']; C=g['C']
def f(v): return '空欄' if v is None else f'{v:,}'
last=months[-1]
byt={}
for r in rows: byt.setdefault(r['tag'],[]).append(r)
def matrix(get,title):
    h='<div class="scroll"><table>\n<thead><tr><th>国（語の言語）</th>'+''.join(f'<th>{c}</th>' for c in C)+'</tr></thead>\n<tbody>\n'
    for tag,c,l in ORDER:
        h+=f'<tr><td>{c}（{l}）</td>'+''.join(f'<td>{f(get(r))}</td>' for r in byt[tag])+'</tr>\n'
    return h+'</tbody></table></div>\n'
M1=matrix(lambda r:r['vol'],'avg'); M2=matrix(lambda r:r['m'].get(last),'last')
# 全データ
h='<div class="scroll"><table>\n<thead><tr><th>国</th><th>語の言語</th><th>意味</th><th>キーワード</th><th>12か月の数字（API）</th><th>競合度</th><th>CPC(USD)</th><th>入札額 下限〜上限(USD)</th>'+''.join(f'<th>{y}-{m:02d}</th>' for y,m in months)+'</tr></thead>\n<tbody>\n'
for r in rows:
    h+=f"<tr><td>{r['country']}</td><td>{r['lang']}</td><td>{r['concept']}</td><td>{html.escape(r['kw'])}</td><td>{f(r['vol'])}</td><td>{f(r['ci'])}</td><td>{f(r['cpc'])}</td><td>{f(r['lo'])}〜{f(r['hi'])}</td>"+''.join(f'<td>{f(r["m"].get(k))}</td>' for k in months)+'</tr>\n'
FULL=h+'</tbody></table></div>\n'
open('/home/user/tools/articles/_inc/ml13_avg.html','w').write(M1)
open('/home/user/tools/articles/_inc/ml13_last.html','w').write(M2)
open('/home/user/tools/articles/_inc/ml13_full.html','w').write(FULL)
print(M2)
