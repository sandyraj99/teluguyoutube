import json
sc={l["id"]:l for l in json.load(open("script.json"))}
W=json.load(open("audio/words.json")); old=json.load(open("timeline.json"))
lines=[]
for ch in W:
    ws=[w for w in ch["words"] if w["text"].strip()]
    need=sum(len(sc[i]["text"].split()) for i in ch["ids"])
    assert len(ws)==need, (ch["ids"][0], len(ws), need)
    k=0
    for i in ch["ids"]:
        n=len(sc[i]["text"].split()); seg=ws[k:k+n]; k+=n
        lines.append(dict(id=i, section=sc[i]["scene"], text=sc[i]["text"], start=round(seg[0]["start"]-0.04,3), end=round(seg[-1]["end"]+0.06,3)))
json.dump(dict(duration=old["duration"], lines=lines), open("timeline.json","w"), ensure_ascii=False, indent=1)
r=[(l["id"], round(len(l["text"])/(l["end"]-l["start"]),1)) for l in lines]
print("rates min/max", min(r,key=lambda x:x[1]), max(r,key=lambda x:x[1]))
print([x for x in r if x[1]<10 or x[1]>20])
