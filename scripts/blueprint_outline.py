#!/usr/bin/env python3
"""Print the machine blueprint's outline, with the reader-facing boxes counted per section.

Written for Pass 4315's reorganisation.  The document has grown to 200+ pages across many
sessions and its shape is no longer visible from the source; this makes the shape legible
so the reorganisation is a decision rather than a guess.

The three box environments carry the document's audience split:
  plain -- the cream box, plain language, for the non-specialist
  spec  -- the exact statement, for the specialist
  warn  -- the errata / withdrawn-claim box

A section with no `plain` box is one a non-engineer cannot enter.

    py -3 scripts/blueprint_outline.py
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BODY = ROOT / "holonet_machine_blueprint_body.tex"

HEAD = re.compile(r"^\\(part|section|subsection)\*?\{(.*)$", re.M)
BOX = re.compile(r"\\begin\{(plain|spec|warn)\}")


def main() -> int:
    txt = BODY.read_text(encoding="utf-8", errors="replace")
    heads = [(m.start(), m.group(1), m.group(2).rstrip("}")[:62])
             for m in HEAD.finditer(txt)]
    print(f"  {'level':10s} {'plain':>5s} {'spec':>5s} {'warn':>5s}  title")
    tot = {"plain": 0, "spec": 0, "warn": 0}
    silent = []
    for i, (pos, lvl, title) in enumerate(heads):
        end = heads[i + 1][0] if i + 1 < len(heads) else len(txt)
        seg = txt[pos:end]
        c = {k: 0 for k in tot}
        for m in BOX.finditer(seg):
            c[m.group(1)] += 1
            tot[m.group(1)] += 1
        ind = {"part": "", "section": "  ", "subsection": "    "}[lvl]
        # SUBSECTIONS COUNT TOO.  The first version only checked part and section level
        # and reported one silent section, while several long subsections -- the frame
        # unit datapath, the whole system at a glance -- had no way in for a
        # non-specialist either.  A reader does not care what level a heading is.
        if c["plain"] == 0 and end - pos > 1200:
            silent.append((lvl, title, end - pos))
        print(f"  {ind}{lvl:8s} {c['plain']:5d} {c['spec']:5d} {c['warn']:5d}  {title}")
    print(f"\n  totals: plain {tot['plain']}, spec {tot['spec']}, warn {tot['warn']}")
    print(f"  headings over 1200 chars with NO plain-language box: {len(silent)}")
    for lvl, t, n in sorted(silent, key=lambda r: -r[2]):
        print(f"    {n:6d}  {lvl:10s} {t}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
