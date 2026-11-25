# Telugu YouTube skill

`telugu-money-explainer/SKILL.md` is the complete skill (workflow, script, voice, footage, editing, audio, QA, delivery).

Status (EP03/EP04 production runs): the full pipeline has been used end to end — `tts_elevenlabs.ts` (primed chunks + start-drift check), `falign.ts` + `timeline_from_words.py`, `commons_fetch.py`, `render_v2.mjs`, `stills.mjs`, `mix.sh`, `finish.sh`, `thumbnail.mjs`, `upload.ts`.

New in v5 (EP04 gold episode):
- Shorts: `scripts/shorts_overlays.mjs` + `scripts/shorts_build.py` cut 3 vertical Shorts (1080x1920) from the finished episode (same voice/music, no new TTS), with a 2-line Telugu headline, the 16:9 clip at y=470 and timed number cards kept above YouTube's bottom UI. Reference spec: `templates/shorts_spec_example.py`. See SKILL.md section 10.1.
- Voice: if one chapter keeps failing the drift check, rewrite its opening calmly instead of retrying; `TAKES` / `SEED_OFFSET` env vars in `tts_elevenlabs.ts` for extra takes.

New in v4:
- `scripts/lint_script.py` — script checker (no English announcer phrases, every chapter starts in plain Telugu, max 2 English words per sentence, no next-topic teases). Must show 0 errors before voice generation.
- `scripts/voice_stats.py` — pitch/liveliness measurement used by the voice drift check.
- Voice: each chunk is primed with the previous chunk's last 2 sentences (cut off afterwards) and regenerated if its first 12 s drift more than 5% in pitch from the reference voice.
- Topic secrecy rule: never name the next topic in a video, description or pinned comment.

Paths: render scripts expect the engine at `backend/tools/telugu/engine.html` (copy `scripts/` there in a Vibecode project). Paid-API scripts run from `backend/` with `bun --env-file=.env`.
