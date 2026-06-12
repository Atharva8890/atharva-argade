#!/usr/bin/env python3
"""Download copyright-free footage of Colonel Sanders and 1950s America.

All media is sourced from Wikimedia Commons under Public Domain or Creative
Commons licenses, placed into the per-archetype pools at ``assets/pool/<scene>/``
(so the montage uses real photos automatically), and every file's author and
license is written to ``assets/CREDITS.md``.

Usage:  python3 scripts/fetch_footage.py [--force]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POOL = ROOT / "assets" / "pool"
CREDITS = ROOT / "assets" / "CREDITS.md"
UA = "ColonelSandersDocFetch/1.0 (educational motivational render pipeline)"
API = "https://commons.wikimedia.org/w/api.php"
FILEPATH = "https://commons.wikimedia.org/wiki/Special:FilePath/"

# Commons file  ->  which scene pools it feeds, and a clean local base name.
MEDIA = [
    # --- Colonel Harland Sanders (the man) ---
    ("Colonel Harland Sanders in character (cropped).jpg",
     ["title", "portrait", "success", "final"], "sanders_iconic"),
    ("Colonel Sanders in Tehran, 1970s - 01.png",
     ["title", "portrait", "success"], "sanders_elderly_01"),
    ("Colonel Sanders in Tehran, 1970s - 02.jpg",
     ["handshake", "success"], "sanders_meeting"),
    ("Col. Harland Sanders' Portrait Commissioned by Winston L. Shelton.jpg",
     ["success", "final", "portrait"], "sanders_portrait"),
    ("Harland Sanders (circa 1914).png",
     ["portrait"], "sanders_young"),
    ("Harland Sanders the railroad worker.png",
     ["portrait"], "sanders_worker"),
    ("Colonel Sanders' business card, c. late 1940s.jpg",
     ["recipe"], "sanders_business_card"),
    # --- 1950s America B-roll ---
    ("1955 - Interior of the Brass Rail Restaurant.jpg",
     ["recipe", "growth", "closed"], "diner_brass_rail_1955"),
    ("Seattle - Carnival Restaurant interior, 1954.jpg",
     ["growth", "crowd"], "diner_carnival_1954"),
    ("Seattle - Bar at Jack Knop's Restaurant - 1953.jpg",
     ["closed", "growth"], "diner_jackknop_1953"),
    ("Restaurant cook, Seattle, 1954.jpg",
     ["recipe"], "diner_cook_1954"),
    ("D St at Main St, Tustin, 1950s.jpg",
     ["crowd"], "mainstreet_tustin_1950s"),
    ("Highway and Railroad, Jefferson Parish, Louisiana, 1951 cropped.jpg",
     ["road", "horizon"], "highway_jefferson_1951"),
    ("Glenn Highway bridge over Eagle River, 1950s.jpg",
     ["road", "horizon"], "highway_glenn_1950s"),
    ("Bayou Road New Orleans 1950s Car June 2021 - 01.jpg",
     ["car"], "car_1950s_bayou"),
]


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def _strip_html(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s or "")
    return re.sub(r"\s+", " ", s).strip()


def fetch_meta(filename: str) -> dict:
    params = {
        "action": "query", "titles": f"File:{filename}", "prop": "imageinfo",
        "iiprop": "extmetadata|url", "format": "json",
    }
    data = json.loads(_get(API + "?" + urllib.parse.urlencode(params)))
    pages = data.get("query", {}).get("pages", {})
    for p in pages.values():
        ii = (p.get("imageinfo") or [{}])[0]
        em = ii.get("extmetadata", {})
        return {
            "artist": _strip_html(em.get("Artist", {}).get("value", "")) or "Unknown",
            "license": em.get("LicenseShortName", {}).get("value", "?"),
            "license_url": em.get("LicenseUrl", {}).get("value", ""),
            "desc_url": ii.get("descriptionurl",
                               f"https://commons.wikimedia.org/wiki/File:{filename}"),
        }
    return {"artist": "Unknown", "license": "?", "license_url": "", "desc_url": ""}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="re-download even if present")
    ap.add_argument("--width", type=int, default=2200)
    args = ap.parse_args()

    POOL.mkdir(parents=True, exist_ok=True)
    credits: list[dict] = []
    seen: set[str] = set()

    for filename, scenes, base in MEDIA:
        ext = Path(filename).suffix.lower()
        if ext == ".png":
            ext = ".png"
        url = (FILEPATH + urllib.parse.quote(filename) + f"?width={args.width}")
        try:
            blob = _get(url)
        except Exception as e:
            print(f"  ! failed {filename}: {e}", file=sys.stderr)
            continue
        targets = []
        for sc in scenes:
            d = POOL / sc
            d.mkdir(parents=True, exist_ok=True)
            out = d / f"{base}{ext}"
            if out.exists() and not args.force:
                targets.append(out)
                continue
            out.write_bytes(blob)
            targets.append(out)
        print(f"  + {filename} -> {', '.join(s for s in scenes)}")

        if filename not in seen:
            seen.add(filename)
            meta = fetch_meta(filename)
            meta["filename"] = filename
            meta["scenes"] = scenes
            credits.append(meta)
            time.sleep(0.2)

    # write CREDITS.md
    lines = [
        "# Media Credits",
        "",
        "All footage below is used under Public Domain or Creative Commons licenses",
        "and sourced from Wikimedia Commons. CC BY / CC BY-SA images require",
        "attribution (and, for SA, share-alike); details per file are listed here.",
        "",
        "| File | Used for | Author | License | Source |",
        "|------|----------|--------|---------|--------|",
    ]
    for c in credits:
        scenes = ", ".join(c["scenes"])
        lic = c["license"]
        if c.get("license_url"):
            lic = f"[{lic}]({c['license_url']})"
        lines.append(
            f"| {c['filename']} | {scenes} | {c['artist']} | {lic} "
            f"| [Commons]({c['desc_url']}) |"
        )
    lines.append("")
    CREDITS.write_text("\n".join(lines))
    print(f"\nWrote {CREDITS} with {len(credits)} entries.")


if __name__ == "__main__":
    main()
