#!/usr/bin/env python3
"""Fetch read books from Goodreads RSS and write src/misc/books.json."""

import json
import ssl
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

RSS_URL = "https://www.goodreads.com/review/list_rss/201263692?shelf=read&sort=date_read"
OUT = Path(__file__).parent.parent / "src" / "misc" / "books.json"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(RSS_URL, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
    tree = ET.parse(r)

books = []
for item in tree.findall(".//item"):
    raw_title = item.findtext("title", "").strip()
    author = item.findtext("author_name", "").strip()

    # Title in RSS is "Book Title by Author" — strip the author suffix
    if author and raw_title.endswith(f" by {author}"):
        title = raw_title[: -(len(author) + 4)].strip()
    else:
        title = raw_title

    cover = (
        item.findtext("book_large_image_url")
        or item.findtext("book_image_url")
        or ""
    ).strip()

    if title:
        books.append({"title": title, "author": author, "cover": cover})

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(books, indent=2))
print(f"Wrote {len(books)} books to {OUT}")
