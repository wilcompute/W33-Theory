"""Guard: an order matching a set size is not an action.

WARN-ONLY, like every guard here.

Coincidences nine and ten both died to one question, and it is mechanical:

    a group of order n acting REGULARLY on n points is TRANSITIVE,
    so if the n-set carries an invariant partition into UNEQUAL parts,
    no regular action exists and the two n's are different n's.

Pass 5639 killed |Rot(Q4)| = 192 = tomotope flags that way: the flags split 24+84+84.
Pass 5644 killed |Aut(16-face graph)| = 1152 = |W(F4)| a different way -- the orders
matched and the groups did not.  This guard reports the first kind and, when it can, the
divisibility test that also settles the second.

Two tests, both cheap:

  1. UNEQUAL PARTITION.  A certificate that records both `..order..: n` and a partition
     of n into unequal parts has refuted its own regular action.
  2. DIVISIBILITY.  Every orbit length of a group of order g divides g.  A certificate
     asserting a group of order g acts with an orbit of size m where m does not divide g
     has asserted something impossible.  Pass 5648 used exactly this: 84 does not divide
     576, so W(F4)/Z can never have the codec partition as orbits.

    py -3 scripts/check_transitivity.py --selftest
    py -3 scripts/check_transitivity.py data/YOUR_CERTIFICATE.json
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ORDER_KEY = re.compile(r"(order|aut|group_order|\|g\|)", re.I)
PART_KEY = re.compile(r"(orbit_sizes|orbits|block_sizes|partition|strata)", re.I)


def walk(doc):
    """Yield (key, value) for every scalar and list leaf under a nameable key."""
    def rec(o, key=""):
        if isinstance(o, dict):
            for k, v in o.items():
                yield from rec(v, k)
        elif isinstance(o, list):
            if o and all(isinstance(x, int) and not isinstance(x, bool) for x in o):
                yield key, o
            else:
                for x in o:
                    yield from rec(x, key)
        elif isinstance(o, int) and not isinstance(o, bool):
            yield key, o
    yield from rec(doc)


def findings(doc) -> list[str]:
    orders, parts = {}, []
    for k, v in walk(doc):
        if isinstance(v, int) and ORDER_KEY.search(k) and v > 1:
            orders[k] = v
        elif isinstance(v, list) and PART_KEY.search(k) and len(v) > 1:
            parts.append((k, v))
    out = []
    for pk, pv in parts:
        total, uneq = sum(pv), len(set(pv)) > 1
        for ok, ov in orders.items():
            if ov == total and uneq:
                out.append(f"{ok}={ov} matches sum({pk})={total}, but {pk}={pv} is "
                           f"UNEQUAL -- no regular action; the two {ov}s differ")
            if ov != total:
                bad = sorted({m for m in pv if m > 1 and ov % m})
                if bad:
                    out.append(f"{ok}={ov} cannot have orbit(s) {bad} in {pk} -- "
                               f"orbit lengths must divide the group order")
    return out


def selftest() -> int:
    cases = [
        ("coincidence nine (192 flags, 24+84+84)",
         {"rot_q4_order": 192, "orbit_sizes": [24, 84, 84]}, True),
        ("a genuine regular action (two equal orbits)",
         {"group_order": 192, "orbit_sizes": [96, 96]}, False),
        ("Pass 5648: 84 does not divide 576",
         {"aut_order": 576, "orbit_sizes": [24, 84, 84]}, True),
        ("unequal partition summing to a matching order",
         {"aut_order": 576, "orbit_sizes": [64, 512]}, True),
        ("clean: equal orbits, each dividing the order",
         {"aut_order": 576, "orbit_sizes": [288, 288]}, False),
        ("no partition recorded at all",
         {"aut_order": 1152, "flags": 1152}, False),
    ]
    ok = True
    print("  selftest -- unequal-partition and divisibility tests\n")
    for name, doc, want in cases:
        got = bool(findings(doc))
        ok &= got == want
        print(f"    {name:44s} got={str(got):5s} want={str(want):5s} "
              f"{'ok' if got == want else 'FAIL'}")
    print(f"""
  NOTE THE FOURTH AND FIFTH CASES. [64, 512] divides 576 on both parts, but it is UNEQUAL
  and sums to a matching order, so no regular action exists and it IS a finding; [288,
  288] is equal and clean. And note the last: a bare order/size match with no orbit data is NOT reported, because this
  guard tests actions, and no partition means no action was claimed. Reporting it would
  reproduce the near-universal firing rate that made the certificate guard useless
  (Pass 5635: 70%, moved 2 certificates of 5,056 by blocklist).""")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    total = 0
    files = [Path(a) for a in argv if not a.startswith("-")]
    for f in files:
        if not f.is_file() or f.suffix != ".json":
            continue
        try:
            doc = json.loads(f.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        for msg in findings(doc):
            total += 1
            print(f"  {f.name}\n      {msg}")
    print(f"\n  {total} transitivity finding(s) in {len(files)} certificate(s)")
    if total:
        print("""
  CANDIDATES. Exhibit the action or accept that the two n's are different n's.
  Coincidences nine and ten both ended here.""")
    print("  (zero means nothing unless --selftest passes; run it)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
