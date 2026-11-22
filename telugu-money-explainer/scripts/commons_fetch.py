# Search Wikimedia Commons for license-safe photos/videos, download candidates + manifest, build contact sheets.
import json, os, re, subprocess, sys, urllib.parse, urllib.request, html
UA = {"User-Agent": "AsaluLekkaVideoBot/1.0 (educational YouTube explainer; vibecode)"}
OK = re.compile(r"^(CC0|Public domain|PD.*|CC BY(-SA)? [1-4]\.0.*|CC BY(-SA)? 2\.5.*)$", re.I)
import time
def fetch(url, timeout=60):
    for a in range(6):
        try:
            time.sleep(0.6)
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(15 * (a + 1)); continue
            raise
    raise RuntimeError("429 retries exhausted")
def get(url): return json.loads(fetch(url))
def thumb(url, w):
    base, name = url.rsplit("/", 1)
    return base.replace("/commons/", "/commons/thumb/", 1) + f"/{name}/{w}px-{name}"
def search(q, kind, n):
    ft = "bitmap" if kind == "photo" else "video"
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({"action":"query","format":"json","generator":"search","gsrsearch":f"{q} filetype:{ft}","gsrnamespace":6,"gsrlimit":n*3,"prop":"imageinfo","iiprop":"url|size|extmetadata|mime","iiurlwidth":1920})
    d = get(u); out = []
    for p in sorted(d.get("query",{}).get("pages",{}).values(), key=lambda p: p.get("index",0)):
        ii = p["imageinfo"][0]; md = ii.get("extmetadata",{})
        lic = md.get("LicenseShortName",{}).get("value","")
        if not OK.match(lic.strip()): continue
        if kind == "photo" and (ii["width"] < 1280 or ii["width"] < ii["height"]): continue
        if kind == "video" and ii.get("width",0) < 1200: continue
        artist = re.sub("<[^>]+>","",html.unescape(md.get("Artist",{}).get("value",""))).strip()
        out.append({"title":p["title"],"license":lic,"artist":artist[:120],"page":ii["descriptionurl"],"url":(ii.get("thumburl") if ii["width"]>1920 else thumb(ii["url"],1280)) if kind=="photo" else ii["url"],"w":ii["width"],"h":ii["height"]})
        if len(out) >= n: break
    return out
if __name__ == "__main__":
    ep, qfile = sys.argv[1], sys.argv[2]
    Q = json.load(open(qfile)); man_p = f"{ep}/footage/candidates.json"
    man = json.load(open(man_p)) if os.path.exists(man_p) else {}
    for key, spec in Q.items():
        if key in man: continue
        kind = spec.get("kind","photo"); n = spec.get("n",6); res=[]
        for q in spec["q"]:
            try: res += search(q, kind, n)
            except Exception as e: print("ERR", key, e)
        seen=set(); res=[r for r in res if not (r["title"] in seen or seen.add(r["title"]))][:spec.get("max",8)]
        d = f"{ep}/footage/cand/{key}"; os.makedirs(d, exist_ok=True)
        for i, r in enumerate(res):
            ext = ".jpg" if kind=="photo" else os.path.splitext(r["url"])[1]
            f = f"{d}/{i}{ext}"
            try:
                urllib.request.urlretrieve if False else None
                open(f,"wb").write(fetch(r["url"], 180))
                r["file"] = f
            except Exception as e: print("DL fail", key, i, e)
        man[key] = [r for r in res if "file" in r]
        if not man[key]: del man[key]; print(key, 'EMPTY'); continue
        json.dump(man, open(man_p,"w"), ensure_ascii=False, indent=1)
        # contact sheet
        files = [r["file"] for r in man[key]]
        if files:
            inputs=[]; filt=""
            for i,f in enumerate(files):
                if kind=="video": inputs += ["-ss","3","-i",f]
                else: inputs += ["-i",f]
                filt += f"[{i}]scale=480:270:force_original_aspect_ratio=increase,crop=480:270,drawtext=text='{i}':fontsize=40:fontcolor=yellow:box=1:boxcolor=black:x=8:y=8[v{i}];"
            cols=4; layout="|".join(f"{(i%cols)*480}_{(i//cols)*270}" for i in range(len(files)))
            filt += "".join(f"[v{i}]" for i in range(len(files))) + (f"xstack=inputs={len(files)}:layout={layout}:fill=black" if len(files)>1 else "null")
            subprocess.run(["ffmpeg","-nostdin","-loglevel","error","-y",*inputs,"-filter_complex",filt,"-frames:v","1",f"{ep}/footage/sheet_{key}.jpg"])
        print(key, kind, len(man[key]), [r["license"] for r in man[key]])
