# Never Quit — The Colonel Sanders Documentary (Cinematic Render Pipeline)

A self-contained pipeline that renders a **5-minute cinematic, motivational
documentary** about **Colonel Harland Sanders**, the founder of KFC — narrated
by a deep, calm, "wise mentor" voice and edited in a premium, CapCut-Pro /
MotivationHub style: a **fast montage of many clips** (several quick cuts per
narration line) with 3D zooms, parallax, push-ins, camera shake, speed ramps,
light-flash & whip transitions, lens flare, dust particles, film grain and
cinematic color grading, plus **animated word-by-word captions** (that keep
flowing across the cuts) which highlight the keywords `REJECTED`,
`PERSISTENCE`, `SUCCESS`, and `NEVER QUIT`.

The whole film is generated from code, so it is fully reproducible and easy to
re-edit. It renders **end-to-end out of the box** using synthesized cinematic
scene plates, and reaches **photoreal "Netflix" quality** the moment you drop
real 1950s photos into `assets/images/` (see [Photoreal mode](#photoreal-mode)).

```
narration (neural TTS)  ─┐
timed storyboard  ───────┼──►  cinematic frame compositor  ──►  final .mp4
procedural score  ───────┘        (effects + captions + look)
```

---

## Quick start

```bash
make setup        # install deps + download the voice model and fonts
make draft        # fast 540p preview  -> output/draft.mp4   (~1-2 min)
make render       # full 1080p film     -> output/colonel_sanders_documentary.mp4
```

`make setup` runs:

```bash
pip install -r requirements.txt
bash scripts/fetch_voice.sh    # Piper neural voice (en_US-ryan-high)
bash scripts/fetch_fonts.sh    # Montserrat (captions) + Anton (titles), OFL
```

> Requires `ffmpeg` and Python 3.10+. No GPU needed (CPU only).

### Common options

```bash
python3 render.py --draft                 # 540p/24fps preview
python3 render.py                          # 1080p/30fps final
python3 render.py --width 2560 --height 1440 --crf 16   # 1440p
python3 render.py --limit 6 --draft        # render only the first 6 beats
python3 render.py --no-captions            # clean plate (burn captions elsewhere)
python3 render.py --music path/to/track.mp3  # use a real music bed
python3 render.py --storyboard-only        # (re)write the image-prompt sheet
```

---

## Montage editing (many clips)

The edit is cut as a fast montage — each narration line is split into several
short sub-clips with quick cuts (whip / light-flash / speed-ramp / dissolve),
each with its own camera move, while the captions keep running across the cuts.

```bash
python3 render.py --clip-density 1.8   # more, faster cuts
python3 render.py --clip-density 3.0   # fewer, slower cuts
python3 render.py --no-montage         # one shot per line
```

Feed the montage with real footage by supplying **multiple assets per beat**:

- Extra photos: `assets/images/04_closed-2.jpg`, `04_closed-3.jpg`, …
- Video clips: `assets/clips/04_closed.mp4` (and `-2.mp4`, …) — used as moving
  B-roll for that line.

With a single photo per beat, the montage automatically re-frames it (a
different zoom/crop per cut) so it still reads as several distinct shots.

## Photoreal mode

The default render uses **procedurally synthesized cinematic plates** so it
always works without external assets. For a true Hollywood / ultra-realistic
1950s look, supply real photos:

1. Generate the image-prompt sheet:

   ```bash
   make storyboard      # writes storyboard/storyboard.md
   ```

2. `storyboard/storyboard.md` lists every shot with a ready-to-use photoreal
   image prompt and the exact **file name** to save it as.

3. Create each image (any AI image generator or licensed stock photo) and drop
   it into `assets/images/` using that file name, e.g.:

   ```
   assets/images/00_title.jpg
   assets/images/01_portrait.jpg
   assets/images/04_closed.jpg
   ...
   ```

   Recommended: 2560×1440 or larger, 16:9.

4. Re-run `make render`. Any beat with a supplied photo uses it automatically
   (with full camera motion, parallax/depth, DOF, grading and captions); beats
   without one fall back to the synthesized plate. Mix and match freely.

---

## What's in the edit

**Camera & motion** (`pipeline/effects.py`)
- Smooth cinematic **push-in** / pull-out, **3D zoom**, **tracking** pans
- **Parallax / depth** — background and a foreground plate move at different
  rates (real depth-of-field blur behind the subject)
- **Camera shake** that grows with each line's emotional intensity
- Eased (smootherstep) keyframe motion — never a static frame

**Transitions** (`pipeline/compositor.py`)
- **Dissolve**, **light flash**, **speed ramp** (motion-blurred), **whip** L/R

**Look** (`pipeline/effects.py::LookEngine`)
- Warm cinematic **color grade** (teal-shadow / warm-highlight, contrast, sat)
- **Bloom / glow**, **lens flare**, drifting **dust particles**, **film grain**,
  **vignette**

**Captions** (`pipeline/captions.py`)
- Large bold white, **word-by-word** pop-in reveal, drop-shadow for legibility
- **Keyword highlighting** in glowing gold (`REJECTED`, `PERSISTENCE`,
  `SUCCESS`, `NEVER QUIT`, and related power words)
- Giant centered **hero title cards** for the final screen (Anton typeface)

**Narration** (`pipeline/narration.py`)
- Neural **Piper TTS**, slowed for gravitas and **pitch-deepened** with EQ,
  compression and subtle room reverb for the "legendary mentor" tone
- Scripted **dramatic pauses**; word timing drives the caption animation

**Score** (`pipeline/music.py`)
- Procedural **orchestral-style** bed (string pads + sub + swells + impact hits)
  whose dynamics follow the story's **emotional arc** and **build in the final
  30 seconds**; ducked under the voice via sidechain compression

**Story & timing** (`pipeline/script.py`)
- The full narration is the exact script from the brief, broken into ~55 beats
  (one scene per line → a cut every few seconds for maximum retention),
  opening with a 3-second hook and ending on a dramatic fade-out

---

## Project layout

```
render.py                 # CLI entry point
pipeline/
  config.py               # all render settings + quality presets
  script.py               # the storyboard: lines, scenes, effects, intensity
  narration.py            # neural TTS + dramatic pacing + word timing
  scenes.py               # photo loader + procedural cinematic plate generator
  effects.py              # camera paths, transitions, color/light look
  captions.py             # animated keyword captions + hero title cards
  music.py                # procedural cinematic score with emotional arc
  compositor.py           # frame compositor + ffmpeg encode orchestrator
assets/images/            # drop real photos here (see storyboard sheet)
assets/music/             # optional: score.wav/mp3 to override the synth
assets/fonts/             # Montserrat + Anton (downloaded by setup)
models/                   # Piper voice model (downloaded by setup)
storyboard/storyboard.md  # generated shot list + image prompts
output/                   # rendered video + caches
```

## Tuning the run-time / pacing

The piece is timed to ~5:00 via the narration. Adjust in `pipeline/config.py`
or on the CLI:

- `--length-scale` (speech speed, higher = slower) and `--pause-scale`
  (dramatic pause multiplier) change total length; the visuals auto-resync.

## Credits & licenses

- Voice: [Piper](https://github.com/rhasspy/piper) (`en_US-ryan-high`, MIT-licensed model)
- Fonts: Montserrat & Anton — SIL Open Font License
- Code: this repository. Music is synthesized (royalty-free).

This is an original, educational/motivational retelling. Supply your own
licensed imagery for any public/commercial use.
