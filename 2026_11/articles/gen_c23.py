import json,csv,html,statistics,collections
R='/home/user/tools/'; D=R+'2026_11/articles/data/'; INC=R+'articles/_inc/'; OUT=R+'site/articles/data/'
e=html.escape
ai=json.load(open(D+'C23_538_2026-11-25.json'))['tasks'][0]['result'][0]['items']
g={x['keyword'].lower():x for x in json.load(open(D+'C24_538_2026-11-25.json'))['tasks'][0]['result']}
def mm(x,key): return {(m['year'],m['month']):m['search_volume' if key=='g' else 'ai_search_volume'] for m in (x.get('monthly_searches' if key=='g' else 'ai_monthly_searches') or [])}
months=sorted(mm(ai[0],'a')); H=[f'{y}-{m:02d}' for y,m in months]
def wcsv(name,head,rows):
    with open(OUT+name,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f); w.writerow(head); w.writerows(rows)
def tbl(head,rows):
    return '<div class="scroll"><table class="data">\n<thead><tr>'+''.join(f'<th>{e(h)}</th>' for h in head)+'</tr></thead>\n<tbody>\n'+'\n'.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)+'\n</tbody></table></div>'
def pear(a,b):
    n=len(a); ma=sum(a)/n; mb=sum(b)/n
    sa=sum((x-ma)**2 for x in a)**.5; sb=sum((x-mb)**2 for x in b)**.5
    return None if sa==0 or sb==0 else sum((x-ma)*(y-mb) for x,y in zip(a,b))/(sa*sb)
rows=[];csv1=[];cmp_rows=[];csv2=[];nz=[]
for x in ai:
    k=x['keyword']; am=mm(x,'a'); gx=g[k]; gv=gx['search_volume']; av=x['ai_search_volume']
    csv1.append([k,av]+[am.get(m,'') for m in months])
    rows.append([e(k),str(av)]+[str(am.get(m,'')) for m in months])
    ratio=''
    if gv and av: ratio=round(av/gv*100,1)
    csv2.append([k,'' if gv is None else gv,av,ratio])
    cmp_rows.append([e(k),'空欄' if gv is None else f'{gv:,}',str(av),str(ratio) if ratio!='' else ''])
    if av>0: nz.append((k,av,gv,am,mm(gx,'g')))
wcsv('c23-538-ai-volumes-2026-11-25.csv',['キーワード','AIでの質問回数(月間)']+H,csv1)
open(INC+'c23_table538.html','w',encoding='utf-8').write(tbl(['キーワード','AIでの質問回数(直近)']+H,rows))
wcsv('c23-vs-google-538-2026-11-25.csv',['キーワード','Google月間検索数(C24)','AI質問回数(C23)','AI÷Google(%)'],csv2)
open(INC+'c23_cmp538.html','w',encoding='utf-8').write(tbl(['キーワード','Googleの月間検索数（C24）','AIでの質問回数（C23）','AI÷Google（%）'],cmp_rows))
nz.sort(key=lambda r:-r[1])
open(INC+'c23_nonzero.html','w',encoding='utf-8').write(tbl(['キーワード','AIでの質問回数','Googleの月間検索数（C24）'],[[e(k),str(av),'空欄' if gv is None else f'{gv:,}'] for k,av,gv,_,_ in nz]))
# 月ごとの比較（AI>0 上位15）
trows=[];tcsv=[];cors=[]
for k,av,gv,am,gm in nz[:15]:
    a=[am[m] for m in months]; gg=[gm.get(m) for m in months]
    r=pear(a,gg) if None not in gg else None
    cors.append((k,r))
    trows.append([e(k),'AI']+[str(am[m]) for m in months]+['']); trows.append(['','Google']+[('' if gm.get(m) is None else f'{gm[m]:,}') for m in months]+['' if r is None else f'{r:.2f}'])
    tcsv.append([k,'AI']+[am[m] for m in months]+['']);tcsv.append([k,'Google']+[gm.get(m,'') for m in months]+[('' if r is None else round(r,2))])
wcsv('c23-monthly-top15-2026-11-25.csv',['キーワード','種類']+H+['相関係数'],tcsv)
open(INC+'c23_monthly.html','w',encoding='utf-8').write(tbl(['キーワード','種類']+H+['動きの似かた（相関係数）'],trows))
av=[x['ai_search_volume'] for x in ai]
both=[(k,gm['search_volume'],a['ai_search_volume']) for a in ai for k in [a['keyword']] for gm in [g[k]]]
gv_pos=[b for b in both if b[1]]; gv_empty=[b for b in both if b[1] is None]
bins=collections.Counter('0' if v==0 else '1〜9' if v<10 else '10〜99' if v<100 else '100以上' for v in av)
gz=[b for b in gv_pos if b[2]==0]
st=dict(n=len(ai),zero=sum(1 for v in av if v==0),nz=len(nz),bins=dict(bins),maxv=max(av),max_kw=nz[0][0],top10=[(k,a,gg) for k,a,gg,_,_ in nz[:10]],
  gv_pos=len(gv_pos),gv_empty=len(gv_empty),gempty_nonzero=sum(1 for b in gv_empty if b[2]>0),gpos_zero=len(gz),gpos_nonzero=len(gv_pos)-len(gz),
  ai_gt_g=[(b[0],b[2],b[1]) for b in gv_pos if b[2]>b[1]],ratio_med=round(statistics.median([b[2]/b[1]*100 for b in gv_pos if b[2]>0]),1),
  cors=[(k,None if r is None else round(r,2)) for k,r in cors],cost=0.0638,sum_ai=sum(av),sum_g=sum(b[1] for b in gv_pos),
  months=[H[0],H[-1]],g_gt1000=[(b[0],b[1],b[2]) for b in gv_pos if b[1]>=1000][:60],g_gt1000_n=sum(1 for b in gv_pos if b[1]>=1000),g_gt1000_zero=sum(1 for b in gv_pos if b[1]>=1000 and b[2]==0))
json.dump(st,open(INC+'c23_stats.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(json.dumps(st,ensure_ascii=False)[:2400])
