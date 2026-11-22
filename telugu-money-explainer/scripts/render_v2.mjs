// Renders scenes.json through engine.html frame by frame (JPEG) and pipes to ffmpeg.
// usage: node render_v2.mjs <ep> <t0> <t1> <out.mp4> [workers]
import { chromium } from "/usr/local/lib/node_modules/playwright/index.mjs";
import { readFileSync } from "node:fs";
import { spawn } from "node:child_process";
const [ep, a, b, out, nw = "2"] = process.argv.slice(2);
const FPS = 30, f0 = Math.round(+a * FPS), f1 = Math.round(+b * FPS);
const scenes = JSON.parse(readFileSync(`${ep}/graphics/scenes.json`, "utf8")).filter(s => s.end >= +a - 1 && s.start <= +b + 1);
const br = await chromium.launch({ args: ["--allow-file-access-from-files"] });
const N = +nw, per = Math.ceil((f1 - f0) / N);
const parts = await Promise.all([...Array(N)].map(async (_, k) => {
  const s = f0 + k * per, e = Math.min(f1, s + per); const file = `${out}.part${k}.mp4`;
  const p = await br.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto("file:///home/user/workspace/backend/tools/telugu/engine.html");
  await p.evaluate(sc => window.setup(sc), scenes);
  await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => Promise.all([...document.querySelectorAll('.photo')].map(d => new Promise(r => { const i = new Image(); i.onload = i.onerror = r; i.src = d.style.backgroundImage.slice(5, -2); }))));
  const ff = spawn("ffmpeg", ["-nostdin", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", String(FPS), "-c:v", "mjpeg", "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", file], { stdio: ["pipe", "inherit", "inherit"] });
  for (let f = s; f < e; f++) {
    await p.evaluate(t => window.at(t), f / FPS);
    const buf = await p.screenshot({ type: "jpeg", quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once("drain", r));
    if (k === 0 && (f - s) % 300 === 0) console.log(`frame ${f - s}/${e - s}`);
  }
  ff.stdin.end(); await new Promise(r => ff.on("close", r)); return file;
}));
await br.close();
console.log(parts.join("\n"));
