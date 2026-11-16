import os, sys, json
room = sys.argv[1]
d = json.load(open("/home/claude/zh/data3d_zh.json"))
r = [r for r in d["rooms"] if r["id"] == room][0]
packs = sorted({d["packs"][x[k][0]].split("?")[0] for x in r["niches"] if x for k in ("af", "ae") if x.get(k)})
fs = [p for p in packs if os.path.exists("/home/claude/zh/site/" + p)]
print(json.dumps([{"as": "index.html", "path": "/home/claude/zh/site/index.html"}] + [{"as": p, "path": "/home/claude/zh/site/" + p} for p in fs]))
