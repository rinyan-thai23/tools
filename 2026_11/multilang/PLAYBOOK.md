# 多言語展開の手順書（ベトナム語で確立した方法）

## 現状（2026-11-28）
- 公開中：ja（既定）、en、zh-TW（51ツール）、**vi（全62ツール＋トップページSEO整備済み）**。
- 市場調査：2026_11/multilang/README.md、research_memo.md、記事 /articles/c24-13countries-search-volume/ と c24-overseas-research-lessons。
- 調査の結論：ベトナムは月ごとの数字が不安定（平均と最新月が大きく違う）。インドネシアは「SEOツール」が英語で検索される。フィリピン・インドは英語版で足りる。ベンガル語・ウルドゥー語は需要がほぼ無い。SEO需要はAIでここ1年に急減している（運営者の見立て）。次の言語は、再調査（約$0.2）と運営者の判断で決める。**言語を決めるのは運営者**。
- ベトナム語は、AIによる校閲まで。**現地の人の確認は未実施**。

## 新しい言語を足す手順
### A. 土台（1回だけ）
1. `scripts/langs.json` に `{"code":"xx","label":"自国語の名前","partial":true}`。
2. `site/locales/xx.json`：共通の文言97個（`ui.*` `err.*` `key.*` `who.*` `site.*`）。英語版 site/locales/en.json と同じキー。ベトナム語版（vi.json）を見本にする。
3. `site/shared/markets.json`：全国・全言語に `xx` の名前を足し、その言語の国と言語を `"only":["xx"]` で足す。`defaults.xx` も。
4. `scripts/partials/header.xx.html` `footer.xx.html`（説明ページ・依頼・運営者ページは英語版へリンクして「(英語)」と書く）。
5. `scripts/build-worker.mjs` の `noteText`、`site/shared/ui.js` の紹介リンク注記、`scripts/check-tools.mjs` の「向いていない場面」見出しの正規表現（その言語の見出し語を足す）。
6. 最初は1ツール（C24）だけで通す：画面・本文・AIプロンプト・サンプル。検査 → 校閲 → 公開。それから広げる。

### B. 10ツールずつ広げる（ベトナム語は 1+3+8+10+10+10+10+10 と進めた）
1. **サンプル取得（最低料金・3件まで）**：ツールごとに、その国・その言語の語で1回ずつ。Labsは `limit:3`。tool.json の params（日本固定の設定など）を実際のツールと同じにする。`site/Cxx/sample.<lang>.json` に `{"keyword"|"inputs", "fetched_at", "tasks":[{cost,time,result}]}` で保存し、tool.json の `sample_langs` に言語を足す。生データは 2026_11/multilang/<lang>_samples/ に残す。
   - 品質チェックが「列が全部空」と言ったら、別の語で取り直す（空振りは料金が出る場合と0の場合がある）。日本固定で意味が無いもの（C64/C68/C69/C71/C75）は、sample.json（日本語サンプル）のままにする（英語版と同じ）。高額なもの（C51 $0.136、C33 $0.18）は英語版サンプルをコピー。
2. **翻訳をサブエージェントに任せる**：1ツール2本ずつ、5人並行。入力 `in_N.json`（`{ "C08": {"locale_en": {キー: 英語}, "content_en": "英語HTML"} }`）、出力 `out_N.json`（`{ "C08": {"locale": {...}, "content": "..."} }`）。指示書は `pipeline/translate_instructions_vi.md`（用語集・守ること）をその言語用に作り直す。
3. **機械検査してから取り込む**：`pipeline/merge_lang.py <フォルダ> [--write]`（プレースホルダー・金額・``` ・HTMLタグ数・リンク・title≤70・meta≤200・stepsの形）。問題があれば書き込まない。桁区切り・小数点をその言語の書き方に揃える。
4. `node scripts/build-worker.mjs` → `npm run check`（62/62）→ `node scripts/smoke.mjs <ids>`。
5. **校閲サブエージェント1人**：10ツールをまとめて。修正箇所だけを JSON（`{"locale":{},"content":[{"file","old","new"}],"notes"}`）で出させ、**厳格に適用**（1か所でも一致しなければ止まる）。
6. 再ビルド・全検査 → `CLOUDFLARE_ACCOUNT_ID=04b402248ae5c56d6d24177a0f812040 CLOUDFLARE_API_TOKEN=proxy-injected npm run deploy` → URLが200か確認 → `2026_11/USAGE.tsv` に費用を追記 → コミット・push（他のセッションも push するので `git pull --rebase origin main`）。

### C. トップページ（全ツール後）
`scripts/index-categories.json` と `index-descriptions.json` に言語キーを足す（機能別10ジャンル＋62ツールの説明）。`site.index_title`（70字以内）、`site.index_meta`（160字以内）、`site.title`（H1）はSEOを意識して書く。翻訳3人（機能別紹介／説明31個×2）＋校閲1人。見本はベトナム語。`pipeline/toppage_instructions_vi.md`。

## 失敗から学んだこと（必ず守る）
- **シェルのヒアドキュメントに `$0.09` を書くと壊れる**（`/bin/bash.09` になる）。必ず `<<'EOF'`（引用符つき）か、Writeツール／Pythonで書く。検査で金額の一致を確認する（merge_lang.py が見る）。
- **反映スクリプトがエラーを出したら、そこで止める**（公開まで進めない）。`&&` でつなぐ。
- サブエージェントの指示書には、「このフォルダの out_N.json 以外を作らない」「`$` を含む文をヒアドキュメントで書かない」を必ず入れる。
- 校閲は「AIによる確認」で、現地の人の確認ではない。公開時に正直に伝える。
- 費用は透明に。サンプルは最低料金。空振りは記録する。
- 返信は日本語、短く、中学生でも分かる語り口、たとえ話つき。運営者の哲学は「誰のために、なぜ喜ばれるか」（whoを起点）。
- Stop hook が「未コミットがある」と言ったらコミット・push（mainへ。PRは作らない。コミットメッセージ末尾に Co-Authored-By と Claude-Session の2行）。

## 英語版の国（2026-11-28）
- 英語の画面では、国を選べる。インドネシア・フィリピン・インド・タイ・シンガポール・マレーシア・NZ・アイルランド・南アフリカ・UAE・ナイジェリア・パキスタンを追加（`markets.json` の `only:["en"]`）。
- 確認は無料の一覧（各 locations / locations_and_languages）。Labsとai_keyword_dataは、国ごとに対応言語が違う（タイは英語なし）→ `not_for`（エンドポイントの先頭）で外す。台湾もLabsは繁体字のみ（未対応のまま。要修正）。
- **言語（運営者の指摘）**：英語画面で国だけ足しても、現地語の検索（最大のデータ）が取れない。→ 国ごとに `langs`（選べる言語）を持たせ、現地語（th id hi tl ms ur ar）を `country_only` で足した。タイは th が先頭、Labs/AI系は en 非対応のため `not_lang_for` で外す。
- 実測：C08で ID PH IN TH とも英語で動いた（$0.008）。

## 次にやること（候補）
1. 次の言語の決定（運営者）。候補の調査データは README.md と記事を参照。再調査する場合は research_memo.md の方法（約$0.09/国）。
2. 英語版の強化（インドネシア・フィリピン・インド・タイ向けの案内。英語キーワードが多く検索されているため）。
3. 紹介ページ（「DataForSEOとは？」「運営者について」）の多言語化（いまは英語ページへのリンク）。
4. vi の現地の人の確認を得る方法（読者の反応、SNS など）。
