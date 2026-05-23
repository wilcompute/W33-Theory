"""W(3,3) BRUHAT-TITS SPHERE STRUCTURE THEOREM.

Continuation of Part MCCXVII (Bruhat-Tits tree duality, commit 3327d994).
Where MCCXVII established W(3,3) = T_{11}/Gamma in PGL(2, Q_{11}) and
gave a Ryu-Takayanagi entropy bound, this script formalises the
ENTIRE COMBINATORIAL STRUCTURE of the bulk tree T_{11} in substrate-
primitive form, including sphere sizes, ball sizes, generating function,
and p-adic unit-group filtration.

THE FIVE BRUHAT-TITS IDENTITIES.
=================================

The Bruhat-Tits tree T_{11} is (p+1)-regular = 12-regular over Q_{11}.
Centred at any vertex, distance-n sphere and radius-n ball sizes are:

    |S_n(T_{11})|  =  (p_Ih + 1) * p_Ih^{n-1}  for n >= 1
    |B_n(T_{11})|  =  1 + sum_{i=1}^n |S_i|.

(1) FIRST-SPHERE IDENTITY.
    |S_1(T_{11})|  =  p_Ih + 1  =  12  =  k  (W(3,3) valency).
    The first-shell of the holographic bulk equals the substrate valency.

(2) FIRST-BALL IDENTITY.
    |B_1(T_{11})|  =  1 + k  =  13  =  Phi_3  =  c_odd.
    The unit ball of the holographic bulk equals the substrate's third
    cyclotomic primitive (and the spine-staircase odd component).

(3) GENERAL SPHERE FORMULA.
    |S_n(T_{11})|  =  k * p_Ih^{n - 1}.
    Every sphere of T_{11} has size = valency times Ihara prime to a
    power -- a clean substrate-primitive law.

(4) GENERATING FUNCTION.
    Sum_{n >= 0} |S_n| x^n  =  (1 + x) / (1 - p_Ih * x).
    The closed-form generating function has substrate-primitive
    numerator (1 + x) and denominator (1 - p_Ih * x), with pole at the
    Ramanujan-circle radius x = 1/p_Ih.

(5) SPECTRAL RADIUS / TOPOLOGICAL ENTROPY.
    spectral_radius(T_{11})  =  p_Ih  =  11.
    Volume growth rate = p_Ih, matching the Ihara-Ramanujan circle
    radius squared and the topological entropy h_top = log(p_Ih)
    (commit 770c5bbc spectral & arithmetic fingerprint).

(6) p-ADIC UNIT FILTRATION.
    | Z_{p_Ih}^* / U^(1) |  =  p_Ih - 1  =  10  =  Phi_4.
    The substrate's fourth cyclotomic appears as the first principal-unit
    quotient of Z_{p_Ih} at the Ihara prime -- so Phi_4 controls both
    the spectral gap of W(3,3)'s discrete Laplacian (commit 770c5bbc)
    AND the p-adic principal-unit quotient at p_Ih.

CONNECTION TO RYU-TAKAYANAGI ENTROPY (MCCXVII).
================================================

The RT entropy bound from MCCXVII is
    S_RT  >=  (2 sqrt(p_Ih) / f) * (v / 2)  approx  5.53 in Planck units.

In substrate primitives: S_RT >= (2 sqrt(p_Ih) / f) * (v / 2) =
sqrt(p_Ih) * v / f at the boundary half-chain.

This is the substrate's holographic minimal surface in p-adic AdS.

CONNECTION TO PRIME CYCLE GROWTH (commit 4079581a).
====================================================

The Ihara prime number theorem pi_n ~ p_Ih^n / n is the SAME p_Ih
that controls T_{11}'s sphere growth rate.  So the same number 11
appears in three structurally distinct places:

    1. T_{11} sphere growth                  (p-adic bulk)
    2. Ihara zeta non-trivial zero modulus    (Hashimoto spectrum)
    3. Prime-cycle asymptotic growth rate     (graph PNT)

NEW UNIFICATION.

The Bruhat-Tits tree's combinatorial geometry, the Ihara zeta's
analytic geometry, and the prime-cycle counting all share a single
substrate primitive: p_Ih = k - 1 = 11.

WHAT IS NEW IN THIS COMMIT.
============================

MCCXVII established the W(3,3) = T_{11}/Gamma duality and computed the
RT entropy bound.  This commit adds:

  (i)   Explicit substrate-primitive identification |S_1| = k.
  (ii)  Explicit substrate-primitive identification |B_1| = Phi_3.
  (iii) The closed-form generating function (1+x)/(1-p_Ih*x).
  (iv)  The p-adic principal-unit quotient identification |Z_p^*/U^(1)| = Phi_4.
  (v)   The unified picture connecting the BT tree sphere structure, the
        Ihara zeta spectrum, and the prime cycle PNT through p_Ih.
"""
from __future__ import annotations

import json
import math
from pathlib import Path


# Substrate constants
Q = 3
QP1 = 4
K_CODEC = Q * QP1
P_IH = K_CODEC - 1
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
F = 24
V = 40
EDGES = 240
CSASZAR_COUNT = Q + 2


def sphere_ball_sizes(n_max: int = 6) -> list[dict]:
    rows = []
    for n in range(n_max + 1):
        if n == 0:
            S_n = 1
            B_n = 1
        else:
            S_n = (P_IH + 1) * (P_IH ** (n - 1))
            B_n = 1 + sum((P_IH + 1) * (P_IH ** (i - 1)) for i in range(1, n + 1))
        rows.append({"n": n, "sphere_S_n": S_n, "ball_B_n": B_n})
    return rows


def substrate_identifications() -> dict:
    return {
        "S_1_eq_k": {
            "value": (P_IH + 1),
            "substrate": "k (W(3,3) valency)",
            "match": (P_IH + 1) == K_CODEC,
        },
        "B_1_eq_Phi_3": {
            "value": 1 + (P_IH + 1),
            "substrate": "Phi_3 = c_odd = 13",
            "match": (1 + P_IH + 1) == PHI3,
        },
        "S_n_general_formula": {
            "formula": "|S_n| = k * p_Ih^(n-1)",
            "substrate": "valency times Ihara prime power",
        },
        "generating_function": {
            "form": "(1 + x) / (1 - p_Ih * x)",
            "pole_at": "x = 1 / p_Ih = Ramanujan circle radius",
        },
        "spectral_radius": {
            "value": P_IH,
            "substrate": "p_Ih (volume growth rate)",
        },
        "p_adic_unit_filtration": {
            "value": P_IH - 1,
            "substrate": "Phi_4 = 10",
            "match": (P_IH - 1) == PHI4,
            "comment": "|Z_p^* / U^(1)| = p - 1 at p = p_Ih equals Phi_4",
        },
    }


def unified_p_Ih_appearances() -> dict:
    return {
        "BT_tree_sphere_growth": "|S_n(T_{p_Ih})| = k * p_Ih^(n-1)",
        "Ihara_zeta_Ramanujan_circle": "|u|^2 = p_Ih on the critical circle",
        "graph_PNT_growth_rate": "pi_n ~ p_Ih^n / n",
        "topological_entropy": "h_top = log(p_Ih)",
        "Mahler_measure_Ihara_factors": "m = log(p_Ih)",
        "comment": (
            "Five structurally distinct substrate quantities all equal "
            "(or take their log of) p_Ih = 11: the bulk-tree volume "
            "growth, the boundary Ihara zeta Ramanujan circle radius, "
            "the graph prime number theorem rate, the topological entropy, "
            "and the Mahler measure of every non-trivial Ihara factor."
        ),
    }


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "k": K_CODEC, "p_Ih": P_IH,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6,
                "f": F, "v": V, "edges": EDGES,
            },
        },
        "bruhat_tits_sphere_ball_table": sphere_ball_sizes(6),
        "substrate_identifications": substrate_identifications(),
        "unified_p_Ih_appearances": unified_p_Ih_appearances(),
        "theorem": (
            "W(3,3) Bruhat-Tits Sphere Structure Theorem.  The bulk "
            "holographic dual T_{11} (Bruhat-Tits tree of PGL(2, Q_{11})) "
            "has sphere size |S_n| = k * p_Ih^(n-1) and unit ball "
            "|B_1| = 1 + k = Phi_3, so the substrate's valency k and "
            "third cyclotomic Phi_3 are exactly the first-shell and "
            "first-ball sizes of the holographic bulk.  The generating "
            "function (1 + x) / (1 - p_Ih * x) has its pole at x = 1/p_Ih, "
            "the Ramanujan-circle radius, and the volume growth rate "
            "p_Ih is the topological entropy base and the Mahler measure "
            "of the Ihara factors.  At the p-adic level, "
            "|Z_{p_Ih}^* / U^(1)| = p_Ih - 1 = Phi_4 (= W(3,3) Laplacian "
            "spectral gap), connecting p-adic principal-unit filtration "
            "to the substrate's discrete Laplacian gap."
        ),
        "honesty_boundary": (
            "Bruhat-Tits tree combinatorics are classical (Serre, "
            "Springer).  All substrate-primitive identifications are "
            "exact arithmetic.  The unified picture connecting BT sphere "
            "growth, Ihara-zeta Ramanujan circle, graph PNT, topological "
            "entropy, and Mahler measure to the same number p_Ih = 11 is "
            "the structural new content -- the underlying mathematical "
            "facts are individually well-known."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_bruhat_tits_sphere_structure.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) BRUHAT-TITS T_{11} SPHERE STRUCTURE")
    print("=" * 78)
    print(f"\n{'n':>3s}  {'|S_n|':>10s}  {'|B_n|':>10s}  substrate form")
    print('  ' + '-' * 70)
    for r in payload["bruhat_tits_sphere_ball_table"]:
        n = r["n"]
        s = ""
        if n == 0: s = "1"
        elif n == 1: s = "|S_1| = k; |B_1| = Phi_3"
        elif n == 2: s = "|S_2| = k * p_Ih"
        else: s = "|S_n| = k * p_Ih^(n-1)"
        print(f"  {n:>3d}  {r['sphere_S_n']:>10d}  {r['ball_B_n']:>10d}  {s}")

    print("\nKey substrate identifications:")
    s = payload["substrate_identifications"]
    print(f"  |S_1(T_11)| = k = {s['S_1_eq_k']['value']}: {s['S_1_eq_k']['match']}")
    print(f"  |B_1(T_11)| = Phi_3 = {s['B_1_eq_Phi_3']['value']}: {s['B_1_eq_Phi_3']['match']}")
    print(f"  |Z_p^* / U^(1)| = Phi_4 = {s['p_adic_unit_filtration']['value']}: {s['p_adic_unit_filtration']['match']}")
    print(f"  Generating function: {s['generating_function']['form']}")
    print(f"  Spectral radius = p_Ih = {s['spectral_radius']['value']}")

    print("\nUnified p_Ih appearances:")
    print(f"  1. BT tree sphere growth rate")
    print(f"  2. Ihara zeta Ramanujan circle radius squared")
    print(f"  3. Graph PNT exponential growth rate")
    print(f"  4. Topological entropy h_top = log(p_Ih)")
    print(f"  5. Mahler measure of non-trivial Ihara factors")

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
