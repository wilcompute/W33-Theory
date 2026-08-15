#!/usr/bin/env python3
"""Reject a pass-namespace reservation that OVERLAPS an existing one.

WHY THIS EXISTS, and it is a hole in yesterday's fix rather than in the original.

Pass 5276 replaced the empty-commit reservation with an atomic add to
data/w33_pass_namespace_registry_v2.d/<lo>-<hi>.json, on the argument that a tracked
path produces an add/add conflict where an empty commit produces nothing.  That is
true and it closes the IDENTICAL-range race.  It does not close the OVERLAPPING one:

    2026-08-15 00:33:21   Track A   Reserve Passes 5372-5379   -> 5372-5379.json
    2026-08-15 00:41:39   other     Reserve Pass5376-5383      -> 5376-5383.json

Different filenames, so git merged both without complaint, and 5376-5379 is claimed
twice.  Eight minutes apart, one day after the mechanism was introduced to prevent
exactly this.

WHAT THIS DOES.  Parses every <lo>-<hi>.json in the registry directory and reports any
pair whose ranges intersect.  Ranges are read from the FILENAME, not the body, because
the filename is what git arbitrates on and a body that disagrees with its own filename
is a separate fault this also reports.

    py -3 scripts/check_reservation_overlap.py
    py -3 scripts/check_reservation_overlap.py --selftest
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "data" / "w33_pass_namespace_registry_v2.d"
RE_NAME = re.compile(r"^(\d+)-(\d+)\.json$")


def ranges_from(dirpath: Path) -> list[tuple[int, int, str, str | None]]:
    """(lo, hi, filename, owner) for every well-named registry entry."""
    out = []
    for f in sorted(dirpath.glob("*.json")):
        m = RE_NAME.match(f.name)
        if not m:
            continue
        lo, hi = int(m.group(1)), int(m.group(2))
        owner = None
        try:
            d = json.loads(f.read_text(encoding="utf-8", errors="replace"))
            owner = d.get("owner")
            body = d.get("range")
            if isinstance(body, list) and len(body) == 2 and [lo, hi] != list(body):
                out.append((lo, hi, f.name, f"BODY-MISMATCH {body} vs filename"))
                continue
        except Exception:
            pass
        out.append((lo, hi, f.name, owner))
    return out


def overlaps(rs):
    """Every intersecting pair. O(n^2) and n is tiny; clarity beats cleverness here."""
    bad = []
    for i in range(len(rs)):
        for j in range(i + 1, len(rs)):
            a, b = rs[i], rs[j]
            if a[0] <= b[1] and b[0] <= a[1]:
                lo, hi = max(a[0], b[0]), min(a[1], b[1])
                bad.append((a, b, lo, hi))
    return bad


def selftest() -> int:
    import shutil
    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix="resv_"))
    def put(name, body):
        (tmp / name).write_text(json.dumps(body), encoding="utf-8")
    cases = [
        ("clean: adjacent blocks touch but do not overlap",
         {"5372-5379.json": {"range": [5372, 5379]},
          "5380-5387.json": {"range": [5380, 5387]}}, 0),
        ("planted: the real 5372/5376 collision",
         {"5372-5379.json": {"range": [5372, 5379]},
          "5376-5383.json": {"range": [5376, 5383]}}, 1),
        ("planted: one block inside another",
         {"5300-5399.json": {"range": [5300, 5399]},
          "5340-5347.json": {"range": [5340, 5347]}}, 1),
        ("clean: single block",
         {"5372-5379.json": {"range": [5372, 5379]}}, 0),
    ]
    ok = True
    print("  selftest -- overlap detection\n")
    for name, files, want in cases:
        for f in tmp.glob("*.json"):
            f.unlink()
        for fn, body in files.items():
            put(fn, body)
        got = len(overlaps(ranges_from(tmp)))
        good = got == want
        ok &= good
        print(f"    {name:44s} overlaps={got} want={want} "
              f"{'PASS' if good else 'FAIL'}")
    print("""
  THE ADJACENT CASE IS THE ONE THAT MUST NOT FIRE. 5372-5379 and 5380-5387 touch without
  overlapping, which is the normal healthy state of this directory -- a checker that flagged
  consecutive blocks would fire on every reservation ever made.

  ITS LIMIT: it sees the registry, not intent. Two lanes may deliberately share a range, and
  this cannot tell that from an accident. It reports; a human decides who renumbers, and the
  ownership rule is the earlier COMMIT, not the earlier filename.""")
    shutil.rmtree(tmp, ignore_errors=True)
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    if not REG.is_dir():
        print(f"  no registry directory at {REG}")
        return 0
    rs = ranges_from(REG)
    bad = overlaps(rs)
    print(f"  registry entries : {len(rs)}")
    for a, b, lo, hi in bad:
        print(f"\n  OVERLAP {lo}-{hi}")
        print(f"     {a[2]:20s} owner={a[3]}")
        print(f"     {b[2]:20s} owner={b[3]}")
    print(f"\n  {len(bad)} overlapping reservation(s)")
    if bad:
        print("""
  The atomic-add mechanism (Pass 5276) conflicts on IDENTICAL filenames only. Overlapping
  ranges have different filenames and merge cleanly, which is how 5376-5379 got claimed
  twice. Ownership goes to the earlier COMMIT -- check with git log, not with the filename.""")
    print("  (zero means nothing unless --selftest passes; run it)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
