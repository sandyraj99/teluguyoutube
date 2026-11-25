# EP04 (gold) Shorts spec - the reference. Copy to episodes/<slug>/shorts_spec.py, edit, run: python3 shorts_spec.py -> shorts_spec.json
# segs: (src_start, src_end) in the FINAL video, taken from timeline.json line times (start-0.2 .. end+0.2).
# cards: (out_t_in, out_t_out, slot, html) in OUTPUT seconds. For a later segment: out = src + offset (offset = output start - src start).
# slot = vertical position (0..3 for cards, 0..4 when list=True). Numbers must match model.json.
import json
# segments: (src_start, src_end) cut from final.mp4 ; cards: (out_t_in, out_t_out, slot, html)
def row(label, val, cls="gold", size=84):
    return f'<div class="card"><div class="lab">{label}</div><div class="num {cls}" style="font-size:{size}px">{val}</div></div>'
SH = []
# Short 1: hook + resale twist
segs = [(0.0, 18.4), (209.6, 217.9), (224.8, 230.1), (218.1, 222.7)]
SH.append(dict(name="Short1_Gold_resale", tag="బంగారం", segs=segs,
  top=('ఒక తులం హారం', 'మరుసటి రోజే <span class="gold">అమ్మితే?</span>'),
  cards=[
    (2.4, 13.8, 0, row("షాప్ బిల్లు", "₹1,35,156")),
    (13.8, 18.4, 0, '<div class="card"><div class="q">మీ అంచనా ఎంత?</div><div class="num gray" style="font-size:84px">₹ ? ? ?</div></div>'),
    (18.6, 36.5, 0, row("చేతికి వచ్చేది", "₹1,13,645", "sage")),
    (22.4, 36.5, 1, row("ఒక్క రాత్రిలో నష్టం", "− ₹21,511", "red")),
    (26.9, 36.5, 2, '<div class="card"><div class="lab">నష్టం పూడాలంటే ధర</div><div class="num gold" style="font-size:84px">+19% పెరగాలి</div></div>'),
  ]))
# Short 2: who gets what
segs = [(147.1, 151.8), (153.6, 186.9)]
o = 4.7 - 153.6  # out = src + o for 2nd segment
SH.append(dict(name="Short2_Gold_who_gets_what", tag="బంగారం", segs=segs,
  top=('₹1,35,156 బిల్లు', '<span class="gold">ఎవరికి ఎంత?</span>'),
  cards=[
    (0.2, 4.7, 0, row("మొత్తం బిల్లు · 10 g హారం", "₹1,35,156")),
    (158.0+o, 37.9, 0, row("అసలు బంగారం (బయటి దేశం)", "₹1,01,878", "gold", 76)),
    (162.2+o, 37.9, 1, row("దుకాణం (తరుగు 12% · అంచనా)", "₹14,059", "sage", 76)),
    (167.1+o, 37.9, 2, row("ప్రభుత్వం (సుంకం ₹15,282 + GST ₹3,937)", "₹19,218", "red", 76)),
    (176.3+o, 37.9, 3, '<div class="verdict">ప్రభుత్వం <span class="red">&gt;</span> దుకాణం</div>'),
  ]))
# Short 3: 5 questions
segs = [(2.4, 6.0), (275.6, 311.1), (329.7, 333.8)]
o = 3.6 - 275.6
qs = [(275.8, "తులం = ఎన్ని గ్రాములు?", "బిల్లులో గ్రాములే రాయించండి"),
      (282.6, "ఈ రోజు 22K ధర ఎంత?", ""),
      (287.3, "తరుగు ఎంత శాతం?", "1% తగ్గినా ≈ ₹1,200 మిగులు"),
      (297.3, "హాల్‌మార్క్ HUID కోడ్ ఉందా?", "6 అక్షరాల కోడ్"),
      (304.7, "రేపు అమ్మితే ఎంత తగ్గిస్తారు?", "కాగితం మీద రాయించండి")]
cards = [(0.2, 3.6, 0, row("ఒక తులం హారం బిల్లు", "≈ ₹1,35,000"))]
for i, (t, q, sub) in enumerate(qs):
    cards.append((t+o, 39.1, i, f'<div class="qrow"><span class="qn">{i+1}</span><div><div class="qt">{q}</div>' + (f'<div class="qs">{sub}</div>' if sub else '') + '</div></div>'))
cards.append((39.1, 43.2, 0, '<div class="card"><div class="q">మీ ఊర్లో తరుగు ఎంత?</div><div class="num gold" style="font-size:64px">కామెంట్‌లో చెప్పండి</div></div>'))
SH.append(dict(name="Short3_Gold_5_questions", tag="బంగారం", segs=segs, list=True,
  top=('నగల షాప్‌లో', 'అడగాల్సిన <span class="gold">5 ప్రశ్నలు</span>'), cards=cards))
json.dump(SH, open("shorts_spec.json", "w"), ensure_ascii=False, indent=1)
for s in SH: print(s["name"], round(sum(b-a for a,b in s["segs"]),1))
