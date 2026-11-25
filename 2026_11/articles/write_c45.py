import json,html
R='/home/user/tools/'
S=json.load(open(R+'articles/_inc/c45_stats.json')); H=html.escape
meta=S['meta']; r1=S['r1c']
BOX='''<li>日付：2026年11月25日、地域と言語：日本、日本語</li>
<li>ツール：<a href="/C45/ja/">サイトが上位にいるキーワードを見る（C45）</a>（DataForSEOのAPIが、サイトごとに「10位以内のキーワード」を返します）</li>'''
SITES10=[s for s in S['sites'] if meta[s]['n']>0]
INPUT=f'''<li>調べたサイト：{"、".join(SITES10)}（10サイト。私が選びました）。ほかに hatenablog.com も調べましたが、0件でした</li>
<li>条件（ツールと同じ）：通常の検索結果で10位以内、検索数の多い順に、サイトごとに100件</li>
<li>費用：サイト1つにつき<strong>$0.024</strong>。11サイトで<strong>${S["cost"]}</strong>（0件だった hatenablog.com は$0.012）</li>'''
ovrows=''.join(f'<tr><td>{H(k)}</td><td>{" ／ ".join(v)}</td></tr>' for k,v in S['ov_top'])
r1rows=''.join(f'<tr><td>{H(s)}</td><td>{n}</td></tr>' for s,n in sorted(r1.items(),key=lambda t:-t[1]))
ft=''.join(f'<tr><td>{H(s)}</td><td>{H(k)}</td><td>{v:,}</td></tr>' for s,k,v in S['first_top'])
big=''.join(f'<tr><td>{H(s)}</td><td>{"（0件）" if t is None else f"{t:,}"}</td></tr>' for s,t in S['big'])
bands=''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>' for a,b,c,d,e in S['bands'])
a1=f'''<p>競合のサイトが、Googleの検索で10位以内にいるキーワードを知りたい。そんなときに使えるのが<a href="/C45/ja/">サイトが上位にいるキーワードを見るツール</a>です。日本の情報サイト<strong>10個</strong>について、10位以内にいるキーワードを、検索数の多い順に<strong>100件ずつ</strong>取りました。全部で{S["total_rows"]:,}件のデータです。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>10位以内にいるキーワードの数（全部）は、サイトで大きく違いました。<strong>note.comが1,937,304個</strong>、canva.comが73,557個、xserver.ne.jpが3,241個、ja.wordpress.orgが354個です。</li>
<li>取れたのは、検索数の多い順の<strong>100件ずつ</strong>です。1回のAPI呼び出しで取れる件数は、このツールの設定で100件でした。</li>
<li>一番検索数が多かったのは、note.comの<strong>「転機」（月間55,600,000）</strong>でした。</li>
<li>hatenablog.com を調べたら、<strong>0件</strong>でした。</li>
</ul>
<p>お店でいうと、「10店のレジの、売上の大きい商品ベスト100」を、全部書き出した表です。</p>

<h2>サイトごとのまとめ</h2>
<p>「10位以内のキーワード数（全部）」はAPIが返した合計、「取得した件数」はこの記事で取った100件です。</p>
<p><a href="/articles/data/c45-site-summary-2026-11-25.csv" download>CSVでダウンロード</a></p>
<!--include:c45_summary-->

<h2>全データ：10サイト×100件（{S["total_rows"]:,}件）</h2>
<p>サイト、キーワード、順位、Googleの月間検索数、URLを、APIが返したまま載せています。</p>
<p><a href="/articles/data/c45-10sites-top100-2026-11-25.csv" download>CSVでダウンロード（1,000行）</a></p>
<details><summary>1,000件の表を開く</summary>
<!--include:c45_table-->
</details>

<h2>この表から作った記事</h2>
<ul>
<li><a href="/articles/c45-shared-keywords/">10サイトで、同じキーワードで上位に入っていたもの</a></li>
<li><a href="/articles/c45-rank1-keywords/">1位のキーワードだけを集めたら</a></li>
<li><a href="/articles/c45-volume-vs-rank/">検索数と順位を並べて見る</a></li>
<li><a href="/articles/c45-competitor-keywords-limits/">競合サイトのキーワードを調べる方法と、わからないこと</a></li>
</ul>

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
{INPUT}
</ul>
</div>
<p class="note">検索数や順位は、DataForSEOがGoogleの検索結果から推計した、この日のデータです。実際の数字とは違うことがあります。サイトの良し悪しの評価ではありません。</p>
'''
a2=f'''<p>10個のサイトは、同じキーワードで上位に入っているのでしょうか。<a href="/articles/c45-10-sites-top100/">10サイト×100件</a>のデータで、<strong>2つ以上のサイトに出てきたキーワード</strong>を探しました。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>1,000件のキーワードのうち、<strong>2つ以上のサイトに出たものは{S["ov_n"]}個</strong>でした。</li>
<li>いちばん多くのサイトに共通していたのは<strong>{S["ov_max"]}サイト</strong>でした。</li>
<li>3サイトに共通していたのは、<strong>「vps」「ホームページの作成」「楽天 アフィリエイト」</strong>などでした（conoha.jp、onamae.com、xserver.ne.jpの3つが重なるものが多い）。</li>
<li>「楽天 アフィリエイト」は、「楽天アフィリエイト」「楽天のアフィリエイト」のように、<strong>書き方の違いが別のキーワードとして</strong>並んでいます。</li>
</ul>
<p>同じ商店街の店が、同じお客さんを取り合っているのに、「看板の書き方が少しずつ違う」ような様子です。</p>

<h2>共通したキーワード（出たサイト数の多い順・上位12個）</h2>
<div class="scroll"><table class="data"><thead><tr><th>キーワード</th><th>出たサイト</th></tr></thead><tbody>{ovrows}</tbody></table></div>

<h2>全データ：2つ以上のサイトに出たキーワード（{S["ov_n"]}個）</h2>
<p><a href="/articles/data/c45-overlap-2026-11-25.csv" download>CSVでダウンロード</a></p>
<!--include:c45_overlap-->

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
{INPUT}
<li>数え方：キーワードの文字が完全に同じものを、同じキーワードとして数えました</li>
<li>データ：<a href="/articles/c45-10-sites-top100/">10サイト×100件の記事</a>と同じ</li>
</ul>
</div>
<p class="note">各サイトの「検索数の多い順に100件」だけを見ています。100件の外には、重なるキーワードがもっとあるかもしれません。</p>
'''
import csv as _c
_r=list(_c.DictReader(open(R+'site/articles/data/c45-rank1-2026-11-25.csv',encoding='utf-8-sig')))
_cv=[x for x in _r if x['サイト']=='canva.com']
CANVA=len(_cv);ILL=sum('イラスト' in x['キーワード'] for x in _cv)
a3=f'''<p>10位以内のキーワードのうち、<strong>1位</strong>を取っているキーワードだけを集めると、どんな言葉が並ぶのでしょうか。<a href="/articles/c45-10-sites-top100/">10サイト×100件</a>の中から、順位が1位のものを全部取り出しました。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>1,000件のうち、順位が<strong>1位だったのは{S["r1_n"]}件</strong>（{S["r1_n"]/10:.1f}%）でした。</li>
<li>1位の数が多かったのは、<strong>ja.wordpress.org（{r1["ja.wordpress.org"]}件）</strong>と<strong>canva.com（{r1["canva.com"]}件）</strong>でした。</li>
<li>検索数が一番大きい1位は、canva.comの<strong>「canva」（月間1,830,000）</strong>でした。</li>
<li>1位の言葉には、サービス名（「canva」「キャンバ」「wordpress」など）と、その<strong>つづりの違い</strong>（「wo rdpress」「word press」など）が並びました。canva.comの1位{CANVA}件のうち、<strong>{ILL}件は「イラスト」を含む言葉</strong>（「イラスト 馬」など）でした。</li>
</ul>
<p>お店の名前で探す人は、その店に行きたい人です。サービス名が1位に並ぶのは、そういう言葉だからです。</p>

<h2>サイトごとの、1位の数</h2>
<div class="scroll"><table class="data"><thead><tr><th>サイト</th><th>1位のキーワード数（100件のうち）</th></tr></thead><tbody>{r1rows}</tbody></table></div>

<h2>検索数が多かった1位（上位10件）</h2>
<div class="scroll"><table class="data"><thead><tr><th>サイト</th><th>キーワード</th><th>月間検索数</th></tr></thead><tbody>{ft}</tbody></table></div>

<h2>全データ：1位のキーワード（{S["r1_n"]}件）</h2>
<p>検索数の多い順です。</p>
<p><a href="/articles/data/c45-rank1-2026-11-25.csv" download>CSVでダウンロード</a></p>
<!--include:c45_rank1-->

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
{INPUT}
<li>データ：<a href="/articles/c45-10-sites-top100/">10サイト×100件の記事</a>のうち、順位が1位のもの</li>
</ul>
</div>
<p class="note">各サイトの検索数の多い順100件の中の1位です。「サービス名」「イラスト」の分類は、キーワードの文字を見て数えたもので、意味での分類ではありません。</p>
'''
a4=f'''<p>検索数が多いキーワードは、順位も高いのでしょうか。<a href="/articles/c45-10-sites-top100/">10サイト×100件</a>のデータで、検索数の帯ごとに、順位を並べました。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>順位ごとの件数は、1位が{S["allr"]["1"]}件、2位が{S["allr"]["2"]}件、…、10位が{S["allr"]["10"]}件で、<strong>1位から10位まで、ほぼ同じくらいずつ</strong>に分かれました（最少は2位の{S["allr"]["2"]}件、最多は4位の{S["allr"]["4"]}件）。</li>
<li>検索数の帯で比べると、<strong>順位の中央値は5〜6</strong>で、大きくは変わりませんでした。</li>
<li>1位の割合は、10万以上の帯が<strong>14%</strong>、1万〜9.9万の帯が<strong>8%</strong>、1,000〜9,999の帯が<strong>15%</strong>でした。</li>
</ul>
<p>テストでいうと、「難しい問題（検索数が多い言葉）でも、簡単な問題でも、1位を取れる割合はそれほど変わらなかった」という結果です。</p>

<h2>検索数の帯ごとの順位</h2>
<div class="scroll"><table class="data"><thead><tr><th>月間検索数の帯</th><th>キーワードの数</th><th>順位の中央値</th><th>1位の数</th><th>1位の割合</th></tr></thead><tbody>{bands}</tbody></table></div>
<p class="note">取れた1,000件は、各サイトの「検索数の多い順の100件」なので、検索数が1,000未満のキーワードは含まれません。</p>

<h2>全データ：サイトごとの順位の分布</h2>
<p>100件が、1位〜10位にそれぞれ何件ずつあるかです。</p>
<p><a href="/articles/data/c45-rank-distribution-2026-11-25.csv" download>CSVでダウンロード</a></p>
<!--include:c45_rankdist-->

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
{INPUT}
<li>データ：<a href="/articles/c45-10-sites-top100/">10サイト×100件の記事</a>と同じ。1,000件の検索数と順位を使いました</li>
</ul>
</div>
'''
a5=f'''<p>競合サイトのキーワードを調べるには、いくつか方法があります。<a href="/C45/ja/">サイトが上位にいるキーワードを見るツール</a>を、実際に11サイトで使って確かめた事実を整理します。</p>

<h2>方法の違い</h2>
<div class="scroll"><table>
<thead><tr><th>見たいこと</th><th>Search Console（Google公式）</th><th>ブラウザで検索</th><th>このツール（C45）</th></tr></thead>
<tbody>
<tr><td>自分のサイトのキーワード</td><td>見られる（登録したサイトのみ）</td><td>1語ずつ手で探す</td><td>見られる（10位以内のもの）</td></tr>
<tr><td>他人のサイトのキーワード</td><td>見られない</td><td>思いついた語を1語ずつ確認</td><td>見られる（検索数の多い順に100件）</td></tr>
<tr><td>まとめて見る</td><td>自分のサイトの検索語の一覧</td><td>できない</td><td>サイトごとに100件をまとめて</td></tr>
<tr><td>費用</td><td>無料</td><td>無料</td><td>1サイト$0.024（約3.7円）を実測</td></tr>
</tbody></table></div>
<p class="note">Search Consoleとブラウザの項目は、一般的な説明です。細かい仕様は変わることがあるので、公式で確認してください。</p>

<h2>このツールで、わかること（実測）</h2>
<ul>
<li>サイトが10位以内にいるキーワードの<strong>合計数</strong>（例：xserver.ne.jpは3,241個）。</li>
<li>検索数の多い順の<strong>上位100件</strong>の、キーワード・順位・検索数・URL。</li>
<li>10サイトを、10回の呼び出しで調べられました（hatenablog.comの0件を含めると11回で${S["cost"]}）。</li>
</ul>

<h2>わからないこと・気をつけること（実測）</h2>
<ul>
<li><strong>100件より先は見えない。</strong>note.comは10位以内が1,937,304個ありますが、取れたのは100件です。</li>
<li><strong>サイトによって、0件になる。</strong>hatenablog.comを調べたら0件でした（費用は$0.012）。理由は確かめていません。</li>
<li><strong>「10位以内」だけ。</strong>11位以下のキーワードは、この設定では取れません。</li>
<li><strong>つづりの違いが別のキーワードになる。</strong>「wordpress」「word press」「wo rdpress」が別々に並びました。</li>
<li><strong>推計の数字。</strong>順位も検索数も、この日のデータです。</li>
<li><strong>サイトの良し悪しは分からない。</strong>データを見せるだけです。</li>
</ul>

<h2>どう使い分ける？</h2>
<ul>
<li><strong>自分のサイトの検索語</strong> → Search Consoleが向いています。無料で、実際のデータです。</li>
<li><strong>競合のサイトが、どんな言葉で上位にいるか、表で見たい</strong> → このツールが向いています。</li>
</ul>
<p>確認だけなら、まずブラウザで1語検索するだけでも十分です。競合を何サイトも並べたくなったら、このツールを使ってみてください。</p>

<h2>全データ：サイトごとのまとめ</h2>
<p>10位以内のキーワード数（全部）です。</p>
<div class="scroll"><table class="data"><thead><tr><th>サイト</th><th>10位以内のキーワード数（全部）</th></tr></thead><tbody>{big}</tbody></table></div>

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
{INPUT}
<li>データ：<a href="/articles/c45-10-sites-top100/">10サイト×100件の記事</a>と同じ</li>
</ul>
</div>
'''
for slug,body in [('c45-10-sites-top100',a1),('c45-shared-keywords',a2),('c45-rank1-keywords',a3),('c45-volume-vs-rank',a4),('c45-competitor-keywords-limits',a5)]:
    open(R+f'articles/{slug}.html','w',encoding='utf-8').write(body)
idx=json.load(open(R+'articles/index.json',encoding='utf-8')); idx=[a for a in idx if a['tool']!='C45']
idx+=[
 {"slug":"c45-10-sites-top100","tool":"C45","date":"2026-11-25","title":"【実測】日本の情報サイト10個が、10位以内にいるキーワードを、検索数の多い順に100件ずつ（全1,000件）","description":"10サイトのキーワードを100件ずつ、順位・検索数・URLつきで全部載せます。10位以内のキーワード数は、note.comが1,937,304個、ja.wordpress.orgが354個でした。"},
 {"slug":"c45-shared-keywords","tool":"C45","date":"2026-11-25","title":"10サイトで、同じキーワードで上位に入っていたものは？（44個）","description":"10サイト×100件の中で、2つ以上のサイトに出たキーワードは44個でした。3サイトに共通した言葉を全部並べています。"},
 {"slug":"c45-rank1-keywords","tool":"C45","date":"2026-11-25","title":"1位のキーワードだけを集めたら、どんな言葉が並ぶ？（114件）","description":"10サイト×100件のうち、順位が1位の114件を全部並べました。サービス名とそのつづりの違いが多く並びました。"},
 {"slug":"c45-volume-vs-rank","tool":"C45","date":"2026-11-25","title":"検索数と順位を並べて見る：1位の割合は、検索数の帯でどう違う？","description":"1,000件を、検索数の帯ごとに並べて、順位の中央値と1位の割合を出しました。大きな差はありませんでした。"},
 {"slug":"c45-competitor-keywords-limits","tool":"C45","date":"2026-11-25","title":"競合サイトのキーワードを調べる方法の違いと、このツールでわからないこと","description":"Search Console・ブラウザ・このツールの違いと、11サイトで確かめた限界です。hatenablog.comは0件でした。"}]
idx.sort(key=lambda a:(a['tool'],a['slug'])); json.dump(idx,open(R+'articles/index.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
c=json.load(open(R+'articles/costs.json',encoding='utf-8'))
for sl in ['c45-10-sites-top100','c45-shared-keywords','c45-rank1-keywords','c45-volume-vs-rank','c45-competitor-keywords-limits']:
    c['per'][sl]={'usd':0.252 if sl=='c45-10-sites-top100' else 0.252,'note':'11サイト×1回（1サイト$0.024、0件だった1サイトは$0.012）' if sl=='c45-10-sites-top100' else '10サイト×100件のデータ（11回）を使用'}
c['real']['C45']=0.252
json.dump(c,open(R+'articles/costs.json','w',encoding='utf-8'),ensure_ascii=False,indent=1); print(len(idx))
