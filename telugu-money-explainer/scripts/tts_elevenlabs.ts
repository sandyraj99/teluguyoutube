// Narration with ElevenLabs eleven_v3 in ONE consistent voice.
// Groups script sentences by scene into chunks (<= MAX chars), makes up to TAKES takes per chunk,
// transcribes each take, keeps the most accurate, then joins chunks with natural pauses.
// Usage: bun scripts/tts_elevenlabs.ts <episodeDir> [--voice roger|chris|<voiceId>] [--single]
//   --single  one request for the whole script (use for pilots of 90 s or less)
// Output: <ep>/audio/chunk_XX.mp3, <ep>/audio/voice.wav (48 kHz mono), <ep>/audio/chunks.json
import "./common.ts";
import { loadScript, similarity, transcribeTelugu } from "./common.ts";
import { mkdir, writeFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";

const VOICES: Record<string, string> = { roger: "CwhRBWXzGAHq8TQ4Fs17", chris: "iP95p4xoKVk53GoZ742B", daniel: "onwK4e9ZLuTAKqWW03F9" };
const args = process.argv.slice(2);
const ep = args[0]; if (!ep) throw new Error("usage: tts_elevenlabs.ts <episodeDir> [--voice roger] [--single]");
const vArg = args[args.indexOf("--voice") + 1];
const voiceId = args.includes("--voice") ? (VOICES[vArg] ?? vArg) : VOICES.roger;
const single = args.includes("--single");
const KEY = process.env.ELEVENLABS_USER_KEY || process.env.ELEVENLABS_API_KEY;
const MAX = 2400, TAKES = 4, PASS = 0.97, SEED = 4242;
const GAP_SCENE = 0.55, LEAD = 0.4, TAIL = 2.5;

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

const report: any[] = [];
for (let i = 0; i < chunks.length; i++) {
  const c = chunks[i]; let best: { score: number; bytes: Uint8Array; tx: string } | null = null;
  for (let k = 0; k < TAKES; k++) {
    const bytes = await tts(c.text, SEED + k);
    const tx = await transcribeTelugu(bytes);
    const score = similarity(c.text, tx);
    console.log(`chunk ${i + 1}/${chunks.length} take ${k + 1}: ${score.toFixed(3)}`);
    if (!best || score > best.score) best = { score, bytes, tx };
    if (score >= PASS) break;
  }
  const f = `${ep}/audio/chunk_${String(i + 1).padStart(2, "0")}.mp3`;
  await writeFile(f, best!.bytes);
  report.push({ file: f, ids: c.ids, text: c.text, score: +best!.score.toFixed(3), transcript: best!.tx, pass: best!.score >= PASS });
}

// Join: lead-in, chunks separated by scene pauses, tail. Trim each chunk's edge silence first.
const parts: string[] = []; let filter = ""; let t = LEAD; const offsets: number[] = [];
report.forEach((r, i) => {
  parts.push("-i", r.file);
  filter += `[${i}]aresample=48000,aformat=channel_layouts=mono,silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=${GAP_SCENE}[c${i}];`;
});
filter += report.map((_, i) => `[c${i}]`).join("") + `concat=n=${report.length}:v=0:a=1,adelay=${LEAD * 1000},apad=pad_dur=${TAIL}[out]`;
const res = spawnSync("ffmpeg", ["-nostdin", "-hide_banner", "-loglevel", "error", "-y", ...parts, "-filter_complex", filter, "-map", "[out]", `${ep}/audio/voice.wav`], { stdio: "inherit" });
if (res.status !== 0) throw new Error("ffmpeg join failed");
// Record each chunk's offset inside voice.wav (needed by align.py).
for (const r of report) {
  const d = +spawnSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "-i", r.file], { encoding: "utf8" }).stdout;
  r.offset = +t.toFixed(3); offsets.push(t);
  const trimmed = spawnSync("ffmpeg", ["-nostdin", "-hide_banner", "-i", r.file, "-af", "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse", "-f", "null", "-"], { encoding: "utf8" }).stderr;
  const m = [...trimmed.matchAll(/time=(\d+):(\d+):([\d.]+)/g)].pop();
  const td = m ? +m[1] * 3600 + +m[2] * 60 + +m[3] : d;
  r.duration = +td.toFixed(3); t += td + GAP_SCENE;
}
await writeFile(`${ep}/audio/chunks.json`, JSON.stringify({ voiceId, model: "eleven_v3", chunks: report }, null, 1));
const failed = report.filter((r) => !r.pass);
console.log(failed.length ? `WARNING: ${failed.length} chunk(s) below ${PASS}. Check audio/chunks.json transcripts.` : "All chunks passed.");
