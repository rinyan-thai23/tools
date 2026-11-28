#!/usr/bin/env python3
# 次の言語の再調査（2026-11-28）。Google広告 検索ボリューム live。1回=1国・約40語（$0.09）。
# 使い方: python3 q2.py <tag>   tag = fr | pt | id | th | tr
# 結果: raw2_<tag>_2026-11-28.json（生データ）
import json, subprocess, sys

# 国コード, 言語コード, 語。語はAIが現地語にしたもの（現地の人の確認はしていない）。
# 先頭の6語は、前回（2026-11-26）と同じ語で、比べられるようにしてある。
SETS = {
    "fr": (2250, "fr", """recherche de mots-clés
outil seo
marketing d'affiliation
comment créer un blog
apprendre le seo
agence seo
outil de recherche de mots clés
outils seo
outil seo gratuit
logiciel seo
meilleur outil seo
suivi de position
vérifier position google
backlinks
vérificateur de backlinks
netlinking
audit seo
audit seo gratuit
analyse de site web
test vitesse site
api seo
api serp
api google
semrush
ahrefs
ubersuggest
dataforseo
consultant seo
freelance seo
formation seo
cours seo
créer un blog
générateur de mots clés
planificateur de mots clés
longue traîne
volume de recherche
analyse concurrentielle seo
rédaction seo
référencement naturel
outil de référencement
scraper google"""),
    "pt": (2076, "pt", """pesquisa de palavras-chave
ferramenta de seo
marketing de afiliados
como criar um blog
aprender seo
serviço de seo
ferramenta de pesquisa de palavras-chave
ferramentas de seo
ferramenta de seo grátis
software de seo
melhor ferramenta de seo
rastreador de posições
verificar posição google
backlinks
verificador de backlinks
link building
auditoria seo
auditoria de seo gratuita
análise de site
teste de velocidade do site
api de seo
api serp
api do google
semrush
ahrefs
ubersuggest
dataforseo
agência de seo
consultor seo
freelancer seo
curso de seo
criar blog
gerador de palavras-chave
planejador de palavras-chave
cauda longa
volume de busca
análise de concorrentes seo
redação seo
otimização para mecanismos de busca
ferramenta de otimização
raspador do google"""),
    "id": (2360, "id", """riset kata kunci
alat seo
affiliate marketing
cara membuat blog
belajar seo
jasa seo
alat riset kata kunci
tools seo
seo tools gratis
software seo
tools seo terbaik
pelacak peringkat
cek posisi google
cek ranking keyword
backlink
cek backlink
link building
audit seo
audit seo gratis
analisis website
tes kecepatan website
api seo
api serp
api google
semrush
ahrefs
ubersuggest
dataforseo
konsultan seo
freelance seo
kursus seo
buat blog
generator kata kunci
perencana kata kunci
long tail keyword
volume pencarian
analisis kompetitor seo
penulisan artikel seo
optimasi mesin pencari
tools optimasi
scraper google"""),
    "th": (2764, "th", """วิจัยคีย์เวิร์ด
เครื่องมือ seo
affiliate
วิธีทำบล็อก
เรียน seo
รับทำ seo
เครื่องมือค้นหาคีย์เวิร์ด
seo tools
เครื่องมือ seo ฟรี
โปรแกรม seo
เครื่องมือ seo ที่ดีที่สุด
เช็คอันดับ google
ติดตามอันดับ
เช็คอันดับคีย์เวิร์ด
backlink
เช็ค backlink
สร้าง backlink
ตรวจสอบ seo
audit seo
วิเคราะห์เว็บไซต์
ทดสอบความเร็วเว็บไซต์
seo api
serp api
google api
semrush
ahrefs
ubersuggest
dataforseo
ที่ปรึกษา seo
ฟรีแลนซ์ seo
คอร์ส seo
affiliate marketing
สร้างบล็อก
ตัวสร้างคีย์เวิร์ด
keyword planner
long tail keyword
ปริมาณการค้นหา
วิเคราะห์คู่แข่ง seo
เขียนบทความ seo
การทำ seo"""),
    "tr": (2792, "tr", """anahtar kelime araştırması
seo aracı
affiliate pazarlama
blog nasıl açılır
seo öğrenme
seo hizmeti
anahtar kelime araştırma aracı
seo araçları
ücretsiz seo aracı
seo yazılımı
en iyi seo aracı
sıralama takibi
google sıralama kontrolü
anahtar kelime sıralama
backlink
backlink kontrol
link building
seo analizi
seo denetimi
web sitesi analizi
site hız testi
seo api
serp api
google api
semrush
ahrefs
ubersuggest
dataforseo
seo danışmanı
freelance seo
seo eğitimi
blog oluşturma
anahtar kelime oluşturucu
anahtar kelime planlayıcı
uzun kuyruk anahtar kelime
arama hacmi
rakip analizi seo
seo makale yazımı
arama motoru optimizasyonu
seo optimizasyon aracı
google scraper"""),
}

tag = sys.argv[1]
loc, lang, text = SETS[tag]
kws = [l.strip() for l in text.split("\n") if l.strip()]
body = json.dumps([{"location_code": loc, "language_code": lang, "keywords": kws}], ensure_ascii=False)
out = f"raw2_{tag}_2026-11-28.json"
subprocess.run(["curl", "-s", "-m", "120", "-X", "POST", "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live",
                "-H", "Content-Type: application/json", "--data-binary", body, "-o", out], check=True)
d = json.load(open(out))
t = d["tasks"][0]
print(tag, len(kws), "語", t["status_code"], t["status_message"], "cost", t.get("cost"), "結果", len(t.get("result") or []))
