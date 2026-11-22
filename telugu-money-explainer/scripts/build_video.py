# Renders the episode: per-shot segments (Ken Burns photo + grade + overlays) -> concat -> mux with mix.
# Usage: python3 build_video.py <episodeDir> [--only N] [--preview a:b]   (preview: render shots a..b only)
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
EP = sys.argv[1]; FPS = 30
TL = json.load(open(f"{EP}/timeline.json")); DUR = TL["duration"]
EDL = json.load(open(f"{EP}/edl.json")); MAN = json.load(open(f"{EP}/footage/candidates.json"))
CUES = json.load(open(f"{EP}/graphics/cues.json"))
SEG = f"{EP}/out/seg"; os.makedirs(SEG, exist_ok=True); os.makedirs(f"{EP}/out/pre", exist_ok=True)
PNG = lambda gid: f"{EP}/graphics/png/{gid}.png"

# ---- cue clean-up: no gaps/overlaps between consecutive cards, end card to the end ----
cards = sorted([c for c in CUES if c["kind"] in ("card", "full")], key=lambda c: c["start"])
for a, b in zip(cards, cards[1:]):
    if b["start"] < a["end"] or b["start"] - a["end"] < 1.2: a["end"] = b["start"]
for c in cards:
    if c["id"] == "end": c["end"] = DUR
subs = [c for c in CUES if c["kind"] == "sub"]
brand = {"id": "brand", "start": 0, "end": DUR, "fade": 0}
LAYERS = [brand] + cards + subs  # draw order

# ---- frame-exact shot boundaries ----
fr = lambda t: int(round(t * FPS))
for i, s in enumerate(EDL):
    s["f0"] = fr(s["start"]); s["f1"] = fr(EDL[i + 1]["start"]) if i + 1 < len(EDL) else fr(DUR)

def prescale(src):
    k, i = src.split(":"); f = MAN[k][int(i)]["file"]
    out = f"{EP}/out/pre/{k}_{i}.png"
    if not os.path.exists(out):
        subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", f, "-vf",
                        "scale=2112:1188:force_original_aspect_ratio=increase:flags=lanczos,crop=2112:1188", "-frames:v", "1", out], check=True)
    return out

def move_filter(move, D):
    p = f"(t/{D:.3f})"
    # zoom moves: scale grows/shrinks per frame (sub-pixel smooth), then crop 1920x1080
    if move in ("in", "inR", "out"):
        z = f"(1+0.075*{p})" if move != "out" else f"(1.075-0.075*{p})"
        xx = "(iw-1920)/2" if move != "inR" else "(iw-1920)*0.72"
        return f"scale=w='trunc(1920*{z}/2)*2':h='trunc(1080*{z}/2)*2':eval=frame:flags=bicubic,crop=1920:1080:'{xx}':'(ih-1080)/2'"
    if move == "panL":  # camera moves left -> crop x decreases
        return f"scale=2032:1143,crop=1920:1080:'(iw-1920)*(1-{p})':'(ih-1080)/2'"
    return f"scale=2032:1143,crop=1920:1080:'(iw-1920)*{p}':'(ih-1080)/2'"

GRADE = "eq=contrast=1.05:saturation=0.93,colorbalance=rs=0.025:bs=-0.025:rm=0.02:bm=-0.02,vignette=angle=PI/5.5,noise=alls=3:allf=t"

def render(i):
    s = EDL[i]; out = f"{SEG}/{i:03d}.mp4"
    if os.path.exists(out) and not os.environ.get("FORCE"): return out
    n = s["f1"] - s["f0"]; T0 = s["f0"] / FPS; T1 = s["f1"] / FPS; D = n / FPS
    img = prescale(s["src"])
    args = ["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-t", f"{D + 0.2:.3f}", "-i", img]
    filt = f"[0:v]{move_filter(s['move'], D)},{GRADE}[b0];"
    cur = "b0"; k = 1
    for c in LAYERS:
        a, b = c["start"], c["end"]
        if b <= T0 or a >= T1: continue
        la, lb = max(0.0, a - T0), min(D + 0.2, b - T0)
        args += ["-loop", "1", "-framerate", str(FPS), "-t", f"{D + 0.2:.3f}", "-i", PNG(c["id"])]
        fx = "format=rgba"
        if c.get("fade") and a >= T0: fx += f",fade=t=in:st={la:.3f}:d={c['fade']}:alpha=1"
        filt += f"[{k}:v]{fx}[o{k}];[{cur}][o{k}]overlay=0:0:enable='between(t,{la:.3f},{lb:.3f})'[c{k}];"
        cur = f"c{k}"; k += 1
    filt += f"[{cur}]format=yuv420p[v]"
    args += ["-filter_complex", filt, "-map", "[v]", "-frames:v", str(n), "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-x264-params", "keyint=60", out]
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode: raise RuntimeError(f"shot {i}: {r.stderr[-800:]}")
    return out

if __name__ == "__main__":
    rng = range(len(EDL))
    if "--preview" in sys.argv:
        a, b = map(int, sys.argv[sys.argv.index("--preview") + 1].split(":")); rng = range(a, b + 1)
    with ThreadPoolExecutor(max_workers=2) as ex:
        for j, o in enumerate(ex.map(render, rng)): print("seg", o, flush=True)
    if "--preview" in sys.argv: sys.exit(0)
    with open(f"{SEG}/list.txt", "w") as f:
        for i in range(len(EDL)): f.write(f"file '{i:03d}.mp4'\n")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{SEG}/list.txt", "-c", "copy", f"{EP}/out/video_noaudio.mp4"], check=True)
    print("concat done")
