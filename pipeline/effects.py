"""Cinematic camera motion, transitions and the global colour/light look."""
from __future__ import annotations

import numpy as np
import cv2

from . import config
from .script import Beat


# ---------------------------------------------------------------------------
# Camera motion
# ---------------------------------------------------------------------------
def _smooth_noise(n: int, rng: np.random.Generator, sigma: float) -> np.ndarray:
    """A smooth random walk normalised to roughly [-1, 1]."""
    if n <= 1:
        return np.zeros(max(n, 1), np.float32)
    raw = rng.normal(0.0, 1.0, n + 80).astype(np.float32)
    k = max(3, int(sigma))
    ker = cv2.getGaussianKernel(k * 2 + 1, k).flatten().astype(np.float32)
    sm = np.convolve(raw, ker, mode="same")[40:40 + n]
    m = np.max(np.abs(sm)) or 1.0
    return sm / m


def _ease(t: np.ndarray | float):
    # smootherstep for buttery acceleration / deceleration
    return t * t * t * (t * (t * 6 - 15) + 10)


class CameraPath:
    """Per-beat camera motion producing affine matrices for bg and fg plates."""

    def __init__(self, beat: Beat, cfg: config.RenderConfig, n_frames: int,
                 plate_wh: tuple[int, int], rng: np.random.Generator):
        self.cfg = cfg
        self.beat = beat
        self.n = max(1, n_frames)
        self.W, self.H = cfg.width, cfg.height
        self.Wp, self.Hp = plate_wh
        i = np.linspace(0.0, 1.0, self.n, dtype=np.float32)
        e = _ease(i)

        cxp, cyp = self.Wp / 2.0, self.Hp / 2.0
        max_off_x = (self.Wp - self.W) * 0.5
        max_off_y = (self.Hp - self.H) * 0.5
        eff = beat.effect

        z = np.full(self.n, 1.04, np.float32)
        cx = np.full(self.n, cxp, np.float32)
        cy = np.full(self.n, cyp, np.float32)
        th = np.zeros(self.n, np.float32)

        if eff == "pushin":
            z = 1.0 + 0.13 * e
        elif eff == "pullout":
            z = 1.15 - 0.13 * e
        elif eff == "zoom3d":
            z = 1.02 + 0.15 * e
            cx = cxp + max_off_x * 0.35 * (e - 0.5) * 2
        elif eff in ("parallax_l", "track_left"):
            mag = 0.55 if eff == "parallax_l" else 0.85
            z[:] = 1.06
            cx = cxp + max_off_x * mag * (1 - 2 * e)
        elif eff in ("parallax_r", "track_right"):
            mag = 0.55 if eff == "parallax_r" else 0.85
            z[:] = 1.06
            cx = cxp + max_off_x * mag * (2 * e - 1)
        elif eff == "rise":
            z = 1.05 + 0.09 * e
            cy = cyp + max_off_y * 0.6 * (1 - 2 * e)
        else:  # default gentle push
            z = 1.0 + 0.10 * e

        # Camera shake -> grows with emotional intensity (the "emotional moment").
        amp = (0.004 + 0.020 * beat.intensity) * self.H
        sx = _smooth_noise(self.n, rng, sigma=2.2) * amp
        sy = _smooth_noise(self.n, rng, sigma=2.2) * amp
        sth = _smooth_noise(self.n, rng, sigma=2.6) * (0.25 * beat.intensity)
        cx = cx + sx
        cy = cy + sy
        th = th + sth

        half_w = (self.W / 2.0) / z
        half_h = (self.H / 2.0) / z
        cx = np.clip(cx, half_w + 1, self.Wp - half_w - 1)
        cy = np.clip(cy, half_h + 1, self.Hp - half_h - 1)

        self.z, self.cx, self.cy, self.th = z, cx, cy, th
        # foreground parallax/zoom amplification for depth
        self.par_shift = 1.16
        self.par_zoom = 1.035

    @staticmethod
    def _matrix(cx, cy, z, theta, W, H):
        cos = z * np.cos(theta)
        sin = z * np.sin(theta)
        a, b = cos, -sin
        d, e = sin, cos
        c = W / 2.0 - (a * cx + b * cy)
        f = H / 2.0 - (d * cx + e * cy)
        return np.array([[a, b, c], [d, e, f]], np.float32)

    def at(self, idx: int):
        idx = min(idx, self.n - 1)
        z, cx, cy, th = self.z[idx], self.cx[idx], self.cy[idx], self.th[idx]
        m_bg = self._matrix(cx, cy, z, th, self.W, self.H)
        ox = (cx - self.Wp / 2.0) * self.par_shift
        oy = (cy - self.Hp / 2.0) * self.par_shift
        m_fg = self._matrix(self.Wp / 2.0 + ox, self.Hp / 2.0 + oy,
                            z * self.par_zoom, th, self.W, self.H)
        return m_bg, m_fg


def warp(plate: np.ndarray, M: np.ndarray, W: int, H: int) -> np.ndarray:
    return cv2.warpAffine(plate, M, (W, H), flags=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_REFLECT101)


# ---------------------------------------------------------------------------
# Global look
# ---------------------------------------------------------------------------
class LookEngine:
    def __init__(self, cfg: config.RenderConfig):
        self.cfg = cfg
        W, H = cfg.width, cfg.height
        self.W, self.H = W, H

        # vignette
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        cx, cy = W / 2.0, H / 2.0
        d = np.sqrt(((xx - cx) / (W * 0.72)) ** 2 + ((yy - cy) / (H * 0.72)) ** 2)
        vig = 1.0 - np.clip(d - 0.35, 0, 1) ** 2 * (0.55 * cfg.vignette_strength)
        self.vignette = vig[..., None].astype(np.float32)

        # soft dust particles
        n = 110
        rng = np.random.default_rng(cfg.seed + 7)
        self.n_dust = n
        self.p_x = rng.uniform(0, W, n).astype(np.float32)
        self.p_y = rng.uniform(0, H, n).astype(np.float32)
        self.p_vx = rng.uniform(-7, 7, n).astype(np.float32)
        self.p_vy = rng.uniform(-13, -3, n).astype(np.float32)
        self.p_sz = rng.uniform(0.6, 1.5, n).astype(np.float32)
        self.p_br = rng.uniform(0.04, 0.16, n).astype(np.float32)
        self.p_ph = rng.uniform(0, 6.2832, n).astype(np.float32)
        # soft round dust sprite (gaussian falloff)
        rad = max(4, int(W * 0.006))
        ax = np.arange(-rad, rad + 1, dtype=np.float32)
        gx, gy = np.meshgrid(ax, ax)
        self.dust = np.exp(-(gx ** 2 + gy ** 2) / (2 * (rad * 0.42) ** 2)).astype(np.float32)
        self.dust_rad = rad
        self.dust_tint = np.array([1.0, 0.94, 0.82], np.float32)

        # lens-flare sprite anchored near a top light source
        self.flare = self._make_flare(W, H)

        self.teal = np.array([0.06, 0.13, 0.16], np.float32)
        self.warm = np.array([0.16, 0.09, 0.02], np.float32)

    def _make_flare(self, W, H):
        spr = np.zeros((H, W, 3), np.float32)
        src = np.array([W * 0.74, H * 0.22])
        cen = np.array([W * 0.5, H * 0.5])
        # streak
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        dline = np.abs((yy - src[1]) - 0.0) / (H * 0.5)
        streak = np.clip(1 - np.abs(yy - src[1]) / (H * 0.012), 0, 1)
        streak *= np.clip(1 - np.abs(xx - src[0]) / (W * 0.6), 0, 1) ** 2
        spr += streak[..., None] * np.array([0.5, 0.42, 0.25], np.float32)
        # orbs along the axis
        for k, rad, br, col in [
            (0.0, 0.10, 0.9, (0.7, 0.6, 0.35)),
            (0.4, 0.04, 0.5, (0.4, 0.55, 0.5)),
            (0.8, 0.06, 0.4, (0.55, 0.4, 0.5)),
            (1.25, 0.05, 0.45, (0.4, 0.45, 0.6)),
        ]:
            pos = src + (cen - src) * k
            dd = np.sqrt((xx - pos[0]) ** 2 + (yy - pos[1]) ** 2)
            orb = np.clip(1 - dd / (rad * W), 0, 1) ** 2 * br
            spr += orb[..., None] * np.array(col, np.float32)
        return spr

    # --- individual ops ---
    def grade(self, f):
        s = self.cfg.grade_strength
        if s <= 0:
            return f
        luma = (f * np.array([0.299, 0.587, 0.114], np.float32)).sum(2, keepdims=True)
        contrast = 1.0 + 0.18 * s
        g = (f - 0.5) * contrast + 0.5
        g = g + self.teal[None, None] * (1 - luma) * 0.5 * s
        g = g + self.warm[None, None] * luma * 0.6 * s
        sat = 1.0 + 0.22 * s
        g = luma + (g - luma) * sat
        return np.clip(g, 0, 1)

    def bloom(self, f):
        if not self.cfg.bloom:
            return f
        luma = f.max(2, keepdims=True)
        mask = np.clip(luma - 0.72, 0, 1) * f
        small = cv2.resize(mask, (self.W // 4, self.H // 4))
        small = cv2.GaussianBlur(small, (0, 0), 6)
        big = cv2.resize(small, (self.W, self.H))
        return np.clip(f + big * 1.1, 0, 1)

    def particles(self, f, t):
        if not self.cfg.particles:
            return f
        x = (self.p_x + self.p_vx * t) % self.W
        y = (self.p_y + self.p_vy * t) % self.H
        tw = 0.55 + 0.45 * np.sin(self.p_ph + t * 1.7)
        r = self.dust_rad
        spr = self.dust
        tint = self.dust_tint
        H, W = self.H, self.W
        for k in range(self.n_dust):
            cx, cy = int(x[k]), int(y[k])
            x0, x1 = max(0, cx - r), min(W, cx + r + 1)
            y0, y1 = max(0, cy - r), min(H, cy + r + 1)
            if x1 <= x0 or y1 <= y0:
                continue
            sx0, sy0 = x0 - (cx - r), y0 - (cy - r)
            s = spr[sy0:sy0 + (y1 - y0), sx0:sx0 + (x1 - x0), None]
            b = self.p_br[k] * tw[k] * self.p_sz[k]
            f[y0:y1, x0:x1] = np.clip(f[y0:y1, x0:x1] + s * b * tint[None, None], 0, 1)
        return f

    def lens_flare(self, f, t, intensity):
        if not self.cfg.lens_flare:
            return f
        flick = 0.6 + 0.25 * np.sin(t * 2.3) + 0.15 * np.sin(t * 5.1)
        amt = (0.10 + 0.18 * intensity) * flick
        return np.clip(f + self.flare * amt, 0, 1)

    def grain(self, f, rng):
        a = 0.009 * self.cfg.grain_strength
        if a <= 0:
            return f
        # Generate grain at half resolution and upscale: more filmic clusters
        # and far friendlier to the video codec (avoids bitrate blow-up).
        hw, hh = self.W // 2, self.H // 2
        n = rng.normal(0, a, (hh, hw, 1)).astype(np.float32)
        n = cv2.resize(n, (self.W, self.H), interpolation=cv2.INTER_LINEAR)[..., None]
        return np.clip(f + n, 0, 1)

    def finalize(self, f, t, intensity, rng, flash=0.0):
        f = self.grade(f)
        f = self.lens_flare(f, t, intensity)
        f = self.bloom(f)
        f = self.particles(f, t)
        f = f * self.vignette
        if flash > 0:
            f = np.clip(f + flash, 0, 1)
        f = self.grain(f, rng)
        return np.clip(f, 0, 1)


# ---------------------------------------------------------------------------
# Transitions (operate on already-composited RGB frames)
# ---------------------------------------------------------------------------
def crossfade(a, b, t):
    return a * (1 - t) + b * t


def directional_blur(img, angle_deg, strength):
    if strength <= 0:
        return img
    ksize = int(max(3, strength)) | 1
    ker = np.zeros((ksize, ksize), np.float32)
    ker[ksize // 2, :] = 1.0
    M = cv2.getRotationMatrix2D((ksize / 2, ksize / 2), angle_deg, 1.0)
    ker = cv2.warpAffine(ker, M, (ksize, ksize))
    s = ker.sum()
    if s > 0:
        ker /= s
    return cv2.filter2D(img, -1, ker)
