#!/usr/bin/env python3
r"""Derive the guard's geometry vocabulary from the corpus instead of curating it.

WHY (Pass 1483).  `check_rediscovery.py` carries three hand-written lists --
`NAMED`, `ATOMS`, `GEOM_NOUNS`.  Pass 1479 measured the cost of exactly this
shape elsewhere: a hand-written nine-entry LaTeX macro list covered 9 of the 37
macros that actually mattered, and three manuscript builds broke in the gap.

The same risk applies here and is testable, because there is an authority: the
canonical entries in `RESULTS_VOCABULARY.md` are the object names this project
has already decided are load-bearing.  Any of those absent from the guard's
lists is a name the guard cannot see.

This does NOT auto-edit the guard.  The hand lists were calibrated -- Pass 328
measured flag rates per token class and Pass 1107 narrowed `GEOM_NOUNS` from
39.9% noise to 30.9% by REMOVING generic nouns.  Widening a calibrated list
without re-measuring would undo that.  So this reports the gap and leaves the
decision where the calibration is.

Run:  py -3 scripts/compute_geom_vocabulary.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

VOCAB = ROOT / "RESULTS_VOCABULARY.md"
RE_HEADING = re.compile(r"^#{2,3}\s+(.+?)\s*$", re.M)
RE_ALIAS = re.compile(r"`([^`]{3,40})`")


def canonical_names() -> set[str]:
    """Object names RESULTS_VOCABULARY.md treats as canonical."""
    if not VOCAB.exists():
        return set()
    t = VOCAB.read_text(encoding="utf-8", errors="ignore")
    names: set[str] = set()
    for h in RE_HEADING.findall(t):
        # headings look like "The 540 -- and the trap ..." ; keep the word-ish part
        for w in re.findall(r"[A-Za-z][A-Za-z0-9()\-]{3,24}", h):
            names.add(w.lower())
    for a in RE_ALIAS.findall(t):
        a = a.strip()
        if re.fullmatch(r"[A-Za-z][A-Za-z0-9 _\-():]{2,30}", a):
            names.add(a.lower())
    return names


def main() -> int:
    from check_rediscovery import ATOMS, GEOM_NOUNS, NAMED
    guarded = {x.lower() for x in list(NAMED) + list(ATOMS) + list(GEOM_NOUNS)}
    canon = canonical_names()
    # only report multi-word or distinctive single words, not English filler
    STOP = {"the", "and", "with", "that", "this", "from", "under", "over",
            "trap", "there", "which", "them", "were", "into", "when", "what",
            "same", "cite", "never", "object", "these", "than", "only", "both"}
    gap = sorted(n for n in canon - guarded
                 if n not in STOP and not n.isdigit() and len(n) > 4)
    print("=" * 74)
    print("[geometry vocabulary] canonical names the guard cannot see")
    print("=" * 74)
    print(f"guard lists (NAMED + ATOMS + GEOM_NOUNS) : {len(guarded)} entries")
    print(f"names in RESULTS_VOCABULARY.md           : {len(canon)}")
    print(f"canonical but UNGUARDED                  : {len(gap)}")
    for i in range(0, min(len(gap), 60), 6):
        print("   ", ", ".join(gap[i:i + 6]))
    print()
    print("  REPORTED, NOT APPLIED. The hand lists are CALIBRATED: Pass 328")
    print("  measured flag rates per token class, and Pass 1107 narrowed")
    print("  GEOM_NOUNS from 39.9% noise to 30.9% by REMOVING generic nouns.")
    print("  Widening without re-measuring would undo that. Add an entry only")
    print("  with a flag-rate measurement beside it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
