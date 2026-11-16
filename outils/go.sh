#!/bin/bash
# usage: go.sh room  -> build, show pinyin, build site
cd /home/claude/zh
python3 build_zh.py 2>&1 | grep -v Warn | tail -5
python3 -c "
import json,sys; d=json.load(open('data3d_zh.json'))
r=[r for r in d['rooms'] if r['id']=='$1'][0]
for i,x in enumerate(r['niches']):
  if x: print(i,x['pr'],'|',x['epy'])"
python3 make_site.py | tail -1
