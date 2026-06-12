#!/usr/bin/env bash
# Build a 9:16 cinematic motivational video: animated dark gradient background
# + film grain + vignette, with word-synced captions burned in, plus the
# voiceover audio. Output is a ready-to-upload MP4 (YouTube Shorts / Reels).
#
# Usage:
#   ./make_video.sh [AUDIO_MP3] [CAPTIONS_ASS] [OUTPUT_MP4]
set -euo pipefail

AUDIO="${1:-output/voiceover_andrew.mp3}"
ASS="${2:-output/captions.ass}"
OUT="${3:-output/comfort_is_expensive.mp4}"

DUR=$(ffprobe -v error -show_entries format=duration \
        -of default=noprint_wrappers=1:nokey=1 "$AUDIO")
DUR=$(printf "%.2f" "$DUR")
echo "Audio duration: ${DUR}s -> $OUT"

ffmpeg -hide_banner -y \
  -f lavfi -i "gradients=s=1080x1920:c0=0x070710:c1=0x241734:c2=0x0a1226:x0=180:y0=140:x1=940:y1=1820:nb_colors=3:type=linear:speed=0.006:duration=${DUR}:rate=30" \
  -i "$AUDIO" \
  -filter_complex "[0:v]vignette=PI/5,format=yuv420p,ass=${ASS}[v]" \
  -map "[v]" -map "1:a" \
  -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 192k \
  -shortest -movflags +faststart \
  "$OUT"

echo "Done: $OUT"
