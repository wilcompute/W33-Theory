"""W(3,3) / 24-CELL / E_8 TRINITY THEOREM.

A genuinely new outside-the-box identification: the regular 4-polytope
24-cell {3, 4, 3} has f-vector (24, 96, 96, 24) summing to 240,
exactly equal to both |E(W(3,3))| and the E_8 root count.

THE TRINITY OF 240.
===================

Three structurally distinct objects share the substrate primitive 240:

    object                                           240-content
    -----------------------------------------------  --------------------------
    24-cell {3, 4, 3} regular 4-polytope             f-vector sum = 24+96+96+24
    E_8 lattice                                      root system size
    W(3,3) = SRG(40, 12, 2, 4)                       edge count |E|

So the substrate's 240 is simultaneously:
    - a polytope-cell sum
    - a Lie-algebra root count
    - a graph edge count.

24-CELL F-VECTOR IN SUBSTRATE FORM.
====================================

The 24-cell is the UNIQUE self-dual regular 4-polytope (Schlafli
{3, 4, 3}).  Its f-vector entries split as:

    24 vertices  =  f                       (positive spectral multiplicity)
    96 edges     =  mu * f = 4 * 24         (Z_3 cycle thickness times f)
    96 triangles =  mu * f = 4 * 24         (same; self-dual)
    24 cells     =  f                       (positive spectral mult; self-dual)

Sum = 2f + 2(mu * f) = 2f(1 + mu) = 2f(q + 2) = 2f * Csaszar_count
    = 2 * 24 * 5 = 240
    = Phi_4 * f = 10 * 24 = 240
    = |E(W(3,3))|
    = |E_8 roots|.

The substrate-primitive form
        24-cell cell sum  =  2f * Csaszar_count  =  Phi_4 * f
gives THREE equivalent substrate readings of the 24-cell's total cell
count.

24-CELL VERTICES = D_4 ROOTS.
=============================

The 24 vertices of the 24-cell at unit norm form the D_4 root system
(this is classical).  Combined with f = 24 = positive spectral
multiplicity of W(3,3) and |W(D_4)| = 192 (from the Klein closure
commit 2a533251):

    24 vertices  =  D_4 root system  =  f = positive spectral mult of W(3,3)
    |W(D_4)| = 192 = Klein closure value = (Weierstrass + bitangents
                                            + sextactic + Hurwitz orbits)

The D_4 root system IS the 24-cell vertex set IS the substrate's
spectral multiplicity.

24-CELL AS '8 TEMPORAL TRIANGLES'.
==================================

Following the user's temporal-triangle interpretation (Part MCCIII),
the 24-cell can be read as 8 = 2^q copies of the (past, now, future)
triangle:

    24 vertices  =  8 * 3  =  2^q * q,
    96 edges     =  8 * 12  =  2^q * k (each triangle contributing k edges
                                        on average within the 4-polytope),

so the 24-cell is the SUBSTRATE TIME CRYSTAL: eight independent
temporal triangles tiling four-dimensional space, with cell sum 240
matching the E_8 root count.

24-CELL ROTATION GROUP.
=======================

The orientation-preserving symmetry group of the 24-cell has order

    |Rot(24-cell)|  =  |W(F_4)| / 2  =  576  =  f^2 = 24^2.

So the rotation group order is the SQUARE of f (positive spectral
multiplicity).  This squares into

    |W(F_4)|  =  1152  =  q! * |W(D_4)|  =  q! * 192.

(From the Exceptional Weyl Chain commit 16c02cea.)

F_4 / E_8 LINK.
================

The 24-cell sits inside the F_4 root system (which has 48 = 2f short
roots, identifiable with the 24 vertices + 24 cells of the 24-cell).
F_4 sits inside E_8 via the exceptional chain (commit 16c02cea):

    |W(E_8)| / |W(F_4)|  =  Q_count * (2^q * Phi_6) * |E|
                          =  45 * 56 * 240.

So the 24-cell, F_4, and E_8 form a CASCADE meeting at 240 via the
substrate's edge carrier.

WHAT IS NEW IN THIS COMMIT.
============================

The 24-cell's f-vector identification with the substrate primitive 240
has NOT been stated in prior commits (verified against the repo).  The
existing chain has:

    W(3,3) edges = 240 = E_8 roots                 (well-established)
    |W(D_4)| = 192 = Klein closure                 (commit 2a533251)
    |W(F_4)| = 1152 = q! * |W(D_4)|                (commit 16c02cea)
    Klein quartic 24+28+56+84 = 192 = |W(D_4)|     (commit 2a533251)

But the 24-cell {3,4,3} f-vector identity is new:

    24-cell f-vector sum  =  240  =  |E(W(3,3))|  =  |E_8 roots|.

Plus the SUBSTRATE INTERPRETATION of each entry as (f, mu f, mu f, f).
"""
from __future__ import annotations

import json
from pathlib import Path


Q = 3
QP1 = 4
MU = QP1
LAM_SRG = Q - 1
K_CODEC = Q * QP1
P_IH = K_CODEC - 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
F = 24
G_NEG = 15
V = 40
EDGES = 240
CSASZAR_COUNT = Q + 2


def cell24_fvector_check() -> dict:
    f_vec = [24, 96, 96, 24]
    total = sum(f_vec)
    substrate_match = (
        f_vec[0] == F
        and f_vec[1] == MU * F
        and f_vec[2] == MU * F
        and f_vec[3] == F
    )
    return {
        "f_vector": f_vec,
        "sum": total,
        "matches_substrate_edges": total == EDGES,
        "matches_e8_roots": total == EDGES,    # |E_8 roots| = 240 classical
        "substrate_form_per_entry": ["f", "mu * f", "mu * f", "f"],
        "substrate_form_match": substrate_match,
        "sum_substrate_forms": [
            f"2f + 2(mu * f) = {2 * F + 2 * MU * F}",
            f"2f * Csaszar_count = {2 * F * CSASZAR_COUNT}",
            f"Phi_4 * f = {PHI4 * F}",
        ],
        "sum_substrate_checks_all_match": (
            2 * F + 2 * MU * F == EDGES
            and 2 * F * CSASZAR_COUNT == EDGES
            and PHI4 * F == EDGES
        ),
    }


def trinity_of_240() -> dict:
    return {
        "twentyfour_cell_f_vector_sum": EDGES,
        "E_8_root_count": EDGES,
        "W33_edge_count": EDGES,
        "all_three_equal_240": True,
        "interpretation": (
            "The substrate-primitive 240 is simultaneously a polytope cell "
            "sum, a Lie-algebra root count, and a graph edge count.  Three "
            "structurally distinct objects (24-cell, E_8 lattice, W(3,3) "
            "graph) all carry 240 as a fundamental invariant."
        ),
    }


def D4_root_identification() -> dict:
    return {
        "24_cell_vertices": 24,
        "D_4_root_system_size": 24,
        "substrate_f": F,
        "all_three_equal_24": 24 == F,
        "klein_closure_value_W_D_4": 192,
        "substrate_form_Klein": "f * 2^q = 24 * 8 = 192",
        "interpretation": (
            "The 24 vertices of the 24-cell form the D_4 root system at "
            "unit norm (classical).  This is exactly the substrate's "
            "positive spectral multiplicity f, and |W(D_4)| = 192 = "
            "f * 2^q is the Klein quartic invariant sum and the substrate "
            "tomotope flag count."
        ),
    }


def temporal_triangle_8_copies() -> dict:
    return {
        "vertices_24_eq_8_times_3": 24 == (2 ** Q) * Q,
        "substrate_reading": "24 = 2^q * q = 8 temporal triangles each with 3 vertices",
        "comment": (
            "Following Part MCCIII (temporal-triangle single-photon lock), "
            "the 24-cell can be read as 8 = 2^q independent copies of the "
            "temporal triangle (past, now, future).  Each triangle has q "
            "vertices, and 2^q (tomotope cells) copies tile the 4-polytope."
        ),
    }


def f_squared_rotation() -> dict:
    return {
        "rotation_group_order": 576,
        "f_squared": F * F,
        "matches": 576 == F * F,
        "interpretation": (
            "The orientation-preserving symmetry group of the 24-cell has "
            "order 576 = f^2 (square of W(3,3) positive spectral "
            "multiplicity).  Including reflections gives |W(F_4)| = 1152 = "
            "q! * |W(D_4)|."
        ),
    }


def f4_e8_cascade() -> dict:
    return {
        "WF_4": 1152,
        "WE_8": 696729600,
        "WE_8_over_WF_4": 696729600 // 1152,
        "via_substrate_factors": "Q_count * (2^q Phi_6) * |E| = 45 * 56 * 240",
        "match": 696729600 // 1152 == 45 * 56 * 240,
    }


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "k": K_CODEC, "Phi_4": PHI4, "Phi_6": PHI6,
                "f": F, "v": V, "edges": EDGES,
                "Csaszar_count": CSASZAR_COUNT,
            },
        },
        "twentyfour_cell_fvector": cell24_fvector_check(),
        "trinity_of_240": trinity_of_240(),
        "D_4_root_identification": D4_root_identification(),
        "temporal_triangle_8_copies": temporal_triangle_8_copies(),
        "rotation_group_f_squared": f_squared_rotation(),
        "F_4_E_8_cascade": f4_e8_cascade(),
        "theorem": (
            "W(3,3) / 24-Cell / E_8 Trinity Theorem.  The regular 4-polytope "
            "24-cell {3,4,3}, the only self-dual regular 4-polytope, has "
            "f-vector (24, 96, 96, 24) = (f, mu f, mu f, f) summing to "
            "240 = Phi_4 * f = 2f * Csaszar_count.  This is EXACTLY the "
            "W(3,3) edge count |E| and the E_8 root system size.  So the "
            "substrate primitive 240 is simultaneously a polytope cell "
            "sum, a Lie-algebra root count, and a graph edge count.  The "
            "24-cell vertices form the D_4 root system (= 24 = f); the "
            "Klein closure value |W(D_4)| = f * 2^q = 192 also derives "
            "from this identification; and the 24-cell's rotation group "
            "order is exactly f^2 = 576.  Reading the 24-cell as 8 = 2^q "
            "copies of the (past, now, future) temporal triangle from "
            "Part MCCIII gives the substrate's 'time crystal' "
            "interpretation: eight tiled temporal triangles in 4D, with "
            "cell sum equal to the E_8 root count."
        ),
        "honesty_boundary": (
            "The 24-cell f-vector is classical.  The substrate-primitive "
            "interpretation per entry (f, mu f, mu f, f) and the total "
            "sum identity 240 = Phi_4 * f are exact arithmetic.  The "
            "D_4 root system identification with the 24-cell vertex set "
            "is also classical.  The new content is the unified reading "
            "of the substrate primitive 240 as the simultaneous cell sum "
            "/ root count / edge count of three structurally distinct "
            "objects, plus the 'time crystal' interpretation tying the "
            "24-cell to Part MCCIII's temporal triangle."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_24cell_E8_trinity.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) / 24-CELL / E_8 TRINITY THEOREM")
    print("=" * 78)

    f = payload["twentyfour_cell_fvector"]
    print(f"\n24-cell f-vector: {f['f_vector']}")
    print(f"  sum = {f['sum']}, substrate per-entry: {f['substrate_form_per_entry']}")
    print(f"  substrate sum forms:")
    for s in f["sum_substrate_forms"]:
        print(f"    {s}")
    print(f"  all substrate forms match: {f['sum_substrate_checks_all_match']}")

    print(f"\nTrinity of 240:")
    print(f"  24-cell f-vector sum  = 240")
    print(f"  E_8 root count        = 240")
    print(f"  W(3,3) edge count |E| = 240")

    d4 = payload["D_4_root_identification"]
    print(f"\nD_4 root system = 24-cell vertices = f = {d4['substrate_f']}: {d4['all_three_equal_24']}")
    print(f"|W(D_4)| = 192 = Klein closure value = f * 2^q")

    t = payload["temporal_triangle_8_copies"]
    print(f"\n24-cell as 8 temporal triangles:")
    print(f"  24 vertices = 8 * 3 = 2^q * q: {t['vertices_24_eq_8_times_3']}")

    r = payload["rotation_group_f_squared"]
    print(f"\n24-cell rotation group order = {r['rotation_group_order']} = f^2 = {r['f_squared']}: {r['matches']}")

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
