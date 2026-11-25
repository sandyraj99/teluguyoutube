# Pitch stats of an audio file: median F0 and 10-90% F0 range for the first HEAD seconds and the whole file.
# usage: python3 voice_stats.py <file> [head_seconds]   -> JSON
import numpy as np, subprocess, sys, json
def load(f, t=None):
    a = ["ffmpeg", "-v", "error", "-i", f] + (["-t", str(t)] if t else []) + ["-ac", "1", "-ar", "16000", "-f", "s16le", "-"]
    return np.frombuffer(subprocess.run(a, capture_output=True).stdout, np.int16).astype(np.float32) / 32768
def st(x):
    N = 640; f = []
    for i in range(0, len(x) - N, N):
        fr = x[i:i + N]
        if np.sqrt((fr ** 2).mean()) < 0.03: continue
        fr = fr - fr.mean(); ac = np.correlate(fr, fr, "full")[N - 1:]; k = 53 + np.argmax(ac[53:228])
        if ac[k] > 0.4 * ac[0]: f.append(16000 / k)
    if len(f) < 10: return {"f0": 0, "range": 0}
    return {"f0": round(float(np.median(f)), 1), "range": round(float(np.percentile(f, 90) - np.percentile(f, 10)), 1)}
f = sys.argv[1]; h = float(sys.argv[2]) if len(sys.argv) > 2 else 12
print(json.dumps({"head": st(load(f, h)), "all": st(load(f))}))
