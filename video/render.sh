#!/usr/bin/env bash
# Resilient chunked render.
#
# Renders the documentary in muted video-only segments (so a stalled
# OffthreadVideo frame can't kill the whole render), retrying any failed
# segment at progressively lower concurrency, then concatenates the segments
# and muxes the pre-baked master audio. Completed segments are skipped on
# re-run, so the render is fully resumable.
set -u
cd "$(dirname "$0")"

TOTAL=$(node -e "console.log(require('./src/data/timeline.json').durationInFrames)")
AUDIO="public/audio/final_audio.m4a"
CHUNK=1500
mkdir -p out/chunks
: > out/chunklist.txt

idx=0
for ((start=0; start<TOTAL; start+=CHUNK)); do
  end=$((start + CHUNK - 1)); (( end >= TOTAL )) && end=$((TOTAL - 1))
  f=$(printf "out/chunks/%03d.mp4" "$idx")
  if [[ -f "$f" ]] && [[ "$(node -e "try{console.log(require('fs').statSync('$f').size>10000)}catch(e){console.log(false)}")" == "true" ]]; then
    echo "== skip existing chunk $idx ($start-$end)"
  else
    ok=0
    for conc in 4 2 1; do
      echo "== chunk $idx frames $start-$end  concurrency=$conc"
      if npx remotion render Documentary "$f" --frames="${start}-${end}" --muted --concurrency="$conc"; then
        ok=1; break
      else
        echo "!! chunk $idx failed at concurrency $conc"; rm -f "$f"
      fi
    done
    (( ok == 0 )) && { echo "FATAL: chunk $idx failed at all concurrencies"; exit 1; }
  fi
  echo "file '$(pwd)/$f'" >> out/chunklist.txt
  idx=$((idx + 1))
done

echo "== concatenating $idx segments"
if ! ffmpeg -y -loglevel error -f concat -safe 0 -i out/chunklist.txt -c copy out/video_only.mp4; then
  echo "== copy concat failed; re-encoding"
  ffmpeg -y -loglevel error -f concat -safe 0 -i out/chunklist.txt -c:v libx264 -crf 18 -preset veryfast out/video_only.mp4
fi

echo "== muxing master audio"
ffmpeg -y -loglevel error -i out/video_only.mp4 -i "$AUDIO" -c:v copy -c:a aac -b:a 160k -shortest out/documentary.mp4

dur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 out/documentary.mp4)
echo "RENDER_COMPLETE duration=${dur}s file=out/documentary.mp4"
