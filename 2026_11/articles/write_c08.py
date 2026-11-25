import json,html
R='/home/user/tools/'
S=json.load(open(R+'articles/_inc/c08_stats.json')); H=html.escape
BOX='''<li>日付：2026年11月25日、地域と言語：日本、日本語</li>
<li>ツール：<a href="/C08/ja/">検索窓のサジェストを見る（C08）</a>（DataForSEOのAPIが、Googleの検索候補を返します）</li>'''
KW='「ブログ 始め方」「ブログ 収益化 いつから」「確定申告 やり方」「ワイヤレスイヤホン おすすめ」「ノートパソコン 選び方」「ユニクロ」「iPhone」「渋谷 ランチ」「京都 観光」「副業 おすすめ」「転職 エージェント 比較」「ChatGPT とは」「SEO とは」「キーワードプランナー 使い方」「新宿 美容院」「日経平均」「筋トレ 初心者」「カレー レシピ」「天気」「英会話 独学」'
COST_N=lambda n:f'<li>費用：1回につき<strong>$0.002</strong>（約0.3円）。この記事のデータ{n}回で<strong>${n*0.002:.3f}</strong></li>'
nA=S['nA']
a1=f'''<p>Googleの検索窓に言葉を入れると、候補（サジェスト）が出ます。「みんながよく調べている言い方」のヒントになります。<a href="/C08/ja/">検索窓のサジェストを見るツール</a>で、<strong>20個の言葉</strong>の候補を取って、全部載せます。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>20個の言葉で、候補は合計<strong>{S["A_total"]}件</strong>でした。</li>
<li>1つの言葉に出た候補は、<strong>最大15件</strong>でした。15件出たのは、20語のうち<strong>{len(S["A15"])}語</strong>です。</li>
<li>候補が少なかったのは、「ブログ 収益化 いつから」の<strong>2件</strong>と、「転職 エージェント 比較」の<strong>0件</strong>（「No Search Results」）でした。</li>
<li>「iPhone」では「iphone18」「iphone17」「iphone18pro」、「SEO とは」では「<strong>ceo とは</strong>」が最初に出ました。</li>
</ul>
<p>お店でいうと、「店に入る前に、店員さんが『こんな商品はいかがですか』と15個まで見せてくれる」ようなものです。</p>

<h2>言葉ごとの、候補の数</h2>
<!--include:c08_a_counts-->

<h2>全データ：20語の候補（{S["A_total"]}件）</h2>
<p>候補と、APIが返す「relevance」の数字です。relevanceの意味は、このデータからは分かりません。検索数ではありません。</p>
<p><a href="/articles/data/c08-20keywords-suggestions-2026-11-25.csv" download>CSVでダウンロード</a></p>
<!--include:c08_a_table-->

<h2>この表から作った記事</h2>
<ul>
<li><a href="/articles/c08-blog-kana-suggest/">「ブログ」のあとに「あ〜ん」を足したら</a></li>
<li><a href="/articles/c08-suggest-count/">候補の数は、言葉によってどれくらい違う？</a></li>
<li><a href="/articles/c08-fan-out-vs-suggest/">ChatGPTの内部の検索ワードは、Googleの候補に出る言い方？</a></li>
<li><a href="/articles/c08-suggest-limits/">サジェストを調べる方法と、わからないこと</a></li>
</ul>

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
<li>キーワード20個（私が選びました）：{KW}</li>
{COST_N(20)}
</ul>
</div>
<p class="note">検索候補は、時間や場所で変わります。この日の日本の結果です。「候補にある＝検索されている」の証明ではありません。</p>
'''
a2=f'''<p>「ブログ」のあとに、ひらがなを1文字足すと、候補は変わります。「ブログ あ」「ブログ い」…と、<strong>「あ」から「ん」まで46文字</strong>を足して、候補を全部取りました。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>46回の呼び出しで、候補は合計<strong>{S["B_total"]}件</strong>、重なりを除くと<strong>{S["B_uniq"]}件</strong>でした。</li>
<li>46文字のうち、<strong>{S["B15"]}文字</strong>で、候補が上限の15件出ました。14件が2回（「け」「ね」）、13件が1回（「や」）でした。</li>
<li>候補が0件の文字は、ありませんでした。</li>
<li>たとえば、「ブログ あ」は「ブログ アフィリエイト」「ブログ アプリ」「ブログ アメーバ」、「ブログ か」は「ブログ 書き方」「ブログ 稼ぎ方」「ブログ 稼ぐ」などでした。</li>
</ul>
<p>辞書の「あ行」「か行」を順に開いて、ブログに関する言葉を書き出していくのと似ています。</p>

<h2>文字ごとの、候補の数</h2>
<!--include:c08_b_counts-->

<h2>全データ：重なりを除いた候補（{S["B_uniq"]}件）</h2>
<!--include:c08_b_unique-->

<h2>全データ：46文字の候補（{S["B_total"]}件）</h2>
<p><a href="/articles/data/c08-blog-kana-suggestions-2026-11-25.csv" download>CSVでダウンロード</a></p>
<details><summary>46文字×候補の表を開く（{S["B_total"]}件）</summary>
<!--include:c08_b_table-->
</details>

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
<li>入力：「ブログ あ」「ブログ い」…「ブログ ん」の46個（ひらがなの基本の46文字）</li>
{COST_N(46)}
</ul>
</div>
<p class="note">1つの言葉の、この日の結果です。濁音（が・ざ…）や英字、数字は足していません。</p>
'''
a3=f'''<p>検索候補は、いつも同じ数だけ出るのでしょうか。<a href="/articles/c08-20-keywords-suggest/">20語</a>、<a href="/articles/c08-blog-kana-suggest/">「ブログ＋ひらがな」46個</a>、<a href="/articles/c08-fan-out-vs-suggest/">ChatGPTの内部の検索ワードの前半</a>23個、合わせて<strong>{S["calls"]}回</strong>の結果で、候補の数を数えました。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>候補の数は、<strong>最大15件</strong>でした。{S["calls"]}回のうち<strong>{S["n15"]}回</strong>が、ちょうど15件でした。</li>
<li>20語では、15件が{len(S["A15"])}語、15件未満が{20-len(S["A15"])}語。一番少ないのは0件（転職 エージェント 比較）でした。</li>
<li>ひらがなを足した46個では、{S["B15"]}個が15件でした。</li>
<li>0件の2回（「転職 エージェント 比較」「最新 ノートパソコン おすすめ」）は、<strong>料金がかかりました</strong>（1回$0.002）。</li>
</ul>
<p>コップに水を注ぐと、15杯分までしか入らない。ほとんどの言葉で、コップはいっぱいになりました。</p>

<h2>20語の、候補の数</h2>
<!--include:c08_a_counts-->

<h2>46個（ブログ＋ひらがな）の、候補の数</h2>
<!--include:c08_b_counts-->

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
<li>データ：<a href="/articles/c08-20-keywords-suggest/">20語</a>・<a href="/articles/c08-blog-kana-suggest/">46個</a>・<a href="/articles/c08-fan-out-vs-suggest/">23個</a>の、合計{S["calls"]}回</li>
{COST_N(S["calls"])}
</ul>
</div>
<p class="note">上限の15件は、この日のこのAPIの結果です。一般的な決まりかどうかは、確かめていません。</p>
'''
a4=f'''<p>ChatGPTは、答える前に、自分で検索しています（<a href="/articles/c18-fan-out-queries/">内部の検索ワードの記事</a>）。その検索ワードは、Googleの検索候補に出てくる「みんなが使う言い方」なのでしょうか。確かめました。</p>

<h2>やり方</h2>
<p>内部の検索ワード24個のうち、2語以上の23個について、「最後の1語を除いた前半」をGoogleの検索窓に入れました。たとえば「渋谷 おすすめ ラーメン店」なら、「渋谷 おすすめ」を入れて、候補に「渋谷 おすすめ ラーメン店」が出るかを見ました。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>23個のうち、<strong>候補に同じ言葉が出たのは{S["exact"]}個</strong>でした。{S["tested"]-S["exact"]}個は出ませんでした。</li>
<li>「最新 ノートパソコン おすすめ 2023」の前半（「最新 ノートパソコン おすすめ」）は、<strong>候補が0件</strong>でした。</li>
<li>「今日の東京の天気」は、1語だったので、この確かめ方の対象にしていません。</li>
</ul>
<p>ChatGPTが検索に使う言葉と、人が検索窓に打つ言葉は、重なる部分もあれば、重ならない部分もある、ということです。</p>

<h2>全データ：24個の内部の検索ワードと、候補</h2>
<p><a href="/articles/data/c08-fanout-vs-suggest-2026-11-25.csv" download>CSVでダウンロード（候補の一覧つき）</a></p>
<!--include:c08_c_table-->

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
<li>内部の検索ワード：<a href="/articles/c18-fan-out-queries/">ChatGPTの内部の検索ワードの記事</a>の24個（重なりを除く）</li>
<li>確かめ方：最後の1語を除いた前半を入力して、候補に、同じ言葉（スペースと大文字小文字を無視）があるかを見ました</li>
{COST_N(S["nC"])}
</ul>
</div>
<p class="note">「前半を入れる」方法での確認です。別の入れ方では、結果が違うことがあります。内部の検索ワードは、聞き方によっても変わります。</p>
'''
a5=f'''<p>サジェストのAPIでは、何がわかって、何がわからないのでしょうか。<a href="/C08/ja/">検索窓のサジェストを見るツール</a>で{S["calls"]}回調べて、確かめた事実を整理します。</p>

<h2>わかること（実測）</h2>
<ul>
<li><strong>入力した言葉の、検索候補。</strong>候補の文字と、APIが返す「relevance」の数字が返ります。</li>
<li><strong>低い費用。</strong>1回$0.002（約0.3円）。{S["calls"]}回で${S["cost"]}。</li>
</ul>

<h2>わからないこと・気をつけること（実測）</h2>
<ul>
<li><strong>候補は最大15件。</strong>{S["calls"]}回のうち{S["n15"]}回が、ちょうど15件でした。</li>
<li><strong>0件になる言葉がある。</strong>「転職 エージェント 比較」と「最新 ノートパソコン おすすめ」は「No Search Results」でした。<strong>0件でも、料金はかかりました。</strong></li>
<li><strong>入力と違う候補が出ることがある。</strong>「SEO とは」を入れたら、最初の候補が「ceo とは」でした。</li>
<li><strong>表記がそろえられる。</strong>「ChatGPT とは」の候補は「chatgpt とは…」と小文字で返りました。</li>
<li><strong>検索数ではない。</strong>候補の順や「relevance」は、検索の多さそのものではありません。検索数は<a href="/C24/ja/">別のツール（C24）</a>で調べます。</li>
<li><strong>この日の日本の結果。</strong>時間や場所、人で変わることがあります。</li>
</ul>

<h2>どう使い分ける？</h2>
<ul>
<li><strong>1つの言葉の候補を、ちょっと見たい</strong> → Googleの検索窓に、そのまま入力すれば、無料で見られます。</li>
<li><strong>たくさんの言葉の候補を、表やCSVで残したい</strong> → このツールが向いています。「ブログ＋あ〜ん」のような使い方もできます。</li>
</ul>
<p>確認だけなら、まず検索窓で十分です。何十個もの言葉を一度に残したくなったら、このツールを使ってみてください。</p>

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
<li>データ：<a href="/articles/c08-20-keywords-suggest/">20語</a>・<a href="/articles/c08-blog-kana-suggest/">46個</a>・<a href="/articles/c08-fan-out-vs-suggest/">23個</a>の、合計{S["calls"]}回</li>
{COST_N(S["calls"])}
</ul>
</div>
'''
for slug,body in [('c08-20-keywords-suggest',a1),('c08-blog-kana-suggest',a2),('c08-suggest-count',a3),('c08-fan-out-vs-suggest',a4),('c08-suggest-limits',a5)]:
    open(R+f'articles/{slug}.html','w',encoding='utf-8').write(body)
idx=json.load(open(R+'articles/index.json',encoding='utf-8')); idx=[a for a in idx if a['tool']!='C08']
idx+=[
 {"slug":"c08-20-keywords-suggest","tool":"C08","date":"2026-11-25","title":f"【実測】20個の言葉の検索候補（サジェスト）を全部載せる（{S['A_total']}件）","description":"20個の言葉の検索候補を、全部載せます。候補は最大15件で、「転職 エージェント 比較」は0件でした。"},
 {"slug":"c08-blog-kana-suggest","tool":"C08","date":"2026-11-25","title":f"「ブログ」のあとに「あ〜ん」を足したら、候補は何個出る？（46回で{S['B_total']}件）","description":f"「ブログ あ」から「ブログ ん」まで46回調べて、候補{S['B_total']}件（重なりを除いて{S['B_uniq']}件）を全部載せました。"},
 {"slug":"c08-suggest-count","tool":"C08","date":"2026-11-25","title":"候補の数は、言葉によってどれくらい違う？（上限は15件だった）","description":f"{S['calls']}回の結果で、候補の数を数えました。{S['n15']}回がちょうど15件でした。0件の回も料金がかかりました。"},
 {"slug":"c08-fan-out-vs-suggest","tool":"C08","date":"2026-11-25","title":"ChatGPTの内部の検索ワードは、Googleの検索候補に出る言い方？（23個で確かめた）","description":f"ChatGPTが内部で検索した言葉の前半をGoogleに入れて、候補に同じ言葉が出るかを確かめました。出たのは{S['exact']}個でした。"},
 {"slug":"c08-suggest-limits","tool":"C08","date":"2026-11-25","title":"サジェストを調べる方法の違いと、このツールでわからないこと","description":"最大15件、0件でも有料、入力と違う候補が出ることなど、89回で確かめた限界を整理しました。"}]
idx.sort(key=lambda a:(a['tool'],a['slug'])); json.dump(idx,open(R+'articles/index.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
c=json.load(open(R+'articles/costs.json',encoding='utf-8'))
per={'c08-20-keywords-suggest':(0.04,'20語×$0.002'),'c08-blog-kana-suggest':(0.092,'46回×$0.002'),'c08-suggest-count':(S['cost'],f'{S["calls"]}回×$0.002（0件の回も有料）'),'c08-fan-out-vs-suggest':(0.046,'23回×$0.002'),'c08-suggest-limits':(S['cost'],f'{S["calls"]}回ぶんの実測を使用')}
for k,(u,n) in per.items(): c['per'][k]={'usd':u,'note':n}
c['real']['C08']=S['cost']
json.dump(c,open(R+'articles/costs.json','w',encoding='utf-8'),ensure_ascii=False,indent=1); print(len(idx))
