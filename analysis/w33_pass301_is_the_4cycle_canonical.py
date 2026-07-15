#!/usr/bin/env python3
"""Pass 301: is the sqrt(21) 4-cycle canonical under Aut(Csaszar)?

Pass 294 found the four sqrt(21) Szilassi edges dualize to the 4-cycle
0-1-2-5-0 in the Csaszar K7 skeleton.  Since that skeleton is COMPLETE, every
vertex pair is an edge, so a 4-cycle can only be distinguished by how it sits in
the TRIANGULATION.  This witness computes the combinatorial automorphism group of
the Csaszar map (the 14-triangle torus triangulation on 7 vertices) by brute
force over S_7, and measures the orbit of that 4-cycle among all 105 four-cycles
of K7.

The honest framing matters here.  Passes 293/299 showed the sqrt(21) edges were
singled out by a coordinate accident, so any combinatorial distinction they carry
was found by an accident and may reflect nothing.  A small automorphism group
also makes almost ANY object land in a proper orbit, so "distinguished" is cheap.
We therefore report the orbit size as a number rather than a verdict.
"""

from __future__ import annotations

from itertools import combinations, permutations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass301_is_the_4cycle_canonical.json"

CS_FACES = [[0, 1, 2], [0, 2, 5], [0, 5, 4], [0, 4, 6], [0, 6, 3], [0, 3, 1],
            [1, 3, 4], [1, 4, 5], [1, 5, 6], [1, 6, 2], [2, 6, 4], [2, 4, 3],
            [2, 3, 5], [5, 3, 6]]
CYCLE = [(0, 1), (0, 5), (1, 2), (2, 5)]


def canon(faces):
    return frozenset(frozenset(f) for f in faces)


def main():
    checks = {}
    F0 = canon(CS_FACES)
    checks["csaszar_has_14_faces"] = len(F0) == 14

    E = set()
    for f in CS_FACES:
        for i in range(3):
            E.add(tuple(sorted((f[i], f[(i + 1) % 3]))))
    checks["skeleton_is_K7_21_edges"] = len(E) == 21

    aut = [p for p in permutations(range(7))
           if canon([[p[v] for v in f] for f in CS_FACES]) == F0]
    order = len(aut)
    checks["aut_nonempty"] = order > 0
    checks["identity_is_in_aut"] = tuple(range(7)) in aut

    orbit = {frozenset(frozenset((p[a], p[b])) for a, b in CYCLE) for p in aut}

    all_4cycles = set()
    for quad in combinations(range(7), 4):
        a, b, c, d = quad
        for w, x, y, z in ((a, b, c, d), (a, b, d, c), (a, c, b, d)):
            all_4cycles.add(frozenset([frozenset((w, x)), frozenset((x, y)),
                                       frozenset((y, z)), frozenset((z, w))]))
    checks["k7_has_105_four_cycles"] = len(all_4cycles) == 105
    checks["the_cycle_is_a_k7_4cycle"] = (
        frozenset(frozenset(e) for e in CYCLE) in all_4cycles)

    frac = len(orbit) / len(all_4cycles)
    distinguished = len(orbit) < len(all_4cycles)
    checks["orbit_is_proper_subset"] = bool(distinguished)
    # an orbit can never exceed |Aut|
    checks["orbit_bounded_by_aut_order"] = len(orbit) <= order

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass301.is_the_4cycle_canonical.v1",
        "status": "PASS" if all_pass else "FAIL",
        "aut_csaszar_order": order,
        "the_4cycle": [list(e) for e in CYCLE],
        "orbit_size": len(orbit),
        "total_4cycles_in_K7": len(all_4cycles),
        "orbit_fraction": round(frac, 4),
        "measurement": (
            "Aut(Csaszar) has order %d. The sqrt(21) 4-cycle 0-1-2-5-0 has an "
            "orbit of size %d among the %d four-cycles of K7 (%.1f%%)."
            % (order, len(orbit), len(all_4cycles), 100 * frac)
        ),
        "honest_reading": (
            "The orbit is a proper subset, so the cycle is 'distinguished' in the "
            "literal sense that Aut does not move it everywhere. But that is "
            "cheap: with |Aut| = %d the orbit CANNOT exceed %d, so essentially "
            "every 4-cycle lies in a small proper orbit and the label carries "
            "almost no information. Combined with Passes 293/299 -- which showed "
            "the sqrt(21) edges were selected by a coordinate accident rather "
            "than by structure -- the fair conclusion is that this 4-cycle names "
            "nothing established. It is reported as a measurement, not a finding."
            % (order, order)
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
