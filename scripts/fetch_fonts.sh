#!/usr/bin/env bash
# Download the caption fonts (Montserrat variable + Anton), both OFL licensed.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p assets/fonts
GF="https://github.com/google/fonts/raw/main/ofl"
curl -fsSL -o assets/fonts/Montserrat.ttf    "$GF/montserrat/Montserrat%5Bwght%5D.ttf"
curl -fsSL -o assets/fonts/Anton-Regular.ttf "$GF/anton/Anton-Regular.ttf"
echo "Fonts saved to assets/fonts/"
