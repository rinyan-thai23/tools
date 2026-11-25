import json,html
R='/home/user/tools/'
S=json.load(open(R+'articles/_inc/ai4_stats.json')); sh=S['shops']; u=S['usedcnt']; c=S['cost']
NAMES={'chatgpt':'ChatGPT','claude':'Claude','gemini':'Gemini','perplexity':'Perplexity'}
shop_rows=''.join(f'<tr><td>{NAMES[a]}</td><td>{html.escape(" ／ ".join(sh[a]))}</td></tr>' for a in NAMES)
use_rows=''.join(f'<tr><td>{NAMES[a]}</td><td>{u[a]} / 5</td><td>{S["refs_by"][a]}</td><td>{c[a]}</td></tr>' for a in NAMES)
a4=f'''<p>同じ質問を、ChatGPT、Claude、Gemini、Perplexityの4つのAIに聞くと、答えと出典はどれくらい違うのでしょうか。DataForSEOのAPIを使う4つのツール（<a href="/C18/ja/">C18 ChatGPT</a>、<a href="/C19/ja/">C19 Claude</a>、<a href="/C20/ja/">C20 Gemini</a>、<a href="/C21/ja/">C21 Perplexity</a>）で、<strong>5つの質問</strong>を聞き比べました。</p>

<h2>先に、わかったこと</h2>
<ul>
<li><strong>Webを参照したのは、Perplexityが5問すべて、ChatGPTとGeminiが2問、Claudeは0問</strong>でした。ClaudeのツールはWeb検索を使わない設定なので、Web情報は出ません。</li>
<li>渋谷のラーメン店で、<strong>3つのAIが「らーめん はやし」</strong>（ChatGPT、Gemini、Perplexity）を挙げました。Claudeは、ほかの3つとは違う店（鶏そば 玉五郎、ラーメン横丁、一風堂）を挙げました。</li>
<li>「最新のiPhoneの価格」で、Claudeは<strong>「学習データは2024年4月まで」</strong>と書き、現在の価格は答えませんでした。GeminiとPerplexityは、<strong>iPhone 18 Proが219,800円から、iPhone 18 Pro Maxが239,800円から</strong>と書きました。ChatGPTは、iPhone Duoの価格（256GBが364,800円）などを書きました。</li>
<li>1回の費用は、Claudeが約$0.002〜0.003、Perplexityが約$0.006、GeminiとChatGPTは、Webを使った回が約$0.03〜0.06、使わなかった回は約$0.001〜0.003でした。</li>
</ul>
<p>同じ質問を、4人に聞いて回ったようなものです。ある人は調べてから答え、ある人は覚えていることだけで答えます。</p>

<h2>Webを参照した回数（5問のうち）</h2>
<div class="scroll"><table class="data"><thead><tr><th>AI</th><th>Webを参照した質問</th><th>参照URLの合計</th><th>5問の費用の合計(USD)</th></tr></thead><tbody>{use_rows}</tbody></table></div>
<p class="note">ChatGPT、Gemini、Perplexityの「Webを参照」は、APIが返した内部の検索ワードまたは参照URLがあるかで判断しています。Geminiの参照URLは、Google経由の転送URLではなく、元のURLを使っています。</p>

<h2>渋谷のラーメン店（質問「渋谷でおすすめのラーメン店を3つ教えてください」）</h2>
<div class="scroll"><table class="data"><thead><tr><th>AI</th><th>答えに書かれた3つの店</th></tr></thead><tbody>{shop_rows}</tbody></table></div>
<p class="note">店名は、回答の文字をそのまま載せています。同じ質問でも聞くたびに変わることがあります（<a href="/articles/c18-ramen-10-times/">ChatGPTに10回聞いた記事</a>）。ここでは各AIに1回ずつ聞いた結果です。「喜楽」と「中華麺店 喜楽（きらく）」は、書かれた名前のまま並べています。</p>

<h2>全データ：20の答え（5問×4AI）</h2>
<p>質問ごと、AIごとの、Webの参照の有無、内部の検索ワード、参照URL数、トークン、費用です。</p>
<p><a href="/articles/data/ai4-20answers-2026-11-25.csv" download>CSVでダウンロード（回答の全文を含む）</a></p>
<!--include:ai4_summary-->

<h2>全データ：回答の全文（20個）</h2>
<p>返ってきた文章を、そのまま載せています（質問ごとに、4つのAI）。</p>
<!--include:ai4_answers-->

<h2>全データ：参照したURL（{S["nrefs"]}件）</h2>
<p><a href="/articles/data/ai4-references-2026-11-25.csv" download>CSVでダウンロード</a></p>
<details><summary>参照URLの一覧を開く（{S["nrefs"]}件）</summary>
<!--include:ai4_refs-->
</details>

<h2>どうやって調べたか</h2>
<div class="box">
<ul>
<li>日付：2026年11月25日</li>
<li>質問5個：渋谷でおすすめのラーメン店を3つ教えてください／最新のiPhoneの価格を教えてください／SEOとは何ですか／ノートパソコンの選び方を教えてください／キーワードプランナーの使い方を教えてください</li>
<li>モデルと設定：ChatGPT＝gpt-4o-mini（Web検索ができる設定）、Claude＝claude-haiku-4-5（Web検索なし）、Gemini＝gemini-3.5-flash-lite（Web検索ができる設定）、Perplexity＝sonar</li>
<li>ChatGPTの5回は、同じ日に<a href="/articles/c18-40-prompts-references/">別の記事</a>で取った結果を使いました。ほかの3つは、今回取りました（15回）</li>
<li>ツール：<a href="/C18/ja/">C18</a>、<a href="/C19/ja/">C19</a>、<a href="/C20/ja/">C20</a>、<a href="/C21/ja/">C21</a></li>
<li>費用：今回の15回で<strong>${S["cost_new"]}</strong></li>
</ul>
</div>
<p class="note">各AIの画面のサービスとは、モデルや設定が違います。回答は聞くたびに変わることがあり、この結果は「この日の1回ずつ」のものです。どの答えが正しいかは、判断していません。</p>
<p>確認だけなら、各AIの画面で同じ質問を聞いてみるだけでも十分です。答えを記録として残したくなったら、ツールを使ってみてください。</p>
'''
open(R+'articles/c18-four-ai-compared.html','w',encoding='utf-8').write(a4)
idx=json.load(open(R+'articles/index.json',encoding='utf-8'))
idx=[a for a in idx if a['slug']!='c18-four-ai-compared']
idx.append({"slug":"c18-four-ai-compared","tool":"C18","date":"2026-11-25","title":"同じ質問を、ChatGPT・Claude・Gemini・Perplexityに聞いたら、答えと出典はどう違う？","description":"5つの質問を、4つのAIに1回ずつ聞いて、答え・Webの参照・費用を全部載せました。Webを参照したのは、Perplexityが5問すべて、ChatGPTとGeminiが2問、Claudeは0問でした。"})
idx.sort(key=lambda a:(a['tool'],a['slug']))
json.dump(idx,open(R+'articles/index.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
