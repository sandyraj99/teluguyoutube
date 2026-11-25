// Shorts overlays (1080x1920 PNGs): base, headline, one PNG per number card.
// usage: node shorts_overlays.mjs <spec.json> <png_dir>   (spec format: templates/shorts_spec_example.py)
import { chromium } from "/usr/local/lib/node_modules/playwright/index.mjs";
import { readFileSync, mkdirSync } from "node:fs";
const [SPEC, PNG = "png"] = process.argv.slice(2);
const SH = JSON.parse(readFileSync(SPEC, "utf8"));
const css = `
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;background:transparent;overflow:hidden;font-family:"Noto Sans Telugu";color:#f3eee4;-webkit-font-smoothing:antialiased}
.gold{color:#e2c27a}.red{color:#e0594d}.sage{color:#9fc18e}.gray{color:#8f877b}
.base{position:absolute;inset:0;background:radial-gradient(ellipse 120% 70% at 50% 35%,#211d19,#0c0b0a 75%)}
.base::after{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.035) 1px,transparent 1px);background-size:4px 4px}
.frame{position:absolute;left:0;top:467px;width:1080px;height:614px;border-top:3px solid #c9a24a;border-bottom:3px solid #c9a24a}
.top{position:absolute;left:60px;right:60px;top:120px;text-align:center}
.eb{font-family:"IBM Plex Mono";font-size:26px;letter-spacing:.2em;color:#8f877b;font-weight:600;margin-bottom:26px}
.h1{font-weight:800;font-size:84px;line-height:1.2}
.h2{white-space:nowrap;font-weight:900;font-size:90px;line-height:1.25}
.slot{position:absolute;left:60px;right:60px}
.card{background:rgba(28,25,22,.92);border:1px solid rgba(243,238,228,.16);border-left:8px solid #c9a24a;border-radius:18px;padding:18px 34px 22px}
.lab{font-size:34px;font-weight:700;color:#b9b0a2}
.q{font-size:52px;font-weight:800}
.num{font-family:Inter,"Noto Sans Telugu";font-weight:900;letter-spacing:-.01em;line-height:1.15;font-variant-numeric:tabular-nums}
.verdict{text-align:center;font-weight:900;font-size:68px;padding-top:6px}
.qrow{display:flex;align-items:center;gap:26px;background:rgba(28,25,22,.92);border:1px solid rgba(243,238,228,.16);border-radius:16px;padding:12px 26px;height:106px}
.qn{flex:none;width:70px;height:70px;border-radius:50%;background:#c9a24a;color:#14110e;font:900 44px Inter;display:flex;align-items:center;justify-content:center}
.qt{font-size:42px;font-weight:800;line-height:1.2}.qs{font-size:28px;font-weight:600;color:#9fc18e;line-height:1.25}
`;
const fonts = `<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Telugu:wght@600;700;800;900&family=Inter:wght@700;800;900&family=IBM+Plex+Mono:wght@600&display=block" rel="stylesheet">`;
const br = await chromium.launch(); const p = await br.newPage({ viewport: { width: 1080, height: 1920 } });
async function shot(body, out, bg = false) {
  await p.setContent(`<!doctype html><html lang="te"><head><meta charset="utf-8">${fonts}<style>${css}</style></head><body>${body}</body></html>`, { waitUntil: "networkidle" });
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(150);
  await p.screenshot({ path: out, omitBackground: !bg });
}
for (const s of SH) {
  const d = `${PNG}/${s.name}`; mkdirSync(d, { recursive: true });
  await shot(`<div class="base"></div><div class="frame"></div>`, `${d}/base.png`, true);
  await shot(`<div class="top"><div class="eb">REAL NUMBERS · <span style="letter-spacing:0;font-family:Noto Sans Telugu">${s.tag || ""}</span></div><div class="h1">${s.top[0]}</div><div class="h2">${s.top[1]}</div></div>`, `${d}/top.png`);
  const pitch = s.list ? 120 : 188;
  for (const [i, c] of s.cards.entries())
    await shot(`<div class="slot" style="top:${1120 + c[2] * pitch}px">${c[3]}</div>`, `${d}/card${i}.png`);
}
await br.close(); console.log("ok");
