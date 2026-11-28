# ベトナム語の翻訳（out_N.json）を検査して、vi.json と _content.vi.html に入れる
# 使い方: python3 merge_vi.py <フォルダ> [--write]
import json,glob,re,sys
R='/home/user/tools/'
src=sys.argv[1].rstrip('/'); write='--write' in sys.argv
en=json.load(open(R+'site/locales/en.json',encoding='utf-8'))
vp=R+'site/locales/vi.json'; vi=json.load(open(vp,encoding='utf-8'))
PH=re.compile(r'\{\w+\}')
def money(s): return sorted(re.findall(r'\$[0-9]+(?:[.,][0-9]+)*',s))
def tags(s): return {t:len(re.findall(t,s)) for t in ('<h2>','<li>','<tr','<details>','<summary>','<table>','<ul>','<a ','<p','<strong>')}
bad=0; ok_loc={}; ok_con={}
for f in sorted(glob.glob(src+'/out_*.json')):
    d=json.load(open(f,encoding='utf-8'))
    for tid,v in d.items():
        k=tid.lower()+'.'
        ref={kk:vv for kk,vv in en.items() if kk.startswith(k)}
        loc=v.get('locale',{})
        for kk in ref:
            if kk not in loc: print('MISSING',tid,kk); bad+=1; continue
            a,b=ref[kk],loc[kk]
            if isinstance(a,list):
                if not (isinstance(b,list) and len(a)==len(b) and all(isinstance(r,list) and len(r)==3 for r in b)): print('STEPS',tid,kk); bad+=1
                elif [money(x[1]) for x in a]!=[money(x[1]) for x in b]: print('STEPS$',tid,kk); bad+=1
                continue
            if sorted(PH.findall(a))!=sorted(PH.findall(b)): print('PLACEHOLDER',tid,kk); bad+=1
            if a.count('```')!=b.count('```'): print('FENCE',tid,kk); bad+=1
            if money(a)!=money(b): print('MONEY',tid,kk,money(a),money(b)); bad+=1
            if kk.endswith('.title') and len(b)>70: print('TITLE>70',tid,len(b)); bad+=1
            if kk.endswith('.meta') and len(b)>200: print('META>200',tid,len(b)); bad+=1
            if 'bin/bash' in b: print('BASH',tid,kk); bad+=1
        for kk in loc:
            if kk not in ref: print('EXTRA',tid,kk); bad+=1
        c=v.get('content','')
        e=open(R+f'site/{tid}/_content.en.html',encoding='utf-8').read()
        if money(e)!=money(c): print('CONTENT$',tid,money(e),money(c)); bad+=1
        if tags(e)!=tags(c): print('TAGS',tid,{t:(tags(e)[t],tags(c)[t]) for t in tags(e) if tags(e)[t]!=tags(c)[t]}); bad+=1
        if 'không phù hợp' not in c: print('NOFIT',tid); bad+=1
        if 'bin/bash' in c: print('BASH content',tid); bad+=1
        if re.findall(r'href="([^"]+)"',e)!=re.findall(r'href="([^"]+)"',c): print('HREF',tid); bad+=1
        ok_loc.update(loc); ok_con[tid]=c
print('tools',len(ok_con),'keys',len(ok_loc),'problems',bad)
if write and bad==0:
    vi.update(ok_loc)
    out={k:vi[k] for k in en if k in vi}
    json.dump(out,open(vp,'w',encoding='utf-8'),ensure_ascii=False,indent=2); open(vp,'a').write('\n')
    for tid,c in ok_con.items(): open(R+f'site/{tid}/_content.vi.html','w',encoding='utf-8').write(c if c.endswith('\n') else c+'\n')
    print('written')
