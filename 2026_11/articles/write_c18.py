import json,csv,collections,html
R='/home/user/tools/'
S=json.load(open(R+'articles/_inc/c18_stats.json'))
rr=list(csv.DictReader(open(R+'site/articles/data/c18-ramen-10runs-2026-11-25.csv',encoding='utf-8-sig')))
sets=collections.Counter(tuple(sorted(x['店名(答えに出た順)'].split(' / '))) for x in rr)
sets_txt=''.join(f'<tr><td>{html.escape(" ／ ".join(k))}</td><td>{v}</td></tr>' for k,v in sets.most_common())
shops=dict(S['r1_shops']); fq=S['r1_fq']
fq_txt=''.join(f'<tr><td>{html.escape(k)}</td><td>{v}</td></tr>' for k,v in fq)
tok=S['r1_ans_tokens']
n40=S['n40']; ns=S['searched']
top=S['dom_top'][:8]
top_txt=''.join(f'<tr><td>{html.escape(d)}</td><td>{c}</td></tr>' for d,c in top)
no_txt=''.join(f'<li>{html.escape(p)}</li>' for _,p in S['nosearch'])
y=S['y23']
y_txt=''.join(f'<tr><td>{html.escape(b)}</td><td>{html.escape(c)}</td></tr>' for a,b,c in y)
NOTE='このツールが呼ぶChatGPTは<strong>gpt-4o-mini（モデル名：gpt-4o-mini-2024-07-18）、Web検索ができる設定</strong>です。画面のChatGPTと同じ答えになるとは限りません。'
a1=f'''<p>お店のオーナーなら、「お客さんがChatGPTに聞いたとき、うちの店は出てくるのかな」と気になります。でも、ChatGPTは聞くたびに答えが変わる、と聞いたことがあるかもしれません。それなら、<strong>同じ質問を10回</strong>したら、どれくらい変わるのでしょうか。<a href="/C18/ja/">ChatGPTの答えを見るツール</a>で、実際に10回聞いてみました。</p>

<h2>聞いた質問</h2>
<div class="box"><strong>渋谷でおすすめのラーメン店を3つ教えてください</strong></div>
<p>{NOTE}</p>

<h2>先に、わかったこと</h2>
<ul>
<li>10回の答えは、<strong>3つの店の組み合わせ</strong>に分かれました（表記ゆれを含みます）。</li>
<li>「らーめん はやし」は<strong>10回すべて</strong>、「鬼そば 藤谷」は<strong>{shops.get("鬼そば 藤谷")}回</strong>に出ました。</li>
<li>3つ目の店は、「喜楽」が{shops.get("喜楽")}回、「中華麺店 喜楽」が{shops.get("中華麺店 喜楽")}回、「麺処まろ」が{shops.get("麺処まろ")}回でした。</li>
<li>ChatGPTが答える前に内部で検索した言葉は、ほぼ同じでしたが、少し違う回もありました。</li>
</ul>
<p>くじ引きでいうと、「1等と2等はほぼ毎回当たるけれど、3等はたまに入れ替わる」という感じです。</p>

<h2>店の出方</h2>
<div class="scroll"><table class="data"><thead><tr><th>答えに書かれた店名</th><th>10回のうち出た回数</th></tr></thead><tbody>
{''.join(f'<tr><td>{html.escape(k)}</td><td>{v}</td></tr>' for k,v in S["r1_shops"])}
</tbody></table></div>
<p class="note">「喜楽」と「中華麺店 喜楽」は、書かれた名前のまま別に数えています。同じ店かどうかの判断はしていません。</p>

<h2>店の組み合わせ（10回）</h2>
<div class="scroll"><table class="data"><thead><tr><th>答えに出た店の組み合わせ</th><th>回数</th></tr></thead><tbody>
{sets_txt}
</tbody></table></div>

<h2>ChatGPTが内部で検索した言葉</h2>
<p>答える前に、ChatGPTは自分で検索しています。その言葉です（APIが返した<code>fan_out_queries</code>）。</p>
<div class="scroll"><table class="data"><thead><tr><th>内部の検索ワード</th><th>10回のうち</th></tr></thead><tbody>{fq_txt}</tbody></table></div>
<p>内部の検索ワードは、<a href="/articles/c18-fan-out-queries/">別の記事</a>で全部並べました。</p>

<h2>全データ（10回ぶん）</h2>
<p>1回ごとの店名、内部の検索ワード、参照したページ数、使ったトークン、費用です。出力トークンは{tok[0]}〜{tok[1]}の間でした。</p>
<p><a href="/articles/data/c18-ramen-10runs-2026-11-25.csv" download>CSVでダウンロード（回答の全文を含む）</a></p>
<!--include:c18_runs-->

<h2>回答の全文（10回）</h2>
<p>返ってきた文章を、そのまま載せています。店名の文字には、Googleマップの検索リンクがついています。</p>
<!--include:c18_answers10-->

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
<li>日付：2026年11月25日</li>
<li>質問：「{html.escape("渋谷でおすすめのラーメン店を3つ教えてください")}」（同じ文を10回、続けて）</li>
<li>モデル：gpt-4o-mini（gpt-4o-mini-2024-07-18）、Web検索ができる設定</li>
<li>ツール：<a href="/C18/ja/">ChatGPTの答えを見る（C18）</a></li>
<li>費用：10回で<strong>${S["cost_r1"]}</strong>（1回あたり約$0.027）</li>
</ul>
</div>
<p class="note">1つの質問、1つの日付の結果です。ほかの質問や日にちでは、違う結果になることがあります。実在のお店の名前は、ChatGPTが答えた文字をそのまま載せたもので、お店の評価ではありません。</p>
'''
a2=f'''<p>ChatGPTは、質問されると、いつもWeb検索をしているのでしょうか。<a href="/C18/ja/">ChatGPTの答えを見るツール</a>で、<strong>40の質問</strong>を1回ずつ聞いて、検索したか、どのページを参照したかを全部記録しました。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>40の質問のうち、Web検索をしたのは<strong>{ns}問</strong>、しなかったのは<strong>{n40-ns}問</strong>でした。</li>
<li>Web検索をしたのは、「お店を3つ教えて」のような<strong>場所の質問</strong>や、「最新の」「今日の」を含む質問が中心でした。</li>
<li>検索をした{ns}問が参照したページは、合計<strong>{S["nrefs"]}件</strong>（重なりを含む）で、ドメインは<strong>{S["dom_n"]}種類</strong>でした。</li>
<li>検索をしたときとしないときで、1回の費用が大きく違いました（下の表）。</li>
</ul>

<h2>検索あり・なしで、費用がちがう</h2>
<div class="scroll"><table class="data"><thead><tr><th></th><th>回数</th><th>1回あたりの費用(USD)</th><th>入力トークン(平均)</th><th>出力トークン(平均)</th></tr></thead><tbody>
<tr><td>Web検索あり</td><td>{S["n_s"]}</td><td>{S["s_cost"]}</td><td>{S["s_it"]:,}</td><td>{S["s_ot"]:,}</td></tr>
<tr><td>Web検索なし</td><td>{S["n_n"]}</td><td>{S["n_cost"]}</td><td>{S["n_it"]:,}</td><td>{S["n_ot"]:,}</td></tr>
</tbody></table></div>
<p class="note">この表は、前の記事の10回（渋谷のラーメン）と、この記事の40問を合わせた{S["n_s"]+S["n_n"]}回の平均です。</p>
<p>検索ありは、検索で見つけたページの文章が入力に加わるので、入力トークンが大きく増えます。そのぶん、費用も大きくなります。</p>

<h2>Web検索をしなかった質問（{n40-ns}問）</h2>
<ul>{no_txt}</ul>

<h2>参照されたドメイン（上位）</h2>
<p>検索をした質問のうち、そのドメインが参照された質問の数です。</p>
<div class="scroll"><table class="data"><thead><tr><th>ドメイン</th><th>質問の数</th></tr></thead><tbody>{top_txt}</tbody></table></div>
<p>google.comは、お店の質問でGoogleマップの検索リンクが参照ページに入っていたものです。全ドメインの一覧は<a href="/articles/data/c18-domains-2026-11-25.csv" download>CSV</a>にあります。</p>

<h2>全データ：40の質問</h2>
<p>質問ごとに、Web検索の有無、内部の検索ワード、参照ページ数、ドメイン数、トークン、費用です。</p>
<p><a href="/articles/data/c18-40prompts-2026-11-25.csv" download>CSVでダウンロード（回答の全文を含む・40行）</a></p>
<!--include:c18_prompts-->

<h2>全データ：参照したページ（{S["nrefs"]}件）</h2>
<p>APIが返した参照ページを、URLのまま全部載せています（「?utm_source=openai」は除いています）。タイトルや抜粋は、APIが返さなかったので空欄です。</p>
<p><a href="/articles/data/c18-40prompts-references-2026-11-25.csv" download>CSVでダウンロード</a></p>
<details><summary>参照ページの一覧を開く（{S["nrefs"]}件）</summary>
<!--include:c18_refs-->
</details>

<h2>全データ：回答の全文（40問）</h2>
<!--include:c18_answers40-->

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
<li>日付：2026年11月25日</li>
<li>質問40個：一般的な質問20個（ブログ、家電、旅行、お金、レシピなど）と、新しさ・場所・価格をふくむ質問20個。私が選びました。1つの質問につき1回</li>
<li>モデル：gpt-4o-mini（gpt-4o-mini-2024-07-18）、Web検索ができる設定（使うかどうかは、ChatGPTが決めます）</li>
<li>ツール：<a href="/C18/ja/">ChatGPTの答えを見る（C18）</a></li>
<li>費用：40問で<strong>${S["cost_40"]}</strong></li>
</ul>
</div>
<p class="note">{NOTE}検索をするかどうかは、質問の言い方でも変わると考えられます。この結果は、この40問についてのものです。</p>
'''
a3=f'''<p>ChatGPTは、答える前に、自分で検索しています。そのとき、どんな言葉で検索しているのでしょうか。APIは、その言葉（<code>fan_out_queries</code>）を返してくれます。<a href="/C18/ja/">ChatGPTの答えを見るツール</a>で聞いた50回のうち、検索した{S["n_s"]}回の内部の検索ワード<strong>{S["fq_total"]}個</strong>を、全部載せます。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>50回のうち、Web検索をしたのは<strong>{S["n_s"]}回</strong>で、内部の検索ワードは<strong>{S["fq_total"]}個</strong>でした（1回につき1個）。</li>
<li>内部の検索ワードは、質問の文章そのものではなく、<strong>短い言葉</strong>に直されていました。たとえば「渋谷でおすすめのラーメン店を3つ教えてください」は、「渋谷 おすすめ ラーメン店」になりました。</li>
<li>{S["fq_total"]}個のうち<strong>{len(y)}個</strong>に、<strong>「2023」</strong>の文字が入っていました。調べた日は2026年11月25日です。</li>
</ul>
<p>たとえば、「お手紙を書くとき、日付を去年のままにしてしまった」ような状態です。実際に起きた数なので、そのまま載せます。</p>

<h2>「2023」が入っていた内部の検索ワード（{len(y)}個）</h2>
<div class="scroll"><table class="data"><thead><tr><th>聞いた質問</th><th>内部の検索ワード</th></tr></thead><tbody>{y_txt}</tbody></table></div>

<h2>全データ：内部の検索ワード（{S["fq_total"]}個）</h2>
<p>質問と、そのときの内部の検索ワードです（ID：R＝同じ質問を10回、Q＝一般的な質問、W＝新しさ・場所・価格の質問）。</p>
<p><a href="/articles/data/c18-fanout-2026-11-25.csv" download>CSVでダウンロード</a></p>
<!--include:c18_fanout-->

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
<li>日付：2026年11月25日</li>
<li>データ：<a href="/articles/c18-ramen-10-times/">同じ質問を10回</a>と、<a href="/articles/c18-40-prompts-references/">40の質問</a>のAPI結果（合計50回）</li>
<li>ツール：<a href="/C18/ja/">ChatGPTの答えを見る（C18）</a></li>
<li>数え方：APIが返した内部の検索ワードを、そのまま数えました</li>
</ul>
</div>
<p class="note">{NOTE}「2023」が入る理由は、このデータからは分かりません。同じ現象が、ほかの質問やモデルでも起きるかは確かめていません。</p>
'''
a5=f'''<p>「ChatGPTの画面で聞けば同じでは？」と思うかもしれません。<a href="/C18/ja/">ChatGPTの答えを見るツール</a>は、ChatGPTのAPIを使っています。画面と同じではありません。ここでは、分かっている違いと、実測した事実を整理します。</p>

<h2>違いを並べる</h2>
<div class="scroll"><table>
<thead><tr><th>項目</th><th>ChatGPTの画面</th><th>このツール（API）</th></tr></thead>
<tbody>
<tr><td>使うモデル</td><td>画面や契約の種類で変わることがあります（OpenAIの公式で確認）</td><td>gpt-4o-mini（実測：gpt-4o-mini-2024-07-18）</td></tr>
<tr><td>Web検索</td><td>画面の設定や質問による</td><td>使える設定。使うかどうかはChatGPTが決める（実測：40問のうち{ns}問で検索）</td></tr>
<tr><td>あなたの履歴・設定</td><td>ログインした人の履歴や設定が影響することがあります</td><td>履歴のない、1回ごとの質問</td></tr>
<tr><td>結果の保存</td><td>画面を見る</td><td>表とCSVで保存できる</td></tr>
<tr><td>まとめて確認</td><td>1問ずつ</td><td>1問ずつ実行（結果をCSVで保存）</td></tr>
<tr><td>内部の検索ワード</td><td>画面では見えない</td><td>見える（実測：検索した{S["n_s"]}回で{S["fq_total"]}個）</td></tr>
<tr><td>費用</td><td>契約による（公式で確認）</td><td>1回ごとの従量課金（実測：検索あり約${S["s_cost"]}、検索なし約${S["n_cost"]}）</td></tr>
</tbody></table></div>
<p class="note">ChatGPTの画面についての項目は、一般的な説明です。細かい仕様は変わることがあるので、公式で確認してください。</p>

<h2>どう使い分ける？</h2>
<ul>
<li><strong>自分の画面で、ちょっと試してみたい</strong> → ChatGPTの画面で十分です。無料でも試せます。</li>
<li><strong>お客さんがどう聞いても同じ状態で、答えを記録したい。内部の検索ワードも見たい</strong> → このツールが向いています。</li>
</ul>
<p>確認だけなら、まずChatGPTの画面で聞いてみてください。記録として残したくなったら、このツールを使ってみてください。</p>

<h2>このツールで、できないこと</h2>
<ul>
<li><strong>画面のChatGPTと、同じ答えを出すこと。</strong>モデルや条件が違います。</li>
<li><strong>同じ質問で、いつも同じ答えを出すこと。</strong>10回聞いて、店の組み合わせは{S["r1_sets"]}通りに分かれました（<a href="/articles/c18-ramen-10-times/">10回の記事</a>）。</li>
<li><strong>ChatGPTに載る方法を教えること。</strong>データを見せるだけで、「こうすれば載る」とは言えません。</li>
<li><strong>Claude・Gemini・Perplexityの答え。</strong>それぞれ別のツール（C19・C20・C21）です。</li>
</ul>

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
<li>日付：2026年11月25日</li>
<li>実測：<a href="/articles/c18-ramen-10-times/">10回の記事</a>と<a href="/articles/c18-40-prompts-references/">40問の記事</a>の結果（合計50回）</li>
<li>ChatGPTの画面についての説明：一般的な内容です</li>
</ul>
</div>
'''
for slug,body in [('c18-ramen-10-times',a1),('c18-40-prompts-references',a2),('c18-fan-out-queries',a3),('c18-api-vs-chatgpt-app',a5)]:
    open(R+f'articles/{slug}.html','w',encoding='utf-8').write(body)
idx=json.load(open(R+'articles/index.json',encoding='utf-8'))
idx=[a for a in idx if a['tool']!='C18']
idx+=[
 {"slug":"c18-ramen-10-times","tool":"C18","date":"2026-11-25","title":"【実測】同じ質問をChatGPTに10回聞いたら、答えは毎回同じだった？（渋谷のラーメン店）","description":"同じ質問を10回聞いて、答えに出た店と内部の検索ワードを全部載せました。毎回同じ店と、入れ替わる店がありました。"},
 {"slug":"c18-40-prompts-references","tool":"C18","date":"2026-11-25","title":"【実測】ChatGPTが参照したサイトを全部見る：40の質問のうち、Web検索をしたのは21問","description":"40の質問を1回ずつ聞いて、Web検索をしたか、どのページを参照したかを全部記録しました。検索あり・なしの費用の違いも実測しています。"},
 {"slug":"c18-fan-out-queries","tool":"C18","date":"2026-11-25","title":"ChatGPTは答える前に、何を検索している？内部の検索ワード31個を全部載せる","description":"APIが返す、ChatGPTが内部で検索した言葉を全部載せました。「2023」が入った検索ワードの一覧もあります。"},
 {"slug":"c18-api-vs-chatgpt-app","tool":"C18","date":"2026-11-25","title":"ChatGPTの画面で聞くのと、このツール（API）で聞くのは何が違う？できないことも","description":"画面のChatGPTとの違いを、事実で整理しました。同じ答えにならない点と、このツールでできないことも書いています。"}]
idx.sort(key=lambda a:(a['tool'],a['slug']))
json.dump(idx,open(R+'articles/index.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(idx))
