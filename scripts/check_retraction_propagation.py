#!/usr/bin/env python3
"""Find withdrawn claims that are still asserted somewhere else.  Pass 4770.

WHY THIS EXISTS
---------------
Pass 4563 withdrew "W(3,3) is self-dual".  Pass 4755 settled it by canonical form.  Pass
4761 then found **20 files still asserting it flat**, one of them load-bearing: a network
topology argument derives "perfect load balancing -- there are no hot spots" from
vertex-transitivity AND self-duality.  The transitivity half carries the conclusion; the
self-duality half is false and inert, which is the only reason the conclusion survives.

That was found by accident, while reading something else.

THE STRUCTURAL PROBLEM, which is not a discipline problem: a retraction is written in ONE
file, on the day it is discovered, in a corpus indexed by date.  Nothing carries it
backwards.  Every existing guard here checks a NEW file against prior art; none checks OLD
files against a new correction.  The arrow only points one way, and retractions travel the
other way.

HOW IT WORKS
------------
A retraction is a sentence that withdraws a claim: "NOT self-dual", "retracted", "is false",
"withdrawn".  The CLAIM is the thing being withdrawn, and it must be supplied -- inferring
it from prose is the part no regex does.  So this reads a small registry,
`data/w33_retractions.json`, of records:

    {"claim": "W(3,3) is self-dual",
     "assert_pattern": "...", "exempt_pattern": "...",
     "retracted_by": "Pass 4563", "settled_by": "Pass 4755"}

and reports every file matching `assert_pattern` without `exempt_pattern` nearby.

WHAT IT CANNOT DO: discover retractions on its own.  The registry is written by hand,
because deciding that a sentence withdraws a claim -- rather than discussing, quoting, or
restating one -- is a reading task.  What it does is make each entry permanent: once a
retraction is registered, no future file can reassert it without the hook saying so.

    py -3 scripts/check_retraction_propagation.py --selftest
    py -3 scripts/check_retraction_propagation.py [paths...]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "w33_retractions.json"
CONTEXT = 4


def load_registry():
    if not REGISTRY.exists():
        return []
    return json.loads(REGISTRY.read_text(encoding="utf-8")).get("retractions", [])


def scan_text(text: str, rec: dict):
    """Lines asserting the retracted claim with no exemption nearby."""
    ap = re.compile(rec["assert_pattern"], re.I)
    ex = re.compile(rec["exempt_pattern"], re.I) if rec.get("exempt_pattern") else None
    lines = text.splitlines()
    hits = []
    for i, line in enumerate(lines):
        if not ap.search(line):
            continue
        lo, hi = max(0, i - CONTEXT), min(len(lines), i + CONTEXT + 1)
        if ex and ex.search("\n".join(lines[lo:hi])):
            continue
        hits.append({"line": i + 1, "text": line.strip()[:100]})
    return hits


SELF_DUAL = {
    "claim": "W(3,3) is self-dual",
    "assert_pattern": r"(?=.*(?:W\(3,\s*3\)|\bW33\b|GQ\(3,\s*3\)|SRG\(40,\s*12,\s*2,\s*4\)))"
                      r".*self[- ]dual",
    "exempt_pattern": r"not\s+self[- ]dual|NOT\s+self[- ]dual|iff?\s+q\s+is\s+even|"
                      r"q\s+even|only\s+for\s+even|retract|withdraw|is\s+false|"
                      r"Pass\s*45(6[0-9]|9[0-9])|Pass\s*47[0-9][0-9]",
    "retracted_by": "Pass 4563",
    "settled_by": "Pass 4755 (BLISS canonical form, q = 2,3,4,5)",
    "why": "W(3,q) is self-dual iff q is even; q = 3 is odd. Equal point and line counts "
           "(40 = 40) and equal SRG parameters are not a duality.",
}


def selftest() -> int:
    cases = [
        ("planted: flat assertion", True,
         "The W(3,3) quadrangle is self-dual, so points and lines are interchangeable."),
        ("planted: parenthetical", True,
         "GQ(3,3) = W(3,3): 40 points and 40 lines (self-dual), the smallest case."),
        ("clean: states the retraction", False,
         "W(3,3) is NOT self-dual -- the quadrangle is self-dual iff q is even."),
        ("clean: correct parity rule", False,
         "W(3,3) self-duality holds only for even q, so not here."),
        ("clean: different subject", False,
         "The tetrahedron is a self-dual chiral hinge whose edge axes pair up."),
    ]
    ok = True
    print("  selftest -- planted-fault recall\n")
    for name, want, text in cases:
        got = bool(scan_text(text + "\n", SELF_DUAL))
        good = got == want
        ok &= good
        print(f"    {name:32s} flagged={str(got):5s} want={str(want):5s} "
              f"{'PASS' if good else 'FAIL'}")
    print("""
  THE LAST CLEAN CASE IS THE ONE THAT COST A REWRITE. Pass 4761's first audit accepted any
  subject and immediately flagged "the tetrahedron is a self-dual chiral hinge" -- a true
  statement about a different object. Self-duality is an ordinary property that many things
  genuinely have; the retracted claim is about ONE of them, so the pattern must name it.

  ITS LIMIT, AND IT IS THE BINDING ONE: this cannot DISCOVER a retraction. Every entry is
  written by hand, because deciding that a sentence withdraws a claim -- rather than
  discussing, quoting or restating one -- is a reading task. What it buys is permanence:
  once registered, no future file reasserts the claim without this saying so.""")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    recs = load_registry()
    if not recs:
        print(f"  no registry at {REGISTRY.relative_to(ROOT).as_posix()}")
        return 0

    exempt = {f for rec in recs for f in rec.get("exempt_files", [])}
    paths = [Path(p) for p in a.paths] if a.paths else sorted(
        list((ROOT / "analysis").rglob("*.py")) + list((ROOT / "analysis").rglob("*.md")) +
        list(ROOT.glob("*.tex")))
    total = 0
    for rec in recs:
        hits = []
        for p in paths:
            if not p.is_file():
                continue
            rel0 = p.relative_to(ROOT).as_posix() if ROOT in p.parents else p.name
            if rel0 in rec.get("exempt_files", []):
                continue        # the file that records a retraction must quote it
            try:
                t = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for h in scan_text(t, rec):
                rel = p.relative_to(ROOT).as_posix() if ROOT in p.parents else p.name
                hits.append((rel, h))
                break               # one line per file is enough to flag it
        if not hits:
            continue
        print(f"\n  RETRACTED: {rec['claim']}")
        print(f"    withdrawn by {rec['retracted_by']}"
              + (f", settled by {rec['settled_by']}" if rec.get("settled_by") else ""))
        print(f"    {rec.get('why', '')}")
        print(f"    still asserted in {len(hits)} file(s):")
        for rel, h in hits[:20]:
            print(f"      {rel}:{h['line']}")
            print(f"        {h['text']}")
        total += len(hits)

    print(f"\n  {total} live assertions of retracted claims across {len(recs)} registered")
    if total == 0:
        print("  (zero means nothing unless --selftest passes; run it)")
    return 0        # advisory, never blocks


if __name__ == "__main__":
    raise SystemExit(main())
