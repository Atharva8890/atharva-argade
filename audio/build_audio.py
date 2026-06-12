# -*- coding: utf-8 -*-
"""
Build the full audio + synced timeline for the documentary.

Steps
-----
1. Synthesise every narration cue with Piper (deep US-male neural TTS).
2. Post-process each cue (deepen pitch, warm EQ, light room) -> consistent VO.
3. Measure real durations and lay out an absolute timeline (lead-in, pauses,
   chapter cards, end card).
4. Concatenate the narration, generate an ORIGINAL procedural score that tracks
   the emotional arc, and side-chain duck the music under the voice.
5. Emit:
      video/public/audio/final_audio.wav   (master mix used by Remotion)
      video/public/audio/narration.wav      (VO only, reference)
      video/public/audio/music.wav          (score only, reference)
      video/src/data/timeline.json          (drives the video)
      video/public/captions.srt             (sidecar subtitles)
      docs/SCRIPT.md                         (human-readable shooting script)

Run:  python3 audio/build_audio.py
"""
import json
import math
import os
import re
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
AUDIO = ROOT / "audio"
sys.path.insert(0, str(AUDIO))
import script_data as SD          # noqa: E402
from make_music import render_music, SR  # noqa: E402

HOME = Path(os.environ.get("HOME", "/home/ubuntu"))
PIPER = HOME / ".local" / "bin" / "piper"
MODEL = AUDIO / "voices" / "en_US-ryan-high.onnx"

OUT_AUDIO = ROOT / "video" / "public" / "audio"   # only the compressed master ships here
REF = ROOT / "audio" / "reference"                # full-quality WAV stems (gitignored)
OUT_DATA = ROOT / "video" / "src" / "data"
OUT_SRT = ROOT / "video" / "public" / "captions.srt"
DOCS = ROOT / "docs"
TMP = AUDIO / ".cache"
for d in (OUT_AUDIO, REF, OUT_DATA, DOCS, TMP):
    d.mkdir(parents=True, exist_ok=True)

FPS = 30
W, H = 1920, 1080
LEAD_IN = 2.0        # silence/score before the first word
TAIL = 2.2           # silence after the last word
ENDCARD_LEN = 7.5    # silent end-card with music swell
GAP_BONUS = 0.14     # extra breath added after every cue (pacing)

VO_FILTER = (
    "asetrate=22050*0.94,aresample=44100,atempo=1.0638298,"
    "highpass=f=80,"
    "equalizer=f=170:t=q:w=1.1:g=2.5,"
    "equalizer=f=3400:t=q:w=2:g=1.8,"
    "acompressor=threshold=-18dB:ratio=3:attack=10:release=200,"
    "aecho=0.85:0.9:55:0.15"
)

# emotional arc: one chord + intensity per chapter (Hz sets are original voicings)
A2, C3, D3, E3, F3, G3 = 110.0, 130.81, 146.83, 164.81, 174.61, 196.0
A3, B3, C4, D4, E4, F4, G4 = 220.0, 246.94, 261.63, 293.66, 329.63, 349.23, 392.0
MOOD = {
    "cold_open": (dict(chord=[A2, C3, E3], intensity=0.34), False),
    "title":     (dict(chord=[F3, A3, C4], intensity=0.42), True),
    "roots":     (dict(chord=[A2, C3, E3, A3], intensity=0.36), True),
    "discipline":(dict(chord=[D3, F3, A3], intensity=0.46), True),
    "learn":     (dict(chord=[E3, G3, B3], intensity=0.44), True),
    "build":     (dict(chord=[C3, E3, G3, C4], intensity=0.56), True),
    "fame":      (dict(chord=[F3, A3, C4, F4], intensity=0.60), True),
    "fall":      (dict(chord=[A2, C3, F3], intensity=0.52), True),
    "comeback":  (dict(chord=[C3, G3, C4, E4], intensity=0.60), True),
    "global":    (dict(chord=[G3, B3, D4, G4], intensity=0.64), True),
    "leadership":(dict(chord=[E3, G3, B3, E4], intensity=0.50), True),
    "mindset":   (dict(chord=[A2, C3, E3, A3], intensity=0.50), True),
    "success":   (dict(chord=[C3, E3, G3, C4], intensity=0.60), True),
    "finale":    (dict(chord=[F3, A3, C4, F4, C4], intensity=0.86), True),
}


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-2000:])
        raise RuntimeError(f"cmd failed: {' '.join(cmd[:3])} ...")
    return r


def read_wav_mono(path):
    with wave.open(str(path), "rb") as w:
        sr = w.getframerate()
        ch = w.getnchannels()
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    if ch > 1:
        data = data.reshape(-1, ch).mean(axis=1)
    if sr != SR:
        # linear resample
        n = int(round(len(data) * SR / sr))
        data = np.interp(np.linspace(0, len(data), n, endpoint=False), np.arange(len(data)), data).astype(np.float32)
    return data


def write_wav_mono(path, x):
    x = np.clip(x, -1, 1)
    pcm = (x * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def synth_cue(text, idx):
    raw = TMP / f"cue_{idx:03d}_raw.wav"
    proc = TMP / f"cue_{idx:03d}.wav"
    speak = text.replace("*", "").strip()
    p = subprocess.run(
        [str(PIPER), "-m", str(MODEL), "-f", str(raw),
         "--length_scale", "1.13", "--sentence_silence", "0.26"],
        input=speak, capture_output=True, text=True)
    if p.returncode != 0:
        sys.stderr.write(p.stderr[-1500:])
        raise RuntimeError("piper failed")
    sh(["ffmpeg", "-y", "-i", str(raw), "-af", VO_FILTER, "-ar", str(SR), "-ac", "1", str(proc)])
    return read_wav_mono(proc)


def tokenize(text):
    """Split into display words, flagging emphasis (*...*) spans."""
    words = []
    inside = False
    for raw in text.split():
        emph = inside or raw.startswith("*")
        stars = raw.count("*")
        if stars and (stars % 2 == 1):
            inside = not inside
        clean = raw.replace("*", "")
        if clean:
            words.append({"w": clean, "emph": bool(emph)})
    return words


def distribute_times(words, start, dur):
    weights = []
    for it in words:
        base = len(re.sub(r"[^A-Za-z0-9]", "", it["w"])) + 2
        if it["w"].endswith((".", "!", "?")):
            base += 3
        elif it["w"].endswith((",", ";", ":")):
            base += 1
        if "..." in it["w"]:
            base += 3
        weights.append(base)
    total = float(sum(weights)) or 1.0
    t = start
    for it, wgt in zip(words, weights):
        d = dur * wgt / total
        it["s"] = round(t, 3)
        it["e"] = round(t + d, 3)
        t += d
    return words


def make_lines(words):
    lines, cur = [], []
    for i, it in enumerate(words):
        cur.append(i)
        ends_sentence = it["w"].endswith((".", "!", "?"))
        ellipsis = it["w"] == "..." or it["w"].endswith("...")
        if len(cur) >= 6 or ellipsis or (ends_sentence and len(cur) >= 2):
            lines.append([cur[0], cur[-1] + 1])
            cur = []
    if cur:
        lines.append([cur[0], cur[-1] + 1])
    return lines


def srt_ts(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = int(t % 60); ms = int((t - int(t)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main():
    print("Synthesising narration with Piper ...")
    cursor = LEAD_IN
    cue_idx = 0
    chapters_out = []
    captions = []
    narr_pieces = []   # (start_sample, np.array)

    for ch in SD.CHAPTERS:
        ch_start = cursor
        first_word_start = None
        if ch["kind"] == "endcard":
            seg_start = cursor
            cursor += ENDCARD_LEN
            chapters_out.append({
                "key": ch["key"], "num": ch["num"], "kind": ch["kind"],
                "title": ch["title"], "kicker": ch["kicker"], "scene": ch["scene"],
                "theme": SD.THEMES[ch["key"]], "start": round(seg_start, 3), "end": round(cursor, 3),
            })
            continue

        for cue in ch["cues"]:
            audio = synth_cue(cue["t"], cue_idx)
            dur = len(audio) / SR
            start = cursor
            words = tokenize(cue["t"])
            distribute_times(words, start, dur)
            if first_word_start is None and words:
                first_word_start = words[0]["s"]
            lines = make_lines(words)
            captions.append({
                "chapter": ch["key"], "kind": ch["kind"],
                "start": round(start, 3), "end": round(start + dur, 3),
                "words": words, "lines": lines,
            })
            narr_pieces.append((int(start * SR), audio))
            cursor = start + dur + cue.get("pause", 0.45) + GAP_BONUS
            cue_idx += 1
            sys.stdout.write(f"\r  cue {cue_idx:>3}  t={cursor:6.1f}s")
            sys.stdout.flush()

        chapters_out.append({
            "key": ch["key"], "num": ch["num"], "kind": ch["kind"],
            "title": ch["title"], "kicker": ch["kicker"], "scene": ch["scene"],
            "theme": SD.THEMES[ch["key"]],
            "start": round(ch_start, 3), "end": round(cursor, 3),
            "cardAt": round(first_word_start if first_word_start else ch_start, 3),
        })
    print()

    total_sec = cursor + TAIL
    total_n = int(total_sec * SR) + SR

    # ---- assemble narration ----
    print("Assembling narration track ...")
    narr = np.zeros(total_n, dtype=np.float32)
    for s, a in narr_pieces:
        e = min(total_n, s + len(a))
        narr[s:e] += a[: e - s]
    # normalise VO to a comfortable RMS
    rms = float(np.sqrt(np.mean(narr ** 2))) or 1.0
    narr *= min(6.0, 0.12 / rms)
    narr = np.clip(narr, -1, 1)

    # ---- score ----
    print("Rendering original score ...")
    segments = []
    for i, ch in enumerate(chapters_out):
        mood, _ = MOOD[ch["key"]]
        seg = {"start": ch["start"] if i else 0.0, "end": ch["end"],
               "chord": mood["chord"], "intensity": mood["intensity"],
               "boom": i != 0, "riser": i not in (0,),
               "climax": ch["key"] == "finale"}
        segments.append(seg)
    music = render_music(segments, total_sec)
    if len(music) < total_n:
        music = np.pad(music, (0, total_n - len(music)))
    else:
        music = music[:total_n]

    # ---- side-chain duck music under VO ----
    print("Mixing (side-chain ducking) ...")
    w = int(0.18 * SR)
    absn = np.abs(narr)
    c = np.cumsum(np.insert(absn, 0, 0))
    env = (c[w:] - c[:-w]) / w
    env = np.pad(env, (w // 2, total_n - len(env) - w // 2), mode="edge")
    ref = (np.percentile(env, 92) or 1e-3) * 0.5
    gain = 1.0 - 0.72 * np.clip(env / (ref + 1e-9), 0, 1)
    final = narr + music * 0.55 * gain
    peak = float(np.max(np.abs(final))) or 1.0
    if peak > 0.99:
        final = final / peak * 0.99
    final = np.tanh(final * 1.05) * 0.97

    write_wav_mono(REF / "final_audio.wav", final)
    write_wav_mono(REF / "narration.wav", narr)
    write_wav_mono(REF / "music.wav", music)
    # compressed master actually consumed by the video (keeps repo + bundle light)
    sh(["ffmpeg", "-y", "-i", str(REF / "final_audio.wav"),
        "-c:a", "aac", "-b:a", "160k", str(OUT_AUDIO / "final_audio.m4a")])

    # ---- timeline.json ----
    timeline = {
        "fps": FPS, "width": W, "height": H,
        "totalSeconds": round(total_sec, 3),
        "durationInFrames": int(math.ceil(total_sec * FPS)),
        "audio": "audio/final_audio.m4a",
        "chapters": chapters_out,
        "captions": captions,
    }
    (OUT_DATA / "timeline.json").write_text(json.dumps(timeline, indent=2))

    # ---- SRT ----
    lines_srt = []
    n = 1
    for cap in captions:
        for ln in cap["lines"]:
            ws = cap["words"][ln[0]:ln[1]]
            text = " ".join(x["w"] for x in ws)
            s = ws[0]["s"]; e = ws[-1]["e"]
            lines_srt.append(f"{n}\n{srt_ts(s)} --> {srt_ts(e)}\n{text}\n")
            n += 1
    OUT_SRT.write_text("\n".join(lines_srt))

    # ---- human-readable script ----
    md = ["# THE ART OF NEVER QUITTING", "",
          f"*Original motivational documentary — runtime {int(total_sec//60)}:{int(total_sec%60):02d}*",
          "", "> Narration: deep American male, slow & cinematic. Score: original, ducked under VO.", ""]
    for ch in SD.CHAPTERS:
        if ch["kind"] == "endcard":
            md += [f"## END CARD", "", f"**{ch['title']}**", ""]
            continue
        label = ch["title"] if ch["kind"] != "chapter" else f"Chapter {ch['num']} — {ch['title']}"
        md += [f"## {label}", ""]
        if ch["kicker"]:
            md += [f"*{ch['kicker']}*", ""]
        for cue in ch["cues"]:
            md.append(cue["t"].replace("*", "**" if False else ""))
        md.append("")
    (DOCS / "SCRIPT.md").write_text("\n".join(md))

    print(f"\nDONE  runtime={total_sec:6.1f}s ({int(total_sec//60)}:{int(total_sec%60):02d})  "
          f"frames={timeline['durationInFrames']}  cues={cue_idx}")


if __name__ == "__main__":
    main()
