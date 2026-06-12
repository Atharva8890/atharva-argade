"""Frame compositor + ffmpeg encode orchestrator.

The timeline is a flat list of *clips*. Each narration line (beat) is split
into several quick sub-clips so the edit cuts constantly -- a fast, montage
style (à la MotivationHub) -- while the word-by-word captions keep flowing
across the cuts. Clip art is built lazily with a small rolling cache so the
montage can contain many clips without exhausting memory.
"""
from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path

import cv2
import numpy as np

from . import config, narration, scenes, music
from .effects import CameraPath, LookEngine, warp, crossfade, directional_blur
from .captions import CaptionRenderer
from .script import Beat, storyboard

TRANS_DUR = {
    "fade": 0.40, "dissolve": 0.38, "light_flash": 0.30,
    "speed_ramp": 0.24, "whip_l": 0.22, "whip_r": 0.22,
}

# Camera moves and cut styles rotated through within a montage line.
EFFECT_ROT = ["pushin", "parallax_r", "zoom3d", "parallax_l",
              "pullout", "track_left", "rise", "track_right"]
MONTAGE_TRANS = ["whip_l", "speed_ramp", "whip_r", "light_flash", "dissolve"]


@dataclass
class ClipSpec:
    beat: Beat
    start: float
    end: float
    variant: int
    effect: str
    trans: str
    seed: int
    video_path: Path | None = None
    seg_start: float = 0.0


class BuiltClip:
    """Concrete, renderable clip (lazily constructed from a ClipSpec)."""

    def __init__(self, spec: ClipSpec, cfg: config.RenderConfig):
        self.spec = spec
        self.cfg = cfg
        rng = np.random.default_rng(spec.seed)
        dur = spec.end - spec.start
        self.n = max(1, int(round((dur + 0.5) * cfg.fps)))
        self.video = None
        if spec.video_path is not None:
            self.video = scenes.VideoSource(spec.video_path, cfg, spec.seg_start)
            plate_wh = (self.video.w, self.video.h)
            self.art = None
            self.dof = 0.0
            cam_int = spec.beat.intensity * 0.45  # footage already moves
        else:
            self.art = scenes.build(spec.beat, cfg, rng, spec.variant)
            plate_wh = (self.art.bg.shape[1], self.art.bg.shape[0])
            self.dof = 2.2 if self.art.fg is not None else 0.0
            cam_int = spec.beat.intensity
        self.cam = CameraPath(spec.beat, cfg, self.n, plate_wh, rng,
                              effect=spec.effect, intensity=cam_int)

    def render(self, local_t: float) -> np.ndarray:
        idx = max(0, min(self.n - 1, int(round(local_t * self.cfg.fps))))
        m_bg, m_fg = self.cam.at(idx)
        W, H = self.cfg.width, self.cfg.height
        if self.video is not None:
            plate = self.video.frame(local_t)
            return np.clip(warp(plate, m_bg, W, H), 0, 1)
        bg = warp(self.art.bg, m_bg, W, H)
        if self.art.fg is not None:
            fg = cv2.warpAffine(self.art.fg, m_fg, (W, H), flags=cv2.INTER_LINEAR,
                                borderMode=cv2.BORDER_CONSTANT, borderValue=0)
            if self.dof > 0:
                bg = cv2.GaussianBlur(bg, (0, 0), self.dof)
            a = np.clip(fg[..., 3:4], 0, 1)
            bg = bg * (1 - a) + fg[..., :3] * a
        return np.clip(bg, 0, 1)

    def close(self):
        if self.video is not None:
            self.video.close()


class ClipPool:
    """Builds clips on demand, keeping only a few in memory at a time."""

    def __init__(self, specs: list[ClipSpec], cfg: config.RenderConfig):
        self.specs = specs
        self.cfg = cfg
        self.cache: dict[int, BuiltClip] = {}

    def get(self, ci: int) -> BuiltClip:
        c = self.cache.get(ci)
        if c is None:
            c = BuiltClip(self.specs[ci], self.cfg)
            self.cache[ci] = c
            # evict anything older than the previous clip
            for k in [k for k in self.cache if k < ci - 1]:
                self.cache.pop(k).close()
        return c

    def close(self):
        for c in self.cache.values():
            c.close()
        self.cache.clear()


def build_specs(beats: list[Beat], nar: narration.Narration,
                cfg: config.RenderConfig) -> list[ClipSpec]:
    specs: list[ClipSpec] = []
    gci = 0
    for b in beats:
        t = nar.beats[b._index]
        dur = t.end - t.start
        if cfg.montage:
            k = max(1, round(dur / max(0.5, cfg.clip_density)))
            k = min(k, max(1, int(dur / max(0.4, cfg.min_clip))))
        else:
            k = 1
        bounds = np.linspace(t.start, t.end, k + 1)
        vids = scenes._video_paths(b)
        for j in range(k):
            effect = b.effect if j == 0 else EFFECT_ROT[gci % len(EFFECT_ROT)]
            trans = b.trans if j == 0 else MONTAGE_TRANS[gci % len(MONTAGE_TRANS)]
            vpath = None
            seg = 0.0
            if vids:
                vpath = vids[j % len(vids)]
                seg = (j // len(vids)) * (bounds[j + 1] - bounds[j] + 0.4)
            specs.append(ClipSpec(
                beat=b, start=float(bounds[j]), end=float(bounds[j + 1]),
                variant=j, effect=effect, trans=trans,
                seed=cfg.seed + b._index * 101 + j * 17,
                video_path=vpath, seg_start=seg,
            ))
            gci += 1
    return specs


def _transition(prev: np.ndarray, cur: np.ndarray, kind: str, p: float):
    p = float(np.clip(p, 0, 1))
    ep = p * p * (3 - 2 * p)
    if kind in ("fade", "dissolve"):
        return crossfade(prev, cur, ep), 0.0
    if kind == "light_flash":
        out = crossfade(prev, cur, min(1.0, p * 1.6))
        return out, 0.85 * (1 - p) ** 1.5
    if kind == "speed_ramp":
        s = int(2 + 26 * (1 - abs(p - 0.5) * 2))
        a = directional_blur(prev, 0, s)
        b = directional_blur(cur, 0, s)
        return crossfade(a, b, min(1.0, p * 1.5)), 0.05
    if kind in ("whip_l", "whip_r"):
        W = cur.shape[1]
        sign = -1 if kind == "whip_l" else 1
        s = int(4 + 40 * (1 - abs(p - 0.5) * 2))
        a = directional_blur(prev, 0, s)
        b = directional_blur(cur, 0, s)
        Mp = np.float32([[1, 0, sign * ep * W], [0, 1, 0]])
        Mc = np.float32([[1, 0, sign * (ep - 1) * W], [0, 1, 0]])
        ap = cv2.warpAffine(a, Mp, (W, a.shape[0]), borderMode=cv2.BORDER_REFLECT101)
        bc = cv2.warpAffine(b, Mc, (W, b.shape[0]), borderMode=cv2.BORDER_REFLECT101)
        return crossfade(ap, bc, ep), 0.0
    return crossfade(prev, cur, ep), 0.0


def _open_ffmpeg(cfg: config.RenderConfig, vo: Path, score: Path,
                 out: Path) -> subprocess.Popen:
    gain = cfg.music_gain_db
    fc = (
        f"[2:a]aformat=channel_layouts=stereo,volume={gain}dB[bed];"
        f"[1:a]aformat=channel_layouts=stereo,asplit=2[vo][vokey];"
        f"[bed][vokey]sidechaincompress=threshold=0.025:ratio=8:attack=15:"
        f"release=350:makeup=2[duck];"
        f"[vo][duck]amix=inputs=2:normalize=0:dropout_transition=0[pre];"
        f"[pre]alimiter=limit=0.97[a]"
    )
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error", "-stats",
        "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{cfg.width}x{cfg.height}", "-r", str(cfg.fps), "-i", "-",
        "-i", str(vo), "-i", str(score),
        "-filter_complex", fc,
        "-map", "0:v", "-map", "[a]",
        "-c:v", "libx264", "-preset", cfg.preset, "-crf", str(cfg.crf),
        "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart",
        "-c:a", "aac", "-b:a", cfg.audio_bitrate,
        "-shortest", str(out),
    ]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)


def render(cfg: config.RenderConfig) -> Path:
    config.ensure_dirs()
    t_start = time.time()
    beats = storyboard()
    if cfg.limit_beats > 0:
        beats = beats[:cfg.limit_beats]

    print("[1/4] Narration ...", flush=True)
    nar = narration.generate(beats, cfg)
    duration = nar.beats[len(beats) - 1].end if cfg.limit_beats else nar.duration

    print("[2/4] Score ...", flush=True)
    score = music.generate(nar.beats[:len(beats)], beats, duration, cfg)

    print("[3/4] Building montage timeline ...", flush=True)
    specs = build_specs(beats, nar, cfg)
    pool = ClipPool(specs, cfg)
    clip_starts = np.array([s.start for s in specs])
    clip_ends = np.array([s.end for s in specs])
    beat_starts = np.array([nar.beats[b._index].start for b in beats])
    beat_ends = np.array([nar.beats[b._index].end for b in beats])
    print(f"      {len(specs)} clips across {len(beats)} lines "
          f"(~{duration / max(1, len(specs)):.1f}s/clip)", flush=True)

    look = LookEngine(cfg)
    caps = CaptionRenderer(cfg)
    fps = cfg.fps
    total_frames = int(round(duration * fps))
    out = Path(cfg.out_file)
    proc = _open_ffmpeg(cfg, nar.wav_path, score, out)

    print(f"[4/4] Rendering {total_frames} frames "
          f"({duration:.1f}s @ {cfg.width}x{cfg.height}/{fps}fps) ...", flush=True)

    grain_rng = np.random.default_rng(cfg.seed + 999)
    last_log = time.time()

    for f in range(total_frames):
        tf = f / fps
        ci = min(int(np.searchsorted(clip_ends, tf, side="right")), len(specs) - 1)
        bi = min(int(np.searchsorted(beat_ends, tf, side="right")), len(beats) - 1)
        spec = specs[ci]
        beat = beats[bi]

        clip = pool.get(ci)
        scene = clip.render(tf - spec.start)
        flash = 0.0

        if ci > 0:
            tdur = TRANS_DUR.get(spec.trans, 0.35)
            since = tf - spec.start
            if since < tdur:
                prev = pool.get(ci - 1)
                pscene = prev.render(tf - specs[ci - 1].start)
                scene, flash = _transition(pscene, scene, spec.trans, since / tdur)

        scene = caps.render(scene, beat, nar.beats[beat._index], tf)
        frame = look.finalize(scene, tf, beat.intensity, grain_rng, flash=flash)
        proc.stdin.write((np.clip(frame, 0, 1) * 255).astype(np.uint8).tobytes())

        if time.time() - last_log > 8:
            pct = 100 * (f + 1) / total_frames
            el = time.time() - t_start
            eta = el / (f + 1) * (total_frames - f - 1)
            print(f"   {pct:5.1f}%  frame {f+1}/{total_frames}  clip {ci+1}/{len(specs)}  "
                  f"elapsed {el:5.0f}s  eta {eta:5.0f}s", flush=True)
            last_log = time.time()

    pool.close()
    proc.stdin.close()
    rc = proc.wait()
    if rc != 0:
        raise RuntimeError(f"ffmpeg exited with code {rc}")
    print(f"Done in {time.time() - t_start:.0f}s -> {out}", flush=True)
    return out
