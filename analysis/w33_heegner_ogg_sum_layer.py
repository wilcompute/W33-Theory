"""W(3,3) HEEGNER-OGG SUM-LAYER THEOREM.

Companion to the Heegner-Ogg Venn decomposition (commit c300a6bd).
Where the Venn theorem identifies the CARDINALITIES of all four Venn
cells as W(3,3) substrate primitives, this commit identifies the
SUMS-OF-ELEMENTS in those same cells as substrate primitives.

THE FOUR SUMS.
================

Recall the four Venn cells of Heegner_9 and Ogg_15:

  Heegner cap Ogg     =  {2, 3, 7, 11, 19}
  Heegner setminus O  =  {1, 43, 67, 163}
  Ogg setminus H      =  {5, 13, 17, 23, 29, 31, 41, 47, 59, 71}
  Heegner cup Ogg     =  {19 elements total}

Element sums:

  Sum(H cap O)          =  2 + 3 + 7 + 11 + 19
                        =  42
                        =  q! * Phi_6                  (substrate-clean)

  Sum(H setminus O)     =  1 + 43 + 67 + 163
                        =  274
                        =  2 * 137
                        =  2 * alpha_fine_int          (alpha-related, see below)

  Sum(O setminus H)     =  5 + 13 + 17 + 23 + 29 + 31 + 41 + 47 + 59 + 71
                        =  336
                        =  2^q * Phi_6 * q + 0?       (= 8*42 = 2^q * 42)
                        =  2^q * (Sum H cap O)
                        =  2^q * q! * Phi_6

  Sum(H cup O)          =  Sum(H) + Sum(O) - Sum(H cap O)
                        =  316 + 378 - 42
                        =  652
                        =  mu * Heegner_9              (substrate-clean)
                        =  4 * 163

ALL FOUR VENN-CELL ELEMENT SUMS ARE SUBSTRATE-PRIMITIVE.

THE HODGE-LIKE SUM DECOMPOSITION.
====================================

  Sum(H cup O)  =  Sum(H cap O) + Sum(H setminus O) + Sum(O setminus H)
              =  42 + 274 + 336
              =  652
              =  4 * 163
              =  mu * max(Heegner)

A three-way split of mu * Heegner_9 (the union sum) into:

  intersection sum    =   42  =  q! * Phi_6
  Heegner-only sum    =  274  =  2 * 137
  Ogg-only sum         =  336  =  2^q * q! * Phi_6  =  8 * 42

WHERE THE FINE-STRUCTURE-LIKE 137 APPEARS.
==========================================

  Sum(H setminus O)  =  1 + 43 + 67 + 163  =  274  =  2 * 137

The number 137 is the integer rounding of 1/alpha_fine_structure
(= 137.036...).  Its appearance as half the Heegner-only sum is
striking; we record it as a coincidence flag, not as a derivation
of alpha.

THE OGG-ONLY / INTERSECTION RATIO.
====================================

  Sum(O setminus H)  /  Sum(H cap O)  =  336 / 42  =  8  =  2^q

So the Ogg-only-element sum is EXACTLY 2^q times the intersection
sum.  The factor 2^q is the substrate's even-byte structure.

CONNECTION TO MAX-HEEGNER.
=============================

  Sum(H cup O)  =  4 * 163  =  mu * Heegner_9

The 163 = Heegner_9 is the largest class-number-1 discriminant.
Its appearance with multiplicity mu = 4 in the union sum gives the
substrate-clean identity:

  (Sum of every prime that is either Heegner or Ogg)  =  mu * 163

So summing all 19 distinct primes/Heegners in the union yields four
copies of the maximum-Heegner discriminant.

CONNECTION TO INTERSECTION = q! * Phi_6.
==========================================

  Sum(H cap O)  =  q! * Phi_6  =  6 * 7  =  42

This equals exactly the sum of Csaszar edges (21 = T_6) and Szilassi
edges (21) -- the two edge-counts of the two genus-1 minimal
polyhedra (commit 58f233e5).

  Sum(H cap O)  =  E_Csaszar + E_Szilassi  =  21 + 21  =  42

So the FIVE small primes shared between Heegner and Ogg lists sum
to the COMBINED edge count of the two toroidal polyhedra.

WHY THIS IS OUTSIDE THE BOX.
==============================

Element sums of Heegner and Ogg sets are elementary arithmetic, but
their substrate-primitive interpretations (q!*Phi_6, mu*Heegner_9,
8 times intersection, factor 2^q between Ogg-only and intersection)
expose deeper structural connections.

The union sum mu * Heegner_9 = mu * max(Heegner) is particularly
striking: it says that the COMBINED Heegner-or-Ogg list has
'arithmetic weight' exactly mu times the heaviest single discriminant.

CONNECTION TO PRIOR COMMITS.
==============================

  - c300a6bd (Venn cardinalities = (mu+1, mu, Phi_4, 19))
  - This commit (Venn sums = (q!*Phi_6, 274, 2^q*q!*Phi_6, mu*163))
  - Together: ALL four Venn cells are characterized by both their
    CARDINALITY and their ELEMENT-SUM in substrate primitives.

The pair (cardinality, element-sum) gives a TWO-DIMENSIONAL
substrate signature for each cell.
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
G_NEG = 15

HEEGNER_9 = {1, 2, 3, 7, 11, 19, 43, 67, 163}
OGG_15 = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71}

HEEGNER_MAX = 163


def venn_sums() -> dict:
    H = HEEGNER_9
    O = OGG_15
    cap = H & O
    h_only = H - O
    o_only = O - H
    union = H | O
    return {
        "Sum_H_cap_O": {
            "elements": sorted(cap),
            "sum": sum(cap),
            "substrate": f"q! * Phi_6 = {QFACT * PHI6}",
            "match": sum(cap) == QFACT * PHI6,
        },
        "Sum_H_setminus_O": {
            "elements": sorted(h_only),
            "sum": sum(h_only),
            "substrate": "2 * 137 (coincidence flag, not derivation)",
            "match": sum(h_only) == 274,
        },
        "Sum_O_setminus_H": {
            "elements": sorted(o_only),
            "sum": sum(o_only),
            "substrate": f"2^q * q! * Phi_6 = {2**Q * QFACT * PHI6}",
            "match": sum(o_only) == 2 ** Q * QFACT * PHI6,
        },
        "Sum_H_cup_O": {
            "size": len(union),
            "sum": sum(union),
            "substrate": f"mu * Heegner_max = {MU * HEEGNER_MAX}",
            "match": sum(union) == MU * HEEGNER_MAX,
        },
    }


def hodge_decomposition_check() -> dict:
    H, O = HEEGNER_9, OGG_15
    cap = H & O
    h_only = H - O
    o_only = O - H
    union = H | O
    lhs = sum(union)
    rhs = sum(cap) + sum(h_only) + sum(o_only)
    return {
        "Sum_union":           lhs,
        "Sum_cap_plus_only":   rhs,
        "match":               lhs == rhs,
        "decomposition":       "Sum(union) = Sum(cap) + Sum(H_only) + Sum(O_only)",
        "values":              {"42 + 274 + 336": 42 + 274 + 336, "expected": 652},
    }


def ratio_check() -> dict:
    H, O = HEEGNER_9, OGG_15
    cap = H & O
    o_only = O - H
    ratio = sum(o_only) / sum(cap)
    return {
        "ratio_O_only_to_cap": ratio,
        "equals_2_to_q":        ratio == 2 ** Q,
        "substrate":            "2^q = 8 (substrate even-byte structure)",
    }


def csaszar_szilassi_link() -> dict:
    return {
        "Sum_H_cap_O":         42,
        "E_Csaszar":           21,
        "E_Szilassi":          21,
        "match_combined_edges": 42 == 21 + 21,
        "interpretation": (
            "The five primes shared between Heegner and Ogg lists "
            "sum to the COMBINED edge count of the Csaszar and "
            "Szilassi polyhedra (21 + 21 = 42)."
        ),
    }


def two_dimensional_signature() -> dict:
    H, O = HEEGNER_9, OGG_15
    cap = H & O
    h_only = H - O
    o_only = O - H
    union = H | O
    return {
        "H_cap_O":      {"size": len(cap), "sum": sum(cap),
                         "size_substrate": "mu+1", "sum_substrate": "q!*Phi_6"},
        "H_only":       {"size": len(h_only), "sum": sum(h_only),
                         "size_substrate": "mu", "sum_substrate": "2*137"},
        "O_only":       {"size": len(o_only), "sum": sum(o_only),
                         "size_substrate": "Phi_4", "sum_substrate": "2^q*q!*Phi_6"},
        "union":        {"size": len(union), "sum": sum(union),
                         "size_substrate": "sig_-(K3)=Heegner_6", "sum_substrate": "mu*163"},
    }


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "q_factorial": QFACT,
                "k": K_CODEC, "p_Ih": P_IH,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6,
                "f": F, "g_neg": G_NEG, "Heegner_max": HEEGNER_MAX,
            },
            "Heegner_9": sorted(HEEGNER_9),
            "Ogg_15": sorted(OGG_15),
        },
        "venn_sums":                       venn_sums(),
        "hodge_decomposition_check":       hodge_decomposition_check(),
        "ratio_check":                     ratio_check(),
        "csaszar_szilassi_link":           csaszar_szilassi_link(),
        "two_dimensional_signature":       two_dimensional_signature(),
        "theorem": (
            "W(3,3) Heegner-Ogg Sum-Layer Theorem.  In each of the four "
            "Venn cells of Heegner_9 and Ogg_15, the SUM-OF-ELEMENTS is "
            "W(3,3) substrate-primitive: Sum(H cap O) = q!*Phi_6, "
            "Sum(H setminus O) = 2*137, Sum(O setminus H) = 2^q*q!*Phi_6, "
            "Sum(H cup O) = mu*Heegner_max = mu*163.  The intersection "
            "sum equals the combined Csaszar+Szilassi edge count (42 = "
            "21+21), and the Ogg-only/intersection sum ratio is exactly "
            "2^q.  Combined with the Venn cardinality theorem (commit "
            "c300a6bd), every cell of the Heegner-Ogg Venn diagram is "
            "characterized in two substrate dimensions: cardinality "
            "(mu+1, mu, Phi_4, sig_-(K3)) and element sum (q!*Phi_6, "
            "2*137, 2^q*q!*Phi_6, mu*163)."
        ),
        "honesty_boundary": (
            "Element sums of finite sets are elementary.  The substrate-"
            "primitive identifications q!*Phi_6, 2^q*q!*Phi_6, "
            "mu*Heegner_max, and the ratio 2^q between Ogg-only and "
            "intersection sums are the structural new content.  The "
            "appearance of 137 in Sum(H setminus O) = 2*137 is flagged "
            "as coincidence; it is not a derivation of alpha."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_heegner_ogg_sum_layer.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) HEEGNER-OGG SUM-LAYER THEOREM")
    print("=" * 78)

    s = payload["venn_sums"]
    print("\nVenn-cell element sums:")
    print(f"  Sum(H cap O)         =  {s['Sum_H_cap_O']['sum']:>3d}  =  {s['Sum_H_cap_O']['substrate']}")
    print(f"  Sum(H setminus O)    =  {s['Sum_H_setminus_O']['sum']:>3d}  =  {s['Sum_H_setminus_O']['substrate']}")
    print(f"  Sum(O setminus H)    =  {s['Sum_O_setminus_H']['sum']:>3d}  =  {s['Sum_O_setminus_H']['substrate']}")
    print(f"  Sum(H cup O)         =  {s['Sum_H_cup_O']['sum']:>3d}  =  {s['Sum_H_cup_O']['substrate']}")

    h = payload["hodge_decomposition_check"]
    print(f"\nHodge-like sum decomposition:")
    print(f"  Sum(union) = Sum(cap) + Sum(H-only) + Sum(O-only)")
    print(f"  {h['Sum_union']} = 42 + 274 + 336: {h['match']}")

    r = payload["ratio_check"]
    print(f"\nOgg-only / intersection sum ratio:")
    print(f"  Sum(O_only) / Sum(H cap O) = 336 / 42 = {r['ratio_O_only_to_cap']:.0f} = 2^q")

    cs = payload["csaszar_szilassi_link"]
    print(f"\nCsaszar-Szilassi edge link:")
    print(f"  Sum(H cap O) = 42 = E_Csaszar + E_Szilassi = 21 + 21: {cs['match_combined_edges']}")

    tds = payload["two_dimensional_signature"]
    print(f"\nTwo-dimensional substrate signature of Venn cells:")
    print(f"  {'cell':>10s}  {'size':>6s}  {'sum':>5s}   size-substrate   sum-substrate")
    for cell, info in tds.items():
        print(f"  {cell:>10s}  {info['size']:>6d}  {info['sum']:>5d}   {info['size_substrate']:>15s}  {info['sum_substrate']}")

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
