"""Procedural cinematic underscore with an emotional intensity arc.

Synthesizes a warm, string-like orchestral bed (pads + sub + swells + impact
hits) whose dynamics follow the story's emotional arc and build in the final
30 seconds.  A real track dropped at ``assets/music/score.*`` (or set via
``--music``) overrides this synth.
"""
from __future__ import annotations

import wave
from pathlib import Path

import numpy as np
from scipy.signal import fftconvolve

from . import config
from .narration import BeatTiming
from .script import Beat

SR = 44100

# A4 = 440. Minor-key emotional progression (Am - F - C - G), MIDI roots.
_PROG = [
    [57, 60, 64],   # Am
    [53, 57, 60],   # F
    [48, 52, 55],   # C
    [55, 59, 62],   # G
]
CHORD_LEN = 7.5  # seconds per chord


def _hz(midi: float) -> float:
    return 440.0 * 2 ** ((midi - 69) / 12.0)


def _pad(freqs, n, sr, detune=0.004):
    """Warm string-ish pad via stacked, slightly detuned, vibrato'd sines."""
    t = np.arange(n) / sr
    vib = 0.0025 * np.sin(2 * np.pi * 5.2 * t)   # gentle vibrato (in semitone frac)
    out = np.zeros(n, np.float32)
    for f in freqs:
        for octv, amp in ((1.0, 1.0), (2.0, 0.5), (0.5, 0.6), (3.0, 0.18)):
            for dt, a2 in ((1 - detune, 0.5), (1 + detune, 0.5)):
                inst = f * octv * dt * (1.0 + vib)        # instantaneous freq
                phase = 2 * np.pi * np.cumsum(inst) / sr  # phase accumulation
                out += (amp * a2) * np.sin(phase)
    out /= np.max(np.abs(out)) or 1.0
    return out.astype(np.float32)


def _impact(sr, dur=1.6, root=41):
    n = int(sr * dur)
    t = np.arange(n) / sr
    env = np.exp(-t * 4.5)
    f = _hz(root)
    body = np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 0.5 * t)
    noise = np.random.default_rng(7).normal(0, 1, n) * np.exp(-t * 30)
    sig = (body * 0.8 + noise * 0.3) * env
    return (sig / (np.max(np.abs(sig)) or 1)).astype(np.float32)


def _reverb_ir(sr, dur=1.8, seed=11):
    n = int(sr * dur)
    rng = np.random.default_rng(seed)
    t = np.arange(n) / sr
    ir = rng.normal(0, 1, n) * np.exp(-t * 3.2)
    ir[0] = 1.0
    return (ir / (np.max(np.abs(ir)) or 1) * 0.35).astype(np.float32)


def _arc_envelope(beats: list[BeatTiming], src: list[Beat], total: float) -> np.ndarray:
    """One value per sample (coarse), following beat intensities + a final build."""
    secs = int(np.ceil(total))
    env = np.full(secs + 1, 0.4, np.float32)
    for bt, b in zip(beats, src):
        a, z = int(bt.start), int(min(secs, bt.end))
        env[a:z + 1] = 0.35 + 0.55 * b.intensity
    # final 30s build to full
    for s in range(secs + 1):
        if s > total - 30:
            env[s] = max(env[s], 0.55 + 0.45 * (1 - (total - s) / 30))
    # smooth (5s)
    k = np.ones(5) / 5
    env = np.convolve(env, k, mode="same")
    full = np.interp(np.arange(int(total * SR)) / SR, np.arange(secs + 1), env)
    return full.astype(np.float32)


def _write_stereo(path: Path, left: np.ndarray, right: np.ndarray):
    st = np.stack([left, right], axis=1)
    st = np.clip(st, -1, 1)
    pcm = (st * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def generate(beats: list[BeatTiming], src: list[Beat], total: float,
             cfg: config.RenderConfig) -> Path:
    config.ensure_dirs()
    if cfg.music_file and Path(cfg.music_file).exists():
        return Path(cfg.music_file)
    for ext in (".wav", ".mp3", ".m4a", ".flac", ".ogg"):
        p = config.MUSIC / f"score{ext}"
        if p.exists():
            return p

    out = config.CACHE / "score.wav"
    n = int(total * SR)
    mix = np.zeros(n, np.float32)

    # chord pads across the whole piece
    pos = 0
    ci = 0
    fade = int(0.8 * SR)
    while pos < n:
        seg = min(int(CHORD_LEN * SR), n - pos)
        freqs = [_hz(m) for m in _PROG[ci % len(_PROG)]]
        pad = _pad(freqs, seg, SR)
        win = np.ones(seg, np.float32)
        f = min(fade, seg // 2)
        win[:f] = np.linspace(0, 1, f)
        win[-f:] = np.linspace(1, 0, f)
        mix[pos:pos + seg] += pad * win * 0.6
        pos += seg
        ci += 1

    # sub bass following chord roots
    pos, ci = 0, 0
    while pos < n:
        seg = min(int(CHORD_LEN * SR), n - pos)
        t = np.arange(seg) / SR
        root = _hz(_PROG[ci % len(_PROG)][0] - 12)
        sub = np.sin(2 * np.pi * root * t).astype(np.float32)
        win = np.hanning(seg).astype(np.float32) * 0.5 + 0.5
        mix[pos:pos + seg] += sub * 0.35 * win
        pos += seg
        ci += 1

    # impact hits on the most emotional / flash beats
    imp = _impact(SR)
    for bt, b in zip(beats, src):
        if b.trans in ("light_flash", "speed_ramp") and b.intensity >= 0.78:
            s = int(bt.voice_start * SR)
            e = min(n, s + len(imp))
            if 0 <= s < n:
                mix[s:e] += imp[:e - s] * (0.5 + 0.4 * b.intensity)

    # rising shimmer in the climax (last 45s)
    cl = int(max(0, total - 45) * SR)
    t = np.arange(n - cl) / SR
    shimmer = (np.sin(2 * np.pi * _hz(76) * t) + np.sin(2 * np.pi * _hz(79) * t))
    shimmer *= np.linspace(0, 0.18, len(t))
    mix[cl:] += shimmer.astype(np.float32)

    # apply emotional dynamic arc
    arc = _arc_envelope(beats, src, total)
    m = min(len(arc), len(mix))
    mix[:m] *= arc[:m]

    # reverb + gentle stereo width
    ir = _reverb_ir(SR)
    wet = fftconvolve(mix, ir)[:n].astype(np.float32)
    body = mix * 0.85 + wet * 0.5
    body /= (np.max(np.abs(body)) or 1.0)
    # haas-ish width
    d = int(0.012 * SR)
    left = body.copy()
    right = np.concatenate([np.zeros(d, np.float32), body[:-d]]) if d < n else body
    # global fade in/out
    fi = int(2.5 * SR); fo = int(4.0 * SR)
    g = np.ones(n, np.float32)
    g[:fi] = np.linspace(0, 1, fi)
    g[-fo:] = np.linspace(1, 0, fo)
    left *= g; right *= g
    _write_stereo(out, left * 0.9, right * 0.9)
    return out
