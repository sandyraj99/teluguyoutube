# EP02 v2 plan, 100.4 s to the end (exec'd from plan_v2.py; uses add/lt/w/S/E)
END = json.load(open(f"{EP}/timeline.json"))["duration"]
def te(x, cls=""): return f'<span class="te0 {cls}" style="font-size:48px">{x}</span>'
def cnt(to, t, du=1.1, pre="", suf="", d=0, cls="", size=150, frm=0, inn=None):
    i = f' data-in="{inn if inn is not None else t}"' if inn is not False else ""
    return f'<span class="big {cls}" style="font-size:{size}px"{i} data-count="{frm},{to},{t},{du},{d}" data-pre="{pre}" data-suf="{suf}">{pre}{frm}{suf}</span>'
def chapter(a, b, n, title):
    add(a, b, f'''<div class="center"><div style="font-family:IBM Plex Mono;font-size:30px;letter-spacing:.2em;color:#7b7266" data-in="{a+.05}">CHAPTER {n}</div>
 <div style="font-family:Ramabhadra;font-size:140px;margin-top:26px" data-in="{a+.2}">{title}</div>
 <div class="rule" style="width:160px;margin-top:30px;background:#9c2f26" data-draw="{a+.5},.6"></div></div>''', cls="paper", xf=0.2)
def src(x): return f'<div class="src">SOURCE · {x}</div>'
BOX = 'position:absolute;left:160px;top:150px;width:1600px'

# ---- lottery result ----
a25, a26 = w("s25", "రెండు"), w("s26", "తొంభై")
add(100.4, 110.6, f'''<div style="{BOX}">
 <div class="eyebrow te" data-in="100.5">— Draw తర్వాత</div>
 <div class="row" style="margin-top:60px;align-items:baseline" data-in="{a25}">{cnt(2601, a25, 1.0, cls="gold", size=170, inn=False)}<div style="font-size:50px;font-weight:700">shops allot అయ్యాయి</div></div>
 <div class="row" style="margin-top:50px;align-items:baseline" data-in="{a26}">{cnt(92536, a26, 1.2, size=170, inn=False)}<div style="font-size:50px;font-weight:700">applications కి</div></div>
 <div style="margin-top:40px" data-in="{w("s26","రూపాయి")}"><span class="pill red" style="font-size:44px">₹0 refund · ఒక్క రూపాయి కూడా రాదు</span></div>
</div>{src("NEWSMETER · 29 OCT 2025")}''', cls="dark", xf=0.25)
a28, a29 = w("s28", "తొంభై"), w("s29", "రెండు")
add(110.6, 125.2, f'''<div class="center">
 <div class="eyebrow te" data-in="110.8">— ఒక్క నిమిషం · ఈ లెక్క వేయండి</div>
 <div class="big gray" style="font-size:110px;margin-top:60px" data-in="{a28}">95,137 × ₹3,00,000</div>
 <div class="big" style="font-size:80px;margin-top:20px" data-in="{a29-.4}">=</div>
 <div style="margin-top:10px" data-in="{a29}">{cnt(2854, a29, 1.6, pre="₹", cls="gold", size=210, inn=False)}{te(" కోట్లు","gold") .replace('class="te0','style="font-size:90px" class="te0')}</div>
 <div style="font-size:44px;font-weight:700;margin-top:30px" data-in="{w("s29","shop")}">ఒక్క shop తెరవకముందే · <span class="gold">ప్రభుత్వానికి</span></div>
</div>{src("COMPUTED · 95,137 × ₹3 LAKH")}''', cls="dark", xf=0.25)
add(125.2, 131.2, f'''<div class="center"><div class="eyebrow te" data-in="125.4">— ఈ lottery లో ఖచ్చితంగా గెలిచేది</div>
 <div style="font-weight:800;font-size:170px;margin-top:30px" class="gold" data-pop="{w("s30","ప్రభుత్వం")}">ప్రభుత్వం</div></div>''', "govt:0", "in", full=True)
add(131.2, 135.7, lt(("Shop గెలిచిన వాళ్ళకి", 131.3), f'<div class="head" data-in="{w("s31","అసలు")}"><span class="gold">అసలు పరీక్ష</span> ఇక్కడే మొదలు</div>'), "govt:3", "r")
# ---- chapter 2 ----
chapter(135.7, 138.2, 2, "అసలు ఖర్చు")
add(138.2, 146.8, lt(("Shop గెలిచాక · ముందు కట్టాల్సింది", 138.3),
    f'<div class="head" style="font-size:84px" data-in="{w("s33","Retail")}">Retail Shop <span class="gold">Excise Tax</span></div>'
    f'<div style="margin-top:24px" data-in="{w("s34","జనాభా")}"><span class="pill gold">మీ ఊరి జనాభాని బట్టి మారుతుంది</span></div>', "DECCAN CHRONICLE · AUG 2025"), "govt:1", "in")
a35, a36, a37 = w("s35", "యాభై"), w("s36", "ఒక"), w("s37", "ఐదు")
add(146.8, 162.0, f'''<div style="{BOX}">
 <div class="eyebrow te" data-in="147">— Excise tax · సంవత్సరానికి</div>
 <div data-in="{w("s35","ఐదు")}" style="margin-top:60px"><div style="font-size:40px;font-weight:700">పల్లె · 5,000 లోపు జనాభా</div>
  <div class="row" style="margin-top:14px"><div class="bar" style="width:{1100*50/110:.0f}px;background:var(--gray)" data-draw="{a35},.8"></div>{cnt(50, a35, .8, pre="₹", size=72, inn=False)}{te(" లక్షలు")}</div></div>
 <div data-in="{w("s36","ఇరవై")}" style="margin-top:50px"><div style="font-size:40px;font-weight:700">Hyderabad లాంటి city · 20 లక్షల పైన</div>
  <div class="row" style="margin-top:14px"><div class="bar" style="width:1100px;background:var(--red)" data-draw="{a36},1.0"></div>{cnt(1.1, a36, 1.0, pre="₹", d=1, cls="red", size=72, inn=False)}{te(" కోట్లు","red")}</div></div>
 <div style="margin-top:50px" data-in="{a37}"><span class="pill gold" style="font-size:40px">+ ₹5 లక్షలు special tax · ప్రతి shop</span></div>
</div>{src("DECCAN CHRONICLE · AUG 2025")}''', cls="dark", xf=0.25)
a39, a40 = w("s39", "అరవై"), w("s40", "డెబ్బై")
add(162.0, 176.0, lt(("Model shop · కరీంనగర్ లాంటి town", 162.2),
    f'<div style="font-size:40px;font-weight:700;margin-top:8px" data-in="{w("s39","tax")}">Tax <span data-in="{a40}" class="gold">+ special tax</span> · సంవత్సరానికి</div>'
    f'<div style="position:relative;height:180px"><span class="big gold" style="position:absolute;left:0;top:0;font-size:170px" data-in="{a39}" data-out="{a40}" data-count="0,6500000,{a39},1.0" data-pre="₹">₹0</span>'
    f'<span class="big gold" style="position:absolute;left:0;top:0;font-size:170px" data-in="{a40}" data-count="6500000,7000000,{a40},.8" data-pre="₹">₹65,00,000</span></div>', "DECCAN CHRONICLE · AUG 2025"), "karim:4", "in")
a42, a43 = w("s42", "పంతొమ్మిది"), w("s43", "bottle")
add(176.0, 188.6, f'''<div class="center">
 <div class="eyebrow te" data-in="176.2">— రోజుకి మార్చి చూడండి</div>
 <div class="big gray" style="font-size:110px;margin-top:50px" data-in="{w("s42","డెబ్బై")}">₹70,00,000 ÷ 365</div>
 <div style="margin-top:30px" data-in="{a42}">{cnt(19178, a42, 1.3, pre="₹", cls="gold", size=230, inn=False)}<span class="te0" style="font-size:70px"> / రోజు</span></div>
 <div style="margin-top:36px" data-in="{a43}"><span class="pill red" style="font-size:40px">ఒక్క bottle అమ్మకముందే · ప్రభుత్వానిదే</span></div>
</div>''', cls="dark", xf=0.25)
add(188.6, 192.8, lt(("పండగ రోజైనా · వర్షం పడినా", 188.7), f'<div class="head" data-in="{w("s44","ఈ")}">ఈ <span class="gold">₹19,178</span> లెక్క ఆగదు</div>'), "festival:5", "l")
a45, a45b, a46 = w("s45", "ఆరు"), w("s45", "పది"), w("s46", "పదహారు")
blocks = "".join(f'<div style="width:120px;height:70px;border-radius:8px;background:var(--gold);margin-right:14px" data-in="{a45+i*.12}"></div>' for i in range(6))
add(192.8, 209.0, f'''<div style="{BOX}">
 <div class="eyebrow te" data-in="193">— Tax ఎలా కట్టాలి?</div>
 <div style="font-size:46px;font-weight:700;margin-top:50px" data-in="{a45}">6 instalments · <span class="gold">ముందే</span></div>
 <div class="row" style="gap:0;margin-top:24px">{blocks}</div>
 <div class="row" style="margin-top:30px;align-items:baseline" data-in="{a45b}">{cnt(10.83, a45b, 1.0, pre="₹", d=2, size=110, inn=False)}<span class="te0" style="font-size:46px">లక్షలు · ప్రతి 2 నెలలకి</span></div>
 <div style="margin-top:60px" data-in="{w("s46","నాలుగో")}"><div style="font-size:42px;font-weight:700">+ Bank guarantee <span class="gray">(tax లో ¼)</span></div>
  <div class="row" style="align-items:baseline;margin-top:10px">{cnt(16.25, a46, 1.0, pre="₹", d=2, cls="red", size=130, inn=a46)}<span class="te0 red" style="font-size:50px">లక్షలు</span></div></div>
</div>{src("THE SOUTH FIRST · AUG 2025")}''', cls="dark", xf=0.25)
add(209.0, 214.0, lt(("సరుకు ఎక్కడి నుంచి?", 209.1), f'<div class="head" data-in="{w("s47","beverages")}">ప్రభుత్వ <span class="gold">Beverages Corporation</span></div>'
    f'<div style="margin-top:20px" data-in="{w("s47","cash")}"><span class="pill red">CASH పెట్టే కొనాలి</span></div>'), "truck:6", "r")
add(214.0, 220.1, lt(("కానీ అసలు ప్రశ్న", 214.1), f'<div class="head" data-in="{w("s48","ఒక")}">ఒక bottle అమ్మితే shop కి <span class="gold">ఎంత</span>?</div>'), "liquor2:4", "in")
a50 = w("s50", "కాదు")
add(220.1, 226.5, f'''<div class="center"><div class="eyebrow te" data-in="220.2">— చాలా మంది అనుకునేది</div>
 <div class="head" style="font-size:110px;margin-top:30px" data-in="{w("s50","MRP")}"><span class="strike">MRP మొత్తం shop దే<i data-draw="{a50},.5"></i></span></div>
 <div class="big red" style="font-size:120px;margin-top:30px" data-pop="{a50}">తప్పు</div></div>''', cls="dark", xf=0.25)
a52, a53 = w("s52", "ఇరవై"), w("s53", "ఇరవై")
add(226.5, 237.3, f'''<div style="{BOX}">
 <div class="eyebrow te" data-in="226.7">— Shop కి వచ్చేది · ప్రభుత్వం fix చేసిన margin</div>
 <div data-in="{w("s52","Ordinary")}" style="margin-top:80px"><div style="font-size:44px;font-weight:700">Ordinary మందు</div>
  <div class="row" style="margin-top:14px"><div class="bar" style="width:1100px;background:var(--gold)" data-draw="{a52},.9"></div>{cnt(27, a52, .9, suf="%", cls="gold", size=90, inn=False)}</div></div>
 <div data-in="{w("s53","Premium")}" style="margin-top:60px"><div style="font-size:44px;font-weight:700">Premium · Beer</div>
  <div class="row" style="margin-top:14px"><div class="bar" style="width:{1100*20/27:.0f}px;background:var(--gray)" data-draw="{a53},.9"></div>{cnt(20, a53, .9, suf="%", size=90, inn=False)}</div></div>
</div>{src("TG EXCISE POLICY 2025–27 · DECCAN CHRONICLE")}''', cls="dark", xf=0.25)
add(237.3, 244.0, lt(("ప్రభుత్వం దగ్గర కొన్న ₹100 సరుకు మీద", 237.4),
    f'<div class="row" style="align-items:baseline" data-in="{w("s54","ఇరవై")}"><span class="te0" style="font-size:60px">shop కి →</span><span class="big gold" style="font-size:180px">₹20–27</span></div>'), "money2:6", "in")
a56, a57 = w("s56", "రెండు"), w("s57", "మూడున్నర")
add(244.0, 259.6, f'''<div style="{BOX}">
 <div class="eyebrow te" data-in="244.2">— ఆ ₹19,178 tax తిరిగి రావాలంటే · సంవత్సరానికి ఎంత సరుకు?</div>
 <div data-in="{w("s56","అంతా")}" style="margin-top:80px"><div style="font-size:44px;font-weight:700">అంతా <span class="gold">27%</span> సరుకు అయితే</div>
  <div class="row" style="margin-top:14px"><div class="bar" style="width:{1100*2.59/3.5:.0f}px;background:var(--gold)" data-draw="{a56},1"></div>{cnt(2.59, a56, 1, pre="₹", d=2, size=80, inn=False)}{te(" కోట్లు")}</div></div>
 <div data-in="{w("s57","అంతా")}" style="margin-top:60px"><div style="font-size:44px;font-weight:700">అంతా beer, premium <span class="gray">(20%)</span> అయితే</div>
  <div class="row" style="margin-top:14px"><div class="bar" style="width:1100px;background:var(--red)" data-draw="{a57},1"></div>{cnt(3.5, a57, 1, pre="₹", d=1, cls="red", size=80, inn=False)}{te(" కోట్లు","red")}</div></div>
</div>{src("OUR CALCULATION · ₹70 LAKH ÷ MARGIN")}''', cls="dark", xf=0.25)
a58, a59 = w("s58", "డెబ్బై"), w("s59", "ఓనర్")
add(259.6, 270.9, lt(("రోజుకి కొనాల్సిన సరుకు", 259.7),
    f'<div class="big" style="font-size:130px" data-in="{a58}"><span data-count="0,71030,{a58},1" data-pre="₹">₹0</span> – <span data-count="0,95890,{a58+.3},1" data-pre="₹">₹0</span></div>'
    f'<div class="row" style="margin-top:30px" data-in="{a59}"><span class="te0" style="font-size:54px">ఇది tax కి మాత్రమే · ఓనర్‌కి →</span><span class="big red" style="font-size:120px" data-pop="{a59+.4}">₹0</span></div>'), "night:5", "in")
# ---- chapter 3 ----
chapter(270.9, 273.5, 3, "ఒక రోజు")
add(273.5, 279.0, f'''<div class="center"><div class="eyebrow te" data-in="273.6">— హైదరాబాద్ బయట shops</div>
 <div class="big" style="font-size:190px;margin-top:20px" data-in="{w("s61","ఉదయం")}">10 AM <span class="gold">–</span> 10 PM</div>
 <div style="width:1100px;height:6px;background:rgba(243,238,228,.2);margin:50px auto 0;border-radius:3px"><div class="rule" style="height:6px;width:1100px;border-radius:3px" data-draw="{w("s61","రాత్రి")},2.5"></div></div></div>''', "hyderabad:6", "in", full=True)
a63, a64, a64b = w("s63", "పదమూడు"), w("s64", "యాభై"), w("s64", "పదిహేడు")
add(279.0, 297.4, f'''<div style="{BOX}">
 <div class="eyebrow te" data-in="279.1">— Staff ఖర్చు</div>
 <div class="row" style="margin-top:50px" data-in="{w("s62","నలుగురు")}"><span class="big" style="font-size:120px">4</span><span style="font-size:50px;font-weight:700">workers</span><span class="pill gray" style="font-size:30px">అంచనా</span></div>
 <div class="row" style="margin-top:40px;align-items:baseline" data-in="{w("s63","minimum")}"><span style="font-size:44px;font-weight:700;width:560px">Minimum wage · ఒక్కరికి</span>{cnt(13570, a63, 1, pre="₹", size=90, inn=False)}<span class="te0 gray" style="font-size:40px">/ నెల</span></div>
 <div class="row" style="margin-top:30px;align-items:baseline" data-in="{a64}"><span style="font-size:44px;font-weight:700;width:560px">నలుగురికి</span>{cnt(54280, a64, 1, pre="₹", size=90, inn=False)}<span class="te0 gray" style="font-size:40px">/ నెల</span></div>
 <div class="rule" style="width:1300px;margin-top:40px;opacity:.6" data-draw="{a64b-.3},.5"></div>
 <div class="row" style="margin-top:30px;align-items:baseline" data-in="{a64b}"><span style="font-size:50px;font-weight:800;width:560px">రోజుకి</span>{cnt(1785, a64b, 1, pre="₹", cls="red", size=130, inn=False)}</div>
</div>{src("TELANGANA MINIMUM WAGES · APR 2025")}''', cls="dark", xf=0.25)
add(297.4, 304.7, lt(("ఊరిని బట్టి మారే ఖర్చులు", 297.5),
    f'<div data-in="{w("s65","Rent")}"><span class="pill" style="color:var(--ivory)">Rent</span><span class="pill" style="color:var(--ivory)">Current bill</span><span class="pill" style="color:var(--ivory)">Permit room</span></div>'
    f'<div class="head" style="margin-top:24px" data-in="{w("s65","ఈ")}">ఈ లెక్కలో <span class="red">వేయలేదు</span></div>'), "night:5", "r")
add(304.7, 310.0, f'''<div class="center"><div class="eyebrow te" data-in="304.8">— ఒకే shop · రెండు రకాల రోజులు</div>
 <div class="row" style="margin-top:40px;gap:60px" data-in="{w("s66","రెండు")}"><span class="big" style="font-size:150px">DAY A</span><span class="ser gray" style="font-size:80px">vs</span><span class="big gold" style="font-size:150px">DAY B</span></div>
 <div style="margin-top:40px" data-in="{w("s66","అంచనాలు")}"><span class="pill gray">ఇవి మా అంచనాలు</span></div></div>''', cls="dark", xf=0.25)
def ledger(x0, title, rows, extra=""):
    h = f'<div class="eyebrow" data-in="{x0}">— {title}</div><div style="margin-top:40px">'
    for lbl, val, cls, t in rows:
        h += f'''<div class="row" style="justify-content:space-between;width:1300px;padding:18px 0;border-bottom:1px dashed var(--line)" data-in="{t}">
          <span style="font-size:48px;font-weight:700">{lbl}</span>{val}</div>'''
    return f'<div style="{BOX}">{h}</div></div>{extra}'
a67, a68, a69, a69b, a70 = w("s67", "లక్ష"), w("s68", "ఇరవై"), w("s69", "పంతొమ్మిది"), w("s69", "పదిహేడు"), w("s70", "రెండు")
add(310.0, 335.0, ledger(310.1, "DAY A · అంచనా", [
    ("సరుకు (ప్రభుత్వ ధర)", cnt(100000, a67, .9, pre="₹", size=78, inn=False), "", a67),
    ("Margin <span class='gray' style='font-size:34px'>(సగం ordinary, సగం beer)</span>", cnt(23500, a68, .9, pre="+ ₹", cls="gold", size=78, inn=False), "", a68),
    ("Tax", cnt(19178, a69, .8, pre="− ₹", cls="red", size=78, inn=False), "", a69),
    ("Staff", cnt(1785, a69b, .6, pre="− ₹", cls="red", size=78, inn=False), "", a69b),
    ("<span class='gold'>మిగిలేది</span>", cnt(2537, a70, 1.0, pre="₹", cls="gold", size=110, inn=False), "", a70)],
    f'<div style="position:absolute;left:160px;bottom:120px" data-in="{w("s71","Rent")}"><span class="pill red" style="font-size:40px">Rent, current కడితే → దాదాపు ఏమీ మిగలదు</span></div>'), cls="dark", xf=0.25)
a72, a73, a73b = w("s72", "రెండు"), w("s73", "నలభై"), w("s73", "Tax")
add(335.0, 344.2, ledger(335.1, "DAY B · అదే shop · అంచనా", [
    ("సరుకు (ప్రభుత్వ ధర)", cnt(200000, a72, .9, pre="₹", size=78, inn=False), "", a72),
    ("Margin", cnt(47000, a73, .9, pre="+ ₹", cls="gold", size=78, inn=False), "", a73),
    ("Tax <span class='gray' style='font-size:34px'>· అదే</span>", '<span class="big red" style="font-size:78px">− ₹19,178</span>', "", a73b),
    ("Staff <span class='gray' style='font-size:34px'>· అదే</span>", '<span class="big red" style="font-size:78px">− ₹1,785</span>', "", w("s73", "Staff"))],
    f'<div style="position:absolute;left:160px;bottom:120px" data-in="{w("s74","trap")}"><span class="pill red" style="font-size:44px">కానీ ఇక్కడ ఇంకో trap…</span></div>'), cls="dark", xf=0.25)
a75, a76, a77, a78 = w("s75", "పది"), w("s76", "ఆరున్నర"), w("s77", "ఏడు"), w("s78", "ఎనిమిది")
add(344.2 + 1.9, 373.4, f'''<div style="{BOX}">
 <div class="eyebrow te" data-in="346.3">— Turnover tax trap</div>
 <div class="head" style="font-size:62px;margin-top:30px" data-in="{w("s75","సంవత్సరంలో")}">సరుకు <span class="gold">tax కి 10 రెట్లు</span> దాటితే → పైన ప్రతి సరుకు మీద <span class="red" data-in="{a75+1.5}">+10%</span></div>
 <div style="margin-top:70px;position:relative;width:1500px;height:90px" data-in="{a76-.3}">
   <div class="bar" style="position:absolute;left:0;top:0;width:{1300*6.5/7.3:.0f}px;height:90px;background:var(--gray)" data-draw="{a76},.9"></div>
   <div class="bar" style="position:absolute;left:{1300*6.5/7.3:.0f}px;top:0;width:{1300*0.8/7.3:.0f}px;height:90px;background:var(--red)" data-draw="{a77+.6},.5"></div>
   <div style="position:absolute;left:{1300*6.5/7.3-4:.0f}px;top:-30px;width:4px;height:150px;background:var(--ivory)" data-in="{a76}"></div>
 </div>
 <div class="row" style="margin-top:30px;justify-content:space-between;width:1300px">
   <div data-in="{a76}"><div class="eyebrow">LIMIT</div><span class="big" style="font-size:70px">₹6.5</span>{te(" కోట్లు")}</div>
   <div data-in="{a77}" style="text-align:right"><div class="eyebrow te">రోజుకి ₹2 లక్షలు → సంవత్సరానికి</div>{cnt(7.3, a77, 1, pre="₹", d=1, cls="red", size=70, inn=False)}{te(" కోట్లు","red")}</div></div>
 <div class="row" style="margin-top:50px;align-items:baseline" data-in="{a78}"><span class="te0" style="font-size:48px">₹80 లక్షలు × 10% = ₹8 లక్షలు →</span>{cnt(2192, w("s78","రోజుకి"), 1, pre="− ₹", cls="red", size=110, inn=w("s78","రోజుకి"))}<span class="te0 gray" style="font-size:40px">/ రోజు</span></div>
</div>{src("THE SOUTH FIRST · PETPOOJA · AUG 2025")}''', cls="dark", xf=0.25)
SC[-2]["end"] = 346.1
a79 = w("s79", "ఇరవై")
add(373.4, 378.8, lt(("DAY B · అన్నీ పోగా ఓనర్‌కి", 373.5), f'<div data-in="{a79}">{cnt(23846, a79, 1.2, pre="₹", cls="gold", size=190, inn=False)}<span class="te0" style="font-size:60px"> / రోజు</span></div>'), "festival:6", "in")
a81 = w("s81", "తొమ్మిది")
add(378.8, 392.6, f'''<div style="{BOX}">
 <div class="row" style="gap:40px"><span class="eyebrow te" data-in="{w("s80","ఒకటే")}">ఒకటే shop ·</span><span class="eyebrow te" data-in="{w("s80","license")}">ఒకటే license ·</span><span class="eyebrow te" data-in="{w("s80","tax")}">ఒకటే tax</span></div>
 <div class="row" style="margin-top:60px;gap:60px" data-in="{w("s81","అమ్మకం")}">
  <div class="box" style="padding:40px 60px;width:700px"><div class="eyebrow">DAY A · ₹1,00,000 సరుకు</div><div class="big" style="font-size:130px;margin-top:20px">₹2,537</div></div>
  <div class="box" style="padding:40px 60px;width:700px;border-color:var(--gold)"><div class="eyebrow">DAY B · ₹2,00,000 సరుకు</div><div class="big gold" style="font-size:130px;margin-top:20px">₹23,846</div></div></div>
 <div class="row" style="margin-top:60px;align-items:baseline"><span class="big" style="font-size:110px" data-in="{w("s81","రెట్టింపు")}">2× <span class="te0" style="font-size:54px">అమ్మకం</span></span><span class="big gray" style="font-size:90px" data-in="{a81-.3}">→</span><span class="big gold" style="font-size:150px" data-pop="{a81}">9× <span class="te0" style="font-size:60px">లాభం</span></span></div>
 <div style="margin-top:40px" data-in="{w("s82","పంతొమ్మిది")}"><span class="pill red">ఎందుకంటే ₹19,178 tax ఎప్పుడూ మారదు</span></div>
</div>''', cls="dark", xf=0.25)
add(392.6, 397.0, f'''<div class="center"><div class="eyebrow te" data-in="392.7">— Wine shop business లో అసలు రహస్యం</div>
 <div class="big gold" style="font-size:220px;margin-top:20px" data-pop="{w("s83","Location")}">LOCATION</div></div>''', "village:4", "in", full=True)
# ---- chapter 4 ----
chapter(397.0, 401.8, 4, "₹1 కోటి shop")
a86, a87, a88 = w("s86", "ఒక"), w("s87", "ఒక"), w("s88", "యాభై")
rows = ""
for i, (lbl, val, t, t2) in enumerate([("Town shop", "₹1.10 కోట్లు", a86, a87 - .1), ("Rural shop", "₹1.20 కోట్లు", a87, a88 - .1), ("Partnership మాత్రమే", "₹50 లక్షలు", a88, 419.2)]):
    rows += f'<div class="row" style="justify-content:space-between;width:820px;padding:16px 0;border-bottom:1px dashed var(--line)" data-in="{t}" data-on="{t},{t2}"><span style="font-size:44px;font-weight:700">{lbl}</span><span class="te0 gold" style="font-size:56px">{val}</span></div>'
add(401.8, 419.2, f'''
<div class="box" style="position:absolute;left:120px;top:170px;width:820px;padding:0;overflow:hidden" data-in="401.9">
 <div style="height:54px;background:rgba(243,238,228,.07);display:flex;align-items:center;gap:12px;padding:0 22px"><i style="width:14px;height:14px;border-radius:50%;background:#6b625a"></i><i style="width:14px;height:14px;border-radius:50%;background:#6b625a"></i><i style="width:14px;height:14px;border-radius:50%;background:#6b625a"></i>
  <span style="font-family:IBM Plex Mono;font-size:20px;color:var(--gray);margin-left:20px">telanganatoday.com</span></div>
 <div style="padding:40px 44px;position:relative"><div class="eyebrow">TELANGANA TODAY · 14 NOV 2025</div>
  <div style="font-size:44px;font-weight:800;line-height:1.35;margin-top:20px;position:relative">కరీంనగర్: lottery గెలిచిన కొత్త వాళ్ళ దగ్గర నుంచి <span style="position:relative">syndicates shops తీసుకుంటున్నాయి<span class="rule" style="position:absolute;left:0;bottom:-6px;width:100%;height:5px" data-draw="{w("s85","syndicates")},.7"></span></span></div>
  <div style="font-size:28px;color:var(--gray);margin-top:24px">Report summary · Telugu paraphrase</div></div></div>
<div style="position:absolute;left:1020px;top:220px"><div class="eyebrow te" data-in="{a86-.3}">— ఒక్క shop కోసం ఇచ్చిన ధర</div>{rows}</div>
{src("TELANGANA TODAY · 14 NOV 2025")}''', cls="dark", xf=0.25)
add(419.2, 427.0, lt(("₹3 లక్షల application", 419.3),
    f'<div class="row" style="align-items:baseline" data-in="{w("s89","కోటి")}"><span class="te0" style="font-size:60px">కొందరికి →</span><span class="big gold" style="font-size:170px">₹1 <span class="te0" style="font-size:110px">కోటి</span>+</span></div>'
    f'<div style="margin-top:20px" data-in="{w("s90","అందుకే")}"><span class="pill gold">అందుకే ఒక్కరే 100 applications</span></div>'), "rupee:0", "in")
a92, a93 = w("s92", "ఐదు"), w("s93", "మూడు")
add(427.0, 448.0, f'''<div style="{BOX}">
 <div class="eyebrow te" data-in="427.2">— Demand కూడా తగ్గడం లేదు</div>
 <div data-in="{w("s92","December")}" style="margin-top:60px"><div style="font-size:44px;font-weight:700">DEC 2025 · కొత్త shops మొదటి నెల · తెలంగాణ మద్యం అమ్మకాలు</div>
  <div class="row" style="align-items:baseline;margin-top:10px">{cnt(5100, a92, 1.3, pre="₹", cls="gold", size=180, inn=False)}{te(" కోట్లు","gold").replace('class="te0','style="font-size:70px" class="te0')}<span class="pill gold" data-in="{w("s92","record")}" style="margin-left:30px">RECORD</span></div></div>
 <div data-in="{w("s93","December")}" style="margin-top:60px"><div style="font-size:44px;font-weight:700">30 DEC · ఒక్క రోజే</div>
  <div class="row" style="align-items:baseline;margin-top:10px">{cnt(375, a93, 1.0, pre="₹", size=140, inn=False)}{te(" కోట్లు").replace('class="te0','style="font-size:60px" class="te0')}</div></div>
 <div style="margin-top:50px" data-in="{w("s94","పెద్ద")}"><span class="pill red">పెద్ద భాగం ఎక్కడికి? → ప్రభుత్వానికి</span></div>
</div>{src("THE HANS INDIA · JAN 2026")}''', cls="dark", xf=0.25)
# ---- chapter 5 ----
chapter(448.0, 453.3, 5, "ఆంధ్రప్రదేశ్")
add(453.3, 458.8, lt(("AP · 2024", 453.4), f'<div class="head" data-in="{w("s96","private")}">Private wine shops <span class="gold">మళ్ళీ వచ్చాయి</span></div>', "DECCAN CHRONICLE · SEP 2024"), "andhra:3", "in")
a97, a98, a99, a100 = w("s97", "ఇరవై"), w("s98", "పది"), w("s99", "పదమూడున్నర"), w("s100", "నలభై")
def mrow(lbl, v, col, t, top):
    return f'''<div data-in="{t-.3}" style="margin-top:{top}px"><div style="font-size:44px;font-weight:700">{lbl}</div>
  <div class="row" style="margin-top:12px"><div class="bar" style="width:{1100*v/20:.0f}px;background:{col}" data-draw="{t},.9"></div>{cnt(v, t, .9, suf="%", d=1 if v % 1 else 0, size=84, inn=False)}</div></div>'''
add(458.8, 480.0, f'''<div style="{BOX}">
 <div class="eyebrow te" data-in="459">— AP shops కి margin</div>
 {mrow("Policy లో రాసింది", 20, "var(--gray)", a97, 60)}
 {mrow("మొదట్లో వచ్చింది", 10.5, "var(--red)", a98, 44)}
 {mrow("Aug 2026 · traders చెప్పింది", 13.5, "var(--gold)", a99, 44)}
 <div class="row" style="margin-top:50px;align-items:baseline" data-in="{a100}">{cnt(40, a100, .9, pre="~", suf="%", cls="red", size=120, inn=False)}<span style="font-size:48px;font-weight:700">shops నష్టాల్లో <span class="gray" style="font-size:34px">· associations</span></span></div>
</div>{src("DECCAN CHRONICLE · M9 NEWS · AABKARI TIMES")}''', cls="dark", xf=0.25)
a102, a103 = w("s102", "ఎనిమిది"), w("s103", "ఐదు")
dots = "".join(f'<div style="width:46px;height:46px;border-radius:50%;background:{"var(--red)" if (i*37)%100 < 22 else "rgba(243,238,228,.22)"}" data-in="{(a102 + .4 + i*0.01) if (i*37)%100 < 22 else (w("s102","మూడు") + i*0.008)}"></div>' for i in range(100))
add(480.0, 492.0, f'''<div style="{BOX}">
 <div class="eyebrow te" data-in="480.1">— ఫలితం · AP</div>
 <div class="row" style="margin-top:50px;gap:80px;align-items:flex-start">
  <div style="display:grid;grid-template-columns:repeat(10,46px);gap:14px">{dots}</div>
  <div><div class="row" style="align-items:baseline" data-in="{a102}">{cnt(807, a102, 1, cls="red", size=170, inn=False)}<span class="big gray" style="font-size:80px">/ 3,736</span></div>
   <div style="font-size:44px;font-weight:700;margin-top:10px" data-in="{a102}">shops renew కాలేదు / నడవడం లేదు</div>
   <div class="big gold" style="font-size:150px;margin-top:60px" data-pop="{a103}">1 in 5</div></div></div>
</div>{src("DECCAN CHRONICLE · SEP 2026")}''', cls="dark", xf=0.25)
add(492.0, 497.5, lt(("Margin లో కొన్ని శాతాల తేడా", 492.1), f'<div class="head" data-in="{w("s104","business")}"><span class="gold">లాభం</span> → <span class="red">నష్టం</span></div>'), "andhra:7", "in")
# ---- chapter 6 ----
chapter(497.5, 500.0, 6, "ఫైనల్ లెక్క")
add(500.0, 506.0, lt(("Wine shop అంటే", 500.1), f'<div class="head" data-in="{w("s106","shop")}">ఒక shop కాదు.</div><div class="head" data-in="{w("s106","ప్రభుత్వంతో")}">ప్రభుత్వంతో <span class="gold">పెద్ద పందెం</span></div>'), "liquor2:0", "in")
a107, a108 = w("s107", "Application"), w("s108", "Shop")
pills = "".join(f'<div style="margin-top:22px" data-in="{w("s107",k)}"><span class="pill gold" style="font-size:38px">✓ {k}</span></div>' for k in ["Application", "tax", "bank"])
pills = pills.replace("✓ Application", "✓ Application fee").replace("✓ tax", "✓ Excise tax").replace("✓ bank", "✓ Bank guarantee")
add(506.0, 517.3, f'''<div style="{BOX}"><div class="row" style="gap:80px;align-items:flex-start">
 <div class="box" style="width:740px;padding:50px;border-color:var(--gold)" data-in="506.1"><div class="eyebrow te">— ప్రభుత్వానికి</div>
  <div class="big gold" style="font-size:110px;margin-top:20px">100%</div><div style="font-size:40px;font-weight:700">ముందే గ్యారంటీ · advance లో</div>{pills}</div>
 <div class="box" style="width:740px;padding:50px" data-in="{a108}"><div class="eyebrow te">— Shop ఓనర్‌కి</div>
  <div class="big red" style="font-size:110px;margin-top:20px">?</div><div style="font-size:48px;font-weight:700;margin-top:10px">అమ్మకాలు <span class="gold">బాగుంటేనే</span> లాభం</div></div>
</div></div>''', cls="dark", xf=0.25)
add(517.3, 523.6, lt(("Location", 517.4), f'<div class="head" data-in="{w("s109","మంచి")}">మంచి location → <span class="gold">కోట్లు</span></div><div class="head" data-in="{w("s109","తప్పు")}">తప్పు location → <span class="red">లక్షల్లో నష్టం</span></div>'), "village:5", "r")
add(523.6, 529.2, lt(("₹3 లక్షల application వేసే ముందు", 523.7), f'<div class="head" data-in="{w("s110","ఈ")}">ఈ <span class="gold">లెక్క</span> ఒక్కసారి గుర్తు పెట్టుకోండి</div>'), "lottery:3", "in")
add(529.2, 534.9, f'''<div class="center"><div class="eyebrow" data-in="529.3">— COMMENT లో చెప్పండి</div>
 <div class="box" style="padding:50px 70px;margin-top:30px;max-width:1400px" data-in="{w("s111","మీ")}"><div class="head" style="font-size:72px">మీ ఊర్లో wine shop lottery కి <span class="gold">ఎంత మంది</span> apply చేశారు?</div></div></div>''', "crowd:2", "in", full=True)
add(534.9, END, f'''<div class="center"><div class="head" style="font-size:64px" data-in="{w("s112","ఇలాంటి")}">ఇలాంటి నిజమైన <span class="gold">business లెక్కల</span> కోసం</div>
 <div style="margin-top:40px" data-in="{w("s112","subscribe")}"><span class="pill gold" style="font-size:52px;padding:16px 50px">SUBSCRIBE</span></div>
 <div class="gray" style="font-size:48px;margin-top:50px" data-in="{w("s112","Next")}"><span class="ser">Next video</span> లో కలుద్దాం</div></div>''', cls="dark", xf=0.25)
