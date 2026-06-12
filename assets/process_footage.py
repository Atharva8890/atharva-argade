# -*- coding: utf-8 -*-
"""
Pre-process curated B-roll into render-friendly clips.

Problem: playing footage in Remotion with playbackRate + <Loop> forces many
non-keyframe seeks per frame, which is slow and can time out OffthreadVideo.

Fix: bake the slow-motion + looping + exact length here with ffmpeg, so Remotion
plays each chapter's clip LINEARLY at rate 1.0 (keyframe-friendly = fast/robust).

For every chapter (in timeline order) that has footage, we emit one clip sized to
fully cover that chapter's on-screen slot. Output keyed by chapter INDEX so reuse
(e.g. the summit clip in both 'comeback' and 'finale') and the endcard/finale key
collision are handled cleanly.

Outputs:
  video/public/footage_proc/<i>.mp4
  video/src/data/footage_proc.json   ->  {"clips": {"<i>": "<i>.mp4"}}

Run:  python3 assets/process_footage.py
"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "video" / "public" / "footage"
OUT = ROOT / "video" / "public" / "footage_proc"
OUT.mkdir(parents=True, exist_ok=True)
TL = json.loads((ROOT / "video" / "src" / "data" / "timeline.json").read_text())
FOOT = json.loads((ROOT / "video" / "src" / "data" / "footage.json").read_text())["byChapter"]

PLAYBACK = 0.62            # cinematic slow-motion factor
PAD = 2.6                 # extra seconds beyond chapter length (covers crossfades)
FPS = TL["fps"]


def src_for(ch):
    key = "endcard" if ch["kind"] == "endcard" else ch["key"]
    return FOOT.get(key)


def main():
    chapters = TL["chapters"]
    total = TL["totalSeconds"]
    clips = {}
    for i, ch in enumerate(chapters):
        clip = src_for(ch)
        if not clip:
            continue
        start = ch["start"]
        end = chapters[i + 1]["start"] if i + 1 < len(chapters) else total
        slot = (end - start) + PAD
        src = SRC / clip["file"]
        if not src.exists():
            print(f"  ! missing source {src}")
            continue
        dest = OUT / f"{i}.mp4"
        ss = clip.get("startFrom", 0) or 0
        vf = (
            f"setpts=PTS/{PLAYBACK},"
            f"scale=1920:1080:force_original_aspect_ratio=increase,"
            f"crop=1920:1080,fps={FPS},format=yuv420p"
        )
        cmd = [
            "ffmpeg", "-y", "-loglevel", "error",
            "-stream_loop", "-1", "-ss", str(ss), "-i", str(src),
            "-t", f"{slot:.2f}", "-an", "-vf", vf,
            "-c:v", "libx264", "-crf", "20", "-preset", "veryfast",
            "-g", str(FPS), "-movflags", "+faststart", str(dest),
        ]
        r = subprocess.run(cmd, capture_output=True)
        if r.returncode != 0 or not dest.exists():
            print(f"  ! ffmpeg failed for ch{i} ({clip['file']}):")
            print(r.stderr.decode()[-600:])
            continue
        clips[str(i)] = dest.name
        print(f"  + ch{i:2d} {ch['kind']:8} {ch['key']:10} <- {clip['file']:32} "
              f"slot={slot:5.1f}s  {dest.stat().st_size//1024}KB")

    (ROOT / "video" / "src" / "data" / "footage_proc.json").write_text(
        json.dumps({"clips": clips}, indent=2))
    print(f"\nDONE  {len(clips)} processed clips")


if __name__ == "__main__":
    main()
