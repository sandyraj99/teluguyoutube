import "@vibecodeapp/proxy";
import { createVibecodeSDK } from "@vibecodeapp/backend-sdk";
import { readFile } from "node:fs/promises";
import { basename } from "node:path";
const vibecode = createVibecodeSDK();
for (const p of process.argv.slice(2)) {
  const type = p.endsWith(".mp3") ? "audio/mpeg" : p.endsWith(".mp4") ? "video/mp4" : p.endsWith(".png") ? "image/png" : p.endsWith(".jpg") ? "image/jpeg" : "text/plain";
  const r = await vibecode.storage.upload(new File([await readFile(p)], basename(p), { type }));
  console.log("URL", r.url);
}
