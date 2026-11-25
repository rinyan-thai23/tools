import json,csv,html,statistics,collections
R='/home/user/tools/'; D=R+'2026_11/articles/data/'; INC=R+'articles/_inc/'; OUT=R+'site/articles/data/'
e=html.escape
items=json.load(open(D+'C41_30_2026-11-25.json'))['tasks'][0]['result'][0]['items']
allm=[(y,m) for y in range(2021,2027) for m in range(1,13) if (2021,7)<=(y,m)<=(2026,10)]
KW=[x['keyword'] for x in items]
S={};REV={}
for x in items:
    s0={};u={}
    for ent in x['history']:
        for k,m in enumerate(ent['keyword_info']['monthly_searches']):
            key=(m['year'],m['month'])
            if k==0 and key==(ent['year'],ent['month']): s0[key]=m['search_volume']
            u.setdefault(key,set()).add(m['search_volume'])
    S[x['keyword']]=s0; REV[x['keyword']]=sum(1 for k in s0 if len(u[k])>1)
def wcsv(name,head,rows):
    with open(OUT+name,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f); w.writerow(head); w.writerows(rows)
def tbl(head,rows):
    return '<div class="scroll"><table class="data">\n<thead><tr>'+''.join(f'<th>{e(h)}</th>' for h in head)+'</tr></thead>\n<tbody>\n'+'\n'.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)+'\n</tbody></table></div>'
# --- 全データ (月が行、キーワードが列)
rows=[];csvr=[]
for k in allm:
    vals=[S[w].get(k) for w in KW]
    csvr.append([f'{k[0]}-{k[1]:02d}']+['' if v is None else v for v in vals])
    rows.append([f'{k[0]}-{k[1]:02d}']+['' if v is None else f'{v:,}' for v in vals])
wcsv('c41-30keywords-monthly-2026-11-25.csv',['年月']+KW,csvr)
open(INC+'c41_monthly.html','w',encoding='utf-8').write(tbl(['年月']+[e(k) for k in KW],rows))
# --- 月ごとの平均（2022〜2025）
YRS=[2022,2023,2024,2025]
avg={};cnt={}
for w in KW:
    avg[w]={};cnt[w]={}
    for m in range(1,13):
        v=[S[w][(y,m)] for y in YRS if (y,m) in S[w]]
        cnt[w][m]=len(v); avg[w][m]=round(sum(v)/len(v)) if v else None
def peak(w):
    c=[(avg[w][m],m) for m in range(1,13) if avg[w][m] is not None]
    return max(c)[1],max(c)[0],min(c)[1],min(c)[0]
pk={w:peak(w) for w in KW}
ratio={}
for w in KW:
    mx,mn=pk[w][1],pk[w][3]
    ratio[w]=round(mx/mn,1) if mn>0 else None
nmonths={w:sum(1 for k in allm if k in S[w]) for w in KW}
prow=[];pcsv=[]
for w in KW:
    p=pk[w]
    prow.append([e(w),f'{p[0]}月',f'{p[1]:,}',f'{p[2]}月',f'{p[3]:,}','' if ratio[w] is None else str(ratio[w]),str(sum(cnt[w].values())),str(nmonths[w])])
    pcsv.append([w,p[0],p[1],p[2],p[3],'' if ratio[w] is None else ratio[w],sum(cnt[w].values()),nmonths[w]])
wcsv('c41-peak-months-2026-11-25.csv',['キーワード','ピーク月','ピーク月の平均','いちばん低い月','その月の平均','ピーク÷最低','2022-2025の月数','全期間の記録月数(最大64)'],pcsv)
open(INC+'c41_peaks.html','w',encoding='utf-8').write(tbl(['キーワード','ピーク月','ピーク月の平均','いちばん低い月','その月の平均','ピーク÷最低','使った月数(2022〜2025、最大48)','全期間の記録月数(最大64)'],prow))
# 月別平均の表
arow=[[e(w)]+[('' if avg[w][m] is None else f'{avg[w][m]:,}') for m in range(1,13)] for w in KW]
open(INC+'c41_avg.html','w',encoding='utf-8').write(tbl(['キーワード']+[f'{m}月' for m in range(1,13)],arow))
wcsv('c41-calendar-month-averages-2026-11-25.csv',['キーワード']+[f'{m}月' for m in range(1,13)],[[w]+['' if avg[w][m] is None else avg[w][m] for m in range(1,13)] for w in KW])
# --- 動く語・一定の語 (ratio並べ替え)
STABLE=["カレー レシピ","ブログ 始め方","英会話 独学","筋トレ 初心者","副業 おすすめ","転職 エージェント 比較","ノートパソコン 選び方","ワイヤレスイヤホン おすすめ","新宿 美容院","確定申告 やり方"]
SEAS=[w for w in KW if w not in STABLE]
def rk(w): return ratio[w] if ratio[w] is not None else 1e9
srt=sorted(KW,key=rk)
rrows=[[e(w),'一定を期待した10語' if w in STABLE else '季節の20語','（最低月が0）' if ratio[w] is None else str(ratio[w]),f'{pk[w][0]}月',f'{pk[w][1]:,}',f'{pk[w][3]:,}'] for w in srt]
open(INC+'c41_ratio.html','w',encoding='utf-8').write(tbl(['キーワード','グループ','ピーク÷最低','ピーク月','ピーク月の平均','最低月の平均'],rrows))
# --- 1月と4月
j4=[]
for w in KW:
    j=[S[w][(y,1)] for y in range(2022,2027) if (y,1) in S[w]]; a=[S[w][(y,4)] for y in range(2022,2027) if (y,4) in S[w]]
    ja=round(sum(j)/len(j)) if j else None; aa=round(sum(a)/len(a)) if a else None
    j4.append((w,ja,len(j),aa,len(a)))
j4rows=[[e(w),'' if ja is None else f'{ja:,}',str(nj),'' if aa is None else f'{aa:,}',str(na),'' if (ja in(None,0) or aa is None) else f'{(aa-ja)/ja*100:+.0f}%'] for w,ja,nj,aa,na in j4]
open(INC+'c41_jan_apr.html','w',encoding='utf-8').write(tbl(['キーワード','1月の平均','1月の年数','4月の平均','4月の年数','1月→4月の変化'],j4rows))
wcsv('c41-jan-vs-apr-2026-11-25.csv',['キーワード','1月の平均','1月の年数','4月の平均','4月の年数','1月→4月の変化(%)'],[[w,'' if ja is None else ja,nj,'' if aa is None else aa,na,'' if (ja in(None,0) or aa is None) else round((aa-ja)/ja*100)] for w,ja,nj,aa,na in j4])
# --- 限界
zeros={w:sum(1 for k in allm if S[w].get(k)==0) for w in KW}
gaps={w:64-nmonths[w] for w in KW}
rs=sorted(ratio[w] for w in SEAS if ratio[w] is not None); rst=sorted(ratio[w] for w in STABLE if ratio[w] is not None)
st=dict(n=len(KW),months=len(allm),cost=0.0156,rev=REV,rev_total=sum(REV.values()),rev_max=max(REV.items(),key=lambda x:x[1]),
 gaps=gaps,gaps10=[w for w in KW if gaps[w]>=10],gaps_total=sum(gaps.values()),gaps_max=max(gaps.items(),key=lambda x:x[1]),
 zeros={w:z for w,z in zeros.items() if z},peak={w:pk[w][0] for w in KW},peakv={w:pk[w][1] for w in KW},ratio=ratio,
 seas_ratio=(rs[0],rs[-1],statistics.median(rs),len(rs)),stable_ratio=(rst[0],rst[-1],statistics.median(rst),len(rst)),
 stable_zero=[w for w in STABLE if ratio[w] is None],seas_zero=[w for w in SEAS if ratio[w] is None],
 top5=[(w,ratio[w]) for w in srt[::-1] if ratio[w] is not None][:5],low5=[(w,ratio[w]) for w in srt if ratio[w] is not None][:5],
 j4=[(w,ja,aa) for w,ja,nj,aa,na in j4],STABLE=STABLE,SEAS=SEAS,nmonths=nmonths)
json.dump(st,open(INC+'c41_stats.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(json.dumps({k:st[k] for k in ['rev_total','rev_max','gaps10','gaps_total','gaps_max','zeros','seas_ratio','stable_ratio','stable_zero','seas_zero','top5','low5']},ensure_ascii=False)[:2500])
print({w:pk[w][0] for w in SEAS})
