// Thumbnail (1280x720) in the approved reference style. Usage:
// node thumbnail.mjs <photo.jpg> <out.jpg> '<RED words>' '<BLACK words>' '<YELLOW question>' '<STRIP html, wrap numbers in <b>>' ['55% 0%' photo position]
import { chromium } from "/usr/local/lib/node_modules/playwright/index.mjs";
import { readFileSync, writeFileSync } from "node:fs";
import { resolve, dirname } from "node:path";
const [photo, out, red, black, yellow, strip, pos = "55% 0%"] = process.argv.slice(2);
const dir = dirname(new URL(import.meta.url).pathname);
const html = readFileSync(`${dir}/../templates/thumbnail.html`, "utf8").replace("{{PHOTO}}", "file://" + resolve(photo)).replace("{{POS}}", pos)
  .replace("{{RED}}", red).replace("{{BLACK}}", black).replace("{{YELLOW}}", yellow).replace("{{STRIP}}", strip);
const tmp = `/tmp/thumb_${Date.now()}.html`; writeFileSync(tmp, html);
const b = await chromium.launch({ args: ["--allow-file-access-from-files"] }); const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
await p.goto("file://" + tmp); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
await p.screenshot({ path: out, type: "jpeg", quality: 90 }); await b.close(); console.log("thumbnail", out);
