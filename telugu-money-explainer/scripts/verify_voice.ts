// Re-checks a finished voice track sentence by sentence using timeline.json.
// Cuts every sentence out of audio/voice.wav, transcribes it, and flags mismatches
// (a mismatch usually means a wrong alignment boundary or a mispronounced word).
// Usage: bun scripts/verify_voice.ts <episodeDir>
import "./common.ts";
import { similarity, transcribeTelugu } from "./common.ts";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
const ep = process.argv[2];
const tl = JSON.parse(await readFile(`${ep}/timeline.json`, "utf8"));
let bad = 0;
for (const l of tl.lines) {
  const out = `/tmp/verify_${l.id}.wav`;
  spawnSync("ffmpeg", ["-nostdin", "-loglevel", "error", "-y", "-ss", String(Math.max(0, l.start)), "-to", String(l.end), "-i", `${ep}/audio/voice.wav`, out]);
  const tx = await transcribeTelugu(new Uint8Array(await readFile(out)), "a.wav");
  const s = similarity(l.text, tx);
  const flag = s < 0.9 ? "  <-- CHECK" : "";
  if (flag) bad++;
  console.log(`${l.id} ${s.toFixed(2)}${flag}\n   want: ${l.text}\n   got:  ${tx}`);
}
console.log(bad ? `${bad} sentence(s) need attention.` : "All sentences match.");
