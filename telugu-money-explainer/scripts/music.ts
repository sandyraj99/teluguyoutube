import "@vibecodeapp/proxy";
import { writeFile } from "node:fs/promises";
const out = process.argv[2];
const beds: [string, number, string][] = [
  ["bedA", 305000, "Instrumental documentary background music, curious and light, soft tabla and gentle mridangam pattern, plucked veena motif, warm pads, around 100 BPM, Indian texture, understated, no vocals, steady and loopable, suitable under a narrator explaining business numbers"],
  ["bedB", 150000, "Instrumental documentary background music, focused and slightly tense, soft tabla groove, low strings pulse, sparse santoor plucks, around 96 BPM, Indian texture, understated, no vocals, suitable under a narrator explaining money calculations"],
  ["bedC", 110000, "Instrumental documentary background music, reflective and warm, slow bansuri flute melody over soft tanpura drone and light tabla, around 84 BPM, gentle resolution at the end, no vocals, understated under narration"],
];
await Promise.all(beds.map(async ([name, ms, prompt]) => {
  const r = await fetch("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_192", { method: "POST", headers: { "xi-api-key": process.env.ELEVENLABS_API_KEY!, "Content-Type": "application/json" }, body: JSON.stringify({ prompt, music_length_ms: ms, model_id: "music_v1", force_instrumental: true }) });
  if (!r.ok) { console.error(name, r.status, (await r.text()).slice(0, 300)); return; }
  await writeFile(`${out}/${name}.mp3`, new Uint8Array(await r.arrayBuffer())); console.log("ok", name);
}));
