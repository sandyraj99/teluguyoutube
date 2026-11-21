// Shared helpers. In Vibecode the proxy package swaps placeholder keys for real ones; elsewhere it is skipped.
try { await import("@vibecodeapp/proxy"); } catch { /* not in Vibecode: real keys are used directly */ }
import { readFile } from "node:fs/promises";

export type Line = { id: string; scene: string; text: string; onscreen?: string; broll?: string };
export const loadScript = async (ep: string): Promise<Line[]> => JSON.parse(await readFile(`${ep}/script.json`, "utf8"));
export const norm = (s: string) => s.replace(/[\s,.!?'"’‘:;\-‌‍…]/g, "");

// Similarity ratio like Python difflib (longest-common-subsequence based, good enough for scoring).
export function similarity(a: string, b: string): number {
  a = norm(a); b = norm(b);
  if (!a.length && !b.length) return 1;
  const prev = new Array(b.length + 1).fill(0);
  for (let i = 1; i <= a.length; i++) {
    let diag = 0;
    for (let j = 1; j <= b.length; j++) {
      const tmp = prev[j];
      prev[j] = a[i - 1] === b[j - 1] ? diag + 1 : Math.max(prev[j], prev[j - 1]);
      diag = tmp;
    }
  }
  return (2 * prev[b.length]) / (a.length + b.length);
}

// Telugu transcription with numbers written as words, so it can be compared with the script.
export async function transcribeTelugu(bytes: Uint8Array, filename = "a.mp3"): Promise<string> {
  const fd = new FormData();
  fd.append("file", new Blob([bytes], { type: filename.endsWith(".wav") ? "audio/wav" : "audio/mpeg" }), filename);
  fd.append("model", "gpt-4o-transcribe");
  fd.append("language", "te");
  fd.append("prompt", "తెలుగు వ్యాపార వీడియో. అన్ని సంఖ్యలను అంకెలు కాకుండా తెలుగు పదాలలో రాయండి, ఉదా: ఏడు వందల ఇరవై.");
  const r = await fetch("https://api.openai.com/v1/audio/transcriptions", { method: "POST", headers: { Authorization: `Bearer ${process.env.OPENAI_API_KEY}` }, body: fd });
  const j: any = await r.json();
  if (!r.ok) throw new Error(`transcribe ${r.status}: ${JSON.stringify(j).slice(0, 200)}`);
  return j.text as string;
}
