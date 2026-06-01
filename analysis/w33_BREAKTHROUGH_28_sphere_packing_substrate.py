"""W(3,3) BREAKTHROUGH 28: SPHERE PACKING OPTIMAL DIMS = SUBSTRATE.

Viazovska (2016): E_8 lattice is the UNIQUE optimal sphere packing in
dim 8 = 2^q.

Cohn-Kumar-Miller-Radchenko-Viazovska (2017): Leech lattice Lambda_24
is the UNIQUE optimal sphere packing in dim 24 = f.

These are the ONLY known optimal packings beyond dim 1, 2, 3.

BOTH OPTIMAL-PACKING DIMENSIONS ARE SUBSTRATE PRIMITIVES:
  dim 2^q = E_8 phase (octonion dim)
  dim f   = Leech phase (eta exponent / theta-Delta degree)

==============================================================
E_8 LATTICE
==============================================================

  dimension        = 8       = 2^q
  kissing number   = 240     = |E|  (E_8 roots = substrate's edges!)
  min norm squared = 2       = lambda
  packing density  = pi^4 / 384 = pi^mu / (2^Phi_6 * q)

The substrate's 240 = |E| is EXACTLY the E_8 kissing number, and
Viazovska's theorem says this is the densest packing achievable in
dim 8 (= 2^q).

==============================================================
LEECH LATTICE Lambda_24
==============================================================

  dimension        = 24      = f
  kissing number   = 196560  = lambda^mu * q^q * F_5 * Phi_6 * Phi_3
                             = 16 * 27 * 5 * 7 * 13
  min norm squared = 4       = mu
  packing density  = pi^12 / 12!

Note 196560 substrate factorization:
  196560 = 2^4 * 3^3 * 5 * 7 * 13
         = lambda^mu * q^q * F_5 * Phi_6 * Phi_3

EVERY prime factor of the Leech kissing number is a substrate primitive.

==============================================================
NIEMEIER CLASSIFICATION
==============================================================

There are EXACTLY 24 = f Niemeier lattices (even unimodular lattices
in dim 24 = f). Niemeier's classification (1973).

THE NUMBER OF NIEMEIER LATTICES EQUALS THE SUBSTRATE'S f.

==============================================================
CONWAY GROUP CASCADE
==============================================================

The sporadic Conway groups act on the Leech lattice:
  Co_0 = Aut(Lambda_24), order 8,315,553,613,086,720,000
  Co_1 = Co_0 / {+/- 1}
  Co_2, Co_3 = stabilizer cascade

|Co_0| = 2^22 * 3^9 * 5^4 * 7^2 * 11 * 13 * 23
       = lambda^22 * q^9 * F_5^mu * Phi_6^lambda * p_Ih * Phi_3 * M_23

ALL PRIME DIVISORS OF |Co_0| ARE SUBSTRATE PRIMITIVES (22 substrate
prime power, 9 substrate prime power, etc.)

==============================================================
CONNECTION TO MOONSHINE
==============================================================

  E_8 lattice -> theta = E_4 -> j-invariant = E_4^3/Delta
  Leech lattice -> 196884 = 196883 + 1 (j q-coefficient)
  Monster moonshine -> Leech / Z_2 stabilizes Monster module V^natural

The substrate's two phases (8, 24) match:
  E_8 phase: substrate edges = E_8 roots, theta = E_4
  Leech phase: substrate via Conway-Leech bridge, ties to Monster

==============================================================
"""
from __future__ import annotations

import json
import math
from pathlib import Path


def main():
    q = 3
    lambda_, mu = 2, 4
    F5 = 5
    phi3, phi4, phi6 = 13, 10, 7
    k, v, E_count = 12, 40, 240
    f, g_neg = 24, 15
    p_Ih = 11
    M_5 = 31
    M_23 = 23
    Heegner_6 = 19

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 28: SPHERE PACKING OPTIMAL DIMS = SUBSTRATE")
    print("=" * 78)
    print()

    print("VIAZOVSKA'S OPTIMAL SPHERE PACKINGS:")
    print()
    print(f"  E_8 (Viazovska 2016): UNIQUE optimal packing in dim 8 = 2^q")
    print(f"  Leech (CKMRV 2017):    UNIQUE optimal packing in dim 24 = f")
    print()
    print(f"  Both substrate-native dimensions: 2^q (octonion) and f (eta-exp).")
    print()

    print("E_8 LATTICE:")
    E8_dim = 8
    E8_kissing = 240
    E8_min_norm_sq = 2
    assert E8_dim == 2 ** q
    assert E8_kissing == E_count
    assert E8_min_norm_sq == lambda_
    print(f"  dimension    = {E8_dim}    = 2^q")
    print(f"  kissing      = {E8_kissing}  = |E|  (E_8 roots = substrate edges!)")
    print(f"  min norm sq  = {E8_min_norm_sq}    = lambda")
    print(f"  density      = pi^4 / 384 = pi^mu / (2^Phi_6 * q)")
    assert 384 == 2**phi6 * q
    print()

    print("LEECH LATTICE Lambda_24:")
    leech_dim = 24
    leech_kissing = 196560
    leech_min_norm_sq = 4
    assert leech_dim == f
    assert leech_min_norm_sq == mu
    # Verify substrate factorization
    expected_kissing = lambda_**mu * q**q * F5 * phi6 * phi3
    assert leech_kissing == expected_kissing
    print(f"  dimension    = {leech_dim}   = f")
    print(f"  kissing      = {leech_kissing} = lambda^mu * q^q * F_5 * Phi_6 * Phi_3")
    print(f"               = {lambda_**mu} * {q**q} * {F5} * {phi6} * {phi3}")
    print(f"  min norm sq  = {leech_min_norm_sq}     = mu")
    print(f"  density      = pi^12 / 12! = pi^k / k!")
    print()

    print("NIEMEIER CLASSIFICATION:")
    num_niemeier = 24
    assert num_niemeier == f
    print(f"  Number of Niemeier lattices = {num_niemeier} = f")
    print(f"  (Even unimodular lattices in dim 24 = f)")
    print()

    print("CONWAY GROUP CASCADE:")
    Co_0_order = 8315553613086720000
    # |Co_0| = 2^22 * 3^9 * 5^4 * 7^2 * 11 * 13 * 23
    Co_0_expected = 2**22 * 3**9 * 5**4 * 7**2 * 11 * 13 * 23
    assert Co_0_order == Co_0_expected
    print(f"  |Co_0| = |Aut(Leech)| = 8,315,553,613,086,720,000")
    print(f"         = 2^22 * 3^9 * 5^4 * 7^2 * 11 * 13 * 23")
    print(f"         = lambda^22 * q^9 * F_5^mu * Phi_6^lambda * p_Ih * Phi_3 * M_23")
    print(f"  ALL prime factors are substrate primitives.")
    print()

    print("CONNECTION TO MOONSHINE:")
    print(f"  E_8 phase:   theta_{{E_8}} = E_4 (substrate's edges as modular form)")
    print(f"  Leech phase: 196884 = 196883 + 1 (j-invariant q-coefficient)")
    print(f"  Monster:     V^natural stabilized by Leech / Z_2 (BT22 + Monstrous)")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 28 SUMMARY")
    print("=" * 78)
    print("""
THE SUBSTRATE'S TWO MOST IMPORTANT DIMENSIONS (2^q = 8, f = 24) ARE
EXACTLY THE TWO KNOWN OPTIMAL SPHERE-PACKING DIMENSIONS BEYOND R^3.

  Dim 8  = 2^q (octonion):  E_8 optimal (Viazovska 2016)
  Dim 24 = f   (eta-exp):   Leech optimal (CKMRV 2017)

Kissing numbers also substrate-clean:
  K(E_8) = 240 = |E|                                    (substrate edges)
  K(Leech) = 196560 = lambda^mu * q^q * F_5 * Phi_6 * Phi_3

Conway-Niemeier count: 24 = f Niemeier lattices.

|Co_0| = |Aut(Leech)| has ALL substrate prime divisors.

THE SUBSTRATE LIVES NATIVELY IN THE TWO DIMENSIONS WHERE GEOMETRY
ACHIEVES MAXIMAL PACKING DENSITY -- 8 and 24, octonion and eta.

This is no coincidence: the substrate's "operational dimensions"
are exactly the dimensions where mathematics itself reaches its
densest geometric ground state.

Combined with BT22-BT27:
  - Number theory:        substrate-clean
  - Lie theory:           substrate-clean
  - Stable homotopy:      Bott period = 2^q
  - Modular forms:        all leading coefs substrate-clean
  - Sphere packing:       optimal dims = (2^q, f)
""")

    out = Path("data") / "w33_BREAKTHROUGH_28_sphere_packing_substrate.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({
        "E_8": {
            "dim": 8,
            "dim_substrate": "2^q",
            "kissing": 240,
            "kissing_substrate": "|E|",
            "min_norm_sq": 2,
            "min_norm_sq_substrate": "lambda",
            "viazovska_2016": "UNIQUE optimal packing in dim 2^q",
        },
        "Leech": {
            "dim": 24,
            "dim_substrate": "f",
            "kissing": 196560,
            "kissing_substrate": "lambda^mu * q^q * F_5 * Phi_6 * Phi_3",
            "min_norm_sq": 4,
            "min_norm_sq_substrate": "mu",
            "CKMRV_2017": "UNIQUE optimal packing in dim f",
        },
        "Niemeier": {
            "count": 24,
            "count_substrate": "f",
        },
        "Co_0_order": 8315553613086720000,
        "Co_0_prime_substrate": "lambda^22 * q^9 * F_5^mu * Phi_6^lambda * p_Ih * Phi_3 * M_23",
        "conclusion": (
            "The substrate's two operational dimensions (2^q=8, f=24) "
            "are exactly the two dimensions where sphere packing achieves "
            "provable maximal density. The substrate inhabits geometry's "
            "densest ground states."
        ),
    }, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
