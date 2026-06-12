.PHONY: help setup voice fonts storyboard draft render clean distclean

PY ?= python3

help:
	@echo "make setup       - install python deps + download voice & fonts"
	@echo "make draft       - fast 540p preview  -> output/draft.mp4"
	@echo "make render      - full 1080p render   -> output/colonel_sanders_documentary.mp4"
	@echo "make storyboard  - write storyboard/storyboard.md (image prompts)"
	@echo "make clean       - remove render cache"
	@echo "make distclean   - remove cache, outputs, models"

setup:
	$(PY) -m pip install -r requirements.txt
	bash scripts/fetch_voice.sh
	bash scripts/fetch_fonts.sh

voice:
	bash scripts/fetch_voice.sh

fonts:
	bash scripts/fetch_fonts.sh

storyboard:
	$(PY) render.py --storyboard-only

draft:
	$(PY) render.py --draft

render:
	$(PY) render.py

clean:
	rm -rf output/cache

distclean: clean
	rm -f output/*.mp4
	rm -f models/*.onnx models/*.onnx.json
