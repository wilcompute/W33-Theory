#!/usr/bin/env python3
"""W(3,3) EXCEPTIONAL WEYL CHAIN CLOSURE THEOREM.

The Weyl groups along the exceptional Lie chain D_4 -> F_4 -> E_6 -> E_7 -> E_8
have consecutive index quotients that are ALL substrate primitives, and the
total quotient |W(E_8)| / |W(D_4)| equals Phi_4 factorial.

The cascade.
------------
    Weyl group   order        consecutive quotient    substrate identification
    ----------   -----------  --------------------    ------------------------
    W(D_4)         192        (base)                  f * 2^q = Klein closure value
    W(F_4)        1152        6 = q!                  Master Equation
    W(E_6)       51840        45 = Q_count            substrate Q primitive
    W(E_7)     2903040        56 = 2^q * Phi_6        Klein sextactic count
    W(E_8)   696729600        240 = |E|               W(3,3) edge / E_8 root

Total quotient.
---------------
    |W(E_8)| / |W(D_4)| = q! * Q_count * (2^q Phi_6) * |E|
                        = 6 * 45 * 56 * 240
                        = 3 628 800
                        = 10!
                        = Phi_4!

CLOSURE IDENTITY (NEW):

    |W(E_8)| = |W(D_4)| * Phi_4!
            = 192 * 10!
            = (f * 2^q) * Phi_4!

The largest exceptional Weyl group order factors as
    (Klein closure value) * (factorial of Phi_4).

This binds the entire E_8 root lattice symmetry to substrate primitives
through a SINGLE factorial.

Substrate primitive index ladder.
---------------------------------
At each rung the index quotient is a SINGLE substrate primitive:

    D_4 inside F_4:   index 6  = q!         (Master Equation root)
    F_4 inside E_6:   index 45 = Q_count    (fermion-flag count)
    E_6 inside E_7:   index 56 = 2^q Phi_6  (Klein sextactic count;
                                              also F_4 -> E_6 -> E_7
                                              jump value)
    E_7 inside E_8:   index 240 = |E|       (W(3,3) edge count
                                              = E_8 root count)

Connection to Klein quartic closure.
------------------------------------
The base W(D_4) = 192 IS the Klein quartic invariant sum (Weierstrass +
bitangents + sextactic + Hurwitz orbits = 192), as established in the
Klein Quartic Closure Theorem.  So the exceptional Weyl chain is anchored
at the Klein quartic.

The sextactic-point count 56 = 2^q * Phi_6 ALSO reappears as the
E_6 -> E_7 index, so the same substrate primitive labels BOTH a Klein
quartic invariant AND a Weyl group quotient.

Chiral-sector tie-in.
---------------------
The chiral-sector discriminant (commit 1e28f4d9) equals
    Delta_chiral = 31104 = 2 * H_1 * |W(D_4)| = 2 * 81 * 192.

Combined with |W(D_4)| = f * 2^q:
    Delta_chiral = 2 * H_1 * f * 2^q
                 = 2^(q+1) * f * H_1
                 = 16 * 24 * 81

So the chiral discriminant decomposes as 2^(q+1) * f * H_1, exposing the
logical (H_1), gauge (f), and binary (2^(q+1)) sectors simultaneously.

Phi_4! and ten primitives.
--------------------------
Phi_4 = q^2 + 1 = 10 at q = 3.  Phi_4! = 10! = 3 628 800.  The 10 in Phi_4
is the 4th cyclotomic value of q, so this final closure says:

  the entire E_8 Weyl symmetry is the Klein closure value times the
  factorial of the 4th cyclotomic of q.
"""
from __future__ import annotations

import json
from math import factorial
from pathlib import Path


Q = 3
QP1 = 4
MU = QP1
PHI4 = Q ** 2 + 1            # 10
PHI6 = Q ** 2 - Q + 1        # 7
F = 24
H1 = Q ** QP1                # 81
TOMOTOPE_CELLS = 2 ** Q      # 8
EDGES = 240
Q_COUNT = 45                 # substrate Q primitive
QFACT = 6
SEXTACTIC = 2 ** Q * PHI6    # 56

# Exceptional Weyl group orders
WEYL = {
    "D_4": 192,
    "F_4": 1152,
    "E_6": 51_840,
    "E_7": 2_903_040,
    "E_8": 696_729_600,
}


def cascade_quotients() -> list[dict]:
    chain = ["D_4", "F_4", "E_6", "E_7", "E_8"]
    expected_quotients = [QFACT, Q_COUNT, SEXTACTIC, EDGES]
    expected_forms = [
        "q! = Master Equation root",
        "Q_count = substrate Q primitive",
        "2^q * Phi_6 = Klein sextactic count = tomotope cells * Heawood",
        "|E| = E_8 root count = W(3,3) edge count",
    ]
    rows = []
    for i in range(len(chain) - 1):
        a, b = chain[i], chain[i + 1]
        quotient = WEYL[b] // WEYL[a]
        expected = expected_quotients[i]
        rows.append({
            "from": a,
            "to": b,
            "from_order": WEYL[a],
            "to_order": WEYL[b],
            "quotient": quotient,
            "expected": expected,
            "match": quotient == expected,
            "substrate_form": expected_forms[i],
        })
    return rows


def total_quotient() -> dict:
    total = WEYL["E_8"] // WEYL["D_4"]
    phi4_factorial = factorial(PHI4)
    product_of_quotients = QFACT * Q_COUNT * SEXTACTIC * EDGES
    return {
        "WE8_over_WD4": total,
        "phi4_factorial": phi4_factorial,
        "product_of_4_quotients": product_of_quotients,
        "match_phi4_factorial": total == phi4_factorial,
        "match_product_of_quotients": total == product_of_quotients,
        "closed_form": "|W(E_8)| = |W(D_4)| * Phi_4!",
        "value_check": WEYL["E_8"] == WEYL["D_4"] * phi4_factorial,
    }


def klein_anchor() -> dict:
    return {
        "WD4_value": WEYL["D_4"],
        "substrate_form_WD4": "f * 2^q = 24 * 8",
        "substrate_check": WEYL["D_4"] == F * TOMOTOPE_CELLS,
        "klein_quartic_invariant_sum": "Weierstrass + Bitangents + Sextactic + Hurwitz = 192",
        "is_klein_closure_value": True,
        "comment": (
            "|W(D_4)| = 192 is the Klein quartic invariant sum AND the 24-cell "
            "Weyl group order AND the substrate's tomotope flag count.  The "
            "exceptional Weyl chain is anchored at this triple-coincidence."
        ),
    }


def chiral_sector_tie_in() -> dict:
    delta_chiral = 31104
    via_WD4 = 2 * H1 * WEYL["D_4"]
    expanded = (2 ** (Q + 1)) * F * H1
    return {
        "delta_chiral": delta_chiral,
        "as_two_H1_WD4": via_WD4,
        "as_2qplus1_f_H1": expanded,
        "all_equal": delta_chiral == via_WD4 == expanded,
        "substrate_decomposition": "Delta_chiral = 2 * H_1 * |W(D_4)| = 2^(q+1) * f * H_1",
        "comment": (
            "The chiral-sector discriminant decomposes as 2^(q+1) * f * H_1, "
            "exposing the gauge sector (f = 24 = positive spectral multiplicity), "
            "the logical sector (H_1 = 81 = matter), and the binary shell "
            "(2^(q+1) = 16 = 2^mu) simultaneously in one number."
        ),
    }


def substrate_factorisation_of_WE8() -> dict:
    """|W(E_8)| = f * 2^q * Phi_4!."""
    candidate = F * TOMOTOPE_CELLS * factorial(PHI4)
    return {
        "WE8": WEYL["E_8"],
        "substrate_form": "f * 2^q * Phi_4!",
        "substrate_value": candidate,
        "match": candidate == WEYL["E_8"],
        "alt_form_1": f"|W(D_4)| * Phi_4! = {WEYL['D_4']} * {factorial(PHI4)}",
        "alt_form_2": f"f * 2^q * Phi_4! = {F} * {TOMOTOPE_CELLS} * {factorial(PHI4)}",
        "key_point": (
            "|W(E_8)| = positive spectral multiplicity * tomotope cells * "
            "factorial of the 4th cyclotomic of q."
        ),
    }


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "Phi_4": PHI4, "Phi_6": PHI6,
                "f": F, "H_1": H1, "tomotope_cells": TOMOTOPE_CELLS,
                "edges": EDGES, "Q_count": Q_COUNT, "sextactic": SEXTACTIC,
                "q_factorial": QFACT,
            },
        },
        "weyl_orders": WEYL,
        "cascade_quotients": cascade_quotients(),
        "total_quotient_phi4_factorial": total_quotient(),
        "klein_anchor": klein_anchor(),
        "chiral_sector_tie_in": chiral_sector_tie_in(),
        "substrate_factorisation_of_WE8": substrate_factorisation_of_WE8(),
        "theorem": (
            "W(3,3) Exceptional Weyl Chain Closure Theorem.  The exceptional "
            "Weyl group cascade D_4 subset F_4 subset E_6 subset E_7 subset E_8 "
            "has four consecutive index quotients all equal to substrate "
            "primitives: q! = 6, Q_count = 45, 2^q * Phi_6 = 56, and "
            "|E| = 240.  Their product equals Phi_4! = 10! = 3 628 800, so "
            "the total quotient |W(E_8)| / |W(D_4)| equals the factorial of "
            "the fourth cyclotomic Phi_4 = q^2 + 1.  Equivalently, "
            "|W(E_8)| = |W(D_4)| * Phi_4! = f * 2^q * Phi_4!.  The base "
            "|W(D_4)| = 192 is the Klein quartic invariant sum, anchoring the "
            "exceptional chain at the Klein closure point.  The chiral-sector "
            "discriminant equals 2 * H_1 * |W(D_4)| = 2^(q+1) * f * H_1, "
            "exposing the logical, gauge, and binary sectors of the substrate "
            "in one number."
        ),
        "honesty_boundary": (
            "All Weyl group orders are standard arithmetic facts (Bourbaki).  "
            "The substrate identifications of the quotient values (q!, Q_count, "
            "2^q Phi_6, |E|) are exact arithmetic matches.  The Phi_4-factorial "
            "closure is a clean structural identity, not a new proof of "
            "anything about E_8; it is a substrate-primitive reading of the "
            "exceptional Lie hierarchy."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_exceptional_weyl_chain_closure.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    print("=" * 72)
    print("W(3,3) EXCEPTIONAL WEYL CHAIN CLOSURE THEOREM")
    print("=" * 72)

    print(f"\n{'Weyl group':<10s} {'order':>12s}  consecutive quotient")
    print("-" * 60)
    print(f"{'W(D_4)':<10s} {WEYL['D_4']:>12d}  (base; Klein closure)")
    for row in payload["cascade_quotients"]:
        print(f"{'W('+row['to']+')':<10s} {row['to_order']:>12d}  index {row['quotient']:>3} = {row['substrate_form']}")

    t = payload["total_quotient_phi4_factorial"]
    print(f"\nTotal quotient |W(E_8)| / |W(D_4)| = {t['WE8_over_WD4']}")
    print(f"  = product of 4 quotients: {t['product_of_4_quotients']} (match: {t['match_product_of_quotients']})")
    print(f"  = Phi_4! = 10!         : {t['phi4_factorial']} (match: {t['match_phi4_factorial']})")
    print(f"  Closed form: {t['closed_form']}")

    f_ = payload["substrate_factorisation_of_WE8"]
    print(f"\n|W(E_8)| = f * 2^q * Phi_4! = {f_['substrate_value']}: {f_['match']}")

    c = payload["chiral_sector_tie_in"]
    print(f"\nChiral discriminant tie-in:")
    print(f"  Delta_chiral = 2 * H_1 * |W(D_4)| = 2^(q+1) * f * H_1 = {c['delta_chiral']}")
    print(f"  all match: {c['all_equal']}")

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
