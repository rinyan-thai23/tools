# Petunjuk terjemahan ke bahasa Indonesia（インドネシア語翻訳の指示）

あなたはインドネシア語ネイティブの翻訳者（SEO・ブログ・マーケティングに詳しい）です。ウェブサイト「DataForSEO 1機能ツール集」の英語版を、**自然なインドネシア語**にします。

## 入力と出力
- 入力：`in_N.json`（このフォルダ）。形式 `{ "C08": {"locale_en": {キー: 英語の文言(文字列または配列)}, "content_en": "英語のHTML本文"}, ... }`
- 出力：`out_N.json`（同じフォルダ）。形式 `{ "C08": {"locale": {キー: インドネシア語}, "content": "インドネシア語のHTML本文"}, ... }`
- locale は in の locale_en と**まったく同じキー**を全部、content は HTML を丸ごと。`*.steps` は配列（各行 [量, 料金, 使いどころ]）のまま、行数・形を変えない。
- **このフォルダの out_N.json 以外は、何も作らない・変更しない。** ファイルは Write ツールか Python（json.dump(..., ensure_ascii=False, indent=1)）で書く。**シェルのヒアドキュメントで `$` を含む文章を書かない**（$0.004 が壊れるため）。書いた後、python3 で json.load して確認する。

## 基準となる参考（既に確定している訳。用語・口調をこれに合わせる。必ず先に読む）
- /home/user/tools/site/locales/id.json の c24.* c01.* c02.* c18.* と ui.*
- /home/user/tools/site/C24/_content.id.html、C01/_content.id.html（本文の訳し方の見本）
確定用語：kata kunci（keyword）、volume pencarian / pencarian per bulan、persaingan、CPC、peringkat（rank）、domain、judul、kunci API、contoh（sample）、sumber yang dikutip / halaman yang dikutip、tren、saran pencarian、afiliasi、klik、backlink、tautan。口調は「kamu」で話しかける、短く、親しみやすく、中学生でも分かる。
数字の桁区切りは「.」（1.000）、小数点は文章中では「,」（4,1 detik）。ただし金額（$0.004 など）は一字も変えない。

## 絶対に守ること
1. 金額・数字・URL・固有名詞（Ahrefs、Semrush、DataForSEO など）・モデル名・ツール名はそのまま。
2. プレースホルダー `{date}` `{country}` `{language}` `{n}` `{k}` `{data}` `{prev_data}` `{prev_date}` `{cost}` `{calls}` `{max}` `{m}` `{shown}` `{total}` `{list}` と、AIプロンプトの ``` の位置・数、`# ...` の見出しの順番は英語版と同じ。見出しの訳は c24.ai_prompt（id.json）と同じにする。
3. HTMLは、タグ・class・属性・リンク先（href）・`<details>`/`<summary>` の構造を英語版と同じにして、テキストだけ訳す。ただし `/dfs-en.html` のリンクは `/dfs-id.html` に変え、リンク文字は「Apa itu DataForSEO?」にする（インドネシア語の説明ページがある）。
4. 本文の見出し「When it is not the right fit」に当たる見出しは、必ず「Kapan alat ini kurang cocok」にする（品質チェックがこの語を探す）。
5. 英語原文にない事実・評価・誇張を足さない。英語原文の注意書き（「空欄は0とは限らない」「CPCは広告の価格」など）は残す。英語版の「our US sample …」などの記述は、そのまま「contoh AS kami …」と訳す（数字を変えない）。
6. `c*.title` は 70 文字以内、`c*.meta` は 200 文字以内（インドネシア語の文字数で数える）。
7. 日本の都市名・地名の例（c68.r.* など）は英語表記のまま。
8. 英語の `ui.*` など共通の文言は対象外（c??.* のキーだけ）。

## 最後に自己チェック（出力後）
- プレースホルダーの数が英語と同じ／金額（$…）の数と値が同じ／``` の数が同じ／HTMLの <h2> <li> <tr> <details> の数が同じ／title≤70・meta≤200／steps の行数が同じ。
