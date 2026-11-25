import json,csv,html,glob,statistics,collections,re
R='/home/user/tools/'; D=R+'2026_11/articles/data/c62/'; INC=R+'articles/_inc/'; OUT=R+'site/articles/data/'
e=html.escape
def wcsv(name,head,rows):
    with open(OUT+name,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f); w.writerow(head); w.writerows(rows)
def tbl(head,rows):
    return '<div class="scroll"><table class="data">\n<thead><tr>'+''.join(f'<th>{e(h)}</th>' for h in head)+'</tr></thead>\n<tbody>\n'+'\n'.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)+'\n</tbody></table></div>'
CATS=['performance','accessibility','best-practices','seo']; CN={'performance':'パフォーマンス','accessibility':'アクセシビリティ','best-practices':'ベストプラクティス','seo':'SEO'}
MET=['first-contentful-paint','largest-contentful-paint','total-blocking-time','cumulative-layout-shift','speed-index']; MN={'first-contentful-paint':'FCP','largest-contentful-paint':'LCP','total-blocking-time':'TBT','cumulative-layout-shift':'CLS','speed-index':'Speed Index'}
def load(name):
    t=json.load(open(D+name+'_2026-11-25.json'))['tasks'][0]
    if t['status_code']!=20000: return None,t
    r=(t.get('result') or [None])[0]
    return r,t
def rec(r,t):
    sc={c:(None if r['categories'][c]['score'] is None else round(r['categories'][c]['score']*100)) for c in CATS}
    me={m:(r['audits'][m].get('displayValue','').replace('\xa0',' '),r['audits'][m].get('numericValue')) for m in MET}
    return sc,me
def t_sec(t):
    m=re.match(r'([\d.]+)',t.get('time','') or ''); return float(m.group(1)) if m else None
# ---- A
A=[];AERR=[];times=[]
for f in sorted(glob.glob(D+'A*_2026-11-25.json')):
    name=f.split('/')[-1].replace('_2026-11-25.json',''); dom=name.split('_',1)[1]
    r,t=load(name)
    if r is None:
        AERR.append((dom,t['status_message'].split('code: ')[-1][:40])); continue
    sc,me=rec(r,t); times.append(t_sec(t))
    A.append(dict(dom=dom,req=r['requestedUrl'],fin=r['finalUrl'],sc=sc,me=me))
head=['サイト','測った URL','最終的に開いた URL']+[CN[c] for c in CATS]+[MN[m] for m in MET]
rows=[[e(a['dom']),e(a['req']),e(a['fin'])]+[str(a['sc'][c]) for c in CATS]+[e(a['me'][m][0]) for m in MET] for a in A]
wcsv('c62-30sites-mobile-2026-11-25.csv',head,[[a['dom'],a['req'],a['fin']]+[a['sc'][c] for c in CATS]+[a['me'][m][0] for m in MET] for a in A])
open(INC+'c62_sites.html','w',encoding='utf-8').write(tbl(head,rows))
open(INC+'c62_errors.html','w',encoding='utf-8').write(tbl(['サイト','エラーの内容（Lighthouseのコード）'],[[e(d),e(m)] for d,m in AERR]))
# 分布
dist={}
for c in CATS:
    v=[a['sc'][c] for a in A if a['sc'][c] is not None]
    dist[c]=dict(n=len(v),min=min(v),max=max(v),med=statistics.median(v),sd=round(statistics.pstdev(v),1),rng=max(v)-min(v))
open(INC+'c62_dist.html','w',encoding='utf-8').write(tbl(['点数','サイト数','最低','中央値','最高','最高−最低','標準偏差'],[[CN[c],str(dist[c]['n']),str(dist[c]['min']),str(dist[c]['med']),str(dist[c]['max']),str(dist[c]['rng']),str(dist[c]['sd'])] for c in CATS]))
srt=sorted(A,key=lambda a:-(a['sc']['performance'] or 0))
open(INC+'c62_perf_rank.html','w',encoding='utf-8').write(tbl(['順','サイト','パフォーマンス','LCP','TBT'],[[str(i),e(a['dom']),str(a['sc']['performance']),e(a['me']['largest-contentful-paint'][0]),e(a['me']['total-blocking-time'][0])] for i,a in enumerate(srt,1)]))
# ---- B 3回
B=collections.OrderedDict()
for f in sorted(glob.glob(D+'B_*_2026-11-25.json')):
    name=f.split('/')[-1].replace('_2026-11-25.json',''); _,site,k=name.split('_')
    r,t=load(name)
    if r is None: B.setdefault(site,[]).append(None); continue
    sc,me=rec(r,t); B.setdefault(site,[]).append((r['requestedUrl'],sc,me))
brow=[];bcsv=[];bst={}
for site,L in B.items():
    for k,x in enumerate(L,1):
        if x is None: brow.append([site,str(k),'エラー']+['']*9); continue
        u,sc,me=x
        brow.append([e(u),str(k)]+[str(sc[c]) for c in CATS]+[e(me[m][0]) for m in MET]+[''])
        bcsv.append([u,k]+[sc[c] for c in CATS]+[me[m][0] for m in MET])
    okL=[x for x in L if x]
    bst[site]={c:(min(x[1][c] for x in okL),max(x[1][c] for x in okL)) for c in CATS}
    bst[site]['n']=len(okL); bst[site]['lcp']=[x[2]['largest-contentful-paint'][0] for x in okL]
wcsv('c62-repeat3-2026-11-25.csv',['URL','回']+[CN[c] for c in CATS]+[MN[m] for m in MET],bcsv)
open(INC+'c62_repeat.html','w',encoding='utf-8').write(tbl(['URL','回']+[CN[c] for c in CATS]+[MN[m] for m in MET]+[''],brow))
# ---- C pairs
P=[];perr=[]
for i in range(1,11):
    fs=glob.glob(D+f'C{i:02d}_top_*_2026-11-25.json'); fa=glob.glob(D+f'C{i:02d}_article_*_2026-11-25.json')
    nt=fs[0].split('/')[-1].replace('_2026-11-25.json',''); na=fa[0].split('/')[-1].replace('_2026-11-25.json','')
    dom=nt.split('_',2)[2]
    rt,tt=load(nt); ra,ta=load(na)
    if rt is None or ra is None: perr.append((dom,'top' if rt is None else '', 'article' if ra is None else '')); continue
    st_,mt=rec(rt,tt); sa,ma=rec(ra,ta)
    P.append(dict(dom=dom,top=rt['requestedUrl'],art=ra['requestedUrl'],st=st_,sa=sa,mt=mt,ma=ma))
phead=['サイト','トップ／記事','URL']+[CN[c] for c in CATS]+[MN[m] for m in MET]
prow=[];pcsv=[]
for p in P:
    for kind,u,sc,me in (('トップ',p['top'],p['st'],p['mt']),('記事',p['art'],p['sa'],p['ma'])):
        prow.append([e(p['dom']),kind,e(u)]+[str(sc[c]) for c in CATS]+[e(me[m][0]) for m in MET]); pcsv.append([p['dom'],kind,u]+[sc[c] for c in CATS]+[me[m][0] for m in MET])
wcsv('c62-top-vs-article-2026-11-25.csv',phead,pcsv)
open(INC+'c62_pairs.html','w',encoding='utf-8').write(tbl(phead,prow))
diff=[(p['dom'],p['sa']['performance']-p['st']['performance']) for p in P]
pst=dict(n=len(P),diff=diff,art_higher=sum(1 for d,x in diff if x>0),art_lower=sum(1 for d,x in diff if x<0),same=sum(1 for d,x in diff if x==0),
  med_top=statistics.median(p['st']['performance'] for p in P),med_art=statistics.median(p['sa']['performance'] for p in P),perr=perr)
# 全体
nok=len(A)+sum(len(v) for v in B.values())+len(P)*2
cost=0.28
allt=[t_sec(json.load(open(f))['tasks'][0]) for f in glob.glob(D+'*_2026-11-25.json') if json.load(open(f))['tasks'][0]['status_code']==20000]
st=dict(nA=len(A),AERR=AERR,dist=dist,bst=bst,pst=pst,cost=cost,calls=59,ok_calls=len(allt),avg_time=round(statistics.mean(allt),1),max_time=round(max(allt),1),min_time=round(min(allt),1),
  best=[(a['dom'],a['sc']['performance']) for a in srt[:5]],worst=[(a['dom'],a['sc']['performance']) for a in srt[-5:]],
  redirects=[(a['dom'],a['fin']) for a in A if a['fin'].rstrip('/').replace('https://www.','https://')!=a['req'].rstrip('/').replace('https://www.','https://')][:12],
  minseo=[(a['dom'],a['sc']['seo']) for a in sorted(A,key=lambda a:(a['sc']['seo'] if a['sc']['seo'] is not None else 999))[:3]],
  allbp100=sum(1 for a in A if a['sc']['best-practices']==100),
  perf_lt50=sum(1 for a in A if (a['sc']['performance'] or 0)<50),perf_ge90=sum(1 for a in A if (a['sc']['performance'] or 0)>=90))
json.dump(st,open(INC+'c62_stats.json','w',encoding='utf-8'),ensure_ascii=False,indent=1,default=list)
print(json.dumps(st,ensure_ascii=False,default=list)[:3800])
