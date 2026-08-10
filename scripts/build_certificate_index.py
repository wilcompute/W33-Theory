#!/usr/bin/env python3
"""Index certificate VALUES, so answers stop hiding in data/.

Built at Pass 2570 after six reports as "proposed, not built".  The business case is
measured, not speculative: in one session seven questions were treated as open while
their answers sat in committed certificates --

    why 73 divides the cover count        orbit histogram, pass1510
    the G-orbit structure on covers        228/84/15 by stabiliser, pass1510
    is the cover family intersecting       no, explicit pair, pass1511
    do all 327 orbits have partners        yes, pass1512
    max packing with the canonical cover   4, no K4, pass1513
    can a fifth cover be added             no, integrality gap, pass1515
    where the frame graph H is built       pass1505/1533/1821/2412

`build_topical_aliases.py` indexes prose tokens and cannot see any of these, because
certificates are prose-free.  This indexes the NUMBERS.

What it emits: for every distinctive integer appearing in any data/*.json, the files
containing it and the key path where it sits.  "Distinctive" is calibrated below --
indexing every integer would reproduce the noise problem that check_rediscovery.py and
check_certificates.py both had to be calibrated away from.

Usage:
    py -3 scripts/build_certificate_index.py            # write CERTIFICATE_INDEX.md
    py -3 scripts/build_certificate_index.py 3547800    # look one value up
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "CERTIFICATE_INDEX.md"

# Calibration.  Small integers are ubiquitous and carry no signal: 0, 1, 2, 3 appear in
# essentially every certificate as counts, flags and dimensions.  Very large ones are
# usually hashes-as-ints or byte counts.  The band below was chosen so that a value like
# 3547800, 394200, 13648, 25920 or 51840 is indexed while 0..99 and >10^12 are not.
MIN_VALUE = 100
MAX_VALUE = 10**12
# A value appearing in more than this many files is structural noise, not an answer.
MAX_FILES_PER_VALUE = 12


def walk(obj, path=""):
    """Yield (key_path, int_value) for every integer in a JSON object."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk(v, f"{path}/{k}")
            # keys are often the interesting integers (stabiliser_order_histogram)
            if isinstance(k, str) and k.lstrip("-").isdigit():
                try:
                    yield (path or "/", int(k))
                except ValueError:
                    pass
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, f"{path}[{i}]" if len(obj) < 40 else f"{path}[]")
    elif isinstance(obj, bool):
        return
    elif isinstance(obj, int):
        yield (path or "/", obj)


# Added Pass 2666.  Three withdrawals in two batches (Passes 2650, 2651, 2652) traced
# to photonic_holonet_body.tex, which nothing indexed: the certificate index covered
# data/*.json only, and prose indexes cover words rather than values.  Manuscripts and
# analysis notes carry load-bearing NUMBERS in running text, so they are indexed here
# too -- by value, with the surrounding line as the location.
TEXT_GLOBS = ("*.tex", "analysis/*.md", "docs/*.md", "*.md")
NUM = __import__("re").compile(r"(?<![\w.])(\d{3,12})(?![\w.])")


def build_text_index() -> dict[int, list[tuple[str, str]]]:
    """Values appearing in manuscripts and notes, with their line number."""
    idx: dict[int, list[tuple[str, str]]] = defaultdict(list)
    seen_files = set()
    for pat in TEXT_GLOBS:
        for f in sorted(ROOT.glob(pat)):
            if f in seen_files or not f.is_file():
                continue
            seen_files.add(f)
            try:
                lines = f.read_text(encoding="utf-8", errors="ignore").splitlines()
            except Exception:
                continue
            local: set[tuple[int, int]] = set()
            for ln, line in enumerate(lines, 1):
                for m in NUM.finditer(line.replace(",", "")):
                    v = int(m.group(1))
                    if not (MIN_VALUE <= v <= MAX_VALUE):
                        continue
                    if (v, ln) in local:
                        continue
                    local.add((v, ln))
                    idx[v].append((f.name, f":{ln}"))
    return idx


def build() -> dict[int, list[tuple[str, str]]]:
    index: dict[int, list[tuple[str, str]]] = defaultdict(list)
    for p in sorted(DATA.glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        seen: set[tuple[int, str]] = set()
        for keypath, val in walk(d):
            if not (MIN_VALUE <= abs(val) <= MAX_VALUE):
                continue
            if (val, keypath) in seen:
                continue
            seen.add((val, keypath))
            index[val].append((p.name, keypath))
    return index


def main(argv: list[str]) -> int:
    index = build()

    if argv:
        try:
            q = int(argv[0])
        except ValueError:
            print(f"not an integer: {argv[0]}")
            return 2
        tidx = build_text_index()
        hits = index.get(q, []) + tidx.get(q, [])
        if not hits:
            print(f"{q}: not found in any certificate")
            return 0
        print(f"{q}: found in {len(hits)} place(s)")
        for name, keypath in hits[:40]:
            print(f"  {name}{keypath}")
        return 0

    keep = {v: f for v, f in index.items() if len(f) <= MAX_FILES_PER_VALUE}
    lines = [
        "# Certificate value index",
        "",
        "Generated by `py -3 scripts/build_certificate_index.py`.",
        "",
        "Certificates are prose-free, so no topic search reaches them. This maps",
        "**values** to the certificates that contain them. Look a number up here",
        "**before** opening a question about it.",
        "",
        f"- certificates scanned: {len(list(DATA.glob('*.json')))}",
        f"- distinct values indexed: {len(keep)}",
        f"- calibration: values in [{MIN_VALUE}, {MAX_VALUE}] appearing in"
        f" at most {MAX_FILES_PER_VALUE} files",
        "",
        "| value | certificates |",
        "|---|---|",
    ]
    for v in sorted(keep, key=lambda x: -len(keep[x]))[:4000]:
        where = "; ".join(f"`{n}{k}`" for n, k in sorted(keep[v])[:4])
        if len(keep[v]) > 4:
            where += f" (+{len(keep[v]) - 4} more)"
        lines.append(f"| `{v}` | {where} |")
    OUT.write_text("\n".join(lines, encoding="utf-8") + "\n", encoding="utf-8")
    print(f"wrote {OUT.name}: {len(keep)} values from "
          f"{len(list(DATA.glob('*.json')))} certificates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
