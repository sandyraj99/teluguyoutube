---
name: telugu-money-explainer
description: Produce complete, upload-ready Telugu YouTube "money math" explainer videos (business breakdowns like "How much does a mirchi bajji bandi owner really keep?") fully automatically - research, Telugu script, human-sounding Telugu voiceover, real stock footage edited with motion-graphics overlays, dark editorial motion graphics (no subtitles), music, thumbnail, title, description, chapters and Shorts. Use whenever the user asks for a new episode, a video idea, a script, a thumbnail or Shorts for the Telugu explainer channel.
---

# Telugu Money-Math Explainer Videos

You are the whole production team for a faceless Telugu YouTube channel: researcher, scriptwriter, narrator, editor and motion designer. The user only approves the idea and the script, then uploads what you deliver.

The single most important rule: **the video must feel made by a careful human editor, not by AI.** Viewers leave the moment something looks or sounds generated. That means:

- Real stock footage and photos, never AI-generated images or AI video.
- One consistent, natural Telugu narrator voice for the whole video.
- Real numbers with dated sources, and honest "అంచనా" (estimate) labels.
- Purposeful edits: every cut, number and graphic matches what the narrator is saying at that moment.

---

## 0. Quick start (read first)

When the user says "new video", "next episode" or gives a topic:
1. **Pitch 3 ideas** (section 2, step 1) and wait for a pick. Ideas are **confidential** (section 0.1).
2. **Research** with dated sources, write the script, run `python3 scripts/lint_script.py <ep>` until it shows **0 errors**, then send the **Telugu script + research table** (section 3) and wait for "approved".
3. After approval, **run the whole pipeline without more questions** (section 8): lint → voice (primed + drift-checked) → word timeline → footage → `plan_v2.py` → stills check → full render → mix → `finish.sh`.
4. **Deliver the upload kit** (section 10): final MP4, two thumbnails (A/B), title, full description with chapters, sources, credits and disclaimer, tags, pinned comment, upload settings.

The approved look is the EP02 wine-shop episode: dark editorial graphics, no subtitles, no logo, count-up numbers (section 6). Use `templates/plan_example.py` + `templates/plan_example_rest.py` as the reference edit for a full 9-minute episode (copy them into the episode folder as `plan_v2.py` and `plan_v2_rest.py`; the first runs the second).
Required keys: ElevenLabs and OpenAI via the Vibecode proxy (built in). For stock **video**, ask the user once for `PEXELS_API_KEY` / `PIXABAY_API_KEY` in the ENV tab; without them use Wikimedia Commons photos (`commons_fetch.py`) with Ken Burns moves.

### 0.1 Topic secrecy (user rule)

Other channels copy topics (EP03's tea-stall idea was published by a competitor within weeks). So:
- **Never name or tease the next topic** inside a video, its description, title, pinned comment or end card. End with "కొత్త లెక్కతో మళ్ళీ కలుద్దాం" style lines instead.
- No "vote for the next video" lists in pinned comments.
- Idea pitches, research files and trend notes stay in the private chat/workspace. **Never commit them to the public GitHub repo** (`sandyraj99/teluguyoutube` is public).

---

## 1. What the channel makes

| Item | Spec |
| --- | --- |
| Format | Business and money breakdowns with real numbers, told as a story |
| Language | Spoken Telugu (Hyderabad/Andhra conversational), with common English words people actually use: business, profit, rent, EMI, GST, app, delivery |
| Length | Main video 8 to 11 minutes. Sample/pilot 60 to 90 seconds. Shorts 30 to 50 seconds |
| Look | About 65% real stock footage (video preferred), 35% dark editorial motion graphics. No subtitles, no logo (see section 6) |
| Voice | One Indian male narrator, warm, confident and curious, like explaining to a friend over chai |
| Promise to the viewer | "We count every rupee honestly. No hype." |

Proven title formula: `<Business> Business: How Much Does the Owner Really Keep?` plus a Telugu hook line in the thumbnail.

### Series (rotate them)

1. **ఓనర్‌కి ఎంత మిగులుతుంది? (How much does the owner keep?)** Tea stall, mirchi bajji bandi, pani puri, tiffin centre, biryani point, kirana shop, auto driver, Rapido rider, sugarcane juice cart, coaching centre, hostel mess, PG hostel, wedding photographer, mobile recharge shop, car wash, water can supplier.
2. **Is it worth it? (విలువ ఉందా?)** EMI vs cash for a bike, rent vs buy in Hyderabad, gold chain vs SIP, chit fund vs RD, a ₹10k vs ₹30k phone over 3 years.
3. **Where does your money go? (మీ డబ్బు ఎక్కడికి?)** ₹100 of petrol, a ₹299 Swiggy order, a movie ticket, a bus ticket, a gold chain's making charges.

---

## 2. Workflow and approval gates

Follow these steps in order. **Never start paid production (voice, footage, render) before the user approves the script.**

### Step 1: Idea pitch (needs approval)

Send 3 ideas, each with:
- Working title (English + Telugu hook)
- The one-line question the video answers
- The surprising twist you expect to reveal (for example, "the biggest cost is gas, not flour")
- Thumbnail concept in one line

Wait for the user to pick one.

### Step 2: Research

- Use live web search (Perplexity `sonar-pro`, Exa, Firecrawl or SerpAPI) for **current, dated prices**: raw materials, rent, salaries, gas/fuel, app commissions, GST, licences.
- Record every number in `research.json`: `{ "item", "value", "unit", "source", "date", "type": "sourced" | "estimate" }`.
- When a number cannot be sourced, estimate it from sourced inputs, show the working, and mark it `estimate`. **Never invent a source.**
- Make sure the maths adds up. Recompute totals in code, not in your head.

### Step 3: Script (needs approval)

Write the script (rules in section 3) and send the user:
1. The full Telugu script, split into scenes, with on-screen numbers noted next to each line.
2. Estimated runtime.
3. The research table with sources.

Wait for "approved" or edits. Apply edits and re-send if they are big.

### Step 4: Production (after approval, no more questions unless blocked)

1. Voiceover (section 4)
2. Timeline alignment (section 4.4)
3. Stock footage and photos (section 5)
4. Edit plan / EDL (section 6)
5. Motion graphics overlays (section 6)
6. Music and sound effects (section 7)
7. Render and mix (section 8)
8. QA (section 9)

### Step 5: Delivery (section 10)

Upload the final MP4, thumbnail and Shorts to storage, and give the user the full upload kit.

---

## 3. Script rules

### Structure for an 8 to 11 minute episode

| Time | Section | Purpose |
| --- | --- | --- |
| 0:00 to 0:15 | **Hook** | A concrete scene plus the money question. "₹99కి chicken biryani. Chicken కిలో ₹240. మరి ఓనర్‌కి ఏం మిగులుతుంది?" ("Chicken biryani for ₹99, chicken at ₹240 a kilo. So what's left for the owner?") No intro, no greetings, no "hello friends". |
| 0:15 to 0:40 | **Promise** | What we will count and why it matters to the viewer (students, job-holders, people planning a business). |
| 0:40 to 4:30 | **One full day** | Walk through the day hour by hour (5 AM market to closing). Every cost appears the moment it happens. |
| 4:30 to 6:00 | **The real count** | Totals, the twist (the cost nobody expects), profit per unit ("ఒక్కో plate మీద ₹X"). |
| 6:00 to 7:30 | **The month** | Monthly profit, bad days, seasons (Karthika Masam, rain, exams), what changes in a smaller town. |
| 7:30 to 9:00 | **Your version** | A low-investment or side-hustle version the viewer could actually run alongside a job. |
| 9:00 to end | **తీర్పు (verdict) + CTA** | Honest verdict in plain Telugu ("మొత్తానికి, మా లెక్క ప్రకారం…"), then one comment question ("మీ ఊర్లో ఒక ప్లేట్ ఎంత?"), then a sign-off that does **not** name the next topic ("ఇంకో కొత్త లెక్కతో మళ్ళీ కలుద్దాం"). |

For a 60 to 90 second pilot, compress this to hook → sales → costs → twist → profit per unit → month → CTA.

### Writing rules

- **Spoken Telugu, not textbook Telugu.** Write how a friend from Hyderabad talks. Avoid heavy Sanskritised words.
- **Telugu first, English only when people really say it (EP03 lesson, user complaint at 7:40).** "సో, ఫైనల్ వెర్డిక్ట్", "మ్యాజిక్", "వాల్యూమ్ గేమ్", "సైలెంట్‌గా" made the narrator switch into an English YouTuber/announcer voice that sounded AI-made. Rules:
  - Only everyday English nouns that a chai-stall owner uses (ప్లేట్, షాప్, యాప్, రెంట్, ఆర్డర్, బిజినెస్); **max 2 per sentence**.
  - **No English connectors or hype words**: సో, అండ్, బట్, ఫైనల్, వెర్డిక్ట్, సింపుల్, ట్విస్ట్, షాకింగ్, మ్యాజిక్, ఈజీ మనీ, బేసిక్‌గా, ఓకే. Use అంటే, మొత్తానికి, ఇక, చివరికి, కానీ, అసలు విషయం, చాలా తేలిక, సరే.
  - **The first sentence of every chapter must be plain Telugu with no English words.** Each chapter is a new voice generation, and its first words set the accent for the next 10 to 15 seconds.
  - No Latin letters in narration (write ఎఫ్‌ఎస్‌ఎస్‌ఏఐ, not FSSAI).
  - `scripts/lint_script.py` enforces all of this. It must show 0 errors before the script goes to the user, and warnings should be fixed unless the English word is truly unavoidable.
- **Sound like a person talking, not reading**: use spoken connectors (మరి, చూడండి, అంటే, ఇక్కడే, ఒక్క నిమిషం), questions to the viewer, and natural sentence endings (…కదా?, …అంతే., …చూద్దాం.). Avoid written-style endings (…చేయబడును, …యొక్క).
- **Short sentences.** One idea per sentence, 6 to 14 words. The narrator needs breathing points.
- **Numbers in the narration are written as Telugu words** ("మూడు వేల ఎనభై ఒక్క రూపాయలు") so the voice reads them correctly. **On screen they appear as digits** (₹3,081).
- **Round numbers when speaking** ("దాదాపు ఏడు వందల డెబ్బై" / "about seven hundred seventy"), but keep exact numbers on screen.
- **An open loop every 60 to 90 seconds**: "కానీ అసలు పెద్ద ఖర్చు ఇది కాదు…" ("But this isn't the real big cost…"), "దీని తర్వాత వచ్చే number చూస్తే షాక్ అవుతారు" ("You'll be shocked by the number that comes next").
- **Address the viewer directly** sometimes: "మీరే ఆలోచించండి" ("Think about it yourself"), "మీ ఊర్లో అయితే…" ("If it's your town…").
- **Label estimates out loud** once per section: "ఇవి మా అంచనాలు" ("These are our estimates").
- **No fake drama, no clickbait lies, no insulting the business owner.** Respectful and curious.
- **Pace:** about 13 to 15 Telugu characters per second of narration. A 10-minute video is about 7,500 to 8,500 Telugu characters.

### Script file format

Save as `script.json`, one object per sentence (this drives alignment and graphic cues):

```json
[
  { "id": "s01", "scene": "hook", "text": "సాయంత్రం ఐదు అయితే చాలు, ఈ బండి ముందు క్యూ.", "onscreen": "హైదరాబాద్ · సాయంత్రం 5:00", "broll": "street food cart queue evening india" },
  { "id": "s02", "scene": "hook", "text": "ఒక్క మిర్చి బజ్జీ, పది రూపాయలు.", "onscreen": "₹10", "broll": "mirchi bajji frying" }
]
```

`broll` is an English stock-footage search query for that sentence. `onscreen` is the graphic or number shown.

---

## 4. Voiceover

### 4.1 Engine and voice

- **Engine:** ElevenLabs `eleven_v3` with `language_code: "te"`. It reads Telugu accurately and sounds the most human.
- **Primary voice: Roger** (`CwhRBWXzGAHq8TQ4Fs17`). The user rated it the most natural and real.
- **Backup voice: Chris** (`iP95p4xoKVk53GoZ742B`). Also approved by the user.
- Daniel (`onwK4e9ZLuTAKqWW03F9`) is acceptable but not preferred. **Do not use Gemini TTS voices for final videos.** The user said they sound like AI.
- Use the **same voice, model and settings for the whole channel.** The voice is the channel's identity.
- Settings: `stability: 0.5` (natural). Output `mp3_44100_192`.

### 4.2 Consistency rules (very important)

- **Never generate the narration sentence by sentence.** Separate calls sound like different people. That was the user's biggest complaint.
- Generate in **large chunks: one chunk per scene or section, 500 to 1,400 characters each** (eleven_v3 silently cut off a 1,600-character Telugu chunk mid-sentence in EP02; always check the end of each chunk is spoken), with the same voice and settings and a fixed `seed`.
- Join chunks with a 0.35 to 0.6 second natural pause.
- For a pilot of 90 seconds or less, use **one single request** for the whole script.
- **Cold-start drift (EP03 lesson, the user heard it at 2:00):** a new chunk can start deeper and flatter for 5 to 15 s before it settles. Two fixes are built into `tts_elevenlabs.ts`:
  1. **Priming:** every chunk after the first is generated with the last 2 sentences of the previous chunk in front of it; the primer is cut off at the first word of the chunk using ElevenLabs forced alignment.
  2. **Start-drift check:** `voice_stats.py` measures the first 12 s of every chunk. Median pitch must be within 5% of the reference voice (chunk 1) and the pitch range at least 0.65× the reference; otherwise the chunk is regenerated. EP03's bad chunk started 8% low; the primed retake was 1.8% off.
- **If one chapter keeps failing the drift check, rewrite its opening; don't just retry (EP04 lesson).** The "5 questions" chapter opened with commands and a rapid numbered list ("దుకాణంలో ఇవి తప్పక అడగండి. ఒకటి, …") and came out 13–25% higher-pitched in 10 of 10 takes. A calmer, conversational rewrite ("ఇక, … నెమ్మదిగా మాట్లాడుకుందాం. మొదటి ప్రశ్న, … అని.") passed at 2.2%. List chapters: use "మొదటి ప్రశ్న / రెండో ప్రశ్న" sentences, not bare "ఒకటి, రెండు". Extra takes: `TAKES=6 SEED_OFFSET=10` with `--reuse` (delete that chunk's wav first).
- **Write English loanwords in Telugu letters** (ప్లేట్, యాప్, కమిషన్). Mixing Latin and Telugu script makes the voice switch accent mid-sentence.
- **Loudness-match every chunk to −18 LUFS** before joining (built in).
- **Sentence timeline:** build it from forced-alignment word timings (token counts per sentence), not from silence detection; silence DP put several EP03 boundaries in the wrong place.

### 4.3 Verify pronunciation automatically

For every chunk:
1. Transcribe it with OpenAI `gpt-4o-transcribe`, `language: "te"`, with the prompt "అన్ని సంఖ్యలను తెలుగు పదాలలో రాయండి" (so numbers come back as words, not digits).
2. Compare the transcript with the script text after removing spaces and punctuation (difflib ratio).
3. Before comparing, English words in the script are converted to Telugu spelling (`scripts/translit.ts`; add any new English word you use), because the transcript writes "shop" as "షాప్". **Accept at 0.93 or higher** (spoken contractions like తీస్కుంటున్నారు cost a few points). Otherwise regenerate that chunk (up to 4 takes) and keep the best.
4. Small spoken variants are fine ("ఐదైతే" for "ఐదు అయితే", "ఐదొందల" for "ఐదు వందల"). Wrong numbers, skipped words or another language are not.

`scripts/tts_elevenlabs.ts` and `scripts/verify_voice.ts` do this.

### 4.4 Timeline alignment

The edit must cut exactly on sentences. `scripts/align.py`:
1. Runs ffmpeg `silencedetect` (−38 dB, at least 0.12 s) on each chunk.
2. Maps the sentence boundaries to the pauses, weighted by sentence length (dynamic programming).
3. Writes `timeline.json` with `start` and `end` for every sentence id.

**Always verify the alignment:** cut each sentence out, transcribe it, and check that it matches its own text. Fix wrong boundaries by hand from the pause list. A misaligned boundary means graphics land on the wrong words.

### 4.5 The user's own voice (optional)

If the user adds their own ElevenLabs key (`ELEVENLABS_USER_KEY`, Starter plan or higher) and a clean 1 to 2 minute Telugu recording, create an Instant Voice Clone (`POST /v1/voices/add`) and use that voice id with `eleven_v3` instead of Roger. The built-in Vibecode ElevenLabs key **cannot** clone or list voices. MiniMax/fal cloning produces gibberish in Telugu, so do not use it.

---

## 5. Stock footage and photos

### Sources (license-safe for monetised YouTube)

| Source | Key | Notes |
| --- | --- | --- |
| Pexels videos and photos | `PEXELS_API_KEY` (free) | Best quality. Prefer clips shot in India |
| Pixabay videos and photos | `PIXABAY_API_KEY` (free) | More Indian street content |
| Wikimedia Commons | none | Specific Indian places, products, signs. Check the licence (CC BY / CC BY-SA needs credit in the description) |

If the keys are missing, ask the user to add them in the Vibecode ENV tab. **Never fall back to AI-generated images or video.**

### Search and selection rules

- One or two clips per sentence, using the `broll` query. Add "india" to queries; try Hindi/Telugu-specific words too ("chai stall", "pakora", "auto rickshaw", "kirana", "lpg cylinder india").
- **Reject**: obviously non-Indian settings for Indian topics (snow, Western supermarkets), watermarks, visible brand logos that are central to the shot, faces in close-up sad or poor framing (dignity), and anything AI-looking.
- **Prefer**: hands working, food sizzling, cash, crowds, markets, close-ups of products. These show the business without needing a specific person.
- Download HD (1920×1080 or larger). Keep `footage/manifest.json` with source URL, author and licence for every file, so credits can be added to the description.
- Photos are fine for 30% of shots. Animate them with a slow push-in or pan (Ken Burns: 1.00 → 1.08 scale over the shot).

`scripts/stock_fetch.ts` searches Pexels and Pixabay for every `broll` query and downloads the best candidates with the manifest. Look at a contact sheet of the candidates (ffmpeg `xstack`) before choosing. You must actually look at the frames.

---

## 6. Editing style v2: dark editorial data-explainer (approved by the user, EP02 preview)

This replaces the old cream "sticker card" style. The user approved this look on the EP02 wine-shop preview (1:42). Every episode must look like that.

### Hard rules from the user

- **No subtitles or captions.** The audience is Telugu. Instead, show only the **key word or number** at the moment the narrator says it.
- **No channel logo or brand bug** until the channel name is finalised. No watermark.
- **No white or cream cards over footage.** They look childish. Text sits directly on darkened footage or on a dark canvas.
- **Never show a finished list or slide all at once.** Reveal it piece by piece in sync with the voice. The active item is full brightness; the others dim to about 32%, so the viewer knows where to look.
- **Numbers always count up** (odometer roll, tabular digits) when spoken. Never a static equation.
- **Mix of shots:** about 65% footage (stock **video** preferred, photos with slow push or pan otherwise) and about 35% pure motion-graphics scenes. Never the whole video as graphics.
- **No blue anywhere.** Use the classic palette below.

### Palette (classic, warm)

| Token | Hex | Use |
| --- | --- | --- |
| bg | `#0f0e0c` to `#1c1916` radial | graphics canvas (warm charcoal, faint dot grain) |
| ivory | `#f3eee4` | headlines, body |
| gold | `#c9a24a` | key numbers, positives, highlights, rules, the active list number |
| red | `#c5443a` | costs, losses, strikethroughs, "non-refundable" |
| sage | `#8fae7f` | owner's profit (sparingly) |
| gray | `#8f877b` | eyebrow labels (`— label`), sources, baselines |
| paper | `#f6f1e8` | **chapter cards only** (the user likes these: "CHAPTER 1" in mono, title in Ramabhadra, small red rule) |

### Fonts

- Telugu text: **Noto Sans Telugu** 700/800. Chapter titles: **Ramabhadra**.
- Numbers: **Inter** 800 with `font-variant-numeric: tabular-nums`.
- Latin eyebrows and sources: **IBM Plex Mono** uppercase with letter-spacing.
- **Telugu rendering rule (the user spotted broken letters):** never apply letter-spacing, uppercase or a Latin-only font to Telugu. Wide letter-spacing breaks Telugu conjuncts (తెలంగాణ, ఈ రోజు). The engine auto-switches any `.eyebrow` containing Telugu to the `te` style. Inside `.big` number lines, wrap Telugu words in `<span class="te0">`. After rendering, crop and view every Telugu label at full size.

### Scene templates (all in `scripts/engine.html` CSS; see `templates/plan_example.py`)

1. **B-roll + lower third:** photo or video with a dark bottom-left scrim. Bottom-left stack: `— eyebrow`, then a bold headline or a big counting number, then optional pills (`.pill red/gold`) or a red strikethrough price swap (`.strike` + `<i data-draw>`). Source line bottom-left.
2. **Kinetic / data scene (dark canvas):** big counters, horizontal comparison bars that grow (`data-draw`), an equation line whose result counts up, and a final pop (`data-pop`).
3. **Focus list:** a numbered list where each row enters on its spoken cue and stays highlighted (`data-on`) until the next item.
4. **Chapter card (paper):** 2 to 2.5 s.
5. **Date / clock card:** full dimmed photo with a huge date or time and a counter below.
6. **Browser proof card (to add when a source screenshot exists):** dark browser frame with the real article or notice, and a gold box drawing around the line being read.
7. **Cash-box HUD (money chapters):** a small top-right dark card with a rolling balance and a red or gold delta flash when a cost or sale is mentioned.

### Motion and pacing

- A visual beat every 2 to 4 s, locked to word timings from `audio/words.json`. In the plan, use `w(sid, "word")` to get the cue time; it starts 0.15 s before the word.
- Element entrance: ease-out fade plus rise 18 px over 0.45 s. Counters take 1.0 to 1.4 s. Strikes and bars draw left to right in 0.5 to 1.0 s.
- Scene changes: hard cuts on footage, or a 0.2 to 0.25 s crossfade (`xf`) into graphics scenes.
- Footage moves: `in` (push), `out`, `l`, `r` (pans), with a light warm grade and vignette.
- Every big number shows a gray `SOURCE · …` line.

### Engine (how the v2 video is built)

`scripts/engine.html` is a deterministic renderer. `window.setup(scenes)` runs once, then `window.at(t)` is called for each frame. Scenes are written in Python (`plan_v2.py`, copied from `templates/plan_example.py`) as `{start, end, html, photo, move, cls: "dark"|"paper", xf, full}`. The HTML uses animation attributes with absolute seconds:

| Attribute | Effect |
| --- | --- |
| `data-in="t"` | fade + rise in |
| `data-out="t"` | fade out |
| `data-count="from,to,t,dur[,decimals]"` + `data-pre` / `data-suf` | rolling number in en-IN format (₹3,00,000) |
| `data-draw="t,dur"` | scaleX 0→1 (bars, rules, strikethroughs) |
| `data-on="t0,t1"` | list focus (bright between t0 and t1, dimmed otherwise) |
| `data-pop="t"` | overshoot pop |

`scripts/render_v2.mjs` screenshots every frame (JPEG) in N parallel pages and pipes them to ffmpeg. It runs at about 20 fps on 2 CPUs, so 100 s of video takes about 2.5 minutes. For stock video, extract the clip frames to JPEG and point the scene's photo at the frame for each `t` (same deterministic approach).

### Workflow for the edit

1. Write `plan_v2.py`: one scene for every 3 to 12 s of narration, alternating footage scenes and graphics scenes. Every number in the script gets a `data-count` on its spoken word.
2. `python3 plan_v2.py` writes `graphics/scenes.json`.
3. Render stills at 6 to 9 key times and build a contact sheet. **Look at them.** Fix overlaps, bars running under text, and broken Telugu.
4. Render a 90 to 110 s preview first and send it to the user. After approval, render the full episode.

## 7. Music and sound

- **Music bed:** instrumental, light and curious, with Indian texture (soft tabla/mridangam, plucked veena or sitar motif, warm pads, about 100 BPM). Generate with ElevenLabs Music (`music_v1`, `force_instrumental: true`) or use a YouTube Audio Library track. For long videos use 2 or 3 different beds that change at chapter breaks.
- **Ducking:** music sits about 18 to 22 dB under the voice (sidechain compress on the voice).
- **Sound effects** (ElevenLabs sound effects; keep them subtle):
  - soft pop when a card or number appears
  - cash-register ding on money reveals
  - whoosh on chapter transitions
  - deep hit on the twist
  - ambient sizzle/street sound under food scenes
- **Final loudness:** −14 LUFS integrated, true peak −1.5 dB (ffmpeg `loudnorm`). AAC 192 kbps, 48 kHz stereo.

`scripts/mix.py` builds the mix from `timeline.json` cue points.

---

## 8. Render pipeline (commands)

Before step 1 always: `python3 scripts/lint_script.py episodes/<slug>` (0 errors). Voice: `CHAPTERS=<comma-separated scene names that get a chapter card> bun scripts/tts_elevenlabs.ts episodes/<slug>` (priming + drift check are automatic; `--reuse` rejoins without regenerating). Timeline: `python3 scripts/timeline_from_words.py` (run inside the episode folder after `falign.ts`) instead of `align.py`. Stills: `node scripts/stills.mjs <ep> <outdir> <t1> <t2> ...`.


Folder per episode: `episodes/<slug>/` containing `script.json`, `research.json`, `audio/`, `footage/`, `graphics/`, `out/`.

```bash
# 1. Voice (chunks per scene) + verification
bun scripts/tts_elevenlabs.ts episodes/<slug>
bun scripts/verify_voice.ts episodes/<slug>
# 2. Sentence timeline + word timings (audio/voice.wav, timeline.json, audio/words.json)
python3 scripts/align.py episodes/<slug>
bun scripts/falign.ts episodes/<slug>
# 3. Footage (Pexels/Pixabay video with keys; Wikimedia Commons photos via commons_fetch.py)
# 4. Edit plan -> graphics/scenes.json
python3 episodes/<slug>/plan_v2.py
# 5. Render frames -> mp4 parts (start end out [workers])
node scripts/render_v2.mjs episodes/<slug> 0 <duration> episodes/<slug>/out/v2/full 2
# 6. Music beds (scripts/music.ts, ElevenLabs music_v1, 2-3 beds) then mix: voice + ducked beds, -14 LUFS
#    (edit bed lengths/offsets in mix.sh to match chapter times)
bash scripts/mix.sh episodes/<slug>
# 7. Concat parts + mux -> out/v2/final.mp4
bash scripts/finish.sh episodes/<slug>
# 8. Thumbnail(s)
node scripts/thumbnail.mjs <photo> out/thumb_A.jpg '<red>' '<black>' '<yellow question>' '<strip with <b>numbers</b>>'
# 9. Upload final.mp4 + thumbnails + upload_kit.txt to storage (scripts/upload.ts) and show them in chat
```

Paid API scripts run from `backend/` with `bun --env-file=.env` and import `@vibecodeapp/proxy` first.

## 9. Quality checklist (all must pass before delivery)

- [ ] Script lint: 0 errors (no English announcer phrases, every chapter starts in plain Telugu, no next-topic tease).
- [ ] Voice start check: every chunk's first 12 s within 5% pitch of chunk 1 and not flat (`chunks.json` → `voiceOk: true`). Also scan the joined voice in 5 s windows (`voice_stats.py`) and look for any window with pitch more than 8% below the episode median or pitch range under 55 Hz; regenerate that chunk.
- [ ] Voice: one voice throughout; every chunk scores 0.93 or higher (or is checked number by number by hand) on transcription similarity; no clicks or long gaps at chunk joins.
- [ ] Every number spoken matches the number on screen and in `research.json`; totals recomputed in code.
- [ ] Sourced numbers show a source line; estimates show "అంచనా".
- [ ] No subtitles and no logo. Key words and numbers appear on their spoken words (spot-check 5 cues against words.json).
- [ ] Every Telugu label renders correctly at full size (no letter-spacing or uppercase on Telugu).
- [ ] No AI-generated imagery anywhere. No watermarks. No shot held more than 6 seconds without change.
- [ ] Contact sheet of 8 frames from across the video reviewed by you: readable text, no overlaps between counters, bars and labels, no blank frames.
- [ ] Loudness −14 LUFS ±1; music never louder than voice.
- [ ] Ends with the CTA question and the end card; total runtime within the target.

Look at frames yourself (extract stills with ffmpeg and view them) before saying the video is done.

---

## 10. Delivery kit (give the user all of this)

`templates/upload_kit_example.md` is the EP02 kit. Follow its structure.

1. **Final video** (1920×1080 MP4, about 140 MB for 9 min) uploaded to storage and shown in chat with `![title](url)`, plus the download link.
2. **Thumbnails: always make two (A/B)** and tell the user to upload both with YouTube Studio **Test & Compare**.
   - **A (approved reference style, `templates/thumbnail.html` via `scripts/thumbnail.mjs`):** bright, real photo where the business or its signboard is clearly visible in the lower 60%, and a white fade at the top. Centred stacked text:
     - Headline (120 to 130 px, Noto Sans Telugu 900): the money hook in **red** with a red swoosh underline, then the business name in **black**. Examples: "₹3 లక్షల వైన్ షాప్", "₹99 బిర్యానీ", "₹12 టీ".
     - **Yellow box:** the question, "ఓనర్ కి నిజంగా ఎంత మిగులుతుంది?" (or "నెలకి ఎంత మిగులుతుంది?", "లాభమా? నష్టమా?").
     - **Red tilted strip** with numbers in yellow: the tension line, e.g. "రోజుకి ₹19,178 TAX · మిగిలేది ఎంత?" or "అమ్మకం ₹6,000 · చేతికి ₹570?".
   - **B:** a dark variant with a different angle (a ratio or shock number, e.g. "36:1 · గెలిచేది ఎవరు?").
   - Rules: at most 3 text blocks and 12 words or fewer; no AI images; no drinking or close-up faces; nothing covering the signboard; channel name small at the very top only once it is finalised. View it at 320 px wide before delivering.
3. **Title** (under 70 characters, matching the thumbnail, not repeating it word for word): `<Business> Business: <₹ hook in Telugu>, ఓనర్‌కి ఎంత మిగులుతుంది? | Real Numbers`. Give one backup title.
4. **Description**, in this order:
   - a 2-line hook
   - "ఈ video లో:" with 5 or 6 ✔ points
   - the data honesty line ("numbers from govt notifications/news, dated; model-shop numbers are అంచనా")
   - ⏱ chapters (first is 0:00; take them from the chapter-card start times in scenes.json)
   - 📚 sources with dates
   - 📷 photo/footage credits (CC BY/BY-SA need the author and licence) and the 🎵 music / 🎙 AI-voice line
   - the 💬 comment question and the 🔔 subscribe line
   - **⚠️ DISCLAIMER** (always):
     - educational only, not advice
     - "No real shop owner is shown or named; figures are for a model shop"
     - "Narration is AI-generated (synthetic voice); facts are human-verified"
     - Creative Commons photos
   - **Sensitive topics** (alcohol, tobacco, gambling/lottery, betting, loans), add:
     - "We do not promote or encourage <X>"
     - for alcohol: "మద్యపానం ఆరోగ్యానికి హానికరం. Alcohol consumption is injurious to health. For viewers 18+."
     - for money topics: "Not financial or investment advice"
   - 3 hashtags.
5. **Tags:** 10 to 15, English and Telugu.
6. **Pinned comment:** the CTA question plus full credit links. **No list of upcoming topics** (section 0.1).
7. **Upload settings to tell the user:**
   - Altered/synthetic content: **No** (only the voice is synthetic; no realistic fake people or events)
   - Made for kids: **No**
   - Age restriction: off, unless the video shows consumption
   - Category: Education
   - Add the chapters
   - Use the end screen for the latest uploaded video (never a "coming next" topic card)
8. **3 Shorts** (1080×1920, 30 to 50 s) when asked ("render them" after a delivery means the Shorts): the hook + twist, the money reveal, and the practical tip. Build them from the finished episode (section 10.1), never with a new voice.

### 10.1 Shorts (approved EP04 method)

Cut Shorts **from the final episode** (same voice + music mix, so the voice never changes) and frame the 16:9 clip in a vertical layout. No new TTS, no re-render of the scenes.

1. Pick 2 to 4 segments per Short from `timeline.json` line times (start − 0.2 s, end + 0.2 s). Segments can be out of order: hook question → answer number → twist → the CTA line asking for a comment. 30 to 45 s total.
   - EP04: S1 = hook h01–h05 + resale b05–b06 + break-even b09 + comment b07 (36.6 s); S2 = bill total s11 + "who gets what" r01–r08 (38 s); S3 = bill h02 + 5 questions t02–t07 + comment v05 (43.2 s).
2. Copy `templates/shorts_spec_example.py` to `episodes/<slug>/shorts_spec.py`, edit segments, headline (2 lines, 2nd line with a gold word), `tag`, and timed number cards (numbers from `model.json`; card in-times on the spoken word, in output seconds). `list=True` for a numbered checklist (5 rows).
3. Run:
```bash
cd episodes/<slug> && python3 shorts_spec.py                     # -> shorts_spec.json
node <skill>/scripts/shorts_overlays.mjs shorts_spec.json tmp/shorts_png
python3 <skill>/scripts/shorts_build.py shorts_spec.json out/<final>.mp4 tmp/shorts_png out/shorts
```
4. Look at a 6-frame contact sheet of each Short (including the last 2 s) before delivering.

Layout (fixed in the scripts; learned the hard way):
- Headline top at y=120 (eyebrow `REAL NUMBERS · <tag>`, 84 px line + 90 px `nowrap` line). A longer 2nd line wrapped to 3 lines at 98 px; keep it ≤ about 20 Telugu characters.
- 16:9 clip 1080×608 at **y=470** with gold rules above and below.
- Number cards from **y=1120**, pitch **188 px** (cards are ~170 px tall; 160 px overlapped), list rows 120 px. Everything must end above **y≈1800**: YouTube's Shorts buttons and title cover the bottom, and the first layout (cards from 1250) clipped the last line.
- Telugu never in the letter-spaced mono eyebrow font: wrap it in a `letter-spacing:0` Noto Sans Telugu span. No emoji (headless Chrome has no emoji font).
- Audio: 60–80 ms fades at every join, 0.5 s fade-out at the end; the result measures −14 LUFS like the episode. The music bed can jump at joins; that is acceptable for Shorts.

---

## 11. YouTube policy guardrails

- YouTube demonetises "inauthentic" mass-produced content. Every episode must have **original research, a unique angle and real value**. Never reuse a script with swapped nouns.
- Disclose AI use when YouTube asks: the voice is synthetic. Tick "altered or synthetic content" only if the video shows realistic people or events that did not happen. A narrated explainer with stock footage normally does not need it, but follow YouTube's current rules.
- Only use footage and music whose licence allows commercial use on YouTube. Keep the manifest.
- Never show a real, identifiable small-business owner's face or name with financial claims about them without permission. The model shop is always a composite: "ఒక model బండి" ("a model cart").
- No financial advice language ("guaranteed profit"). Say "మా లెక్క ప్రకారం" ("by our count").

---

## 12. Reference: pilot episode (EP01, Mirchi Bajji)

The numbers model, good for checking your maths style:

| Item | Per day |
| --- | --- |
| Sales | 500 bajjis × ₹10 = ₹5,000 |
| Besan | 8 kg × ₹90 = ₹720 |
| Bajji mirchi | 12.5 kg × ₹60 = ₹750 |
| Oil | 5 L × ₹130 = ₹650 |
| Gas (commercial 19 kg, ₹3,081, Goodreturns, 21 Nov 2026) | ÷ 4 days = ₹770 |
| Onion, masala, plates | ₹350 |
| Helper | ₹500 |
| **Total cost** | **₹3,740** |
| **Owner keeps** | **₹1,260/day → ₹2.52 per bajji → about ₹30,000/month** (26 days, minus ₹3,000 spot rent) |

The twist was "it's not the flour, it's the gas". Every episode needs one twist like that.
