"""W(3,3) CSASZAR-SZILASSI F-VECTOR FACTORIZATION THEOREM.

A new outside-the-box identification: the f-vectors of the Csaszar
polyhedron and its toroidal-dual Szilassi polyhedron BOTH factor as
Phi_6 times a substrate ternary, with the two ternaries being exact
reverses (1, q, 2) and (2, q, 1).  The component sums of the two
f-vectors equal the common edge count 21 = q * Phi_6 = T_6 = Fano flags.

THE TWO POLYHEDRA.
=================

The Csaszar polyhedron and the Szilassi polyhedron are the only known
genus-1 (toroidal) polyhedra in which every pair of vertices is
joined by an edge (Csaszar) / every pair of faces shares an edge
(Szilassi).  They are dual: V <-> F under the toroidal duality.

  Csaszar:    V_C = 7,   E_C = 21,   F_C = 14
  Szilassi:   V_S = 14,  E_S = 21,   F_S = 7

THE FACTORIZATION.
=================

Each f-vector factors EXACTLY through Phi_6 = 7:

  f(Csaszar)   =  (V_C, E_C, F_C)  =  (7, 21, 14)
                                   =  Phi_6 * (1, q, 2)

  f(Szilassi)  =  (V_S, E_S, F_S)  =  (14, 21, 7)
                                   =  Phi_6 * (2, q, 1)

Substrate reading:
  Phi_6     = 7 = Fano points = octonion imaginaries = c_odd-1
  q         = 3 = fundamental quantum
  (1, q, 2) and (2, q, 1) are EXACT REVERSES of each other.

The toroidal duality EXCHANGES V <-> F and REVERSES the ternary
factor, while leaving E invariant.

THE COMPONENT-SUM IDENTITY.
============================

Reading sums componentwise:

  V_C + V_S  =  7 + 14   =  21  =  E_C  =  E_S
  E_C + E_S  =  21 + 21  =  42  =  q! * Phi_6
  F_C + F_S  =  14 + 7   =  21  =  E_C  =  E_S

VERTICES SUM AND FACES SUM BOTH EQUAL THE COMMON EDGE COUNT.

This is structurally remarkable: the V-pair-sum and F-pair-sum both
collapse to the single edge count (which is itself common to both).
The polyhedra share their edge complement exactly because the dual
exchange preserves edges and the two reversed ternaries (1,q,2)
and (2,q,1) sum to (3, 2q, 3) which contains q+q = 2q in the edge
slot but EQUAL endpoints (1+2 = 2+1 = 3) in the V and F slots.

CONNECTION TO FANO PLANE.
==========================

The Csaszar edge count E_C = 21 = q * Phi_6 = (pts-per-line) * (#points)
which is exactly the TOTAL POINT-LINE INCIDENCE COUNT of the Fano
plane PG(2, F_2):

  Fano plane:  7 points, 7 lines, 3 points per line, 21 incidences

So Csaszar edges = Fano flags = T_6 = q * Phi_6.

Combined with:
  Csaszar V = Fano points = Phi_6
  Csaszar F = 2 * (Fano points) = 14 = dim(G_2)

We get:

  Csaszar f-vector  =  (Fano pts, Fano flags, 2 * Fano pts)
                    =  (Phi_6, q * Phi_6, 2 * Phi_6)
                    =  Phi_6 * (1, q, 2)

The Csaszar polyhedron's combinatorics ARE the Fano plane's flag
structure, scaled by the substrate ternary (1, q, 2).

CONNECTION TO G_2.
===================

  dim(G_2)    =  14  =  Cs_F  =  Sz_V
  |G_2 roots| =  12  =  k       (W(3,3) valency)

So the Szilassi polyhedron has exactly dim(G_2) vertices, and the
Csaszar polyhedron has exactly dim(G_2) faces.  The polyhedral dual
exchanges (V, F) and the same exchange relates G_2 to its dual rep
structure (both 14-dimensional).

THE EULER-CHARACTERISTIC CHECK.
================================

Genus-1 polyhedron: chi = V - E + F = 0.

  Csaszar:    7 - 21 + 14   =  0  (torus)
  Szilassi:   14 - 21 + 7   =  0  (torus)

In substrate-ternary form:

  Phi_6 * (1 - q + 2)  =  Phi_6 * 0  =  0
  Phi_6 * (2 - q + 1)  =  Phi_6 * 0  =  0

Both substrate ternaries (1, q, 2) and (2, q, 1) have alternating
sum 1 - 3 + 2 = 0 (and 2 - 3 + 1 = 0), so the toroidal Euler
characteristic is automatic from the substrate factorization.

WHY THIS IS OUTSIDE THE BOX.
==============================

The Csaszar and Szilassi polyhedra are classical minimal triangulations
of the torus, related to the Heawood map / Fano plane structure.  Their
f-vectors (7, 21, 14) and (14, 21, 7) are well-known.

What is new here is the EXACT FACTORIZATION through the W(3,3)
substrate primitives Phi_6 and q, exhibiting (1, q, 2) and (2, q, 1)
as the dual ternary factors.  This makes the Csaszar-Szilassi duality
a substrate-ternary REVERSAL operation, and lets the genus-1 Euler
characteristic 0 be read off the substrate-ternary alternating sum.

CONNECTION TO MCCXXVI (CSASZAR-HEAWOOD TOWER).
================================================

MCCXXVI established Csaszar-Heawood as a descent tower from W(3,3)
to the Fano plane through T_{11} (Bruhat-Tits).  This commit gives
the EXACT f-vector factorization showing that the Csaszar f-vector
IS the substrate-ternary scaling of (1, q, 2) by Phi_6.

The Szilassi-dual reverses to (2, q, 1), exhibiting the polyhedral
duality as a substrate-ternary reflection.
"""
from __future__ import annotations

import json
from pathlib import Path


Q = 3
MU = 4
QFACT = 6
K_CODEC = Q * MU
P_IH = K_CODEC - 1
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
F = 24
V = 40
EDGES = 240
T_6 = 21  # triangular number T_6 = 6*7/2 = 21


CS_FVECTOR = (7, 21, 14)
SZ_FVECTOR = (14, 21, 7)


def factorization_check() -> dict:
    cs_ternary = (1, Q, 2)
    sz_ternary = (2, Q, 1)
    cs_check = tuple(PHI6 * t for t in cs_ternary)
    sz_check = tuple(PHI6 * t for t in sz_ternary)
    return {
        "Csaszar_fvector":  CS_FVECTOR,
        "Csaszar_ternary":  cs_ternary,
        "Csaszar_factor_match":  cs_check == CS_FVECTOR,
        "Szilassi_fvector": SZ_FVECTOR,
        "Szilassi_ternary": sz_ternary,
        "Szilassi_factor_match": sz_check == SZ_FVECTOR,
        "reverse_property": cs_ternary == sz_ternary[::-1],
    }


def component_sums() -> dict:
    V_sum = CS_FVECTOR[0] + SZ_FVECTOR[0]
    E_sum = CS_FVECTOR[1] + SZ_FVECTOR[1]
    F_sum = CS_FVECTOR[2] + SZ_FVECTOR[2]
    return {
        "V_sum": V_sum,
        "E_sum": E_sum,
        "F_sum": F_sum,
        "V_sum_eq_E": V_sum == CS_FVECTOR[1],
        "F_sum_eq_E": F_sum == CS_FVECTOR[2 - 1],  # F_C + F_S = 21 = E
        "E_sum_substrate": f"q_factorial * Phi_6 = {QFACT * PHI6}",
        "E_sum_match": E_sum == QFACT * PHI6,
    }


def fano_connection() -> dict:
    fano_pts = 7
    fano_lines = 7
    pts_per_line = 3
    fano_flags = fano_pts * pts_per_line
    return {
        "Fano_points":        fano_pts,
        "Fano_lines":         fano_lines,
        "Fano_pts_per_line":  pts_per_line,
        "Fano_flags":         fano_flags,
        "Csaszar_V_eq_FanoP": CS_FVECTOR[0] == fano_pts,
        "Csaszar_E_eq_FanoFlags": CS_FVECTOR[1] == fano_flags,
        "Csaszar_F_eq_2FanoP": CS_FVECTOR[2] == 2 * fano_pts,
        "interpretation": (
            "Csaszar f-vector = (Fano points, Fano flags, 2*Fano points) "
            "= Phi_6 * (1, q, 2).  The Csaszar polyhedron's combinatorics "
            "ARE the Fano flag structure scaled by the substrate ternary."
        ),
    }


def g2_connection() -> dict:
    dim_g2 = 14
    g2_roots = 12
    return {
        "dim_G_2":        dim_g2,
        "|G_2 roots|":    g2_roots,
        "Csaszar_F_eq_dim_G2":  CS_FVECTOR[2] == dim_g2,
        "Szilassi_V_eq_dim_G2": SZ_FVECTOR[0] == dim_g2,
        "k_eq_g2_roots":  K_CODEC == g2_roots,
    }


def euler_characteristic_check() -> dict:
    chi_cs = CS_FVECTOR[0] - CS_FVECTOR[1] + CS_FVECTOR[2]
    chi_sz = SZ_FVECTOR[0] - SZ_FVECTOR[1] + SZ_FVECTOR[2]
    return {
        "chi_Csaszar":   chi_cs,
        "chi_Szilassi":  chi_sz,
        "both_zero":     (chi_cs == 0) and (chi_sz == 0),
        "Cs_ternary_altsum": 1 - Q + 2,
        "Sz_ternary_altsum": 2 - Q + 1,
        "both_substrate_zero":  (1 - Q + 2) == 0 and (2 - Q + 1) == 0,
    }


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "q_factorial": QFACT,
                "k": K_CODEC, "p_Ih": P_IH,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6,
                "f": F, "v": V, "edges": EDGES, "T_6": T_6,
            },
        },
        "factorization_check":    factorization_check(),
        "component_sums":         component_sums(),
        "fano_connection":        fano_connection(),
        "g2_connection":          g2_connection(),
        "euler_characteristic":   euler_characteristic_check(),
        "theorem": (
            "W(3,3) Csaszar-Szilassi F-Vector Factorization Theorem.  "
            "The f-vectors of the Csaszar and Szilassi polyhedra factor "
            "exactly as f(Csaszar) = Phi_6 * (1, q, 2) and f(Szilassi) "
            "= Phi_6 * (2, q, 1), with the two substrate ternaries "
            "being exact reverses.  The toroidal duality V<->F is a "
            "substrate-ternary reflection, the genus-1 Euler "
            "characteristic 0 = Phi_6 * (1 - q + 2) is automatic, and "
            "the component sums obey V_C + V_S = F_C + F_S = E_C = E_S "
            "= q * Phi_6 = T_6 = Fano flag count.  The Csaszar f-vector "
            "IS the substrate-ternary scaling of the Fano plane's flag "
            "structure."
        ),
        "honesty_boundary": (
            "F-vectors of Csaszar and Szilassi polyhedra are classical "
            "(Csaszar 1949, Szilassi 1977).  The factorization through "
            "Phi_6 with the substrate ternaries (1, q, 2) and (2, q, 1) "
            "is exact integer arithmetic.  The structural new content "
            "is the substrate-ternary reading of the dual exchange and "
            "the recovery of Fano flag structure and G_2 dimension as "
            "exact polyhedral primitives."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_csaszar_szilassi_fvector_factorization.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) CSASZAR-SZILASSI F-VECTOR FACTORIZATION THEOREM")
    print("=" * 78)

    f = payload["factorization_check"]
    print("\nF-vector factorization:")
    print(f"  f(Csaszar)  = {f['Csaszar_fvector']}  =  Phi_6 * {f['Csaszar_ternary']}")
    print(f"  f(Szilassi) = {f['Szilassi_fvector']}  =  Phi_6 * {f['Szilassi_ternary']}")
    print(f"  Reverses:   {f['reverse_property']}")

    s = payload["component_sums"]
    print(f"\nComponent sums:")
    print(f"  V_C + V_S = {s['V_sum']:>2d}  (= E = 21)")
    print(f"  E_C + E_S = {s['E_sum']:>2d}  = q! * Phi_6")
    print(f"  F_C + F_S = {s['F_sum']:>2d}  (= E = 21)")

    fc = payload["fano_connection"]
    print(f"\nFano-plane connection:")
    print(f"  Csaszar V = Fano points = {fc['Fano_points']}")
    print(f"  Csaszar E = Fano flags = {fc['Fano_flags']}")
    print(f"  Csaszar F = 2 * Fano points = {2*fc['Fano_points']}")

    g = payload["g2_connection"]
    print(f"\nG_2 connection:")
    print(f"  dim(G_2)  = {g['dim_G_2']} = Csaszar F = Szilassi V")
    print(f"  |G_2 roots| = {g['|G_2 roots|']} = k (W33 valency)")

    e = payload["euler_characteristic"]
    print(f"\nGenus-1 Euler characteristic (toroidal):")
    print(f"  chi(Csaszar)  = 7 - 21 + 14 = {e['chi_Csaszar']}")
    print(f"  chi(Szilassi) = 14 - 21 + 7 = {e['chi_Szilassi']}")
    print(f"  Both substrate altsums = 0: {e['both_substrate_zero']}")

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
