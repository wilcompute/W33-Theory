#!/usr/bin/env python3
"""Flag null results from sampling that never state the power of the search.  Pass 4689.

WHY THIS EXISTS
---------------
Pass 4680 found a sentence of the form "30,000 sampled X produced no witness -- not a proof,
but two independent searches now point the same way."  The hedge was present and the hedge
was not enough: the search covered 0.0095% of its space and had 0.95% power against a
hundred-witness set.  A null with 1% power is not weak evidence, it is very nearly none, and
summing it with a genuinely exhaustive search overstates the case.

Pass 4688 then made the point sharper.  The same space, quotiented by the symmetry the
problem already had, is 26 objects rather than 315,057,600.  So an unpowered null is often
not even the best available move -- it is a sample where an enumeration was sitting there.

The failure is not "no hedge."  It is "a sample size reported without the denominator."  That
is mechanically detectable: a number of draws, a null verdict, and no space size nearby.

WHAT IT FLAGS, AND WHAT IT DELIBERATELY DOES NOT
------------------------------------------------
Flags a file when all three appear near each other:
  * a sample count      ("30,000 sampled", "10000 random draws", "sampled 5,000")
  * a null verdict      ("no witness", "produced none", "found nothing", "zero hits")
  * and NO denominator  (no "of N", no "% of the space", no "power", no "exhaustive")

Does NOT flag exhaustive searches, which have no power question -- an enumeration that
finds nothing has found nothing, full stop.  Does NOT flag a sample that reports its
fraction, because that is the disclosure being asked for.

SELF-TEST IS MANDATORY (CLAUDE.md failure mode 7): a checker that reports zero is
indistinguishable from a clean corpus unless it is known to detect a planted fault.

    py -3 scripts/check_search_power.py --selftest
    py -3 scripts/check_search_power.py [paths...]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SAMPLE = re.compile(
    r"\b(?:sampled?|drew|draws?|random(?:ly)?\s+(?:sampled|drawn|generated|chosen)|"
    r"trials?|monte[\s-]?carlo)\b", re.I)
COUNT = re.compile(r"\b(\d{1,3}(?:,\d{3})+|\d{3,})\b")
NULL = re.compile(
    r"\b(?:no\s+(?:witness|witnesses|example|examples|counterexample|counterexamples|"
    r"solution|solutions|hits?|instances?)|produced\s+(?:no|none|zero)|found\s+(?:no|none|"
    r"nothing)|zero\s+(?:hits?|witnesses|examples|branches)|none\s+(?:were\s+)?found|"
    r"never\s+(?:found|observed)|did\s+not\s+find)\b", re.I)
DENOM = re.compile(
    r"\b(?:power|of\s+the\s+space|%\s*of\s+(?:the\s+)?(?:space|total|all)|"
    r"fraction\s+(?:sampled|of)|out\s+of\s+\d|exhaustive(?:ly)?|enumerat(?:e|ed|ion)|"
    r"all\s+\d[\d,]*\s|denominator|coverage|orbit\s+representatives?)\b", re.I)

WINDOW = 6          # lines of context in which the three must co-occur


def scan_text(text: str):
    lines = text.splitlines()
    hits = []
    for i, line in enumerate(lines):
        if not NULL.search(line):
            continue
        lo, hi = max(0, i - WINDOW), min(len(lines), i + WINDOW + 1)
        ctx = "\n".join(lines[lo:hi])
        if not SAMPLE.search(ctx):
            continue
        m = COUNT.search(ctx)
        if not m:
            continue
        if DENOM.search(ctx):
            continue
        hits.append({"line": i + 1, "count": m.group(1), "text": line.strip()[:96]})
    return hits


PLANT_BAD = """
We ran a broad search for the object.  In total 30,000 sampled stabilizer groups on
six qubits were tested against the annihilation condition, and the search produced no
witness.  Not a proof, but two independent searches now point the same way.
"""

PLANT_BAD2 = """
Monte-carlo over the configuration space: 12500 random draws, none found.
"""

PLANT_GOOD = """
We ran 30,000 sampled stabilizer groups, which is 0.0095% of the space of 315,057,600,
and found no witness.  At that coverage the power against a hundred-witness set is 0.95%,
so the null excludes only abundant witnesses.
"""

PLANT_GOOD2 = """
An exhaustive enumeration over all 5,355 codes and 4 syndromes found no super-linear
branch.  The search was complete, so no power calculation applies.
"""


def selftest() -> int:
    """Planted faults the checker must catch, and clean text it must stay silent on."""
    cases = [
        ("planted: unpowered null", PLANT_BAD, True),
        ("planted: monte-carlo null", PLANT_BAD2, True),
        ("clean: reports its coverage", PLANT_GOOD, False),
        ("clean: exhaustive search", PLANT_GOOD2, False),
    ]
    ok = True
    print("  selftest -- planted-fault recall\n")
    for name, text, want in cases:
        got = bool(scan_text(text))
        good = got == want
        ok &= good
        print(f"    {name:32s} flagged={str(got):5s} want={str(want):5s} "
              f"{'PASS' if good else 'FAIL'}")
    print("""
  The two clean cases carry the SAME sample counts and the SAME null verdicts as the two
  faults. They differ only in whether the denominator is present, which is the whole
  distinction the checker claims to make -- a checker that flagged them too would be
  reporting on the words "no witness" and nothing else.

  ITS LIMIT, STATED: planted-fault recall measures the phrasings it was given. A null
  reported in a table, a plot, or a variable name is invisible to it, and so is one phrased
  in words nobody here has used yet.""")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    paths = [Path(p) for p in a.paths] if a.paths else \
        sorted(list((ROOT / "analysis").rglob("*.py")) +
               list((ROOT / "analysis").rglob("*.md")))
    flagged = 0
    scanned = 0
    for p in paths:
        if not p.is_file():
            continue
        try:
            t = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        scanned += 1
        for h in scan_text(t):
            flagged += 1
            rel = p.relative_to(ROOT).as_posix() if ROOT in p.parents else p.name
            print(f"  {rel}:{h['line']}  n={h['count']}")
            print(f"      {h['text']}")
    print(f"\n  scanned {scanned} files, {flagged} unpowered nulls")
    if flagged == 0:
        print("  (a zero here means nothing unless --selftest passes; run it)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
