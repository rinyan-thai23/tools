# 繁體中文のAI分析プロンプトを、検査してから site/locales/zh-TW.json に入れる
# 使い方: python3 scripts/aiprompts/merge_zh.py <out_*.json のあるフォルダ> [--write]
import json,sys,glob,re
R='/home/user/tools/'
src=sys.argv[1]; write='--write' in sys.argv
en=json.load(open(R+'site/locales/en.json',encoding='utf-8'))
zh=json.load(open(R+'site/locales/zh-TW.json',encoding='utf-8'))
PH=['{date}','{country}','{language}','{n}','{data}','{prev_date}','{prev_n}','{prev_data}']
# 簡体字だけに使われる字（これが入っていたら要確認）と、中国本土の言い方
SIMP=set('这个们为从对还时过说请让与关发应实现经间资料数据网络软件视频质量项目')-set('資料數據網絡')  # 下の ban で別に見る
SIMPCHARS=set('这们为从对还时过说让与关发应实经间问题资数据网络软视频质项总结构开点击选择设计应该显统计优标签发现长')
BAN=['視頻','質量','信息','軟件','網絡','數據','默認','鏈接','博客','鼠標','用戶體驗']
bad=0; ok={}
for f in sorted(glob.glob(src.rstrip('/')+'/out_*.json')):
    d=json.load(open(f,encoding='utf-8'))
    for tid,v in d.items():
        k=tid.lower()
        for kind in ('ai_prompt','ai_prompt_diff'):
            ref=en.get(f'{k}.{kind}')
            if ref is None:
                if kind in v: print('EXTRA',tid,kind); bad+=1
                continue
            z=v.get(kind)
            if not z: print('MISSING',tid,kind); bad+=1; continue
            for ph in PH:
                if ref.count(ph)!=z.count(ph): print('PLACEHOLDER',tid,kind,ph,ref.count(ph),z.count(ph)); bad+=1
            if ref.count('```')!=z.count('```'): print('FENCE',tid,kind); bad+=1
            s=[c for c in z if c in SIMPCHARS]
            if s: print('SIMPLIFIED?',tid,kind,''.join(sorted(set(s)))); bad+=1
            b=[w for w in BAN if w in z]
            if b: print('BANWORD',tid,kind,b); bad+=1
            if re.search(r'[A-Za-z]{4,} [A-Za-z]{4,} [A-Za-z]{4,}',z): print('ENGLISH-RUN?',tid,kind); bad+=1
            ok[f'{k}.{kind}']=z
print('checked',len(ok),'problems',bad)
if write and bad==0:
    zh.update(ok)
    json.dump(zh,open(R+'site/locales/zh-TW.json','w',encoding='utf-8'),ensure_ascii=False,indent=2); open(R+'site/locales/zh-TW.json','a').write('\n')
    print('written',len(ok))
