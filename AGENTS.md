# AGENTS.md

## Cursor Cloud specific instructions

This branch (`cursor/colonel-sanders-documentary-cf9e`) is a **self-contained Python
render pipeline** that generates a ~7.5 minute cinematic documentary to
`output/colonel_sanders_documentary.mp4`. There is no long-running service; the
"app" is a one-shot render (`python3 render.py`). See `README.md` for the full
feature list and CLI flags.

### Environment / dependencies
- Python deps come from `requirements.txt` and are installed by the startup
  update script into the **system** interpreter via
  `pip install --break-system-packages`, so run everything with plain `python3`
  (no virtualenv activation needed).
- The Piper neural voice model (`models/en_US-ryan-high.onnx`, ~120 MB) and the
  caption fonts (`assets/fonts/*.ttf`) are downloaded by
  `scripts/fetch_voice.sh` / `scripts/fetch_fonts.sh`. These are gitignored and
  re-downloaded by the update script if missing. A render **fails without them**.
- `ffmpeg`/`ffprobe` are required and already present on the VM image.

### Running / iterating
- Fast preview (540p/24fps, the whole film): `python3 render.py --draft` →
  `output/draft.mp4`. On this 4-core VM this takes ~15 min.
- Full 1080p/30fps render: `python3 render.py` →
  `output/colonel_sanders_documentary.mp4`. This is CPU-bound and slow
  (~1.5–2 rendered fps, roughly 60–90 min for the full ~13.4k frames). Always
  run it in the background (e.g. `nohup python3 render.py > output/full_render.log 2>&1 &`)
  and poll the log; do not block a single foreground call on it.
- Narration TTS + the procedural score are cached under `output/cache/`
  (keyed by a hash of the script + voice settings), so re-renders that don't
  change the narration **skip TTS** and start compositing almost immediately.
- Render progress is printed as a `NN%  frame X/Y  clip A/B  elapsed ...  eta ...`
  line; note that piping render output through `tail`/`head` buffers it until the
  process exits, so tail the log file instead for live progress.

### Footage / photoreal mode (optional)
- The default render uses **procedurally synthesized cinematic plates** and works
  with no external assets. Dropping real media into `assets/images/`,
  `assets/clips/`, or running `python3 scripts/fetch_footage.py` (network +
  optional `PEXELS_API_KEY`) upgrades beats to real B-roll. Footage files are
  gitignored/regenerable.

### Delivering the rendered video
- Rendered `.mp4` files are gitignored and the VM is ephemeral, so they do not
  persist across sessions and cannot be committed. To hand a video to the user,
  copy it into `/opt/cursor/artifacts/`, which surfaces it as a download in the
  Cursor web UI.
