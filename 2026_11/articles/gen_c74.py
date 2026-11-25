import json,csv,html,glob,collections,re
R='/home/user/tools/'; D=R+'2026_11/articles/data/c74/'; INC=R+'articles/_inc/'; OUT=R+'site/articles/data/'
e=html.escape
def wcsv(name,head,rows):
    with open(OUT+name,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f); w.writerow(head); w.writerows(rows)
def tbl(head,rows):
    return '<div class="scroll"><table class="data">\n<thead><tr>'+''.join(f'<th>{e(h)}</th>' for h in head)+'</tr></thead>\n<tbody>\n'+'\n'.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)+'\n</tbody></table></div>'
GEN={'ニュース':['nikkei.com','asahi.com','yomiuri.co.jp','toyokeizai.net'],'IT・Webメディア':['itmedia.co.jp','ascii.jp','lifehacker.jp','gizmodo.jp','ferret-plus.com'],'EC・ショッピング':['rakuten.co.jp','mercari.com','bookoff.co.jp','kakaku.com'],'暮らし・サービス情報':['cookpad.com','tabelog.com','jalan.net','mynavi.jp'],'個人の投稿サイト':['note.com','ameblo.jp'],'企業サイト':['toyota.jp','sony.jp'],'サーバー会社・行政':['xserver.ne.jp','conoha.jp','onamae.com','digital.go.jp']}
gen_of={s:g for g,L in GEN.items() for s in L}
OK={};STAT=collections.OrderedDict()
for f in sorted(glob.glob(D+'d*_2026-11-25.json')):
    fn=f.split('/')[-1]; site=fn.split('_')[1]
    j=json.load(open(f))['tasks'][0]; r=(j.get('result') or [None])[0]
    if j['status_code']!=20000: res=('エラー',j['status_message'][:60])
    elif not r or r.get('technologies') is None: res=('結果なし（技術が空）','')
    else: res=('取得できた','')
    # 同じサイトを2回呼んだ場合は成功を優先
    if site in STAT and STAT[site][0][0]=='取得できた': continue
    STAT[site]=(res,j['cost'])
    if res[0]=='取得できた': OK[site]=r
sites=list(OK)
tech={}  # site -> {name: set((g,ty))}
rows=[];csvr=[]
for s in sites:
    r=OK[s]; names=collections.defaultdict(set)
    for g,sub in r['technologies'].items():
        for ty,nl in sub.items():
            rows.append([e(s),e(gen_of.get(s,'')),e(g),e(ty),e(' ／ '.join(nl))]); csvr.append([s,gen_of.get(s,''),g,ty,' / '.join(nl)])
            for n in nl: names[n].add((g,ty))
    tech[s]=names
wcsv('c74-technologies-2026-11-25.csv',['ドメイン','ジャンル(筆者が付けた)','大分類','小分類','技術名'],csvr)
open(INC+'c74_table.html','w',encoding='utf-8').write(tbl(['ドメイン','ジャンル（筆者が付けた）','大分類','小分類','技術名'],rows))
# 技術ごとのサイト数
cnt=collections.Counter(); where=collections.defaultdict(list); cat={}
for s in sites:
    for n,c in tech[s].items():
        cnt[n]+=1; where[n].append(s); cat.setdefault(n,sorted(c)[0])
trow=[[e(n),e('/'.join(cat[n])),str(c),e(' ／ '.join(where[n]))] for n,c in sorted(cnt.items(),key=lambda t:(-t[1],t[0]))]
open(INC+'c74_count.html','w',encoding='utf-8').write(tbl(['技術名','分類','使っているサイト数（25サイト中）','使っているサイト'],trow))
wcsv('c74-technology-counts-2026-11-25.csv',['技術名','分類','サイト数','サイト'],[[n,'/'.join(cat[n]),c,' / '.join(where[n])] for n,c in sorted(cnt.items(),key=lambda t:(-t[1],t[0]))])
# サイトごとの数
nsite={s:len(tech[s]) for s in sites}
srow=[[e(s),e(gen_of.get(s,'')),str(nsite[s]),str(OK[s].get('domain_rank') or '')] for s in sorted(sites,key=lambda s:-nsite[s])]
open(INC+'c74_sites.html','w',encoding='utf-8').write(tbl(['ドメイン','ジャンル（筆者が付けた）','見つかった技術の数','domain_rank（APIが返した値）'],srow))
# 取得結果の表
strow=[[e(s),r[0][0],e(r[0][1]),f'{r[1]:.3f}'] for s,r in STAT.items()]
open(INC+'c74_status.html','w',encoding='utf-8').write(tbl(['調べたドメイン','結果','エラーの内容','費用(USD)'],strow))
wcsv('c74-status-2026-11-25.csv',['ドメイン','結果','エラーの内容','費用(USD)'],[[s,r[0][0],r[0][1],r[1]] for s,r in STAT.items()])
# 特定の技術
def has(n): return [s for s in sites if n in tech[s]]
def hasany(pred): return [s for s in sites if any(pred(n) for n in tech[s])]
wp=has('WordPress'); gtm=has('Google Tag Manager'); ga=has('Google Analytics'); fb=has('Facebook Pixel'); gpt=has('Google Publisher Tag'); dfl=has('DoubleClick Floodlight')
cms=[s for s in sites if any(('content','cms') ==x or ('content','blogs')==x for c in tech[s].values() for x in c)]
adv=[s for s in sites if any(x==('marketing','advertising') for c in tech[s].values() for x in c)]
tagm=[s for s in sites if any(x==('analytics','tag_managers') for c in tech[s].values() for x in c)]
anal=[s for s in sites if any(x==('analytics','analytics') for c in tech[s].values() for x in c)]
cdn=[s for s in sites if any(x==('servers','cdn') for c in tech[s].values() for x in c)]
# ジャンル別
grow=[]
for g,L in GEN.items():
    L2=[s for s in L if s in sites]
    if not L2: continue
    c=collections.Counter(n for s in L2 for n in tech[s])
    top=', '.join(f'{n}({k})' for n,k in c.most_common(5))
    grow.append([e(g),str(len(L2)),str(round(sum(nsite[s] for s in L2)/len(L2),1)),e(top)])
open(INC+'c74_genre.html','w',encoding='utf-8').write(tbl(['ジャンル（筆者が付けた）','サイト数','見つかった技術の平均数','よく使われていた技術（サイト数）'],grow))
stats=collections.Counter(r[0][0] for r in STAT.values())
st=dict(n_ok=len(sites),sites=sites,stat=dict(stats),n_all=len(STAT),cost=round(sum(r[1] for r in STAT.values()),4),
 err_kinds=collections.Counter(r[0][1] for r in STAT.values() if r[0][0]=='エラー'),
 empty=[s for s,r in STAT.items() if r[0][0].startswith('結果なし')],errors=[(s,r[0][1]) for s,r in STAT.items() if r[0][0]=='エラー'],
 wp=wp,gtm=gtm,ga=ga,fb=fb,gpt=gpt,dfl=dfl,cms=cms,adv=adv,tagm=tagm,anal=anal,cdn=cdn,
 top=cnt.most_common(15),nsite=nsite,total_techs=len(cnt),
 maxs=max(nsite.items(),key=lambda t:t[1]),mins=min(nsite.items(),key=lambda t:t[1]),genre=grow,
 wp_where={n:where[n] for n in ['WordPress']},
 cms_names={s:[n for n,c in tech[s].items() if any(x in (('content','cms'),('content','blogs')) for x in c)] for s in cms})
json.dump(st,open(INC+'c74_stats.json','w',encoding='utf-8'),ensure_ascii=False,indent=1,default=list)
print(json.dumps({k:st[k] for k in ['n_ok','stat','n_all','cost','err_kinds','empty','errors','wp','gtm','ga','fb','gpt','dfl','cms','cms_names','adv','tagm','anal','cdn','top','maxs','mins','total_techs']},ensure_ascii=False,default=list)[:3500])
