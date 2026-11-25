// Narration with ElevenLabs eleven_v3 in ONE consistent voice.
// Groups script sentences by scene into chunks (<= MAX chars), makes up to TAKES takes per chunk,
// transcribes each take, keeps the most accurate, then joins chunks with natural pauses.
// Usage: bun scripts/tts_elevenlabs.ts <episodeDir> [--voice roger|chris|<voiceId>] [--single]
//   --single  one request for the whole script (use for pilots of 90 s or less)
// Output: <ep>/audio/chunk_XX.mp3, <ep>/audio/voice.wav (48 kHz mono), <ep>/audio/chunks.json
import "./common.ts";
import { loadScript, similarity, transcribeTelugu } from "./common.ts";
import { mkdir, writeFile, readFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import { spawnSync } from "node:child_process";

const VOICES: Record<string, string> = { roger: "CwhRBWXzGAHq8TQ4Fs17", chris: "iP95p4xoKVk53GoZ742B", daniel: "onwK4e9ZLuTAKqWW03F9" };
const args = process.argv.slice(2);
const ep = args[0]; if (!ep) throw new Error("usage: tts_elevenlabs.ts <episodeDir> [--voice roger] [--single]");
const vArg = args[args.indexOf("--voice") + 1];
const voiceId = args.includes("--voice") ? (VOICES[vArg] ?? vArg) : VOICES.roger;
const single = args.includes("--single");
const KEY = process.env.ELEVENLABS_USER_KEY || process.env.ELEVENLABS_API_KEY;
const MAX = 1400, TAKES = +(process.env.TAKES || 4), PASS = 0.93, SEED = 4242 + +(process.env.SEED_OFFSET || 0);
const GAP_SCENE = 0.55, GAP_CHAPTER = 2.4, CHAPTER_SCENES = (process.env.CHAPTERS || "").split(","), LEAD = 0.4, TAIL = 2.5;

const lines = await loadScript(ep);
type Chunk = { ids: string[]; text: string };
const chunks: Chunk[] = [];
for (const l of lines) {
  const last = chunks[chunks.length - 1];
  const sameScene = last && lines.find((x) => x.id === last.ids[last.ids.length - 1])!.scene === l.scene;
  if (last && (single || (sameScene && last.text.length + l.text.length < MAX))) { last.ids.push(l.id); last.text += " " + l.text; }
  else chunks.push({ ids: [l.id], text: l.text });
}
await mkdir(`${ep}/audio`, { recursive: true });

async function tts(text: string, seed: number): Promise<Uint8Array> {
  for (let a = 0; a < 3; a++) {
    const r = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceId}?output_format=mp3_44100_192`, {
      method: "POST", headers: { "xi-api-key": KEY!, "Content-Type": "application/json" },
      body: JSON.stringify({ text, model_id: "eleven_v3", language_code: "te", seed, voice_settings: { stability: 0.5 } }),
    });
    if (r.ok) return new Uint8Array(await r.arrayBuffer());
    console.error("tts", r.status, (await r.text()).slice(0, 200));
  }
  throw new Error("TTS failed");
}

// --reuse: keep earlier takes whose text is unchanged (saves cost when only some chunks change)
const prev = new Map<string, { bytes: Uint8Array; score: number; tx: string }>();
if (args.includes("--reuse") && existsSync(`${ep}/audio/chunks.json`)) {
  for (const c of JSON.parse(await readFile(`${ep}/audio/chunks.json`, "utf8")).chunks)
    if (existsSync(c.file)) prev.set(c.text, { bytes: new Uint8Array(await readFile(c.file)), score: c.score, tx: c.transcript });
}
// Voice consistency (EP03 lesson: a chapter can start deeper/flatter for ~10 s, a "cold start"):
//  1) PRIMING: each chunk after the first is generated with the last PRIME sentences of the previous chunk in front,
//     so the model continues the same delivery; the primer is cut off using forced alignment.
//  2) DRIFT CHECK: the first 12 s of each chunk must match the reference voice (chunk 1) in pitch and liveliness;
//     otherwise the chunk is regenerated (up to TAKES).
const PRIME = 2, F0_TOL = 0.05, RANGE_MIN = 0.65;
const stats = (f: string) => JSON.parse(spawnSync("python3", [`${import.meta.dir}/voice_stats.py`, f, "12"], { encoding: "utf8" }).stdout);
async function align(bytes: Uint8Array, text: string): Promise<{ text: string; start: number; end: number }[]> {
  const fd = new FormData(); fd.append("file", new Blob([bytes], { type: "audio/mpeg" }), "a.mp3"); fd.append("text", text);
  const r = await fetch("https://api.elevenlabs.io/v1/forced-alignment", { method: "POST", headers: { "xi-api-key": process.env.ELEVENLABS_API_KEY! }, body: fd });
  const j: any = await r.json(); if (!r.ok) throw new Error("align " + JSON.stringify(j).slice(0, 200));
  return j.words.filter((w: any) => w.text.trim());
}
const report: any[] = [];
let ref: { f0: number; range: number } | null = process.env.REF ? JSON.parse(process.env.REF) : null;
for (let i = 0; i < chunks.length; i++) {
  const c = chunks[i]; const f = `${ep}/audio/chunk_${String(i + 1).padStart(2, "0")}.wav`;
  const reused = prev.get(c.text);
  if (reused) { await writeFile(f, reused.bytes); report.push({ file: f, ids: c.ids, text: c.text, score: reused.score, transcript: reused.tx, pass: reused.score >= PASS }); console.log(`chunk ${i + 1} reused`); if (!ref) ref = stats(f).all; continue; }
  const primer = i > 0 && !single ? chunks[i - 1].ids.slice(-PRIME).map((id) => lines.find((x) => x.id === id)!.text).join(" ") : "";
  let best: any = null;
  for (let k = 0; k < TAKES; k++) {
    const raw = await tts(primer ? primer + " " + c.text : c.text, SEED + k);
    const tmp = `/tmp/take_${i}_${k}.mp3`; await writeFile(tmp, raw);
    let cut = 0;
    if (primer) { const ws = await align(raw, primer + " " + c.text); const n = primer.split(/\s+/).length; cut = Math.max(0, ws[n].start - 0.08); }
    const out = `/tmp/take_${i}_${k}.wav`;
    spawnSync("ffmpeg", ["-nostdin", "-loglevel", "error", "-y", "-ss", String(cut), "-i", tmp, "-af", "afade=t=in:d=0.03", "-ar", "44100", out]);
    const bytes = new Uint8Array(await readFile(out));
    const tx = await transcribeTelugu(bytes, "a.wav"); const score = similarity(c.text, tx);
    const s = stats(out); if (!ref) ref = s.all;
    const drift = Math.abs(s.head.f0 / ref!.f0 - 1); const flat = s.head.range / ref!.range;
    const voiceOk = i === 0 || (drift <= F0_TOL && flat >= RANGE_MIN);
    console.log(`chunk ${i + 1}/${chunks.length} take ${k + 1}: text ${score.toFixed(3)} | start pitch ${s.head.f0}Hz (ref ${ref!.f0}, drift ${(drift * 100).toFixed(1)}%) range x${flat.toFixed(2)} ${voiceOk ? "OK" : "DRIFT"}`);
    const rank = (score >= PASS ? 2 : 0) + (voiceOk ? 1 : 0) + score / 10;
    if (!best || rank > best.rank) best = { rank, score, bytes, tx, s, voiceOk };
    if (score >= PASS && voiceOk) break;
  }
  await writeFile(f, best.bytes);
  report.push({ file: f, ids: c.ids, text: c.text, score: +best.score.toFixed(3), transcript: best.tx, pass: best.score >= PASS, voiceOk: best.voiceOk, startPitch: best.s.head, pitch: best.s.all, primed: !!primer });
}

// Join: lead-in, chunks separated by scene pauses, tail. Trim each chunk's edge silence first.
const parts: string[] = []; let filter = ""; let t = LEAD; const offsets: number[] = [];
const sceneOf = (i: number) => lines.find((x) => x.id === report[i].ids[0])!.scene;
const gapAfter = (i: number) => (i + 1 < report.length && CHAPTER_SCENES.includes(sceneOf(i + 1)) ? GAP_CHAPTER : GAP_SCENE);
// Loudness-match every chunk to -18 LUFS so no part sounds louder or "different".
const lufs = (f: string) => { const e = spawnSync("ffmpeg", ["-nostdin", "-hide_banner", "-i", f, "-af", "ebur128", "-f", "null", "-"], { encoding: "utf8" }).stderr; const m = [...e.matchAll(/I:\s+(-?[\d.]+) LUFS/g)].pop(); return m ? +m[1] : -18; };
report.forEach((r, i) => {
  parts.push("-i", r.file);
  r.lufs = lufs(r.file); const gain = (-18 - r.lufs).toFixed(2);
  filter += `[${i}]volume=${gain}dB,aresample=48000,aformat=channel_layouts=mono,silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=${gapAfter(i)}[c${i}];`;
});
filter += report.map((_, i) => `[c${i}]`).join("") + `concat=n=${report.length}:v=0:a=1,adelay=${LEAD * 1000},apad=pad_dur=${TAIL}[out]`;
const res = spawnSync("ffmpeg", ["-nostdin", "-hide_banner", "-loglevel", "error", "-y", ...parts, "-filter_complex", filter, "-map", "[out]", `${ep}/audio/voice.wav`], { stdio: "inherit" });
if (res.status !== 0) throw new Error("ffmpeg join failed");
// Record each chunk's offset inside voice.wav (needed by align.py).
for (const r of report) {
  const d = +spawnSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "-i", r.file], { encoding: "utf8" }).stdout;
  r.offset = +t.toFixed(3); offsets.push(t);
  const trimmed = spawnSync("ffmpeg", ["-nostdin", "-hide_banner", "-i", r.file, "-af", `volume=${(-18 - r.lufs).toFixed(2)}dB,silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse`, "-f", "null", "-"], { encoding: "utf8" }).stderr;
  const m = [...trimmed.matchAll(/time=(\d+):(\d+):([\d.]+)/g)].pop();
  const td = m ? +m[1] * 3600 + +m[2] * 60 + +m[3] : d;
  r.duration = +td.toFixed(3); t += td + gapAfter(report.indexOf(r));
}
await writeFile(`${ep}/audio/chunks.json`, JSON.stringify({ voiceId, model: "eleven_v3", chunks: report }, null, 1));
const failed = report.filter((r) => !r.pass || r.voiceOk === false);
console.log(failed.length ? `WARNING: ${failed.length} chunk(s) below ${PASS}. Check audio/chunks.json transcripts.` : "All chunks passed.");
