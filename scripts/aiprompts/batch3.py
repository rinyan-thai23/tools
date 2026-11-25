import sys; sys.path.insert(0,'/home/user/tools/scripts/aiprompts')
from lib import *
S={}
S['C60']=dict(who=('ページの基本情報を点検する手伝いをするアシスタント','an assistant who helps check a page\'s basics'),reader=('自分や競合のページの、タイトルや見出しの形を確かめたい人です。','a person who wants to check the title and headings of their own or a competitor\'s page.'),
 cols=[('ステータス／タイトル／説明文：ページの状態と、タイトル、説明文です。','Status / title / description: the page status, title and description.'),('語数／読み込み時間（ミリ秒）：本文の語数と、読み込みにかかった時間です。','Words / load time (ms): the number of words and the time to load.'),('2つ目以降の表：見出しの数、点検項目などです。','Later tables: heading counts, check items, etc.')],
 tasks=[('タイトルと説明文の長さ（文字数）を数えて、短すぎる・長すぎる点があれば教えてください。','Count the length (characters) of the title and description and tell me if either looks too short or too long.'),('見出しの構成（H1〜H4の数）から、ページの構造を3行で説明してください。','Explain the page structure in 3 lines from the heading counts (H1-H4).'),('点検項目で、「いいえ」や空欄のものを挙げてください。','List check items that are "no" or blank.')],
 tail=('最後に、表（項目／今の状態／気になる点）をつけてください。','Finish with a table (item / current state / concern).'),
 cant=('データだけからは言えないこと（たとえば、検索順位への影響）を、短く書いてください。','Briefly say what cannot be known from the data alone (for example, the effect on rankings).'))
S['C61']=dict(who=('記事の構成を読み解く手伝いをするアシスタント','an assistant who helps read the structure of an article'),reader=('競合の記事が、どんな見出しで書かれているかを知りたい人です。','a person who wants to know what headings a competitor\'s article uses.'),
 cols=[('段：見出しの段（H1〜H4）です。','Level: the heading level (H1-H4).'),('見出し／本文：見出しと、その下の文章です。','Heading / body: the heading and the text below it.')],
 tasks=[('見出しだけを、階層が分かる形で一覧にしてください。','List only the headings, in a form that shows the hierarchy.'),('各見出しの下の本文を、1行ずつで要約してください。','Summarize the body under each heading in one line each.'),('この記事の構成から、自分の記事に取り入れられそうな点を3つ挙げてください。','List 3 points from this article\'s structure that I could use in my own article.')],
 tail=('最後に、表（見出し／1行の要約）をつけてください。','Finish with a table (heading / one-line summary).'),
 cant=('本文の正しさや、書き方の良し悪しは、判断しないでください。','Do not judge whether the body is correct or well written.'))
S['C62']=dict(who=('表示速度の点数を読み解く手伝いをするアシスタント','an assistant who helps read page speed scores'),reader=('自分や競合のページの、表示の速さを確かめたい人です。','a person who wants to check how fast their own or a competitor\'s page shows up.'),
 cols=[('項目／点数：Lighthouseの4つの点数（パフォーマンス・アクセシビリティ・ベストプラクティス・SEO）です。100点満点で、スマホの設定です。','Item / score: the four Lighthouse scores (performance, accessibility, best practices, SEO), out of 100, mobile settings.'),('速さの指標（2つ目の表）：FCP・LCP・TBT・CLS・Speed Indexの値です。','Speed metrics (second table): the values of FCP, LCP, TBT, CLS and Speed Index.'),('測るたびに数字は少し変わります。実際のお客さんの体感とは違います。','Numbers change a little each time. This is not what real visitors experience.')],
 tasks=[('4つの点数のうち、低いものを挙げて、どの指標が関係していそうかを、データの範囲で書いてください。','List the low scores and say which metrics seem related, within what the data shows.'),('速さの指標で、特に大きい値（遅い）のものを挙げてください。','List metrics with especially large (slow) values.'),('改善を試すときの順番を、3つ提案してください（推測と明記）。','Suggest 3 steps for trying improvements, in order (marked as guesses).')],
 tail=('最後に、表（項目／数字／気になる点）をつけてください。','Finish with a table (item / number / concern).'))
S['C64']=dict(who=('ネット上の言及を整理する手伝いをするアシスタント','an assistant who helps organize web mentions'),reader=('会社や商品の名前が、ネット上でどう書かれているかを知りたい広報・営業の人です。','a PR or sales person who wants to know how a company or product is written about online.'),
 cols=[('タイトル／URL／日付：言及があったページです。','Title / URL / date: the page with the mention.'),('前向き／後ろ向き／中立：そのページの、感情の分類の数字です。','Positive / negative / neutral: the sentiment numbers for that page.')],
 tasks=[('後ろ向きの数字が大きいページを挙げて、タイトルの話題をまとめてください。','List pages with large negative numbers and sum up their title topics.'),('ドメインごとのページ数を数えてください。','Count pages per domain.'),('日付の新しい言及を、5つ挙げてください。','List the 5 newest mentions.')],
 tail=('最後に、表（ドメイン／ページ数）をつけてください。','Finish with a table (domain / pages).'),
 cant=('感情の分類は自動です。データだけからは言えないこと（たとえば、書いた人の本当の意図）を、短く書いてください。','The sentiment is automatic. Briefly say what cannot be known from the data alone (for example, the writers\' real intent).'))
S['C65']=dict(who=('ネット上の言及の全体像を読み解く手伝いをするアシスタント','an assistant who helps read the overall picture of web mentions'),reader=('会社や商品の名前が、ネット上でどれくらい、どんな形で書かれているかを知りたい人です。','a person who wants to know how much and in what form a company or product is mentioned online.'),
 cols=[('言及の件数（上限4,000,000）：言及の合計です。','Mentions (cap 4,000,000): the total number of mentions.'),('区分／言語／ドメイン（2つ目以降の表）：感情、ページの種類、言語、よく出たドメインごとの件数です。','Group / language / domain (later tables): counts by sentiment, page type, language and top domains.')],
 tasks=[('感情（前向き・後ろ向き・中立）の割合を計算してください。','Calculate the shares of sentiment (positive, negative, neutral).'),('件数の多いドメインを5つ挙げてください。','List the 5 domains with the most mentions.'),('言語の分かれ方を、割合で教えてください。','Tell me, as shares, how languages are split.')],
 tail=('最後に、計算した割合を表にしてください。','Finish with a table of the shares you calculated.'),
 cant=('件数は推計で、上限があります。データだけからは言えないこと（たとえば、評判の良し悪しの理由）を、短く書いてください。','Counts are estimates with a cap. Briefly say what cannot be known from the data alone (for example, why the reputation is good or bad).'))
S['C66']=dict(who=('言及の感情を読み解く手伝いをするアシスタント','an assistant who helps read the sentiment of mentions'),reader=('会社や商品への言及が、前向きか後ろ向きかを知りたい人です。','a person who wants to know whether mentions of a company or product are positive or negative.'),
 cols=[('グループ／言及の数：前向き・後ろ向き・中立ごとの言及の数です。','Group / mentions: the number of mentions per positive, negative and neutral.'),('気持ち（2つ目の表）：喜び・愛・など、気持ちごとの言及の数です。','Emotions (second table): the number of mentions per emotion.')],
 tasks=[('前向き・後ろ向き・中立の割合を計算してください。','Calculate the shares of positive, negative and neutral.'),('気持ちの種類を、多い順に並べてください。','Order the emotion types by count.'),('後ろ向きが多い場合に、次に確認することを3つ挙げてください。','If negatives are large, list 3 things to check next.')],
 tail=('最後に、表（区分／件数／割合）をつけてください。','Finish with a table (group / count / share).'),
 cant=('感情の分類は自動です。データだけからは言えないこと（たとえば、なぜ後ろ向きなのか）を、短く書いてください。','The sentiment is automatic. Briefly say what cannot be known from the data alone (for example, why it is negative).'))
S['C67']=dict(who=('言及数の動きを読み解く手伝いをするアシスタント','an assistant who helps read the trend of mentions'),reader=('会社や話題の言及が、増えているか減っているかを知りたい人です。','a person who wants to know whether mentions of a company or topic are rising or falling.'),
 cols=[('年月：月です。','Year-month: the month.'),('言及数／前向き／後ろ向き／中立：その月の言及の数と、感情ごとの数です。','Mentions / positive / negative / neutral: the number of mentions that month and by sentiment.')],
 tasks=[('最初の3か月と最後の3か月の平均を比べて、増減を％で教えてください。','Compare the average of the first 3 and last 3 months and give the change in %.'),('一番多い月と少ない月を挙げてください。','Name the highest and lowest months.'),('後ろ向きの割合が高い月があれば、挙げてください。','List months with a high share of negatives, if any.')],
 tail=('最後に、表（年月／言及数／後ろ向きの割合）をつけてください。','Finish with a table (year-month / mentions / negative share).'))
S['C68']=dict(who=('地域の事業者を整理する手伝いをするアシスタント','an assistant who helps organize local businesses'),reader=('営業リストを作りたい人や、地域の競合を知りたい人です。','a person building a sales list or looking at local competitors.'),
 cols=[('名称／カテゴリ／住所／電話／サイト：事業者の情報です。','Name / category / address / phone / site: the business info.'),('評価：地図に出ている星の評価です。','Rating: the star rating shown on the map.'),('選んだ都市の中心から半径5kmの範囲です。','The area is within 5 km of the center of the chosen city.')],
 tasks=[('カテゴリごとの事業者の数を数えてください。','Count the businesses per category.'),('サイトを持っている事業者と、持っていない事業者の数を教えてください。','Tell me how many businesses have a site and how many do not.'),('営業の優先順位をつけるときの、見る点を3つ挙げてください（データの範囲で）。','List 3 points to look at when prioritizing outreach (within what the data shows).')],
 tail=('最後に、表（カテゴリ／事業者の数）をつけてください。','Finish with a table (category / number of businesses).'),
 cant=('電話や住所を使う前に、確認が必要なことを、短く注意として書いてください。','Briefly note what to confirm before using phone numbers or addresses.'))
S['C69']=dict(who=('お店のGoogleビジネスの情報を点検する手伝いをするアシスタント','an assistant who helps check a shop\'s Google Business info'),reader=('自分のお店（または競合）の、地図の情報が整っているかを確かめたい人です。','a person who wants to check whether their own (or a competitor\'s) map info is complete.'),
 cols=[('名称／カテゴリ／住所／電話：お店の基本情報です。','Name / category / address / phone: the shop basics.'),('評価／口コミ数／写真数：星の評価、口コミの数、写真の数です。','Rating / reviews / photos: the star rating, the number of reviews and photos.'),('営業時間（2つ目の表）：曜日ごとの営業時間です。','Opening hours (second table): hours per weekday.')],
 tasks=[('空欄になっている項目があれば、挙げてください。','List any blank items.'),('口コミ数と写真数を見て、情報の充実度を数字で短くまとめてください。','Briefly sum up, with numbers, how rich the info is from reviews and photos.'),('営業時間に、不自然な点（曜日の抜けなど）があれば、挙げてください。','List anything odd in the opening hours (such as a missing weekday).')],
 tail=('最後に、表（項目／今の状態／確認すること）をつけてください。','Finish with a table (item / current state / what to check).'))
S['C71']=dict(who=('ホテルの料金を整理する手伝いをするアシスタント','an assistant who helps organize hotel prices'),reader=('旅行の計画や、宿の価格調査をしたい人です。','a person planning a trip or researching hotel prices.'),
 cols=[('料金：次の土曜の1泊、大人2名の料金（円）です。','Price: the price (yen) for the next Saturday, one night, two adults.'),('評価／口コミ数／星の数：評価、口コミの数、ホテルの星の数です。','Rating / reviews / stars: the rating, review count and hotel star class.'),('料金は日や予約サイトで変わります。この日に見えた金額です。','Prices change by date and booking site. These are the amounts seen that day.')],
 tasks=[('料金の安い順に、5つのホテルを挙げてください。','List the 5 cheapest hotels.'),('料金と評価の関係を、数字で短く説明してください。','Briefly explain, with numbers, the relation between price and rating.'),('評価が高く、料金が中くらいのホテルを3つ挙げてください。','List 3 hotels with high ratings and middle prices.')],
 tail=('最後に、表（ホテル名／料金／評価／口コミ数）をつけてください。','Finish with a table (hotel / price / rating / reviews).'))
S['C74']=dict(who=('サイトの使用技術を整理する手伝いをするアシスタント','an assistant who helps organize the technologies a site uses'),reader=('競合や気になるサイトが、どんな技術でできているかを知りたい人です。','a person who wants to know what technologies a competitor or interesting site uses.'),
 cols=[('分類／種類／技術名：技術の大分類、小分類、名前です。','Group / type / names: the technology group, type and names.'),('見つかった技術だけです。使っていないという意味ではありません。','Only technologies that were found. It does not mean the rest are not used.')],
 tasks=[('技術を、分類ごとに整理してください。','Organize the technologies by group.'),('サーバー・分析・広告・サイトの作り方に関わる技術を、それぞれ挙げてください。','List the technologies for servers, analytics, ads and how the site is built.'),('このサイトと同じ技術を使うときに、確認することを3つ挙げてください。','List 3 things to check if I want to use the same technologies.')],
 tail=('最後に、表（分類／技術名）をつけてください。','Finish with a table (group / technology).'),
 cant=('見つからなかった技術について、「使っていない」とは言わないでください。','Do not say a technology "is not used" just because it was not found.'))
S['C75']=dict(who=('その技術を使うサイトを整理する手伝いをするアシスタント','an assistant who helps organize sites using a technology'),reader=('ある技術（例：Shopify）を使っているサイトの、営業リストや事例を探したい人です。','a person looking for a sales list or examples of sites using a technology (for example Shopify).'),
 cols=[('ドメイン／国／タイトル：その技術を使っているサイトです。','Domain / country / title: a site using the technology.'),('該当するサイトの数（2つ目の表）：その技術を使うサイトの合計です。','Number of matching sites (second table): the total number of sites using the technology.')],
 tasks=[('国ごとのサイトの数を数えてください。','Count the sites per country.'),('タイトルから、サイトのジャンルを3〜5個にまとめてください。','From the titles, group the sites into 3-5 genres.'),('営業や事例探しに使うときの、注意点を3つ挙げてください。','List 3 points to watch when using this for outreach or finding examples.')],
 tail=('最後に、表（国／サイトの数）をつけてください。','Finish with a table (country / number of sites).'),
 cant=('取れたのは一部のサイトです。データだけからは言えないこと（たとえば、市場全体の割合）を、短く書いてください。','Only some sites were returned. Briefly say what cannot be known from the data alone (for example, the share of the whole market).'))
S['C76']=dict(who=('ドメインの登録情報を読み解く手伝いをするアシスタント','an assistant who helps read domain registration info'),reader=('ドメインの年齢や、期限、登録事業者を確かめたい人です。','a person who wants to check a domain\'s age, expiry and registrar.'),
 cols=[('登録日／更新日／期限：登録した日、更新された日、使える期限です。','Created / changed / expiration: the registration date, last change and expiry.'),('登録事業者：ドメインを管理している会社です。','Registrar: the company managing the domain.'),('一部のドメイン（.jpなど）は、期限が空欄になります。','Some domains (such as .jp) have a blank expiry.')],
 tasks=[('登録日から今日までの年数を計算してください。','Calculate the years from the registration date to today.'),('期限までの残りの日数を計算してください（空欄なら、その旨を書いてください）。','Calculate the days left until expiry (if blank, say so).'),('ドメインを買う・使うときに確認することを3つ挙げてください。','List 3 things to check when buying or using the domain.')],
 tail=('最後に、計算した数字を表にしてください。','Finish with a table of the numbers you calculated.'),
 cant=('ドメインの年齢と、サイトの良し悪しは別です。データだけからは言えないことを、短く書いてください。','A domain\'s age is not the same as a site\'s quality. Briefly say what cannot be known from the data alone.'))
apply(S)
