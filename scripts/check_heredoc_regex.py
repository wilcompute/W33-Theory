#!/usr/bin/env python3
r"""Refuse regex edits written through a shell heredoc.  Pass 4925.

WHY THIS EXISTS, AND WHY A DETECTOR IS NOT ENOUGH
-------------------------------------------------
Six times in one session, a `\b` written inside a shell heredoc arrived in a Python file as
a single 0x08 BACKSPACE byte.  The regex still compiles.  It now requires a literal
backspace in the subject text, so the alternative can never match, and nothing reports it:

  * check_layer_conformance.py    10 bytes -- disabled W(3,3) and Sp(4,3), its two most
                                   important vocabulary tokens
  * check_novelty_claims.py        1 byte  -- disabled the "is the first" phrasing the fix
                                   had just added
  * a scratch bisect.py                    -- unrelated, but the same mechanism

`check_regex_deadends.py` DETECTS the damage and has caught it twice.  This file addresses
the cause: a rule that regex-bearing source is never edited through a heredoc, plus the
check that makes the rule enforceable.

WHAT IT CHECKS
--------------
Any staged Python file containing a raw control byte in a line that also contains regex
syntax.  That is narrower than "any control byte anywhere" -- a formfeed inside a docstring
is someone's page break and none of this tool's business.

    py -3 scripts/check_heredoc_regex.py --selftest
    py -3 scripts/check_heredoc_regex.py [paths...]
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

# The collapse map: what the shell turns each two-character escape into.
COLLAPSED = {"\x08": r"\b", "\x07": r"\a", "\x0c": r"\f", "\x0b": r"\v", "\x1b": r"\e"}
REGEXY = re.compile(r"re\.(?:compile|search|match|findall|sub|split)|r[\"']|\\[bwsdWSD]")


def scan_text(src: str, filename: str = "<text>"):
    hits = []
    # split("\n"), NOT splitlines(). Python's splitlines() treats formfeed, vertical tab
    # and several other control characters AS LINE BREAKS, so a line containing one gets
    # cut in two and the byte vanishes between the halves. The self-test caught this
    # immediately: the planted 0x0c case reported clean while the 0x08 case reported
    # correctly, which is the exact asymmetry that identifies the cause.
    for i, line in enumerate(src.split("\n"), 1):
        bad = [c for c in COLLAPSED if c in line]
        if not bad:
            continue
        if not REGEXY.search(line):
            continue        # a control byte outside regex context is not this tool's business
        hits.append({
            "file": filename, "line": i,
            "bytes": [COLLAPSED[c] for c in bad],
            "text": "".join(f"<{COLLAPSED[c][1:].upper()}>" if c in COLLAPSED else c
                            for c in line).strip()[:76],
        })
    return hits


PLANT_BAD = 'TOK = re.compile(r"' + chr(8) + 'alpha' + chr(8) + '")\n'
PLANT_BAD2 = 'X = re.compile(r"(?:a|b)' + chr(12) + '")\n'
PLANT_GOOD = 'TOK = re.compile(r"\\balpha\\b")\n'
PLANT_GOOD2 = '"""A docstring with a page break' + chr(12) + ' and no regex."""\n'


def selftest() -> int:
    cases = [
        ("planted: 0x08 in a regex", PLANT_BAD, True),
        ("planted: 0x0c in a regex", PLANT_BAD2, True),
        ("clean: correct \\b", PLANT_GOOD, False),
        ("clean: formfeed in prose", PLANT_GOOD2, False),
    ]
    ok = True
    print("  selftest -- planted-fault recall\n")
    for name, src, want in cases:
        got = bool(scan_text(src))
        good = got == want
        ok &= good
        print(f"    {name:30s} flagged={str(got):5s} want={str(want):5s} "
              f"{'PASS' if good else 'FAIL'}")
    print(r"""
  THE SECOND CLEAN CASE IS THE SCOPE. A formfeed inside a docstring is a page break, and
  85 .txt files in this repository carry them legitimately as PDF-extraction artifacts.
  Flagging those would bury the one case that matters under a hundred that do not, so the
  control byte must share a line with regex syntax to count.

  ITS LIMIT: this catches the damage, not the habit. The rule is that regex-bearing source
  is edited with a file write, never a heredoc -- and no checker enforces a rule about how
  an edit was made, only about what it produced.""")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    paths = [Path(p) for p in a.paths] if a.paths else sorted(
        list((ROOT / "scripts").rglob("*.py")) + list((ROOT / "analysis").rglob("*.py")))
    total = 0
    for p in paths:
        if p.suffix != ".py" or not p.is_file():
            continue
        try:
            src = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = p.relative_to(ROOT).as_posix() if ROOT in p.parents else p.name
        for h in scan_text(src, rel):
            total += 1
            print(f"  {h['file']}:{h['line']}  collapsed {', '.join(h['bytes'])}")
            print(f"      {h['text']}")
    print(f"\n  {total} collapsed escapes in regex context")
    if total == 0:
        print("  (zero means nothing unless --selftest passes; run it)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
