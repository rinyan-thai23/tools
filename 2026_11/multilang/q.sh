#!/bin/bash
# usage: q.sh <file-tag> <location_name> <lang_code> kw1 kw2 ...
tag=$1; loc=$2; lang=$3; shift 3
kws=$(printf '%s\n' "$@" | python3 -I -c 'import sys,json;print(json.dumps([l.rstrip("\n") for l in sys.stdin if l.strip()],ensure_ascii=False))')
curl -s -X POST https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live -H 'Content-Type: application/json' -d "[{\"location_name\":\"$loc\",\"language_code\":\"$lang\",\"keywords\":$kws}]" -o raw_${tag}_2026-11-26.json
python3 -I -c "
import json;d=json.load(open('raw_${tag}_2026-11-26.json'));t=d['tasks'][0]
print('${tag}',t['status_code'],t['cost'])
for x in (t.get('result') or []): print('  ',x['keyword'],x['search_volume'])
"
