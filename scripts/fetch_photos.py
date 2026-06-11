#!/usr/bin/env python3
"""Scan src/misc/photos/ for place_year.ext files and write src/misc/photos.json.

Filename format: place_year.ext  e.g. chennai_2024.jpg, san_francisco_2024.jpg
Multi-word places use underscores: new_york_2023.jpg → "New York", 2023
"""

import json
from pathlib import Path

PHOTOS_DIR = Path(__file__).parent.parent / "src" / "misc" / "photos"
OUT = Path(__file__).parent.parent / "src" / "misc" / "photos.json"
EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

photos = []
for f in sorted(PHOTOS_DIR.iterdir()):
    if f.suffix.lower() not in EXTS:
        continue
    parts = f.stem.rsplit("_", 1)
    if len(parts) == 2 and parts[1].isdigit():
        place = parts[0].replace("_", " ").title()
        year = parts[1]
    else:
        place = f.stem.replace("_", " ").title()
        year = ""
    photos.append({
        "place": place,
        "year": year,
        "src": f"src/misc/photos/{f.name}",
    })

OUT.write_text(json.dumps(photos, indent=2))
print(f"Wrote {len(photos)} photos to {OUT}")
