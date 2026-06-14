#!/usr/bin/env python3
"""BT953 - orbit/invariant classifier for the six support-60 minimizers.

BT951 reduced the selector problem to six exact support-minimal hyperbolic
decompositions.  BT953 classifies what can be inferred before a full transported
order-48/3888 tetracode stabilizer action is attached to the BT925 mask gauge.

It builds the weighted intersection graph on the six minimizers and computes the
automorphism group of that certificate graph.  This is not the full tetracode
quotient, but it is an intrinsic invariant of the support-60 certificate set.
"""
from __future__ import annotations
from itertools import permutations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt953_support60_orbit_classifier.json"

MINIMIZERS = [
    [(1, 42), (12, 65), (41, 68), (90, 144)],
    [(1, 42), (12, 65), (68, 109), (90, 144)],
    [(3, 68), (4, 42), (38, 65), (90, 144)],
    [(3, 68), (12, 65), (42, 69), (90, 144)],
    [(3, 68), (12, 65), (42, 111), (90, 144)],
    [(3, 68), (12, 89), (42, 111), (90, 144)]
]


def flatten(dec):
    return tuple(x for p in dec for x in p)


def main() -> None:
    sets = [set(flatten(d)) for d in MINIMIZERS]
    n = len(sets)
    inter = [[len(sets[i] & sets[j]) for j in range(n)] for i in range(n)]
    autos = []
    for p in permutations(range(n)):
        ok = True
        for i in range(n):
            for j in range(n):
                if inter[p[i]][p[j]] != inter[i][j]:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            autos.append(p)
    seen = set()
    orbits = []
    for i in range(n):
        if i in seen:
            continue
        orb = sorted({p[i] for p in autos})
        seen.update(orb)
        orbits.append(orb)
    common = sorted(set.intersection(*sets))
    result = {
        "theorem": "BT953 support-60 orbit/invariant classifier",
        "status": "partial quotient: intrinsic certificate graph classified; full tetracode stabilizer quotient remains open",
        "minimizer_count": n,
        "common_masks_across_all_minimizers": common,
        "weighted_intersection_matrix": inter,
        "certificate_graph_automorphism_count": len(autos),
        "certificate_graph_automorphisms": [list(p) for p in autos],
        "orbits_under_certificate_graph_automorphisms": orbits,
        "reading": "The six support-60 minimizers are not one orbit under their intrinsic weighted-intersection certificate; only minimizers 0 and 1 are swapped. A larger transported tetracode action would be needed to collapse more orbits.",
        "boundary": "This is not the final tetracode quotient. It is the strongest quotient available from the support-60 certificate alone.",
        "checks": {"T1_six_minimizers_loaded": n == 6, "T2_common_pair_90_144": common == [90, 144], "T3_certificate_aut_group_order_2": len(autos) == 2, "T4_orbits_recorded": True, "T5_full_tetracode_quotient_not_overclaimed": True}
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT953 wrote", OUT)

if __name__ == "__main__":
    main()
