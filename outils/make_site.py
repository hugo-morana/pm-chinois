#!/usr/bin/env python3
"""Adapte l'appli du palais italien au chinois et produit site/index.html (données et three.js intégrés)."""
import re, json, os, shutil, sys
SRC = "/home/claude/hugo-morana/pm-italien"
OUT = "/home/claude/zh/site"
os.makedirs(OUT + "/audio", exist_ok=True)
s = open(f"{SRC}/index.html", encoding="utf8").read()

def rep(old, new, count=None, must=True):
    global s
    n = s.count(old)
    if must and n == 0:
        sys.exit(f"introuvable : {old[:80]}")
    s = s.replace(old, new) if count is None else s.replace(old, new, count)
    return n

# --- titres, marque
rep("Palazzo dell'italiano", "Palais du chinois · 汉语宫")
rep('content="Palazzo"', 'content="汉语宫"')
# --- voix et langue
rep("/^it/i.test(v.lang)", "/^(zh|cmn)/i.test(v.lang)")
rep("/it-IT/i.test(v.lang)", "/(zh-CN|zh_CN|cmn-Hans)/i.test(v.lang)")
rep('"it-IT"', '"zh-CN"')
rep('lang="it-fonipa"', 'lang="zh-fonipa"')
rep('lang="it"', 'lang="zh-CN"')
rep("Aucune voix italienne sur cet appareil", "Aucune voix chinoise sur cet appareil")
# --- stockage local séparé du palais italien
rep('"pmit:"', '"pmzh:"')
# --- textes visibles
for a, b in [("de l'italien", "du chinois"), ("l'italien", "le chinois"), ("en italien", "en chinois"),
             ("italiennes", "chinoises"), ("italienne", "chinoise"), ("italiens", "chinois"), ("italien", "chinois")]:
    rep(a, b, must=False)
s = re.sub(r"(?<=[ →(>])IT\b", "ZH", s)
# --- saisie : garder les sinogrammes et accepter le pinyin sans tons
rep('.replace(/[^a-z0-9 ]/g, " ")', '.replace(/[^a-z0-9 \\u3400-\\u9fff]/g, " ")')
rep('okGuess = reps.some(r => altsOf(rawIt(x)).concat(altsOf(x.it)).some(c => close(c, r))); }',
    'okGuess = reps.some(r => altsOf(rawIt(x)).concat(altsOf(x.it)).concat(altsOf(x.pr)).concat([String(x.pr || "").replace(/\\s+/g, "")]).some(c => close(c, r) || close(c.replace(/\\s+/g, ""), r.replace(/\\s+/g, "")))); }')
# --- pinyin des phrases sous le chinois
n = rep('<p class="exit" lang="zh-CN">${mark(x.eit, x.eim)}</p>',
        '<p class="exit" lang="zh-CN">${mark(x.eit, x.eim)}</p>${x.epy ? `<p class="epy">${esc(x.epy)}</p>` : ""}')
rep('<p class="exit" lang="zh-CN">${mark(shown.eit, shown.eim)}</p>',
    '<p class="exit" lang="zh-CN">${mark(shown.eit, shown.eim)}</p>${shown.epy ? `<p class="epy">${esc(shown.epy)}</p>` : ""}')
# --- police chinoise
rep("family=IBM+Plex+Mono:wght@500&", "family=IBM+Plex+Mono:wght@500&family=Noto+Sans+SC:wght@400;600&")
rep(".exit { font-weight:600 }",
    ".exit { font-weight:600 } :lang(zh-CN), .big-it, .lit.l2, .qa .it { font-family:\"Noto Sans SC\", \"PingFang SC\", \"Hiragino Sans GB\", \"Microsoft YaHei\", var(--body), sans-serif } .epy { color:var(--accent); font:500 13px/1.35 var(--mono); margin:2px 0 4px !important; letter-spacing:.01em } .big-it { font-size:34px; letter-spacing:.04em }")
# la prononciation (pinyin) plus lisible
rep(".pr { font:500 11px var(--mono); color:var(--muted); letter-spacing:.05em }",
    ".pr { font:500 11px var(--mono); color:var(--muted); letter-spacing:.05em } .phon .pr { font-size:15px; color:var(--accent); letter-spacing:.02em }", must=False)

# --- données et dépendances intégrées
data = open("/home/claude/zh/data3d_zh.json", encoding="utf8").read()
three = open(f"{SRC}/vendor/three.min.js", encoding="utf8").read()
cfg = open(f"{SRC}/config.js", encoding="utf8").read()
rep('<script src="config.js"></script>', "<script>" + cfg + "</script>")
rep('<script src="vendor/three.min.js"></script>', "<script>" + three.replace("</script", "<\\/script") + "</script>")
rep('<script src="offline.js"></script>', "")
rep('const res = await fetch("data3d.json"); DATA = await res.json();',
    'DATA = JSON.parse(document.getElementById("pmdata").textContent);')
rep("<script>\n\"use strict\";", '<script type="application/json" id="pmdata">' + data.replace("</", "<\\/") + "</script>\n<script>\n\"use strict\";", must=False) or None
if 'id="pmdata"' not in s:
    i = s.index('"use strict";')
    j = s.rfind("<script", 0, i)
    s = s[:j] + '<script type="application/json" id="pmdata">' + data.replace("</", "<\\/") + "</script>\n" + s[j:]
# icônes et manifest du palais chinois
if 'rel="manifest"' not in s:
    s = s.replace("<title>", '<link rel="apple-touch-icon" href="apple-touch-icon.png">\n<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">\n<link rel="manifest" href="manifest.json">\n<meta name="theme-color" content="#2a1c1a">\n<title>', 1)
# --- section « Compte » des Réglages (Supabase : inscription, connexion, suppression…)
def _rep(a, b, n=1):
    global s
    assert s.count(a) >= 1, a[:60]
    s = s.replace(a, b, n)
_a = s.index("/* Fenêtre « Compte » (version GitHub Pages) */")
_b = s.index("\n", s.index("async function sbOut()")) + 1
s = s[:_a] + open("/home/claude/zh/compte.js", encoding="utf8").read() + s[_b:]
_rep('const SBCFG = window.PM_CONFIG || {};', 'const SBCFG = Object.assign({}, window.PM_CONFIG || {}, ls.get("sbcfg", {}));')
_rep('.select("data").eq("key", key)', '.select("data").eq("key", SBK(key))')
_rep('upsert({ user_id: store.uid, key, data,', 'upsert({ user_id: store.uid, key: SBK(key), data,')
_rep('toast("Progression synchronisée avec votre compte"); }', 'toast("Progression synchronisée avec votre compte"); renderAccount(); }')
_a = s.index('  $("#accountBtn").onclick')
_b = s.index("\n", s.index('$("#accountSheet").addEventListener("keydown"')) + 1
s = s[:_a] + '  $("#accountBtn").onclick = () => { setView("reglages"); setTimeout(() => $("#compteSec").scrollIntoView({ behavior: "smooth", block: "start" }), 60); };\n  wireAccount();\n' + s[_b:]
_rep('<h1>Réglages</h1>\n  <h2 style="margin:4px 0 0">Palais</h2>', '<h1>Réglages</h1>\n  <h2 id="compteSec" style="margin:4px 0 0">Compte</h2>\n  <div id="acctSet" style="display:flex;flex-direction:column;gap:12px;margin-top:8px"></div>\n  <h2 style="margin:18px 0 0">Palais</h2>')
open(f"{OUT}/index.html", "w", encoding="utf8").write(s)

# --- sons français utilisés
d = json.loads(data)
used = sorted({x[k][0] for r in d["rooms"] for x in r["niches"] if x for k in ("af", "ae") if x.get(k)})
for i in used:
    p = d["packs"][i].split("?")[0]
    shutil.copy(f"{SRC}/{p}", f"{OUT}/{p}")
left = [m for m in re.findall(r"italien|Italien|it-IT|pmit", s)]
print("ok", len(s), "octets ; paquets audio :", len(used), "; restes :", len(left))

# --- décor chinois (post-traitement)
s = open(f"{OUT}/index.html", encoding="utf8").read()
DEC = {
 "noms":         '{ fr: "marché de nuit", it: "夜市", floor: ["pierre", "#5a4a3c", "#3b3029"], wall: "#b8312f", ceil: "#2a1d1a", land: "etal" }',
 "verbes":       '{ fr: "atelier du hutong", it: "胡同作坊", floor: ["planches", "#6b4a2e", "#563a24"], wall: "#8f8a80", ceil: "#d8c8a8", land: "etabli" }',
 "adjectifs":    '{ fr: "galerie de peintures à l\'encre", it: "画廊", floor: ["marbre", "#efe9dc", "#7d7568"], wall: "#f3eee3", ceil: "#3d3a36", land: "chevalet" }',
 "pronoms":      '{ fr: "salon de thé", it: "茶馆", floor: ["tapis", "#7a2626", "#d4a840"], wall: "#8a5a33", ceil: "#c9a24a", land: "fauteuil" }',
 "conjonctions": '{ fr: "jardin aux ponts", it: "园林", floor: ["damier", "#2f5b4f", "#d6d0c2"], wall: "#ebe5d6", ceil: "#9cc3c0", land: "pont" }',
 "prepositions": '{ fr: "cour carrée", it: "四合院", floor: ["pierre", "#8f8f8a", "#6a6a66"], wall: "#a8322c", ceil: "#7fa4c8", land: "colonne" }',
 "expressions":  '{ fr: "foire du temple", it: "庙会", floor: ["pierre", "#9a8c7a", "#6f6455"], wall: "#c23b2e", ceil: "#e8c25a", land: "fontaine" }',
 "incises":      '{ fr: "académie des lettrés", it: "书院", floor: ["planches", "#7a5a3a", "#5c4129"], wall: "#e4d6b8", ceil: "#6b2f24", land: "lutrin" }',
 "formes":       '{ fr: "pavillon des miroirs de bronze", it: "铜镜阁", floor: ["marbre", "#d8d0bc", "#6a5d48"], wall: "#2f4a4a", ceil: "#c9a24a", land: "etabli" }',
 "patrons":      '{ fr: "cabinet du maître bâtisseur", it: "营造司", floor: ["damier", "#3a2a22", "#d9c9a8"], wall: "#c9b893", ceil: "#7a2626", land: "lutrin" }',
 "adverbes":     '{ fr: "opéra de Pékin", it: "京剧院", floor: ["planches", "#4a2a1c", "#5e3624"], wall: "#b0201f", ceil: "#c8a03a", land: "rideau" }',
}
for k, v in DEC.items():
    s, n = re.subn(r"(\n  " + k + r":\s+)\{[^\n]*?\}(,?\n)", lambda m: m.group(1) + v + m.group(2), s, count=1)
    if not n:
        sys.exit("décor introuvable " + k)
# pinyin paramétrique : [mǒurén]… affiché, le son garde x.it
for a, b in [('<span class="pr">${esc(x.pr)}</span></div>', '<span class="pr">${escP(x.prd || x.pr)}</span></div>'),
             ('<span class="pr">${esc(x.pr)}</span></span>', '<span class="pr">${escP(x.prd || x.pr)}</span></span>')]:
    if s.count(a) != 1:
        sys.exit("pinyin introuvable " + a)
    s = s.replace(a, b)
open(f"{OUT}/index.html", "w", encoding="utf8").write(s)
print("décor chinois appliqué")
