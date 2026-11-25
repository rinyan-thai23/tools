import json, collections, html
R='/home/user/tools/'
S=json.load(open(R+'articles/_inc/c01_stats.json')); st=S['st']; ntc=S['ntc']; nt=S['nontrunc']
T=json.load(open(R+'articles/_inc/c01_types.json'))
n=len(T); org=[c.get('organic',0) for k,x,c in T]; tot=sum(x for k,x,c in T)
dist=collections.Counter(org)
tc=collections.Counter()
for k,x,c in T:
    for t in c: tc[t]+=1
JA={'organic':'通常の検索結果（青いリンク）','ai_overview':'AI概要','people_also_ask':'他の人はこちらも質問','related_searches':'関連検索','local_pack':'地図つきのお店リスト','video':'動画','popular_products':'人気の商品','knowledge_graph':'ナレッジパネル（企業や人物の情報）','images':'画像','stocks_box':'株価','recipes':'レシピ','google_reviews':'Googleのレビュー'}
typerows=''.join(f'<tr><td>{JA.get(t,t)}</td><td><code>{t}</code></td><td>{c}</td></tr>' for t,c in sorted(tc.items(),key=lambda x:(-x[1],x[0])))
distrows=''.join(f'<tr><td>{k}本</td><td>{v}語</td></tr>' for k,v in sorted(dist.items(),reverse=True))
dom=S['dom']; top=dom[:8]
domrows=''.join(f'<tr><td>{html.escape(d)}</td><td>{c}</td></tr>' for d,c in top)
ndom=len(dom)
bins=''.join(f'<tr><td>{b}〜{b+9}文字</td><td>{c}</td></tr>' for b,c in S['nbins'])
# ---- 記事1
a1=f'''<p>ブログを書く前に、「いま上位にいるのは、どんなページ？」が気になります。<a href="/C01/ja/">検索の上位を見るツール</a>で、「ブログ 始め方」を検索して、<strong>上位100件を全部</strong>出してみました。順位、タイトル、URL、ドメイン、説明文まで、APIが返したまま載せます。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>100件に出てきたドメイン（サイトの名前）は<strong>{ndom}種類</strong>でした。同じサイトが何回も出ています。</li>
<li>一番多かったのは <strong>{html.escape(top[0][0])}（{top[0][1]}回）</strong>、次が <strong>{html.escape(top[1][0])}（{top[1][1]}回）</strong>でした。</li>
<li>100件のうち、タイトルが「…」で途中までしか出なかったものが<strong>{st["省略(…)で終わる"]}件</strong>ありました。</li>
</ul>
<p>お店の棚にたとえると、100個の商品の中に、同じメーカーの商品がいくつも混ざっている感じです。</p>

<h2>よく出たドメイン（上位{len(top)}）</h2>
<div class="scroll"><table class="data"><thead><tr><th>ドメイン</th><th>100件の中での回数</th></tr></thead><tbody>{domrows}</tbody></table></div>
<p>全ドメインの一覧は、CSVにあります（<a href="/articles/data/c01-blog-100-domains-2026-11-25.csv" download>ドメインごとの回数CSV</a>）。</p>

<h2>全データ（上位100件）</h2>
<p>APIが返した値を、そのまま全部載せています。「順位」は通常の検索結果の中での順位、「全体の位置」は、AI概要や「他の人はこちらも質問」のような他の枠も数えた位置です。</p>
<p><a href="/articles/data/c01-blog-100-2026-11-25.csv" download>CSVでダウンロード（100行）</a></p>
<!--include:c01_table100-->

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
<li>日付：2026年11月25日</li>
<li>地域と言語：日本、日本語</li>
<li>キーワード：「ブログ 始め方」（1語）</li>
<li>件数：上位100件</li>
<li>ツール：<a href="/C01/ja/">検索の上位を見る（C01）</a>。DataForSEOのAPIが、Googleの検索結果を返します</li>
<li>費用：<strong>$0.0175</strong>（約2.7円、1ドル155円で計算）</li>
</ul>
</div>
<p class="note">検索結果は、検索する場所や時間で変わることがあります。これは「APIで取った、この日の日本の結果」です。あなたのブラウザの結果と、少し違うことがあります。</p>
<p>タイトルの文字数や【】の数は、<a href="/articles/c01-top100-title-stats/">次の記事</a>で数えました。</p>
'''
# ---- 記事2
a2=f'''<p>検索すると、1ページ目はずっと「青いリンク」が10本並んでいる、と思っていませんか。いまの検索結果には、AI概要や「他の人はこちらも質問」など、いろいろな枠が混ざります。<a href="/C01/ja/">検索の上位を見るツール</a>で、<strong>20個のキーワード</strong>の1ページ目を取って、中身の種類を数えました。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>20語すべてで調べた、1ページ目の項目は合計<strong>{tot}個</strong>。そのうち「青いリンク」は<strong>{sum(org)}個</strong>でした。</li>
<li><strong>AI概要</strong>が出たのは、20語のうち<strong>{tc["ai_overview"]}語</strong>です。</li>
<li>「他の人はこちらも質問」が出たのは<strong>{tc["people_also_ask"]}語</strong>、地図つきのお店リストが出たのは<strong>{tc["local_pack"]}語</strong>でした。</li>
<li>青いリンクが10本そろっていたのは<strong>{dist[10]}語</strong>です。10本に満たない語もありました。</li>
</ul>
<p>お店の棚にたとえると、商品（青いリンク）のほかに、宣伝のポップや案内板が何枚も立っている感じです。</p>

<h2>青いリンクの本数</h2>
<div class="scroll"><table class="data"><thead><tr><th>青いリンクの本数</th><th>キーワードの数</th></tr></thead><tbody>{distrows}</tbody></table></div>

<h2>出た枠の種類（20語のうち、何語で出たか）</h2>
<div class="scroll"><table class="data"><thead><tr><th>枠</th><th>APIの名前</th><th>出たキーワードの数</th></tr></thead><tbody>{typerows}</tbody></table></div>

<h2>キーワードごとの数（全部）</h2>
<p>1ページ目に出た項目を、種類ごとに数えた表です。0は、その枠が出なかったという意味です。</p>
<p><a href="/articles/data/c01-20keywords-types-2026-11-25.csv" download>この表のCSV</a></p>
<!--include:c01_types-->

<h2>1ページ目の全項目（全部）</h2>
<p>20語の1ページ目に出た、すべての項目です。通常の検索結果以外の枠には、タイトルやURLがないものがあります。</p>
<p><a href="/articles/data/c01-20keywords-items-2026-11-25.csv" download>CSVでダウンロード（{tot}行）</a></p>
<details><summary>全{tot}項目の表を開く</summary>
<!--include:c01_items-->
</details>

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
<li>日付：2026年11月25日、地域と言語：日本、日本語</li>
<li>件数：1語につき上位10件（1ページ目）</li>
<li>キーワード20語：質問の形、商品、ブランド、地域、ニュース、レシピなどを混ぜて、私が選びました</li>
<li>ツール：<a href="/C01/ja/">検索の上位を見る（C01）</a>と同じAPI。ここでは、ツールの表には出ない「通常の検索結果以外の枠」も数えています</li>
<li>費用：1語ごとに$0.004、20語で約$0.08</li>
</ul>
</div>
<p class="note">枠の名前は、APIが返した名前をそのまま使っています。数えただけで、よしあしの評価はしていません。検索結果は、場所や時間で変わることがあります。</p>
<p>1週間後にもう一度同じ20語を調べて、入れ替わりを見る予定です。</p>
'''
# ---- 記事3
ntlen=nt
a3=f'''<p>上位にいる記事のタイトルは、どんな形をしているのでしょうか。<a href="/articles/c01-blog-top100/">「ブログ 始め方」の上位100件</a>のタイトルを、数えてみました。</p>

<h2>先に、気をつけること</h2>
<p>タイトルの長さは、<strong>途中で「...」と切れているものを除いて</strong>数えました。100件のうち<strong>{st["省略(…)で終わる"]}件</strong>は、Googleの検索結果で途中までしか出ていません。その分、文字数が短く出てしまうからです。</p>
<ul>
<li>切れていないタイトル：<strong>{nt[0]}件</strong></li>
<li>切れているタイトル：<strong>{st["省略(…)で終わる"]}件</strong></li>
</ul>

<h2>文字数（切れていない{nt[0]}件）</h2>
<ul>
<li>いちばん短い：<strong>{nt[1]}文字</strong></li>
<li>いちばん長い：<strong>{nt[2]}文字</strong></li>
<li>真ん中の値（中央値）：<strong>{nt[3]}文字</strong></li>
<li>平均：<strong>{S["avg_nt"]}文字</strong></li>
</ul>
<div class="scroll"><table class="data"><thead><tr><th>文字数</th><th>件数</th></tr></thead><tbody>{bins}</tbody></table></div>

<h2>言葉の入り方（100件全体と、切れていない{nt[0]}件）</h2>
<p>切れているタイトルは、続きに言葉が隠れているかもしれません。そのため、「100件全体」は少なめに出る可能性があります。</p>
<div class="scroll"><table class="data"><thead><tr><th>タイトルに含まれる言葉</th><th>100件全体</th><th>切れていない{nt[0]}件</th></tr></thead><tbody>
<tr><td>「ブログ」</td><td>{st["「ブログ」を含む"]}</td><td>{ntc["ブログ"]}</td></tr>
<tr><td>「始め方」</td><td>{st["「始め方」を含む"]}</td><td>{ntc["始め方"]}</td></tr>
<tr><td>「初心者」</td><td>{st["「初心者」を含む"]}</td><td>{ntc["初心者"]}</td></tr>
<tr><td>【 】（隅付き括弧）</td><td>{st["【】を含む"]}</td><td>{ntc["【】"]}</td></tr>
<tr><td>「完全」</td><td>{st["「完全」を含む"]}</td><td>{ntc["完全"]}</td></tr>
<tr><td>年号（20xx）</td><td>{st["年号(20xx)を含む"]}</td><td>{ntc["年号"]}</td></tr>
<tr><td>「無料」</td><td>{st["「無料」を含む"]}</td><td>{ntc["無料"]}</td></tr>
<tr><td>「おすすめ」</td><td>{st["「おすすめ」を含む"]}</td><td>{ntc["おすすめ"]}</td></tr>
</tbody></table></div>

<h2>全データ（100件のタイトルと、文字数）</h2>
<p>タイトルは、APIが返した文字をそのまま載せています。「省略」の列に○があるものは、途中で切れているタイトルです。文字数は、切れた状態での数です。</p>
<!--include:c01_titles-->

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
<li>日付：2026年11月25日、地域と言語：日本、日本語</li>
<li>データ：<a href="/articles/c01-blog-top100/">「ブログ 始め方」の上位100件</a></li>
<li>ツール：<a href="/C01/ja/">検索の上位を見る（C01）</a></li>
<li>数え方：タイトルの文字を数えて、特定の言葉が含まれるかを調べました。意味や出来のよしあしは判断していません</li>
</ul>
</div>
<p class="note">これは「ブログ 始め方」1語だけの結果です。ほかのキーワードでは、ちがう形になることがあります。</p>
'''
# ---- 記事5
a5='''<p>「順位を調べたい」と言っても、調べたいものは人によって違います。自分のサイトの順位か、他の人のサイトの順位か。ここでは、3つの方法の違いを、事実だけで整理します。</p>

<h2>3つの方法の比べ方</h2>
<div class="scroll"><table>
<thead><tr><th>見たいこと</th><th>Search Console（Google公式）</th><th>ブラウザで検索</th><th>このツール（C01）</th></tr></thead>
<tbody>
<tr><td>自分のサイトの順位</td><td>見られる（自分のサイトとして登録したもののみ）</td><td>1語ずつ手で探す</td><td>見られる（上位に入っていれば）</td></tr>
<tr><td>他人のサイトの順位</td><td>見られない</td><td>見られる（手作業）</td><td>見られる</td></tr>
<tr><td>まとめて調べる</td><td>自分のサイトの検索語を、一覧で見られる</td><td>できない（1語ずつ）</td><td>1語ずつ実行（その結果を表とCSVで保存）</td></tr>
<tr><td>上位100件の全データ</td><td>見られない</td><td>手作業になる</td><td>表とCSVで出る</td></tr>
<tr><td>費用</td><td>無料</td><td>無料</td><td>1語ごとに従量課金（10件で$0.004、100件で$0.0175を実測）</td></tr>
<tr><td>結果の性質</td><td>自分のサイトに、実際にあった表示と順位の記録</td><td>見る人の場所やログイン状態で変わることがある</td><td>指定した国・言語での結果（日本・日本語なら日本）</td></tr>
</tbody></table></div>
<p class="note">Search Consoleとブラウザの項目は、Googleが公開している一般的な説明にもとづいています。細かい仕様は変わることがあるので、使う前に公式で確認してください。</p>

<h2>どう使い分ける？</h2>
<ul>
<li><strong>自分のサイトが、どの言葉で何位か</strong> → Search Consoleが向いています。無料で、実際の表示の記録です。</li>
<li><strong>いま上位にどんなページがあるかを、1回見たい</strong> → ブラウザで検索すれば、無料で見られます。</li>
<li><strong>上位10〜100件を、表やCSVで残したい。他人のサイトも見たい</strong> → このツールが向いています。</li>
</ul>
<p>確認だけなら、まずSearch Consoleとブラウザでも十分です。表で残したくなったら、このツールを使ってみてください。</p>

<h2>このツールで、できないこと</h2>
<ul>
<li><strong>毎日の順位の追跡。</strong>実行したときの結果だけです。毎日自動で記録する機能はありません。</li>
<li><strong>あなたのブラウザと、まったく同じ結果。</strong>場所やログイン状態で、結果が変わることがあります。</li>
<li><strong>検索数やキーワードの難しさ。</strong>それは<a href="/C24/ja/">検索ボリュームを一括で見るツール</a>などで調べます。</li>
<li>AI概要の文章や出典は、このツールの表には出ません（<a href="/articles/c01-serp-features-20keywords/">枠が出るかどうかは数えられます</a>）。</li>
</ul>

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
<li>日付：2026年11月25日</li>
<li>費用と時間：C01（<a href="/C01/ja/">検索の上位を見る</a>）を実際に実行して測りました。10件は$0.004、100件は$0.0175（<a href="/articles/c01-blog-top100/">100件の記事</a>）</li>
<li>Search Consoleとブラウザの説明：Googleの公式の説明にもとづく一般的な内容です</li>
</ul>
</div>
'''
for slug,body in [('c01-blog-top100',a1),('c01-serp-features-20keywords',a2),('c01-top100-title-stats',a3),('c01-three-ways-to-check-rank',a5)]:
    open(R+f'articles/{slug}.html','w',encoding='utf-8').write(body)
idx=json.load(open(R+'articles/index.json',encoding='utf-8'))
idx=[a for a in idx if a['tool']!='C01']
idx+= [
 {"slug":"c01-blog-top100","tool":"C01","date":"2026-11-25","title":"【実測】「ブログ 始め方」で検索した上位100件を全部載せる（順位・タイトル・URL・ドメイン）","description":"「ブログ 始め方」の上位100件を、順位・タイトル・URL・ドメイン・説明文まで全部載せます。同じサイトが何回出たかも数えました。"},
 {"slug":"c01-serp-features-20keywords","tool":"C01","date":"2026-11-25","title":"【実測】検索結果の1ページ目に「青いリンク」は何本ある？AI概要や「他の人はこちらも質問」を20語で数えた","description":"20個のキーワードの1ページ目の中身を、種類ごとに数えました。AI概要が出たのは何語か、全データで見られます。"},
 {"slug":"c01-top100-title-stats","tool":"C01","date":"2026-11-25","title":"「ブログ 始め方」上位100件のタイトルを数えた：文字数、【】、年号、キーワード","description":"上位100件のタイトルの文字数と、含まれる言葉を数えました。途中で切れているタイトルがあるので、分けて数えています。"},
 {"slug":"c01-three-ways-to-check-rank","tool":"C01","date":"2026-11-25","title":"順位を調べる3つの方法：Search Console・ブラウザ・このツールで、何が違う？","description":"自分のサイトの順位と他人のサイトの順位で、向いている方法が違います。3つの方法の違いと、このツールでできないことを整理しました。"}]
idx.sort(key=lambda a:(a['tool'],a['slug']))
json.dump(idx,open(R+'articles/index.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(tot,sum(org),dict(dist),dict(tc))
