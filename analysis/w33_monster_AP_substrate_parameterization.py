"""W(3,3) MONSTER-REP AP SUBSTRATE PARAMETERIZATION THEOREM.

A new outside-the-box identification advancing MCCXLIX (Monster Module
E6-AP Decomposition).  The AP {47, 59, 71} of MCCXLVIII, whose product
196883 = dim(V^natural) - 1 (McKay), admits an EXACT substrate
parameterization through W(3,3) primitives:

  47  =  mu * k - 1   =  4 * 12 - 1
  59  =  (mu + 1) * k - 1   =  5 * 12 - 1
  71  =  q! * k - 1   =  6 * 12 - 1

The three multipliers (mu, mu+1, q!) are THREE CONSECUTIVE INTEGERS,
each substrate-primitive:

  mu     =  4      (substrate co-quantum)
  mu + 1 =  5      (Csaszar realization count)
  q!     =  6      (= mu + 2 = perm symmetry of 3 elements)

So the entire Monster-rep AP is a substrate ladder

  AP_i  =  (mu + i - 1) * k - 1     for i in {1, 2, 3}

with i indexing through three substrate-meaningful consecutive
multipliers.

THE McKAY COEFFICIENT.
======================

  dim(V^natural) - 1  =  196883
                      =  47 * 59 * 71
                      =  (mu*k - 1)((mu+1)*k - 1)(q!*k - 1)
                      =  (4k-1)(5k-1)(6k-1)

Expanded:
  196883  =  120k^3 - 74k^2 + 15k - 1
          =  k * Phi_4 * k^3 - 74k^2 + g_neg * k - 1

Substrate readings of the coefficients:
  120  =  k * Phi_4    (= Hodge boundary rank)
   74  =  (no clean substrate identification yet)
   15  =  g_neg         (chiral Hashimoto multiplicity)
    1  =  identity

SUM OF AP PRIMES.
=================

  47 + 59 + 71  =  177
                =  q * 59  =  q * (middle of AP)
                =  3 * (mu+1) * k - 3
                =  q * (mu+1) * k - q
                =  q * ((mu+1)*k - 1)
                =  q * Ogg_14

Sum of multipliers (4 + 5 + 6) = 15 = g_neg.  So:

  47 + 59 + 71  =  k * g_neg - q  =  12 * 15 - 3  =  177

OUTER VS INNER GAP.
====================

  Common difference of AP:  d   =  59 - 47  =  71 - 59  =  12  =  k
  Outer gap of AP:          D   =  71 - 47  =  24       =  f   =  gauge_mult

So the AP common difference is W(3,3) valency, and the outer gap is
the Hashimoto gauge sector multiplicity.

OGG MOD-4 SUBSTRATE DECOMPOSITION.
====================================

Splitting the 15 Ogg primes by residue mod 4:

  Ogg = 1 mod 4    {5, 13, 17, 29, 41}                size 5 = mu + 1
        (Pythagorean-eligible primes, Csaszar realiz. count)

  Ogg = 3 mod 4    {3, 7, 11, 19, 23, 31, 47, 59, 71} size 9 = q^2
        (not Pythagorean hypotenuses, equals |Heegner_9|)

  Ogg = 2 mod 4    {2}                                 size 1
        (the unique even Ogg prime)

  Total:           5 + 9 + 1                          = 15 = g_neg

Three substrate-primitive sizes summing to g_neg.  The Monster-rep
AP {47, 59, 71} lies entirely in the 3-mod-4 class.

PYTHAGOREAN COMPLEMENT.
========================

The 5 Pythagorean-hypotenuse Ogg primes {5, 13, 17, 29, 41} (all 1 mod 4)
are exactly the Ogg primes that CAN appear as Pythagorean hypotenuses
(Fermat's theorem: p = a^2 + b^2 iff p == 1 mod 4 or p == 2).

  17 = 4^2 + 1^2  (Ogg-Pythagorean-hypotenuse, commit dd1eb6fd)
  29 = 5^2 + 2^2
  41 = 5^2 + 4^2  (Pythagorean (40, 9, 41) with q^2 + (v/2)^2 readings)

The 5 = mu+1 Pythagorean-Ogg primes split further:
  small: 5, 13
  large: 17, 29, 41   (the substrate-Pythagorean hypotenuse triple)

CONNECTION TO MCCXLVIII / MCCXLIX.
====================================

MCCXLVIII established {47, 59, 71} as the Monster-rep AP with common
difference 12 = k = h(E_6).  MCCXLIX opens the question of how the
196883-dim rep decomposes with 47, 59, 71 as summand-dim indices.

This commit advances both by giving the explicit substrate
parameterization

  AP  =  ((mu)k - 1, (mu+1)k - 1, (q!)k - 1)

with consecutive multipliers mu, mu+1, q!.  The triple is now a
substrate object, not just an arithmetic AP -- it walks through
THREE consecutive integers (mu, mu+1, q!) at substrate multiplier
positions.

WHY THIS IS OUTSIDE THE BOX.
==============================

Decompositions of 196883 = dim(V^natural) - 1 are standard in
moonshine, but parameterizing the prime factorization 47*59*71 as
(mu*k-1)((mu+1)*k-1)(q!*k-1) makes the SUBSTRATE STRUCTURE explicit.
The Monster-rep AP is now a substrate ladder, indexed by three
consecutive integers (mu, mu+1, q!), with sum-of-multipliers = g_neg
and common difference = k.

The mod-4 decomposition (5, 9, 1) = (mu+1, q^2, 1) of Ogg primes
gives another substrate reading of g_neg = 15.
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


OGG_15 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71]
AP_PRIMES = [47, 59, 71]


def AP_substrate_param() -> list[dict]:
    return [
        {"prime": 47, "param": "mu * k - 1",     "rhs": MU * K_CODEC - 1,
         "multiplier": MU, "multiplier_substrate": "mu (co-quantum)"},
        {"prime": 59, "param": "(mu+1) * k - 1", "rhs": (MU + 1) * K_CODEC - 1,
         "multiplier": MU + 1, "multiplier_substrate": "mu+1 (Csaszar realiz.)"},
        {"prime": 71, "param": "q! * k - 1",     "rhs": QFACT * K_CODEC - 1,
         "multiplier": QFACT, "multiplier_substrate": "q! = mu + 2"},
    ]


def check_param() -> dict:
    results = []
    for r in AP_substrate_param():
        results.append({
            "prime": r["prime"],
            "param": r["param"],
            "computed": r["rhs"],
            "match": r["prime"] == r["rhs"],
        })
    all_match = all(r["match"] for r in results)
    return {"results": results, "all_match": all_match}


def McKay_factorization() -> dict:
    cubic_lhs = 47 * 59 * 71
    cubic_rhs_at_k = (
        (MU * K_CODEC - 1)
        * ((MU + 1) * K_CODEC - 1)
        * (QFACT * K_CODEC - 1)
    )
    return {
        "dim_V_natural_minus_1": 196883,
        "product_lhs": cubic_lhs,
        "product_rhs_from_param": cubic_rhs_at_k,
        "match": cubic_lhs == cubic_rhs_at_k == 196883,
        "expanded_form": "(4k-1)(5k-1)(6k-1) = 120k^3 - 74k^2 + 15k - 1",
        "coefficient_120_substrate": "k * Phi_4 = 12 * 10",
        "coefficient_15_substrate":  "g_neg (chiral Hashimoto mult.)",
    }


def AP_sums() -> dict:
    s = sum(AP_PRIMES)
    return {
        "sum_of_AP": s,
        "equals_q_times_middle": s == Q * 59,
        "equals_k_times_g_neg_minus_q": s == K_CODEC * G_NEG - Q,
        "substrate_form": "k * g_neg - q",
        "AP_common_difference": 59 - 47,
        "AP_common_diff_substrate": f"k = {K_CODEC} (W33 valency)",
        "AP_outer_gap": 71 - 47,
        "AP_outer_gap_substrate": f"f = gauge_mult = {F}",
    }


def ogg_mod_4_split() -> dict:
    one_mod_4 = [p for p in OGG_15 if p % 4 == 1]
    three_mod_4 = [p for p in OGG_15 if p % 4 == 3]
    two_mod_4 = [p for p in OGG_15 if p % 4 == 2]
    return {
        "Ogg_1_mod_4": {
            "primes": one_mod_4,
            "size": len(one_mod_4),
            "substrate": "mu + 1 (Csaszar realization count)",
            "match": len(one_mod_4) == MU + 1,
            "comment": "Pythagorean-eligible (sum of two squares)",
        },
        "Ogg_3_mod_4": {
            "primes": three_mod_4,
            "size": len(three_mod_4),
            "substrate": "q^2 (= |Heegner_9|)",
            "match": len(three_mod_4) == Q * Q,
            "comment": "Not Pythagorean hypotenuses; contains Monster-rep AP",
        },
        "Ogg_2_mod_4": {
            "primes": two_mod_4,
            "size": len(two_mod_4),
            "substrate": "1 (unique even Ogg prime)",
            "match": len(two_mod_4) == 1,
        },
        "sum_check": {
            "total": len(one_mod_4) + len(three_mod_4) + len(two_mod_4),
            "equals_g_neg": (len(one_mod_4) + len(three_mod_4) + len(two_mod_4)) == G_NEG,
        },
    }


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "q_factorial": QFACT,
                "k": K_CODEC, "p_Ih": P_IH,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6,
                "f": F, "g_neg": G_NEG,
            },
            "AP_primes": AP_PRIMES,
            "Ogg_15": OGG_15,
        },
        "AP_substrate_parameterization": AP_substrate_param(),
        "param_check":                    check_param(),
        "McKay_factorization":            McKay_factorization(),
        "AP_sums":                        AP_sums(),
        "ogg_mod_4_split":                ogg_mod_4_split(),
        "theorem": (
            "W(3,3) Monster-Rep AP Substrate Parameterization Theorem.  "
            "The Monster-rep AP {47, 59, 71} (MCCXLVIII) admits the exact "
            "substrate parameterization (mu*k - 1, (mu+1)*k - 1, q!*k - 1) "
            "= ((4)(12)-1, (5)(12)-1, (6)(12)-1), with three consecutive "
            "substrate multipliers mu, mu+1, q!.  The McKay coefficient "
            "factorizes as 196883 = (mu*k-1)((mu+1)*k-1)(q!*k-1), the "
            "AP-sum is k*g_neg - q, the common difference is k, and "
            "the outer gap is f = gauge_mult.  The Ogg primes themselves "
            "split mod 4 into (5, 9, 1) = (mu+1, q^2, 1) classes, with "
            "the entire Monster-rep AP residing in the q^2-size 3-mod-4 "
            "class.  This advances MCCXLIX from arithmetic curiosity "
            "to substrate ladder."
        ),
        "honesty_boundary": (
            "The arithmetic identities 47 = 4*12 - 1, 59 = 5*12 - 1, "
            "71 = 6*12 - 1 are trivial.  The substrate interpretation "
            "of (4, 5, 6) as (mu, mu+1, q!) makes the AP a substrate "
            "ladder; the cubic expansion's coefficient 120 = k*Phi_4 "
            "ties it to the Hodge boundary; and the mod-4 split of "
            "Ogg primes gives an independent substrate decomposition "
            "of g_neg = 15.  The 74k^2 coefficient has no current "
            "substrate identification."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_monster_AP_substrate_parameterization.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) MONSTER-REP AP SUBSTRATE PARAMETERIZATION THEOREM")
    print("=" * 78)

    print("\nAP substrate parameterization:")
    for r in AP_substrate_param():
        print(f"  {r['prime']:>2d} = {r['param']:>15s}  =  {r['rhs']:>2d}   (mult = {r['multiplier_substrate']})")

    print("\nMcKay coefficient factorization:")
    m = payload["McKay_factorization"]
    print(f"  196883 = (mu*k - 1)((mu+1)*k - 1)(q!*k - 1)")
    print(f"         = (4*12-1)(5*12-1)(6*12-1) = 47*59*71 = {m['product_lhs']}")
    print(f"         = {m['expanded_form']}")
    print(f"         match: {m['match']}")

    print("\nAP sums and gaps:")
    s = payload["AP_sums"]
    print(f"  47+59+71 = {s['sum_of_AP']} = k*g_neg - q = q * Ogg_14")
    print(f"  common diff = {s['AP_common_difference']} = k (W33 valency)")
    print(f"  outer gap   = {s['AP_outer_gap']} = f = gauge_mult")

    print("\nOgg mod-4 substrate decomposition:")
    o = payload["ogg_mod_4_split"]
    print(f"  Ogg = 1 mod 4: {o['Ogg_1_mod_4']['primes']}  ({o['Ogg_1_mod_4']['substrate']})")
    print(f"  Ogg = 3 mod 4: {o['Ogg_3_mod_4']['primes']}")
    print(f"                  ({o['Ogg_3_mod_4']['substrate']})")
    print(f"  Ogg = 2 mod 4: {o['Ogg_2_mod_4']['primes']}  ({o['Ogg_2_mod_4']['substrate']})")
    print(f"  Total:          {o['sum_check']['total']} = g_neg")

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
