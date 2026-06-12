#!/usr/bin/env bash
# Download the Piper neural voice used for narration.
# Default: en_US-ryan-high (clear American male, deepened/slowed at render time
# for the "wise elderly mentor" tone). Override with VOICE_URL_BASE.
set -euo pipefail

cd "$(dirname "$0")/.."
mkdir -p models

VOICE="${1:-en_US-ryan-high}"
BASE="${VOICE_URL_BASE:-https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US}"

case "$VOICE" in
  en_US-ryan-high)        URL="$BASE/ryan/high/en_US-ryan-high" ;;
  en_US-john-medium)      URL="$BASE/john/medium/en_US-john-medium" ;;
  en_US-norman-medium)    URL="$BASE/norman/medium/en_US-norman-medium" ;;
  en_US-hfc_male-medium)  URL="$BASE/hfc_male/medium/en_US-hfc_male-medium" ;;
  *) echo "Unknown voice '$VOICE'. Pass a full base path via VOICE_URL_BASE." >&2; exit 1 ;;
esac

echo "Downloading $VOICE ..."
curl -fsSL -o "models/$VOICE.onnx"      "$URL.onnx"
curl -fsSL -o "models/$VOICE.onnx.json" "$URL.onnx.json"
echo "Saved to models/$VOICE.onnx"
