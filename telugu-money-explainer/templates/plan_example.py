# v2 edit plan: dark editorial style, no subtitles, no logo. Writes graphics/scenes.json
import json, os
EP = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(f"{EP}/audio/words.json")); TL = {l["id"]: l for l in json.load(open(f"{EP}/timeline.json"))["lines"]}
M = json.load(open(f"{EP}/footage/candidates.json"))
words = {}
for ch in W:
    ws = [w for w in ch["words"] if w["text"].strip()]
    # map words to sentence ids by timeline windows
    for sid in ch["ids"]:
        l = TL[sid]; words[sid] = [w for w in ws if l["start"] - 0.15 <= w["start"] < l["end"] + 0.05]
def w(sid, sub="", lead=0.15):
    """start time of first word in sentence sid containing sub (minus a small lead)."""
    for x in words[sid]:
        if sub in x["text"]: return round(x["start"] - lead, 3)
    raise KeyError(f"{sid}:{sub}")
S = lambda sid: TL[sid]["start"]
E = lambda sid: TL[sid]["end"]
ph = lambda k: "file://" + EP + "/" + M[k.split(":")[0]][int(k.split(":")[1])]["file"].lstrip("./")

SC = []
def add(start, end, html, photo=None, move="in", cls="", xf=0.0, full=False):
    SC.append(dict(start=round(start, 3), end=round(end, 3), html=html, photo=ph(photo) if photo else None, move=move, cls=cls, xf=xf, full=full))
def lt(eyebrow, body, src=None):
    return f'<div class="lt"><div class="eyebrow te" data-in="{eyebrow[1]}">— {eyebrow[0]}</div>{body}</div>' + (f'<div class="src">SOURCE · {src}</div>' if src else "")

# ---------------- HOOK ----------------
t = w("s01", "మూడు")
add(0, 4.0, lt(("ఒక్క application", 0.3),
    f'<div class="big gold" style="font-size:190px;margin-top:10px" data-in="{t}" data-count="0,300000,{t},1.1" data-pre="₹">₹0</div>'), "lottery:3", "in")
add(4.0, 8.6, lt(("గెలిస్తే wine shop · ఓడిపోతే?", 4.1),
    f'<div class="big" style="font-size:150px;margin-top:10px"><span class="strike">₹3,00,000<i data-draw="{w("s02","ఓడిపోతే")+.5},.5"></i></span></div>'
    f'<div style="margin-top:28px" data-in="{w("s02","రావు")}"><span class="pill red">తిరిగి రావు · NON-REFUNDABLE</span></div>',
    "DECCAN CHRONICLE · AUG 2025"), "wineshop:0", "l")
# applications vs shops: dark data scene
a3, a4, a5 = w("s03", "తొంభై"), w("s04", "రెండు"), w("s05", "ముప్పై")
add(8.6, 21.5, f'''
<div style="position:absolute;left:160px;top:150px;width:1600px">
 <div class="eyebrow" data-in="8.7">— తెలంగాణ · 2025–27 WINE SHOP LOTTERY</div>
 <div style="margin-top:70px" data-in="{a3}">
   <div class="row"><div class="big" style="font-size:120px;width:620px" data-count="0,95137,{a3},1.4">0</div><div style="font-size:46px;font-weight:700">applications</div></div>
   <div class="bar" style="width:1150px;background:var(--gold);margin-top:18px" data-draw="{a3},1.4"></div>
 </div>
 <div style="margin-top:60px" data-in="{a4}">
   <div class="row"><div class="big" style="font-size:120px;width:620px" data-count="0,2620,{a4},1.0">0</div><div style="font-size:46px;font-weight:700">shops మాత్రమే</div></div>
   <div class="bar" style="width:{1150*2620/95137:.0f}px;background:var(--ivory);margin-top:18px" data-draw="{a4+.4},.6"></div>
 </div>
 <div style="position:absolute;right:0;top:520px;text-align:right" data-in="{a5}">
   <div class="eyebrow te">ఒక్కో shop కోసం</div>
   <div class="big red" style="font-size:260px" data-count="0,36,{a5},1.0">0</div>
   <div style="font-size:42px;font-weight:700">applications పోటీ</div>
 </div>
</div><div class="src">SOURCE · DECCAN CHRONICLE · AUG–OCT 2025</div>''', cls="dark", xf=0.25)
add(21.5, 28.6, lt(("ఇంత మంది · ఇంత పెద్ద risk", 21.8),
    f'<div class="head" data-in="{w("s07","గెలిచిన")}">గెలిచిన వాళ్ళకి నిజంగా</div>'
    f'<div class="head" data-in="{w("s07","ఎంత")}"><span class="gold">ఎంత</span> మిగులుతుంది?</div>'), "night:0", "in")
add(28.6, 34.6, f'''<div class="center"><div class="eyebrow" data-in="28.8">— ఈ రోజు</div>
 <div class="head" style="font-size:96px;margin-top:20px" data-in="{w("s08","ప్రతి")}">ప్రతి <span class="gold">రూపాయి</span> లెక్క</div>
 <div class="rule" style="width:420px;margin-top:34px" data-draw="{w("s08","లెక్క")},.7"></div></div>''', cls="dark", xf=0.25)
items = [("s10", "ఒకటి", "Lottery లో ఖచ్చితంగా గెలిచేది ఎవరు?"), ("s11", "రెండు", "రోజుకి ఎంత అమ్మితే లాభం?"), ("s12", "మూడు", "ఒక్క shop కి <span class='gold'>₹1 కోటి</span> ఎందుకు?")]
rows = ""
for i, (sid, k, txt) in enumerate(items):
    a = w(sid, k); b = S(items[i + 1][0]) - .2 if i < 2 else E("s12") + 0.6
    rows += f'''<div class="row" style="margin-top:46px" data-in="{a}" data-on="{a},{b}">
      <div class="big gold" style="font-size:92px;width:110px">{i+1}</div>
      <div style="font-size:60px;font-weight:700">{txt}</div></div>'''
add(34.6, 49.2, f'''<div style="position:absolute;left:200px;top:200px"><div class="eyebrow te" data-in="34.7">— ఈ video చివరికి మీకు తెలిసేవి</div>
 <div class="rule" style="width:900px;margin-top:22px;opacity:.5" data-draw="34.8,.8"></div>{rows}</div>''', cls="dark", xf=0.25)
add(49.2, 53.9, lt(("Disclaimer", 49.4),
    f'<div class="head" data-in="{w("s13","ఇది")}">ఇది కేవలం <span class="gold">business లెక్క</span></div>'), "liquor2:0", "out")
add(53.9, 58.2, lt(("ప్రతి number కి source", 54.0),
    f'<div style="margin-top:14px" data-in="{w("s14","ప్రభుత్వ")}"><span class="pill gold">ప్రభుత్వ notifications</span></div>'
    f'<div style="margin-top:20px" data-in="{w("s14","news")}"><span class="pill" style="color:var(--ivory)">News reports</span></div>'), "news:0", "r")
# chapter card (paper style the user liked)
add(58.2, 60.7, '''<div class="center"><div style="font-family:IBM Plex Mono;font-size:30px;letter-spacing:.2em;color:#7b7266" data-in="58.25">CHAPTER 1</div>
 <div style="font-family:Ramabhadra;font-size:150px;margin-top:26px" data-in="58.4">లాటరీ</div>
 <div class="rule" style="width:160px;margin-top:30px;background:#9c2f26" data-draw="58.7,.6"></div></div>''', cls="paper", xf=0.2)
# ---------------- CHAPTER 1 ----------------
add(60.7, 66.5, lt(("ఒక్కో application fee", 60.9),
    f'<div class="row" style="margin-top:14px"><div class="big gray" style="font-size:110px"><span class="strike">₹2,00,000<i data-draw="{w("s16","ఇంతకు")},.5"></i></span></div>'
    f'<div class="eyebrow" style="font-size:30px" data-in="{w("s16","ఇంతకు")}">ముందు</div></div>'
    f'<div class="big gold" style="font-size:170px;margin-top:6px" data-in="{w("s16","మూడు")}" data-count="200000,300000,{w("s16","మూడు")},1.0" data-pre="₹">₹2,00,000</div>',
    "TELANGANA EXCISE NOTIFICATION · 2025"), "papers:1", "in")
add(66.5, 69.8, lt(("Rule", 66.6), f'<div class="head" data-in="{w("s17","ఎన్ని")}">ఒక్క మనిషి <span class="gold">ఎన్ని</span> applications అయినా</div>'), "money2:3", "r")
a18, a19, a20 = w("s18", "వంద"), w("s19", "మూడు"), w("s20", "మూడు")
add(69.8, 81.0, f'''<div style="position:absolute;left:160px;top:170px">
 <div class="eyebrow te" data-in="70.0">— సంగారెడ్డి · ఒక్క వ్యక్తి</div>
 <div class="row" style="margin-top:50px;align-items:baseline" data-in="{a18}">
   <div class="big" style="font-size:200px" data-count="0,100,{a18},1.0" data-suf="+">0</div><div style="font-size:52px;font-weight:700">applications</div></div>
 <div class="row" style="margin-top:50px;align-items:baseline;font-size:84px" data-in="{w('s19','వంద')}">
   <span class="big gray">100 × ₹3 <span class="te0">లక్షలు</span> =</span>
   <span class="big red" data-in="{a19}" data-count="0,3,{a19},.9" data-pre="₹" >₹0</span><span class="te0 red"> కోట్లు</span></div>
 <div class="row" style="margin-top:60px" data-in="{a20}">
   <div class="eyebrow te" style="font-size:40px">వచ్చింది →</div><div class="big gold" style="font-size:150px" data-pop="{a20}">3 shops</div></div>
</div><div class="src">SOURCE · DECCAN CHRONICLE · OCT 2025</div>''', cls="dark", xf=0.25)
a21, a22 = w("s21", "ఎనిమిది"), w("s22", "ఎనభై")
add(81.0, 92.6, f'''<div style="position:absolute;left:160px;top:150px;width:1600px">
 <div class="eyebrow te" data-in="81.2">— శంషాబాద్ area</div>
 <div class="row" style="margin-top:40px;align-items:baseline" data-in="{a21}"><div class="big" style="font-size:150px" data-count="0,8536,{a21},1.3">0</div>
   <div style="font-size:48px;font-weight:700">applications · <span class="gold">100 shops</span></div></div>
 <div style="margin-top:90px" data-in="{a22-.6}"><div class="eyebrow te">ఒక్కో shop కోసం పోటీ</div>
  <div class="row" style="margin-top:24px"><div style="width:300px;font-size:38px;font-weight:700">తెలంగాణ సగటు</div><div class="bar" style="width:{1000*36/85:.0f}px;background:var(--gray)" data-draw="{a22-.5},.6"></div><div class="big" style="font-size:60px">36</div></div>
  <div class="row" style="margin-top:24px"><div style="width:300px;font-size:38px;font-weight:700">శంషాబాద్</div><div class="bar" style="width:1000px;background:var(--red)" data-draw="{a22},1.0"></div><div class="big red" style="font-size:60px" data-count="0,85,{a22},1.0">0</div></div>
 </div></div><div class="src">SOURCE · DECCAN CHRONICLE · OCT 2025</div>''', cls="dark", xf=0.25)
a23, a24 = w("s23", "October"), w("s24", "తొంభై")
add(92.6, 101.0, f'''<div class="center"><div class="eyebrow" data-in="{a23}">— LOTTERY DRAW · COLLECTORS ముందు</div>
 <div class="big" style="font-size:200px;margin-top:20px" data-in="{a23}">27 OCT 2025</div>
 <div style="margin-top:40px" data-in="{a24}"><span class="big gold" style="font-size:120px" data-count="0,95137,{a24},1.3">0</span> <span style="font-size:48px;font-weight:700">applications</span></div></div>''',
    "govt:7", "in", full=True)

json.dump(SC, open(f"{EP}/graphics/scenes.json", "w"), ensure_ascii=False, indent=0)
print(len(SC), "scenes, until", SC[-1]["end"])
