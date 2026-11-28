# Petunjuk terjemahan halaman utama ke bahasa Indonesia（インドネシア語版トップページの翻訳）

あなたはインドネシア語ネイティブの翻訳者・SEOライターです。ウェブサイト「DataForSEO 1機能ツール集」（BYOK＝自分のAPIキーを使う、使った分だけ払う）の**トップページの説明文**を、英語からインドネシア語にします。これは検索エンジン（Google）に載る文章でもあるので、インドネシアの人が実際に検索する自然な言葉（例：alat SEO, riset kata kunci, cek peringkat kata kunci, volume pencarian bulanan, pesaing, optimasi untuk pencarian AI）を使います。ただし、英語原文にない事実・数字・機能は足さない。

## 入力と出力
- 入力：同じフォルダの `in_N.json`。出力：同じフォルダの `out_N.json`（このファイル以外は何も作らない・変更しない）。
- in_1.json：`{"categories": {"title","intro","sections":[{"title","text"}...]}}` → out_1.json に同じ形でインドネシア語にして書く（sections の数と順番は同じ）。
- in_2.json / in_3.json：`{"descriptions": {"C01": "英語の説明", ...}}` → out に同じキーのまま、インドネシア語の説明にする（キーは全部残す）。
- Write ツールか Python の json.dump(..., ensure_ascii=False, indent=1) で書く。**シェルのヒアドキュメントで `$` を含む文章を書かない**（$0.09 が壊れるため）。書いた後 json.load で確認する。

## 守ること
1. 金額・数字・固有名詞（DataForSEO, Google, ChatGPT, Gemini, Claude, Perplexity, YouTube, WHOIS, Lighthouse など）・URL はそのまま。`$0.09` のような金額は一字も変えない。数字は、桁区切りを「1.000」（ドット）、小数点を「2,3」（カンマ）のインドネシア式にする。
2. 用語は、既に確定している訳に合わせる：kata kunci, volume pencarian bulanan, persaingan, CPC, peringkat, domain, judul, tingkat kesulitan kata kunci, maksud pencarian, kata kunci terkait, pesaing, trafik, contoh（sample）, Kunci API, tren, situs, afiliasi, klik, sumber yang dikutip, komentar, subtitle, penyebutan, sentimen, tayangan, kanal。詳しい訳例は /home/user/tools/site/locales/id.json（`c01.desc`, `c24.desc`, `c35.desc` など）を参照。「genre」は使わず topik / kategori、「traffic」は trafik と書く。
3. 語り口：親しみやすく、短く、中学生でも分かる。「kamu」で話しかける。
4. 英語原文の注意書き（「毎日の順位追跡はしない」「SEOの難しさではない」など）は必ず残す。評価や誇張を足さない。
5. 説明の1文目で、そのツールが「何を入れると何が表になるか」が分かる形を保つ（英語と同じ構成）。
