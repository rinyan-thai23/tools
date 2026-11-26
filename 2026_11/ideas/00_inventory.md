# 00 棚卸し：記事 × エンドポイント × 使ったデータ × API費用

作成：2026-11-26（読むだけ。APIは使っていない）

## 全体像
- 記事：**50本**（articles/index.json）。API代の合計：記事ごとの表示額の足し算は$9.19だが、同じデータを何本かで使い回しているので**二重に数えている**。実際に使った額は articles/costs.json の `real` の合計 約$4.14（C24 $1.8、C18 $1.0、C74 $0.372、C62 $0.28、C45 $0.252、C08 $0.178、C01 $0.0975、C02 $0.08、C23 $0.0638、C41 $0.0156）＋多言語13か国 $1.35 ※real欄の数字を足したもの（計算値）
- ツール：公開中は tool.json が **62本**。うち記事にしたのは **13ツール**（C01 C02 C08 C18 C19 C20 C21 C23 C24 C41 C45 C62 C74）。C19〜C21は「4つのAI比較」記事のみ
- **まだ記事にしていない：49ツール**（下の表の「未」）

## 1. 記事一覧（50本）

| 記事スラッグ | ツール | エンドポイント | 使ったデータ | API費用(表示額) | 備考 |
|---|---|---|---|---|---|
| c01-blog-top100 | C01 | serp/google/organic/live/advanced | 「ブログ 始め方」上位100件／20キーワードの1ページ目 | $0.0175 | 上位100件を1回 |
| c01-serp-features-20keywords | C01 | serp/google/organic/live/advanced | 「ブログ 始め方」上位100件／20キーワードの1ページ目 | $0.08 | 20語×1回（1回$0.004） |
| c01-three-ways-to-check-rank | C01 | serp/google/organic/live/advanced | 「ブログ 始め方」上位100件／20キーワードの1ページ目 | $0 | 他の記事の実測（10件$0.004、100件$0.0175）を引用 |
| c01-top100-title-stats | C01 | serp/google/organic/live/advanced | 「ブログ 始め方」上位100件／20キーワードの1ページ目 | $0.0175 | 上位100件のデータ（1回）を使用 |
| c02-ai-mode-20-questions | C02 | serp/google/ai_mode/live/advanced | 20の質問（AIモード） | $0.08 | 20回（1回$0.004） |
| c02-ai-mode-api-limits | C02 | serp/google/ai_mode/live/advanced | 20の質問（AIモード） | $0.08 | 20回のデータを使用 |
| c02-ai-mode-cited-domains | C02 | serp/google/ai_mode/live/advanced | 20の質問（AIモード） | $0.08 | 20回のデータを使用 |
| c02-ai-mode-vs-top10 | C02 | serp/google/ai_mode/live/advanced | 20の質問（AIモード） | $0.16 | AIモード20回$0.08＋通常の検索結果20回$0.08 |
| c08-20-keywords-suggest | C08 | serp/google/autocomplete/live/advanced | 20語＋「ブログ あ〜ん」46回＋ChatGPT内部検索ワード23個 | $0.04 | 20語×$0.002 |
| c08-blog-kana-suggest | C08 | serp/google/autocomplete/live/advanced | 20語＋「ブログ あ〜ん」46回＋ChatGPT内部検索ワード23個 | $0.092 | 46回×$0.002 |
| c08-fan-out-vs-suggest | C08 | serp/google/autocomplete/live/advanced | 20語＋「ブログ あ〜ん」46回＋ChatGPT内部検索ワード23個 | $0.046 | 23回×$0.002 |
| c08-suggest-count | C08 | serp/google/autocomplete/live/advanced | 20語＋「ブログ あ〜ん」46回＋ChatGPT内部検索ワード23個 | $0.178 | 89回×$0.002（0件の回も有料） |
| c08-suggest-limits | C08 | serp/google/autocomplete/live/advanced | 20語＋「ブログ あ〜ん」46回＋ChatGPT内部検索ワード23個 | $0.178 | 89回ぶんの実測を使用 |
| c18-40-prompts-references | C18 | ai_optimization/chat_gpt/llm_responses/live | 渋谷ラーメンを10回／40の質問／内部検索ワード | $0.5887 | 40の質問を1回ずつ |
| c18-api-vs-chatgpt-app | C18 | ai_optimization/chat_gpt/llm_responses/live | 渋谷ラーメンを10回／40の質問／内部検索ワード | $0 | 他の記事の実測（50回ぶん、合計$0.8601）を引用 |
| c18-fan-out-queries | C18 | ai_optimization/chat_gpt/llm_responses/live | 渋谷ラーメンを10回／40の質問／内部検索ワード | $0.8601 | 50回ぶん（10回＋40問）のデータを使用 |
| c18-four-ai-compared | C18 | ai_optimization/chat_gpt/llm_responses/live | 渋谷ラーメンを10回／40の質問／内部検索ワード | $0.1399 | 新しく取った15回。ChatGPTの5回は別の記事のデータ |
| c18-ramen-10-times | C18 | ai_optimization/chat_gpt/llm_responses/live | 渋谷ラーメンを10回／40の質問／内部検索ワード | $0.2714 | 同じ質問を10回 |
| c23-ai-monthly-trend | C23 | ai_optimization/ai_keyword_data/keywords_search_volume/live | 538語（C24と同じ語）／上位15語の月別 | $0.1538 | AI質問回数$0.0638＋Google検索数（C24）$0.09 |
| c23-ai-search-volume-538 | C23 | ai_optimization/ai_keyword_data/keywords_search_volume/live | 538語（C24と同じ語）／上位15語の月別 | $0.0638 | 538語を1回 |
| c23-ai-volume-limits | C23 | ai_optimization/ai_keyword_data/keywords_search_volume/live | 538語（C24と同じ語）／上位15語の月別 | $0.0638 | 538語のデータ（1回）を使用 |
| c23-ai-volume-nonzero-words | C23 | ai_optimization/ai_keyword_data/keywords_search_volume/live | 538語（C24と同じ語）／上位15語の月別 | $0.0638 | 538語のデータ（1回）を使用 |
| c23-ai-vs-google-volume | C23 | ai_optimization/ai_keyword_data/keywords_search_volume/live | 538語（C24と同じ語）／上位15語の月別 | $0.1538 | AI質問回数$0.0638＋Google検索数（C24）$0.09 |
| c24-1000-keywords-limits | C24 | keywords_data/google_ads/search_volume/live | SEOツール系538語・1,200語・10語・13か国 | $0.18 | 1,200語を2回に分けて調べた。4語・538語の各$0.09は別の実測 |
| c24-empty-volume-keywords | C24 | keywords_data/google_ads/search_volume/live | SEOツール系538語・1,200語・10語・13か国 | $0.09 | 538語のデータ（1回）を使用 |
| c24-how-to-read-table | C24 | keywords_data/google_ads/search_volume/live | SEOツール系538語・1,200語・10語・13か国 | $0 | ツールの無料サンプルの1行を使用（追加のAPI代なし） |
| c24-keyword-volume-538 | C24 | keywords_data/google_ads/search_volume/live | SEOツール系538語・1,200語・10語・13か国 | $0.09 | 538語を1回の呼び出しで調べた |
| c24-vs-keyword-planner | C24 | keywords_data/google_ads/search_volume/live | SEOツール系538語・1,200語・10語・13か国 | $0.18 | C24を同じ10語で2回（スペースの有無の確認を含む）。キーワードプランナーは無料 |
| c41-30-keywords-monthly | C41 | dataforseo_labs/google/historical_keyword_data/live | 季節20語＋一定10語＝30語×5年分 | $0.0156 | 30語を1回 |
| c41-flat-keywords-jan-vs-apr | C41 | dataforseo_labs/google/historical_keyword_data/live | 季節20語＋一定10語＝30語×5年分 | $0.0156 | 30語のデータ（1回）を使用 |
| c41-monthly-volume-limits | C41 | dataforseo_labs/google/historical_keyword_data/live | 季節20語＋一定10語＝30語×5年分 | $0.0156 | 30語のデータ（1回）を使用 |
| c41-peak-months | C41 | dataforseo_labs/google/historical_keyword_data/live | 季節20語＋一定10語＝30語×5年分 | $0.0156 | 30語のデータ（1回）を使用 |
| c41-seasonal-vs-flat | C41 | dataforseo_labs/google/historical_keyword_data/live | 季節20語＋一定10語＝30語×5年分 | $0.0156 | 30語のデータ（1回）を使用 |
| c45-10-sites-top100 | C45 | dataforseo_labs/google/ranked_keywords/live | 日本の情報サイト11個（xserver, conoha, onamae, note, hatenablog, ferret-plus 他）×上位100件 | $0.252 | 11サイト×1回（1サイト$0.024、0件だった1サイトは$0.012） |
| c45-competitor-keywords-limits | C45 | dataforseo_labs/google/ranked_keywords/live | 日本の情報サイト11個（xserver, conoha, onamae, note, hatenablog, ferret-plus 他）×上位100件 | $0.252 | 10サイト×100件のデータ（11回）を使用 |
| c45-rank1-keywords | C45 | dataforseo_labs/google/ranked_keywords/live | 日本の情報サイト11個（xserver, conoha, onamae, note, hatenablog, ferret-plus 他）×上位100件 | $0.252 | 10サイト×100件のデータ（11回）を使用 |
| c45-shared-keywords | C45 | dataforseo_labs/google/ranked_keywords/live | 日本の情報サイト11個（xserver, conoha, onamae, note, hatenablog, ferret-plus 他）×上位100件 | $0.252 | 10サイト×100件のデータ（11回）を使用 |
| c45-volume-vs-rank | C45 | dataforseo_labs/google/ranked_keywords/live | 日本の情報サイト11個（xserver, conoha, onamae, note, hatenablog, ferret-plus 他）×上位100件 | $0.252 | 10サイト×100件のデータ（11回）を使用 |
| c62-30-sites-lighthouse | C62 | on_page/lighthouse/live/json | 日本の人気サイト30個（測れた27）／3URL×3回／10サイトのトップvs記事 | $0.135 | 30サイトを測った費用（成功27回×$0.005。エラーは無料） |
| c62-lighthouse-limits | C62 | on_page/lighthouse/live/json | 日本の人気サイト30個（測れた27）／3URL×3回／10サイトのトップvs記事 | $0.28 | 59回ぶん（成功56回×$0.005）の実測を使用 |
| c62-repeat-3-times | C62 | on_page/lighthouse/live/json | 日本の人気サイト30個（測れた27）／3URL×3回／10サイトのトップvs記事 | $0.045 | 3URL×3回（9回×$0.005） |
| c62-score-spread | C62 | on_page/lighthouse/live/json | 日本の人気サイト30個（測れた27）／3URL×3回／10サイトのトップvs記事 | $0.135 | 30サイトのデータを使用 |
| c62-top-vs-article | C62 | on_page/lighthouse/live/json | 日本の人気サイト30個（測れた27）／3URL×3回／10サイトのトップvs記事 | $0.1 | 20回×$0.005 |
| c74-analytics-ad-tags | C74 | domain_analytics/technologies/domain_technologies/live | 日本の人気サイト39個（取れた25） | $0.372 | 39サイトのデータを使用 |
| c74-sites-technologies | C74 | domain_analytics/technologies/domain_technologies/live | 日本の人気サイト39個（取れた25） | $0.372 | 39サイトを調べた費用（1サイト$0.012。エラーは無料、結果が空の回は有料） |
| c74-technology-by-genre | C74 | domain_analytics/technologies/domain_technologies/live | 日本の人気サイト39個（取れた25） | $0.372 | 39サイトのデータを使用 |
| c74-technology-lookup-limits | C74 | domain_analytics/technologies/domain_technologies/live | 日本の人気サイト39個（取れた25） | $0.372 | 39サイトのデータを使用 |
| c74-wordpress-count | C74 | domain_analytics/technologies/domain_technologies/live | 日本の人気サイト39個（取れた25） | $0.372 | 39サイトのデータを使用 |
| c24-13countries-search-volume | C24 | keywords_data/google_ads/search_volume/live | SEOツール系538語・1,200語・10語・13か国 | $1.35 | 13か国＋英語キーワード2回＝成功15回（1回$0.09）。同時アクセス制限の失敗1回は$0 |
| c24-overseas-research-lessons | C24 | keywords_data/google_ads/search_volume/live | SEOツール系538語・1,200語・10語・13か国 | $0 | 13か国の記事のデータを使用（追加のAPI代なし） |

※ c18-four-ai-compared は C18・C19・C20・C21 の4つを使用。

## 2. エンドポイント一覧（全ツール）と記事の有無

| ID | エンドポイント | 単価（tools_simple.tsv / tool.json） | 記事 |
|---|---|---|---|
| C01 | serp/google/organic/live/advanced | $0.004 | 済 4本 |
| C02 | serp/google/ai_mode/live/advanced | $0.004 | 済 4本 |
| C03 | serp/google/maps/live/advanced | $0.002（100件まで） | 未 |
| C04 | serp/google/local_finder/live/advanced | $0.002 | 未 |
| C05 | serp/google/news/live/advanced | $0.002 | 未 |
| C07 | serp/google/images/live/advanced | $0.002（100件まで） | 未 |
| C08 | serp/google/autocomplete/live/advanced | $0.002 | 済 5本 |
| C09 | serp/google/dataset_search/live/advanced | $0.002（20件） | 未 |
| C10 | serp/google/ads_advertisers/live/advanced | $0.002 | 未 |
| C11 | serp/google/ads_search/live/advanced | $0.002（40件） | 未 |
| C14 | serp/youtube/organic/live/advanced | $0.002（20件） | 未 |
| C15 | serp/youtube/video_info/live/advanced | $0.006 | 未 |
| C16 | serp/youtube/video_comments/live/advanced | $0.002（20件ごと）。100件で$0.01 | 未 |
| C17 | serp/youtube/video_subtitles/live/advanced | $0.006 | 未 |
| C18 | ai_optimization/chat_gpt/llm_responses/live | 約$0.03（実測$0.027。gpt-4o-mini・Web検索あり。TSV旧：$0.0006＋モデル料金） | 済 5本 |
| C19 | ai_optimization/claude/llm_responses/live | 約$0.002（実測$0.0022。claude-haiku-4-5・Web検索なし） | 済(4AI比較) |
| C20 | ai_optimization/gemini/llm_responses/live | 約$0.016〜0.06（実測。gemini-3.5-flash-lite・Web検索あり） | 済(4AI比較) |
| C21 | ai_optimization/perplexity/llm_responses/live | 約$0.006（実測$0.0059。sonar） | 済(4AI比較) |
| C22 | ai_optimization/chat_gpt/llm_scraper/live/advanced | $0.004 | 未 |
| C23 | ai_optimization/ai_keyword_data/keywords_search_volume/live | $0.0101 | 済 5本 |
| C24 | keywords_data/google_ads/search_volume/live | $0.09（1〜1000語まで同額） | 済 7本 |
| C25 | keywords_data/google_ads/keywords_for_site/live | $0.09 | 未 |
| C26 | keywords_data/google_ads/keywords_for_keywords/live | $0.09 | 未 |
| C29 | keywords_data/google_trends/explore/live | $0.011 | 未 |
| C30 | keywords_data/dataforseo_trends/explore/live | $0.0012 | 未 |
| C31 | keywords_data/dataforseo_trends/subregion_interests/live | $0.0024 | 未 |
| C32 | keywords_data/dataforseo_trends/demography/live | $0.0024 | 未 |
| C33 | keywords_data/clickstream_data/global_search_volume/live | $0.18 | 未 |
| C34 | dataforseo_labs/google/keywords_for_site/live | $0.024（100件） | 未 |
| C35 | dataforseo_labs/google/related_keywords/live | $0.024（100件） | 未 |
| C36 | dataforseo_labs/google/keyword_suggestions/live | $0.024（100件） | 未 |
| C37 | dataforseo_labs/google/keyword_ideas/live | $0.024（100件） | 未 |
| C38 | dataforseo_labs/google/bulk_keyword_difficulty/live | $0.024（100語） | 未 |
| C39 | dataforseo_labs/google/search_intent/live | $0.024（100語） | 未 |
| C40 | dataforseo_labs/google/keyword_overview/live | $0.012 | 未 |
| C41 | dataforseo_labs/google/historical_keyword_data/live | $0.012 | 済 5本 |
| C42 | dataforseo_labs/google/categories_for_domain/live | $0.024（100件） | 未 |
| C43 | dataforseo_labs/google/top_searches/live | $0.024（100件） | 未 |
| C44 | dataforseo_labs/google/serp_competitors/live | $0.024（100件） | 未 |
| C45 | dataforseo_labs/google/ranked_keywords/live | $0.024（100件） | 済 5本 |
| C46 | dataforseo_labs/google/competitors_domain/live | $0.024（100件） | 未 |
| C47 | dataforseo_labs/google/domain_intersection/live | $0.024（100件） | 未 |
| C48 | dataforseo_labs/google/relevant_pages/live | $0.024（100件） | 未 |
| C49 | dataforseo_labs/google/domain_rank_overview/live | $0.012 | 未 |
| C50 | dataforseo_labs/google/historical_serps/live | $0.0007（実測。TSV旧：$0.0014） | 未 |
| C51 | dataforseo_labs/google/historical_rank_overview/live | $0.134（12か月） | 未 |
| C52 | dataforseo_labs/google/page_intersection/live | $0.024（100件） | 未 |
| C53 | dataforseo_labs/google/bulk_traffic_estimation/live | $0.024（100件） | 未 |
| C60 | on_page/instant_pages | $0.00015 | 未 |
| C61 | on_page/content_parsing/live | $0.00015 | 未 |
| C62 | on_page/lighthouse/live/json | $0.005 | 済 5本 |
| C63 | on_page/page_screenshot | $0.0048 | 未 |
| C64 | content_analysis/search/live | $0.028（100件） | 未 |
| C65 | content_analysis/summary/live | $0.028 | 未 |
| C66 | content_analysis/sentiment_analysis/live | $0.028 | 未 |
| C67 | content_analysis/phrase_trends/live | $0.028 | 未 |
| C68 | business_data/business_listings/search/live | $0.048（100件） | 未 |
| C69 | business_data/google/my_business_info/live | $0.0054 | 未 |
| C71 | business_data/google/hotel_searches/live | $0.004 | 未 |
| C74 | domain_analytics/technologies/domain_technologies/live | $0.012 | 済 5本 |
| C75 | domain_analytics/technologies/domains_by_technology/live | $0.024（10件） | 未 |
| C76 | domain_analytics/whois/overview/live | $0.1212 | 未 |

## 3. 読んで分かった「決まりごと」（企画の前提）

- 費用の形：1回の基本 約$0.01＋1件ごと約$0.0001〜（bulk_notes.md）。C24は1,000語まで$0.09で同額。
- 1ツール＝1エンドポイント。表はAPIの値だけ。判定・ランキングは作らない（CLAUDE.md）。
- 日本専用で台湾版・英語版がないもの：C15 C16 C17 C64 C68 C69 C71 C75（zh-TW無し）。C30〜C32は台湾非対応。
- 複数入力型（改行で1件ずつ）：C01 C02 C03 C04 C05 C07 C08 C18〜C22 C60 C61 C62 C74 C76。
- 記事の型：「【実測】〜を全部載せる」＋「わかること・わからないこと」＋API代の明記。
- 既にある実データ（再取得せず使える）：2026_11/articles/data/（C01 20語＋ブログ100件、C02、C08、C18、C23、C24、C41、C45、C62、C74）。
- ツール未作成（TSVにあるが tool.json なし）：C06 C54〜C59 C70 C72 C73 C77〜C88。企画に使うなら、まずツール担当に作成依頼が必要。
