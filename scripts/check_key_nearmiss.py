#!/usr/bin/env python3
"""Report when a certificate introduces a key name that near-misses an existing one.

WHY THIS EXISTS, and why the obvious alternative does not.  Pass 5557 mined this
corpus and found 26,693 distinct integer-valued key names: `order` occurs in 1,391 of
them, `dim` in 1,238, `rank` in 1,011.  Pass 5556 added a 13-entry alias table to
canonicalise a few, and Pass 5558 measured that against those thousands and concluded
it cannot scale -- an alias repairs a collision somebody already found, which by then
has already cost whatever it was going to cost.

So the direction is reversed here.  Instead of translating old names together, this
flags a NEW name that is one small edit from a name the corpus already uses, at the
moment it is introduced, while renaming it is still free.  `alpha_exact` against an
existing `alpha` is the case that cost six passes; it is a prefix match.

METHOD, deliberately cheap: for each integer-valued key in a staged certificate that
the corpus has never seen, look for existing keys that share its stem, are a prefix or
suffix of it, or differ by one token.  Report those.  No edit distance over 26,693
names -- that is O(n) per key and the stem index is O(1).

    py -3 scripts/check_key_nearmiss.py <certificates>
    py -3 scripts/check_key_nearmiss.py --selftest
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SKIP = {"pass", "passes", "schema", "status", "date", "version", "seed", "n", "id"}


def int_keys(doc) -> set[str]:
    """Every key name in `doc` whose leaf value is an integer."""
    out: set[str] = set()

    def walk(o, pre=""):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, k)
        elif isinstance(o, list):
            for v in o:
                walk(v, pre)
        elif isinstance(o, bool):
            return
        elif isinstance(o, int) and pre:
            k = pre.lower()
            if len(k) >= 4 and k not in SKIP:
                out.add(k)

    walk(doc)
    return out


def corpus_keys(exclude: set[str] | None = None) -> set[str]:
    exclude = exclude or set()
    seen: set[str] = set()
    for p in sorted(DATA.glob("*.json")):
        if p.name in exclude:
            continue
        try:
            seen |= int_keys(json.loads(p.read_text(encoding="utf-8",
                                                    errors="replace")))
        except Exception:
            continue
    return seen


def near_misses(new: str, known: set[str], stems: dict[str, set[str]]) -> list[str]:
    """Existing keys one small edit from `new`: prefix, suffix, or one token apart."""
    out: set[str] = set()
    toks = [t for t in re.split(r"[_\W]+", new) if t]
    for t in toks:
        for cand in stems.get(t, ()):
            if cand == new:
                continue
            ct = [x for x in re.split(r"[_\W]+", cand) if x]
            if cand.startswith(new) or new.startswith(cand):
                out.add(cand)
            elif cand.endswith(new) or new.endswith(cand):
                out.add(cand)
            elif len(set(toks) ^ set(ct)) <= 1:
                out.add(cand)
    return sorted(out)[:6]


def build_stems(known: set[str]) -> dict[str, set[str]]:
    stems: dict[str, set[str]] = defaultdict(set)
    for k in known:
        for t in re.split(r"[_\W]+", k):
            if len(t) >= 4:
                stems[t].add(k)
    return stems


def selftest() -> int:
    known = {"alpha", "hoffman", "aut_order", "orbit_sizes", "deficit"}
    stems = build_stems(known)
    cases = [
        ("alpha_exact near-misses alpha", "alpha_exact", "alpha", True),
        ("hoffman_bound near-misses hoffman", "hoffman_bound", "hoffman", True),
        ("orbit_size near-misses orbit_sizes", "orbit_size", "orbit_sizes", True),
        ("unrelated key reports nothing", "genus", None, False),
    ]
    ok = True
    print("  selftest -- near-miss detection\n")
    for name, new, want, should in cases:
        hits = near_misses(new, known, stems)
        got = bool(hits)
        good = got == should and (want in hits if should else True)
        ok &= good
        print(f"    {name:38s} -> {hits if hits else '(none)'}   "
              f"{'PASS' if good else 'FAIL'}")
    print("""
  THE UNRELATED CASE IS THE CALIBRATION. A key sharing no stem with anything must report
  nothing, or every new certificate drowns in suggestions and the tool is switched off. The
  three positives are the three shapes that actually occur here: a suffix added
  (alpha -> alpha_exact), a qualifier added (hoffman -> hoffman_bound), and a plural
  (orbit_size -> orbit_sizes).

  ITS LIMIT: stems of four characters or more. `q` and `mu` and `k` are invisible, and two
  authors who both invent a short name for one quantity will not be caught. That is the same
  floor the rediscovery guard has, for the same reason -- short tokens are everywhere.""")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    files = [Path(a) for a in argv if not a.startswith("-") and a.endswith(".json")]
    if not files:
        print("  no certificates given")
        return 0
    known = corpus_keys(exclude={f.name for f in files})
    stems = build_stems(known)
    total = 0
    for f in files:
        if not f.is_file():
            continue
        try:
            doc = json.loads(f.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        for k in sorted(int_keys(doc) - known):
            hits = near_misses(k, known, stems)
            if hits:
                total += 1
                print(f"  {f.name}\n      new key `{k}` near-misses: "
                      f"{', '.join('`' + h + '`' for h in hits)}")
    print(f"\n  {total} near-miss key name(s) over {len(files)} certificate(s)")
    if total:
        print("""
  Renaming a key before the certificate is committed costs nothing. Pass 4800's `alpha` and
  BT818's `alpha_exact` are one such pair, and keeping them apart cost six passes.""")
    print("  (zero means nothing unless --selftest passes; run it)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
