# THE ART OF NEVER QUITTING

An **original, code-generated cinematic motivational documentary** about Donald
Trump — told as a story of ambition, resilience, risk, failure and the comeback
mindset (intentionally **non-political**). Target runtime **13–15 minutes**;
current build is **~13:17 @ 1920×1080, 30fps**.

Everything here is generated from scratch — the script, the narration, the
score and every visual. There is **no stock footage, no copyrighted music, and
nothing copied** from any reference video. The reference clip was used only as a
benchmark for *editing quality and cinematic presentation*.

https://github.com/  ·  see `docs/` for the full production bible & script.

---

## What's in the box

```
audio/
  script_data.py     # SINGLE SOURCE OF TRUTH — full original narration, by chapter
  build_audio.py     # Piper neural TTS -> deep US-male VO, timeline, SRT, script
  make_music.py      # original procedural cinematic score (numpy synthesis)
  voices/            # Piper voice model (downloaded, gitignored)
  reference/         # full-quality WAV stems (gitignored, regenerable)
video/               # Remotion project (the film itself)
  src/
    Documentary.tsx  # composition root
    scenes/Scenes.tsx        # procedural backdrops (skyline/stars/grid/map/flares/embers)
    components/      # captions, chapter cards, end card, overlays (grain/vignette/shake…)
    data/timeline.json       # GENERATED — drives the whole video
  public/
    audio/final_audio.m4a    # the baked-in master soundtrack
    captions.srt             # sidecar subtitles
docs/
  SCRIPT.md          # GENERATED human-readable shooting script
  PRODUCTION_BIBLE.md# editing style, subtitle spec, music + retention map
```

## How it fits together

1. `audio/script_data.py` holds the entire narration as chapters → cues.
2. `python3 audio/build_audio.py`:
   - synthesises every cue with **Piper** (deep American-male neural voice),
     deepens/EQ/compresses it for a broadcast feel,
   - measures the real audio length of each line and lays out an **absolute,
     frame-accurate timeline** (`video/src/data/timeline.json`),
   - renders an **original score** that tracks the emotional arc and
     **side-chain ducks** it under the voice,
   - writes the master mix, the `.srt`, and `docs/SCRIPT.md`.
3. **Remotion** reads `timeline.json` and renders the film, syncing word-by-word
   captions, chapter cinematics, maps/timelines and transitions to the audio.

## Build it yourself

```bash
# 1) audio + timeline (needs the Piper model in audio/voices/)
pip install piper-tts numpy
python3 audio/build_audio.py

# 2) the video
cd video
npm install
npm run render        # -> video/out/documentary.mp4
npm start             # interactive Remotion Studio for previewing/tweaking
```

If `audio/voices/en_US-ryan-high.onnx` is missing, download it from the
`rhasspy/piper-voices` repo (see `docs/PRODUCTION_BIBLE.md`).

## Swapping the audio

The video consumes a single file: `video/public/audio/final_audio.m4a`.
Drop in any narration/music master with that name (or re-run `build_audio.py`)
and re-render. The captions stay in sync because timing is read from
`timeline.json`; regenerate that too if you change the spoken length of lines.
