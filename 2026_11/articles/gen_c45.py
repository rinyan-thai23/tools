import json,csv,html,glob,collections,statistics,re
from urllib.parse import urlparse
R='/home/user/tools/'; D=R+'2026_11/articles/data/c45/'; INC=R+'articles/_inc/'; OUT=R+'site/articles/data/'
e=html.escape
def wcsv(name,head,rows):
    with open(OUT+name,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f); w.writerow(head); w.writerows(rows)
def tbl(head,rows):
    return '<div class="scroll"><table class="data">\n<thead><tr>'+''.join(f'<th>{e(h)}</th>' for h in head)+'</tr></thead>\n<tbody>\n'+'\n'.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)+'\n</tbody></table></div>'
SITES=[];ROWS=[];meta={}
for f in sorted(glob.glob(D+'site*_2026-11-25.json')):
    j=json.load(open(f))['tasks'][0]; r=(j.get('result') or [{}])[0]; s=r.get('target') or f.split('_')[1]
    name=f.split('/')[-1].split('_')[1]
    items=r.get('items') or []
    meta[name]=dict(cost=j['cost'],total=r.get('total_count'),n=len(items))
    SITES.append(name)
    for it in items:
        kd=it['keyword_data']; se=it['ranked_serp_element']['serp_item']
        ROWS.append(dict(site=name,kw=kd['keyword'],vol=kd['keyword_info']['search_volume'],rank=se['rank_group'],url=se.get('url') or '',cpc=kd['keyword_info'].get('cpc'),comp=kd['keyword_info'].get('competition_level')))
head=['サイト','キーワード','順位','Googleの月間検索数','URL']
wcsv('c45-10sites-top100-2026-11-25.csv',head+['CPC(USD)'],[[x['site'],x['kw'],x['rank'],'' if x['vol'] is None else x['vol'],x['url'],'' if x['cpc'] is None else round(x['cpc'],2)] for x in ROWS])
open(INC+'c45_table.html','w',encoding='utf-8').write(tbl(head,[[e(x['site']),e(x['kw']),str(x['rank']),'' if x['vol'] is None else f"{x['vol']:,}",e(x['url'])] for x in ROWS]))
# サイト別まとめ
srow=[];scsv=[]
by=collections.defaultdict(list)
for x in ROWS: by[x['site']].append(x)
for s in SITES:
    L=by[s]; m=meta[s]
    if not L: srow.append([e(s),'0','0','','','','','（0件）']); scsv.append([s,m['total'],0,'','','','']); continue
    vols=[x['vol'] for x in L if x['vol'] is not None]; rk=[x['rank'] for x in L]
    srow.append([e(s),f"{m['total']:,}",str(len(L)),f"{max(vols):,}",f"{int(statistics.median(vols)):,}",str(statistics.median(rk)),str(sum(1 for r in rk if r==1)),str(sum(1 for r in rk if r<=3))])
    scsv.append([s,m['total'],len(L),max(vols),int(statistics.median(vols)),statistics.median(rk),sum(1 for r in rk if r==1),sum(1 for r in rk if r<=3)])
wcsv('c45-site-summary-2026-11-25.csv',['サイト','10位以内のキーワード数(total_count)','取得した件数','最大の検索数','検索数の中央値','順位の中央値','1位の数','3位以内の数'],scsv)
open(INC+'c45_summary.html','w',encoding='utf-8').write(tbl(['サイト','10位以内のキーワード数（全部）','取得した件数','最大の検索数','検索数の中央値','順位の中央値','1位の数','3位以内の数'],srow))
# 重なり
kwsites=collections.defaultdict(set)
for x in ROWS: kwsites[x['kw']].add(x['site'])
ov=sorted([(k,sorted(v)) for k,v in kwsites.items() if len(v)>=2],key=lambda t:(-len(t[1]),t[0]))
vmap={}
for x in ROWS: vmap[x['kw']]=x['vol']
orow=[[e(k),str(len(v)),e(' ／ '.join(v)),'' if vmap[k] is None else f'{vmap[k]:,}'] for k,v in ov]
open(INC+'c45_overlap.html','w',encoding='utf-8').write(tbl(['キーワード','出たサイト数','出たサイト','月間検索数'],orow) if ov else '<p>（なし）</p>')
wcsv('c45-overlap-2026-11-25.csv',['キーワード','出たサイト数','出たサイト','月間検索数'],[[k,len(v),' / '.join(v),'' if vmap[k] is None else vmap[k]] for k,v in ov])
# 1位だけ
first=[x for x in ROWS if x['rank']==1]
first.sort(key=lambda x:(-(x['vol'] or 0)))
open(INC+'c45_rank1.html','w',encoding='utf-8').write(tbl(['サイト','キーワード','月間検索数','URL'],[[e(x['site']),e(x['kw']),'' if x['vol'] is None else f"{x['vol']:,}",e(x['url'])] for x in first]))
wcsv('c45-rank1-2026-11-25.csv',['サイト','キーワード','月間検索数','URL'],[[x['site'],x['kw'],'' if x['vol'] is None else x['vol'],x['url']] for x in first])
r1c=collections.Counter(x['site'] for x in first)
# 順位の分布
dist=collections.defaultdict(collections.Counter)
for x in ROWS: dist[x['site']][x['rank']]+=1
drow=[[e(s)]+[str(dist[s].get(r,0)) for r in range(1,11)] for s in SITES]
open(INC+'c45_rankdist.html','w',encoding='utf-8').write(tbl(['サイト']+[f'{r}位' for r in range(1,11)],drow))
wcsv('c45-rank-distribution-2026-11-25.csv',['サイト']+[f'{r}位' for r in range(1,11)],[[s]+[dist[s].get(r,0) for r in range(1,11)] for s in SITES])
allr=collections.Counter(x['rank'] for x in ROWS)
# 検索数順×順位
vol_sorted=sorted([x for x in ROWS if x['vol'] is not None],key=lambda x:-x['vol'])
# 検索数の帯ごとの順位の中央値
bands=[(100000,10**9,'10万以上'),(10000,99999,'1万〜9.9万'),(1000,9999,'1,000〜9,999'),(100,999,'100〜999'),(0,99,'0〜99')]
brow=[]
for lo,hi,name in bands:
    L=[x for x in ROWS if x['vol'] is not None and lo<=x['vol']<=hi]
    if not L: continue
    brow.append([name,str(len(L)),'' if not L else str(statistics.median(x['rank'] for x in L)),'' if not L else str(sum(1 for x in L if x['rank']==1)),'' if not L else f"{sum(1 for x in L if x['rank']==1)/len(L)*100:.0f}%"])
open(INC+'c45_bands.html','w',encoding='utf-8').write(tbl(['月間検索数の帯','キーワードの数','順位の中央値','1位の数','1位の割合'],brow))
st=dict(sites=SITES,meta=meta,total_rows=len(ROWS),nz=[s for s in SITES if not by[s]],ov_n=len(ov),ov_top=ov[:12],ov_max=max((len(v) for k,v in ov),default=0),
  r1_n=len(first),r1c=dict(r1c),allr=dict(sorted(allr.items())),first_top=[(x['site'],x['kw'],x['vol']) for x in first[:10]],
  bands=brow,cost=round(sum(m['cost'] for m in meta.values()),4),nvol_none=sum(1 for x in ROWS if x['vol'] is None),
  max_all=max((x for x in ROWS if x['vol'] is not None),key=lambda x:x['vol'])['kw'],max_vol=max(x['vol'] for x in ROWS if x['vol'] is not None),
  big=sorted(((s,meta[s]['total']) for s in SITES),key=lambda t:-(t[1] or 0)))
json.dump(st,open(INC+'c45_stats.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(json.dumps(st,ensure_ascii=False)[:3000])
