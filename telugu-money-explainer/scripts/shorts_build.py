# Builds each Short: cuts segments from the final 16:9 episode (same voice+music mix), places it at y=470 on the
# dark base, adds the headline and timed number cards, fades, AAC 192k. ~2 min per 40 s Short on 2 CPUs.
# usage: python3 shorts_build.py <spec.json> <final.mp4> <png_dir> <out_dir> [name ...]
import json, subprocess, sys
SPEC, SRC, PNG, OUT = sys.argv[1:5]; ONLY = sys.argv[5:]
SH = json.load(open(SPEC))
for s in SH:
    if ONLY and s["name"] not in ONLY: continue
    d = f"{PNG}/{s['name']}"; segs = s["segs"]; T = round(sum(b - a for a, b in segs), 3)
    ins = ["-i", SRC, "-loop", "1", "-i", f"{d}/base.png", "-loop", "1", "-i", f"{d}/top.png"]
    for i in range(len(s["cards"])): ins += ["-loop", "1", "-i", f"{d}/card{i}.png"]
    f = []
    for k, (a, b) in enumerate(segs):
        f.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,scale=1080:608:flags=lanczos[v{k}]")
        f.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.06,afade=t=out:st={b-a-0.08:.3f}:d=0.08[a{k}]")
    n = len(segs)
    f.append("".join(f"[v{k}][a{k}]" for k in range(n)) + f"concat=n={n}:v=1:a=1[vc][ac0]")
    f.append(f"[ac0]afade=t=in:d=0.15,afade=t=out:st={T-0.5:.3f}:d=0.5[aout]")
    f.append(f"[1:v]trim=0:{T},setpts=PTS-STARTPTS,fps=30,format=yuv420p[bg]")
    f.append("[bg][vc]overlay=0:470:shortest=1[x0]")
    f.append(f"[2:v]trim=0:{T},fade=in:st=0:d=0.3:alpha=1[top]")
    f.append("[x0][top]overlay=0:0[x1]")
    last = "x1"
    for i, (t0, t1, slot, html) in enumerate(s["cards"]):
        t1 = min(t1, T)
        f.append(f"[{i+3}:v]format=rgba,trim=0:{T},setpts=PTS-STARTPTS,fade=in:st={t0:.3f}:d=0.25:alpha=1[c{i}]")
        f.append(f"[{last}][c{i}]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[y{i}]"); last = f"y{i}"
    f.append(f"[{last}]fade=in:st=0:d=0.2,fade=out:st={T-0.4:.3f}:d=0.4,format=yuv420p[vout]")
    out = f"{OUT}/{s['name']}.mp4"
    cmd = ["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(f), "-map", "[vout]", "-map", "[aout]", "-t", str(T),
           "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True); print("done", out, T)
