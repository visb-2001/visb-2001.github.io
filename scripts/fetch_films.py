#!/usr/bin/env python3
"""Fetch watched films from Letterboxd RSS and write src/misc/films.json."""

import json
import re
import ssl
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

RSS_URL = "https://letterboxd.com/visbaskaran/rss/"
OUT = Path(__file__).parent.parent / "src" / "misc" / "films.json"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(RSS_URL, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
    tree = ET.parse(r)

LB = "https://a.ltrbxd.com/resized"
ns = {"letterboxd": "https://letterboxd.com"}

films = []
for item in tree.findall(".//item"):
    title = item.findtext("{https://letterboxd.com}filmTitle", "").strip()
    year  = item.findtext("{https://letterboxd.com}filmYear", "").strip()

    # poster is in <description> as an <img src="..."> tag
    desc = item.findtext("description", "")
    match = re.search(r'<img src="([^"]+)"', desc)
    poster = match.group(1) if match else ""

    if title:
        films.append({"title": title, "year": year, "poster": poster})

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(films, indent=2))
print(f"Wrote {len(films)} films to {OUT}")
