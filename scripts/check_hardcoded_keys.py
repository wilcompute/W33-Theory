#!/usr/bin/env python3
r"""Find hard-coded key names where a canonical list already exists.  Pass 4882.

WHY THIS EXISTS
---------------
`check_certificates.py` produced FOUR false-positive families in one session, and all four
reduce to one habit: assuming a key name implies a convention.

  Pass 4801  numeric keys read as evidence the producer used integer keys
  Pass 4932  `sha256` read as self-digest inside registry POINTER entries
  Pass 4933  a mismatch read as staleness when the target had no digest at all
  Pass 4873  the target's digest looked up under ONE name when THREE are canonical

The fourth is the sharpest: that file defines `SELF_DIGEST_KEYS = ("sha256_without_hash_
field", "sha256", "universe_sha256")` at the top, documents why all three are needed, and
then six lines below hard-codes `td.get("sha256")`. The canonical list existed, was
correct, and was ignored by its own author.

That is greppable. A module that defines a tuple or frozenset of key names, and then also
calls `.get("<one of them>")` on a dict, is either using the list or shadowing it.

WHAT IT CANNOT DO: tell which. A single-key lookup is legitimate when the code genuinely
means that one key. Every hit needs reading; the value is that there are few of them.

    py -3 scripts/check_hardcoded_keys.py --selftest
    py -3 scripts/check_hardcoded_keys.py [paths...]
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

# a module-level tuple/frozenset/list of string literals, named like a key registry
CANON = re.compile(
    r"^(?P<name>[A-Z_][A-Z0-9_]*(?:KEYS|NAMES|FIELDS|ALIASES))\s*=\s*[\(\[{]"
    r"(?P<body>[^)\]}]*)[\)\]}]", re.M)
LITERAL = re.compile(r"[\"']([\w.]+)[\"']")
GETCALL = re.compile(r"\.get\(\s*[\"'](?P<key>[\w.]+)[\"']|\[\s*[\"'](?P<k2>[\w.]+)[\"']\s*\]")


def scan_text(src: str, filename: str = "<text>"):
    hits = []
    for m in CANON.finditer(src):
        name = m.group("name")
        members = set(LITERAL.findall(m.group("body")))
        if len(members) < 2:
            continue
        tail = src[m.end():]
        for g in GETCALL.finditer(tail):
            key = g.group("key") or g.group("k2")
            if key in members:
                ln = src[:m.end() + g.start()].count("\n") + 1
                hits.append({"file": filename, "line": ln, "canonical_list": name,
                             "hard_coded": key,
                             "siblings": sorted(members - {key})[:3]})
    return hits


PLANT_BAD = '''
SELF_DIGEST_KEYS = ("sha256_without_hash_field", "sha256", "universe_sha256")

def f(d):
    return d.get("sha256")
'''
PLANT_GOOD = '''
SELF_DIGEST_KEYS = ("sha256_without_hash_field", "sha256", "universe_sha256")

def f(d):
    for k in SELF_DIGEST_KEYS:
        if k in d:
            return d[k]
'''
PLANT_GOOD2 = '''
def f(d):
    return d.get("sha256")
'''


def selftest() -> int:
    cases = [
        ("planted: list defined, one key hard-coded", PLANT_BAD, True),
        ("clean: iterates the list", PLANT_GOOD, False),
        ("clean: no canonical list exists", PLANT_GOOD2, False),
    ]
    ok = True
    print("  selftest -- planted-fault recall\n")
    for name, src, want in cases:
        got = bool(scan_text(src))
        good = got == want
        ok &= good
        print(f"    {name:44s} flagged={str(got):5s} want={str(want):5s} "
              f"{'PASS' if good else 'FAIL'}")
    print("""
  THE THIRD CASE IS THE SCOPE. `d.get("sha256")` is perfectly correct code when no
  canonical list exists to contradict it. The fault is not the single-key lookup; it is a
  single-key lookup living beside a list that says one key is not enough. Without the list
  there is nothing to shadow.

  ITS LIMIT: it cannot tell whether a hit is wrong. Code may legitimately mean one specific
  member of a canonical set. Every hit needs reading -- the value is that there are few.""")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    paths = [Path(p) for p in a.paths] if a.paths else sorted(
        list((ROOT / "scripts").glob("*.py")) + list((ROOT / "analysis").rglob("*.py")))
    total = 0
    for p in paths:
        if p.suffix != ".py" or not p.is_file():
            continue
        if p.resolve() == Path(__file__).resolve():
            # this file's PLANT_* fixtures contain a canonical list and a hard-coded
            # lookup, by construction. Flagging its own test data is noise -- the same
            # self-reference check_pattern_inversions needed.
            continue
        try:
            src = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = p.relative_to(ROOT).as_posix() if ROOT in p.parents else p.name
        for h in scan_text(src, rel):
            total += 1
            print(f"  {h['file']}:{h['line']}  {h['canonical_list']} lists "
                  f"{h['hard_coded']!r} among others")
            print(f"      hard-coded here; siblings ignored: {h['siblings']}")
    print(f"\n  {total} single-key lookups beside a canonical list")
    if total == 0:
        print("  (zero means nothing unless --selftest passes; run it)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
