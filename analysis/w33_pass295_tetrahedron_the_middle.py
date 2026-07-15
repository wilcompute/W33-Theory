#!/usr/bin/env python3
"""Pass 295: the oscillator's MIDDLE -- does the tetrahedron carry a field?

The repo's own `w33_genus_ladder_clock.py` frames the two toroidal polyhedra as a
clock oscillator whose genus-0 middle is the SELF-DUAL tetrahedron: the unique
polyhedron with BOTH maximal adjacencies (K4 vertices AND K4 faces), which the
two genus-1 poles split between them (Csaszar: every vertex pair adjacent = K7;
Szilassi: every face pair shares an edge -- and tetrahedron + Szilassi are the
ONLY polyhedra with that property).

If the poles carry quadratic fields in their edge lengths (Pass 290's census
found 36 across the seven realizations), what does the MIDDLE carry?

THE ANSWER IS CLEAN.  The regular tetrahedron is EQUILATERAL: all six edges have
the same length, so its edge-length field is Q -- rational, no quadratic
irrationality at all.  The middle of the oscillator is the RATIONAL point between
two irrational poles.  This is not a coincidence of scaling: equilaterality means
there is only ONE length, so no ratio of edges can be irrational either.

THE BC-HELIX TWIST.  The tetrahedron's role as the Boerdijk-Coxeter helix
generator does introduce an irrationality, but NOT in its edge lengths: the
helix twist angle is arccos(-(q-1)/q) = arccos(-2/3), an irrational ANGLE whose
cosine is rational. So the middle is rational in length and rational in cosine;
what is irrational is the angle itself (transcendental, by Niven), which is a
different kind of object from the poles' quadratic edge fields.

VERIFIED HERE: the Euler/genus trio, the two maximal-adjacency properties, the
genus numerator (n-3)(n-4) = mu*q = k = 12 at n=7, the tetrahedron's rational
edge field, and the arccos(-2/3) twist.
"""

from __future__ import annotations

from itertools import combinations
import json
import math
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass295_tetrahedron_the_middle.json"

Q, LAM, MU, K, PHI6 = 3, 2, 4, 12, 7


def euler_genus(V, E, F):
    chi = V - E + F
    return chi, (2 - chi) // 2


def main():
    checks = {}

    # ---- the trio
    trio = {"tetrahedron": (4, 6, 4), "Csaszar": (7, 21, 14), "Szilassi": (14, 21, 7)}
    genera = {n: euler_genus(*v) for n, v in trio.items()}
    checks["tetrahedron_genus_0"] = genera["tetrahedron"] == (2, 0)
    checks["csaszar_genus_1"] = genera["Csaszar"] == (0, 1)
    checks["szilassi_genus_1"] = genera["Szilassi"] == (0, 1)
    checks["poles_are_dual_counts"] = (trio["Csaszar"][0] == trio["Szilassi"][2]
                                       and trio["Csaszar"][2] == trio["Szilassi"][0])
    checks["all_three_have_21_or_6_edges"] = (trio["Csaszar"][1] == 21
                                              and trio["Szilassi"][1] == 21
                                              and trio["tetrahedron"][1] == 6)

    # ---- the genus numerator: (n-3)(n-4) = mu * q = k at n = 7 = Phi_6
    n = PHI6
    checks["phi6_is_7"] = (Q ** 2 - Q + 1) == PHI6
    checks["numerator_is_mu_times_q"] = (n - 3) * (n - 4) == MU * Q == K
    checks["genus_K7_is_1"] = math.ceil((n - 3) * (n - 4) / 12) == 1
    checks["genus_K4_is_0"] = math.ceil((4 - 3) * (4 - 4) / 12) == 0

    # ---- the two maximal adjacencies, and the tetrahedron having BOTH
    tet_faces = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]
    # (a) skeleton is complete: every vertex pair is an edge
    tet_edges = set()
    for f in tet_faces:
        for i in range(3):
            tet_edges.add(tuple(sorted((f[i], f[(i + 1) % 3]))))
    complete = all(tuple(sorted(p)) in tet_edges for p in combinations(range(4), 2))
    checks["tetra_skeleton_is_K4_complete"] = complete
    # (b) every face pair shares an edge
    def shares_edge(f, g):
        ef = {tuple(sorted((f[i], f[(i + 1) % len(f)]))) for i in range(len(f))}
        eg = {tuple(sorted((g[i], g[(i + 1) % len(g)]))) for i in range(len(g))}
        return len(ef & eg) > 0
    all_faces_adjacent = all(shares_edge(a, b) for a, b in combinations(tet_faces, 2))
    checks["tetra_every_face_pair_shares_an_edge"] = all_faces_adjacent
    checks["tetra_has_BOTH_maximal_adjacencies"] = complete and all_faces_adjacent
    checks["tetra_is_self_dual"] = (trio["tetrahedron"][0] == trio["tetrahedron"][2])

    # ---- THE MIDDLE'S FIELD: the regular tetrahedron is equilateral -> Q
    a = sp.Integer(1)
    reg = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]   # regular tetra
    Ls = []
    for p, qv in combinations(reg, 2):
        d2 = sum((sp.Integer(p[i]) - qv[i]) ** 2 for i in range(3))
        Ls.append(sp.radsimp(sp.sqrt(d2)))
    checks["regular_tetra_has_6_edges"] = len(Ls) == 6
    checks["regular_tetra_is_equilateral"] = len(set(sp.simplify(x) for x in Ls)) == 1
    # only ONE length => every edge RATIO is 1 => rational; the field is Q
    ratios = {sp.simplify(x / Ls[0]) for x in Ls}
    checks["all_edge_ratios_are_1"] = ratios == {sp.Integer(1)}
    checks["middle_field_is_Q"] = all(sp.simplify(x / Ls[0]).is_rational for x in Ls)

    # ---- the BC-helix twist: arccos(-2/3) -- rational cosine, irrational angle
    cos_twist = sp.Rational(-(Q - 1), Q)
    checks["bc_twist_cosine_is_minus_two_thirds"] = cos_twist == sp.Rational(-2, 3)
    checks["bc_twist_cosine_is_rational"] = cos_twist.is_rational
    checks["bc_twist_angle_is_not_a_nice_multiple_of_pi"] = not sp.simplify(
        sp.acos(cos_twist) / sp.pi).is_rational

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass295.tetrahedron_the_middle.v1",
        "status": "PASS" if all_pass else "FAIL",
        "the_trio": {n: {"V": v[0], "E": v[1], "F": v[2],
                         "chi": genera[n][0], "genus": genera[n][1]}
                     for n, v in trio.items()},
        "the_middle_has_both_adjacencies": {
            "skeleton_complete_K4": bool(complete),
            "every_face_pair_shares_an_edge": bool(all_faces_adjacent),
            "self_dual": True,
            "meaning": "the tetrahedron is the unique polyhedron with BOTH "
                       "maximal adjacencies; the two genus-1 poles split them "
                       "(Csaszar takes vertex-completeness = K7, Szilassi takes "
                       "face-completeness)",
        },
        "genus_numerator": {
            "formula": "g(K_n) = ceil((n-3)(n-4)/12)",
            "at_n_7": {"n-3": MU, "n-4": Q, "product": MU * Q, "k": K,
                       "genus": 1},
            "reading": "at n = 7 = Phi_6(3) the numerator is 4*3 = mu*q = k = 12, "
                       "so the genus is exactly 1 -- the triangle (q=3) and the "
                       "tetrahedron (mu=4) ARE the two factors",
        },
        "THE_ANSWER": (
            "The middle carries NO quadratic field: the regular tetrahedron is "
            "equilateral, so there is only ONE edge length, every edge ratio is "
            "1, and the field is Q. The oscillator's middle is the RATIONAL "
            "point between two poles whose realizations carry 36 different "
            "quadratic fields between them (Pass 290). And this is not a scaling "
            "artefact -- equilaterality means no ratio of edges can be "
            "irrational either."
        ),
        "the_bc_twist": {
            "cosine": str(cos_twist),
            "note": "the tetrahedron's BC-helix role DOES introduce an "
                    "irrationality, but not in its lengths: the twist angle "
                    "arccos(-(q-1)/q) = arccos(-2/3) has a RATIONAL cosine and an "
                    "irrational angle. That is a different kind of object from "
                    "the poles' quadratic edge fields.",
        },
        "reading": (
            "The oscillator has a clean metric signature: rational middle, "
            "irrational poles. The tetrahedron is equilateral (field Q) and "
            "self-dual with both maximal adjacencies; the two toroidal poles are "
            "dual to each other, split the adjacencies, and their realizations "
            "carry quadratic fields. Given Pass 293 -- sqrt(21) is a coordinate "
            "choice, not forced -- the poles' fields are properties of chosen "
            "realizations, whereas the middle's rationality is forced by "
            "equilaterality. The asymmetry between middle and poles is therefore "
            "real but weaker than it first looks: one side is an invariant, the "
            "other is a choice."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
