# Telugu YouTube skill

`telugu-money-explainer/SKILL.md` is the complete skill (workflow, script, voice, footage, editing, audio, QA, delivery).

Status (EP03 production run): the full pipeline has been used end to end — `tts_elevenlabs.ts` (primed chunks + start-drift check), `falign.ts` + `timeline_from_words.py`, `commons_fetch.py`, `render_v2.mjs`, `stills.mjs`, `mix.sh`, `finish.sh`, `thumbnail.mjs`, `upload.ts`.

New in v4:
- `scripts/lint_script.py` — script checker (no English announcer phrases, every chapter starts in plain Telugu, max 2 English words per sentence, no next-topic teases). Must show 0 errors before voice generation.
- `scripts/voice_stats.py` — pitch/liveliness measurement used by the voice drift check.
- Voice: each chunk is primed with the previous chunk's last 2 sentences (cut off afterwards) and regenerated if its first 12 s drift more than 5% in pitch from the reference voice.
- Topic secrecy rule: never name the next topic in a video, description or pinned comment.

Paths: render scripts expect the engine at `backend/tools/telugu/engine.html` (copy `scripts/` there in a Vibecode project). Paid-API scripts run from `backend/` with `bun --env-file=.env`.
