# -*- coding: utf-8 -*-
"""
Original, royalty-free procedural cinematic score.

No samples, no copyrighted material: the score is synthesised from scratch with
numpy. It follows the emotional arc of the documentary (dark open -> rise ->
fall -> hopeful comeback -> grand climax) by changing chords + intensity per
chapter, with transition booms/risers and a building finale.

render_music(segments, total_sec) -> float32 mono numpy array @ SR
  segments: list of dicts {start, end, chord (list[Hz]), intensity, boom, riser, climax}
"""
import numpy as np

SR = 44100


def _adsr(n, a, r):
    env = np.ones(n, dtype=np.float32)
    ai = int(a * SR)
    ri = int(r * SR)
    if ai > 0:
        env[:ai] = np.linspace(0, 1, ai, dtype=np.float32) ** 1.6
    if ri > 0:
        env[-ri:] = np.linspace(1, 0, ri, dtype=np.float32) ** 1.6
    return env


def _voice(freq, n, intensity):
    """A warm detuned pad voice (a few soft harmonics)."""
    t = np.arange(n, dtype=np.float32) / SR
    sig = np.zeros(n, dtype=np.float32)
    # slight pitch drift for an organic, non-synthetic feel
    drift = 1.0 + 0.0015 * np.sin(2 * np.pi * 0.07 * t + freq)
    for det, amp in ((0.996, 0.5), (1.004, 0.5)):
        ph = 2 * np.pi * freq * det * drift
        sig += amp * np.sin(ph * t)
        sig += amp * 0.32 * np.sin(2 * ph * t)   # 2nd harmonic
        sig += amp * 0.16 * np.sin(3 * ph * t)   # 3rd harmonic
    # slow breathing tremolo
    sig *= (1.0 + 0.06 * np.sin(2 * np.pi * 0.09 * t))
    return sig


def _segment(seg):
    n = max(1, int((seg["end"] - seg["start"]) * SR))
    chord = seg["chord"]
    intensity = seg["intensity"]
    out = np.zeros(n, dtype=np.float32)

    for f in chord:
        out += _voice(f, n, intensity)
    out /= max(1, len(chord))

    # sub bass on the root
    t = np.arange(n, dtype=np.float32) / SR
    root = min(chord) / 2.0
    sub = np.sin(2 * np.pi * root * t) * (0.9 + 0.1 * np.sin(2 * np.pi * 0.05 * t))
    out += 0.6 * sub

    out *= intensity
    # gentle edge fades so overlap-add crossfades cleanly
    out *= _adsr(n, 0.9, 1.3)
    return out


def _boom(intensity):
    n = int(2.4 * SR)
    t = np.arange(n, dtype=np.float32) / SR
    decay = np.exp(-t / 0.9)
    tone = np.sin(2 * np.pi * 46 * t) + 0.5 * np.sin(2 * np.pi * 92 * t)
    click = (np.random.randn(n).astype(np.float32)) * np.exp(-t / 0.04) * 0.25
    return (tone * decay + click) * 0.55 * (0.7 + 0.6 * intensity)


def _riser(dur=1.6):
    n = int(dur * SR)
    t = np.arange(n, dtype=np.float32) / SR
    ramp = (t / dur) ** 2.2
    sweep = np.sin(2 * np.pi * (200 + 2200 * (t / dur) ** 2) * t)
    noise = np.random.randn(n).astype(np.float32)
    return (0.5 * sweep + 0.5 * noise) * ramp * 0.18


def _reverb(x):
    """Cheap multi-tap reverb for a sense of space."""
    out = x.copy()
    for delay, gain in ((0.071, 0.30), (0.137, 0.22), (0.211, 0.15), (0.307, 0.09)):
        d = int(delay * SR)
        pad = np.zeros(len(x) + d, dtype=np.float32)
        pad[d:] += x * gain
        out += pad[: len(x)]
    return out


def render_music(segments, total_sec):
    total = int(total_sec * SR) + SR
    bus = np.zeros(total, dtype=np.float32)
    xfade = int(1.1 * SR)
    win = np.hanning(2 * xfade)

    for seg in segments:
        s = int(seg["start"] * SR)
        body = _segment(seg)
        # crossfade in/out at segment joints
        if len(body) > 2 * xfade:
            body[:xfade] *= win[:xfade]
            body[-xfade:] *= win[xfade:]
        end = min(total, s + len(body))
        bus[s:end] += body[: end - s]

        if seg.get("riser"):
            r = _riser()
            rs = max(0, s - len(r))
            bus[rs:rs + len(r)] += r[: total - rs]
        if seg.get("boom", True):
            b = _boom(seg["intensity"])
            be = min(total, s + len(b))
            bus[s:be] += b[: be - s]

    # finale climax: a swelling octave shimmer + soft sub pulse on the last region
    climax = [s for s in segments if s.get("climax")]
    if climax:
        cs = int(climax[0]["start"] * SR)
        ce = min(total, int(climax[-1]["end"] * SR))
        n = ce - cs
        t = np.arange(n, dtype=np.float32) / SR
        swell = (t / (n / SR)) ** 1.3
        chord = climax[0]["chord"]
        sh = np.zeros(n, dtype=np.float32)
        for f in chord:
            sh += np.sin(2 * np.pi * f * 2 * t)
        sh *= swell * 0.12 / max(1, len(chord))
        # heartbeat-ish sub pulse building intensity
        pulse_hz = 1.4
        pulse_env = (0.5 + 0.5 * np.sin(2 * np.pi * pulse_hz * t - np.pi / 2)) ** 6
        pulse = np.sin(2 * np.pi * 50 * t) * pulse_env * swell * 0.25
        bus[cs:ce] += sh + pulse

    bus = _reverb(bus)

    # master: soft-knee normalise + tanh limiter
    peak = float(np.max(np.abs(bus))) or 1.0
    bus = bus / peak * 0.9
    bus = np.tanh(bus * 1.1) * 0.92
    return bus[: int(total_sec * SR)]
