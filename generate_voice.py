#!/usr/bin/env python3
"""Generate a motivational voiceover from a text script using Microsoft Edge neural TTS.

Usage:
    python3 generate_voice.py                      # default: Andrew voice -> output/voiceover_andrew.mp3
    python3 generate_voice.py --voice en-US-ChristopherNeural --out output/voiceover_christopher.mp3
    python3 generate_voice.py --rate -8% --pitch -3Hz

Requirements: edge-tts (pip install edge-tts), internet access.
"""
import argparse
import asyncio
import sys
from pathlib import Path

import edge_tts

# Deep / authoritative male voices that suit motivational narration.
PRESETS = {
    "andrew": "en-US-AndrewNeural",          # warm, confident, authentic
    "christopher": "en-US-ChristopherNeural",  # reliable, authoritative
    "guy": "en-US-GuyNeural",                # passionate
    "brian": "en-US-BrianNeural",            # approachable, sincere
}


async def synthesize(text: str, voice: str, rate: str, pitch: str, volume: str, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        pitch=pitch,
        volume=volume,
    )
    await communicate.save(str(out_path))


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a TTS voiceover from a script.")
    parser.add_argument("--script", default="script.txt", help="Path to the input text script.")
    parser.add_argument("--voice", default="andrew",
                        help="Voice preset (andrew/christopher/guy/brian) or a full edge-tts voice id.")
    parser.add_argument("--out", default=None, help="Output audio file path (.mp3).")
    parser.add_argument("--rate", default="-8%", help="Speaking rate, e.g. -10%%, +5%%.")
    parser.add_argument("--pitch", default="-2Hz", help="Pitch shift, e.g. -3Hz, +0Hz.")
    parser.add_argument("--volume", default="+0%", help="Volume adjustment, e.g. +0%%.")
    args = parser.parse_args()

    voice = PRESETS.get(args.voice.lower(), args.voice)

    script_path = Path(args.script)
    if not script_path.exists():
        print(f"Script not found: {script_path}", file=sys.stderr)
        return 1
    text = script_path.read_text(encoding="utf-8").strip()
    if not text:
        print("Script is empty.", file=sys.stderr)
        return 1

    if args.out:
        out_path = Path(args.out)
    else:
        label = args.voice.lower() if args.voice.lower() in PRESETS else "custom"
        out_path = Path("output") / f"voiceover_{label}.mp3"

    print(f"Voice : {voice}")
    print(f"Rate  : {args.rate}   Pitch: {args.pitch}   Volume: {args.volume}")
    print(f"Output: {out_path}")
    asyncio.run(synthesize(text, voice, args.rate, args.pitch, args.volume, out_path))
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
