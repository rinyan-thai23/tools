import json,html
R='/home/user/tools/'
S=json.load(open(R+'articles/_inc/c02_stats.json'))
zero=S['zero']; zl=''.join(f'<li>{html.escape(k)}</li>' for k in zero)
top=S['top'][:10]; tq=dict(S['top_q'])
toprows=''.join(f'<tr><td>{html.escape(d)}</td><td>{n}</td><td>{tq[d]}</td></tr>' for d,n in top)
dist=''.join(f'<tr><td>{k}件</td><td>{v}問</td></tr>' for k,v in S['refs_dist'])
BOX='<li>日付：2026年11月25日、地域と言語：日本、日本語</li>\n<li>ツール：<a href="/C02/ja/">GoogleのAIモードの答えを見る（C02）</a>（DataForSEOのAPIが、GoogleのAIモードの答えを返します）</li>'
KW='「ブログ 始め方」「ブログ 収益化 いつから」「確定申告 やり方」「ワイヤレスイヤホン おすすめ」「ノートパソコン 選び方」「ユニクロ」「iPhone」「渋谷 ランチ」「京都 観光」「副業 おすすめ」「転職 エージェント 比較」「ChatGPT とは」「SEO とは」「キーワードプランナー 使い方」「新宿 美容院」「日経平均」「筋トレ 初心者」「カレー レシピ」「天気」「英会話 独学」'
a1=f'''<p>GoogleのAIモードは、質問に答える文章といっしょに、「どのサイトを参考にしたか」を出します。<a href="/C02/ja/">GoogleのAIモードの答えを見るツール</a>で、<strong>20個のキーワード</strong>を1回ずつ聞いて、答えと引用元を全部記録しました。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>20問のうち、引用元（リンク）が出たのは<strong>{S["n_withref"]}問</strong>、出なかったのは<strong>{len(zero)}問</strong>でした。</li>
<li>引用元は、合計<strong>{S["total_refs"]}件</strong>、ドメイン（サイトの名前）は<strong>{S["uniq_dom"]}種類</strong>でした。</li>
<li>1問あたりの引用は、最大<strong>{S["max_refs"]}件</strong>（「筋トレ 初心者」）。出た{S["n_withref"]}問の真ん中の値は{S["med_refs"]}件です。</li>
<li>答えの長さは、短いもので<strong>{S["md_min"]}文字</strong>、長いもので<strong>{S["md_max"]:,}文字</strong>でした（真ん中は約{S["md_med"]:,}文字）。</li>
</ul>
<p>先生に質問して、「参考にした本」を教えてもらうようなものです。20人に質問したら、5人は答えるだけで、本の名前を教えてくれませんでした。</p>

<h2>引用元が出なかった質問（{len(zero)}問）</h2>
<ul>{zl}</ul>
<p>この5問は、答えの文章は返ってきましたが、引用元のリンクは返りませんでした。</p>

<h2>引用元の数の分かれ方</h2>
<div class="scroll"><table class="data"><thead><tr><th>1問あたりの引用数</th><th>質問の数</th></tr></thead><tbody>{dist}</tbody></table></div>

<h2>全データ：質問ごとの表</h2>
<p>引用数、ドメイン数、通常の検索結果（上位10件）との重なり、回答の長さ、費用です。重なりについては<a href="/articles/c02-ai-mode-vs-top10/">別の記事</a>で数えました。</p>
<p><a href="/articles/data/c02-20questions-2026-11-25.csv" download>CSVでダウンロード（回答の全文を含む）</a></p>
<!--include:c02_summary-->

<h2>全データ：引用元（{S["total_refs"]}件）</h2>
<p>引用元の名前、ドメイン、タイトル、URLを、APIが返したまま載せています。</p>
<p><a href="/articles/data/c02-references-2026-11-25.csv" download>CSVでダウンロード</a></p>
<!--include:c02_refs-->

<h2>全データ：AIモードの答え（20問）</h2>
<p>返ってきた文章（markdown）を、そのまま載せています。「[ハイライトの開始]」などの印は、APIが返したままです。</p>
<!--include:c02_answers-->

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
<li>キーワード20個（私が選びました。質問、商品、ブランド、地域、ニュース、レシピなどを混ぜています）：{KW}</li>
<li>1つのキーワードにつき1回</li>
<li>費用：20回で<strong>${S["cost"]}</strong>（1回あたり$0.004）</li>
</ul>
</div>
<p class="note">AIモードの答えは、聞くたびに変わることがあります。これは「この日の1回ずつ」の結果です。</p>
'''
a2=f'''<p>AIモードが引用するサイトは、普通の検索結果の上位に出るサイトと同じなのでしょうか。<a href="/articles/c02-ai-mode-20-questions/">AIモードに聞いた20個のキーワード</a>について、同じ日に取った<a href="/C01/ja/">通常の検索結果（上位10件）</a>と、引用されたサイトを並べて数えました。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>引用元が出た{S["n_withref"]}問のうち、<strong>{len(S["ov_any"])}問</strong>で、通常の検索上位10件と<strong>同じドメイン</strong>が1つ以上ありました。1つも重ならなかったのは「{html.escape(S["ov_zero"][0])}」の1問です。</li>
<li>{S["n_withref"]}問で引用されたドメインは、のべ<strong>{S["tot_ds_withref"]}個</strong>。そのうち、通常の上位10件にも出たドメインは<strong>{S["tot_ov"]}個</strong>でした。</li>
<li>URLまで同じ（同じページ）だったのは、のべ<strong>{S["ovu_total"]}件</strong>でした。</li>
<li>重なりが一番多かったのは「筋トレ 初心者」（9ドメイン）、次が「転職 エージェント 比較」（7ドメイン）でした。</li>
</ul>
<p>「同じ生徒が、ふつうの成績表でも、先生のおすすめリストでも名前が出る」ような場合と、「リストにだけ出る」場合があった、ということです。</p>

<h2>全データ：質問ごとの、重なったドメイン</h2>
<!--include:c02_overlap-->

<h2>全データ：質問ごとの表</h2>
<p><a href="/articles/data/c02-20questions-2026-11-25.csv" download>CSVでダウンロード</a></p>
<!--include:c02_summary-->

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
<li>通常の検索結果：同じ日に、同じ20個のキーワードを、<a href="/C01/ja/">検索の上位を見る（C01）</a>と同じAPIで取りました（日本、日本語、上位10件）。<a href="/articles/c01-serp-features-20keywords/">別の記事</a>のデータです</li>
<li>数え方：ドメインは「www.」を除いて比べました。URLの重なりは、URLの文字が完全に一致したものです</li>
</ul>
</div>
<p class="note">20個のキーワードだけの結果です。ほかのキーワードや日では、違う数字になることがあります。</p>
'''
a3=f'''<p>GoogleのAIモードは、どのサイトを引用しているのでしょうか。<a href="/articles/c02-ai-mode-20-questions/">20個のキーワード</a>で出た引用元{S["total_refs"]}件を、ドメインごとに数えました。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>引用元は<strong>{S["total_refs"]}件</strong>、ドメインは<strong>{S["uniq_dom"]}種類</strong>でした。</li>
<li>一番多かったのは<strong>google.com（{S["top"][0][1]}回、{tq["google.com"]}問）</strong>で、次が<strong>youtube.com（{S["top"][1][1]}回、{tq["youtube.com"]}問）</strong>でした。</li>
<li>2回以上引用されたドメインは、上位{sum(1 for d,n in S["top"] if n>=2)}種類だけでした。残りは1回ずつでした。</li>
</ul>
<p>図書館でいうと、「同じ本が何度も紹介される」のではなく、ほとんどの本が1回ずつ出てくる、という様子です。</p>

<h2>引用の回数（上位10ドメイン）</h2>
<div class="scroll"><table class="data"><thead><tr><th>ドメイン</th><th>引用された回数</th><th>引用された質問の数</th></tr></thead><tbody>{toprows}</tbody></table></div>
<p class="note">google.comは、「渋谷 ランチ」などの質問で、Googleの検索結果ビューア（searchviewer）のURLが引用されたものです。youtube.comは、動画やショートのURLです。</p>

<h2>全データ：全ドメイン（{S["uniq_dom"]}種類）</h2>
<p><a href="/articles/data/c02-domains-2026-11-25.csv" download>CSVでダウンロード</a></p>
<!--include:c02_domains-->

<h2>全データ：引用元（{S["total_refs"]}件）</h2>
<p><a href="/articles/data/c02-references-2026-11-25.csv" download>CSVでダウンロード</a></p>
<details><summary>引用元の一覧を開く（{S["total_refs"]}件）</summary>
<!--include:c02_refs-->
</details>

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
<li>データ：<a href="/articles/c02-ai-mode-20-questions/">20個のキーワードの記事</a>と同じ</li>
<li>数え方：URLからドメインを取り出し、「www.」を除いて数えました。サブドメイン（biz.moneyforward.com と moneyforward.com など）は、別のドメインとして数えています</li>
</ul>
</div>
<p class="note">20個のキーワードだけの結果です。どのサイトが「よい」かの判断はしていません。</p>
'''
a5=f'''<p>GoogleのAIモードのAPIでは、何がわかって、何がわからないのでしょうか。<a href="/C02/ja/">GoogleのAIモードの答えを見るツール</a>を、実際に20回使って確かめた事実を整理します。</p>

<h2>わかること（実測）</h2>
<ul>
<li><strong>答えの文章。</strong>20回すべて、文章（markdown）が返りました。長さは{S["md_min"]}〜{S["md_max"]:,}文字でした。</li>
<li><strong>引用元のリンク。</strong>{S["n_withref"]}問では、引用元の名前、ドメイン、タイトル、URLが返りました。</li>
<li><strong>地域と言語の指定。</strong>日本・日本語で取れました。</li>
<li><strong>低い費用。</strong>1回$0.004。20回で${S["cost"]}でした。</li>
</ul>

<h2>わからないこと・できないこと（実測）</h2>
<ul>
<li><strong>引用元が出ない質問がある。</strong>20問のうち{len(zero)}問は、引用元のリンクが返りませんでした（<a href="/articles/c02-ai-mode-20-questions/">20問の記事</a>）。</li>
<li><strong>返るのはAIモードの答えだけ。</strong>20回とも、返ってきた項目は1つ（AIの答え）だけでした。通常の検索結果は、<a href="/C01/ja/">別のツール（C01）</a>で取ります。</li>
<li><strong>毎回同じ答えとは限らない。</strong>この日の1回の結果です。聞くたびに変わることがあります。</li>
<li><strong>あなたのサイトが引用されるための方法。</strong>データを見せるだけで、「こうすれば引用される」とは言えません。</li>
<li><strong>画面のAIモードと同じ見た目。</strong>返るのは文章と引用元のリンクで、画面の表示とは違います。</li>
</ul>

<h2>参考：返ってきた文章のようす</h2>
<ul>
<li>20問のうち{S["hl"]}問の文章に、「[ハイライトの開始]」「[ハイライトの終了]」という印が入っていました。</li>
<li>{S["inl"]}問の文章に、「[[1]](URL)」のような、文中のリンクが入っていました。</li>
</ul>

<h2>どう使い分ける？</h2>
<ul>
<li><strong>ちょっと確認したいだけ</strong> → GoogleのAIモードの画面で質問すれば、無料で見られます。</li>
<li><strong>20個、30個のキーワードで、答えと引用元を記録して、表やCSVで残したい</strong> → このツールが向いています。</li>
</ul>
<p>確認だけなら、まず画面で試してみてください。記録に残したくなったら、このツールを使ってみてください。</p>

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
<li>実測：<a href="/articles/c02-ai-mode-20-questions/">20個のキーワードの記事</a>のデータ（20回）</li>
</ul>
</div>
'''
for slug,body in [('c02-ai-mode-20-questions',a1),('c02-ai-mode-vs-top10',a2),('c02-ai-mode-cited-domains',a3),('c02-ai-mode-api-limits',a5)]:
    open(R+f'articles/{slug}.html','w',encoding='utf-8').write(body)
idx=json.load(open(R+'articles/index.json',encoding='utf-8')); idx=[a for a in idx if a['tool']!='C02']
idx+=[
 {"slug":"c02-ai-mode-20-questions","tool":"C02","date":"2026-11-25","title":"【実測】GoogleのAIモードに20の質問をしたら、引用されたサイトはどこだった？","description":"20個のキーワードをAIモードに聞いて、答えと引用元を全部記録しました。引用元が出たのは15問、出なかったのは5問でした。"},
 {"slug":"c02-ai-mode-vs-top10","tool":"C02","date":"2026-11-25","title":"AIモードが引用したサイトと、通常の検索上位10件は、どれくらい重なる？（20の質問）","description":"同じ日に取った通常の検索結果（上位10件）と、AIモードの引用元を、ドメインとURLで並べて数えました。"},
 {"slug":"c02-ai-mode-cited-domains","tool":"C02","date":"2026-11-25","title":"AIモードが引用するドメインを全部数えた（75件・58ドメイン）","description":"AIモードの引用元75件を、ドメインごとに数えました。2回以上引用されたドメインは少数でした。"},
 {"slug":"c02-ai-mode-api-limits","tool":"C02","date":"2026-11-25","title":"AIモードのAPIで、わかること・わからないこと（20回の実測）","description":"20回使って確かめた、AIモードのAPIで返るもの・返らないものを整理しました。引用元が出ない質問もありました。"}]
idx.sort(key=lambda a:(a['tool'],a['slug'])); json.dump(idx,open(R+'articles/index.json','w',encoding='utf-8'),ensure_ascii=False,indent=1); print(len(idx))
