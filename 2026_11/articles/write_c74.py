import json,html
R='/home/user/tools/'
S=json.load(open(R+'articles/_inc/c74_stats.json')); H=html.escape
n=S['n_ok']; na=S['n_all']
L=lambda xs:'、'.join(xs)
BOX='''<li>日付：2026年11月25日</li>
<li>ツール：<a href="/C74/ja/">サイトの使用技術を見る（C74）</a>（DataForSEOのAPIが、サイトが使っている技術を返します）</li>'''
INPUT=f'''<li>調べたサイト：日本の人気サイトなどを、私が{na}個選びました（ニュース、IT・Webメディア、EC、暮らし・サービス情報、個人の投稿サイト、企業サイト、サーバー会社・行政）</li>
<li>結果：<strong>取れたのは{n}サイト</strong>。ほかの{na-n}サイトは、結果が空だったか、エラーでした（<a href="/articles/c74-technology-lookup-limits/">こちらの記事</a>）</li>
<li>費用：1サイトにつき<strong>$0.012</strong>。{na}サイトで<strong>${S["cost"]}</strong>（エラーは無料、結果が空の回は料金がかかりました）</li>'''
top=''.join(f'<tr><td>{H(k)}</td><td>{v}</td></tr>' for k,v in S['top'])
gen=''.join(f'<tr>{"".join(f"<td>{c}</td>" for c in row)}</tr>' for row in S['genre'])
a1=f'''<p>気になるサイトは、どんな技術でできているのでしょうか。<a href="/C74/ja/">サイトの使用技術を見るツール</a>で、日本の人気サイトなど<strong>{na}個</strong>を調べました。取れたのは<strong>{n}サイト</strong>です。その全データを載せます。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>{na}サイトのうち、技術のデータが取れたのは<strong>{n}サイト</strong>、結果が空だったのが<strong>{S["stat"]["結果なし（技術が空）"]}サイト</strong>、エラーが<strong>{S["stat"]["エラー"]}サイト</strong>でした。</li>
<li>取れた{n}サイトで見つかった技術は、重なりを除いて<strong>{S["total_techs"]}種類</strong>でした。</li>
<li>見つかった技術の数が一番多かったのは<strong>{S["maxs"][0]}（{S["maxs"][1]}個）</strong>、一番少なかったのは<strong>{S["mins"][0]}（{S["mins"][1]}個）</strong>でした。</li>
<li>一番多く使われていたのは<strong>Google Tag Manager（{n}サイト中{len(S["gtm"])}サイト）</strong>でした。</li>
</ul>
<p>家の外から、壁の素材や屋根の種類をのぞいて、メモした表です。見えないものは、メモできません。</p>

<h2>よく使われていた技術（上位15）</h2>
<div class="scroll"><table class="data"><thead><tr><th>技術名</th><th>使っているサイト数（{n}サイト中）</th></tr></thead><tbody>{top}</tbody></table></div>

<h2>全データ：サイトごとの技術</h2>
<p>サイトごとの、大分類・小分類・技術名を、APIが返したまま載せています。ジャンルは私が付けたものです。</p>
<p><a href="/articles/data/c74-technologies-2026-11-25.csv" download>CSVでダウンロード</a></p>
<!--include:c74_table-->

<h2>全データ：技術ごとの、使っているサイト（全{S["total_techs"]}種類）</h2>
<p><a href="/articles/data/c74-technology-counts-2026-11-25.csv" download>CSVでダウンロード</a></p>
<!--include:c74_count-->

<h2>全データ：サイトごとの、見つかった技術の数</h2>
<!--include:c74_sites-->

<h2>この表から作った記事</h2>
<ul>
<li><a href="/articles/c74-wordpress-count/">WordPressを使っているサイトは何個？</a></li>
<li><a href="/articles/c74-analytics-ad-tags/">分析ツールと広告タグは、どれくらい使われている？</a></li>
<li><a href="/articles/c74-technology-by-genre/">ジャンル別に、使われている技術を並べたら</a></li>
<li><a href="/articles/c74-technology-lookup-limits/">サイトの使用技術を調べる方法と、わからないこと</a></li>
</ul>

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
{INPUT}
</ul>
</div>
<p class="note">APIが見つけた技術だけの結果です。サイトが実際に使っている技術のすべてではありません（たとえば rakuten.co.jp は、見つかったのが1個だけでした）。</p>
'''
a2=f'''<p>「WordPressは、世界でも日本でも、よく使われている」と聞きます。人気サイトの中では、どれくらい使われているのでしょうか。<a href="/articles/c74-sites-technologies/">技術が取れた{n}サイト</a>で数えました。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>WordPressが見つかったのは、{n}サイトのうち<strong>{len(S["wp"])}サイト</strong>（{L(S["wp"])}）でした。</li>
<li>CMS（記事を管理する仕組み）が見つかったのは<strong>{len(S["cms"])}サイト</strong>で、残りの{n-len(S["cms"])}サイトでは、CMSの名前は返りませんでした。WordPress以外には、<strong>Drupal</strong>（digital.go.jp）が見つかりました。</li>
<li>CMSが返らなかったサイトも、実際には何かのCMSを使っているかもしれません。APIが見つけられなかっただけの可能性があります。</li>
</ul>
<p>お店の看板が出ていないからといって、お店がないとは限りません。「見つかった」と「使っていない」は、別の話です。</p>

<h2>CMSが見つかった{len(S["cms"])}サイト</h2>
<div class="scroll"><table class="data"><thead><tr><th>サイト</th><th>見つかったCMS</th></tr></thead><tbody>{"".join(f"<tr><td>{H(s)}</td><td>{H(' ／ '.join(S['cms_names'][s]))}</td></tr>" for s in S["cms"])}</tbody></table></div>

<h2>全データ：サイトごとの技術</h2>
<p><a href="/articles/data/c74-technologies-2026-11-25.csv" download>CSVでダウンロード</a></p>
<details><summary>全データの表を開く</summary>
<!--include:c74_table-->
</details>

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
{INPUT}
<li>数え方：APIが返した技術名が「WordPress」のものを数えました。CMSは、大分類「content」の小分類「cms」「blogs」に入っていたものです</li>
<li>データ：<a href="/articles/c74-sites-technologies/">{n}サイトの記事</a>と同じ</li>
</ul>
</div>
<p class="note">{na}サイトは、私が選んだものです。日本のサイト全体の割合ではありません。</p>
'''
a3=f'''<p>サイトの中には、アクセスを数える「分析ツール」や、広告を出す「広告タグ」が入っています。<a href="/articles/c74-sites-technologies/">技術が取れた{n}サイト</a>の中で、どれくらい使われているかを数えました。</p>

<h2>先に、わかったこと</h2>
<ul>
<li><strong>Google Tag Manager</strong>（タグをまとめて管理する仕組み）は、{n}サイト中<strong>{len(S["gtm"])}サイト</strong>で見つかりました。</li>
<li><strong>Google Analytics</strong>は{len(S["ga"])}サイト（{L(S["ga"])}）。Facebook Pixelは{len(S["fb"])}サイト（{L(S["fb"])}）でした。</li>
<li><strong>広告の技術</strong>（Google Publisher Tag、DoubleClick Floodlight）は、どちらも同じ<strong>{len(S["gpt"])}サイト</strong>で見つかりました。ニュースやITメディアが中心です（{L(S["gpt"])}）。</li>
<li>Google Tag Managerの中でGoogle Analyticsなどを動かしているサイトは、<strong>Google Analyticsとして見つからないことがあります</strong>。この表の数字は、「見つかった数」です。</li>
</ul>
<p>建物の入口に、「出入りを数える機械」と「看板を貼る場所」があるか、のぞいて数えた感じです。</p>

<h2>数えた結果</h2>
<div class="scroll"><table class="data"><thead><tr><th>技術</th><th>見つかったサイト数（{n}サイト中）</th><th>サイト</th></tr></thead><tbody>
<tr><td>Google Tag Manager</td><td>{len(S["gtm"])}</td><td>{H(L(S["gtm"]))}</td></tr>
<tr><td>Google Analytics</td><td>{len(S["ga"])}</td><td>{H(L(S["ga"]))}</td></tr>
<tr><td>Facebook Pixel</td><td>{len(S["fb"])}</td><td>{H(L(S["fb"]))}</td></tr>
<tr><td>Google Publisher Tag</td><td>{len(S["gpt"])}</td><td>{H(L(S["gpt"]))}</td></tr>
<tr><td>DoubleClick Floodlight</td><td>{len(S["dfl"])}</td><td>{H(L(S["dfl"]))}</td></tr>
<tr><td>大分類「広告（advertising）」が見つかった</td><td>{len(S["adv"])}</td><td>{H(L(S["adv"]))}</td></tr>
</tbody></table></div>

<h2>全データ：技術ごとの、使っているサイト</h2>
<p><a href="/articles/data/c74-technology-counts-2026-11-25.csv" download>CSVでダウンロード</a></p>
<!--include:c74_count-->

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
{INPUT}
<li>データ：<a href="/articles/c74-sites-technologies/">{n}サイトの記事</a>と同じ</li>
</ul>
</div>
<p class="note">サイトは私が選んだ{na}個です。日本のサイト全体の傾向ではありません。</p>
'''
a4=f'''<p>ニュースサイト、ECサイト、企業サイト。ジャンルが違うと、使われている技術も違うのでしょうか。<a href="/articles/c74-sites-technologies/">技術が取れた{n}サイト</a>を、私が付けたジャンルで分けて、並べました。</p>

<h2>先に、わかったこと</h2>
<ul>
<li>広告の技術（Google Publisher Tag、DoubleClick Floodlight）が見つかった{len(S["gpt"])}サイトは、<strong>ニュースサイト3つ（asahi.com、yomiuri.co.jp、toyokeizai.net）、IT・Webメディア5つ（itmedia.co.jp、ascii.jp、lifehacker.jp、gizmodo.jp、ferret-plus.com）、kakaku.com、tabelog.com</strong>でした。</li>
<li>見つかった技術の数は、ジャンルで平均が違いました（下の表）。</li>
<li>CMSのWordPressが見つかったのは、ニュース（yomiuri.co.jp）と、暮らし・サービス情報（mynavi.jp）の2サイトです。</li>
</ul>

<h2>ジャンルごとの技術</h2>
<p>ジャンルは、私が付けたものです（意味での分類で、APIの分類ではありません）。</p>
<div class="scroll"><table class="data"><thead><tr><th>ジャンル</th><th>サイト数</th><th>見つかった技術の平均数</th><th>よく使われていた技術（サイト数）</th></tr></thead><tbody>{gen}</tbody></table></div>

<h2>全データ：サイトごとの見つかった技術の数</h2>
<!--include:c74_sites-->

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
{INPUT}
<li>ジャンル：私が付けました。ニュース、IT・Webメディア、EC・ショッピング、暮らし・サービス情報、個人の投稿サイト、企業サイト、サーバー会社・行政の7つ</li>
<li>データ：<a href="/articles/c74-sites-technologies/">{n}サイトの記事</a>と同じ</li>
</ul>
</div>
<p class="note">1つのジャンルに、サイトが2〜5個しかありません。傾向と言うには数が少ないので、参考として見てください。</p>
'''
errrows=''.join(f'<tr><td>{H(s)}</td><td>{H(m)}</td></tr>' for s,m in S['errors'])
a5=f'''<p>サイトの使用技術のAPIでは、何がわかって、何がわからないのでしょうか。<a href="/C74/ja/">サイトの使用技術を見るツール</a>で、{na}サイトを調べて、確かめた事実を整理します。</p>

<h2>結果（{na}サイトを調べた）</h2>
<ul>
<li><strong>技術が取れた：{S["stat"]["取得できた"]}サイト</strong></li>
<li><strong>結果が空だった：{S["stat"]["結果なし（技術が空）"]}サイト</strong>（{L(S["empty"])}）。リクエストは成功（Ok）でしたが、技術の情報が返りませんでした。<strong>この場合も、料金はかかりました</strong>。</li>
<li><strong>エラー：{S["stat"]["エラー"]}サイト</strong>。うち4サイトは「Target page took too long to respond（サイトの応答が遅すぎた）」でした。エラーの回は、料金はかかりませんでした。</li>
</ul>

<h2>エラーになったサイト</h2>
<div class="scroll"><table class="data"><thead><tr><th>サイト</th><th>エラーの内容</th></tr></thead><tbody>{errrows}</tbody></table></div>
<p>hatenablog.comは「別のドメインへリダイレクトされる」というエラーでした。応答が遅かった4サイトのうち、suumo.jpとuniqlo.comは、2回試しても同じでした。</p>

<h2>わかること（実測）</h2>
<ul>
<li><strong>見つかった技術の一覧。</strong>大分類・小分類・技術名で返ります。</li>
<li><strong>低い費用。</strong>1サイトにつき$0.012（約1.9円）。</li>
</ul>

<h2>わからないこと・気をつけること（実測）</h2>
<ul>
<li><strong>見つかる技術は、一部だけ。</strong>rakuten.co.jpは、見つかったのが1個（Apache HTTP Server）だけでした。</li>
<li><strong>CMSが返らないサイトが多い。</strong>{n}サイト中、CMSが見つかったのは{len(S["cms"])}サイトでした。</li>
<li><strong>結果が空・エラーのサイトがある。</strong>{na}サイト中{na-n}サイト（{(na-n)/na*100:.0f}%）で、技術のデータが取れませんでした。</li>
<li><strong>Google Tag Managerの中の技術は、見えにくい。</strong>タグマネージャーの中で動かしている分析ツールは、別に見つからないことがあります。</li>
<li><strong>サイトの良し悪しは分からない。</strong>データを見せるだけです。</li>
</ul>

<h2>どう使い分ける？</h2>
<ul>
<li><strong>1つのサイトを、ちょっと確認したい</strong> → ブラウザの開発者ツールや、ブラウザの拡張機能でも見られます。</li>
<li><strong>たくさんのサイトを、表やCSVで残したい</strong> → このツールが向いています。</li>
</ul>
<p>確認だけなら、まず無料の方法でも十分です。表にまとめたくなったら、このツールを使ってみてください。</p>

<h2>全データ：{na}サイトの結果</h2>
<p><a href="/articles/data/c74-status-2026-11-25.csv" download>CSVでダウンロード</a></p>
<!--include:c74_status-->

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
{BOX}
{INPUT}
</ul>
</div>
'''
for slug,body in [('c74-sites-technologies',a1),('c74-wordpress-count',a2),('c74-analytics-ad-tags',a3),('c74-technology-by-genre',a4),('c74-technology-lookup-limits',a5)]:
    open(R+f'articles/{slug}.html','w',encoding='utf-8').write(body)
idx=json.load(open(R+'articles/index.json',encoding='utf-8')); idx=[a for a in idx if a['tool']!='C74']
idx+=[
 {"slug":"c74-sites-technologies","tool":"C74","date":"2026-11-25","title":f"【実測】日本の人気サイト{n}個が使っている技術を全部載せる（{na}サイトを調べて、取れたのは{n}）","description":f"{na}サイトを調べて、技術のデータが取れたのは{n}サイト。見つかった技術を、サイトごとに全部載せます。"},
 {"slug":"c74-wordpress-count","tool":"C74","date":"2026-11-25","title":f"WordPressを使っているサイトは何個？{n}サイトで数えた（見つかったのは{len(S['wp'])}個）","description":f"{n}サイトのうち、WordPressが見つかったのは{len(S['wp'])}サイトでした。CMSの名前が返らないサイトが多い点も書いています。"},
 {"slug":"c74-analytics-ad-tags","tool":"C74","date":"2026-11-25","title":"分析ツールと広告タグは、どれくらい使われている？（25サイトで数えた）","description":f"Google Tag Managerは{len(S['gtm'])}サイト、Google Analyticsは{len(S['ga'])}サイト、広告の技術は{len(S['gpt'])}サイトで見つかりました。"},
 {"slug":"c74-technology-by-genre","tool":"C74","date":"2026-11-25","title":"ジャンル別に、使われている技術を並べたら（25サイト）","description":"ニュース、IT・Webメディア、EC、企業などのジャンルごとに、見つかった技術を並べました。"},
 {"slug":"c74-technology-lookup-limits","tool":"C74","date":"2026-11-25","title":f"サイトの使用技術を調べる方法の違いと、このツールでわからないこと（{na}サイト中{na-n}サイトは取れなかった）","description":"結果が空のサイト、エラーのサイト、見つからない技術。39サイトで確かめた限界を整理しました。"}]
idx.sort(key=lambda a:(a['tool'],a['slug'])); json.dump(idx,open(R+'articles/index.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
c=json.load(open(R+'articles/costs.json',encoding='utf-8'))
for sl in ['c74-sites-technologies','c74-wordpress-count','c74-analytics-ad-tags','c74-technology-by-genre','c74-technology-lookup-limits']:
    c['per'][sl]={'usd':S['cost'],'note':f'{na}サイトを調べた費用（1サイト$0.012。エラーは無料、結果が空の回は有料）' if sl=='c74-sites-technologies' else f'{na}サイトのデータを使用'}
c['real']['C74']=S['cost']
json.dump(c,open(R+'articles/costs.json','w',encoding='utf-8'),ensure_ascii=False,indent=1); print(len(idx))
