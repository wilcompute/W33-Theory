#!/usr/bin/env python3
"""Is the published site actually the site in this repository?

Written after an outage in which GitHub's legacy Pages builder reported
`status: built` against the current commit while the CDN served an artifact 116 KB and
three sections behind, under a different <title>.  The existing smoke test asserted
HTTP 200 and stayed green for the entire duration.

So this checks the only thing that would have caught it: whether the bytes being served
are the bytes in `docs/index.html`.  Status codes are not evidence; content is.

    py -3 scripts/check_site_is_current.py
    py -3 scripts/check_site_is_current.py --url https://example.github.io/repo/

Exit codes: 0 current, 1 stale or unreachable.  Safe to run from CI or by hand.
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_URL = "https://wilcompute.github.io/W33-Theory/"
LOCAL = ROOT / "docs" / "index.html"

TITLE = re.compile(r"<title>(.*?)</title>", re.S | re.I)
SECTION = re.compile(r"<section", re.I)


def fetch(url: str) -> str | None:
    req = urllib.request.Request(url, headers={"User-Agent": "w33-site-check"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as exc:                                   # noqa: BLE001
        print(f"  could not fetch {url}: {exc}")
        return None


def summarise(name: str, doc: str) -> dict:
    t = TITLE.search(doc)
    d = {"bytes": len(doc),
         "title": (t.group(1).strip() if t else "<no title>"),
         "sections": len(SECTION.findall(doc))}
    print(f"  {name:8s} {d['bytes']:>9,d} bytes  {d['sections']:>3d} sections  "
          f"{d['title'][:58]}")
    return d


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default=DEFAULT_URL)
    args = ap.parse_args(argv)

    if not LOCAL.exists():
        print(f"local file missing: {LOCAL}")
        return 1
    local = LOCAL.read_text(encoding="utf-8", errors="ignore")

    print("comparing the published site against docs/index.html\n")
    ld = summarise("local", local)
    served = fetch(args.url)
    if served is None:
        return 1
    sd = summarise("served", served)

    print()
    if served == local:
        print("CURRENT: the published bytes are exactly the repository's bytes.")
        return 0

    print("STALE: the published site is NOT the file in this repository.")
    if sd["title"] != ld["title"]:
        print(f"  title differs  -- served {sd['title'][:50]!r}")
        print(f"                    local  {ld['title'][:50]!r}")
    if sd["bytes"] != ld["bytes"]:
        print(f"  size differs   -- served is {ld['bytes'] - sd['bytes']:+,d} bytes "
              f"from local")
    if sd["sections"] != ld["sections"]:
        print(f"  sections differ-- served {sd['sections']}, local {ld['sections']}")
    print("\n  A 200 response proves the CDN answered, not that it answered with this")
    print("  page.  If a deploy just reported success, this is the check that disagrees.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
