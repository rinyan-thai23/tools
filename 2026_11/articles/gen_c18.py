import json, csv, html, re, collections, glob, statistics
from urllib.parse import urlparse
R='/home/user/tools/'; D=R+'2026_11/articles/data/c18/'; INC=R+'articles/_inc/'; OUT=R+'site/articles/data/'
e=html.escape
P1="渋谷でおすすめのラーメン店を3つ教えてください"
Q=["新宿でおすすめのカフェを3つ教えてください","初心者向けのブログの始め方を教えてください","ワイヤレスイヤホンのおすすめを3つ教えてください","ノートパソコンの選び方を教えてください","京都で2日間の観光プランを教えてください","副業でおすすめのものを教えてください","確定申告のやり方を簡単に教えてください","転職エージェントの選び方を教えてください","SEOとは何ですか","英会話を独学で上達させる方法を教えてください","筋トレ初心者向けの週3日メニューを教えてください","カレーの簡単なレシピを教えてください","大阪で子連れで行けるランチのお店を3つ教えてください","美容院を選ぶときのポイントを教えてください","日本のおすすめの温泉地を3つ教えてください","インボイス制度とは何ですか","在宅勤務に向いている椅子の選び方を教えてください","NISAの始め方を教えてください","犬を飼う前に知っておくことを教えてください","キーワードプランナーの使い方を教えてください"]
W=["2026年に発売されたおすすめのワイヤレスイヤホンを教えてください","今日の東京の天気を教えてください","東京駅周辺でおすすめのカフェを3つ教えてください","最新のiPhoneの価格を教えてください","名古屋で人気のきしめん店を3つ教えてください","福岡でおすすめのホテルを3つ教えてください","札幌でおすすめの寿司店を3つ教えてください","横浜で評判のいい美容院を3つ教えてください","今年のNISA制度の変更点を教えてください","最新のChatGPTの料金プランを教えてください","日経平均株価の最新の値を教えてください","今週末に東京で開催されるイベントを教えてください","仙台でおすすめの焼肉店を3つ教えてください","神戸で人気のパン屋を3つ教えてください","最新のノートパソコンのおすすめを教えてください","渋谷でおすすめの居酒屋を3つ教えてください","池袋でおすすめの整体院を3つ教えてください","広島でおすすめのお好み焼き店を3つ教えてください","近くのおすすめのラーメン店を教えてください","キーワードプランナーの最新の仕様を教えてください"]
def load(n):
    j=json.load(open(D+f'{n}_2026-11-25.json'))['tasks'][0]; r=j['result'][0]
    txt='\n'.join(x['text'] for x in r['items'][0]['sections'] if x.get('text'))
    sr=r['search_results'] or []
    return dict(cost=j['cost'],model=r['model_name'],it=r['input_tokens'],ot=r['output_tokens'],fq=r['fan_out_queries'] or [],sr=sr,text=txt)
def clean(u): return re.sub(r'[?&]utm_source=openai$','',u or '')
def dom(u): return (urlparse(u).hostname or '').removeprefix('www.')
def wcsv(name,head,rows):
    with open(OUT+name,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f); w.writerow(head); w.writerows(rows)
def tbl(head,rows):
    return '<div class="scroll"><table class="data">\n<thead><tr>'+''.join(f'<th>{e(h)}</th>' for h in head)+'</tr></thead>\n<tbody>\n'+'\n'.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)+'\n</tbody></table></div>'
S={}
R1=[(f'r{i:02d}',P1) for i in range(1,11)]
R2=[(f'q{i:02d}',p) for i,p in enumerate(Q,1)]+[(f'w{i:02d}',p) for i,p in enumerate(W,1)]
for n,p in R1+R2: S[n]=load(n); S[n]['p']=p
# ---- 記事1
shops=collections.Counter(); runrows=[]; csvr=[]
for i,(n,p) in enumerate(R1,1):
    d=S[n]; names=re.findall(r'\*\*\[([^\]]+)\]',d['text']); shops.update(names); d['names']=names
    runrows.append([str(i),e(' ／ '.join(names)),e(' ／ '.join(d['fq'])),str(len(d['sr'])),f"{d['it']:,}",f"{d['ot']:,}",f"{d['cost']:.4f}"])
    csvr.append([i,' / '.join(names),' / '.join(d['fq']),len(d['sr']),d['it'],d['ot'],d['cost'],d['text']])
wcsv('c18-ramen-10runs-2026-11-25.csv',['回','店名(答えに出た順)','内部の検索ワード','参照ページ数','入力トークン','出力トークン','費用(USD)','回答の全文'],csvr)
open(INC+'c18_runs.html','w',encoding='utf-8').write(tbl(['回','答えに出た店','ChatGPTが内部で検索した言葉','参照ページ数','入力トークン','出力トークン','費用(USD)'],runrows))
open(INC+'c18_shops.html','w',encoding='utf-8').write(tbl(['答えに書かれた店名','10回のうち出た回数'],[[e(k),v] for k,v in shops.most_common()]))
ans=''.join(f'<details><summary>{i}回目の回答（全文）</summary><pre class="raw" style="white-space:pre-wrap">{e(S[n]["text"])}</pre></details>\n' for i,(n,p) in enumerate(R1,1))
open(INC+'c18_answers10.html','w',encoding='utf-8').write(ans)
sets=collections.Counter(tuple(S[n]['names']) for n,_ in R1); order=collections.Counter(tuple(sorted(S[n]['names'])) for n,_ in R1)
fq1=collections.Counter(q for n,_ in R1 for q in S[n]['fq'])
# ---- 記事2・3
rows=[]; allrefs=[]; dc=collections.Counter(); fqrows=[]; csv40=[]
searched=0
for n,p in R2:
    d=S[n]; ok=len(d['sr'])>0; searched+=ok
    doms=[dom(clean(x['url'])) for x in d['sr']]; dc.update(set(doms))
    rows.append([n.upper(),e(p),'あり' if ok else 'なし',e(' ／ '.join(d['fq'])),str(len(d['sr'])),str(len(set(doms))),f"{d['it']:,}",f"{d['ot']:,}",f"{d['cost']:.4f}"])
    for k,x in enumerate(d['sr'],1): allrefs.append([n.upper(),p,k,clean(x['url']),dom(clean(x['url'])),x.get('title') or '',x.get('date') or '',x.get('snippet') or ''])
    csv40.append([n.upper(),p,'あり' if ok else 'なし',' / '.join(d['fq']),len(d['sr']),d['it'],d['ot'],d['cost'],d['text']])
wcsv('c18-40prompts-2026-11-25.csv',['ID','質問','Web検索','内部の検索ワード','参照ページ数','入力トークン','出力トークン','費用(USD)','回答の全文'],csv40)
wcsv('c18-40prompts-references-2026-11-25.csv',['ID','質問','順','URL','ドメイン','タイトル','日付','抜粋'],allrefs)
open(INC+'c18_prompts.html','w',encoding='utf-8').write(tbl(['ID','質問','Web検索','内部の検索ワード','参照ページ数','ドメイン数','入力トークン','出力トークン','費用(USD)'],rows))
open(INC+'c18_refs.html','w',encoding='utf-8').write(tbl(['ID','質問','順','URL','ドメイン'],[[a,e(b),str(c),e(u),e(dm)] for a,b,c,u,dm,_,_,_ in allrefs]))
domrows=[[e(k),v] for k,v in dc.most_common()]
open(INC+'c18_domains.html','w',encoding='utf-8').write(tbl(['ドメイン','参照された質問の数（Web検索した質問のうち）'],domrows))
wcsv('c18-domains-2026-11-25.csv',['ドメイン','質問の数'],dc.most_common())
ans=''.join(f'<details><summary>{n.upper()}：{e(p)}</summary><pre class="raw" style="white-space:pre-wrap">{e(S[n]["text"])}</pre></details>\n' for n,p in R2)
open(INC+'c18_answers40.html','w',encoding='utf-8').write(ans)
# ---- 記事3: 内部検索ワード
allq=[(n.upper(),S[n]['p'],q) for n,p in R1+R2 for q in S[n]['fq']]
open(INC+'c18_fanout.html','w',encoding='utf-8').write(tbl(['ID','質問','ChatGPTが内部で検索した言葉'],[[a,e(b),e(c)] for a,b,c in allq]))
wcsv('c18-fanout-2026-11-25.csv',['ID','質問','内部の検索ワード'],allq)
y23=[x for x in allq if '2023' in x[2]]
calls=R1+R2
srch=[S[n] for n,_ in calls if S[n]['sr']]; nos=[S[n] for n,_ in calls if not S[n]['sr']]
def avg(xs,k): return round(sum(x[k] for x in xs)/len(xs),4) if xs else 0
stats=dict(r1_sets=len(order),r1_shops=shops.most_common(),r1_fq=fq1.most_common(),n40=len(R2),searched=searched,
  dom_n=len(dc),dom_top=dc.most_common(10),fq_total=len(allq),y23=[(a,b,c) for a,b,c in y23],
  cost_total=round(sum(S[n]['cost'] for n,_ in calls),4),cost_r1=round(sum(S[n]['cost'] for n,_ in R1),4),cost_40=round(sum(S[n]['cost'] for n,_ in R2),4),
  s_cost=avg(srch,'cost'),s_it=round(avg(srch,'it')),s_ot=round(avg(srch,'ot')),n_cost=avg(nos,'cost'),n_it=round(avg(nos,'it')),n_ot=round(avg(nos,'ot')),n_s=len(srch),n_n=len(nos),
  nosearch=[(n.upper(),S[n]['p']) for n,_ in R2 if not S[n]['sr']],models=sorted({S[n]['model'] for n,_ in calls}),
  sr_counts=sorted(collections.Counter(len(S[n]['sr']) for n,_ in calls if S[n]['sr']).items()),
  nsr_title=sum(1 for a in allrefs if a[5]),nrefs=len(allrefs),
  r1_ans_tokens=(min(S[n]['ot'] for n,_ in R1),max(S[n]['ot'] for n,_ in R1)))
json.dump(stats,open(INC+'c18_stats.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(json.dumps(stats,ensure_ascii=False,indent=1)[:2600])
