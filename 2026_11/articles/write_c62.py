import json,html,csv
R='/home/user/tools/'
S=json.load(open(R+'articles/_inc/c62_stats.json')); H=html.escape
d=S['dist']; CN={'performance':'パフォーマンス','accessibility':'アクセシビリティ','best-practices':'ベストプラクティス','seo':'SEO'}
BOX='''<li>日付：2026年11月25日</li>
<li>ツール：<a href="/C62/ja/">表示速度の点数を見る（C62）</a>（DataForSEOのAPIが、Lighthouseの点数を返します）</li>
<li>測定の設定：スマホ（モバイル）、パフォーマンス・アクセシビリティ・ベストプラクティス・SEOの4つの点数</li>'''
n=S['nA']
INPUT_A=f'''<li>サイト：日本の人気サイトなど30個のトップページ（私が選びました。<a href="/articles/c74-sites-technologies/">技術を調べた記事</a>と同じ顔ぶれ）</li>
<li>結果：<strong>測れたのは{n}サイト</strong>。3サイトはエラーでした</li>'''
COST=f'<li>費用：1回につき<strong>$0.005</strong>（約0.8円）。この記事のデータ全部（59回）で<strong>${S["cost"]}</strong>（エラーの回は無料）</li>'
best=''.join(f'<tr><td>{H(a)}</td><td>{b}</td></tr>' for a,b in S['best']); worst=''.join(f'<tr><td>{H(a)}</td><td>{b}</td></tr>' for a,b in S['worst'])
a1=f'''<p>サイトを開くのが速いか遅いか。それを点数にしてくれるのが「Lighthouse」です。<a href="/C62/ja/">表示速度の点数を見るツール</a>で、日本の人気サイトなど<strong>30個</strong>のトップページを、スマホの設定で測りました。測れたのは<strong>{n}サイト</strong>です。その全データを載せます。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>30サイトのうち、<strong>測れたのは{n}サイト</strong>。ほかの3サイト（yahoo.co.jp、zozo.jp、muji.com）は、Lighthouseのエラーでした。</li>
<li>パフォーマンスの点数は、<strong>{d["performance"]["min"]}〜{d["performance"]["max"]}</strong>（中央値{d["performance"]["med"]:.0f}）でした。<strong>90点以上のサイトはなく、50点未満が{S["perf_lt50"]}サイト</strong>でした。</li>
<li>一番高かったのは<strong>cookpad.com（78）</strong>、一番低かったのは<strong>toyota.jp（7）</strong>でした。</li>
<li>アクセシビリティは{d["accessibility"]["min"]}〜{d["accessibility"]["max"]}、ベストプラクティスは{d["best-practices"]["min"]}〜{d["best-practices"]["max"]}、SEOは{d["seo"]["min"]}〜{d["seo"]["max"]}でした。</li>
</ul>
<p>通知表にたとえると、「パフォーマンス」は体育の点数です。27人のクラスで、90点を取った子はいませんでした。</p>
<p class="note">測るたびに点数は少し変わります（<a href="/articles/c62-repeat-3-times/">3回測った記事</a>）。ここは、「この日の1回の結果」です。また、<strong>cookpad.comは、測るとドイツ語のページ（/de）に移って測られました</strong>（<a href="/articles/c62-lighthouse-limits/">こちらの記事</a>）。cookpad.comの点数は、その移った先のページのものです。</p>

<h2>パフォーマンスの高かった5サイト</h2>
<div class="scroll"><table class="data"><thead><tr><th>サイト</th><th>パフォーマンス</th></tr></thead><tbody>{best}</tbody></table></div>

<h2>パフォーマンスの低かった5サイト</h2>
<div class="scroll"><table class="data"><thead><tr><th>サイト</th><th>パフォーマンス</th></tr></thead><tbody>{worst}</tbody></table></div>

<h2>全データ：{n}サイトの点数と数値</h2>
<p>4つの点数（100点満点）と、5つの数値（FCP＝最初の文字や画像が出るまで、LCP＝一番大きい部分が出るまで、TBT＝操作できない時間、CLS＝レイアウトのずれ、Speed Index）です。「最終的に開いたURL」は、測ったときにたどり着いたページです。</p>
<p><a href="/articles/data/c62-30sites-mobile-2026-11-25.csv" download>CSVでダウンロード</a></p>
<!--include:c62_sites-->

<h2>エラーになった3サイト</h2>
<!--include:c62_errors-->

<h2>この表から作った記事</h2>
<ul>
<li><a href="/articles/c62-score-spread/">4つの点数のうち、いちばんばらつくのはどれ？</a></li>
<li><a href="/articles/c62-repeat-3-times/">同じURLを3回測ったら、点数は毎回同じ？</a></li>
<li><a href="/articles/c62-top-vs-article/">トップページと記事ページで、点数はどれくらい違う？</a></li>
<li><a href="/articles/c62-lighthouse-limits/">表示速度を測る方法と、このツールでわからないこと</a></li>
</ul>

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
{INPUT_A}
{COST}
</ul>
</div>
<p class="note">Lighthouseの点数は、測る場所や回線で変わります。実際のお客さんの体感の速さとは違います。サイトの良し悪しの評価ではありません。</p>
'''
a2=f'''<p>Lighthouseには、4つの点数があります。<a href="/articles/c62-30-sites-lighthouse/">測れた{n}サイト</a>で、どの点数がサイトによって一番ばらついたのかを比べました。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>「最高点−最低点」が一番大きかったのは<strong>パフォーマンス（{d["performance"]["rng"]}点：{d["performance"]["min"]}〜{d["performance"]["max"]}）</strong>でした。</li>
<li>次に大きかったのは、SEOが{d["seo"]["rng"]}点（{d["seo"]["min"]}〜{d["seo"]["max"]}）、ベストプラクティスが{d["best-practices"]["rng"]}点（{d["best-practices"]["min"]}〜{d["best-practices"]["max"]}）、アクセシビリティが{d["accessibility"]["rng"]}点（{d["accessibility"]["min"]}〜{d["accessibility"]["max"]}）でした。</li>
<li>標準偏差（ばらつきの目安）も、パフォーマンスが{d["performance"]["sd"]}で最大でした。</li>
<li>SEOの最低は{S["minseo"][0][0]}の{S["minseo"][0][1]}点、次が{S["minseo"][1][0]}の{S["minseo"][1][1]}点でした。</li>
</ul>
<p>4教科のテストで、「体育だけは、クラスの中で点数の差が大きかった」ということです。</p>

<h2>4つの点数の分布（{n}サイト）</h2>
<!--include:c62_dist-->

<h2>全データ：パフォーマンスの順位</h2>
<p>パフォーマンスの高い順です。</p>
<!--include:c62_perf_rank-->

<h2>全データ：{n}サイトの点数</h2>
<p><a href="/articles/data/c62-30sites-mobile-2026-11-25.csv" download>CSVでダウンロード</a></p>
<!--include:c62_sites-->

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
{INPUT_A}
{COST}
<li>データ：<a href="/articles/c62-30-sites-lighthouse/">{n}サイトの記事</a>と同じ</li>
</ul>
</div>
<p class="note">点数は、測るたびに少し変わります。「ばらつき」の順位は、この日の1回ずつの結果です。</p>
'''
b=S['bst']
brow=''.join(f'<tr><td>{H(u)}</td><td>{x["performance"][0]}〜{x["performance"][1]}</td><td>{x["accessibility"][0]}〜{x["accessibility"][1]}</td><td>{x["best-practices"][0]}〜{x["best-practices"][1]}</td><td>{x["seo"][0]}〜{x["seo"][1]}</td><td>{H("、".join(x["lcp"]))}</td></tr>' for u,x in {'https://www.xserver.ne.jp/':b['xserver'],'https://www.itmedia.co.jp/':b['itmedia'],'https://note.com/':b['note']}.items())
rc=list(csv.DictReader(open(R+'site/articles/data/c62-30sites-mobile-2026-11-25.csv',encoding='utf-8-sig')))
rc2=list(csv.DictReader(open(R+'site/articles/data/c62-top-vs-article-2026-11-25.csv',encoding='utf-8-sig')))
def a_row(dom): return next(x for x in rc if x['サイト']==dom)
def c_row(dom): return next(x for x in rc2 if x['サイト']==dom and x['トップ／記事']=='トップ')
same=''.join(f'<tr><td>{H(dm)}</td><td>{a_row(dm)["パフォーマンス"]}</td><td>{H(a_row(dm)["LCP"])}</td><td>{c_row(dm)["パフォーマンス"]}</td><td>{H(c_row(dm)["LCP"])}</td></tr>' for dm in ['xserver.ne.jp','conoha.jp','onamae.com'])
a3=f'''<p>Lighthouseの点数は、同じURLを測ったら、毎回同じになるのでしょうか。3つのURLを、それぞれ<strong>3回</strong>ずつ測りました。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>3つのURLの、4つの点数は、<strong>3回でほぼ同じ</strong>でした。パフォーマンスの差は、最大で3点（itmedia：31〜34）でした。アクセシビリティ、ベストプラクティス、SEOは、3回とも同じ点数でした。</li>
<li>一方で、<strong>LCP（一番大きい部分が出るまでの時間）は大きく変わりました</strong>。itmedia.co.jpは、10.8秒、19.2秒、20.8秒でした。</li>
<li>別の測定（URLの書き方が違う呼び出し）でも、同じサイトの点数は少しずつ違いました（下の表）。</li>
</ul>
<p>同じ人が、同じ道を3回走っても、タイムは毎回ちがう。でも「順位」は大きく変わらなかった、という感じです。</p>

<h2>3回の結果</h2>
<div class="scroll"><table class="data"><thead><tr><th>URL</th><th>パフォーマンス</th><th>アクセシビリティ</th><th>ベストプラクティス</th><th>SEO</th><th>LCPの3回</th></tr></thead><tbody>{brow}</tbody></table></div>

<h2>全データ：9回ぶん（3URL×3回）</h2>
<p><a href="/articles/data/c62-repeat3-2026-11-25.csv" download>CSVでダウンロード</a></p>
<!--include:c62_repeat-->

<h2>参考：同じサイトを、別の回で測った結果</h2>
<p>「30サイトの記事」の測定（https://ドメイン/）と、「トップと記事の記事」の測定（https://www.ドメイン/）で、同じサイトのトップページを測った結果です。URLの書き方（wwwの有無）が違います。</p>
<div class="scroll"><table class="data"><thead><tr><th>サイト</th><th>30サイト記事：パフォーマンス</th><th>LCP</th><th>トップ記事：パフォーマンス</th><th>LCP</th></tr></thead><tbody>{same}</tbody></table></div>

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
<li>URL：https://www.xserver.ne.jp/、https://www.itmedia.co.jp/、https://note.com/ を、それぞれ3回ずつ（続けて）</li>
{COST}
</ul>
</div>
<p class="note">3つのURLだけの結果です。ほかのサイトや時間帯では、ばらつき方が違うことがあります。</p>
'''
P=S['pst']; dd=P['diff']
a4=f'''<p>サイトのトップページと、中の記事ページでは、点数は同じくらいなのでしょうか。同じサイトの<strong>トップページと記事ページ</strong>を、10組測りました。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>パフォーマンスの点数は、10組のうち<strong>記事ページのほうが高かったのが{P["art_higher"]}組、低かったのが{P["art_lower"]}組</strong>でした。</li>
<li>トップページの中央値は<strong>{P["med_top"]:.0f}</strong>、記事ページの中央値は<strong>{P["med_art"]:.1f}</strong>でした。</li>
<li>差が一番大きかったのは、<strong>onamae.com（記事が40点低い）</strong>と<strong>canva.com（記事が37点低い）</strong>。記事のほうが20点高かったのは、shopify.comでした。</li>
</ul>
<p>お店でいうと、「店先の売り場」と「奥の売り場」で、同じ点が取れるかを比べた表です。点が高い組と低い組が、バラバラでした。</p>

<h2>10組の点数の差（記事−トップ、パフォーマンス）</h2>
<div class="scroll"><table class="data"><thead><tr><th>サイト</th><th>記事−トップ（点）</th></tr></thead><tbody>{"".join(f"<tr><td>{H(a)}</td><td>{x:+d}</td></tr>" for a,x in dd)}</tbody></table></div>

<h2>全データ：10組（トップと記事）</h2>
<p><a href="/articles/data/c62-top-vs-article-2026-11-25.csv" download>CSVでダウンロード</a></p>
<!--include:c62_pairs-->

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
<li>URL：10サイトの、トップページと記事ページ（<a href="/articles/c01-blog-top100/">「ブログ 始め方」の上位100件</a>に出てきたページ）。1ページ1回ずつ、合計20回</li>
{COST}
</ul>
</div>
<p class="note">1回ずつの結果です。点数は測るたびに少し変わります（<a href="/articles/c62-repeat-3-times/">3回測った記事</a>）。10組だけの結果で、傾向とは言えません。</p>
'''
red=''.join(f'<tr><td>{H(a)}</td><td>{H(u)}</td></tr>' for a,u in S['redirects'])
a5=f'''<p>Lighthouseの点数のAPIでは、何がわかって、何がわからないのでしょうか。<a href="/C62/ja/">表示速度の点数を見るツール</a>で59回測って、確かめた事実を整理します。</p>

<h2>わかること（実測）</h2>
<ul>
<li><strong>4つの点数と、5つの数値。</strong>パフォーマンス・アクセシビリティ・ベストプラクティス・SEOの点数と、FCP・LCP・TBT・CLS・Speed Indexです。</li>
<li><strong>低い費用。</strong>1回$0.005（約0.8円）。</li>
<li><strong>1回にかかる時間。</strong>{S["ok_calls"]}回の平均は約{S["avg_time"]}秒（最短{S["min_time"]}秒、最長{S["max_time"]}秒）でした。</li>
</ul>

<h2>わからないこと・気をつけること（実測）</h2>
<ul>
<li><strong>エラーになるサイトがある。</strong>30サイトのうち3サイト（yahoo.co.jp、zozo.jp、muji.com）は、Lighthouseのエラー（ERRORED_DOCUMENT_REQUEST、NO_FCP）でした。エラーの回は無料でした。</li>
<li><strong>測る場所で、開くページが変わる。</strong>測ったときに、たどり着いたURLが、入力と違うサイトがありました（下の表）。cookpad.comは「/de」（ドイツ語のページ）に飛びました。</li>
<li><strong>測るたびに、数字が変わる。</strong>同じURLを3回測ると、LCPは10.8秒〜20.8秒まで動きました（<a href="/articles/c62-repeat-3-times/">3回の記事</a>）。</li>
<li><strong>スマホ設定の結果だけ。</strong>このツールは、モバイルの設定で測ります。</li>
<li><strong>実際のお客さんの体感の速さではない。</strong>テスト用の環境で測った点数です。</li>
</ul>

<h2>入力のURLと、たどり着いたURLが違ったサイト</h2>
<div class="scroll"><table class="data"><thead><tr><th>サイト</th><th>最終的に開いたURL</th></tr></thead><tbody>{red}</tbody></table></div>
<p class="note">「www」の有無の違いは除いています。asahi.comの「/sp/」、itmedia.co.jpの「/spv/」、kakaku.comの「s.kakaku.com」は、URLからスマホ用のページに見えます。測定がスマホの設定のため、移った可能性がありますが、理由は確かめていません。</p>

<h2>どう使い分ける？</h2>
<ul>
<li><strong>自分のサイトを1回だけ、無料で測りたい</strong> → ChromeのDevToolsにもLighthouseが入っています（公式の機能）。</li>
<li><strong>たくさんのURLを、表やCSVで残したい</strong> → このツールが向いています。</li>
</ul>
<p>確認だけなら、まずChromeの機能でも十分です。何十ものURLを一度に測って残したくなったら、このツールを使ってみてください。</p>

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
<li>実測：<a href="/articles/c62-30-sites-lighthouse/">30サイトの記事</a>、<a href="/articles/c62-repeat-3-times/">3回の記事</a>、<a href="/articles/c62-top-vs-article/">トップと記事の記事</a>の、合計59回（成功56回、エラー3回）</li>
{COST}
</ul>
</div>
'''
for slug,body in [('c62-30-sites-lighthouse',a1),('c62-score-spread',a2),('c62-repeat-3-times',a3),('c62-top-vs-article',a4),('c62-lighthouse-limits',a5)]:
    open(R+f'articles/{slug}.html','w',encoding='utf-8').write(body)
idx=json.load(open(R+'articles/index.json',encoding='utf-8')); idx=[a for a in idx if a['tool']!='C62']
idx+=[
 {"slug":"c62-30-sites-lighthouse","tool":"C62","date":"2026-11-25","title":f"【実測】日本の人気サイト{n}個のLighthouse（モバイル）の点数を全部載せる（30サイトを測って、測れたのは{n}）","description":f"30サイトを測って、測れたのは{n}サイト。パフォーマンスは7〜78点で、90点以上のサイトはありませんでした。"},
 {"slug":"c62-score-spread","tool":"C62","date":"2026-11-25","title":"Lighthouseの4つの点数のうち、いちばんばらつくのはどれ？（27サイト）","description":"4つの点数の最高−最低を比べました。一番ばらついたのは、パフォーマンスでした。"},
 {"slug":"c62-repeat-3-times","tool":"C62","date":"2026-11-25","title":"同じURLを3回測ったら、点数は毎回同じ？（3つのURL×3回）","description":"点数はほぼ同じでしたが、LCP（一番大きい部分が出るまでの時間）は、10.8秒から20.8秒まで動きました。"},
 {"slug":"c62-top-vs-article","tool":"C62","date":"2026-11-25","title":"トップページと記事ページで、Lighthouseの点数はどれくらい違う？（10サイトのペア）","description":"10サイトのトップと記事を測りました。記事が高い組と低い組がバラバラで、差は最大で40点でした。"},
 {"slug":"c62-lighthouse-limits","tool":"C62","date":"2026-11-25","title":"表示速度を測る方法の違いと、このツールでわからないこと（測る場所でページが変わる）","description":"エラーになるサイト、測る場所で開くページが変わるサイト、測るたびに変わる数字。59回で確かめた限界を整理しました。"}]
idx.sort(key=lambda a:(a['tool'],a['slug'])); json.dump(idx,open(R+'articles/index.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
c=json.load(open(R+'articles/costs.json',encoding='utf-8'))
for sl in ['c62-30-sites-lighthouse','c62-score-spread','c62-repeat-3-times','c62-top-vs-article','c62-lighthouse-limits']:
    c['per'][sl]={'usd':{'c62-30-sites-lighthouse':0.135,'c62-score-spread':0.135,'c62-repeat-3-times':0.045,'c62-top-vs-article':0.10,'c62-lighthouse-limits':S['cost']}[sl],'note':{'c62-30-sites-lighthouse':'30サイトを測った費用（成功27回×$0.005。エラーは無料）','c62-score-spread':'30サイトのデータを使用','c62-repeat-3-times':'3URL×3回（9回×$0.005）','c62-top-vs-article':'20回×$0.005','c62-lighthouse-limits':'59回ぶん（成功56回×$0.005）の実測を使用'}[sl]}
c['real']['C62']=S['cost']
json.dump(c,open(R+'articles/costs.json','w',encoding='utf-8'),ensure_ascii=False,indent=1); print(len(idx))
