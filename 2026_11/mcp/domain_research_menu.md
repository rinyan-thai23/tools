# ドメイン調査メニュー（対象：khansei.co.jp）

状態：メニュー案のみ（APIは未実行）。金額は実測（★）と目安（△、実行前に公式docsで再確認）。
流れ：「●●を調べたい」を選ぶ → 種類・回数・概算金額を出す → **ここでストップ** → 承認 → 実行。

| ●● | 出せるデータ | エンドポイント | 回数 | 概算 |
|---|---|---|---|---|
| A 全体の強さ | 検索流入の推定・順位分布・有料広告の有無 | labs/google/domain_rank_overview | 1 | △$0.01〜0.02 |
| B 何で見つかっているか | 上位キーワード・順位・検索数・どのページか | labs/google/ranked_keywords | 1（100件） | ★$0.024（1000件★$0.132） |
| C どのページが稼ぐか | ページ別の推定流入 | labs/google/relevant_pages | 1 | △$0.02〜0.03 |
| D ライバルは誰か | 同じ言葉で競う他サイト・重なり度 | labs/google/competitors_domain | 1 | △$0.02〜0.03 |
| E ライバルとの差 | 相手は取れて自分は取れていない言葉 | labs/google/domain_intersection | 1〜3 | △$0.02〜0.03/回 |
| F 技術・つくり | 使用CMS・ツール | domain_analytics/technologies | 1 | △$0.01 |
| G サイトの健康診断 | 速度・SEOの不備（トップ1ページ） | on_page/instant_pages / lighthouse | 1〜2 | △$0.002〜0.01 |
| H 被リンク | 被リンク数・参照元ドメイン・スパム度 | backlinks/*（summary等） | 2〜3 | △別契約が必要か要確認 |
| I 運営情報 | 取得日・登録情報 | domain_analytics/whois | 1 | △$0.01〜 |

おすすめ最小セット（A＋B(100件)＋D）：約 $0.07〜0.10。
