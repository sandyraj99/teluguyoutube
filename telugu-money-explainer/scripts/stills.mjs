import { chromium } from "/usr/local/lib/node_modules/playwright/index.mjs";
import { readFileSync } from "node:fs";
const [ep, outdir, ...ts] = process.argv.slice(2);
const scenes = JSON.parse(readFileSync(`${ep}/graphics/scenes.json`, "utf8"));
const br = await chromium.launch({ args: ["--allow-file-access-from-files"] });
const p = await br.newPage({ viewport: { width: 1920, height: 1080 } });
await p.goto("file:///home/user/workspace/backend/tools/telugu/engine.html");
await p.evaluate(sc => window.setup(sc), scenes); await p.evaluate(() => document.fonts.ready);
await p.evaluate(() => Promise.all([...document.querySelectorAll('.photo')].map(d => new Promise(r => { const i = new Image(); i.onload = i.onerror = r; i.src = d.style.backgroundImage.slice(5, -2); }))));
for (const t of ts) { await p.evaluate(t => window.at(t), +t); await p.screenshot({ path: `${outdir}/st_${t}.jpg`, type: "jpeg", quality: 80 }); }
await br.close();
