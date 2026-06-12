"""Frame compositor + ffmpeg encode orchestrator."""
from __future__ import annotations

import subprocess
import time
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


class BeatClip:
    """Renders the (pre-look) scene image for one beat at any local time."""

    def __init__(self, beat: Beat, timing: narration.BeatTiming,
                 cfg: config.RenderConfig, rng: np.random.Generator):
        self.beat = beat
        self.timing = timing
        self.cfg = cfg
        self.art = scenes.build(beat, cfg, rng)
        dur = timing.end - timing.start
        pad = 0.5  # extra so motion keeps flowing through the next cut
        self.n = max(1, int(round((dur + pad) * cfg.fps)))
        plate_wh = (self.art.bg.shape[1], self.art.bg.shape[0])
        self.cam = CameraPath(beat, cfg, self.n, plate_wh, rng)
        self.dof = 2.2 if self.art.fg is not None else 0.0

    def render(self, local_t: float) -> np.ndarray:
        idx = int(round(local_t * self.cfg.fps))
        idx = max(0, min(self.n - 1, idx))
        m_bg, m_fg = self.cam.at(idx)
        W, H = self.cfg.width, self.cfg.height
        bg = warp(self.art.bg, m_bg, W, H)
        if self.art.fg is not None:
            fg = cv2.warpAffine(self.art.fg, m_fg, (W, H), flags=cv2.INTER_LINEAR,
                                borderMode=cv2.BORDER_CONSTANT, borderValue=0)
            if self.dof > 0:
                bg = cv2.GaussianBlur(bg, (0, 0), self.dof)
            a = np.clip(fg[..., 3:4], 0, 1)
            bg = bg * (1 - a) + fg[..., :3] * a
        return np.clip(bg, 0, 1)


def _transition(prev: np.ndarray, cur: np.ndarray, kind: str, p: float):
    """Blend two scene frames. p in [0,1] across the transition window."""
    p = float(np.clip(p, 0, 1))
    ep = p * p * (3 - 2 * p)
    if kind in ("fade", "dissolve"):
        return crossfade(prev, cur, ep), 0.0
    if kind == "light_flash":
        out = crossfade(prev, cur, min(1.0, p * 1.6))
        flash = 0.85 * (1 - p) ** 1.5
        return out, flash
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

    print("[3/4] Building scene clips ...", flush=True)
    rng = np.random.default_rng(cfg.seed)
    clips: list[BeatClip] = []
    for b in beats:
        t = nar.beats[b._index]
        clips.append(BeatClip(b, t, cfg, np.random.default_rng(cfg.seed + b._index * 17)))

    look = LookEngine(cfg)
    caps = CaptionRenderer(cfg)
    fps = cfg.fps
    total_frames = int(round(duration * fps))
    out = Path(cfg.out_file)
    proc = _open_ffmpeg(cfg, nar.wav_path, score, out)

    print(f"[4/4] Rendering {total_frames} frames "
          f"({duration:.1f}s @ {cfg.width}x{cfg.height}/{fps}fps) ...", flush=True)

    # map frame -> active beat index
    starts = np.array([nar.beats[b._index].start for b in beats])
    ends = np.array([nar.beats[b._index].end for b in beats])
    grain_rng = np.random.default_rng(cfg.seed + 999)
    last_log = time.time()

    for f in range(total_frames):
        tf = f / fps
        bi = int(np.searchsorted(ends, tf, side="right"))
        bi = min(bi, len(beats) - 1)
        clip = clips[bi]
        b = clip.beat
        local = tf - starts[bi]
        scene = clip.render(local)
        flash = 0.0

        # transition into this beat
        if bi > 0:
            tdur = TRANS_DUR.get(b.trans, 0.35)
            since = tf - starts[bi]
            if since < tdur:
                prev = clips[bi - 1]
                prev_local = tf - starts[bi - 1]
                pscene = prev.render(prev_local)
                p = since / tdur
                scene, flash = _transition(pscene, scene, b.trans, p)

        scene = caps.render(scene, b, clip.timing, tf)
        frame = look.finalize(scene, tf, b.intensity, grain_rng, flash=flash)
        u8 = (np.clip(frame, 0, 1) * 255).astype(np.uint8)
        proc.stdin.write(u8.tobytes())

        if time.time() - last_log > 8:
            pct = 100 * (f + 1) / total_frames
            el = time.time() - t_start
            eta = el / (f + 1) * (total_frames - f - 1)
            print(f"   {pct:5.1f}%  frame {f+1}/{total_frames}  "
                  f"elapsed {el:5.0f}s  eta {eta:5.0f}s", flush=True)
            last_log = time.time()

    proc.stdin.close()
    rc = proc.wait()
    if rc != 0:
        raise RuntimeError(f"ffmpeg exited with code {rc}")
    print(f"Done in {time.time() - t_start:.0f}s -> {out}", flush=True)
    return out
