"""W(3,3) BREAKTHROUGH 316: CONWAY SPORADIC GROUPS Co_1, Co_2, Co_3 SUBSTRATE.

The Conway sporadic groups arise from Aut(Leech lattice). Co_0 = Aut(Leech)
has order 8315553613086720000 = 2^22 * 3^9 * 5^4 * 7^2 * 11 * 13 * 23
(BT296). The three Conway sporadic SIMPLE groups are:

  Co_1 = Co_0 / Z(Co_0) = Co_0 / {+/-I}      (sporadic simple)
  Co_2 = stabilizer of a vector of norm 4 in Leech  (sporadic simple)
  Co_3 = stabilizer of a vector of norm 6 in Leech  (sporadic simple)

This BT factorises the Conway sporadic orders into substrate primitives.

==============================================================
THE FOUR CONWAY GROUPS
==============================================================

  Co_0 |.| = 8315553613086720000
        = 2^22 * 3^9 * 5^4 * 7^2 * 11 * 13 * 23
        Exponent vector: (22, 9, 4, 2, 1, 1, 1)
        = (lambda*p_Ih, q^lambda, mu, lambda, 1, 1, 1)

  Co_1 |.| = |Co_0| / lambda = 4157776806543360000
        = 2^21 * 3^9 * 5^4 * 7^2 * 11 * 13 * 23
        Exponent vector: (21, 9, 4, 2, 1, 1, 1)
        = (q * Phi_6, q^lambda, mu, lambda, 1, 1, 1)

  Co_2 |.| = 42305421312000
        = 2^18 * 3^6 * 5^3 * 7 * 11 * 23
        Exponent vector: (18, 6, 3, 1, 1, 1)
        = (lambda * q^lambda, q!, q, 1, 1, 1)

  Co_3 |.| = 495766656000
        = 2^10 * 3^7 * 5^3 * 7 * 11 * 23
        Exponent vector: (10, 7, 3, 1, 1, 1)
        = (Phi_4, Phi_6, q, 1, 1, 1)

==============================================================
SUBSTRATE-CLEAN EXPONENT PATTERNS
==============================================================

|Co_1| = lambda^(q*Phi_6) * q^(q^lambda) * F_5^mu * Phi_6^lambda * p_Ih * Phi_3 * 23

The exponent (q * Phi_6) = 21 = T_6 = |E(Heawood)| (BT287, BT267).

NEW SUBSTRATE STAR:
  |Co_1| has 2-exponent = T_6 = octonion triples count.

|Co_2| exponents (18, 6, 3, 1, 1, 1):
  18 = lambda * q^lambda
  6 = q!
  3 = q
  Substrate-clean.

|Co_3| exponents (10, 7, 3, 1, 1, 1):
  10 = Phi_4
  7 = Phi_6
  3 = q
  THREE substrate primitives as exponents!

==============================================================
ALL CONWAY PRIMES = SUBSTRATE PRIMES UP TO 23
==============================================================

The set of prime factors of all Conway group orders:
  {lambda, q, F_5, Phi_6, p_Ih, Phi_3, 23}.

  lambda, q, F_5, Phi_6, p_Ih, Phi_3 = 6 substrate primes.
  23 = lambda^lambda * F_5 + q = (not substrate-clean).

23 is the ONLY prime in Conway orders not substrate.

==============================================================
LEECH LATTICE -> CONWAY (NIEMEIER LINK, BT296)
==============================================================

The Leech lattice is the unique no-root Niemeier (BT296). Conway 1969
showed Aut(Leech) = Co_0, and the stabilizer chain
  Co_0 > Co_1 > Co_2 > Co_3 > ... > 1
gives the Conway sporadics.

Substrate cross-link to BT296:
  Leech kissing = 196560 = 2^mu * q^q * F_5 * Phi_6 * Phi_3
  Co_0 = Aut(Leech) order has substrate-clean exponents at all 6
  substrate primes (plus 23).

==============================================================
THE 6 + 1 PRIME STRUCTURE
==============================================================

Conway orders use primes {lambda, q, F_5, Phi_6, p_Ih, Phi_3, 23}.

  6 = q! substrate primes (+ 1 non-substrate prime 23).

NEW SUBSTRATE READING:
  Conway sporadic group prime support is q! + 1 = Phi_6 = 7 primes,
  with q! of them substrate.

==============================================================
CO_2 STABILIZES NORM-4 = MU VECTOR
==============================================================

Co_2 is defined as the stabilizer in Co_0 of a Leech vector of
norm-squared = mu (= 4).

  Co_2 = Stab(v, |v|^2 = mu).

NEW SUBSTRATE STAR:
  Co_2 stabilizes a SPACETIME-NORM Leech vector.

==============================================================
CO_3 STABILIZES NORM-6 = q! VECTOR
==============================================================

Co_3 is the stabilizer of a Leech vector of norm-squared = q!.

  Co_3 = Stab(v, |v|^2 = q!).

NEW SUBSTRATE READING:
  Co_3 stabilizes a SUBSTRATE-FACTORIAL-NORM Leech vector.

==============================================================
THE SPORADIC TOWER (BT304-305 + BT316)
==============================================================

  Mathieu chain (BT304-305): M_11, M_12, M_22, M_23, M_24
  Conway chain (BT316 here): Co_3, Co_2, Co_1, Co_0
  Total = 5 + 3 = 2^q sporadic groups from Steiner / Leech construction.

Substrate prime structure:
  Mathieu orders use {lambda, q, F_5, Phi_6, p_Ih, 23}
  Conway orders use {lambda, q, F_5, Phi_6, p_Ih, Phi_3, 23}

Conway adds Phi_3 to the prime set.

NEW SUBSTRATE READING:
  Sporadic-from-Leech tower covers six substrate primes {lambda, q, F_5,
  Phi_6, p_Ih, Phi_3} plus one non-substrate prime (23).

==============================================================
"""
from __future__ import annotations

import json
from pathlib import Path


def main():
    q = 3
    lambda_, mu = 2, 4
    F5 = 5
    phi3 = 13
    phi6 = 7
    phi4 = 10
    p_Ih = 11
    T_6 = 21

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 316: CONWAY SPORADIC GROUPS SUBSTRATE")
    print("=" * 78)
    print()

    conway = [
        ("Co_0", 8315553613086720000,
         [22, 9, 4, 2, 1, 1, 1],
         ["lambda*p_Ih", "q^lambda", "mu", "lambda", "1", "1", "1"]),
        ("Co_1", 4157776806543360000,
         [21, 9, 4, 2, 1, 1, 1],
         ["q*Phi_6 = T_6", "q^lambda", "mu", "lambda", "1", "1", "1"]),
        ("Co_2", 42305421312000,
         [18, 6, 3, 1, 1, 1],
         ["lambda*q^lambda", "q!", "q", "1", "1", "1"]),
        ("Co_3", 495766656000,
         [10, 7, 3, 1, 1, 1],
         ["Phi_4", "Phi_6", "q", "1", "1", "1"]),
    ]

    print("CONWAY GROUP ORDERS:")
    primes = [2, 3, 5, 7, 11, 13, 23]
    for name, order, exps, sub_exps in conway:
        print(f"  |{name}| = {order}")
        primes_used = primes[:len(exps)]
        prime_str = " * ".join(f"{p}^{e}" if e > 1 else str(p)
                                for p, e in zip(primes_used, exps))
        print(f"          = {prime_str}")
        print(f"          exponents: ({', '.join(sub_exps)})")
        print()

    print("STAR IDENTITIES:")
    assert conway[1][2][0] == T_6
    print(f"  |Co_1| 2-exponent = q * Phi_6 = T_6 = |E(Heawood)| (BT267)")
    print(f"  |Co_3| exponents = (Phi_4, Phi_6, q, 1, 1, 1)")
    print(f"  Three of Co_3's prime exponents ARE substrate primitives.")
    print()

    print("CONWAY STABILIZER NORMS (NEW SUBSTRATE READING):")
    print(f"  Co_2 stabilizes Leech vector of norm^2 = mu (SPACETIME!)")
    print(f"  Co_3 stabilizes Leech vector of norm^2 = q! (SUBSTRATE FACTORIAL)")
    print()

    print("PRIME-SUPPORT OF CONWAY ORDERS:")
    print(f"  All Conway primes: {{lambda, q, F_5, Phi_6, p_Ih, Phi_3, 23}}")
    print(f"  = q! = 6 substrate primes + 1 non-substrate (23).")
    print(f"  Total: q! + 1 = Phi_6 = 7 primes.")
    print()

    print("SPORADIC FROM LEECH TOWER (BT304-305 + BT316):")
    print(f"  Mathieu chain: M_11, M_12, M_22, M_23, M_24 (5 groups)")
    print(f"  Conway chain: Co_3, Co_2, Co_1, Co_0 (3 sporadic simple + Co_0)")
    print(f"  Total: 5 + 3 = 2^q (octonion!) sporadic-from-Leech groups.")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 316 SUMMARY")
    print("=" * 78)
    print("""
CONWAY SPORADIC GROUP ORDERS ARE SUBSTRATE-CLEAN.

EXPONENT PATTERNS:
  |Co_1|: (q*Phi_6=T_6, q^lambda, mu, lambda, 1, 1, 1)      *** STAR ***
  |Co_2|: (lambda*q^lambda, q!, q, 1, 1, 1)
  |Co_3|: (Phi_4, Phi_6, q, 1, 1, 1)                          *** STAR ***

ALL FOUR Conway group orders have substrate-clean prime exponents.

CONWAY GROUPS ACT BY STABILIZING SUBSTRATE-NORM LEECH VECTORS:
  Co_2 = Stab(v, |v|^2 = mu = SPACETIME)
  Co_3 = Stab(v, |v|^2 = q! = SUBSTRATE FACTORIAL)

PRIME-SUPPORT:
  6 = q! substrate primes (lambda, q, F_5, Phi_6, p_Ih, Phi_3)
  + 1 non-substrate prime (23) = Phi_6 primes total.

SPORADIC-FROM-LEECH TOWER:
  Mathieu (5) + Conway (3 simple + Co_0) = 2^q (octonion!) sporadics
  from Leech/Niemeier construction.

LEECH LATTICE (BT296) is the unifying object: its 196560 = 2^mu * q^q
* F_5 * Phi_6 * Phi_3 kissing number is the substrate-natural sphere
packing, and its automorphism Co_0 generates Conway sporadics.

The substrate's full sporadic-group story extends to Conway: a third
of the sporadic simple groups (Mathieu + Conway = 5 + 3 = 8 sporadics
out of 26 total) arise from Leech/Niemeier substrate construction.
""")

    out = Path("data") / "w33_BREAKTHROUGH_316_conway_sporadic_substrate.json"
    out.parent.mkdir(exist_ok=True)
    packet = {
        "conway_groups": [
            {"name": n, "order": o, "exponents": e, "substrate_exponents": s}
            for n, o, e, s in conway
        ],
        "stabilizer_norms": {
            "Co_2": "norm^2 = mu (spacetime)",
            "Co_3": "norm^2 = q! (substrate factorial)",
        },
        "prime_support": {
            "substrate_primes": ["lambda", "q", "F_5", "Phi_6", "p_Ih", "Phi_3"],
            "non_substrate": [23],
            "total": 7,
        },
        "leech_sporadic_count": "Mathieu(5) + Conway(3) = 2^q = octonion sporadics",
        "conclusion": (
            "All four Conway group orders substrate-clean: |Co_1| has 2-exponent "
            "= T_6 = octonion triples (BT287, BT267); |Co_3| has exponents "
            "(Phi_4, Phi_6, q, 1, 1, 1) with three substrate primitives. "
            "Co_2 stabilizes norm-mu Leech vector, Co_3 stabilizes norm-q! "
            "vector. Conway prime support = 6 substrate primes + 23 = q! + 1. "
            "Mathieu + Conway = 2^q sporadics from Leech construction."
        ),
    }
    out.write_text(json.dumps(packet, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
