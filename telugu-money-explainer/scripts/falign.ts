// ElevenLabs forced alignment per chunk -> word timings (absolute in voice.wav)
import "./common.ts";
import { readFile, writeFile } from "node:fs/promises";
const ep = process.argv[2];
const ch = JSON.parse(await readFile(`${ep}/audio/chunks.json`, "utf8")).chunks;
const { spawnSync } = await import("node:child_process");
const out: any[] = [];
for (const [i, c] of ch.entries()) {
  // trimmed chunk exactly as placed in voice.wav
  const f = `/tmp/fa_${i}.wav`;
  spawnSync("ffmpeg", ["-nostdin", "-loglevel", "error", "-y", "-ss", String(c.offset), "-t", String(c.duration), "-i", `${ep}/audio/voice.wav`, "-ac", "1", "-ar", "16000", f]);
  const fd = new FormData();
  fd.append("file", new Blob([await readFile(f)], { type: "audio/wav" }), "a.wav");
  fd.append("text", c.text);
  const r = await fetch("https://api.elevenlabs.io/v1/forced-alignment", { method: "POST", headers: { "xi-api-key": process.env.ELEVENLABS_API_KEY! }, body: fd });
  const j: any = await r.json();
  if (!r.ok) { console.error(r.status, JSON.stringify(j).slice(0, 300)); process.exit(1); }
  out.push({ offset: c.offset, ids: c.ids, words: j.words.map((w: any) => ({ text: w.text, start: +(w.start + c.offset).toFixed(3), end: +(w.end + c.offset).toFixed(3) })), loss: j.loss });
  console.log(`chunk ${i + 1}: ${j.words.length} words, loss ${j.loss}`);
}
await writeFile(`${ep}/audio/words.json`, JSON.stringify(out));
