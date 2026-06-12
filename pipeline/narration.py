"""Neural narration generation with dramatic pacing and word-level timing."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import wave
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from . import config
from .script import Beat

SR = 22050


@dataclass
class WordTiming:
    word: str          # display form (keeps punctuation)
    clean: str         # lowercase, punctuation stripped (for highlight match)
    start: float
    end: float


@dataclass
class BeatTiming:
    index: int
    start: float          # scene start (seconds)
    voice_start: float    # first word
    voice_end: float      # last word ends
    end: float            # scene end (after dramatic pause)
    words: list[WordTiming] = field(default_factory=list)

    @property
    def duration(self) -> float:
        return self.end - self.start


@dataclass
class Narration:
    wav_path: Path
    duration: float
    beats: list[BeatTiming]


_WORD_RE = re.compile(r"[A-Za-z0-9']+")


def _clean(word: str) -> str:
    m = _WORD_RE.findall(word.lower())
    return "".join(m)


def _silence(seconds: float) -> np.ndarray:
    return np.zeros(int(round(seconds * SR)), dtype=np.float32)


def _synth_line(voice, text: str, cfg: config.RenderConfig) -> np.ndarray:
    from piper.config import SynthesisConfig

    sc = SynthesisConfig(
        length_scale=cfg.voice_length_scale,
        noise_scale=cfg.voice_noise_scale,
        noise_w_scale=cfg.voice_noise_w,
        normalize_audio=True,
        volume=1.0,
    )
    parts = [chunk.audio_float_array for chunk in voice.synthesize(text, sc)]
    if not parts:
        return np.zeros(0, dtype=np.float32)
    return np.concatenate(parts).astype(np.float32)


def _word_timings(text: str, start: float, end: float) -> list[WordTiming]:
    raw = text.split()
    words = [w for w in raw if _clean(w)]
    if not words:
        return []
    weights = np.array([len(_clean(w)) + 1.5 for w in words], dtype=np.float64)
    weights /= weights.sum()
    span = max(end - start, 1e-3)
    out: list[WordTiming] = []
    t = start
    for w, frac in zip(words, weights):
        dur = frac * span
        out.append(WordTiming(w, _clean(w), t, t + dur))
        t += dur
    return out


def _write_wav(path: Path, audio: np.ndarray) -> None:
    audio = np.clip(audio, -1.0, 1.0)
    pcm = (audio * 32767.0).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def _deepen(raw: Path, out: Path, cfg: config.RenderConfig) -> None:
    """Deepen / warm the voice with ffmpeg, preserving total duration."""
    k = cfg.voice_pitch
    # asetrate lowers pitch + slows; atempo restores original length.
    chain = [
        f"asetrate={int(round(SR * k))}",
        "aresample=" + str(SR),
        f"atempo={1.0/k:.5f}",
        # gentle warmth: lift low-mids, tame harsh highs
        "equalizer=f=120:t=q:w=1.0:g=3",
        "equalizer=f=320:t=q:w=1.2:g=1.5",
        "equalizer=f=6500:t=q:w=1.0:g=-2",
        # mentor-grade presence + compression
        "acompressor=threshold=-18dB:ratio=3:attack=8:release=180:makeup=3",
    ]
    if cfg.voice_reverb:
        chain.append("aecho=0.85:0.85:55:0.18")  # subtle room
    chain.append("alimiter=limit=0.95")
    af = ",".join(chain)
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(raw),
        "-af", af, "-ar", str(SR), "-ac", "1", str(out),
    ]
    subprocess.run(cmd, check=True)


def _duration(path: Path) -> float:
    with wave.open(str(path), "rb") as w:
        return w.getnframes() / float(w.getframerate())


def generate(beats: list[Beat], cfg: config.RenderConfig,
             force: bool = False) -> Narration:
    """Synthesize the full narration track and compute timing for every beat."""
    config.ensure_dirs()
    sig = hashlib.sha256(
        json.dumps({
            "voice": Path(cfg.voice_model).name,
            "ls": cfg.voice_length_scale, "ns": cfg.voice_noise_scale,
            "nw": cfg.voice_noise_w, "pitch": cfg.voice_pitch,
            "reverb": cfg.voice_reverb, "pause_scale": cfg.pause_scale,
            "lead_in": cfg.lead_in, "tail_out": cfg.tail_out,
            "lines": [(b.text, b.pause) for b in beats],
        }, sort_keys=True).encode()
    ).hexdigest()[:16]

    wav_path = config.CACHE / f"narration_{sig}.wav"
    json_path = config.CACHE / f"narration_{sig}.json"

    if wav_path.exists() and json_path.exists() and not force:
        data = json.loads(json_path.read_text())
        timings = [
            BeatTiming(
                index=b["index"], start=b["start"], voice_start=b["voice_start"],
                voice_end=b["voice_end"], end=b["end"],
                words=[WordTiming(**w) for w in b["words"]],
            ) for b in data["beats"]
        ]
        return Narration(wav_path, data["duration"], timings)

    from piper import PiperVoice

    if not Path(cfg.voice_model).exists():
        raise FileNotFoundError(
            f"Voice model not found: {cfg.voice_model}\n"
            "Run scripts/fetch_voice.sh to download it."
        )
    voice = PiperVoice.load(cfg.voice_model)

    track: list[np.ndarray] = []
    timings: list[BeatTiming] = []
    cursor = 0.0

    def append(audio: np.ndarray) -> None:
        nonlocal cursor
        track.append(audio)
        cursor += len(audio) / SR

    append(_silence(cfg.lead_in))

    for b in beats:
        start = cursor
        if b.text.strip():
            audio = _synth_line(voice, b.text, cfg)
            # small breath before the line for gravitas
            breath = _silence(0.12)
            append(breath)
            voice_start = cursor
            append(audio)
            voice_end = cursor
        else:
            voice_start = voice_end = cursor
        pause = max(0.0, b.pause * cfg.pause_scale)
        append(_silence(pause))
        end = cursor
        timings.append(BeatTiming(
            index=b._index, start=start, voice_start=voice_start,
            voice_end=voice_end, end=end,
            words=_word_timings(b.text, voice_start, voice_end),
        ))

    append(_silence(cfg.tail_out))

    full = np.concatenate(track) if track else np.zeros(0, np.float32)
    raw_path = config.CACHE / f"narration_raw_{sig}.wav"
    _write_wav(raw_path, full)
    _deepen(raw_path, wav_path, cfg)

    duration = _duration(wav_path)
    # ffmpeg filters can nudge length by a few ms; rescale timing to match.
    raw_dur = len(full) / SR
    if raw_dur > 0:
        scale = duration / raw_dur
        for t in timings:
            t.start *= scale; t.voice_start *= scale
            t.voice_end *= scale; t.end *= scale
            for w in t.words:
                w.start *= scale; w.end *= scale
    timings[-1].end = duration

    json_path.write_text(json.dumps({
        "duration": duration,
        "beats": [
            {
                "index": t.index, "start": t.start, "voice_start": t.voice_start,
                "voice_end": t.voice_end, "end": t.end,
                "words": [w.__dict__ for w in t.words],
            } for t in timings
        ],
    }))
    raw_path.unlink(missing_ok=True)
    return Narration(wav_path, duration, timings)
