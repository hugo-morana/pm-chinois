import json, sys
d=json.load(open('/home/claude/hugo-morana/pm-italien/data3d.json'))
r=[r for r in d['rooms'] if r['id']==sys.argv[1]][0]
for i,x in enumerate(r['niches']):
    if x: print(f"{i:02d}|{x['fr']}|{x['it']}|{x['efr']}")
