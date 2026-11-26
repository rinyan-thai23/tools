# MCP実験メモ（DataForSEO 公式MCP と 直接API の比較）

作成日：2026-11-26　状態：**計画のみ（APIはまだ叩いていない）**

## 1. 公式MCPサーバー
- 名前：`dataforseo-mcp-server`（npm）。最新 3.1.3（2026-10-02公開）、Node 22以上
- 出所：npmの公開者は dataforseo（info@dataforseo.com）。リポジトリは github.com/dataforseo/mcp-server-typescript（npmのメタ情報で確認。GitHub本体はこの環境から未確認）
- 旧版（v2）は非推奨。v3 は道具が4つだけ：`docs_index` / `docs_list_sections` / `docs_search` / `api_request`
  → 「機能ごとに道具が山ほどある」型ではない。`api_request` が実質、直接APIの代理
- 認証：環境変数 `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD`（`DATAFORSEO_USERNAME`も可）。ダミー値を渡し、プロキシが本物に置換
- 公式のリモート版もあり：https://mcp.dataforseo.com/v3/mcp（OAuth。今回は使わない）

## 2. この環境での動かし方
1. `npx dataforseo-mcp-server@3.1.3`（npmは通る）。バージョン固定で再現性を確保
2. stdioで起動。環境変数はダミー文字（`DATAFORSEO_LOGIN=dummy` など）
3. Claude Code に `claude mcp add` で登録（またはスクリプトからstdioで直接呼ぶ）
4. ネットワーク：必要なホストは `api.dataforseo.com`（許可済）と `docs.dataforseo.com`（疎通OK。docs系の道具用）。`data.dataforseo.com` がコード内にあるが用途は未確認（使うかは実測で確認）。
   足りないホストは今のところなし
- 注意：`api_request` は既定で「.ai パス」を使う（`noAiMode: true` で通常パス）。同じ仕事にするため、比較時は通常パスを指定する

## 3. 費用の注意（大事）
C24（search_volume/live）は **$0.09/回**。予算$0.1では **1回しか叩けない**。
直接＋MCPの2本立てにすると $0.18 で予算オーバー。

## 4. 比べる実験の計画（案）
| 案 | 中身 | 費用 |
|---|---|---|
| A（おすすめ） | 安い同型API **C23**（ai_keyword_data/keywords_search_volume/live、キーワード3つ）を、直接2回＋MCP2回 | 約 $0.04 |
| B | C24を**MCPで1回だけ**。直接は過去の実績ログと比較 | $0.09 |
| 無料枠 | `docs_*` 道具の呼び出し（料金なし想定）でトークン量だけ測る | $0 |

比べる4項目：トークン量（Claude側の入出力）／所要時間／手間（手順の数・つまずき）／失敗しやすさ（エラー内容）。
安全策：1回ごとに料金（レスポンスの cost）を記録し、累計が$0.08に近づいたら止める。

## 5. 結果
（承認後に記入）

## 結果メモ（対象サイト A〜E 実行・2026-11-26、詳細は社外秘のため 個別レポートは非公開でコミットしない）
- 実行：A,B(100件),C,D,E×2 を、npmのMCPサーバーをstdioで起動し MCP SDK から `api_request` で呼んだ（全6回）
- つまずき1：Nodeはプロキシを自動で使わない。`NODE_USE_ENV_PROXY=1` が無いと、ダミー認証のまま届いて 40100（費用0）
- つまずき2：.aiモードの応答は `cost` が返らない。費用は直接APIの実測（$0.012/回〜）からの推定で、合計 約$0.08〜0.12
- 軽さ：.aiモードの応答は軽い（B 100件でも60KB弱、素のJSONより小さい見込み。比較は未実施）。`docs_search` は1回で約43KB（約1万トークン）と重い
- 速さ：各呼び出し 0.5〜1.2秒
- 直接curlより増えた手間：サーバーのインストール、クライアントのコード、プロキシ設定
