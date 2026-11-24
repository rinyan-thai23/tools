# DataForSEO 1機能ツール集を作る

## このリポジトリは何か

DataForSEOのAPIを1つずつ使った、小さなWebツールの集まり。
ツールの一覧は `tools_simple.tsv`。1行＝1ツール。

コンセプト：**すぐ公開できる・気軽に試せる・エージェントがサクサク作れる**

## 絶対ルール（やらないこと）

1. **APIが返した値を、表にして見せるだけ**。判定・ランキング・分類・色分け・独自リスト・スコアは作らない
2. **TSVの行に書いていないものは作らない**。「あると便利」と思っても足さない。提案したい時は、報告の最後に1行書くだけにする
3. **1ツール＝1エンドポイント**。2つのAPIを組み合わせない
4. **入力欄はTSVの「入力」列のとおり**。増やさない
5. 迷ったら、作り込まずに一番単純な形で作る

## 共通の土台（全ツール同じ）

### APIキー
- ユーザーが画面で入力する（ログインメール＋APIパスワード）
- `localStorage` に保存するだけ。運営者のサーバーには送らない
- 「キーを消す」ボタンを付ける
- `localStorage` の読み書きは try/catch で囲む（使えない環境でも画面が壊れないように）
- 「APIパスワードは、DataForSEOのダッシュボードのAPI Access画面にある。ログイン用のパスワードとは別」と1行書く

### サンプルデータ（ダミー出力）
- 各ツールに `sample.json` を1つ置く
- APIキーがなくても「サンプルを見る」ボタンで、結果の画面をそのまま見せる
- 画面に「これはサンプルです（取得日：◯年◯月）」と必ず出す
- 中身は、DataForSEO公式ドキュメントのレスポンス例か、開発中に1回だけ取った実データを短くしたもの。数字を手で作らない
- 開発もまずサンプルで画面を作り、実APIは最後に1〜2回だけ呼ぶ（料金と時間の節約）

### 国と言語
- 画面に「国」と「言語」の選択欄を置く。初期値は画面の言語に合わせる
  - 日本語の画面 → 日本（2392）・日本語（ja）
  - 英語の画面 → 米国（2840）・英語（en）
- 選べる国と言語の一覧は `shared/markets.json` にまとめる
- そのAPIが国・言語を受け付けない時（URLや動画IDだけで動くもの）は、選択欄を出さない

### 紹介リンク
- URLは `shared/site-config.json` の `referral_url` で一元管理する。各ツールに直書きしない
- キー入力欄の近くに「DataForSEOのアカウントを作る」リンクを出す
- `referral_url` が入っている時は、リンクのすぐ近くに「紹介リンクです」と出す（紹介プログラムの規約で必須）
- 空の時は公式トップへのリンクだけにして、注記は出さない

### 画面の並び
1. ツール名と、1行の説明（TSVの「使う場面」）
2. APIキー欄（設定済みなら折りたたむ）
3. 入力欄と、国・言語の選択欄
4. 「調べる」ボタン ／ 「サンプルを見る」ボタン
5. 結果の表（TSVの「表示する項目」の列だけ）
6. 今回の料金（APIの `cost` をそのまま表示）と取得日時
7. CSVダウンロード（UTF-8・BOM付き）

### 文言
- 画面の文言は全部 `locales/ja.json` と `locales/en.json` から読む。HTMLやJSに直書きしない

### エラー
`shared/api.js` にまとめる。各ツールで書かない。

| コード | 表示 |
|---|---|
| キー未入力 | 先にAPIキーを設定してください |
| 40100 | APIキーが正しくありません |
| 40210 | 残高が足りません。DataForSEOでチャージしてください |
| 40207 | DataForSEO側でIP制限がかかっています。API設定で制限を外してください |
| 40102 | 結果が見つかりませんでした |
| 40101・40103・通信エラー | 自動で最大3回やり直す。だめなら「混み合っています。少し待って試してください」 |

## 1本の作り方

1. `tools_simple.tsv` の該当行を読む
2. 公式ドキュメントでそのエンドポイントの送るデータとレスポンス例を確認する
3. `sample.json` を作り、サンプルで画面を完成させる
4. 実APIを1回だけ呼び、表示とcostを確認する
5. 報告して止まる

報告は次の形だけ：
- できたもの（パス）
- 実APIで使った料金
- 想定外だったこと（なければ「なし」）
- 提案（あれば1行。実装はしない）

## 学んだこと

- Google通常検索（Organic）は `resolve_goto_urls` と `resolve_poisoned_results` を付ける。付けないと、URLが全部Googleの中継リンクになり、偽の検索結果が混ざる。`shared/api.js` が自動で付ける
  - `resolve_goto_urls` の対象：Organic・News・Local Finder・Search By Image
  - `resolve_poisoned_results` の対象：Organic のみ（`udm=web` `udm=14` とは併用不可）
  - Organicは1回 $0.004、所要時間 1〜2分
- fetch のタイムアウトは300秒
- `domain` の `www.` は外して表示してよい
- depth=10 でも organic は7〜9件しか返らない（AI概要などの枠が混ざるため）。そのまま表示する
- SERPは取るたびに少し変わる
- このクラウド環境ではプロキシが認証を上書きするので、間違ったキーのテストはできない
- ブラウザのテストでは `localhost` をプロキシから外す

新しく分かったことは、この章に1行ずつ足す。
- 公開は `npm run deploy`（site/ を1つのWorkerに埋め込んで公開。`wrangler.jsonc` の main は `dist/worker.js`）。このクラウド環境ではWranglerの `assets` 機能が使えない（プロキシが認証を上書きして401になる）ため、この方式にした
- ブラウザからDataForSEOを直接呼べる（CORS許可済み）。キー入力は全ツール共通の `localStorage`（`dfs_creds`）
- サンプルは `site/Cxx/sample.json`（jaとenで共用）。ページからは `../sample.json` で読む
- SEO：各ツールのページに、比較表・メリット・向かない場面・FAQを**HTMLに直接**書く（JS表示だと検索エンジンに読まれにくいため。locales の例外）。title・description・canonical・hreflang も付ける。`{{SITE_URL}}` はビルドで `site/shared/site-config.json` の `site_url` に置換される。sitemap.xml と robots.txt もビルドで自動生成
- 比較に書く他社の料金・機能は、必ず調べてから書く。「無料より安い」などの言い方はしない（AhrefsにはSERPが無料で見られるチェッカーがある）。日付（○年○月時点）を添える

## 多言語化の予定（全ツールが仕上がってから）

最終的な対応言語は9つ。**今は ja と en だけ作る**。

| 言語 | フォルダ・ファイル名 | 初期の国（要確認） |
|---|---|---|
| 日本語 | `ja` | 日本 2392 |
| English | `en` | 米国 2840 |
| Tiếng Việt | `vi` | ベトナム 2704 |
| Bahasa Indonesia | `id` | インドネシア 2360 |
| Português (Brasil) | `pt-BR` | ブラジル 2076 |
| 繁體中文 | `zh-TW` | 台湾 2158 |
| Türkçe | `tr` | トルコ 2792 |
| ไทย | `th` | タイ 2764 |
| Français | `fr` | フランス 2250 |

- 並び順は、ツール内の言語切替もこの順
- 国コードは記憶ベース。追加する時に DataForSEO の locations API で確かめる
- 追加するもの：`locales/<言語>.json`、`shared/markets.json` の各言語の名前と初期値、各ツールのページ（`/Cxx/<言語>/`）、`hreflang`、sitemap
- ツールのページに書くSEO用の長文（比較表・FAQ）は、翻訳だけでなく、その国で使われている大手ツールに合わせて書き直す（例：台湾・ベトナム・タイにはそれぞれ有名なSEOツールがある）。機械翻訳のままにしない
- 言語が増えるとページが倍々になるので、全ツールが仕上がった時に「ページをテンプレートから自動生成する」形へ移す
- 件数（depth）を増やしても料金は単純な倍にならない。Organic実測：10件 $0.004、20件 $0.0055。所要時間は20件で約78秒（API側の値）。料金の説明には実測値を書く
- 取得中は、動くバー＋経過秒数＋目安時間を出す（`shared/ui.js` の `startProgress`）。再試行中は「やり直しています（2/3回目）」に変わる
- 検索系ツール（Googleの結果を取るもの）は遅い。Googleの検索結果リンクが「いったんGoogleを経由する」仕様（クリック計測のため）に変わり、本物のURLを確かめる処理（`resolve_goto_urls` など）に時間がかかる。実測：10件で約90秒（付けなければ約4秒だが、URLが全部 google.com の中継リンクになり使えない）。**この理由を、検索系ツールの画面（`ui.slow_search`）とFAQに必ず書く**。速さより正確さを選んだ（2026-11 に決定）

## サイトの共通パーツ
- ヘッダー・フッター（アカウントを作るリンク、DataForSEOとは、カスタム依頼、「公式ではありません」の注記）は `scripts/partials/` にあり、ビルドで全ページに差し込まれる（ページには `<!--SITE_HEADER-->` と `<!--SITE_FOOTER-->` を置く。言語は `<html lang>` で判定）
- 紹介リンクは `site/shared/site-config.json` の `referral_url` だけで管理。入れると、ヘッダー・フッター・キー欄・説明ページに「紹介リンクです」付きで出る（`rel="sponsored"` も付く）
- `site-config.json` の他の項目：`site_url`（canonical・sitemap用）、`google_site_verification`（Search Console確認用。トップの `<head>` に自動で入る）、`contact_url`（カスタム依頼の窓口。まだ未使用）
- `noindex` を書いたページは sitemap に載らない（カスタム依頼ページは仮のため noindex）
- 目的：①アフィリエイト ②カスタムツール・データ定期便の依頼。データだけ欲しい人向けには、GAS か公式MCPで出す案（未定）

## ツールの追加のしかた（2026-11 に仕組みを変更）
ページと一覧はビルドが自動で作る。1本あたり、書くのは次の4つだけ。

1. `site/Cxx/tool.json` — エンドポイント、入力欄、国・言語の有無、件数、結果の取り出し方と列、`who`（誰の）
   - `result.items`：結果の配列の場所（例 `result.0.items`）、`where`：絞り込み、`columns`：`key`・`from`（元の項目。`a.b` で入れ子も可）・`label`（文言のキー）・`link`・`transform`（今は `strip_www`）
   - 検索系（Googleの結果リンクを直すもの）は `"slow_search": true`
2. `site/Cxx/sample.json` — 実データを短くしたもの。`keyword`・`fetched_at`・`tasks` を持つ
3. `site/Cxx/_content.<言語>.html` — SEO本文（比較表・メリット・向かない場面・FAQ）。`_` で始まるファイルは公開されない
4. `site/locales/<言語>.json` に `cxx.name` `cxx.desc` `cxx.price` `cxx.eta` `cxx.title` `cxx.meta`、入力欄・列の文言を足す

- 本文ファイルとロケールがそろった言語だけ、ページが作られる（言語を足す時は `scripts/langs.json` に追加）
- トップページ（`/`=ja、`/en/` など）は、`who` ごとにツールが並ぶ。`who` の名前は locales の `who.<キー>`
- 共通の動きは `site/shared/tool.js`。個別の JS は書かない。`tool.json` で足りない時だけ、`tool.js` に足す（全ツールで使える形で）
- 確認：`node scripts/build-worker.mjs` → ブラウザでサンプル表示 → 実APIを1回だけ

## 作業の前に必ず読む
- `2026_11/PLAN.md`（72本を作る計画・品質の決まり・バッチの手順）と `2026_11/PROGRESS.tsv`（現在地）
- コマンド：`npm run check`（本文・文言・サンプルの機械チェック）、`npm run smoke`（ブラウザで全ツール×全言語）、`npm run deploy`（チェックを通ると公開）
- **基準は下げない。** 満たせないツールは作らずに報告して止まる
- 本文のFAQ・比較表は、生成後のHTMLを直接直す時、表は `<tr><td>`、FAQは `<details>` の形（Pythonの書き方ではない）。独立レビューで見つかった典型の指摘：日英の表の不一致、未測定の数字を断定、同じ言い回しの使い回し、本文内の矛盾。書いたら自分で見直す
- Maps/画像検索は件数を変えても同額（20件・100件とも$0.002）。News は10件ごとに加算。Local Finder は20件$0.002／100件$0.01。件数の料金は必ず実測して書く
- 画像の列は `"type": "image"`、日付は `"transform": "date"`、文章で返る結果は `result.answer.markdown`（安全な簡易Markdown表示）

## このクラウド環境での作業メモ（新しいセッション向け）
- 公開：`CLOUDFLARE_ACCOUNT_ID=04b402248ae5c56d6d24177a0f812040 CLOUDFLARE_API_TOKEN=proxy-injected npm run deploy`（トークンはプロキシが差し込む。チェックを通らないと公開されない）。`wrangler` は `npx` で動く
- ブラウザ検査：`NO_PROXY=localhost,127.0.0.1 node scripts/smoke.mjs [ID...]`（Playwrightは入っている。`scripts/smoke.mjs` が探す）。画面の見た目を見る時だけ、スクリーンショットを撮る
- DataForSEO：`api.dataforseo.com` はプロキシが認証を差し込む。curl で直接呼べる（`-u` や `Authorization` は不要）
- 一時ファイルは、スクラッチパッド（`/tmp/claude-0/...`）に置く。リポジトリには入れない
- コミットとプッシュは **main** に直接してよい（ユーザー承認済み）
- 使用量の記録：バッチの最初と最後に `get_session`（`external_metadata.usage`）を見て、差を `USAGE.tsv` に足す
- コマンドに `rm` を含めると安全チェックで止まることがある。ファイル作成は Write ツールか、Python のスクリプトファイルで行う
