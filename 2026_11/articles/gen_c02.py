import json,csv,html,re,collections,statistics
from urllib.parse import urlparse
R='/home/user/tools/'; D=R+'2026_11/articles/data/'; INC=R+'articles/_inc/'; OUT=R+'site/articles/data/'
e=html.escape
def dom(u): return (urlparse(u).hostname or '').removeprefix('www.')
def wcsv(name,head,rows):
    with open(OUT+name,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f); w.writerow(head); w.writerows(rows)
def tbl(head,rows):
    return '<div class="scroll"><table class="data">\n<thead><tr>'+''.join(f'<th>{e(h)}</th>' for h in head)+'</tr></thead>\n<tbody>\n'+'\n'.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)+'\n</tbody></table></div>'
Q=[];A={}
for i in range(1,21):
    j=json.load(open(D+f'c02/kw{i:02d}_2026-11-25.json'))['tasks'][0]; r=j['result'][0]; it=r['items'][0]
    k=r['keyword']; refs=it.get('references') or []; md=it.get('markdown') or ''
    c1=json.load(open(D+f'C01_kw{i:02d}_2026-11-25.json'))['tasks'][0]['result'][0]
    org=[x for x in c1['items'] if x['type']=='organic']
    A[k]=dict(i=i,md=md,refs=refs,cost=j['cost'],org=org,n_items=len(r['items']),hl='[ハイライトの開始]' in md,inl=len(re.findall(r'\[\[\d+\]\]\(',md)))
    Q.append(k)
# --- 質問ごとの表
rows=[];csvr=[];refrows=[];dc=collections.Counter();dq=collections.defaultdict(set)
for k in Q:
    a=A[k]; ds=[dom(x['url']) for x in a['refs']]
    org_d=[dom(x['url']) for x in a['org']]
    ov=sorted(set(ds)&set(org_d)); ovu=sorted(set(x['url'] for x in a['refs'])&set(x['url'] for x in a['org']))
    a['ov']=ov;a['ovu']=ovu;a['ds']=ds
    rows.append([f"Q{a['i']:02d}",e(k),str(len(a['refs'])),str(len(set(ds))),str(len(a['org'])),str(len(ov)),str(len(ovu)),f"{len(a['md']):,}",f"{a['cost']:.4f}"])
    csvr.append([f"Q{a['i']:02d}",k,len(a['refs']),len(set(ds)),len(a['org']),len(ov),' / '.join(ov),len(ovu),len(a['md']),a['cost'],a['md']])
    for n,x in enumerate(a['refs'],1):
        refrows.append([f"Q{a['i']:02d}",k,n,x.get('source') or '',dom(x['url']),x.get('title') or '',x['url']])
        dc[dom(x['url'])]+=1; dq[dom(x['url'])].add(k)
wcsv('c02-20questions-2026-11-25.csv',['ID','キーワード','引用数','引用ドメイン数','通常の検索結果(10件)','ドメインの重なり数','重なったドメイン','URLの重なり数','回答の文字数','費用(USD)','回答の全文(markdown)'],csvr)
wcsv('c02-references-2026-11-25.csv',['ID','キーワード','順','引用元の名前','ドメイン','タイトル','URL'],refrows)
open(INC+'c02_summary.html','w',encoding='utf-8').write(tbl(['ID','キーワード','AIモードの引用数','引用ドメイン数','通常の検索結果(上位10)','ドメインの重なり','URLの重なり','回答の文字数','費用(USD)'],rows))
open(INC+'c02_refs.html','w',encoding='utf-8').write(tbl(['ID','キーワード','順','引用元の名前','ドメイン','タイトル','URL'],[[a,e(b),str(c),e(d),e(f),e(g),e(h)] for a,b,c,d,f,g,h in refrows]))
dom_rows=[[e(d),str(n),str(len(dq[d]))] for d,n in dc.most_common()]
open(INC+'c02_domains.html','w',encoding='utf-8').write(tbl(['ドメイン','引用された回数','引用された質問の数'],dom_rows))
wcsv('c02-domains-2026-11-25.csv',['ドメイン','引用された回数','引用された質問の数'],[[d,n,len(dq[d])] for d,n in dc.most_common()])
ans=''.join(f'<details><summary>Q{A[k]["i"]:02d}：{e(k)}（引用{len(A[k]["refs"])}件）</summary><pre class="raw" style="white-space:pre-wrap">{e(A[k]["md"])}</pre></details>\n' for k in Q)
open(INC+'c02_answers.html','w',encoding='utf-8').write(ans)
# 通常の検索上位10 と AIモード引用 のドメイン対応
ovrows=[]
for k in Q:
    a=A[k]
    ovrows.append([f"Q{a['i']:02d}",e(k),e(' ／ '.join(a['ov'])) or '（なし）',e(' ／ '.join(sorted(set(a['ds'])-set(a['ov'])))) or '（なし）'])
open(INC+'c02_overlap.html','w',encoding='utf-8').write(tbl(['ID','キーワード','両方に出たドメイン','AIモードだけが引用したドメイン'],ovrows))
nrefs=[len(A[k]['refs']) for k in Q]; mdl=[len(A[k]['md']) for k in Q]
zero=[k for k in Q if not A[k]['refs']]
withr=[k for k in Q if A[k]['refs']]
totov=sum(len(A[k]['ov']) for k in Q); totds=sum(len(set(A[k]['ds'])) for k in Q)
st=dict(total_refs=sum(nrefs),uniq_dom=len(dc),zero=zero,n_withref=len(withr),refs_dist=sorted(collections.Counter(nrefs).items()),
  med_refs=statistics.median(nrefs),max_refs=max(nrefs),md_min=min(mdl),md_med=int(statistics.median(mdl)),md_max=max(mdl),
  top=dc.most_common(12),top_q=[(d,len(dq[d])) for d,_ in dc.most_common(12)],
  tot_ov=totov,tot_ds_withref=totds,ov_by_q={k:len(A[k]['ov']) for k in Q},ovu_total=sum(len(A[k]['ovu']) for k in Q),
  org_tot=sum(len(A[k]['org']) for k in Q),cost=round(sum(A[k]['cost'] for k in Q),4),hl=sum(A[k]['hl'] for k in Q),inl=sum(1 for k in Q if A[k]['inl']),
  n_items=collections.Counter(A[k]['n_items'] for k in Q).most_common(),
  ov_zero=[k for k in withr if not A[k]['ov']],ov_any=[k for k in withr if A[k]['ov']])
json.dump(st,open(INC+'c02_stats.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(json.dumps(st,ensure_ascii=False)[:2500])
