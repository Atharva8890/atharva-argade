"""Animated, word-by-word motivational captions with keyword glow."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from . import config
from .script import Beat, HIGHLIGHT_WORDS
from .narration import BeatTiming, WordTiming


@dataclass
class _Placed:
    word: WordTiming
    cx: int          # tile centre on the frame
    cy: int
    highlight: bool


REVEAL = 0.18        # seconds for a word to pop in


def _font(path: str, size: int, weight: int | None) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(path, size)
    if weight is not None:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    return f


class CaptionRenderer:
    def __init__(self, cfg: config.RenderConfig):
        self.cfg = cfg
        self.W, self.H = cfg.width, cfg.height
        self.size = max(20, int(cfg.caption_size_frac * self.H))
        self.font = _font(cfg.caption_font, self.size, cfg.caption_font_weight)
        self.hi_font = _font(cfg.caption_font, int(self.size * 1.04),
                             cfg.caption_font_weight)
        self.hero_font = ImageFont.truetype(cfg.hero_font, int(self.H * 0.118))
        self.accent = np.array(cfg.accent_rgb, np.float32) / 255.0
        self._layout_cache: dict[int, list[_Placed]] = {}
        self._tile_cache: dict[tuple, tuple[np.ndarray, int, int]] = {}

    # -- layout -----------------------------------------------------------
    def _measure(self, font, text):
        b = font.getbbox(text)
        return b[2] - b[0], b[3] - b[1]

    def _layout(self, beat: Beat, timing: BeatTiming) -> list[_Placed]:
        if timing.index in self._layout_cache:
            return self._layout_cache[timing.index]
        words = timing.words
        placed: list[_Placed] = []
        if not words:
            self._layout_cache[timing.index] = placed
            return placed

        final = beat.is_final
        font = self.hero_font if final else self.font
        max_w = self.W * (0.80 if final else 0.86)
        space = int(self.size * 0.34)

        # group words into lines that fit
        lines: list[list[WordTiming]] = [[]]
        widths: list[int] = [0]
        for w in words:
            disp = w.word.upper() if final else w.word
            ww, _ = self._measure(font, disp)
            add = ww + (space if lines[-1] else 0)
            if widths[-1] + add > max_w and lines[-1]:
                lines.append([w]); widths.append(ww)
            else:
                lines[-1].append(w); widths[-1] += add
        line_h = int(self.size * (1.55 if final else 1.28))
        total_h = line_h * len(lines)
        if final:
            y0 = self.H // 2 - total_h // 2 + line_h // 2
        else:
            y0 = int(self.H * 0.82) - total_h + line_h // 2

        for li, line in enumerate(lines):
            lw = widths[li]
            x = self.W // 2 - lw // 2
            cy = y0 + li * line_h
            for j, w in enumerate(line):
                disp = w.word.upper() if final else w.word
                ww, _ = self._measure(font, disp)
                hl = final or (w.clean in HIGHLIGHT_WORDS)
                placed.append(_Placed(w, x + ww // 2, cy, hl))
                x += ww + space
        self._layout_cache[timing.index] = placed
        return placed

    # -- tiles ------------------------------------------------------------
    def _tile(self, text, highlight, final):
        key = (text, highlight, final)
        if key in self._tile_cache:
            return self._tile_cache[key]
        font = self.hero_font if final else (self.hi_font if highlight else self.font)
        b = font.getbbox(text)
        tw, th = b[2] - b[0], b[3] - b[1]
        pad = int(self.size * (0.9 if highlight else 0.6)) + 8
        W = tw + pad * 2
        H = th + pad * 2
        ox, oy = pad - b[0], pad - b[1]

        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        gcol = tuple(self.cfg.accent_rgb) if highlight else (0, 0, 0)
        ga = 255 if highlight else 220
        gd.text((ox, oy), text, font=font, fill=gcol + (ga,))
        radius = self.size * (0.30 if highlight else 0.16)
        glow = glow.filter(ImageFilter.GaussianBlur(radius))
        if highlight:  # punchier glow
            arr = np.asarray(glow, np.float32)
            arr[..., 3] = np.clip(arr[..., 3] * 1.7, 0, 255)
            glow = Image.fromarray(arr.astype(np.uint8))

        crisp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        cd = ImageDraw.Draw(crisp)
        # legibility shadow
        cd.text((ox + 3, oy + 4), text, font=font, fill=(0, 0, 0, 170))
        fill = tuple(self.cfg.accent_rgb) if highlight else (255, 255, 255)
        cd.text((ox, oy), text, font=font, fill=fill + (255,))

        out = Image.alpha_composite(glow, crisp)
        arr = np.asarray(out, np.float32) / 255.0
        self._tile_cache[key] = (arr, W, H)
        return arr, W, H

    # -- compositing ------------------------------------------------------
    @staticmethod
    def _blend(frame, tile_rgb, alpha, x0, y0):
        H, W = frame.shape[:2]
        th, tw = tile_rgb.shape[:2]
        fx0, fy0 = max(0, x0), max(0, y0)
        fx1, fy1 = min(W, x0 + tw), min(H, y0 + th)
        if fx1 <= fx0 or fy1 <= fy0:
            return
        tx0, ty0 = fx0 - x0, fy0 - y0
        a = alpha[ty0:ty0 + (fy1 - fy0), tx0:tx0 + (fx1 - fx0)]
        c = tile_rgb[ty0:ty0 + (fy1 - fy0), tx0:tx0 + (fx1 - fx0)]
        region = frame[fy0:fy1, fx0:fx1]
        frame[fy0:fy1, fx0:fx1] = region * (1 - a) + c * a

    def render(self, frame, beat: Beat, timing: BeatTiming, t: float):
        if not self.cfg.captions:
            return frame
        placed = self._layout(beat, timing)
        if not placed:
            return frame
        final = beat.is_final
        for p in placed:
            w = p.word
            if t < w.start:
                continue
            local = min(1.0, (t - w.start) / REVEAL)
            ease = 1 - (1 - local) ** 3
            disp = w.word.upper() if final else w.word
            tile, tw, th = self._tile(disp, p.highlight, final)
            scale = 1.0 + (0.22 if p.highlight else 0.14) * (1 - ease)
            active = w.start <= t < w.end + 0.12
            if active:
                scale *= 1.06
            if abs(scale - 1.0) > 0.01:
                nw, nh = max(1, int(tw * scale)), max(1, int(th * scale))
                im = Image.fromarray((np.clip(tile, 0, 1) * 255).astype(np.uint8))
                im = im.resize((nw, nh), Image.LANCZOS)
                t2 = np.asarray(im, np.float32) / 255.0
            else:
                t2 = tile; nw, nh = tw, th
            rise = int((1 - ease) * self.size * 0.18)
            x0 = p.cx - nw // 2
            y0 = p.cy - nh // 2 + rise
            rgb = t2[..., :3]
            alpha = (t2[..., 3:4]) * ease
            if active:
                alpha = np.clip(alpha * 1.08, 0, 1)
            self._blend(frame, rgb, alpha, x0, y0)
        return frame
