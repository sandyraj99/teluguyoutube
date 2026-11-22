// Renders each graphic spec in gfx.json to a transparent 1920x1080 PNG using gfx.html.
import { chromium } from "/usr/local/lib/node_modules/playwright/index.mjs";
import { readFileSync, mkdirSync, existsSync } from "node:fs";
const ep = process.argv[2]; const only = process.argv[3];
const specs = JSON.parse(readFileSync(`${ep}/graphics/gfx.json`, "utf8"));
mkdirSync(`${ep}/graphics/png`, { recursive: true });
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
await p.goto("file:///home/user/workspace/backend/tools/telugu/gfx.html"); await p.evaluate(() => document.fonts.ready);
let n = 0;
for (const s of specs) {
  const f = `${ep}/graphics/png/${s.id}.png`;
  if (only ? !s.id.startsWith(only) : existsSync(f) && !process.env.FORCE) continue;
  await p.evaluate((spec) => window.draw(spec), s); await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: f, omitBackground: true }); n++;
}
await b.close(); console.log("rendered", n);
