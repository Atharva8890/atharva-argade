# Motivational Voiceover Generator — "Comfort Is Expensive"

AI voiceover for a USA motivational YouTube channel, in a Napoleon Hill–style
authentic, deep, confident delivery. Built with Microsoft Edge's free neural
text-to-speech (`edge-tts`).

## What's included

| File | Description |
| --- | --- |
| `script.txt` | The full narration script ("Comfort is expensive. Discipline is hard. Regret is harder."). |
| `generate_voice.py` | Generates an MP3 voiceover from the script. |
| `output/voiceover_andrew.mp3` | **Main take** — `en-US-AndrewNeural` (warm, confident, *authentic*). ~1:50 |
| `output/voiceover_christopher.mp3` | Alternative — `en-US-ChristopherNeural` (reliable, authoritative). ~2:16 |
| `make_captions.py` | Generates audio **+** word-synced `.ass` captions in one pass. |
| `make_video.sh` | Renders the final 9:16 video (background + captions + voiceover). |
| `output/captions.ass` | Word-synced captions (punchy 1–3 word chunks, gold power-words). |
| `output/comfort_is_expensive.mp4` | **Final video** — 1080×1920, 30 fps, ready for YouTube Shorts / Reels. |
| `requirements.txt` | Python dependency. |

## Quick start

```bash
pip install -r requirements.txt

# Main authentic voice (Andrew)
python3 generate_voice.py --voice andrew --rate="-8%" --pitch="-2Hz"

# Authoritative alternative (Christopher)
python3 generate_voice.py --voice christopher --rate="-6%" --pitch="-3Hz"
```

The audio is written to the `output/` folder as an MP3 you can drop straight
into your video editor (CapCut, Premiere, DaVinci Resolve, etc.).

## Make the full video (9:16)

```bash
# 1) Generate the voiceover + perfectly synced captions
python3 make_captions.py --voice andrew --rate="-8%" --pitch="-2Hz" \
    --audio output/voiceover_andrew.mp3 --ass output/captions.ass

# 2) Render the video (animated dark gradient + vignette + burned captions + audio)
./make_video.sh output/voiceover_andrew.mp3 output/captions.ass output/comfort_is_expensive.mp4
```

The result is `output/comfort_is_expensive.mp4` — a vertical 1080×1920 video with
bold, word-synced captions (key "power words" in gold) over a cinematic dark
background. Upload it directly, or add your own background music / B-roll in your
editor first. Requires `ffmpeg` (with libass) installed.

## Options

- `--voice`  : preset (`andrew`, `christopher`, `guy`, `brian`) or any full
  edge-tts voice id (run `python3 -m edge_tts --list-voices`).
- `--rate`   : speaking speed, e.g. `--rate="-10%"` (slower) or `--rate="+5%"`.
- `--pitch`  : pitch shift, e.g. `--pitch="-3Hz"` for a deeper tone.
- `--volume` : loudness, e.g. `--volume="+0%"`.
- `--script` : path to a different text file.
- `--out`    : custom output path.

> Tip: use the `=` form for negative values (`--rate="-8%"`) so they aren't
> parsed as flags.

## Editing the script

Just edit `script.txt` and re-run the command. Keep one idea per line/paragraph;
blank lines give the narrator natural breathing room.

## Notes

- `edge-tts` requires an internet connection.
- These are synthetic AI voices (not a recording of any real person), so they
  are safe to monetize on YouTube. Always confirm your channel follows
  YouTube's policies on AI-generated/automated content disclosure.
- Add your own background music and B-roll on top of the voiceover in your editor.
