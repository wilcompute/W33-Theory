#!/usr/bin/env python3
"""Does this pass state its own scope?  The 2026-05 convention, reinstated.

WHY THIS EXISTS
---------------
Pass 4388 set out to measure whether the corpus's coincidence-language concentrated in
decorative sections.  It did not (19 decorative vs 20 load-bearing over 216 flags, hypothesis
refuted).  But the falsifying run turned up something the hypothesis had been standing in
front of:

    arc              files   closes with "Honest boundary"
    2026-05             98   86  (88%)
    2026-06             15    0
    2026-07             69    0
    everything else   1427   22  ( 2%)

One arc wrote a short closing section on every file naming exactly what had been proved and
what had not.  It worked -- three of the five passages hardest to judge in Pass 4388's
sample turned out to be scoped by their own file's boundary section -- and then it stopped,
and nothing replaced it.

`CLAUDE.md`'s two most expensive failure modes both reduce to a missing sentence:

    mode 2  over-read        -- the result is right, the framing exceeds the proof
    mode 6  untested premise -- a comparison made before checking it was licensed

A boundary section is where that sentence goes, and having a standard heading for it is
what makes it auditable instead of a matter of authorial mood.

WHAT COUNTS
-----------
Any of: "Honest boundary", "Honesty boundary", "Evidence boundary", "Scope", "What this
does not show", or a `boundary`/`scope` key in the pass's emitted certificate.  The point
is the statement, not the wording.

This check WARNS, it never blocks.  A blocking novelty-style gate trains `--no-verify`
(CLAUDE.md says so about check_rediscovery.py, which was calibrated the same way).

    py -3 scripts/check_honest_boundary.py --selftest
    py -3 scripts/check_honest_boundary.py analysis/w33_pass43*.py
    py -3 scripts/check_honest_boundary.py --since-arc 2026-06     # md files by arc
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# In prose: a heading.  In a pass script: a heading in the docstring, a printed banner,
# or a certificate key -- all three are in live use and all three are the same statement.
HEADING = re.compile(
    r"^\s*#{1,6}\s*(honest\w*|honesty|evidence)\s+boundary\b"
    r"|^\s*#{1,6}\s*scope\b"
    r"|^\s*#{1,6}\s*what this (?:does not|doesn't) (?:show|prove|establish)\b",
    re.I | re.M)
INLINE = re.compile(
    r"\b(honest\w*\s+boundary|honesty\s+boundary|evidence\s+boundary|"
    r"scope\s+(?:of\s+this|statement)|what this does not (?:show|prove|license)|"
    r"does not (?:yet )?license|stated here as open|scope stated|"
    r"and that is all it says|is not licensed by)\b", re.I)
CERT_KEY = re.compile(r'["\'](boundary|scope|open|honest_boundary|evidence_boundary|'
                      r'not_established|limits)["\']\s*:', re.I)
# Scope language ANYWHERE in the file, however phrased.  The gap between this and the
# findable forms above is the measurement that matters: files that DO state their scope
# but bury it where no reader or auditor will look.
LOOSE = re.compile(
    r"\b(this (?:does|proves|establishes) not\b|does not (?:yet )?(?:prove|show|"
    r"establish|license|settle)|is an assumption\b|not a measurement\b|"
    r"only the\b.{0,30}\bsubgroup|measured (?:only )?at\b|"
    r"is not licensed|open question|stated as open|remains open|"
    r"not sufficient\b|necessary and not sufficient|"
    r"i have not\b|has not been (?:asked|run|attempted|checked)|"
    r"cannot conclude|withdraw)\b", re.I)


def has_boundary(text: str) -> tuple[bool, str]:
    m = HEADING.search(text)
    if m:
        return True, "heading: " + " ".join(m.group(0).split())[:44]
    m = CERT_KEY.search(text)
    if m:
        return True, "certificate key: " + m.group(1)
    m = INLINE.search(text)
    if m:
        return True, "inline: " + m.group(0)[:44]
    return False, ""


def selftest() -> int:
    """A checker that cannot fail is not evidence (CLAUDE.md failure mode 7)."""
    cases = [
        ("prose with a boundary heading",
         "# A pass\n\nText.\n\n## Honest boundary\n\nThis proves X only.\n", True),
        ("prose with an evidence boundary",
         "# A pass\n\n### Evidence boundary\n\nMeasured at q=3 only.\n", True),
        ("script with a certificate key",
         'out = {"result": 7, "boundary": "q=3 only"}\n', True),
        ("script with an inline scope sentence",
         'print("""this does not license the design conclusion""")\n'
         'x = 1  # stated here as open\n', True),
        ("nothing at all",
         "# A pass\n\n## Result\n\nThe answer is 40.\n\n## Next\n\nMore.\n", False),
        ("the word boundary used for something else",
         "# A pass\n\nThe boundary of the polytope has 12 faces.\n", False),
    ]
    ok = True
    print("  selftest")
    for name, text, want in cases:
        got, why = has_boundary(text)
        good = got == want
        ok &= good
        print(f"    {name:42s} expected {str(want):5s} got {str(got):5s} "
              f"{'PASS' if good else 'FAIL'}  {why}")
    print("""
  The last two cases are the ones that matter. A checker that accepts any occurrence of
  the word "boundary" would pass a file describing a polytope, and would then report a
  clean corpus while measuring nothing -- failure mode 7 exactly.""")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--since-arc", help="only date-named analysis files from this arc on")
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    if a.files:
        paths = [Path(f) if Path(f).is_absolute() else ROOT / f for f in a.files]
    else:
        paths = sorted((ROOT / "analysis").glob("*.md")) + \
                sorted((ROOT / "analysis").glob("w33_pass*.py"))
    if a.since_arc:
        paths = [p for p in paths
                 if re.match(r"\d{4}-\d{2}", p.name) and p.name[:7] >= a.since_arc]

    findable, buried, absent = [], [], []
    for p in paths:
        try:
            t = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        ok, _ = has_boundary(t)
        if ok:
            findable.append(p.name)
        elif LOOSE.search(t):
            buried.append(p.name)
        else:
            absent.append(p.name)

    n = len(findable) + len(buried) + len(absent)
    print(f"  files scanned                              : {n}")
    print(f"  scope statement in a FINDABLE place        : {len(findable):4d}"
          f"  ({100 * len(findable) / max(n, 1):3.0f}%)")
    print(f"  scope language present but BURIED in prose : {len(buried):4d}"
          f"  ({100 * len(buried) / max(n, 1):3.0f}%)")
    print(f"  no scope language ANYWHERE                 : {len(absent):4d}"
          f"  ({100 * len(absent) / max(n, 1):3.0f}%)")

    print("""
  READ THE MIDDLE ROW CORRECTLY -- IT IS NOT A DEFECT COUNT.  A file in the BURIED row
  states its scope; it just does not put the statement anywhere a reader or an auditor
  can find without reading the whole file.  Pass 4363 says "SO THE THIRD FACTOR IS AN
  ASSUMPTION, not a measurement" in the middle of a printed paragraph; Pass 4335 says
  "that pass audits only the LINEAR subgroup" on line 87.  Both are exemplary and both
  are invisible to a grep.

  THAT GAP IS THE WHOLE POINT OF THE CONVENTION.  The 2026-05 arc did not write better
  scope statements than these -- it wrote them UNDER A STANDARD HEADING, which is what
  turns a habit into something auditable. The bottom row is the one to worry about.""")
    if absent:
        print("\n  no scope language anywhere:")
        for name in absent[:25]:
            print(f"    {name}")
        if len(absent) > 25:
            print(f"    ... and {len(absent) - 25} more")
    print("""
  WARNS, NEVER BLOCKS. A missing boundary section is not a defect in the mathematics; it
  is a missing sentence about what the mathematics covers. Blocking on it would train
  --no-verify, and the whole value of the convention is that people keep using it.""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
