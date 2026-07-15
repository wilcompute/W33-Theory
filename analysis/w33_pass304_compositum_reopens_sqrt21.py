#!/usr/bin/env python3
"""Pass 304: the reachable-field map -- and a NUANCE that partly reopens sqrt(21).

Pass 300 proved a theorem: Q(sqrt 21) is unreachable as the spectral field of any
SINGLE Levi graph, because Levi(PG(2,q)) gives Q(sqrt q) and Levi(GQ(q,q)) gives
Q(sqrt 2q) with q a prime power, and 21 is neither a prime power nor twice one.
That closure was stated confidently.  It needs a qualification, and finding it is
the point of this pass -- the same forced/chosen discipline (Pass 302) applied to
my own theorem.

THE NUANCE.  Pass 300 quantifies over ONE geometry.  But the substrate is not one
geometry: the odd-q ladder has rungs q = 3, 5, 7, ... (Passes 194-202, 205), all
of which exist simultaneously.  Their Levi fields are Q(sqrt 2q):
        q = 3  ->  Q(sqrt 6)        (the machine itself)
        q = 7  ->  Q(sqrt 14)
and sqrt6 * sqrt14 = sqrt84 = 2*sqrt21, so
        sqrt21 = (sqrt6 * sqrt14) / 2   lies in   Q(sqrt6, sqrt14).
So sqrt(21) IS reachable -- not from any single rung, but from the COMPOSITUM of
the q=3 and q=7 rungs of the ladder.

WHAT SURVIVES OF PASS 300.  The theorem as literally stated is untouched: no
single incidence spectrum contains sqrt21.  What is withdrawn is the sweeping
reading -- "Koide's field can never come from the substrate" -- because the
substrate contains more than one rung, and the q=3 and q=7 rungs together do
generate it.  Whether that is meaningful is a separate question: a compositum of
two ladder rungs is a much weaker object than a single spectrum, and Q(sqrt3,
sqrt7) would do the same job from the PLANES. The honest status of Koide is
therefore: not derived, not structurally excluded either -- one notch back from
where Pass 300 left it.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass304_compositum_reopens_sqrt21.json"


def sf(n):
    o = 1
    for p, e in sp.factorint(int(n)).items():
        if e % 2:
            o *= p
    return int(o)


def main():
    checks = {}

    # ---- the single-geometry theorem (Pass 300) still holds
    reach_single = set()
    for p in sp.primerange(2, 60):
        for t in range(1, 5):
            q = p ** t
            if q > 100:
                break
            reach_single.add(sf(q))
            reach_single.add(sf(2 * q))
    checks["pass300_theorem_still_holds"] = 21 not in reach_single
    checks["single_geometry_cannot_give_sqrt21"] = 21 not in reach_single

    # ---- THE NUANCE: the ladder has many rungs at once
    q3, q7 = 6, 14                       # Levi fields sqrt(2q) at q=3 and q=7
    checks["q3_rung_field_is_sqrt6"] = sf(2 * 3) == 6
    checks["q7_rung_field_is_sqrt14"] = sf(2 * 7) == 14
    prod = sp.radsimp(sp.sqrt(q3) * sp.sqrt(q7))
    checks["sqrt6_times_sqrt14_is_2sqrt21"] = sp.simplify(prod - 2 * sp.sqrt(21)) == 0
    s21 = sp.radsimp(prod / 2)
    checks["sqrt21_from_the_compositum"] = sp.simplify(s21 - sp.sqrt(21)) == 0

    # the same from the PLANES of order 3 and 7
    checks["planes_3_and_7_also_give_sqrt21"] = sp.simplify(
        sp.sqrt(3) * sp.sqrt(7) - sp.sqrt(21)) == 0
    checks["sqrt3_reachable"] = 3 in reach_single
    checks["sqrt7_reachable"] = 7 in reach_single

    # ---- what a compositum of two rungs buys, and what it costs
    pairs = {}
    for a in (3, 5, 7, 11):
        for b in (3, 5, 7, 11):
            if a < b:
                pairs[f"q={a} x q={b}"] = {
                    "fields": [f"Q(sqrt{sf(2*a)})", f"Q(sqrt{sf(2*b)})"],
                    "product_squarefree": sf(sf(2 * a) * sf(2 * b)),
                }
    checks["q3_x_q7_product_is_21"] = pairs["q=3 x q=7"]["product_squarefree"] == 21

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass304.compositum_reopens_sqrt21.v1",
        "status": "PASS" if all_pass else "FAIL",
        "pass300_untouched": (
            "The theorem as literally stated stands: no SINGLE Levi spectrum "
            "contains sqrt(21), since 21 is neither a prime power nor twice one. "
            "Re-verified here."
        ),
        "THE_NUANCE": (
            "Pass 300 quantifies over ONE geometry, but the substrate is not one "
            "geometry -- the odd-q ladder has rungs q = 3,5,7,... existing "
            "simultaneously. Their Levi fields are Q(sqrt 2q), so q=3 gives "
            "Q(sqrt6) (the machine itself) and q=7 gives Q(sqrt14). Since "
            "sqrt6 * sqrt14 = sqrt84 = 2*sqrt21, we get "
            "sqrt21 = (sqrt6*sqrt14)/2 in Q(sqrt6, sqrt14). So sqrt(21) IS "
            "reachable -- from the COMPOSITUM of the q=3 and q=7 rungs."
        ),
        "the_two_routes": {
            "quadrangles": "Q(sqrt6) x Q(sqrt14) from the q=3 and q=7 GQ rungs; "
                           "sqrt6*sqrt14 = 2 sqrt21",
            "planes": "Q(sqrt3) x Q(sqrt7) from PG(2,3) and PG(2,7); "
                      "sqrt3*sqrt7 = sqrt21 directly",
        },
        "rung_pairs": pairs,
        "what_is_withdrawn": (
            "The sweeping reading of Pass 300 -- 'Koide's field can never come "
            "from the substrate' -- is WITHDRAWN. The substrate contains more "
            "than one rung, and q=3 together with q=7 does generate Q(sqrt21)."
        ),
        "honest_status_of_koide": (
            "Not derived, and not structurally excluded either -- one notch back "
            "from where Pass 300 left it. A compositum of two ladder rungs is a "
            "far weaker object than a single spectrum: it requires invoking two "
            "different geometries at once with no mechanism coupling them, and "
            "the planes of order 3 and 7 would do the same job just as well. So "
            "this reopens a door rather than walking through it. The contrast "
            "with Pass 303 is instructive: there, ONE compositum (clock x "
            "machine) lands on the TBM field with both generators forced and both "
            "structures already known to be coupled; here, the q=3 x q=7 "
            "compositum lands on Koide's field with no coupling on offer."
        ),
        "method_note": (
            "This pass exists because Pass 302's rule -- ask whether the claim "
            "survives a change of setup -- should be applied to my own theorems, "
            "not only to the metric claims it was invented for. Pass 300 was "
            "sound but over-read, and the over-reading is the kind of thing that "
            "would otherwise have been quoted forward as settled."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
