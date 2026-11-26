#!/bin/sh
# 3業種のサイトを、並列6でブラウザ表示して文章を取る
cd "$(dirname "$0")/.."
for n in gym pilates juku; do
  sort -u -t "$(printf '\t')" -k2,2 data/targets_$n.tsv | xargs -P6 -L1 sh -c 'NO_PROXY=localhost node tool/render_text.cjs "$1" data/sites_'$n'/$0.txt 5 >/dev/null 2>&1'
  echo "$n done $(ls data/sites_$n | wc -l)"
done
echo ALLDONE
