import { chromium } from "/usr/local/lib/node_modules/playwright/index.mjs";
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
await p.goto("file:///tmp/thumb.html"); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
await p.screenshot({ path: process.argv[2], type: "jpeg", quality: 92 }); await b.close();
