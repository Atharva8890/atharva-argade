"""Render configuration and quality presets."""
from __future__ import annotations

import os
from dataclasses import dataclass, field, asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
IMAGES = ASSETS / "images"
MUSIC = ASSETS / "music"
FONTS = ASSETS / "fonts"
MODELS = ROOT / "models"
OUTPUT = ROOT / "output"
CACHE = OUTPUT / "cache"


@dataclass
class RenderConfig:
    """All knobs for a render in one place."""

    # Canvas / encoding ---------------------------------------------------
    width: int = 1920
    height: int = 1080
    fps: int = 30
    crf: int = 20                 # x264 quality (lower = better)
    preset: str = "medium"        # x264 speed/quality tradeoff
    audio_bitrate: str = "256k"

    # Narration -----------------------------------------------------------
    voice_model: str = str(MODELS / "en_US-ryan-high.onnx")
    voice_length_scale: float = 1.33   # >1 = slower, more gravitas
    voice_noise_scale: float = 0.60
    voice_noise_w: float = 0.80
    # Deepening / warmth applied with ffmpeg (duration preserving).
    voice_pitch: float = 0.93          # <1 = deeper voice
    voice_reverb: bool = True

    # Pauses (tuned so the full piece runs ~5 minutes) --------------------
    pause_scale: float = 3.25          # multiplies every scripted dramatic pause
    lead_in: float = 3.5               # silence before first word (music intro)
    tail_out: float = 5.0              # hold on final screen after last word

    # Music ---------------------------------------------------------------
    music_gain_db: float = -16.0       # bed level under narration
    music_file: str = ""               # optional real track (overrides synth)

    # Look ----------------------------------------------------------------
    grade_strength: float = 1.0        # cinematic color grade intensity
    grain_strength: float = 1.0        # film grain
    vignette_strength: float = 1.0
    particles: bool = True
    lens_flare: bool = True
    bloom: bool = True

    # Captions ------------------------------------------------------------
    captions: bool = True
    caption_font: str = str(FONTS / "Montserrat.ttf")
    caption_font_weight: int = 800
    hero_font: str = str(FONTS / "Anton-Regular.ttf")
    caption_size_frac: float = 0.060   # caption height as fraction of frame height
    accent_rgb: tuple = (255, 196, 64)  # gold highlight for keywords

    # Pipeline ------------------------------------------------------------
    oversample: float = 1.22           # render plates larger so camera has room
    seed: int = 1950
    threads: int = 0                   # 0 = auto (cpu count)
    out_file: str = str(OUTPUT / "colonel_sanders_documentary.mp4")
    keep_frames: bool = False
    limit_beats: int = 0               # >0 renders only the first N beats (debug)

    def as_dict(self) -> dict:
        return asdict(self)


def draft(cfg: RenderConfig | None = None) -> RenderConfig:
    """A fast, low-resolution preset for iterating."""
    cfg = cfg or RenderConfig()
    cfg.width, cfg.height = 960, 540
    cfg.fps = 24
    cfg.crf = 23
    cfg.preset = "veryfast"
    cfg.out_file = str(OUTPUT / "draft.mp4")
    return cfg


def ensure_dirs() -> None:
    for d in (ASSETS, IMAGES, MUSIC, FONTS, MODELS, OUTPUT, CACHE):
        d.mkdir(parents=True, exist_ok=True)


def cpu_threads(cfg: RenderConfig) -> int:
    if cfg.threads > 0:
        return cfg.threads
    return max(1, (os.cpu_count() or 2))
