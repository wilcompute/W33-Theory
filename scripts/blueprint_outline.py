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
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BODY = ROOT / "holonet_machine_blueprint_body.tex"

# Pass 4356: all three manuscripts, not just the blueprint.  The blueprint reached zero
# unentered headings at Pass 4348, which moved the problem rather than solving it -- the
# other two carry 477 and 347 pages and have the shared box system wired in with no
# plain-language content in it at all.
BODIES = [ROOT / "holonet_machine_blueprint_body.tex",
          ROOT / "w33_paper_body.tex",
          ROOT / "photonic_holonet_body.tex"]

HEAD = re.compile(r"^\\(part|section|subsection)\*?\{(.*)$", re.M)
# `plain`/`spec`/`warn` are the blueprint's names; `plainbox`/`specbox`/`warnbox` are the
# shared ones the other manuscripts use (renamed at Pass 4316 after `spec` collided with
# photonic_holonet's \spec math operator).
BOX = re.compile(r"\\begin\{(plain|spec|warn)(?:box)?\}")


def audit(body):
    """Per-heading box counts for one manuscript; returns the silent headings."""
    txt = body.read_text(encoding="utf-8", errors="replace")
    heads = [(m.start(), m.group(1), m.group(2).rstrip("}")[:62])
             for m in HEAD.finditer(txt)]
    tot = {"plain": 0, "spec": 0, "warn": 0}
    silent = []
    for i, (pos, lvl, title) in enumerate(heads):
        end = heads[i + 1][0] if i + 1 < len(heads) else len(txt)
        c = {k: 0 for k in tot}
        for m in BOX.finditer(txt[pos:end]):
            c[m.group(1)] += 1
            tot[m.group(1)] += 1
        if c["plain"] == 0 and end - pos > 1200:
            silent.append((lvl, title, end - pos))
    return len(heads), tot, silent


def main() -> int:
    verbose = "--verbose" in sys.argv
    grand = 0
    for body in BODIES:
        if not body.exists():
            continue
        n, tot, silent = audit(body)
        grand += len(silent)
        print(f"\n  {body.name}")
        print(f"    headings {n}   plain {tot['plain']}  spec {tot['spec']}  "
              f"warn {tot['warn']}")
        print(f"    headings over 1200 chars with NO plain-language box: {len(silent)}")
        for lvl, t, sz in sorted(silent, key=lambda r: -r[2])[:12 if not verbose else 999]:
            print(f"      {sz:6d}  {lvl:10s} {t}")
        if len(silent) > 12 and not verbose:
            print(f"      ... and {len(silent) - 12} more (--verbose for all)")
    print(f"\n  TOTAL headings with no way in for a non-specialist: {grand}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
