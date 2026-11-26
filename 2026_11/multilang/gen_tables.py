import json,csv,glob
R='/home/user/tools/'
C=['キーワード調査','SEOツール','アフィリエイト','ブログの作り方','SEOを学ぶ','SEO代行']
ORDER=[('vi','ベトナム','ベトナム語'),('id','インドネシア','インドネシア語'),('pt','ブラジル','ポルトガル語'),('th','タイ','タイ語'),('tr','トルコ','トルコ語'),('fr','フランス','フランス語'),('es','メキシコ','スペイン語'),('pl','ポーランド','ポーランド語'),('ro','ルーマニア','ルーマニア語'),('uk','ウクライナ','ウクライナ語'),('bn','バングラデシュ','ベンガル語'),('ur','パキスタン','ウルドゥー語'),('tl','フィリピン','タガログ語＋英語キーワード'),('vi_en','ベトナム','英語キーワード'),('id_en','インドネシア','英語キーワード')]
rows=[]
for tag,c,l in ORDER:
    t=json.load(open(f'raw_{tag}_2026-11-26.json'))['tasks'][0]
    for i,x in enumerate(t['result']):
        rows.append(dict(tag=tag,country=c,lang=l,concept=C[i],kw=x['keyword'],vol=x['search_volume'],comp=x['competition'],ci=x['competition_index'],cpc=x['cpc'],lo=x['low_top_of_page_bid'],hi=x['high_top_of_page_bid'],m={(y['year'],y['month']):y['search_volume'] for y in (x['monthly_searches'] or [])}))
months=sorted({k for r in rows for k in r['m']})
with open(R+'site/articles/data/13countries-search-volume-2026-11-26.csv','w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f); w.writerow(['国','言語','調べた語の意味','キーワード','月間検索数（直近12か月の平均）','競合度（0〜100）','CPC（USD）','入札額の下限（USD）','入札額の上限（USD）']+[f'{y}-{m:02d}' for y,m in months])
    for r in rows: w.writerow([r['country'],r['lang'],r['concept'],r['kw'],'' if r['vol'] is None else r['vol'],'' if r['ci'] is None else r['ci'],'' if r['cpc'] is None else r['cpc'],'' if r['lo'] is None else r['lo'],'' if r['hi'] is None else r['hi']]+['' if r['m'].get(k) is None else r['m'][k] for k in months])
print(months[0],months[-1])
for r in rows:
    if r['tag'] in('vi','vi_en','id','id_en'): print(r['tag'],r['kw'],r['vol'],r['ci'],r['cpc'],[r['m'].get(k) for k in months][:3])
print('none',[(r['tag'],r['kw']) for r in rows if r['vol'] is None])
