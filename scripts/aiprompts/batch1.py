import sys; sys.path.insert(0,'/home/user/tools/scripts/aiprompts')
from lib import *
S={}
S['C02']=dict(answer=True,who=('GoogleのAIモードの答えを読み解く手伝いをするアシスタント','Google AI Mode answers'),reader=('自分のサイトが、AIモードの答えに引用されるかを調べたい人です。','a person who wants to see whether their site is cited in Google AI Mode answers.'),
 cols=[('タイトル／URL：AIモードの答えが引用したページです。','Title / URL: the pages the AI Mode answer cited.'),'ai'],
 extra=[('引用元が1件も返らない質問もあります。','Some questions return no sources at all.')],
 tasks=[('答えの文章の内容を、3行で要約してください。','Summarize the answer in 3 lines.'),('引用元のドメインを数えて、何回出たかを教えてください。','Count the cited domains and tell me how many times each appears.'),('自分のサイトが引用されているかを確認するときに、見るべき点を3つ挙げてください。','List 3 points to check when seeing whether my site is cited.')],
 tail=('最後に、表（ドメイン／出た回数）をつけてください。','Finish with a table (domain / count).'))
S['C03']=dict(who=('お店の地図での順位を整理する手伝いをするアシスタント','an assistant who helps organize map rankings of shops'),reader=('お店（またはお店の集客を手伝う人）で、「地図で上位に出ているお店はどこか」を知りたい人です。','a shop owner (or someone helping a shop) who wants to know which shops show at the top of the map.'),
 cols=[('順位：地図の検索結果での順位です。','Rank: the position in the map results.'),('評価／口コミ数：地図に出ている星の評価と、口コミの数です。','Rating / reviews: the star rating and the number of reviews shown on the map.'),('住所・電話・サイト：地図に出ているお店の情報です。','Address, phone, site: the shop info shown on the map.'),'now'],
 tasks=[('上位5店の、評価と口コミ数を並べて、特徴を短くまとめてください。','Line up the rating and review count of the top 5 shops and briefly sum up what they have in common.'),('口コミ数が多い店と少ない店の違いを、数字で教えてください。','Tell me, with numbers, how shops with many reviews differ from those with few.'),('自分の店を上位に出すために、確認できることを3つ挙げてください（データから言える範囲で）。','List 3 things I can check to get my shop to show higher (only as far as the data allows).')],
 tail=('最後に、表（店名／順位／評価／口コミ数）をつけてください。','Finish with a table (shop / rank / rating / reviews).'))
S['C04']=dict(who=('地図の「もっと見る」一覧を整理する手伝いをするアシスタント','an assistant who helps organize the map "more places" list'),reader=('地図の上位3店のあとに出る店まで含めて、競合を知りたいお店の人です。','a shop person who wants to know competitors, including shops listed after the top 3 on the map.'),
 cols=[('順位：「もっと見る」の一覧での順位です。','Rank: the position in the "more places" list.'),('評価／口コミ数：星の評価と、口コミの数です。','Rating / reviews: the star rating and the number of reviews.'),('説明：地域や営業時間などの短い説明です。','Description: a short note such as area or opening hours.'),'now'],
 tasks=[('評価と口コミ数から、競合になりそうな店を5つ挙げてください。','From rating and review count, list 5 shops that look like competitors.'),('説明（地域・営業時間）に共通する点を、短くまとめてください。','Briefly sum up what the descriptions (area, hours) have in common.'),('自分の店と比べるときに、見るべき点を3つ挙げてください。','List 3 points to check when comparing with my own shop.')],
 tail=('最後に、表（店名／順位／評価／口コミ数）をつけてください。','Finish with a table (shop / rank / rating / reviews).'))
S['C05']=dict(who=('ニュース記事を整理する手伝いをするアシスタント','an assistant who helps organize news articles'),reader=('会社や商品の名前が、ニュースにどう出ているかを知りたい広報・営業の人です。','a PR or sales person who wants to know how a company or product shows up in the news.'),
 cols=[('媒体名／日付／タイトル：記事を出した媒体と、日付、見出しです。','Source / date / title: the outlet, the date and the headline.'),'now'],
 tasks=[('媒体ごとの記事の数を数えてください。','Count the articles per outlet.'),('日付の新しい順に、記事の話題を3〜5個にまとめてください。','Sum up the topics in 3-5 groups, newest date first.'),('タイトルに多く出ている言葉を、数えられる範囲で挙げてください。','List words that appear often in the titles, as far as they can be counted.')],
 tail=('最後に、表（媒体／記事の数）をつけてください。','Finish with a table (outlet / number of articles).'),
 cant=('データだけからは言えないこと（たとえば、記事の評価が良いか悪いか）を、短く書いてください。','Briefly say what cannot be known from the data alone (for example, whether coverage is favorable).'))
S['C07']=dict(who=('画像検索の結果を整理する手伝いをするアシスタント','an assistant who helps organize image search results'),reader=('サムネイルや表紙、ブログの画像を考える前に、画像検索で何が上に出ているかを知りたい人です。','a person who wants to see what shows at the top of image search before designing thumbnails, covers or blog images.'),
 cols=[('画像：検索結果に出た画像（表のコピーには、画像そのものは入りません）。','Image: the image shown in the results (the copied table does not include the image itself).'),('タイトル／掲載ページURL：画像のタイトルと、載っているページです。','Title / page URL: the image title and the page it appears on.'),'now'],
 tasks=[('掲載ページのドメインを数えて、よく出るサイトを挙げてください。','Count the page domains and list the sites that appear often.'),('タイトルに共通する言葉を、数えられる範囲で挙げてください。','List words the titles share, as far as they can be counted.'),('画像そのものは見えないので、「見た目」についての判断はしないでください。','You cannot see the images themselves, so do not judge how they look.')],
 tail=('最後に、表（ドメイン／出た回数）をつけてください。','Finish with a table (domain / count).'))
S['C08']=dict(who=('検索候補（サジェスト）を整理する手伝いをするアシスタント','an assistant who helps organize search suggestions'),reader=('記事のネタや、キーワードの言い換えを探しているブログ初心者です。','a beginner blogger looking for article ideas and keyword variations.'),
 cols=[('サジェスト候補：Googleの検索窓に出る候補です。最大15件で、検索数ではありません。','Suggestion: a candidate shown in the Google search box. Up to 15, not a search volume.'),'now'],
 tasks=[('候補を、テーマごとに3〜5個のグループに分けてください。','Group the suggestions into 3-5 themes.'),('記事のタイトル案を、候補から3つ作ってください。','Make 3 article title ideas from the suggestions.'),('候補の中で、悩みや疑問の形をしているものを挙げてください。','List suggestions that look like worries or questions.')],
 tail=('最後に、表（グループ／候補）をつけてください。','Finish with a table (group / suggestion).'),
 cant=('データだけからは言えないこと（たとえば、どの候補がよく検索されているか）を、短く書いてください。','Briefly say what cannot be known from the data alone (for example, which suggestion is searched the most).'))
S['C09']=dict(who=('公開データを探す手伝いをするアシスタント','an assistant who helps find open data'),reader=('記事や本に引用できる、統計や公開データを探している人です。','a person looking for statistics and open data to cite in articles or books.'),
 cols=[('名称／提供元／更新日／URL：データセットの名前、出している組織、更新日、リンクです。','Name / provider / updated / URL: the dataset name, the publisher, the update date and the link.')],
 tasks=[('引用に使いやすそうなデータセットを5つ選んで、理由を書いてください（提供元と更新日を見て）。','Pick 5 datasets that look easy to cite and give reasons (look at provider and update date).'),('更新日が古いものを挙げて、注意点を書いてください。','List the ones with old update dates and note what to watch for.'),('使う前に確認することを3つ挙げてください（ライセンス、出典の書き方など）。','List 3 things to check before using one (license, how to credit, etc.).')],
 tail=('最後に、表（名称／提供元／更新日）をつけてください。','Finish with a table (name / provider / updated).'),
 cant=('データの中身は見えていないので、データの正しさや使いやすさは判断しないでください。','You cannot see the data itself, so do not judge its accuracy or usability.'))
S['C10']=dict(who=('広告主を調べる手伝いをするアシスタント','an assistant who helps look up advertisers'),reader=('競合の会社が、Google広告を出しているかを知りたい人です。','a person who wants to know whether a competitor runs Google ads.'),
 cols=[('広告主名／広告主ID／国：広告主の名前、ID、登録の国です。','Advertiser / ID / country: the advertiser name, ID and country.'),('広告数（目安）：出ている広告のおおよその数です。','Ads (estimate): the rough number of ads shown.')],
 tasks=[('名前が入力に近い広告主を挙げて、同じ会社かどうかを確認するための点を書いてください。','List advertisers whose names are close to my input and note how to check whether they are the same company.'),('広告数の多い順に並べて、数字を教えてください。','Order them by number of ads and tell me the numbers.'),('次に調べること（広告の中身を見るなど）を3つ挙げてください。','List 3 next things to check (such as looking at the ads themselves).')],
 tail=('最後に、表（広告主名／広告主ID／広告数）をつけてください。','Finish with a table (advertiser / ID / ads).'))
S['C11']=dict(who=('出稿中の広告を整理する手伝いをするアシスタント','an assistant who helps organize running ads'),reader=('競合のサイトが、どんな広告を、いつから出しているかを知りたい人です。','a person who wants to know what ads a competitor runs and since when.'),
 cols=[('形式：広告の形式（文字・画像・動画など）です。','Format: the ad format (text, image, video, etc.).'),('広告主名：広告を出している名前です。','Advertiser: the name running the ad.'),('最初の表示日／最後の表示日：その広告が出ていた期間の、始めと終わりです。','First / last shown: the start and end of the period the ad ran.'),('プレビューは画像・リンクで、表のコピーには入らないことがあります。','The preview is an image or link and may not be included in the copied table.')],
 tasks=[('形式ごとの広告の数を数えてください。','Count the ads per format.'),('表示期間が長い広告と短い広告を挙げて、数字で比べてください。','List long-running and short-running ads and compare them with numbers.'),('広告主名が複数あれば、分けて整理してください。','If there are several advertiser names, organize them separately.')],
 tail=('最後に、表（形式／広告の数）をつけてください。','Finish with a table (format / number of ads).'),
 cant=('データだけからは言えないこと（たとえば、広告の効果）を、短く書いてください。','Briefly say what cannot be known from the data alone (for example, how well the ads work).'))
S['C14']=dict(who=('YouTubeの検索結果を整理する手伝いをするアシスタント','an assistant who helps organize YouTube search results'),reader=('動画を作る前に、「いま上位にどんな動画があるか」を知りたい人です。','a person who wants to know what videos are at the top before making one.'),
 cols=[('順位：YouTube検索での順位です。','Rank: the position in YouTube search.'),('タイトル／チャンネル：動画の題名と、投稿したチャンネルです。','Title / channel: the video title and the channel that posted it.'),('再生数／投稿日／長さ：再生回数、投稿日、動画の長さです。','Views / posted / length: the view count, the post date and the duration.'),'now'],
 tasks=[('上位動画の、再生数・投稿日・長さの傾向を、数字でまとめてください。','Sum up, with numbers, the trend in views, post dates and length among the top videos.'),('同じチャンネルが何回出ているかを数えてください。','Count how many times the same channel appears.'),('タイトルに共通する言葉を、数えられる範囲で挙げてください。','List words the titles share, as far as they can be counted.')],
 tail=('最後に、表（チャンネル／出た回数）をつけてください。','Finish with a table (channel / count).'))
S['C15']=dict(who=('動画の数字を読み解く手伝いをするアシスタント','an assistant who helps read the numbers of a video'),reader=('動画1本の数字から、反応のようすを知りたい人です。','a person who wants to see how viewers reacted, from one video\'s numbers.'),
 cols=[('再生数／高評価数／コメント数：動画の数字です。','Views / likes / comments: the video numbers.'),('投稿日／説明文：投稿日と、動画の説明です。','Posted / description: the post date and the video description.')],
 tasks=[('再生数に対する、高評価とコメントの割合を計算してください。','Calculate likes and comments as a share of views.'),('投稿日から今日までの日数と、1日あたりの再生数を計算してください。','Calculate the days from the post date to today and the views per day.'),('説明文に書かれている内容を、3行で要約してください。','Summarize the description in 3 lines.')],
 tail=('最後に、計算した数字を表にしてください。','Finish with a table of the numbers you calculated.'),
 cant=('データだけからは言えないこと（たとえば、動画の良し悪し）を、短く書いてください。','Briefly say what cannot be known from the data alone (for example, whether the video is good).'))
S['C16']=dict(who=('動画のコメントを整理する手伝いをするアシスタント','an assistant who helps organize video comments'),reader=('動画のコメントから、見ている人の反応や疑問を知りたい人です。','a person who wants to know viewers\' reactions and questions from video comments.'),
 cols=[('コメント：コメントの文章です。','Comment: the comment text.'),('いいね数／返信数／投稿日：コメントの反応と、日付です。','Likes / replies / posted: the reactions to the comment and the date.')],
 tasks=[('コメントを、話題ごとに3〜5個のグループに分けて、それぞれの数を数えてください。','Group the comments into 3-5 topics and count each.'),('質問の形をしているコメントを挙げてください。','List comments that are phrased as questions.'),('いいね数の多いコメントを5つ挙げてください。','List the 5 comments with the most likes.')],
 tail=('最後に、表（話題／コメントの数／例）をつけてください。','Finish with a table (topic / number of comments / example).'),
 cant=('データだけからは言えないこと（たとえば、コメントを書いた人の本当の気持ち）を、短く書いてください。','Briefly say what cannot be known from the data alone (for example, the commenters\' real feelings).'))
S['C17']=dict(who=('動画の字幕を整理する手伝いをするアシスタント','an assistant who helps organize video captions'),reader=('動画の内容を、文章で読んでつかみたい人です。','a person who wants to grasp a video by reading its text.'),
 cols=[('時間：その字幕が出る時刻です。','Time: when the caption appears.'),('字幕：その時刻の字幕の文章です。','Caption: the caption text at that time.')],
 tasks=[('動画の内容を、5行で要約してください。','Summarize the video in 5 lines.'),('話題が変わる場所（時間）を、見出しつきで挙げてください。','List the places (times) where the topic changes, with headings.'),('重要そうな数字や固有名詞を、字幕に書かれているとおりに挙げてください。','List important-looking numbers and names exactly as written in the captions.')],
 tail=('最後に、時間つきの見出しの一覧を表にしてください。','Finish with a table of headings with times.'),
 cant=('字幕の聞き取り間違いがあるかもしれないことを、注意として書いてください。','Note that the captions may contain mis-heard words.'))
apply(S)
