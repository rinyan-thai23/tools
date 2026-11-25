import json,csv,html,glob,collections,statistics,re
R='/home/user/tools/'; D=R+'2026_11/articles/data/c08/'; INC=R+'articles/_inc/'; OUT=R+'site/articles/data/'
e=html.escape
def wcsv(name,head,rows):
    with open(OUT+name,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f); w.writerow(head); w.writerows(rows)
def tbl(head,rows):
    return '<div class="scroll"><table class="data">\n<thead><tr>'+''.join(f'<th>{e(h)}</th>' for h in head)+'</tr></thead>\n<tbody>\n'+'\n'.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)+'\n</tbody></table></div>'
def load(prefix):
    out=[]
    for f in sorted(glob.glob(D+prefix+'*_2026-11-25.json')):
        j=json.load(open(f))['tasks'][0]; r=(j.get('result') or [{}])[0] or {}
        its=[i for i in (r.get('items') or []) if i['type']=='autocomplete']
        name=f.split('/')[-1][:3]
        out.append(dict(name=name,kw=(r.get('keyword') or ''),status=j['status_code'],msg=j['status_message'],cost=j['cost'],its=its))
    return out
# 検索語は result.keyword が空のとき（0件）があるので、リクエスト語を補う
req={}
for f in glob.glob('/tmp/c08_*.json'):
    n=f.split('c08_')[1].replace('.json',''); req[n]=json.load(open(f))[0]['keyword']
A=load('A');B=load('B');C=load('C')
for x in A+B+C: x['kw']=req.get(x['name'],x['kw'])
# ---- A
head=['キーワード','順','候補','relevance（APIの値）']
rowsA=[];csvA=[]
for x in A:
    for i in x['its']:
        rowsA.append([e(x['kw']),str(i['rank_group']),e(i['suggestion']),str(i.get('relevance'))]); csvA.append([x['kw'],i['rank_group'],i['suggestion'],i.get('relevance')])
wcsv('c08-20keywords-suggestions-2026-11-25.csv',head,csvA)
open(INC+'c08_a_table.html','w',encoding='utf-8').write(tbl(head,rowsA))
cntA=[(x['kw'],len(x['its'])) for x in A]
open(INC+'c08_a_counts.html','w',encoding='utf-8').write(tbl(['キーワード','候補の数'],[[e(k),str(n)] for k,n in cntA]))
# ---- B
rowsB=[];csvB=[]
for x in B:
    for i in x['its']:
        rowsB.append([e(x['kw']),str(i['rank_group']),e(i['suggestion']),str(i.get('relevance'))]); csvB.append([x['kw'],i['rank_group'],i['suggestion'],i.get('relevance')])
wcsv('c08-blog-kana-suggestions-2026-11-25.csv',head,csvB)
open(INC+'c08_b_table.html','w',encoding='utf-8').write(tbl(head,rowsB))
cntB=[(x['kw'],len(x['its'])) for x in B]
open(INC+'c08_b_counts.html','w',encoding='utf-8').write(tbl(['入力','候補の数'],[[e(k),str(n)] for k,n in cntB]))
uniqB=sorted({i['suggestion'] for x in B for i in x['its']})
open(INC+'c08_b_unique.html','w',encoding='utf-8').write('<ol class="cols">\n'+'\n'.join(f'<li>{e(s)}</li>' for s in uniqB)+'\n</ol>')
# ---- C fan-out と候補
fq=json.load(open(D+'fq_list.json'))['fq']
norm=lambda s:re.sub(r'\s+','',s).lower()
crow=[];ccsv=[];hit=0;tested=0;skipped=[]
cmap={x['kw']:x for x in C}
for q in fq:
    toks=q.split()
    if len(toks)<2: skipped.append(q); continue
    pre=' '.join(toks[:-1]); x=cmap.get(pre)
    if x is None: skipped.append(q); continue
    sug=[i['suggestion'] for i in x['its']]
    exact=any(norm(s)==norm(q) for s in sug)
    starts=[s for s in sug if norm(s).startswith(norm(q))]
    tested+=1; hit+= (exact or bool(starts))
    crow.append([e(q),e(pre),str(len(sug)),'あり' if exact else 'なし','あり' if starts else 'なし'])
    ccsv.append([q,pre,len(sug),'あり' if exact else 'なし','あり' if starts else 'なし',' / '.join(sug)])
wcsv('c08-fanout-vs-suggest-2026-11-25.csv',['ChatGPTの内部の検索ワード','入力した前半','候補の数','完全に同じ候補','その言葉で始まる候補','候補の一覧'],ccsv)
open(INC+'c08_c_table.html','w',encoding='utf-8').write(tbl(['ChatGPTの内部の検索ワード','Googleに入力した前半','候補の数','同じ言葉の候補','その言葉で始まる候補'],crow))
exact_n=sum(1 for r in ccsv if r[3]=='あり'); starts_n=sum(1 for r in ccsv if r[4]=='あり')
# ---- 全体
allc=[len(x['its']) for x in A+B+C]
zeros=[(x['kw'],x['msg']) for x in A+B+C if x['status']!=20000]
st=dict(nA=len(A),nB=len(B),nC=len(C),cntA=cntA,cntB=cntB,
 A_total=sum(n for k,n in cntA),B_total=sum(n for k,n in cntB),B_uniq=len(uniqB),
 maxc=max(allc),n15=sum(1 for c in allc if c==15),zeros=zeros,calls=len(A)+len(B)+len(C),cost=round(sum(x['cost'] or 0 for x in A+B+C),4),
 Amed=statistics.median(n for k,n in cntA),Bmed=statistics.median(n for k,n in cntB),
 A15=[k for k,n in cntA if n==15],Alow=[(k,n) for k,n in cntA if n<8],Blow=[(k,n) for k,n in cntB if n<10],B15=sum(1 for k,n in cntB if n==15),
 tested=tested,exact=exact_n,starts=starts_n,skipped=skipped,fq=len(fq),
 odd=[(x['kw'],[i['suggestion'] for i in x['its']][:3]) for x in A if x['kw'] in ('SEO とは','iPhone')],
 rel_max=max((i.get('relevance') or 0) for x in A+B+C for i in x['its']))
json.dump(st,open(INC+'c08_stats.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(json.dumps(st,ensure_ascii=False)[:3000])
