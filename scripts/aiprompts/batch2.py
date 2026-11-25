import sys; sys.path.insert(0,'/home/user/tools/scripts/aiprompts')
from lib import *
S={}
def ai(tid,name_ja,name_en,extra_ja,extra_en,cols):
    S[tid]=dict(answer=True,who=(f'{name_ja}の答えを読み解く手伝いをするアシスタント',f'an assistant who helps read {name_en} answers'),
     reader=('お客さんがAIに聞きそうな質問で、自分の会社や商品が出てくるかを確認したい人です。','a person who wants to check whether their company or product appears when customers ask AI such questions.'),
     cols=cols+['ai'],extra=[(extra_ja,extra_en)] if extra_ja else [],
     tasks=[('答えに出てくる会社名・商品名・店名を、出てきた順にすべて挙げてください。','List every company, product and shop name in the answer, in the order they appear.'),('自分の会社や商品が出ているかを確認するための点を、3つ挙げてください。','List 3 points to check whether my company or product appears.'),('参照元（引用元）があれば、ドメインを数えてください。なければ「なし」と書いてください。','If sources are shown, count the domains. If not, write "none".')],
     tail=('最後に、表（名前／出てきた順）をつけてください。','Finish with a table (name / order of appearance).'),
     cant=('データだけからは言えないこと（たとえば、どうすれば答えに載るか）を、短く書いてください。','Briefly say what cannot be known from the data alone (for example, how to get into the answer).'))
ai('C18','ChatGPT','ChatGPT','このツールのChatGPTは、画面のChatGPTと同じとは限りません。','The ChatGPT used by this tool may differ from the ChatGPT screen.',[('引用ページのタイトル／URL：答えが参照したページです。','Cited page title / URL: the pages the answer used.')])
ai('C19','Claude','Claude','このツールのClaudeは、Web検索を使いません。引用元は出ません。','The Claude in this tool does not use web search. No sources are shown.',[('答え：Claudeの答えの文章です。','Answer: the text of Claude\'s answer.')])
ai('C20','Gemini','Gemini','','',[('引用元の名前／URL：答えが引用したページです。','Source name / URL: the pages the answer cited.')])
ai('C21','Perplexity','Perplexity','','',[('ページのタイトル／URL：答えが参照したページです。','Page title / URL: the pages the answer used.')])
S['C22']=dict(answer=True,who=('ChatGPT検索の結果を読み解く手伝いをするアシスタント','an assistant who helps read ChatGPT search results'),reader=('自分の商品や店が、ChatGPTの買い物・検索の答えに出るかを確認したい人です。','a person who wants to check whether their product or shop appears in ChatGPT shopping and search answers.'),
 cols=[('引用元のタイトル／サイト／URL：答えが参照したページです。','Source title / site / URL: the pages the answer used.'),('商品名／タグ：答えに出た商品と、その分類（2つ目の表）です。','Product / tag: the products shown in the answer and their tags (second table).'),'ai'],
 tasks=[('答えに出てくる商品名・ブランド名を、出てきた順にすべて挙げてください。','List every product and brand name in the answer, in the order they appear.'),('引用元のサイトを数えて、よく出るサイトを挙げてください。','Count the source sites and list the ones that appear often.'),('自分の商品が出ているかを確認するための点を、3つ挙げてください。','List 3 points to check whether my product appears.')],
 tail=('最後に、表（ブランド・商品名／出てきた順）をつけてください。','Finish with a table (brand / product / order).'))
S['C23']=dict(who=('AIでの質問回数を読み解く手伝いをするアシスタント','an assistant who helps read AI question volumes'),reader=('このテーマが、AIでも聞かれているかを知りたい人です。','a person who wants to know whether this topic is also asked in AI.'),
 cols=[('年月：月です。','Year-month: the month.'),('AI上の検索数：その月に、AIで聞かれた回数の推計です。実際の回数ではありません。0もあります。','AI searches: an estimate of how many times it was asked in AI that month. Not exact. Zero is possible.')],
 tasks=[('一番多い月と少ない月を挙げて、差（何倍か）を計算してください。','Name the busiest and quietest months and calculate the ratio.'),('増えているか減っているかを、最初の3か月と最後の3か月の平均で比べてください。','Compare the average of the first 3 months with the last 3 months to see if it is rising or falling.'),('0の月があれば、教えてください。','Tell me about months with zero, if any.')],
 tail=('最後に、表（年月／AI上の検索数）をつけてください。','Finish with a table (year-month / AI searches).'))
S['C26']=dict(who=('広告用のキーワードを整理する手伝いをするアシスタント','an assistant who helps organize ad keywords'),reader=('広告やSEOで使うキーワードを、候補から選びたい人です。','a person choosing keywords for ads or SEO from candidates.'),
 cols=['vol','cpc','comp'],
 tasks=[('キーワードを、テーマごとに3〜5個のグループに分けてください。','Group the keywords into 3-5 themes.'),('検索数が大きく、CPCが低めの候補を5つ挙げて、数字つきで理由を書いてください。','List 5 candidates with large searches and lower CPC, with reasons and numbers.'),('競合度が高い候補を挙げて、注意点を書いてください。','List high-competition candidates and note what to watch for.')],
 tail=('最後に、表（グループ／キーワード／月間検索数／CPC）をつけてください。','Finish with a table (group / keyword / searches / CPC).'))
def trend(tid,who_ja,who_en,reader_ja,reader_en,cols,tasks,tail,extra=None):
    S[tid]=dict(who=(who_ja,who_en),reader=(reader_ja,reader_en),cols=cols+['now'],tasks=tasks,tail=tail,extra=extra or [])
trend('C29','Googleトレンドを読み解く手伝いをするアシスタント','an assistant who helps read Google Trends','言葉の人気の動きを、比べたい人です。','a person who wants to compare how popular terms move.',
 [('期間（週）：その週です。','Period (week): the week.'),('人気度（入れた順）：入力した言葉の順に、人気度（0〜100）が入っています。検索数そのものではありません。','Popularity (in input order): the popularity (0-100) of each term in the order entered. Not a search volume.')],
 [('言葉ごとに、一番高い週と平均を挙げてください。','For each term, name the peak week and the average.'),('増えている言葉と減っている言葉を、最初と最後の4週の平均で比べてください。','Compare the average of the first and last 4 weeks to see which terms rise and fall.'),('言葉どうしの動きが似ているかを、数字で短く書いてください。','Briefly say, with numbers, whether the terms move alike.')],
 ('最後に、表（言葉／ピーク週／平均）をつけてください。','Finish with a table (term / peak week / average).'))
trend('C30','人気度の推移を読み解く手伝いをするアシスタント','an assistant who helps read a popularity trend','1つの言葉の人気が、いつ高くなるかを知りたい人です。','a person who wants to know when one term gets popular.',
 [('期間（週）：その週です。','Period (week): the week.'),('人気度（0〜100）：期間の中の最大を100とした、相対的な値です。検索数ではありません。','Popularity (0-100): a relative value where the maximum in the period is 100. Not a search volume.')],
 [('ピークの週を挙げてください。毎年同じ時期になっているかも教えてください。','Name the peak weeks and tell me whether they fall in the same season each year.'),('最近の4週の平均と、1年前の同じ時期の平均を比べてください。','Compare the average of the last 4 weeks with the same weeks a year ago.'),('0や小さい値が続く期間があれば、教えてください。','Tell me about periods with zero or small values, if any.')],
 ('最後に、表（時期／人気度）で、ピークのまとめをつけてください。','Finish with a table summarizing the peaks (period / popularity).'))
trend('C31','地域ごとの人気を読み解く手伝いをするアシスタント','an assistant who helps read popularity by region','どの地域で、その言葉が人気かを知りたい人です。','a person who wants to know in which regions a term is popular.',
 [('地域：都道府県などの地域です。','Region: a prefecture or other region.'),('人気度（最大=100）：一番高い地域を100とした、相対的な値です。検索数ではありません。','Popularity (max=100): a relative value where the top region is 100. Not a search volume.')],
 [('人気度の高い地域を、上位5つ挙げてください。','List the top 5 regions by popularity.'),('人気度が低い地域を、下位5つ挙げてください。','List the bottom 5 regions.'),('地域のかたよりを、数字で短くまとめてください。','Briefly sum up, with numbers, how the regions are skewed.')],
 ('最後に、表（地域／人気度）をつけてください。','Finish with a table (region / popularity).'))
trend('C32','検索する人の特徴を読み解く手伝いをするアシスタント','an assistant who helps read who is searching','その言葉を検索している人が、どんな年齢・性別かを知りたい人です。','a person who wants to know the age and gender of people searching a term.',
 [('年齢層／性別：人の区分です。','Age group / gender: the person groups.'),('値（最大=100）：一番高い区分を100とした、相対的な値です。人数ではありません。','Value (max=100): a relative value where the top group is 100. Not a headcount.')],
 [('年齢層で値が高い順に並べてください。','Order the age groups by value.'),('性別の値を比べて、どちらが高いかを教えてください。','Compare the gender values and tell me which is higher.'),('この言葉で記事を書くときに、読者の年齢や性別をどう考えるか、データの範囲で提案してください。','Suggest how to think about readers\' age and gender when writing about this term, within what the data shows.')],
 ('最後に、表（区分／値）をつけてください。','Finish with a table (group / value).'),)
S['C33']=dict(who=('国別の検索数を読み解く手伝いをするアシスタント','an assistant who helps read searches by country'),reader=('この言葉が、海外でも検索されているかを知りたい人です。','a person who wants to know whether this term is also searched abroad.'),
 cols=[('国（ISOコード）：国の2文字コードです（JP＝日本）。','Country (ISO code): the 2-letter code (JP = Japan).'),('検索数／割合（％）：その国の検索数の推計と、全体に対する割合です。','Searches / share (%): the estimated searches in that country and its share of the total.')],
 tasks=[('割合の高い国を、上位5つ挙げてください。','List the top 5 countries by share.'),('日本の割合と、日本以外の割合を比べてください。','Compare Japan\'s share with the rest.'),('海外向けに書くかどうかを考えるときの、注意点を3つ挙げてください。','List 3 points to watch when considering writing for overseas readers.')],
 tail=('最後に、表（国／検索数／割合）をつけてください。','Finish with a table (country / searches / share).'))
def kwtool(tid,who_ja,who_en,reader_ja,reader_en,cols,tasks,tail,cant=None):
    S[tid]=dict(who=(who_ja,who_en),reader=(reader_ja,reader_en),cols=cols,tasks=tasks,tail=tail,cant=cant)
kwtool('C34','サイトに合うキーワードを整理する手伝いをするアシスタント','an assistant who helps organize keywords that fit a site','自分のサイトや競合のサイトに合うキーワードを知りたい人です。','a person who wants keywords that fit their own or a competitor\'s site.',
 ['vol','kd','now'],[('キーワードを、テーマごとに3〜5個のグループに分けてください。','Group the keywords into 3-5 themes.'),('検索数が大きく、難易度が低めのキーワードを5つ挙げて、数字つきで理由を書いてください。','List 5 keywords with large searches and lower difficulty, with reasons and numbers.'),('次に書く記事の候補を3つ、提案してください。','Suggest 3 articles to write next.')],
 ('最後に、表（グループ／キーワード／月間検索数／難易度）をつけてください。','Finish with a table (group / keyword / searches / difficulty).'))
kwtool('C36','関連する長いキーワードを整理する手伝いをするアシスタント','an assistant who helps organize long-tail keywords','1つのキーワードを含む、具体的な言葉（ロングテール）から、記事を選びたい人です。','a person who wants to choose articles from specific terms (long-tail) containing one keyword.',
 ['vol','kd','now'],[('キーワードを、悩みや目的ごとに3〜5個のグループに分けてください。','Group the keywords by worry or purpose into 3-5 groups.'),('検索数は小さくても、書きやすそうな候補を5つ挙げて、理由を数字つきで書いてください。','List 5 candidates that look easy to write even with small searches, with reasons and numbers.'),('タイトル案を3つ作ってください。','Make 3 title ideas.')],
 ('最後に、表（グループ／キーワード／月間検索数／難易度）をつけてください。','Finish with a table (group / keyword / searches / difficulty).'))
kwtool('C37','同じジャンルのキーワードを整理する手伝いをするアシスタント','an assistant who helps organize keywords in the same genre','1つのキーワードの、言い換えや近い言葉を知りたい人です。','a person who wants paraphrases and near terms of one keyword.',
 ['vol','kd','now'],[('言い換え・同じ意味のキーワードを、まとめてください。','Gather paraphrases and keywords with the same meaning.'),('検索数の多い順に5つ挙げてください。','List 5 by search volume.'),('記事の中で、言い換えて使えそうな言葉を3つ提案してください。','Suggest 3 terms that can be used as variations in an article.')],
 ('最後に、表（キーワード／月間検索数／難易度）をつけてください。','Finish with a table (keyword / searches / difficulty).'))
S['C42']=dict(who=('サイトのジャンルを整理する手伝いをするアシスタント','an assistant who helps organize a site\'s categories'),reader=('競合のサイトが、どのジャンルで強いかを知りたい人です。','a person who wants to know which genres a competitor is strong in.'),
 cols=[('カテゴリ：Googleでそのサイトが出ているジャンルです。','Category: the genre the site shows up for in Google.'),('キーワード数：そのジャンルで出ているキーワードの数です。','Keywords: the number of keywords in that genre.'),'etv'],
 tasks=[('推定流入の多いカテゴリを5つ挙げてください。','List the 5 categories with the most estimated traffic.'),('流入がどのカテゴリに集中しているかを、割合で教えてください。','Tell me, as shares, how concentrated the traffic is by category.'),('キーワード数は多いが、流入が小さいカテゴリを挙げてください。','List categories with many keywords but small traffic.')],
 tail=('最後に、表（カテゴリ／キーワード数／推定流入）をつけてください。','Finish with a table (category / keywords / estimated traffic).'))
S['C43']=dict(who=('よく検索されている言葉を整理する手伝いをするアシスタント','an assistant who helps organize widely searched terms'),reader=('どんな言葉がよく検索されているかを、見て回りたい人です。','a person who wants to browse what terms are widely searched.'),
 cols=['vol','now'], tasks=[('言葉を、ジャンルごとに3〜5個のグループに分けてください。','Group the terms into 3-5 genres.'),('検索数の多い順に10個挙げてください。','List 10 by search volume.'),('自分のブログに関係しそうな言葉があれば、挙げてください。','List terms that may relate to my blog, if any.')],
 tail=('最後に、表（ジャンル／キーワード／月間検索数）をつけてください。','Finish with a table (genre / keyword / searches).'),
 cant=('これは、検索数の多い言葉の一覧であって、急に増えている言葉ではありません。データだけからは言えないこと（たとえば、いま話題かどうか）を、短く書いてください。','This is a list of widely searched terms, not terms that are rising fast. Briefly say what cannot be known from the data alone (for example, whether it is trending now).'))
S['C44']=dict(who=('キーワード群で強いサイトを整理する手伝いをするアシスタント','an assistant who helps find sites strong for a set of keywords'),reader=('自分のキーワードで、上位に出ているサイトを知りたい人です。','a person who wants to know which sites rank for their keywords.'),
 cols=[('ドメイン：入力したキーワードで上位に出ているサイトです。','Domain: a site that ranks for the keywords I entered.'),('平均順位：入力したキーワードでの、そのサイトの順位の平均です。','Average position: the site\'s average rank over the keywords I entered.'),'etv'],
 tasks=[('平均順位のよい順に、サイトを5つ挙げてください。','List the 5 sites with the best average position.'),('推定流入が大きいサイトを挙げて、平均順位と比べてください。','List sites with large estimated traffic and compare with their average position.'),('強いライバルとして見るべきサイトを3つ、理由つきで挙げてください。','List 3 sites to watch as strong rivals, with reasons.')],
 tail=('最後に、表（ドメイン／平均順位／推定流入）をつけてください。','Finish with a table (domain / average position / estimated traffic).'))
S['C49']=dict(who=('サイトの規模を読み解く手伝いをするアシスタント','an assistant who helps read the size of a site'),reader=('競合のサイトが、検索からどれくらい訪問を集めていそうかを知りたい人です。','a person who wants to estimate how many visits a competitor gets from search.'),
 cols=['etv',('キーワード数：検索結果に出ているキーワードの数です。','Keywords: the number of keywords shown in the results.'),('順位帯／キーワード数（2つ目の表）：順位の範囲ごとの、キーワードの数です。','Rank band / keywords (second table): the number of keywords per rank range.')],
 tasks=[('推定流入とキーワード数から、サイトの規模を一言で説明してください。','Describe the site\'s size in a sentence using estimated traffic and keywords.'),('順位帯ごとのキーワード数の分かれ方を、割合で教えてください。','Tell me, as shares, how keywords are split across rank bands.'),('1位〜3位のキーワードが全体に占める割合を計算してください。','Calculate the share of rank 1-3 keywords in the total.')],
 tail=('最後に、計算した数字を表にしてください。','Finish with a table of the numbers you calculated.'))
S['C50']=dict(who=('検索結果の入れ替わりを読み解く手伝いをするアシスタント','an assistant who helps read changes in search results'),reader=('あるキーワードの上位のサイトが、時間がたつと変わるかを知りたい人です。','a person who wants to know whether the top sites for a keyword change over time.'),
 cols=[('日付：その検索結果が記録された日です。','Date: the day that result was recorded.'),('順位／ドメイン：その日の順位と、サイトです。','Rank / domain: the rank that day and the site.'),'now'],
 tasks=[('日付ごとに、1位のドメインを並べてください。','List the rank-1 domain for each date.'),('何回も上位に出るドメインを、回数つきで挙げてください。','List domains that appear often at the top, with counts.'),('日付の間で、入れ替わったドメインを挙げてください。','List domains that changed between dates.')],
 tail=('最後に、表（ドメイン／上位に出た回数）をつけてください。','Finish with a table (domain / times in the top).'))
S['C51']=dict(who=('サイトの推定流入の動きを読み解く手伝いをするアシスタント','an assistant who helps read the trend of estimated traffic'),reader=('自分や競合のサイトが、伸びているか、減っているかを知りたい人です。','a person who wants to know whether their own or a competitor\'s site is growing or shrinking.'),
 cols=[('年月：月です。','Year-month: the month.'),'etv',('キーワード数：その月に出ていたキーワードの数です。','Keywords: the number of keywords that month.')],
 tasks=[('最初の3か月と最後の3か月の平均を比べて、増減を％で教えてください。','Compare the average of the first 3 and last 3 months and give the change in %.'),('一番多い月と少ない月を挙げてください。','Name the highest and lowest months.'),('流入とキーワード数が、同じ向きに動いているかを短く書いてください。','Briefly say whether traffic and keywords move in the same direction.')],
 tail=('最後に、表（年月／推定流入／キーワード数）をつけてください。','Finish with a table (year-month / estimated traffic / keywords).'))
S['C52']=dict(who=('2つの記事の重なりを調べる手伝いをするアシスタント','an assistant who helps compare two articles'),reader=('自分の記事と、上位の記事で、どのキーワードがかぶっているかを知りたい人です。','a person who wants to know which keywords overlap between their article and a top article.'),
 cols=[('キーワード：2つのページの両方が出ているキーワードです。','Keyword: a keyword for which both pages show up.'),('1つ目の順位／2つ目の順位：2つのページそれぞれの順位です。','Rank of the 1st / 2nd page: each page\'s rank.'),'vol'],
 tasks=[('2つ目のほうが順位の高いキーワードを、検索数の多い順に5つ挙げてください。','List the 5 keywords (by search volume) where the 2nd page ranks higher.'),('1つ目のほうが高いキーワードを、検索数の多い順に5つ挙げてください。','List the 5 keywords where the 1st page ranks higher.'),('1つ目の記事に足すとよい内容の案を3つ、データの範囲で提案してください。','Suggest 3 ideas to add to the 1st article, within what the data shows.')],
 tail=('最後に、表（キーワード／1つ目の順位／2つ目の順位／月間検索数）をつけてください。','Finish with a table (keyword / rank of 1st / rank of 2nd / searches).'))
S['C53']=dict(who=('複数サイトの規模を比べる手伝いをするアシスタント','an assistant who helps compare the size of several sites'),reader=('候補のサイトの一覧を、検索からの訪問の大きさで比べたい人です。','a person who wants to compare a list of sites by the size of their search visits.'),
 cols=[('ドメイン：入力したサイトです。','Domain: a site I entered.'),'etv'],
 tasks=[('推定流入の多い順に並べてください。','Order them by estimated traffic.'),('上位3サイトが全体に占める割合を計算してください。','Calculate the share of the top 3 sites in the total.'),('推定流入が0または空欄のサイトがあれば、挙げてください。','List sites with zero or blank estimated traffic.')],
 tail=('最後に、表（ドメイン／推定流入／全体に占める割合）をつけてください。','Finish with a table (domain / estimated traffic / share of the total).'))
apply(S)
