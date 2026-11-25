import json,html
R='/home/user/tools/'
S=json.load(open(R+'articles/_inc/c23_stats.json'))
n=S['n']; z=S['zero']; nz=S['nz']; b=S['bins']
pct=lambda a,t: f'{a/t*100:.1f}'
t10=S['top10']
top_rows=''.join(f'<tr><td>{html.escape(k)}</td><td>{a}</td><td>{g:,}</td></tr>' for k,a,g in t10)
g1k=S['g_gt1000']
g1k_rows=''.join(f'<tr><td>{html.escape(k)}</td><td>{g:,}</td><td>{a}</td></tr>' for k,g,a in g1k)
cor_rows=''.join(f'<tr><td>{html.escape(k)}</td><td>{"" if r is None else r}</td></tr>' for k,r in S['cors'])
BOX=f'''<li>日付：2026年11月25日、地域と言語：日本、日本語</li>
<li>ツール：<a href="/C23/ja/">AIでの質問回数を見る（C23）</a>（DataForSEOのAPIが、AIでの質問回数を返します）</li>'''
INPUT='<li>キーワード：<a href="/articles/c24-keyword-volume-538/">検索ボリュームの記事</a>と同じ538語（SEO関連。重なりは除いています）。APIは、アルファベットを小文字にして返します</li>'
a1=f'''<p>「AIでどれくらい質問されているか」を数字で見られるAPIがあります。<a href="/C23/ja/">AIでの質問回数を見るツール</a>で、<a href="/articles/c24-keyword-volume-538/">Googleの検索数を調べた538語</a>と同じ言葉を、全部調べました。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>538語のうち、AIでの質問回数が<strong>0より大きかったのは{nz}語（{pct(nz,n)}%）</strong>、<strong>0だったのは{z}語（{pct(z,n)}%）</strong>でした。</li>
<li>一番多かったのは<strong>「{html.escape(S["max_kw"])}」の{S["maxv"]}回</strong>です。</li>
<li>0より大きかった{nz}語の内訳は、1〜9回が{b["1〜9"]}語、10〜99回が{b["10〜99"]}語、100回以上が{b["100以上"]}語でした。</li>
<li>538語の合計は<strong>{S["sum_ai"]:,}回</strong>（月間）でした。</li>
</ul>
<p>Googleの検索数では、大きな数字の言葉がたくさんありました。AIでの質問回数は、同じ言葉でも、ずっと小さい数字でした。</p>

<h2>AIでの質問回数が多かった上位10語</h2>
<div class="scroll"><table class="data"><thead><tr><th>キーワード</th><th>AIでの質問回数</th><th>Googleの月間検索数（C24）</th></tr></thead><tbody>{top_rows}</tbody></table></div>

<h2>全データ：538語（月別の数字つき）</h2>
<p>「AIでの質問回数（直近）」と、{S["months"][0]}〜{S["months"][1]}の12か月分を、APIが返したまま載せています。</p>
<p><a href="/articles/data/c23-538-ai-volumes-2026-11-25.csv" download>CSVでダウンロード（538行）</a></p>
<!--include:c23_table538-->

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
{INPUT}
<li>1回のAPI呼び出しに、538語をまとめて入れました</li>
<li>費用：<strong>${S["cost"]}</strong>（538語で1回）</li>
</ul>
</div>
<p class="note">AIでの質問回数は、DataForSEOが推計した数字です。実際の回数ではありません。0と出た言葉も、「誰も聞いていない」とは言い切れません。</p>
'''
a2=f'''<p>同じ言葉で、Googleの検索数とAIでの質問回数を並べると、どれくらい違うのでしょうか。<a href="/articles/c24-keyword-volume-538/">Googleの検索数（C24）</a>と<a href="/articles/c23-ai-search-volume-538/">AIでの質問回数（C23）</a>を、同じ538語で並べました。同じ日（2026年11月25日）に取っています。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>Googleの検索数に数字があった<strong>{S["gv_pos"]}語</strong>のうち、AIでの質問回数が0だったのは<strong>{S["gpos_zero"]}語</strong>、0より大きかったのは<strong>{S["gpos_nonzero"]}語</strong>でした。</li>
<li>Googleの検索数が<strong>空欄だった{S["gv_empty"]}語</strong>のうち、AIの質問回数が0より大きかったのは<strong>{S["gempty_nonzero"]}語</strong>だけでした。</li>
<li>Googleで月1,000回以上あった<strong>{S["g_gt1000_n"]}語</strong>では、{S["g_gt1000_n"]-S["g_gt1000_zero"]}語でAIの質問回数が0より大きく、{S["g_gt1000_zero"]}語（wappalyzer）だけが0でした。</li>
<li>AIの質問回数がGoogleの検索数より大きかったのは、<strong>「aiモード とは」だけ</strong>（AI 442、Google 170）でした。</li>
<li>両方に数字があった言葉で、AI÷Googleの割合の真ん中の値は<strong>{S["ratio_med"]}%</strong>でした。</li>
</ul>
<p>お店でいうと、「店に来る人」と「電話で問い合わせる人」を数えたら、電話のほうが、ずっと少なかった、という感じです。</p>

<h2>Googleで月1,000回以上あった{S["g_gt1000_n"]}語</h2>
<div class="scroll"><table class="data"><thead><tr><th>キーワード</th><th>Googleの月間検索数（C24）</th><th>AIでの質問回数（C23）</th></tr></thead><tbody>{g1k_rows}</tbody></table></div>

<h2>AIでの質問回数が多かった上位10語</h2>
<div class="scroll"><table class="data"><thead><tr><th>キーワード</th><th>AIでの質問回数</th><th>Googleの月間検索数（C24）</th></tr></thead><tbody>{top_rows}</tbody></table></div>

<h2>全データ：538語を並べた表</h2>
<p>「AI÷Google（%）」は、両方に数字があるとき、AIの質問回数をGoogleの検索数で割った割合です。</p>
<p><a href="/articles/data/c23-vs-google-538-2026-11-25.csv" download>CSVでダウンロード（538行）</a></p>
<!--include:c23_cmp538-->

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
<li>Googleの検索数：<a href="/C24/ja/">検索ボリュームを一括で見る（C24）</a>、AIでの質問回数：C23。どちらも同じ日、同じ538語、日本・日本語</li>
<li>費用：C23が${S["cost"]}、C24が$0.09</li>
</ul>
</div>
<p class="note">どちらも推計の数字です。Googleの検索数は、データがないと空欄で返り、AIでの質問回数は0で返ります。返り方が違うので、「空欄」と「0」は同じ意味とは限りません。</p>
'''
import csv,re
_r=list(csv.DictReader(open(R+'site/articles/data/c23-vs-google-538-2026-11-25.csv',encoding='utf-8-sig')))
_ai=re.compile(r'ai|gemini|perplexity|llmo|geo|claude|chatgpt|gpt',re.I)
AIALL=sum(1 for x in _r if _ai.search(x['キーワード']));AINZ=sum(1 for x in _r if _ai.search(x['キーワード']) and int(x['AI質問回数(C23)'])>0)
YTALL=sum(1 for x in _r if 'youtube' in x['キーワード']);YTNZ=sum(1 for x in _r if 'youtube' in x['キーワード'] and int(x['AI質問回数(C23)'])>0)
a3=f'''<p>AIでの質問回数が<strong>0より大きかった言葉</strong>は、どんな言葉なのでしょうか。538語のうち{nz}語を全部並べて、見てみます。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>538語のうち、0より大きかったのは<strong>{nz}語</strong>、0だったのは<strong>{z}語</strong>でした。</li>
<li>AI関連の言葉（ai、gemini、perplexity、llmo、geo、claude、chatgptのどれかを含む言葉）は、538語のうち<strong>{AIALL}語</strong>。そのうち0より大きかったのは<strong>{AINZ}語</strong>でした。AI関連の言葉でも、0の言葉のほうが多い結果です。</li>
<li>「youtube」を含む言葉は、538語のうち{YTALL}語で、0より大きかったのは<strong>{YTNZ}語</strong>でした。</li>
<li>Googleの検索数に数字があった{S["gv_pos"]}語のうち、AIが0だったのは{S["gpos_zero"]}語でした。0より大きい言葉は、AIの話題だけに限られていませんでした。</li>
</ul>
<p class="note">上の分類は、キーワードに含まれる文字で数えたものです。意味での分類ではありません。表で全部確認できます。</p>

<h2>0より大きかった{nz}語（全部）</h2>
<p>AIでの質問回数の多い順です。Googleの月間検索数も並べています。</p>
<!--include:c23_nonzero-->

<h2>0だった{z}語</h2>
<p>538語の全データ（<a href="/articles/c23-ai-search-volume-538/">こちらの記事</a>）の表で、AIでの質問回数が0の行です。CSVを並べ替えると、見つけられます。</p>
<p><a href="/articles/data/c23-538-ai-volumes-2026-11-25.csv" download>538語のCSV</a></p>

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
{INPUT}
<li>データ：<a href="/articles/c23-ai-search-volume-538/">538語の記事</a>と同じ</li>
</ul>
</div>
<p class="note">538語は、私がSEO関連で選んだ言葉です。ほかの分野の言葉では、違う結果になることがあります。</p>
'''
a4=f'''<p>AIでの質問回数の「12か月の動き」は、Googleの検索数の動きと似ているのでしょうか。AIでの質問回数が多かった上位15語について、<strong>12か月ぶんの数字を、AIとGoogleで並べました</strong>。</p>

<h2>動きの似かた（相関係数）</h2>
<p>12か月の数字を並べて、「動きが同じか」を−1〜1の数字で出したものです。1に近いほど同じ動き、0に近いほど関係がなく、−1に近いほど逆の動きです。</p>
<div class="scroll"><table class="data"><thead><tr><th>キーワード</th><th>相関係数（AI×Google、12か月）</th></tr></thead><tbody>{cor_rows}</tbody></table></div>
<p>15語の値は、<strong>−0.72から0.79</strong>まで、ばらばらでした。同じ動きの言葉も、逆の動きの言葉もあります。</p>
<p class="note">12個の数字だけから出した値です。数字が小さい言葉は、1回の増減で大きく動きます。傾向として使うには、数が足りません。</p>

<h2>全データ：月別の数字（上位15語）</h2>
<p>1語につき2行です。上の行がAIでの質問回数、下の行がGoogleの月間検索数（C24）です。</p>
<p><a href="/articles/data/c23-monthly-top15-2026-11-25.csv" download>CSVでダウンロード</a></p>
<!--include:c23_monthly-->

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
<li>Googleの月別検索数：<a href="/C24/ja/">C24</a>の「直近12か月」の列。AIの月別：C23の月別の列。期間は{S["months"][0]}〜{S["months"][1]}</li>
<li>データ：<a href="/articles/c23-ai-search-volume-538/">538語の記事</a>と同じ</li>
<li>計算：ピアソンの相関係数を、12か月の数字で計算しました</li>
</ul>
</div>
'''
a5=f'''<p>AIでの質問回数のAPIでは、何がわかって、何がわからないのでしょうか。<a href="/C23/ja/">AIでの質問回数を見るツール</a>を実際に使って確かめた事実を整理します。</p>

<h2>わかること（実測）</h2>
<ul>
<li><strong>1語ごとの、AIでの質問回数（月間）。</strong>538語すべてで、数字が返りました（0を含む）。</li>
<li><strong>12か月分の月別の数字。</strong>{S["months"][0]}〜{S["months"][1]}が、全語で返りました。</li>
<li><strong>たくさんの語を、まとめて。</strong>538語を1回のAPI呼び出しで取れました。費用は${S["cost"]}です（1語あたり約$0.0001）。</li>
</ul>

<h2>わからないこと・できないこと（実測）</h2>
<ul>
<li><strong>多くの言葉が0。</strong>538語のうち{z}語（{pct(z,n)}%）が0でした。</li>
<li><strong>どのAIで聞かれたか。</strong>返るのは1つの数字だけで、ChatGPTやGeminiなどの内訳は返りません。</li>
<li><strong>実際の質問回数。</strong>推計の数字です。</li>
<li><strong>アルファベットの大文字小文字。</strong>キーワードは小文字にして返ります（「Google AIモード」→「google aiモード」）。</li>
<li><strong>Googleの検索数と同じ大きさの数字。</strong>同じ538語で、Googleは合計{S["sum_g"]:,}（数字がある{S["gv_pos"]}語）、AIは合計{S["sum_ai"]:,}でした。</li>
</ul>
<p class="note">このサイトのツール画面は、1語ずつ調べる形です。APIは、たくさんの語をまとめて取れることを、この実測で確かめました。</p>

<h2>どう使い分ける？</h2>
<ul>
<li><strong>Googleの検索数が知りたい</strong> → <a href="/C24/ja/">C24</a>（またはGoogleのキーワードプランナー）。</li>
<li><strong>AIでも聞かれているテーマか、確かめたい</strong> → このツールが向いています。数字が小さくても、0かどうかで、AIで聞かれているかの手がかりになります。</li>
</ul>
<p>確認だけなら、まずGoogleの検索数だけでも十分です。AIでも気になるテーマだけ、このツールで確かめてみてください。</p>

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
{INPUT}
<li>データ：<a href="/articles/c23-ai-search-volume-538/">538語の記事</a>と同じ</li>
</ul>
</div>
'''
for slug,body in [('c23-ai-search-volume-538',a1),('c23-ai-vs-google-volume',a2),('c23-ai-volume-nonzero-words',a3),('c23-ai-monthly-trend',a4),('c23-ai-volume-limits',a5)]:
    open(R+f'articles/{slug}.html','w',encoding='utf-8').write(body)
idx=json.load(open(R+'articles/index.json',encoding='utf-8')); idx=[a for a in idx if a['tool']!='C23']
idx+=[
 {"slug":"c23-ai-search-volume-538","tool":"C23","date":"2026-11-25","title":"【実測】538キーワードの、AIでの質問回数を月別に全部載せる：0より大きかったのは84語だけ","description":"Googleの検索数を調べた538語を、AIでの質問回数で調べました。0だったのは454語、一番多かったのは「aiモード とは」の442回でした。"},
 {"slug":"c23-ai-vs-google-volume","tool":"C23","date":"2026-11-25","title":"Googleの検索数とAIでの質問回数を、同じ538語で並べたら","description":"同じ日、同じ538語で、Googleの月間検索数とAIでの質問回数を並べました。AIのほうが大きかったのは1語だけでした。"},
 {"slug":"c23-ai-volume-nonzero-words","tool":"C23","date":"2026-11-25","title":"AIでの質問回数が0より大きかった84語は、どんな言葉？","description":"538語のうち、AIでの質問回数が0より大きかった84語を全部並べました。Googleの検索数との対応も載せています。"},
 {"slug":"c23-ai-monthly-trend","tool":"C23","date":"2026-11-25","title":"AIでの質問回数の12か月の動きは、Googleの検索数と同じ？（上位15語）","description":"AIでの質問回数が多かった15語の月別の数字を、Googleの検索数と並べました。動きの似かたは、語によってばらばらでした。"},
 {"slug":"c23-ai-volume-limits","tool":"C23","date":"2026-11-25","title":"AI検索のボリュームで、わかること・わからないこと（538語の実測）","description":"538語で確かめた、AIでの質問回数のAPIでわかること・わからないことを整理しました。0が多い点や、内訳が返らない点も書いています。"}]
idx.sort(key=lambda a:(a['tool'],a['slug'])); json.dump(idx,open(R+'articles/index.json','w',encoding='utf-8'),ensure_ascii=False,indent=1); print(len(idx))
