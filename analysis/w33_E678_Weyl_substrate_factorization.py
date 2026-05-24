"""W(3,3) E_6/E_7/E_8 WEYL-GROUP ORDER SUBSTRATE FACTORIZATION THEOREM.

A new outside-the-box identification: the orders of the Weyl groups
W(E_6), W(E_7), W(E_8) all factor EXACTLY into the W(3,3) substrate
primitives q^q (Heisenberg-Weyl order), 2^q (substrate byte), Phi_6
(Fano points / octonion imaginaries), and |E| = 240 (W33 edge count).

THE THREE FACTORIZATIONS.
==========================

  |W(E_6)|  =  51,840
            =  q^q  *  2^q  *  |E|
            =  27   *  8    *  240

  |W(E_7)|  =  2,903,040
            =  q^q  *  2^(2q)  *  Phi_6  *  |E|
            =  27   *  64       *  7      *  240

  |W(E_8)|  =  696,729,600
            =  q^q  *  2^(2q)  *  Phi_6  *  |E|^2
            =  27   *  64       *  7      *  57,600

ALL THREE WEYL ORDERS FACTOR EXACTLY INTO {q^q, 2^q, Phi_6, |E|}.

SUBSTRATE LADDER STRUCTURE.
============================

Going up the exceptional series E_6 -> E_7 -> E_8:

  |W(E_7)| / |W(E_6)|  =  Phi_6 * 2^q  =  7 * 8  =  56
  |W(E_8)| / |W(E_7)|  =  |E|          =  240    =  W(3,3) edge count

Each Weyl-group enlargement multiplies by a SUBSTRATE PRIMITIVE:
  E_6 -> E_7:   factor  =  Phi_6 * 2^q       (Fano-pt * substrate-byte)
  E_7 -> E_8:   factor  =  |E|                (W(3,3) edges)

CROSS-CHECK WITH STANDARD FACTORIZATIONS.
==========================================

The classical prime factorizations of the Weyl orders are:

  |W(E_6)|  =  2^7  *  3^4  *  5
  |W(E_7)|  =  2^10 *  3^4  *  5  *  7
  |W(E_8)|  =  2^14 *  3^5  *  5^2  *  7

Substrate-primitive factorizations match exactly:

  q^q = 3^3,  2^q = 2^3,  2^(2q) = 2^6,  Phi_6 = 7,  |E| = 2^4 * 3 * 5

  q^q * 2^q * |E|
    =  3^3 * 2^3 * 2^4 * 3 * 5
    =  2^7 * 3^4 * 5
    =  51,840  =  |W(E_6)|   CHECK

  q^q * 2^(2q) * Phi_6 * |E|
    =  3^3 * 2^6 * 7 * 2^4 * 3 * 5
    =  2^10 * 3^4 * 5 * 7
    =  2,903,040  =  |W(E_7)|   CHECK

  q^q * 2^(2q) * Phi_6 * |E|^2
    =  3^3 * 2^6 * 7 * 2^8 * 3^2 * 5^2
    =  2^14 * 3^5 * 5^2 * 7
    =  696,729,600  =  |W(E_8)|   CHECK

CONNECTION TO BINARY POLYHEDRAL TOWER (MCCXLVII).
====================================================

MCCXLVII established the binary polyhedral / E-type / Golay tower:

  Heisenberg(F_3) (= |order q^q = 27)
   subset Hessian (order q!^3 = 216)
   subset W(E_6) (order 51840)

The Hessian order q!^3 = 216 = (mu+2)^3 factors as 6^3 = 2^3 * 3^3 =
2^q * q^q, equal to q^q * 2^q.

  |Hessian|       =  q^q * 2^q  =  216
  |W(E_6)|        =  q^q * 2^q * |E|  =  |Hessian| * |E|

So the W(E_6) order is the Hessian order multiplied by |E| (W33 edges).

CONNECTION TO E_8 = dim(E_8) + |E| (commit 752437be).
======================================================

The 24-cell / E_8 trinity established that dim(E_8) = 248, |E(24-cell)|
= 240, and the difference is rank(E_8) = 8.  Here we see another
incarnation of |E| = 240 as the factor that promotes |W(E_7)| to
|W(E_8)|.

CONNECTION TO TRIALITY AT GAMMA = 3 (MCCXL).
================================================

The factor Phi_6 = 7 appearing in |W(E_7)|/|W(E_6)| ties the
exceptional-Lie ladder to the Fano-plane triality / G_2 octonion
structure (MCCXXI).  The 2^q factor (= 8) is the same byte-count
appearing as W(3,3) octant count and the substrate's even-byte
structure.

ALTERNATIVE READING IN POWERS.
================================

Read as substrate exponential structure:

  |W(E_6)|  =  q^q * 2^q * 2^mu * q * (q+2)  =  q^q * 2^{q+mu} * q * (q+2)
            =  q^q * 2^7 * q * 5
            (since |E| = 240 = 2^mu * 2^q * q * (q+2) = 16 * 15 = 240)

But the substrate ladder reading (q^q, 2^q, Phi_6, |E|) is cleaner.

WHY THIS IS OUTSIDE THE BOX.
==============================

The Weyl-group orders for E_6, E_7, E_8 are computed in countless
references via root systems and Coxeter graphs.  Their substrate-
primitive factorization through W(3,3) quantities (q^q, 2^q, Phi_6,
|E|) is the structural new content.

In particular, the appearance of |E| = 240 (= W(3,3) edges) as the
factor going from W(E_7) to W(E_8) is a direct exceptional-Lie /
W(3,3) bridge: the W(3,3) graph's edge count IS the index of
W(E_7) in W(E_8).

The factor q^q = 27 = |Heis(F_3)| appears uniformly across all three
W(E_n) orders, tying the Heisenberg-Weyl substrate to the entire
E-type Weyl tower.
"""
from __future__ import annotations

import json
from pathlib import Path


Q = 3
MU = 4
K_CODEC = Q * MU
P_IH = K_CODEC - 1
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
F = 24
G_NEG = 15
V = 40
EDGES = 240

W_E6_ORDER = 51_840
W_E7_ORDER = 2_903_040
W_E8_ORDER = 696_729_600


def factorization_checks() -> list[dict]:
    rows = []

    # E_6
    rhs_E6 = (Q ** Q) * (2 ** Q) * EDGES
    rows.append({
        "Weyl_group": "W(E_6)",
        "order":       W_E6_ORDER,
        "factorization": "q^q * 2^q * |E|",
        "computed":    rhs_E6,
        "match":       rhs_E6 == W_E6_ORDER,
        "values":      f"{Q**Q} * {2**Q} * {EDGES}",
    })

    # E_7
    rhs_E7 = (Q ** Q) * (2 ** (2 * Q)) * PHI6 * EDGES
    rows.append({
        "Weyl_group": "W(E_7)",
        "order":       W_E7_ORDER,
        "factorization": "q^q * 2^(2q) * Phi_6 * |E|",
        "computed":    rhs_E7,
        "match":       rhs_E7 == W_E7_ORDER,
        "values":      f"{Q**Q} * {2**(2*Q)} * {PHI6} * {EDGES}",
    })

    # E_8
    rhs_E8 = (Q ** Q) * (2 ** (2 * Q)) * PHI6 * (EDGES ** 2)
    rows.append({
        "Weyl_group": "W(E_8)",
        "order":       W_E8_ORDER,
        "factorization": "q^q * 2^(2q) * Phi_6 * |E|^2",
        "computed":    rhs_E8,
        "match":       rhs_E8 == W_E8_ORDER,
        "values":      f"{Q**Q} * {2**(2*Q)} * {PHI6} * {EDGES**2}",
    })

    return rows


def substrate_ratios() -> dict:
    return {
        "W_E7_over_W_E6": {
            "value": W_E7_ORDER // W_E6_ORDER,
            "substrate": "Phi_6 * 2^q",
            "expected": PHI6 * (2 ** Q),
            "match": W_E7_ORDER // W_E6_ORDER == PHI6 * (2 ** Q),
        },
        "W_E8_over_W_E7": {
            "value": W_E8_ORDER // W_E7_ORDER,
            "substrate": "|E| = W(3,3) edge count",
            "expected": EDGES,
            "match": W_E8_ORDER // W_E7_ORDER == EDGES,
        },
    }


def prime_factorization_match() -> list[dict]:
    return [
        {"Weyl": "W(E_6)", "standard": "2^7 * 3^4 * 5",
         "substrate": "q^q * 2^q * |E| = 2^7 * 3^4 * 5"},
        {"Weyl": "W(E_7)", "standard": "2^10 * 3^4 * 5 * 7",
         "substrate": "q^q * 2^(2q) * Phi_6 * |E| = 2^10 * 3^4 * 5 * 7"},
        {"Weyl": "W(E_8)", "standard": "2^14 * 3^5 * 5^2 * 7",
         "substrate": "q^q * 2^(2q) * Phi_6 * |E|^2 = 2^14 * 3^5 * 5^2 * 7"},
    ]


def connection_to_hessian() -> dict:
    hessian_order = 216
    return {
        "Hessian_order":      hessian_order,
        "substrate":          "q^q * 2^q = q!^3 = 216",
        "match_substrate":    hessian_order == (Q ** Q) * (2 ** Q),
        "match_q_factorial_cubed": hessian_order == 6 ** 3,
        "W_E6_over_Hessian": W_E6_ORDER // hessian_order,
        "ratio_substrate":    f"|E| = {EDGES}",
        "match_ratio":        W_E6_ORDER // hessian_order == EDGES,
    }


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "k": K_CODEC, "p_Ih": P_IH,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6,
                "f": F, "g_neg": G_NEG, "v": V, "edges": EDGES,
            },
            "Weyl_orders": {
                "W_E_6": W_E6_ORDER,
                "W_E_7": W_E7_ORDER,
                "W_E_8": W_E8_ORDER,
            },
        },
        "factorization_checks":         factorization_checks(),
        "substrate_ratios":             substrate_ratios(),
        "prime_factorization_match":    prime_factorization_match(),
        "connection_to_hessian":        connection_to_hessian(),
        "theorem": (
            "W(3,3) E_6/E_7/E_8 Weyl-Group Order Substrate Factorization "
            "Theorem.  The Weyl-group orders factor exactly into the "
            "W(3,3) substrate primitives q^q (Heisenberg-Weyl), 2^q "
            "(substrate byte), Phi_6 (Fano points), |E| (W33 edges): "
            "|W(E_6)| = q^q * 2^q * |E|, |W(E_7)| = q^q * 2^(2q) * Phi_6 "
            "* |E|, |W(E_8)| = q^q * 2^(2q) * Phi_6 * |E|^2.  The "
            "exceptional-Lie ladder ratios are |W(E_7)|/|W(E_6)| = "
            "Phi_6 * 2^q and |W(E_8)|/|W(E_7)| = |E|, so the W(3,3) "
            "edge count IS the index of W(E_7) in W(E_8) and the Fano-"
            "point count times substrate-byte is the index of W(E_6) "
            "in W(E_7)."
        ),
        "honesty_boundary": (
            "Weyl-group orders are classical (Coxeter, Bourbaki).  "
            "Their factorizations into prime powers are standard.  "
            "The substrate-primitive identifications q^q = 27, 2^q = 8, "
            "Phi_6 = 7, |E| = 240, and the uniform appearance of these "
            "four (and only these four) factors across W(E_6), W(E_7), "
            "W(E_8) are the structural new content -- in particular, "
            "the identification of the W(E_7)->W(E_8) index as exactly "
            "the W(3,3) edge count |E|."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_E678_Weyl_substrate_factorization.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) E_6/E_7/E_8 WEYL-GROUP ORDER SUBSTRATE FACTORIZATION")
    print("=" * 78)

    print("\nFactorizations:")
    for r in payload["factorization_checks"]:
        print(f"  |{r['Weyl_group']}|  =  {r['order']:>12,d}  =  {r['factorization']}")
        print(f"      =  {r['values']}  ({r['match']})")

    print("\nSubstrate ladder ratios:")
    r = payload["substrate_ratios"]
    print(f"  |W(E_7)| / |W(E_6)|  =  {r['W_E7_over_W_E6']['value']}  =  {r['W_E7_over_W_E6']['substrate']}")
    print(f"  |W(E_8)| / |W(E_7)|  =  {r['W_E8_over_W_E7']['value']}  =  {r['W_E8_over_W_E7']['substrate']}")

    print("\nPrime-factorization comparison:")
    for p in payload["prime_factorization_match"]:
        print(f"  {p['Weyl']:>8s}: standard {p['standard']:>22s}  /  substrate {p['substrate']}")

    print("\nConnection to Hessian group (MCCXLVII):")
    h = payload["connection_to_hessian"]
    print(f"  |Hessian|  =  {h['Hessian_order']}  =  q^q * 2^q  =  q!^3")
    print(f"  |W(E_6)| / |Hessian|  =  {h['W_E6_over_Hessian']}  =  |E|")
    print(f"  So W(E_6) = Hessian extended by W(3,3) edge count.")

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
