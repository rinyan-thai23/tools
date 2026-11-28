# 多言語展開の手順書（ベトナム語で確立した方法）

## 現状（2026-11-28）
- 公開中：ja（既定）、en、zh-TW（51ツール）、**vi（全62ツール＋トップページSEO整備済み）**、**id（C24 C01 C02 C18 C08 C23 C35 C40 C41 C45 C62 C74 C03 C04 C05 C07 C19 C20 C21 C22 C25 C26 C09 C10 C11 C14 C15 C16 C17 C29 C30 C31 C32 C33 C34 C36 C37 C38 C39 C42 C43 C44＝42本。2026-11-28。1+3+8+10+10+10の順で、ベトナム語と同じ手順。現地確認はしない方針）**。
- 2026-11-28 再調査（fr pt id th tr、各約40語、$0.45）：raw2_*.json。ツール名ではなくブランド名（semrush・ahrefs）で探される。インドネシアだけ現地語（SEO代行・ブログの作り方）が増加中 → idを試作。
- 市場調査：2026_11/multilang/README.md、research_memo.md、記事 /articles/c24-13countries-search-volume/ と c24-overseas-research-lessons。
- 調査の結論：ベトナムは月ごとの数字が不安定（平均と最新月が大きく違う）。インドネシアは「SEOツール」が英語で検索される。フィリピン・インドは英語版で足りる。ベンガル語・ウルドゥー語は需要がほぼ無い。SEO需要はAIでここ1年に急減している（運営者の見立て）。次の言語は、再調査（約$0.2）と運営者の判断で決める。**言語を決めるのは運営者**。
- ベトナム語は、AIによる校閲まで。**現地の人の確認は未実施**。

## インドネシア語（id）の足し方メモ（実績）
- 土台：`langs.json`、`markets.json` の defaults（国・言語は `markets.generated.json` が自動なので、名前の翻訳は不要）、partials 2本、`noteText`、`ui.js` の紹介リンク注記、`check-tools.mjs` の見出し語（kurang cocok）。**英語版の4項目（国・言語の名前）はもう要らない。**
- サンプルは、再調査の生データ（raw2_id）から3語を流用（$0）。
- 次：idの校閲（サブエージェント1人）、現地確認、需要を見て広げるか決める。

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

## 国・言語の選択欄（2026-11-28に作り直し。共通パーツ）
- 一覧は無料のエンドポイントから作る：`node scripts/gen-markets.mjs`（$0、ときどき1回）→ `site/shared/markets.generated.json`。**国と言語は全部選べる**（SERP 240国・129言語、Google広告 244国・46言語など。APIの系統ごとに違う）。
- 名前は `Intl.DisplayNames`（ブラウザ）で、ISOコード／言語コードから画面の言語で作る。**新しい言語を足しても、国と言語の名前は訳さなくてよい**。
- 初期値は「画面の言語の国と言語」だけ（`site/shared/markets.json` の `defaults`。新しい言語を足すときは、ここに1行）。
- Labs系・AIキーワード系だけは、国ごとに言語が決まっている（日本は ja のみ、タイは th のみ）。国を変えると言語の一覧も変わる。
- 系統の判定は `ui.js` の `FAM`（エンドポイントの先頭）。手書きの国リスト（`country_codes`・`only`・`not_for` など）は廃止。
- 実測：SERPは国と言語の組み合わせが自由（タイ×ja、日本×th、米国×ar とも通った。C08で$0.006）。英語版のタイ・インドネシア・フィリピン・インドの英語も通った（$0.008）。

## 次にやること（候補）
1. 次の言語の決定（運営者）。候補の調査データは README.md と記事を参照。再調査する場合は research_memo.md の方法（約$0.09/国）。
2. 英語版の強化（インドネシア・フィリピン・インド・タイ向けの案内。英語キーワードが多く検索されているため）。
3. 紹介ページ（「DataForSEOとは？」「運営者について」）の多言語化（いまは英語ページへのリンク）。
4. vi の現地の人の確認を得る方法（読者の反応、SNS など）。
