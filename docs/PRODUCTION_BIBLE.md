# Production Bible — *The Art of Never Quitting*

A premium, cinematic motivational documentary about Donald Trump, told purely as
a story of **ambition, resilience, risk, failure and the comeback mindset**.
**Non-political by design.** Runtime **~13:17** (target 13–15 min), 1920×1080, 30 fps.

This document is the creative + technical spec. The film is generated entirely
from code and copyright-free assets — see `README.md` for the build pipeline.

---

## 1. How the reference video was used

The reference clip was studied **only as an editing benchmark** — pacing, hook
discipline, caption animation, camera energy, music timing, retention technique.
**Nothing** was copied: not the script, narration, structure, scenes, visuals or
content. Story, voice, score and every frame here are original.

## 2. Voice & tone

- **Narrator:** deep American male, authoritative, intelligent, inspiring.
- Implemented with the neural `en_US-ryan-high` voice, then **pitch-deepened
  (~6%), warm-EQ'd, lightly compressed and given a touch of room** for a
  broadcast-documentary timbre (`audio/build_audio.py` → `VO_FILTER`).
- **Slow, dramatic pacing**: `length_scale 1.13`, sentence silences, and
  scripted `...` beats plus per-cue pauses create deliberate gravitas.

## 3. Score & sound (100% original, royalty-free)

- Synthesised from scratch in `audio/make_music.py` — evolving pads, sub-bass,
  transition booms, risers and a building finale.
- **Emotional arc** drives chord + intensity per chapter (dark open → rise →
  fall → hopeful comeback → grand climax). See `MOOD` in `build_audio.py`.
- **Side-chain ducking** keeps the score under the voice automatically; the
  final minute swells with an octave shimmer and a heartbeat sub-pulse.

## 4. Subtitle / caption spec

- Large, bold cinematic captions (Inter 800), centered lower-third.
- **Word-by-word karaoke animation**: the active word pops (spring scale + lift),
  spoken words are bright, upcoming words dimmed.
- **Keyword highlighting**: words wrapped in `*asterisks*` in the script render
  in the chapter accent colour and UPPERCASE (e.g. *undeniable*, *comeback*).
- Timing is frame-accurate — derived from the **measured** length of each spoken
  cue, so captions always match the voice. Sidecar `captions.srt` is exported.

## 5. Visual language

| Layer | Technique |
|---|---|
| B-roll | Real copyright-free clips (skylines, rain, mountains, aurora, city drives, aerials), **slow-motion + Ken Burns + looped** to fill each chapter |
| Grade | Contrast + low-saturation base + per-chapter accent tint (soft-light) + screen glow for a cohesive teal-orange cinematic look |
| Motion-graphics scenes | Original procedural backdrops where no clip fits: parallax skyline, starfield, blueprint grid, dot-matrix world map w/ arcs, anamorphic flares, rising embers |
| Title sequences | `Anton` display type, staggered word springs, clip-path wipes, accent rules |
| Chapter cards | Big ghost numerals, accent kicker, wipe-in title, animated rule |
| Camera | Handheld micro-shake + **boom kicks** on every chapter transition |
| Finish | Cinematic letterbox, vignette, moving film grain, drifting light leak, open/close fades |

Captions are kept **outside** the camera-shake group so text stays rock-steady.

## 6. Retention design

- **Hook in <3s**: "Love him… or hate him." over a dark anamorphic flare.
- **Mini-cliffhangers** end most chapters ("…build him, or destroy him?",
  "And the fall… was coming.", "Sometimes it is the *beginning* of the real one.").
- **Constant motion**: Ken Burns, parallax, slow-mo, shimmering type — never a
  static frame. Backdrop crossfades every chapter; captions animate every word.
- **Curiosity loops & pattern interrupts**: scene/colour palette flips per
  chapter; booms + risers cue the brain that something changed.
- Subtle **progress bar + chapter HUD** orient the viewer without clutter.

## 7. Structure (15 segments)

Cold open → Title (*The Art of Never Quitting*) → Ch.1 Roots → Ch.2 The Forge →
Ch.3 The Apprentice → Ch.4 The Rise → Ch.5 The Icon → Ch.6 The Fall →
Ch.7 The Comeback → Ch.8 The Brand → Ch.9 The Playbook (leadership) →
Ch.10 The Mind (mindset) → Ch.11 The Price (what success requires) →
Ch.12 The Climb (final motivation) → End card: **THINK BIGGER. STAY RESILIENT.
NEVER QUIT.**

Full narration: `docs/SCRIPT.md`. Asset licensing: `docs/CREDITS.md`.

## 8. Authenticity / safety notes

- Framed strictly around universal lessons (confidence, persistence, risk,
  adaptability, responsibility). No partisan claims.
- Biographical beats are kept to widely-documented, non-controversial business
  history (Queens upbringing, military academy, Wharton, Manhattan deals,
  1990s debt crisis & restructuring, brand/television era).
- No real footage or images of any individual are used; all B-roll is generic.
