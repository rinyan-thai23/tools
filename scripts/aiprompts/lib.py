# AI分析プロンプトを、ロケール（ja/en）に書き込む道具。使い方: python3 scripts/aiprompts/batchN.py
import json
R='/home/user/tools/'
K={ # よく使う列の説明（ja, en）
 'vol':('月間検索数：Google広告のデータにもとづく目安です。空欄は「データがない」という意味で、0回とは限りません。','Monthly searches: an estimate based on Google Ads data. Blank means "no data", not necessarily zero.'),
 'cpc':('CPC（米ドル）：広告の1クリック単価です。記事の価値ではありません。','CPC (USD): the average price per click for advertisers. It is not the value of an article.'),
 'comp':('競合度（0〜100）：広告の競争の強さです。SEOの難しさではありません。','Competition (0-100): how competitive the keyword is for ads. It is not SEO difficulty.'),
 'kd':('難易度（0〜100）：検索で上位に入る難しさの目安です。目安であって、保証ではありません。','Difficulty (0-100): a guide to how hard it is to rank at the top. It is a guide, not a guarantee.'),
 'etv':('推定流入：検索からの訪問数の推計です。実際の訪問数ではありません。','Estimated traffic: an estimate of search visits. It is not the real number of visits.'),
 'rank':('順位：その検索での順位です。','Rank: the position in that search.'),
 'top100':('上位100件だけです。全部ではありません。','Only the top 100, not everything.'),
 'now':('検索結果や数字は、場所や時間で変わることがあります。この日の、この条件での結果です。','Results and numbers can change with place and time. This is for this day and these conditions.'),
 'ai':('回答は、聞くたびに変わることがあります。この日の1回の結果です。','Answers can change each time you ask. This is one result from this day.'),
}
DEF_CANT=('データだけからは言えないこと（たとえば、理由や今後の成果）を、短く書いてください。','Briefly say what cannot be known from the data alone (for example, the reasons or future results).')
RJ='# ルール\n- 渡した数字だけを使ってください。ない数字を作らないでください。\n- 推測は、「推測です」と書いてください。\n- 中学生にも分かる言葉で、短く書いてください。\n'
RE='# Rules\n- Use only the numbers I gave you. Do not make up numbers.\n- Say "this is a guess" when you guess.\n- Write short and simple, so that a middle-school student can understand.\n'
def build(spec):
    """spec: who=(ja,en) reader=(ja,en) cols=[str|(ja,en)] tasks=[(ja,en)] tail=(ja,en) cant=(ja,en)|None extra=[(ja,en)]"""
    out={}
    for idx,lg in ((0,'ja'),(1,'en')):
        cols=[(K[c][idx] if isinstance(c,str) else c[idx]) for c in spec['cols']]
        ex=[e[idx] for e in spec.get('extra',[])]
        tasks=[t[idx] for t in spec['tasks']]+[(spec.get('cant') or DEF_CANT)[idx]]
        tn=''.join(f'{i}. {t}\n' for i,t in enumerate(tasks,1)).rstrip('\n')
        tail=spec['tail'][idx]
        rowsline_ja='内容：AIの答えの文章と、引用元などの表' if spec.get('answer') else '行数：{n}行'
        rowsline_en='Contents: the AI answer text and a table of sources' if spec.get('answer') else 'Rows: {n}'
        if lg=='ja':
            facts='- 列の意味\n'+'\n'.join('  - '+c for c in cols)+('\n'+'\n'.join('- '+e for e in ex) if ex else '')
            txt=f"あなたは{spec['who'][0]}です。\n読むのは、{spec['reader'][0]}\n\n# 渡すデータ\n- 取得日：{{date}}\n- 地域と言語：{{country}}・{{language}}\n- {rowsline_ja}\n{facts}\n\n# お願いしたいこと\n{tn}\n\n{RJ}- {tail}\n\n# データ（タブ区切り）\n```\n{{data}}\n```"
        else:
            facts='- Columns\n'+'\n'.join('  - '+c for c in cols)+('\n'+'\n'.join('- '+e for e in ex) if ex else '')
            txt=f"You are {spec['who'][1]}.\nThe reader is {spec['reader'][1]}\n\n# About the data\n- Date: {{date}}\n- Country and language: {{country}} / {{language}}\n- {rowsline_en}\n{facts}\n\n# What I would like you to do\n{tn}\n\n{RE}- {tail}\n\n# Data (tab-separated)\n```\n{{data}}\n```"
        out[lg]=txt
    return out
def apply(specs):
    L={lg:json.load(open(R+f'site/locales/{lg}.json',encoding='utf-8')) for lg in ('ja','en')}
    for tid,spec in specs.items():
        o=build(spec)
        for lg in ('ja','en'): L[lg][tid.lower()+'.ai_prompt']=o[lg]
        p=R+f'site/{tid}/tool.json'; j=json.load(open(p,encoding='utf-8')); j['copy']=True
        json.dump(j,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=2); open(p,'a').write('\n')
    for lg in ('ja','en'):
        json.dump(L[lg],open(R+f'site/locales/{lg}.json','w',encoding='utf-8'),ensure_ascii=False,indent=2); open(R+f'site/locales/{lg}.json','a').write('\n')
    print('done',len(specs))
