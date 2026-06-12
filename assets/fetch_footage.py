# -*- coding: utf-8 -*-
"""
Fetch copyright-free cinematic B-roll for the documentary.

Sources (in priority order, all license-clean):
  1) Pexels   — Pexels License (free, commercial OK, no attribution required).
                Used opportunistically; the egress proxy supplies credentials.
  2) Wikimedia Commons — Public Domain / Creative Commons. Reliable, no auth.
                NASA space footage here is Public Domain.

Everything is GENERIC imagery (cities, architecture, nature, space) — no real
footage of any individual is used. Clips are transcoded to clean 1080p H.264 and
trimmed, so they drop straight into Remotion.

Outputs:
  video/public/footage/<key>_<i>.mp4     (gitignored; regenerable)
  video/src/data/footage.json            (manifest the video reads)
  docs/CREDITS.md                        (full attribution)

Run:  python3 assets/fetch_footage.py
"""
import json
import os
import subprocess
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "video" / "public" / "footage"
TMP = ROOT / "assets" / ".cache"
MANIFEST = ROOT / "video" / "src" / "data" / "footage.json"
CREDITS = ROOT / "docs" / "CREDITS.md"
for d in (OUT, TMP, MANIFEST.parent, CREDITS.parent):
    d.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
PEXELS_KEY = os.environ.get("PEXELS_API_KEY", "")
CLIP_SECONDS = 16          # max length we keep per clip
TARGET_W, TARGET_H = 1920, 1080

# 1-3 on-theme, generic search terms per chapter
QUERIES = {
    "cold_open": ["city skyline night", "dark storm clouds"],
    "title":     ["new york city skyline", "city aerial skyscrapers"],
    "roots":     ["brooklyn brownstone street", "old city buildings"],
    "discipline":["foggy road morning", "rain on window"],
    "learn":     ["city traffic timelapse", "financial district"],
    "build":     ["skyscraper construction", "modern skyscraper"],
    "fame":      ["city lights night", "times square"],
    "fall":      ["thunderstorm clouds", "heavy rain night"],
    "comeback":  ["sunrise mountains", "ocean waves"],
    "global":    ["earth from space", "dubai skyline"],
    "leadership":["city business district", "skyscraper low angle"],
    "mindset":   ["stars night sky timelapse", "milky way"],
    "success":   ["mountain summit clouds", "highway timelapse"],
    "finale":    ["aerial mountains sunrise", "new york sunrise"],
    "endcard":   ["city skyline night"],
}


def run(cmd, timeout=180):
    return subprocess.run(cmd, capture_output=True, timeout=timeout)


def curl_json(url, headers=None):
    cmd = ["curl", "-s", "--max-time", "30", "-A", UA]
    for h in headers or []:
        cmd += ["-H", h]
    cmd.append(url)
    out = run(cmd, timeout=40).stdout
    return json.loads(out or b"{}")


def curl_dl(url, dest, timeout=240):
    r = run(["curl", "-sL", "--max-time", str(timeout), "-A", UA, "-o", str(dest), url], timeout=timeout + 10)
    return dest.exists() and dest.stat().st_size > 10000


def transcode(src, dest, grade=False):
    vf = (
        f"scale={TARGET_W}:{TARGET_H}:force_original_aspect_ratio=increase,"
        f"crop={TARGET_W}:{TARGET_H},fps=30,format=yuv420p"
    )
    r = run([
        "ffmpeg", "-y", "-loglevel", "error", "-t", str(CLIP_SECONDS), "-i", str(src),
        "-an", "-vf", vf, "-c:v", "libx264", "-crf", "20", "-preset", "veryfast",
        "-movflags", "+faststart", str(dest),
    ], timeout=300)
    return dest.exists() and dest.stat().st_size > 10000


# ------------------------------- Pexels --------------------------------------
def pexels(query):
    url = (f"https://api.pexels.com/videos/search?query={urllib.parse.quote(query)}"
           f"&orientation=landscape&size=medium&per_page=6")
    headers = [f"Authorization: {PEXELS_KEY}"] if PEXELS_KEY else []
    try:
        data = curl_json(url, headers)
    except Exception:
        return None
    for v in data.get("videos", []):
        if v.get("duration", 0) < 5:
            continue
        files = [f for f in v.get("video_files", [])
                 if f.get("file_type") == "video/mp4" and f.get("width", 0) > f.get("height", 0)]
        if not files:
            continue
        inr = [f for f in files if 1280 <= f["width"] <= 1920]
        f = (sorted(inr, key=lambda x: x["width"])[-1] if inr
             else sorted(files, key=lambda x: x["width"])[-1])
        return {
            "link": f["link"], "needs_transcode": f["width"] != TARGET_W or f["height"] != TARGET_H,
            "author": v.get("user", {}).get("name", "Pexels"),
            "src": v.get("url"), "license": "Pexels License", "source": "Pexels",
        }
    return None


# ---------------------------- Wikimedia Commons ------------------------------
def commons(query):
    s = (f"https://commons.wikimedia.org/w/api.php?action=query&format=json&list=search"
         f"&srnamespace=6&srlimit=12&srsearch={urllib.parse.quote(query + ' filetype:video')}")
    try:
        hits = curl_json(s).get("query", {}).get("search", [])
    except Exception:
        return None
    titles = [h["title"] for h in hits]
    if not titles:
        return None
    info = (f"https://commons.wikimedia.org/w/api.php?action=query&format=json"
            f"&prop=imageinfo&iiprop=url|size|mime|extmetadata&titles="
            + urllib.parse.quote("|".join(titles[:12])))
    try:
        pages = curl_json(info).get("query", {}).get("pages", {})
    except Exception:
        return None
    cands = []
    for p in pages.values():
        ii = (p.get("imageinfo") or [{}])[0]
        mime = ii.get("mime", "")
        w = ii.get("width", 0) or 0
        size = ii.get("size", 0) or 0
        if mime not in ("video/webm", "video/ogg", "video/mp4"):
            continue
        if w < 960 or size > 120_000_000:   # skip tiny or huge files
            continue
        m = ii.get("extmetadata", {})
        cands.append({
            "url": ii["url"], "w": w,
            "author": (m.get("Artist", {}).get("value", "Wikimedia Commons")[:120]
                       .replace("<", "").replace(">", "")),
            "license": m.get("LicenseShortName", {}).get("value", "CC"),
            "src": p.get("title"),
        })
    if not cands:
        return None
    cands.sort(key=lambda c: abs(c["w"] - 1600))
    best = cands[0]
    best["needs_transcode"] = True
    best["link"] = best["url"]
    best["source"] = "Wikimedia Commons"
    return best


def acquire(query, out_path):
    """Return clip-meta if a clip was placed at out_path, else None."""
    for finder in (pexels, commons):
        meta = finder(query)
        if not meta:
            continue
        raw = TMP / "raw_dl"
        if raw.exists():
            raw.unlink()
        if not curl_dl(meta["link"], raw):
            continue
        if meta.get("needs_transcode", True):
            if not transcode(raw, out_path):
                continue
        else:
            run(["ffmpeg", "-y", "-loglevel", "error", "-t", str(CLIP_SECONDS), "-i", str(raw),
                 "-an", "-c", "copy", "-movflags", "+faststart", str(out_path)], timeout=120)
            if not out_path.exists():
                if not transcode(raw, out_path):
                    continue
        # probe duration
        try:
            dur = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                             "-of", "default=nk=1:nw=1", str(out_path)]).stdout.decode().strip())
        except Exception:
            dur = CLIP_SECONDS
        meta["duration"] = round(dur, 2)
        meta["file"] = out_path.name
        return meta
    return None


def main():
    manifest = {"byChapter": {}, "credits": []}
    for key, queries in QUERIES.items():
        clips = []
        for qi, q in enumerate(queries):
            dest = OUT / f"{key}_{qi}.mp4"
            meta = acquire(q, dest)
            if not meta:
                print(f"  ! none for [{key}] {q}")
                continue
            clips.append({k: meta[k] for k in ("file", "duration", "author", "license", "src", "source")})
            manifest["credits"].append(
                {"query": q, "author": meta["author"], "license": meta["license"],
                 "src": meta["src"], "source": meta["source"]})
            print(f"  + {key}: {meta['file']} {meta['source']} {meta['duration']}s "
                  f"({meta['license']}) [{q}]")
            time.sleep(0.2)
        manifest["byChapter"][key] = clips

    MANIFEST.write_text(json.dumps(manifest, indent=2))

    lines = ["# Footage & Music Credits", "",
             "All B-roll is copyright-free stock used under permissive licenses",
             "(Pexels License, Public Domain, or Creative Commons). All clips are",
             "generic city / architecture / nature / space imagery — no real footage",
             "of any individual is used.", "",
             "The musical score is **100% original**, synthesised from scratch in",
             "`audio/make_music.py`. The narration is neural TTS (Piper, MIT-licensed",
             "`en_US-ryan-high` voice).", "", "## Clips", ""]
    for c in manifest["credits"]:
        lines.append(f"- *{c['query']}* — {c['author']} · {c['license']} · "
                     f"{c['source']}{(' · ' + str(c['src'])) if c.get('src') else ''}")
    CREDITS.write_text("\n".join(lines))

    total = sum(len(v) for v in manifest["byChapter"].values())
    covered = sum(1 for v in manifest["byChapter"].values() if v)
    print(f"\nDONE  {total} clips · {covered}/{len(QUERIES)} chapters have footage")


if __name__ == "__main__":
    main()
