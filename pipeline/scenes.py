"""Scene art generation.

Every beat resolves to a *plate pair*: a background ``bg`` (RGB) and an optional
foreground ``fg`` (RGBA).  The compositor moves the two plates at slightly
different rates to create real parallax / depth.

If a photo is dropped into ``assets/images/<key>.(jpg|png)`` it is used as the
background automatically (``key`` is e.g. ``04_closed`` -- see the generated
``storyboard/storyboard.md``).  Otherwise a cinematic, era-styled plate is
synthesized procedurally so the pipeline always renders end to end.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from . import config
from .script import Beat


@dataclass
class SceneArt:
    bg: np.ndarray            # float32 HxWx3 in 0..1
    fg: np.ndarray | None     # float32 HxWx4 (RGBA) in 0..1 or None
    photo: bool = False       # True if sourced from a real dropped-in image


# --- 1950s cinematic palettes (RGB 0..1) ---------------------------------
def _c(r, g, b):
    return np.array([r, g, b], dtype=np.float32) / 255.0


PALETTES = {
    "warm":   (_c(60, 38, 24), _c(196, 122, 54), _c(255, 196, 120)),   # sky_top, sky_bot, sun
    "gold":   (_c(74, 44, 20), _c(240, 168, 70), _c(255, 224, 150)),
    "cold":   (_c(38, 46, 56), _c(120, 132, 140), _c(180, 190, 196)),
    "dusk":   (_c(28, 28, 48), _c(150, 86, 96), _c(255, 170, 130)),
    "dark":   (_c(10, 10, 14), _c(34, 28, 26), _c(150, 96, 50)),
}

MOOD = {
    "title": "dark", "portrait": "warm", "crowd": "cold", "closed": "cold",
    "money": "dark", "horizon": "cold", "recipe": "warm", "car": "dusk",
    "road": "gold", "door_closed": "cold", "doors_many": "cold",
    "sunrise": "gold", "time": "dusk", "handshake": "warm", "growth": "warm",
    "map": "dusk", "success": "gold", "lesson": "dark", "final": "gold",
}


def _dims(cfg: config.RenderConfig) -> tuple[int, int]:
    w = int(round(cfg.width * cfg.oversample))
    h = int(round(cfg.height * cfg.oversample))
    return w, h


def _gradient(w: int, h: int, top: np.ndarray, bot: np.ndarray) -> np.ndarray:
    t = np.linspace(0.0, 1.0, h, dtype=np.float32)[:, None, None]
    return (top[None, None] * (1 - t) + bot[None, None] * t) * np.ones((h, w, 1), np.float32)


def _radial_glow(w: int, h: int, cx: float, cy: float, radius: float,
                 color: np.ndarray, strength: float = 1.0) -> np.ndarray:
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt((xx - cx * w) ** 2 + (yy - cy * h) ** 2)
    g = np.clip(1.0 - d / (radius * w), 0.0, 1.0) ** 2
    return (g[..., None] * color[None, None]) * strength


def _grain(img: np.ndarray, rng: np.random.Generator, amt: float = 0.015) -> np.ndarray:
    n = rng.normal(0.0, amt, img.shape[:2]).astype(np.float32)[..., None]
    return np.clip(img + n, 0.0, 1.0)


def _silhouette(w: int, h: int, draw_fn, blur: float = 2.0,
                color=(8, 7, 10), alpha: float = 1.0) -> np.ndarray:
    """Draw a shape with PIL and return an RGBA float plate."""
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    draw_fn(d, w, h)
    if blur > 0:
        mask = mask.filter(ImageFilter.GaussianBlur(blur))
    a = (np.asarray(mask, np.float32) / 255.0) * alpha
    rgba = np.zeros((h, w, 4), np.float32)
    col = np.array(color, np.float32) / 255.0
    rgba[..., 0:3] = col[None, None]
    rgba[..., 3] = a
    return rgba


# --- procedural archetype builders ---------------------------------------
def _bg_sky(w, h, mood, rng, sun=(0.5, 0.28)):
    top, bot, suncol = PALETTES[mood]
    bg = _gradient(w, h, top, bot)
    if mood in ("warm", "gold", "dusk", "dark"):
        bg = bg + _radial_glow(w, h, sun[0], sun[1], 0.55, suncol, 0.9)
    bg = np.clip(bg, 0, 1)
    return _grain(bg, rng)


def _ground(d: ImageDraw.ImageDraw, w, h, y=0.72):
    d.rectangle([0, int(h * y), w, h], fill=255)


def build_procedural(beat: Beat, cfg: config.RenderConfig,
                     rng: np.random.Generator) -> SceneArt:
    w, h = _dims(cfg)
    s = beat.scene
    mood = MOOD.get(s, "warm")
    sun = (0.5, 0.26)
    bg = _bg_sky(w, h, mood, rng, sun)
    fg = None

    def portrait(d, w, h):
        # head + shoulders bust, slightly off-center
        cx = int(w * 0.5)
        d.ellipse([cx - int(w * 0.085), int(h * 0.20), cx + int(w * 0.085),
                   int(h * 0.42)], fill=255)
        d.polygon([(cx - int(w * 0.20), h), (cx - int(w * 0.13), int(h * 0.42)),
                   (cx + int(w * 0.13), int(h * 0.42)), (cx + int(w * 0.20), h)],
                  fill=255)

    def building(d, w, h):
        _ground(d, w, h, 0.78)
        bx0, bx1 = int(w * 0.22), int(w * 0.78)
        by0, by1 = int(h * 0.40), int(h * 0.78)
        d.rectangle([bx0, by0, bx1, by1], fill=255)
        d.polygon([(bx0 - int(w*0.03), by0), (bx1 + int(w*0.03), by0),
                   (int(w*0.5), int(h*0.30))], fill=255)

    def road(d, w, h):
        horizon = int(h * 0.55)
        d.polygon([(0, h), (int(w * 0.5 - w*0.02), horizon),
                   (int(w * 0.5 + w*0.02), horizon), (w, h)], fill=255)

    def car(d, w, h):
        _ground(d, w, h, 0.80)
        cx, cy = int(w * 0.5), int(h * 0.62)
        bw, bh = int(w * 0.26), int(h * 0.12)
        d.rounded_rectangle([cx - bw, cy, cx + bw, cy + bh], radius=int(h*0.03), fill=255)
        d.rounded_rectangle([cx - int(bw*0.55), cy - int(bh*0.9),
                             cx + int(bw*0.55), cy], radius=int(h*0.02), fill=255)
        for sx in (-0.6, 0.6):
            d.ellipse([cx + int(bw*sx) - int(w*0.03), cy + bh - int(h*0.01),
                       cx + int(bw*sx) + int(w*0.03), cy + bh + int(h*0.05)], fill=255)

    def door(d, w, h):
        dx0, dx1 = int(w * 0.40), int(w * 0.60)
        d.rectangle([dx0, int(h * 0.30), dx1, int(h * 0.92)], fill=255)

    def doors(d, w, h):
        for i in range(5):
            x = int(w * (0.10 + i * 0.18))
            sc = 1.0 - i * 0.12
            dw = int(w * 0.07 * sc)
            top = int(h * (0.40 - 0.03 * (4 - i)))
            d.rectangle([x, top, x + dw, int(h * 0.85)], fill=255)

    def skyline(d, w, h):
        _ground(d, w, h, 0.82)
        x = int(w * 0.06)
        while x < w * 0.94:
            bw = int(w * rng.uniform(0.04, 0.09))
            bh = int(h * rng.uniform(0.10, 0.34))
            d.rectangle([x, int(h * 0.82) - bh, x + bw, int(h * 0.82)], fill=255)
            x += bw + int(w * 0.012)

    def clock(d, w, h):
        cx, cy, r = int(w*0.5), int(h*0.42), int(h*0.16)
        d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=255, width=int(h*0.012))
        d.line([cx, cy, cx, cy-int(r*0.8)], fill=255, width=int(h*0.012))
        d.line([cx, cy, cx+int(r*0.6), cy], fill=255, width=int(h*0.012))

    def figure(d, w, h):
        _ground(d, w, h, 0.84)
        cx = int(w * 0.5)
        d.ellipse([cx-int(w*0.03), int(h*0.40), cx+int(w*0.03), int(h*0.50)], fill=255)
        d.rectangle([cx-int(w*0.035), int(h*0.50), cx+int(w*0.035), int(h*0.84)], fill=255)

    builders = {
        "title": portrait, "portrait": portrait, "closed": building,
        "diner": building, "growth": building, "road": road, "horizon": road,
        "car": car, "door_closed": door, "doors_many": doors,
        "map": skyline, "success": figure, "handshake": figure,
        "crowd": figure, "time": clock, "sunrise": figure, "final": figure,
    }
    fn = builders.get(s)
    if fn is not None:
        col = (6, 6, 9) if mood != "gold" else (14, 9, 6)
        fg = _silhouette(w, h, fn, blur=max(2.0, w * 0.0016), color=col)
    elif s in ("money", "recipe", "lesson"):
        # atmospheric only -> rely on light + particles + captions
        fg = None
    return SceneArt(bg=bg, fg=fg, photo=False)


def _load_photo(path: Path, w: int, h: int) -> np.ndarray:
    img = Image.open(path).convert("RGB")
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    img = img.resize((int(iw * scale) + 1, int(ih * scale) + 1), Image.LANCZOS)
    nw, nh = img.size
    left = (nw - w) // 2
    top = (nh - h) // 2
    img = img.crop((left, top, left + w, top + h))
    return np.asarray(img, np.float32) / 255.0


def _photo_path(beat: Beat) -> Path | None:
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        p = config.IMAGES / f"{beat.key}{ext}"
        if p.exists():
            return p
    return None


def build(beat: Beat, cfg: config.RenderConfig,
          rng: np.random.Generator) -> SceneArt:
    w, h = _dims(cfg)
    p = _photo_path(beat)
    if p is not None:
        bg = _load_photo(p, w, h)
        # build a soft center-weighted foreground copy for subject "pop"/parallax
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        cx, cy = w * 0.5, h * 0.46
        d = np.sqrt(((xx - cx) / (w * 0.42)) ** 2 + ((yy - cy) / (h * 0.46)) ** 2)
        alpha = np.clip(1.0 - d, 0.0, 1.0) ** 1.5
        fg = np.dstack([bg, alpha]).astype(np.float32)
        return SceneArt(bg=bg, fg=fg, photo=True)
    return build_procedural(beat, cfg, rng)
