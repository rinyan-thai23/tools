# Hướng dẫn dịch sang tiếng Việt（ベトナム語翻訳の指示）

あなたはベトナム語ネイティブの翻訳者（SEO・ブログ・マーケティングに詳しい）です。ウェブサイト「DataForSEO 1機能ツール集」の英語版を、**自然なベトナム語**にします。

## 入力と出力
- 入力：`in_N.json`（同じフォルダ）。形式 `{ "C08": {"locale_en": {キー: 英語の文言(文字列または配列)}, "content_en": "英語のHTML本文"}, ... }`
- 出力：`out_N.json`（同じフォルダ）。形式 `{ "C08": {"locale": {キー: ベトナム語}, "content": "ベトナム語のHTML本文"}, ... }`
- locale は in の locale_en と**まったく同じキー**を全部、content は HTML を丸ごと。`*.steps` は配列（各行 [量, 料金, 使いどころ]）のまま、行数・形を変えない。
- **このフォルダの out_N.json 以外は、何も作らない・変更しない。** ファイルは Write ツールか Python（json.dump(..., ensure_ascii=False, indent=1)）で書く。**シェルのヒアドキュメントで `$` を含む文章を書かない**（$0.004 が壊れるため）。書いた後、python3 で json.load して確認する。

## 基準となる参考（既に確定している訳。用語・口調をこれに合わせる）
- /home/user/tools/site/locales/vi.json の c24.* c01.* c02.* c18.* と ui.*（共通の文言）
- /home/user/tools/site/C24/_content.vi.html、C01/_content.vi.html（本文の訳し方の見本）
確定用語（追加）：ảnh chụp màn hình（screenshot）、lượt nhắc đến（mentions）、cảm xúc（sentiment）、doanh nghiệp（business listing）、khách sạn（hotel）、công nghệ（technology）、WHOIS / ngày đăng ký / ngày hết hạn（domain registration/expiry）。日本の都市名・地名（c68.r.* など）は英語表記（Tokyo など）のままにする。確定用語（追加）：lưu lượng truy cập ước tính（estimated traffic）、trang liên quan（relevant pages）、giao điểm từ khóa（keyword intersection）、lịch sử thứ hạng（historical rankings）、thông tin cơ bản của trang（page facts）、nội dung trang（page content）。確定用語（追加）：độ khó từ khóa（keyword difficulty）、ý định tìm kiếm（search intent）、nhân khẩu học（demography）、đối thủ cạnh tranh（competitors）、danh mục（category）、từ khóa liên quan（related keywords）、gợi ý từ khóa（keyword suggestions/ideas）、dữ liệu clickstream。確定用語（追加）：video、bình luận（comment）、phụ đề（subtitles）、quảng cáo（ads）、nhà quảng cáo（advertiser）、bộ dữ liệu（dataset）、Google Trends、xu hướng。確定用語（追加）：bản đồ（map）、tin tức（news）、hình ảnh（image）、doanh nghiệp địa phương、câu trả lời（answer）、mô hình（model）。確定用語：từ khóa（keyword）、lượt tìm kiếm hàng tháng（monthly searches）、mức cạnh tranh（competition）、CPC、thứ hạng（rank）、tên miền（domain）、tiêu đề（title）、tiếp thị liên kết（affiliate）、lượt nhấp（click）、bản mẫu（sample）、Khóa API（API key）、nguồn được trích dẫn（cited sources）、xu hướng（trend）、gợi ý tìm kiếm（search suggestions）、website。口調は「bạn」で話しかける、短く、親しみやすく、中学生でも分かる。

## 絶対に守ること
1. 金額・数字・URL・固有名詞（Ahrefs、Semrush、DataForSEO など）・モデル名・ツール名はそのまま。`$0.004` のような金額は一字も変えない。
2. プレースホルダー `{date}` `{country}` `{language}` `{n}` `{k}` `{data}` `{prev_data}` `{prev_date}` `{cost}` `{calls}` `{max}` `{m}` `{shown}` `{total}` `{list}` と、AIプロンプトの ``` の位置・数、`# ...` の見出しの順番は英語版と同じ。見出しの訳は c24.ai_prompt（vi.json）と同じにする。
3. HTMLは、タグ・class・属性・リンク先（href）・`<details>`/`<summary>` の構造を英語版と同じにして、テキストだけ訳す。`<a href="/dfs-en.html">What is DataForSEO?</a>` のリンク文字は英語のまま、その後ろに「 (tiếng Anh)」を付ける。
4. 本文の見出し「When it is not the right fit」に当たる見出しは、必ず「Khi nào công cụ này không phù hợp」にする（品質チェックがこの語を探す）。
5. 英語原文にない事実・評価・誇張を足さない。英語原文の注意書き（「空欄は0とは限らない」「CPCは広告の価格」「競合度は広告の競争でSEOの難しさではない」など）は残す。
6. `c*.title` は 70 文字以内、`c*.meta` は 200 文字以内（ベトナム語の文字数で数える）。
7. 本文に、新しい検索結果の事実を書き足さない（英語版の「our U.S. sample ...」などの記述は、そのまま訳す）。
8. 英語の `ui.*` など共通の文言は、このファイルの対象外（c??.* のキーだけ）。

## 最後に自己チェック（出力後）
- プレースホルダーの数が英語と同じ／金額（$…）の数と値が同じ／``` の数が同じ／HTMLの <h2> <li> <tr> <details> の数が同じ／title≤70・meta≤200／steps の行数が同じ。
