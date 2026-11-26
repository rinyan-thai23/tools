# mcp/ — 公式MCP（DataForSEO v3）で「レポート事業」を100本試す場所

## ねらい
「誰を喜ばせるか」から考えて、DataForSEOのデータで作れる **レポート型の事業案を100個**、実際にAPIを叩いて試す。
その中から良かったものを **10個** 採用する。1つの案は、LP・データ・作り方まで **1フォルダ(`exp/NNN_名前/`)に全部入れる**。

## フォルダの決まり
```
mcp/
  README.md          ← これ
  INDEX.tsv          ← 100本の台帳（番号・誰向け・費用・点数・判定）
  IDEAS.md           ← アイデア帳。需要から考える。毎回の「強引チェック」つき
  PATTERNS.md        ← 成り立ちそうな型／そうでない型の判断（根拠つき）。節目ごとに更新
  package.json       ← 公式MCPサーバーのバージョン固定（3.1.3）。`npm i` で入る
  lib/               ← 共通部品（mcp.mjs: MCP接続 / grid.mjs: 場所ごとの地図順位）
  exp/NNN_slug/      ← 1案＝1フォルダ
      README.md      ← 何を・なぜ・どのように・結果・費用・気づき（必須）
      data/          ← 取った生データ（再現・再計算用）
      lp/            ← LP（index.html）。店名・会社名は伏せ字
      tool/ など     ← その案で作った道具（あれば）
      sample_output/ ← 道具が出した見本（あれば）
  _prelude/ 相当     ← 000：最初の実験（ドメイン診断・MCPの比較）は mcp_test.md / khansei_report.* / data/site01
```

## 動かし方（クラウド環境）
```
cd 2026_11/mcp && npm i
NODE_USE_ENV_PROXY=1 node lib/grid.mjs --keyword ラーメン --lat 35.7057 --lng 139.6497 --n 5 --out out.json
```
- ID・パスワードはダミー（プロキシが本物に差し替える）。`NODE_USE_ENV_PROXY=1` がないと認証エラー（費用0）になる
- 自分のPCで動かす時は `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD` に本物を入れる
- `.ai` モード（既定）の応答は軽いが `cost` が返らない。費用を見たい時は `noAi: true`（`lib/mcp.mjs` の既定）

## 1案のつくり方（毎回同じ）
0. **強引チェック**（`IDEAS.md`）：悩みは本当にあるか／APIなしでも価値が成り立つか／既存の代わりより何が良いか。強引度が「高」なら、作らずに人に聞く
1. **誰の、どんな悩みか**を1文で書く（whoから始める）
2. 使うエンドポイントと**1回の原価**を、叩く前に見積もる（`docs_search` は無料）
3. 実際に叩く（少数で）。`data/` に生データを保存
4. 「見せた瞬間に分かる1枚」を作る（図・診断書）
5. LPを作る。**実データ＋店名・社名は伏せ字**。「見本です」と必ず書く。約束できないこと（順位保証など）は書かない
6. `README.md` に何をどうしたか、費用、弱点を残す
7. `INDEX.tsv` に1行足して点数をつける

## 採用の基準（100本→10本）
各0〜3点。21点満点。**合計14点以上＋外の人の反応が1つ以上**で採用候補。

| 項目 | 見るところ |
|---|---|
| 誰か | 悩みを持つ人を1文で言えるか |
| 一枚の絵 | 見せた瞬間に「おっ」となる絵があるか |
| 原価 | 1回の原価と、売値の差が大きいか |
| 次の一手 | 取った数字だけで「次にやること」が決まるか |
| 届け方 | 誰が・どこで・どうやって届けるかが具体的か |
| くり返し | 月次や複数店で、繰り返し売れるか |
| 安全 | 規約・法的リスクが低いか |

※INDEX.tsv の点数は、いまはAIによる暫定の自己採点。外の人の反応が入ったら付け直す。

「外の人の反応」は、実際に知り合いや見込み客に見せたときの言葉。100本は自分たちのテスト。**採用は、外の人の反応で決める。**

## 公開サイト（社内用・検索に出さない）
- https://lab.byokkit.com/ ：このフォルダの資料を、1案1ページにまとめて公開（Cloudflare Worker `lab-byokkit`、独自ドメイン）
- 検索に出さない設定：全ページに noindex の meta、全応答に `X-Robots-Tag: noindex, nofollow, noarchive`、`/robots.txt` は全拒否。**パスワードはない**ので、URLを知っている人は開ける。店名つきの生データも含む
- 更新：資料を直したら、次を実行
```
cd 2026_11/mcp && npm i
node deploy/build-lab.mjs
cd deploy && CLOUDFLARE_ACCOUNT_ID=04b402248ae5c56d6d24177a0f812040 CLOUDFLARE_API_TOKEN=proxy-injected npx wrangler@4 deploy -c wrangler.lab.jsonc
```
- 仕組み：`deploy/build-lab.mjs` が README・INDEX・PATTERNS・各 `exp/NNN_*` を読んで、静的ページを作り、1つのWorkerに埋め込む（既存の `dfs-tools` とは別のWorker）
