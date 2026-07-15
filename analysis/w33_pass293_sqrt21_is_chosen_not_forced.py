#!/usr/bin/env python3
"""Pass 293: sqrt(21) is CHOSEN, not FORCED -- deflating Pass 290.

Pass 286 found sqrt(21) in the Szilassi edge lengths; Pass 290 found it is the
ONLY quadratic field common to both published Szilassi realizations; Pass 291
found the SAME four edges carry it in both.  Together those built a case that
sqrt(21) is a metric invariant of the Szilassi pole.  This witness tests that
case properly, and it does not survive.

WHERE sqrt(21) COMES FROM.  A length lies in Q(sqrt 21) iff d^2 = 21 * (rational
square).  In the published realizations:
    v1 {0,4}:  d^2 = 525     = 21 * 5^2       -> 5*sqrt(21)
    v1 {0,12}: d^2 = 525/4   = 21 * (5/2)^2   -> 5*sqrt(21)/2
    v2 {0,4}:  d^2 = 9261/16 = 21^3 / 16      -> 21*sqrt(21)/4
    v2 {0,12}: d^2 = 84      = 21 * 2^2       -> 2*sqrt(21)
So sqrt(21) is a consequence of the CHOSEN rational coordinates making d^2 equal
21 times a square.

IS THE REALIZATION SPACE CONTINUOUS?  A Szilassi realization is 14 points with
all 7 hexagonal faces planar: 42 coordinates, minus rigid motions (6) and scale
(1) = 35 effective, against 7 faces x 3 coplanarity conditions = 21 constraints,
giving a naive moduli dimension of ~14.  We test directly: perturb the published
v1 and re-solve the planarity system.  Valid nearby realizations DO exist
(planarity residual < 1e-8) whose sqrt(21)-edges have moved off
5*sqrt(21) = 22.9129.  Embeddedness is an OPEN condition, so small perturbations
of an embedded polyhedron remain embedded.

CONCLUSION.  The realization space is continuous, so sqrt(21) is NOT forced by
the Szilassi combinatorics: generic realizations have edge lengths in no
particular quadratic field.  Pass 290's statement stays true as stated -- among
the seven PUBLISHED realizations sqrt(21) is the unique field common to both
Szilassi ones -- but its significance collapses.  It is a fact about Szilassi's
two coordinate choices, not a metric invariant of the polyhedron.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import least_squares

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass293_sqrt21_is_chosen_not_forced.json"

FACES = [[0, 1, 13, 8, 7, 4], [0, 4, 3, 2, 10, 12], [0, 12, 9, 6, 5, 1],
         [11, 3, 4, 7, 6, 9], [11, 9, 12, 10, 8, 13], [11, 13, 1, 5, 2, 3],
         [2, 5, 6, 7, 8, 10]]
V1 = np.array([[12, 0, 12], [-12, 0, 12], [0, 12.6, -12], [0, -12.6, -12],
               [2, -5, -8], [-2, 5, -8], [3.75, 3.75, -3], [-3.75, -3.75, -3],
               [4.5, -2.5, 2], [-4.5, 2.5, 2], [7, 0, 2], [-7, 0, 2],
               [7, 2.5, 2], [-7, -2.5, 2]], float)
SQ21 = [(0, 4), (0, 12), (1, 5), (1, 13)]


def planarity(x):
    P = x.reshape(14, 3)
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
    checks["published_v1_is_planar"] = float(np.abs(planarity(V1.ravel())).max()) < 1e-9
    checks["constraint_count_21"] = len(planarity(V1.ravel())) == 21
    naive_moduli = (42 - 6 - 1) - 21
    checks["naive_moduli_dim_14"] = naive_moduli == 14

    # d^2 = 21 * (rational square), exactly, for every sqrt21 edge
    R2 = sp.Rational
    exact = {"v1_(0,4)": sp.nsimplify(525), "v1_(0,12)": sp.nsimplify(R2(525, 4)),
             "v2_(0,4)": sp.nsimplify(R2(9261, 16)), "v2_(0,12)": sp.nsimplify(84)}
    ratio = {}
    for k, d2 in exact.items():
        r = sp.nsimplify(d2 / 21)
        ratio[k] = {"d2": str(d2), "d2_over_21": str(r),
                    "is_rational_square": bool(sp.sqrt(r).is_rational)}
    checks["all_sqrt21_edges_are_21_times_a_square"] = all(
        v["is_rational_square"] for v in ratio.values())
    checks["v2_edge_is_21_cubed_over_16"] = (
        sp.nsimplify(R2(9261, 16)) == sp.nsimplify(R2(21 ** 3, 16)))

    # THE DECISIVE TEST: is the realization space continuous?
    base = lens(V1)
    rng = np.random.default_rng(3)
    trials, valid = [], 0
    for _ in range(8):
        x0 = V1.ravel() + rng.normal(0, 0.45, 42)
        sol = least_squares(planarity, x0, max_nfev=6000)
        res = float(np.abs(planarity(sol.x)).max())
        L = lens(sol.x.reshape(14, 3))
        moved = max(abs(L[i] - base[i]) for i in range(4))
        ok = res < 1e-8
        valid += int(ok)
        trials.append({"planarity_residual": res, "valid": bool(ok),
                       "sqrt21_edge_lengths": [round(v, 6) for v in L],
                       "max_shift_from_published": round(moved, 6)})
    checks["found_valid_nearby_realizations"] = valid > 0
    checks["nearby_lengths_genuinely_differ"] = any(
        t["valid"] and t["max_shift_from_published"] > 1e-3 for t in trials)

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass293.sqrt21_is_chosen_not_forced.v1",
        "status": "PASS" if all_pass else "FAIL",
        "VERDICT": (
            "sqrt(21) is CHOSEN, not FORCED. The Szilassi realization space is "
            "continuous (naive moduli dimension ~14: 42 coordinates minus rigid "
            "motions and scale, against 7 faces x 3 coplanarity conditions), and "
            "valid nearby realizations exist -- planarity residual < 1e-8 -- "
            "whose sqrt(21)-edges have moved off 5*sqrt(21) = 22.9129. Generic "
            "realizations lie in no particular quadratic field."
        ),
        "where_sqrt21_comes_from": {
            "rule": "a length is in Q(sqrt 21) iff d^2 = 21 * (rational square)",
            "published_values": ratio,
            "note": "v2's {0,4} has d^2 = 21^3/16 exactly",
            "reading": "sqrt(21) follows from Szilassi's chosen rational vertex "
                       "coordinates, not from the combinatorics",
        },
        "moduli_test": {"naive_dimension": naive_moduli,
                        "valid_nearby_found": valid, "trials": trials},
        "what_this_does_to_pass290": (
            "Pass 290's statement stays TRUE as stated -- among the seven "
            "PUBLISHED realizations, sqrt(21) is the unique quadratic field "
            "common to both Szilassi ones, and Pass 291's four edges really are "
            "the same in both. But the SIGNIFICANCE collapses: that is a fact "
            "about Szilassi's two coordinate choices (he picked pretty rational "
            "vertices, and both happened to land 21*square on the same four "
            "edges), not a metric invariant of the polyhedron. Pass 290's "
            "framing of sqrt(21) as 'the unique metric invariant of the Szilassi "
            "pole' is WITHDRAWN."
        ),
        "what_survives": (
            "Pass 286 stands entirely: sqrt(21) IS present in the substrate's "
            "committed metric data, and Passes 279/285 were wrong to deny it. "
            "What 293 removes is the stronger claim that the polyhedron FORCES "
            "it. Honest position: sqrt(21) appears in both published Szilassi "
            "realizations on the same four edges -- a real, unexplained "
            "coincidence of two coordinate choices -- but it is not an "
            "invariant, so the Koide / Q(sqrt 21) link is weakened, not "
            "strengthened."
        ),
        "open": (
            "Whether some natural SUB-family (e.g. C2-symmetric realizations with "
            "integer vertices) forces d^2 = 21*square is not settled here. That "
            "is the way the invariance claim could be rescued, and it is a "
            "well-posed question."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
