#!/usr/bin/env python3
"""Render the Colonel Sanders cinematic motivational documentary.

Examples
--------
    python3 render.py --draft              # fast 540p preview
    python3 render.py                       # full 1080p render
    python3 render.py --width 2560 --height 1440 --crf 16
    python3 render.py --storyboard         # also (re)write the image prompt sheet
    python3 render.py --limit 6 --draft    # render only the first 6 beats
"""
from __future__ import annotations

import argparse
from pathlib import Path

from pipeline import config
from pipeline.script import storyboard


def write_storyboard_sheet() -> Path:
    beats = storyboard()
    out = config.ROOT / "storyboard" / "storyboard.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Storyboard & Image Prompts",
        "",
        "Drop a photoreal image for any beat into `assets/images/` using the",
        "**file name** column below (e.g. `assets/images/04_closed.jpg`). The",
        "renderer will use it automatically with full cinematic motion; any beat",
        "without a supplied image falls back to a synthesized cinematic plate.",
        "",
        "**Montage / many clips.** The edit cuts several quick sub-clips per line.",
        "To feed the montage with real footage, supply *multiple* assets per beat:",
        "",
        "- Extra photos: `04_closed-2.jpg`, `04_closed-3.jpg`, ... (any number).",
        "- Video clips: `04_closed.mp4` (or `assets/clips/04_closed.mp4`), plus",
        "  `04_closed-2.mp4`, ... — used as moving B-roll for that line.",
        "",
        "If only one image is supplied, the montage automatically re-frames it",
        "(different zoom/crop per cut). Control cut speed with `--clip-density`.",
        "",
        "Recommended size: 2560x1440 or larger, 16:9. Suggested style suffix for",
        "every prompt: *photoreal, 1950s America, cinematic lighting, Kodachrome,",
        "film grain, shallow depth of field, ultra realistic, no text*.",
        "",
        "| # | File name | Scene | Effect | Narration | Image prompt |",
        "|---|-----------|-------|--------|-----------|--------------|",
    ]
    for b in beats:
        narr = b.text.replace("|", "/")
        prm = b.prompt.replace("|", "/")
        lines.append(
            f"| {b._index} | `{b.key}.jpg` | {b.scene} | {b.effect} "
            f"| {narr} | {prm} |"
        )
    out.write_text("\n".join(lines) + "\n")
    return out


def build_cfg(args) -> config.RenderConfig:
    cfg = config.RenderConfig()
    if args.draft:
        cfg = config.draft(cfg)
    if args.width:
        cfg.width = args.width
    if args.height:
        cfg.height = args.height
    if args.fps:
        cfg.fps = args.fps
    if args.crf is not None:
        cfg.crf = args.crf
    if args.preset:
        cfg.preset = args.preset
    if args.out:
        cfg.out_file = args.out
    if args.music:
        cfg.music_file = args.music
    if args.no_captions:
        cfg.captions = False
    if args.no_montage:
        cfg.montage = False
    if args.clip_density is not None:
        cfg.clip_density = args.clip_density
    if args.limit:
        cfg.limit_beats = args.limit
    if args.pause_scale is not None:
        cfg.pause_scale = args.pause_scale
    if args.length_scale is not None:
        cfg.voice_length_scale = args.length_scale
    if args.voice:
        cfg.voice_model = args.voice
    return cfg


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--draft", action="store_true", help="fast 540p/24fps preview")
    p.add_argument("--width", type=int)
    p.add_argument("--height", type=int)
    p.add_argument("--fps", type=int)
    p.add_argument("--crf", type=int)
    p.add_argument("--preset")
    p.add_argument("--out")
    p.add_argument("--music", help="path to a real music track to use instead of synth")
    p.add_argument("--voice", help="path to a Piper .onnx voice model")
    p.add_argument("--no-captions", action="store_true")
    p.add_argument("--no-montage", action="store_true",
                   help="one shot per line instead of many montage cuts")
    p.add_argument("--clip-density", type=float,
                   help="target seconds per clip (lower = more cuts, default 2.2)")
    p.add_argument("--limit", type=int, help="render only the first N beats")
    p.add_argument("--pause-scale", type=float)
    p.add_argument("--length-scale", type=float)
    p.add_argument("--storyboard", action="store_true",
                   help="(re)write storyboard/storyboard.md and exit unless rendering")
    p.add_argument("--storyboard-only", action="store_true",
                   help="only write the storyboard sheet, do not render")
    args = p.parse_args()

    config.ensure_dirs()
    if args.storyboard or args.storyboard_only:
        sheet = write_storyboard_sheet()
        print(f"Wrote storyboard sheet -> {sheet}")
        if args.storyboard_only:
            return

    from pipeline import compositor
    cfg = build_cfg(args)
    out = compositor.render(cfg)
    print(f"\nFinished: {out}")


if __name__ == "__main__":
    main()
