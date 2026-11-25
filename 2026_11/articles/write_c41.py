import json,html
R='/home/user/tools/'
S=json.load(open(R+'articles/_inc/c41_stats.json'))
H=html.escape
STABLE=S['STABLE']; SEAS=S['SEAS']; r=S['ratio']
KWS=lambda L:'、'.join(f'「{k}」' for k in L)
BOX='''<li>日付：2026年11月25日、地域と言語：日本、日本語</li>
<li>ツール：<a href="/C41/ja/">過去の月別検索数を見る（C41）</a>（DataForSEOのAPIが、Google広告のデータから月別の検索数を返します）</li>'''
INPUT=f'''<li>キーワード30語（私が選びました）：<strong>季節の20語</strong>＝{KWS(SEAS)}／<strong>一定を期待した10語</strong>＝{KWS(STABLE)}</li>
<li>期間：2021年7月〜2026年10月（64か月）。1回のAPI呼び出しに30語をまとめて入れました</li>
<li>費用：<strong>${S["cost"]}</strong>（30語で1回）</li>'''
top5=''.join(f'<tr><td>{H(k)}</td><td>{v}</td></tr>' for k,v in S['top5'])
low5=''.join(f'<tr><td>{H(k)}</td><td>{v}</td></tr>' for k,v in S['low5'])
j4s=''.join(f'<tr><td>{H(w)}</td><td>{"" if ja is None else f"{ja:,}"}</td><td>{"" if aa is None else f"{aa:,}"}</td><td>{"" if (ja in (None,0) or aa is None) else f"{(aa-ja)/ja*100:+.0f}%"}</td></tr>' for w,ja,aa in S['j4'] if w in STABLE)
pk=S['peak']
peak_sum=''.join(f'<tr><td>{H(w)}</td><td>{pk[w]}月</td></tr>' for w in SEAS)
a1=f'''<p>季節で動くキーワードは、一年のうち、いつ検索されるのでしょうか。<a href="/C41/ja/">過去の月別検索数を見るツール</a>で、<strong>30語の月別の検索数を、2021年7月から2026年10月まで</strong>全部取りました。この記事では、その全データを載せます。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>1回のAPI呼び出しで、30語×最大64か月ぶんの月別検索数が返りました。費用は<strong>${S["cost"]}</strong>です。</li>
<li>一番大きな数字は<strong>「母の日」の7,480,000</strong>、「ふるさと納税」は4,090,000でした。</li>
<li>30語のうち<strong>{len(S["gaps10"])}語</strong>は、記録のない月が10か月以上ありました（{KWS(S["gaps10"])}）。</li>
<li>記録のない月は、<strong>空欄</strong>のまま載せています。</li>
</ul>
<p>家計簿にたとえると、30種類の買い物の「毎月の金額」を、5年ぶん並べた表です。抜けている月は、空欄のままにしてあります。</p>

<h2>全データ：月別の検索数（30語×64か月）</h2>
<p>行が年月、列がキーワードです。数字は、その月の検索数（その月の記録）です。</p>
<p><a href="/articles/data/c41-30keywords-monthly-2026-11-25.csv" download>CSVでダウンロード（64行）</a></p>
<!--include:c41_monthly-->

<h2>この表から作った記事</h2>
<ul>
<li><a href="/articles/c41-peak-months/">一年でいちばん検索される月は？（ピーク月）</a></li>
<li><a href="/articles/c41-seasonal-vs-flat/">動く言葉と一定の言葉の違い</a></li>
<li><a href="/articles/c41-flat-keywords-jan-vs-apr/">「一定のはず」の10語は、1月と4月でどれくらい違う？</a></li>
<li><a href="/articles/c41-monthly-volume-limits/">月別検索数のAPIで、わかること・わからないこと</a></li>
</ul>

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
{INPUT}
</ul>
</div>
<p class="note">検索数は、Google広告のデータにもとづく目安で、実際の回数ではありません。月ごとの数字は、あとから別の値に変わっていることがあります（<a href="/articles/c41-monthly-volume-limits/">こちらの記事</a>）。</p>
'''
a2=f'''<p>「花粉症は3月」「母の日は5月」のように、季節の言葉には、ピークの月があります。30語について、<strong>月ごとの平均の検索数</strong>を出して、いちばん検索される月を数えました。</p>

<h2>先に、わかったこと（季節の20語のピーク月）</h2>
<div class="scroll"><table class="data"><thead><tr><th>キーワード</th><th>ピーク月</th></tr></thead><tbody>{peak_sum}</tbody></table></div>
<p>ピーク月は、2022〜2025年の4年間の、月ごとの平均で決めました。たとえば「母の日」は5月、「熱中症」は7月、「ハロウィン」は10月、「年賀状」は12月でした。</p>
<p class="note">「ハロウィン」「クリスマス ケーキ」は、API側に記録のない月が多く、使えたデータが少ない語です（<a href="/articles/c41-monthly-volume-limits/">こちらの記事</a>）。表の「使った月数」の列で確認できます。</p>

<h2>全データ：ピーク月と最低月（30語）</h2>
<p>「ピーク÷最低」は、月ごとの平均のうち、いちばん高い月を、いちばん低い月で割った数字です。「使った月数」は、2022〜2025年の48か月のうち、記録があった月の数です。</p>
<p><a href="/articles/data/c41-peak-months-2026-11-25.csv" download>CSVでダウンロード</a></p>
<!--include:c41_peaks-->

<h2>全データ：月ごとの平均（1〜12月）</h2>
<p>2022〜2025年の同じ月（たとえば各年の1月）の数字を平均したものです。記録のない年は、平均に入れていません。</p>
<p><a href="/articles/data/c41-calendar-month-averages-2026-11-25.csv" download>CSVでダウンロード</a></p>
<!--include:c41_avg-->

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
{INPUT}
<li>計算：月ごとに、2022〜2025年の平均を出しました。ピーク月は、平均がいちばん高い月です</li>
<li>データ：<a href="/articles/c41-30-keywords-monthly/">30語の月別の記事</a>と同じ</li>
</ul>
</div>
'''
a3=f'''<p>キーワードの中には、季節で大きく動く言葉と、ほとんど動かない言葉があります。30語について、<strong>「いちばん検索される月」÷「いちばん少ない月」</strong>を計算して、動きの大きさを数字にしました。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>季節の20語は、ピーク÷最低が<strong>{S["seas_ratio"][0]}倍から{S["seas_ratio"][1]}倍</strong>まで（真ん中は約{S["seas_ratio"][2]:.1f}倍）でした。</li>
<li>一定を期待した10語は、<strong>{S["stable_ratio"][0]}倍から{S["stable_ratio"][1]}倍</strong>まで（真ん中は約{S["stable_ratio"][2]:.1f}倍）でした。</li>
<li>一定を期待した10語のうち、<strong>「確定申告 やり方」だけは14.3倍</strong>と大きく動いていました。残りの9語は、2.5倍以下でした。</li>
<li>一番大きく動いたのは<strong>「クリスマス ケーキ」の252.3倍</strong>でした。</li>
</ul>
<p>お店でいうと、「年中同じくらいお客さんが来る店」と、「ある月だけ行列ができる店」を、並べて比べた表です。</p>

<h2>動きが大きかった5語</h2>
<div class="scroll"><table class="data"><thead><tr><th>キーワード</th><th>ピーク÷最低</th></tr></thead><tbody>{top5}</tbody></table></div>

<h2>動きが小さかった5語</h2>
<div class="scroll"><table class="data"><thead><tr><th>キーワード</th><th>ピーク÷最低</th></tr></thead><tbody>{low5}</tbody></table></div>

<h2>全データ：30語（動きの小さい順）</h2>
<!--include:c41_ratio-->

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
{INPUT}
<li>計算：月ごと（1〜12月）に、2022〜2025年の平均を出し、いちばん高い平均÷いちばん低い平均を計算しました</li>
<li>データ：<a href="/articles/c41-30-keywords-monthly/">30語の月別の記事</a>と同じ</li>
</ul>
</div>
<p class="note">いちばん低い月の数字が小さい語（記録が少ない語）は、割り算の結果が大きくなりやすいです。「ハロウィン」「クリスマス ケーキ」などは、使えた月が少ないので、参考値です。</p>
'''
_o=[(ja,aa) for w,ja,aa in S['j4'] if w in STABLE and w!='確定申告 やり方' and ja and aa]
DOWN=sum(1 for ja,aa in _o if aa<ja);UP=sum(1 for ja,aa in _o if aa>ja);NEAR=sum(1 for ja,aa in _o if abs(aa-ja)/ja<=0.10)
a4=f'''<p>ブログ、転職、英会話など、「一年中だいたい同じ」と思って選んだ10語があります。本当にそうなのでしょうか。<strong>1月と4月</strong>の検索数を比べました。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>10語のうち、<strong>「確定申告 やり方」</strong>は、1月の平均が186,750、4月の平均が22,520で、<strong>大きく動いていました</strong>。</li>
<li>残りの9語は、1月より4月のほうが少なかったのが<strong>{DOWN}語</strong>、多かったのが<strong>{UP}語</strong>でした。1月と4月の差が10%以内だったのは<strong>{NEAR}語</strong>です。</li>
<li>「一定のはず」と思って選んだ言葉にも、動きの大きい言葉が1つ混ざっていました。</li>
</ul>
<p>「毎日同じ数のお客さんが来るはず」と思って開いたお店でも、よく数えると、1月は混み、4月は空いている、ということがあります。</p>

<h2>一定を期待した10語の、1月と4月</h2>
<p>2022〜2026年の、各年の1月・4月の平均です。記録のない年は、平均に入れていません。</p>
<div class="scroll"><table class="data"><thead><tr><th>キーワード</th><th>1月の平均</th><th>4月の平均</th><th>1月→4月の変化</th></tr></thead><tbody>{j4s}</tbody></table></div>
<p class="note">「ブログ 始め方」などの数字が小さい語は、1回の増減で割合が大きく動きます。</p>

<h2>全データ：30語の、1月と4月</h2>
<p>「1月の年数」「4月の年数」は、平均に使えた年の数です（最大5年）。</p>
<p><a href="/articles/data/c41-jan-vs-apr-2026-11-25.csv" download>CSVでダウンロード</a></p>
<!--include:c41_jan_apr-->

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
{INPUT}
<li>計算：2022年〜2026年の、1月と4月を、それぞれ平均しました（記録がある年だけ）</li>
<li>データ：<a href="/articles/c41-30-keywords-monthly/">30語の月別の記事</a>と同じ</li>
</ul>
</div>
'''
a5=f'''<p>月別の検索数のAPIでは、何がわかって、何がわからないのでしょうか。<a href="/C41/ja/">過去の月別検索数を見るツール</a>を、実際に30語で使って確かめた事実を整理します。</p>

<h2>わかること（実測）</h2>
<ul>
<li><strong>5年ぶんの月別の検索数。</strong>2021年7月〜2026年10月（最大64か月）が返りました。</li>
<li><strong>たくさんの語を、まとめて。</strong>30語を1回で取れました。費用は${S["cost"]}です。</li>
</ul>

<h2>わからないこと・気をつけること（実測）</h2>
<ul>
<li><strong>記録のない月がある。</strong>30語で、最大64か月のところ、記録のない月は合計<strong>{S["gaps_total"]}か月</strong>ありました。いちばん多いのは「{H(S["gaps_max"][0])}」の{S["gaps_max"][1]}か月で、記録があったのは13か月だけでした。</li>
<li><strong>同じ月の数字が、記録によって違う。</strong>ある月の数字が、あとの月の記録の12か月欄では別の値になっていることがありました。30語のうち、そのような月が合計<strong>{S["rev_total"]}か月</strong>ありました（最多は「{H(S["rev_max"][0])}」の{S["rev_max"][1]}か月）。</li>
<li><strong>0の月がある。</strong>{"、".join(f"「{H(w)}」{z}か月" for w,z in S["zeros"].items())}で、検索数が0と返った月がありました。</li>
<li><strong>実際の回数ではない。</strong>Google広告のデータにもとづく目安です。</li>
<li><strong>1語につき、1つの数字。</strong>どの地域・どの端末かの内訳は、このツールでは返りません。</li>
</ul>
<p>ノートにたとえると、「何ページか破れていて、書き直された数字もある、5年ぶんのノート」です。まるごと信じるのではなく、「この日のAPIの返事」として読んでください。</p>

<h2>どう使い分ける？</h2>
<ul>
<li><strong>季節のピークだけ知りたい</strong> → Googleトレンド（無料）で足ります。相対的な動きがわかります。</li>
<li><strong>数字（目安の検索数）を、月ごとに表やCSVで残したい</strong> → このツールが向いています。</li>
</ul>
<p>確認だけなら、まずGoogleトレンドでも十分です。数字をそろえて残したくなったら、このツールを使ってみてください。</p>

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
{INPUT}
<li>データ：<a href="/articles/c41-30-keywords-monthly/">30語の月別の記事</a>と同じ</li>
</ul>
</div>
'''
for slug,body in [('c41-30-keywords-monthly',a1),('c41-peak-months',a2),('c41-seasonal-vs-flat',a3),('c41-flat-keywords-jan-vs-apr',a4),('c41-monthly-volume-limits',a5)]:
    open(R+f'articles/{slug}.html','w',encoding='utf-8').write(body)
idx=json.load(open(R+'articles/index.json',encoding='utf-8')); idx=[a for a in idx if a['tool']!='C41']
idx+=[
 {"slug":"c41-30-keywords-monthly","tool":"C41","date":"2026-11-25","title":"【実測】季節の20語と一定の10語の、月別検索数を5年分（2021年7月〜）全部載せる","description":"30語の月別検索数を、2021年7月から2026年10月まで全部載せます。記録のない月は空欄のままです。"},
 {"slug":"c41-peak-months","tool":"C41","date":"2026-11-25","title":"一年でいちばん検索される月は？30語のピーク月と、月ごとの平均","description":"30語のピーク月と最低月を、2022〜2025年の平均で出しました。母の日は5月、熱中症は7月など。月ごとの平均も全部載せています。"},
 {"slug":"c41-seasonal-vs-flat","tool":"C41","date":"2026-11-25","title":"動く言葉と一定の言葉の違い：ピーク÷最低を30語で計算した","description":"30語について、いちばん検索される月÷いちばん少ない月を計算しました。一定のつもりで選んだ「確定申告 やり方」は14.3倍動いていました。"},
 {"slug":"c41-flat-keywords-jan-vs-apr","tool":"C41","date":"2026-11-25","title":"「一定のはず」の10語は、1月と4月でどれくらい違う？","description":"ブログ・転職・英会話など、一年中同じと思った10語の、1月と4月の平均を並べました。"},
 {"slug":"c41-monthly-volume-limits","tool":"C41","date":"2026-11-25","title":"月別検索数のAPIで、わかること・わからないこと（記録のない月、変わる数字）","description":"30語で確かめた、月別検索数のAPIの限界です。記録のない月が239か月ぶん、数字が変わった月が181か月ぶんありました。"}]
idx.sort(key=lambda a:(a['tool'],a['slug'])); json.dump(idx,open(R+'articles/index.json','w',encoding='utf-8'),ensure_ascii=False,indent=1); print(len(idx))
