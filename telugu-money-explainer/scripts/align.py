# Sentence timeline from voice.wav: per chunk, choose N-1 pauses that best match length-proportional positions (DP).
import json, re, subprocess, sys
ep = sys.argv[1]
script = json.load(open(f"{ep}/script.json")); byid = {l["id"]: l for l in script}
ch = json.load(open(f"{ep}/audio/chunks.json"))["chunks"]
def silences(path, start, dur):
    out = subprocess.run(["ffmpeg","-nostdin","-ss",str(start),"-t",str(dur),"-i",path,"-af","silencedetect=n=-38dB:d=0.12","-f","null","-"],capture_output=True,text=True).stderr
    s = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]; e = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    return [(a+start, b+start) for a, b in zip(s, e)]
lines = []
for c in ch:
    ids = c["ids"]; t0 = c["offset"]; t1 = t0 + c["duration"]
    sil = [p for p in silences(f"{ep}/audio/voice.wav", t0, c["duration"]) if p[0] > t0 + 0.3 and p[1] < t1 - 0.2]
    w = [len(byid[i]["text"]) + 8 for i in ids]; tot = sum(w)
    exp = []; acc = 0
    for x in w[:-1]: acc += x; exp.append(t0 + (t1 - t0) * acc / tot)
    n, m = len(exp), len(sil)
    INF = 1e18
    # dp[i][j]: best cost assigning first i boundaries using pauses < j
    cost = lambda i, j: (((sil[j][0]+sil[j][1])/2 - exp[i])**2) / 4 - 3.0 * min(sil[j][1]-sil[j][0], 0.8)
    dp = [[INF]*(m+1) for _ in range(n+1)]; bk = [[None]*(m+1) for _ in range(n+1)]
    for j in range(m+1): dp[0][j] = 0
    for i in range(1, n+1):
        for j in range(1, m+1):
            dp[i][j] = dp[i][j-1]; bk[i][j] = bk[i][j-1]
            v = dp[i-1][j-1] + cost(i-1, j-1)
            if v < dp[i][j]: dp[i][j] = v; bk[i][j] = (j-1)
    assert m >= n, f"chunk {c['file']}: {m} pauses for {n} boundaries"
    # backtrack
    picks = []; i, j = n, m
    while i > 0:
        p = bk[i][j]; picks.append(p); i -= 1; j = p
    picks = picks[::-1]
    bounds = [sil[p] for p in picks]
    st = t0
    for k, id_ in enumerate(ids):
        if k < n: en = bounds[k][0] + 0.05; nxt = bounds[k][1] - 0.05
        else: en = t1; nxt = None
        lines.append({"id": id_, "section": byid[id_]["section"], "text": byid[id_]["text"], "start": round(st, 3), "end": round(en, 3)})
        st = nxt if nxt is not None else st
dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"{ep}/audio/voice.wav"],capture_output=True,text=True).stdout)
json.dump({"duration": dur, "lines": lines}, open(f"{ep}/timeline.json","w"), ensure_ascii=False, indent=1)
for l in lines: print(l["id"], l["start"], l["end"], round(l["end"]-l["start"],2), len(l["text"]), round(len(l["text"])/(l["end"]-l["start"]),1))
