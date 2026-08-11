#!/usr/bin/env python3
r"""Find guard patterns that match the OPPOSITE of what they detect.  Pass 4811.

WHY THIS EXISTS
---------------
`check_novelty_claims.py` had `does not appear to be new` inside its NOVELTY alternation --
the list of phrasings that ASSERT priority.  That phrase is an author DISCLAIMING priority.
So the guard fired on exactly the sentences being careful and stayed silent on the careless
ones, and it did that for as long as it had existed, because nothing ever asked it to
classify a known case.

That is a bug with a shape: a NEGATION inside an assertion list.  It is invisible to
testing-by-running -- the pattern compiles, matches text, and returns hits -- and it is
invisible to reading, because a long alternation of near-synonyms is exactly the kind of
thing eyes slide over.  It is not invisible to grep.

WHAT IT DOES, AND WHAT THE FIRST VERSION DID WRONG
--------------------------------------------------
v1 flagged any alternative CONTAINING a negation, inside a pattern whose name reads as an
assertion list.  That returned 12 hits in scripts/ and every one was legitimate: `no prior
art` and `has never been` ASSERT novelty while containing negations, because the negation
lands on the opposite concept.  0/12 precision, which trains exactly the skimming CLAUDE.md
warns about.

The signal is narrower.  An inversion is a negation applied to the CLAIM WORD itself --
`does not appear to be NEW`, `is NOT NOVEL` -- not a negation of the thing being denied.
So the test is whether a negation sits within a few words of `new|novel|first|original`,
and patterns named for exemption (`EXEMPT`, `CLEAN`, `DISCLAIM`, `SAFE`) are skipped
outright, since a negation there is the point.

WHAT IT CANNOT DO: generalise past the novelty axis.  A minimality list inverted by
`cannot be minimal`, or a correctness list inverted by `is not wrong`, needs its own claim
words, and only the novelty pair is encoded here.

    py -3 scripts/check_pattern_inversions.py --selftest
    py -3 scripts/check_pattern_inversions.py [paths...]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]

ASSERTION_NAME = re.compile(
    r"CLAIM|ASSERT|NOVELTY|RISK|FORBIDDEN|BAD|VIOLAT|WRONG|SUSPECT|HAZARD|RETRACT", re.I)
EXEMPT_NAME = re.compile(
    r"EXEMPT|CLEAN|SAFE|DISCLAIM|\bOK\b|ALLOW|SKIP|IGNORE|NOISE|QUALIF|CORRECT", re.I)
# "CONTAINS A NEGATION" IS THE WRONG SIGNAL, and the first version of this file proved it:
# 12 hits in scripts/, all legitimate. "no prior art" and "has never been" ASSERT novelty
# while containing negations, because the negation lands on the OPPOSITE concept -- prior
# art, previous statement. A checker firing on all of those has 0/12 precision and trains
# the skimming CLAUDE.md warns about.
#
# The inversion is specific: a negation applied to the CLAIM WORD. "does not appear to be
# NEW" and "is NOT NOVEL" reverse the claim; "no PRIOR ART" does not. So the test is
# whether a negation sits within a few words of the concept the list is asserting, and not
# whether the alternative contains a negation anywhere.
CLAIM_WORD = r"(?:new|novel|first|original|unprecedented)"
ANTI_WORD = r"(?:prior|previous|known|stated|published|noticed|precedent|literature)"
INVERSION = re.compile(
    rf"(?:\bnot\b|\bno\b|\bnever\b|\bcannot\b|\bdoes ?n[o']t\b|\bis ?n[o']t\b|"
    rf"\bfails? to\b)(?:\W+\w+){{0,3}}\W+{CLAIM_WORD}\b", re.I)
NEGATION = INVERSION        # kept for the scan below; the name now means what it does

DEF = re.compile(r"^(?P<name>[A-Z_][A-Z0-9_]*)\s*=\s*re\.compile\(", re.M)
STRING = re.compile(r"r?[\"']([^\"']*)[\"']")


def split_alternatives(pat: str):
    out, buf, depth, incls, i = [], [], 0, False, 0
    while i < len(pat):
        c = pat[i]
        if c == "\\" and i + 1 < len(pat):
            buf.append(pat[i:i + 2])
            i += 2
            continue
        if incls:
            if c == "]":
                incls = False
        elif c == "[":
            incls = True
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        elif c == "|":
            out.append("".join(buf))
            buf = []
            i += 1
            continue
        buf.append(c)
        i += 1
    out.append("".join(buf))
    return out


def scan_text(src: str, filename: str = "<text>"):
    hits = []
    for m in DEF.finditer(src):
        name = m.group("name")
        if EXEMPT_NAME.search(name) or not ASSERTION_NAME.search(name):
            continue
        # pattern body: from the compile up to the closing paren-ish region
        tail = src[m.end():m.end() + 1400]
        pat = "".join(STRING.findall(tail.split(")\n")[0]))
        for alt in split_alternatives(pat):
            clean = re.sub(r"[\\()?:*+\[\]{}|^$]", " ", alt)
            if NEGATION.search(clean):
                hits.append({"file": filename, "pattern": name,
                             "alternative": alt.strip()[:70]})
    return hits


PLANT_BAD = '''
NOVELTY = re.compile(
    r"(no prior art|has never been|does not appear to be new|first time)", re.I)
'''
PLANT_GOOD_NAME = '''
DISCLAIM = re.compile(
    r"(does not appear to be new|is not new|not novel|already known)", re.I)
'''
PLANT_GOOD_NONEG = '''
CLAIM = re.compile(r"(is the first|we prove|we establish|novel construction)", re.I)
'''


def selftest() -> int:
    cases = [
        ("planted: negation in an assertion list", PLANT_BAD, True),
        ("clean: same phrases, EXEMPT name", PLANT_GOOD_NAME, False),
        ("clean: assertion list, no negation", PLANT_GOOD_NONEG, False),
    ]
    ok = True
    print("  selftest -- planted-fault recall\n")
    for name, src, want in cases:
        got = bool(scan_text(src))
        good = got == want
        ok &= good
        print(f"    {name:40s} flagged={str(got):5s} want={str(want):5s} "
              f"{'PASS' if good else 'FAIL'}")
    print("""
  THE SECOND CASE CARRIES THE IDENTICAL PHRASES and must stay silent, because a negation
  inside a DISCLAIM list is the entire purpose of a DISCLAIM list. The check is not "does
  this pattern contain a negation" -- most useful patterns do -- but "does an ASSERTION
  list contain one", and the name is the only thing that distinguishes them.

  ITS LIMIT: it cannot decide whether a negation is WRONG. "cannot be beaten" belongs in a
  minimality-claim list and contains one. Every hit needs reading; the value is that there
  are few enough to read.""")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    paths = [Path(p) for p in a.paths] if a.paths else sorted(
        (ROOT / "scripts").glob("*.py"))
    total = 0
    for p in paths:
        if p.suffix != ".py" or not p.is_file():
            continue
        if p.resolve() == Path(__file__).resolve():
            # this file's own PLANT_* constants contain a NOVELTY = re.compile(...) with
            # the planted inversion inside a string literal; the scanner cannot tell that
            # from a real definition, and a checker flagging its own test fixture is noise.
            continue
        try:
            src = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = p.relative_to(ROOT).as_posix() if ROOT in p.parents else p.name
        for h in scan_text(src, rel):
            total += 1
            print(f"  {h['file']}  {h['pattern']}")
            print(f"      negation in an assertion alternative: {h['alternative']!r}")
    print(f"\n  {total} negations inside assertion lists")
    if total == 0:
        print("  (zero means nothing unless --selftest passes; run it)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
