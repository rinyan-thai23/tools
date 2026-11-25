import json,csv,html,re,collections
from urllib.parse import urlparse
R='/home/user/tools/'; D=R+'2026_11/articles/data/c18/'; INC=R+'articles/_inc/'; OUT=R+'site/articles/data/'
e=html.escape
PR={'a':"渋谷でおすすめのラーメン店を3つ教えてください",'b':"最新のiPhoneの価格を教えてください",'c':"SEOとは何ですか",'d':"ノートパソコンの選び方を教えてください",'e':"キーワードプランナーの使い方を教えてください"}
GP={'a':'r01','b':'w04','c':'q09','d':'q04','e':'q20'}
AI=[('chatgpt','ChatGPT'),('claude','Claude'),('gemini','Gemini'),('perplexity','Perplexity')]
def clean(u): return re.sub(r'[?&]utm_source=openai$','',u or '')
def dom(u): return (urlparse(u).hostname or '').removeprefix('www.')
def ld(k,a):
    f=f'{GP[k]}_2026-11-25.json' if a=='chatgpt' else f'ai4_{a}_{k}_2026-11-25.json'
    j=json.load(open(D+f))['tasks'][0]; r=j['result'][0]
    txt='\n'.join(x['text'] for x in r['items'][0]['sections'] if x.get('text'))
    if a=='gemini':
        urls=[]; 
        for x in r['items'][0]['sections']:
            for an in (x.get('annotations') or []):
                u=an.get('direct_url') or an.get('url')
                if u and u not in urls: urls.append(u)
    else:
        urls=[clean(x['url']) for x in (r.get('search_results') or [])]
    return dict(cost=j['cost'],model=r['model_name'],ws=r['web_search'],ot=r['output_tokens'],it=r['input_tokens'],fq=r.get('fan_out_queries') or [],urls=urls,text=txt)
D4={(k,a):ld(k,a) for k in PR for a,_ in AI}
def used(d): return bool(d['fq'] or d['urls'])
def wcsv(name,head,rows):
    with open(OUT+name,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f); w.writerow(head); w.writerows(rows)
def tbl(head,rows):
    return '<div class="scroll"><table class="data">\n<thead><tr>'+''.join(f'<th>{e(h)}</th>' for h in head)+'</tr></thead>\n<tbody>\n'+'\n'.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)+'\n</tbody></table></div>'
rows=[];csvr=[]
for k in PR:
    for a,name in AI:
        d=D4[(k,a)]
        rows.append([e(PR[k]),name,e(d['model']),'あり' if used(d) else 'なし',e(' ／ '.join(d['fq'])),str(len(d['urls'])),str(len(set(dom(u) for u in d['urls']))),f"{d['ot']:,}",f"{d['cost']:.4f}"])
        csvr.append([PR[k],name,d['model'],'あり' if used(d) else 'なし',' / '.join(d['fq']),len(d['urls']),d['it'],d['ot'],d['cost'],d['text']])
wcsv('ai4-20answers-2026-11-25.csv',['質問','AI','モデル','Webの参照','内部の検索ワード','参照URL数','入力トークン','出力トークン','費用(USD)','回答の全文'],csvr)
open(INC+'ai4_summary.html','w',encoding='utf-8').write(tbl(['質問','AI','モデル','Webの参照','内部の検索ワード','参照URL数','ドメイン数','出力トークン','費用(USD)'],rows))
ans=''
for k in PR:
    ans+=f'<h3>{e(PR[k])}</h3>\n'
    for a,name in AI:
        ans+=f'<details><summary>{name}</summary><pre class="raw" style="white-space:pre-wrap">{e(D4[(k,a)]["text"])}</pre></details>\n'
open(INC+'ai4_answers.html','w',encoding='utf-8').write(ans)
refs=[];
for k in PR:
    for a,name in AI:
        for i,u in enumerate(D4[(k,a)]['urls'],1): refs.append([PR[k],name,i,u,dom(u)])
wcsv('ai4-references-2026-11-25.csv',['質問','AI','順','URL','ドメイン'],refs)
open(INC+'ai4_refs.html','w',encoding='utf-8').write(tbl(['質問','AI','順','URL','ドメイン'],[[e(a),b,str(c),e(u),e(dm)] for a,b,c,u,dm in refs]))
# 店名（ラーメン）
def shops(a):
    t=D4[('a',a)]['text']
    if a=='chatgpt': return re.findall(r'\*\*\[([^\]]+)\]',t)
    if a=='claude': return re.findall(r'##\s*\d\.\s*\*\*(.+?)\*\*',t)
    if a=='gemini': return [s.strip().strip('*') for s in re.findall(r'###\s*\d\.\s*(.+)',t)]
    return re.findall(r'\*\*(.+?)\*\*：',t)
sh={a:shops(a) for a,_ in AI}
usedcnt={a:sum(used(D4[(k,a)]) for k in PR) for a,_ in AI}
cost={a:round(sum(D4[(k,a)]['cost'] for k in PR),4) for a,_ in AI}
cost_new=round(sum(D4[(k,a)]['cost'] for k in PR for a,_ in AI if a!='chatgpt'),4)
json.dump(dict(shops=sh,usedcnt=usedcnt,cost=cost,cost_new=cost_new,nrefs=len(refs),
  refs_by={a:sum(len(D4[(k,a)]['urls']) for k in PR) for a,_ in AI},
  ip={a:D4[('b',a)]['text'] for a,_ in AI}),open(INC+'ai4_stats.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(sh,usedcnt,cost,cost_new,len(refs))
