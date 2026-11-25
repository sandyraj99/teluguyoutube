# Script checker: run BEFORE sending the script for approval and BEFORE any voice generation.
# Catches the things that made EP03's voice sound "AI" (7:40 "సో, ఫైనల్ వెర్డిక్ట్"):
#   - banned English/announcer phrases (written in Telugu letters or Latin)
#   - Latin letters in narration (accent switching)
#   - too many English loanwords in one sentence
#   - a chapter (voice chunk) that STARTS with an English word or announcer phrase
#   - a "next video" tease that names the next topic (competitors copy topics)
# usage: python3 lint_script.py <episodeDir>     exit code 1 if any ERROR
import json, re, sys
ep = sys.argv[1]
S = json.load(open(f"{ep}/script.json"))

# Announcer / YouTuber English that sounds dubbed. Use the Telugu on the right instead.
BANNED = {
    "సో": "అంటే / మొత్తానికి / ఇక", "ఫైనల్": "చివరికి", "వెర్డిక్ట్": "మా తీర్పు / అసలు విషయం",
    "మ్యాజిక్": "అద్భుతం / మాయ", "వాల్యూమ్ గేమ్": "ఎక్కువ అమ్మితేనే లాభం", "వాల్యూమ్": "ఎక్కువ అమ్మకం",
    "సైలెంట్‌గా": "తెలియకుండానే / నిశ్శబ్దంగా", "సింపుల్": "చాలా తేలిక", "ఈజీ మనీ": "తేలిగ్గా వచ్చే డబ్బు",
    "ట్విస్ట్": "అసలు విషయం / ఊహించని ఖర్చు", "షాకింగ్": "ఆశ్చర్యం", "బిగ్": "పెద్ద", "ఫ్రెండ్స్": "(remove)",
    "హలో": "(remove: no greetings)", "గైస్": "(remove)", "ఓకే": "సరే", "బేసిక్‌గా": "అసలు", "ఎగ్జాక్ట్‌గా": "సరిగ్గా",
    "అండ్": "ఇంకా / , ", "బట్": "కానీ", "బికాజ్": "ఎందుకంటే", "ఫస్ట్": "ముందు / మొదట", "నెక్స్ట్ వీడియో": "(do not name the next topic)",
    "డైన్-ఇన్": "కూర్చుని తినే", "రియల్": "నిజమైన", "ఇంపార్టెంట్": "ముఖ్యం", "ఇంట్రెస్టింగ్": "ఆసక్తికరం",
}
# Everyday English words Telugu speakers really use. Allowed, but max 2 per sentence and none as a chunk's first word.
COMMON_EN = {"ప్లేట్", "ప్లేట్లు", "షాప్", "షాపు", "యాప్", "ఆర్డర్", "ఆర్డర్లు", "కమిషన్", "జీఎస్టీ", "రెంట్", "బిజినెస్", "కస్టమర్", "కస్టమర్లు",
    "పార్సిల్", "ప్యాకింగ్", "సిలిండర్", "కమర్షియల్", "మార్కెట్", "హోల్‌సేల్", "రిటైల్", "కౌంటర్", "కరెంట్", "లోన్", "ఈఎంఐ", "జాబ్", "సాఫ్ట్‌వేర్",
    "బైక్", "పెట్రోల్", "డెలివరీ", "హెల్పర్", "హెల్పర్లు", "మాస్టర్", "స్టవ్", "గ్యాస్", "బిల్లు", "బిల్లే", "కామెంట్", "వీడియో", "నంబర్", "మోడల్",
    "ఆయిల్", "సెల్లా", "బ్రాయిలర్", "లైవ్", "కటింగ్", "వాట్సాప్", "రిజిస్ట్రేషన్", "ఎఫ్ఎస్ఎస్ఏఐ", "అడ్వాన్స్", "షట్టర్",
    "టిష్యూ", "స్పూన్", "కవర్", "సబ్‌స్క్రిప్షన్", "రైడర్", "ట్రిక్", "గెస్", "స్క్రీన్", "ప్రీ", "రష్", "మ్యాచ్", "వేస్ట్", "జీరో", "డౌన్", "డబుల్", "రూల్స్"}
STRIP = lambda w: re.sub(r"[\s,.!?'\"’‘:;\-…()]", "", w)
def en_words(text):
    ws = [STRIP(w) for w in text.split()]
    base = lambda w: re.sub(r"(కి|లో|ని|ను|తో|దే|లే|కే|‌గా|గా|ల)$", "", w)
    return [w for w in ws if w in COMMON_EN or base(w) in COMMON_EN]

errors, warns = [], []
prev_scene = None
for l in S:
    t, sid = l["text"], l["id"]
    if re.search(r"[A-Za-z]", t): errors.append(f"{sid}: Latin letters in narration -> write in Telugu letters: {t}")
    for b, fix in BANNED.items():
        if re.search(rf"(^|[\s,.!?]){re.escape(b)}($|[\s,.!?‌]|గా|కి)", t): errors.append(f"{sid}: banned '{b}' -> {fix}: {t}")
    en = en_words(t)
    if len(en) > 2: warns.append(f"{sid}: {len(en)} English words {en} (max 2): {t}")
    if l["scene"] != prev_scene:  # first sentence of a chapter = start of a voice chunk
        first = STRIP(t.split()[0])
        if en and first in en: errors.append(f"{sid}: chapter starts with English word '{first}' -> start with plain Telugu")
        if len(en) > 1: warns.append(f"{sid}: chapter's first sentence should be pure Telugu (has {en})")
    if re.search(r"(నెక్స్ట్|తర్వాతి|తదుపరి)\s*(వీడియో|ఎపిసోడ్)", t) and len(t) > 40:
        warns.append(f"{sid}: looks like a next-video tease; never name the next topic: {t}")
    prev_scene = l["scene"]
for e in errors: print("ERROR ", e)
for w in warns: print("WARN  ", w)
print(f"{len(S)} sentences · {len(errors)} errors · {len(warns)} warnings")
sys.exit(1 if errors else 0)
