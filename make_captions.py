#!/usr/bin/env python3
"""Synthesize the voiceover AND build word-synced ASS captions in one pass.

Captures edge-tts WordBoundary events so the on-screen captions line up exactly
with the spoken audio. Captions are grouped into short, punchy chunks (1-3 words)
for the viral motivational look, with key "power words" highlighted in gold.

Usage:
    python3 make_captions.py --voice andrew --rate="-8%" --pitch="-2Hz" \
        --audio output/voiceover_andrew.mp3 --ass output/captions.ass
"""
import argparse
import asyncio
from pathlib import Path

import edge_tts

PRESETS = {
    "andrew": "en-US-AndrewNeural",
    "christopher": "en-US-ChristopherNeural",
    "guy": "en-US-GuyNeural",
    "brian": "en-US-BrianNeural",
}

# Words that get the gold emphasis colour.
POWER_WORDS = {
    "expensive", "hard", "harder", "regret", "discipline", "comfort",
    "today", "never", "tons", "ounces", "price", "choose",
}

MAX_WORDS = 3          # max words per caption cue
ASS_PLAY_W = 1080
ASS_PLAY_H = 1920

ASS_HEADER = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {ASS_PLAY_W}
PlayResY: {ASS_PLAY_H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,DejaVu Sans,94,&H00FFFFFF,&H000000FF,&H00101010,&H96000000,-1,0,0,0,100,100,1,0,1,6,4,5,110,110,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

GOLD = r"{\1c&H0000B9FF&}"
WHITE = r"{\1c&HFFFFFF&}"


def fmt_time(sec: float) -> str:
    if sec < 0:
        sec = 0
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"


def is_power(word: str) -> bool:
    return word.strip(".,!?;:'\"").lower() in POWER_WORDS


async def run(text, voice, rate, pitch, volume, audio_path, ass_path):
    Path(audio_path).parent.mkdir(parents=True, exist_ok=True)
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate,
                                        pitch=pitch, volume=volume,
                                        boundary="WordBoundary")
    words = []  # (start_sec, end_sec, text)
    with open(audio_path, "wb") as af:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                af.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                start = chunk["offset"] / 1e7
                dur = chunk["duration"] / 1e7
                words.append((start, start + dur, chunk["text"]))

    # Group words into short cues; break on sentence-ending punctuation.
    cues = []  # (start, end, [words])
    cur = []
    for w in words:
        cur.append(w)
        ends_sentence = w[2].rstrip().endswith((".", "!", "?", ":", ";", ","))
        if len(cur) >= MAX_WORDS or ends_sentence:
            cues.append(cur)
            cur = []
    if cur:
        cues.append(cur)

    lines = [ASS_HEADER]
    for i, group in enumerate(cues):
        start = group[0][0]
        end = group[-1][1]
        # extend each cue to the next one's start so text never flickers off early
        if i + 1 < len(cues):
            nxt = cues[i + 1][0][0]
            end = max(end, nxt - 0.02)
        words_txt = []
        for (_, _, t) in group:
            clean = t.strip().upper()
            colour = GOLD if is_power(t) else WHITE
            words_txt.append(f"{colour}{clean}")
        text_field = " ".join(words_txt)
        # fade in/out + subtle pop-in scale
        effect = r"{\fad(90,70)}"
        lines.append(
            f"Dialogue: 0,{fmt_time(start)},{fmt_time(end)},Main,,0,0,0,,{effect}{text_field}"
        )

    Path(ass_path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Audio  : {audio_path}")
    print(f"Captions: {ass_path}  ({len(cues)} cues from {len(words)} words)")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--script", default="script.txt")
    p.add_argument("--voice", default="andrew")
    p.add_argument("--rate", default="-8%")
    p.add_argument("--pitch", default="-2Hz")
    p.add_argument("--volume", default="+0%")
    p.add_argument("--audio", default="output/voiceover_andrew.mp3")
    p.add_argument("--ass", default="output/captions.ass")
    a = p.parse_args()
    voice = PRESETS.get(a.voice.lower(), a.voice)
    text = Path(a.script).read_text(encoding="utf-8").strip()
    asyncio.run(run(text, voice, a.rate, a.pitch, a.volume, a.audio, a.ass))


if __name__ == "__main__":
    main()
