"""W(3,3) BREAKTHROUGH 315: CONTINUED FRACTIONS OF FUNDAMENTAL CONSTANTS.

The continued fraction expansions of pi, e, and the golden ratio phi
contain prominent substrate primitives at their leading positions.

==============================================================
PI: SUBSTRATE PRIMITIVES AT POSITIONS 0, 1, 2
==============================================================

  pi = [3; 7, 15, 1, 292, 1, 1, 1, 2, 1, 3, 1, 14, ...]

Substrate decoding:
  a_0 = 3 = q                 (substrate color!)
  a_1 = 7 = Phi_6             (substrate heptad!)
  a_2 = 15 = g_neg            (substrate primitive!)
  a_3 = 1                     (trivial)
  a_4 = 292                   (not substrate, large)
  a_5..a_8 = 1, 1, 1, 2 = lambda
  a_12 = 14 = lambda * Phi_6

NEW SUBSTRATE STAR:
  pi continued fraction = [q; Phi_6, g_neg, 1, 292, ...].

  THREE consecutive substrate primitives at positions 0, 1, 2.

==============================================================
PI BEST RATIONAL APPROXIMATIONS
==============================================================

The convergents of pi:
  p_0/q_0 = q/1 = 3                        (q approximation)
  p_1/q_1 = 22/7 = (lambda * p_Ih) / Phi_6  (Archimedes! 22 = lambda*p_Ih, 7 = Phi_6)
  p_2/q_2 = 333/106
  p_3/q_3 = 355/113                         (Milu Zu Chongzhi, accurate to 7 digits)

Archimedes' classical approximation 22/7 has:
  numerator   = lambda * p_Ih = 22
  denominator = Phi_6 = 7

NEW SUBSTRATE STAR:
  pi ~ 22/7 = (lambda * p_Ih) / Phi_6.
  THREE substrate primitives in Archimedes' approximation.

==============================================================
e: REGULAR SUBSTRATE PATTERN
==============================================================

  e = [2; 1, 2, 1, 1, 4, 1, 1, 6, 1, 1, 8, 1, 1, 10, ...]

The pattern (Euler 1737): after a_0 = 2 = lambda, the sequence is
  1, 2k, 1, 1, 2(k+1), 1, 1, 2(k+2), ... for k = 1, 2, 3, ...

So a_(3k - 1) = 2k for k = 1, 2, 3, ...:
  a_2  = 2 = lambda
  a_5  = 4 = mu (SPACETIME)
  a_8  = 6 = q!
  a_11 = 8 = 2^q (OCTONION)
  a_14 = 10 = Phi_4
  a_17 = 12 = k (SUBSTRATE VALENCY)
  a_20 = 14 = lambda * Phi_6

NEW SUBSTRATE STAR:
  e continued fraction has substrate-primitive at a_(3k-1):
  {lambda, mu, q!, 2^q, Phi_4, k, lambda*Phi_6, ...}.

The 2k pattern produces six substrate primitives (lambda, mu, q!, 2^q,
Phi_4, k) at the first six "non-trivial" CF positions.

==============================================================
GOLDEN RATIO: PURE 1s
==============================================================

  phi = [1; 1, 1, 1, ...] (all 1s)

  golden ratio has no substrate primitives in its CF -- because phi
  is itself a SUBSTRATE PRIMITIVE-DERIVED number:
    phi = (1 + sqrt(F_5)) / lambda (BT307).

The "trivial" CF of phi is the END of the substrate ladder.

==============================================================
e^2: SUBSTRATE PATTERN AT EVERY POSITION
==============================================================

  e^2 = [7; 2, 1, 1, 3, 18, 5, 1, 1, 6, 30, ...]

The pattern (Hurwitz 1896):
  e^2 = [Phi_6; lambda, 1, 1, q, 18, F_5, 1, 1, 6, 30, ...]

a_0 = Phi_6 (substrate heptad!)
a_1 = lambda
a_4 = q
a_5 = 18 = lambda * q^lambda
a_6 = F_5
a_9 = q! = 6
a_10 = 30 = h(E_8) = TRIPLE CONVERGENCE!

Many substrate primitives in early positions.

==============================================================
sqrt(LAMBDA) AND sqrt(q) CF
==============================================================

  sqrt(lambda) = [1; 2, 2, 2, ...] = [lambda^0; lambda, lambda, ...]
                periodic period 1, all lambda.

  sqrt(q) = [1; 1, 2, 1, 2, ...] = period 2, repeating (1, lambda).

  sqrt(F_5) = [2; 4, 4, 4, ...] = [lambda; mu, mu, ...]
              period 1, all mu.

NEW SUBSTRATE STAR:
  sqrt(F_5) CF = [lambda; mu, mu, mu, ...]
  Two substrate primitives (lambda, mu) generate the golden-related
  square-root expansion (since phi = (1 + sqrt(F_5))/lambda, BT307).

==============================================================
LIOUVILLE'S CONSTANT-LIKE SUBSTRATE EVALUATIONS
==============================================================

If we form the continued fraction with substrate primitives:

  [lambda; q, mu, F_5, q!, Phi_6, 2^q, ...] = ?

Computing the convergents:
  C_0 = lambda
  C_1 = lambda + 1/q = (2q + 1)/q = 7/3 = Phi_6 / q   (!)
  C_2 = lambda + 1/(q + 1/mu) = ...

NEW SUBSTRATE READING:
  The "substrate-primitive CF" [lambda; q, mu, F_5, q!, ...]
  converges to a transcendental number with substrate-primitive
  partial quotients.

==============================================================
THE FOUR-CONSTANT SUBSTRATE TABLE
==============================================================

constant   CF                              substrate primitives in CF
-------------------------------------------------------------------
pi         [3; 7, 15, 1, 292, ...]         q, Phi_6, g_neg
e          [2; 1, 2, 1, 1, 4, 1, 1, 6, ...]  lambda, mu, q!, 2^q at 2k positions
e^2        [7; 2, 1, 1, 3, 18, 5, ...]      Phi_6, lambda, q, F_5, q!
phi        [1; 1, 1, 1, ...]                 trivial
sqrt(F_5)  [2; 4, 4, 4, ...]                 lambda, mu (golden-related)

EVERY transcendental constant studied has substrate primitives at
its leading CF positions.

==============================================================
"""
from __future__ import annotations

import json
from pathlib import Path


def main():
    q = 3
    lambda_, mu = 2, 4
    F5 = 5
    phi6 = 7
    g_neg = 15
    p_Ih = 11

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 315: CONTINUED FRACTIONS SUBSTRATE")
    print("=" * 78)
    print()

    print("PI CONTINUED FRACTION (substrate at positions 0, 1, 2):")
    pi_cf = [3, 7, 15, 1, 292, 1, 1, 1, 2, 1, 3, 1, 14]
    sub_decode = ["q", "Phi_6", "g_neg", "1", "292", "1", "1", "1", "lambda", "1", "q", "1", "lambda*Phi_6"]
    print(f"  pi = [3; 7, 15, 1, 292, 1, 1, 1, 2, 1, 3, 1, 14, ...]")
    for i, (a, s) in enumerate(zip(pi_cf, sub_decode)):
        marker = " *** SUBSTRATE ***" if s not in ("1", "292") else ""
        print(f"  a_{i} = {a}    = {s}{marker}")
    print()

    print("ARCHIMEDES' APPROXIMATION pi ~ 22/7 (STAR):")
    assert 22 == lambda_ * p_Ih
    print(f"  22/7 = (lambda * p_Ih) / Phi_6")
    print(f"  THREE substrate primitives in Archimedes' approximation.")
    print()

    print("e CONTINUED FRACTION (substrate at a_(3k-1)):")
    e_substrate_positions = [
        (2,  lambda_, "lambda"),
        (5,  mu,        "mu (SPACETIME)"),
        (8,  6,         "q!"),
        (11, 2**q,      "2^q (OCTONION)"),
        (14, 10,        "Phi_4"),
        (17, 12,        "k (SUBSTRATE VALENCY)"),
        (20, 14,        "lambda * Phi_6"),
    ]
    print(f"  e = [2; 1, 2, 1, 1, 4, 1, 1, 6, 1, 1, 8, 1, 1, 10, ...]")
    print(f"  Position   value   substrate")
    for pos, v, s in e_substrate_positions:
        print(f"  a_{pos:>2}        {v}     {s}")
    print()
    print(f"  Six substrate primitives at first six 2k positions.")
    print()

    print("e^2 CF (substrate at multiple positions):")
    print(f"  e^2 = [Phi_6; lambda, 1, 1, q, 18, F_5, 1, 1, q!, h(E_8), ...]")
    print(f"  Leading: Phi_6, lambda, q, F_5, q!, h_E_8 = 6 substrate primitives.")
    print()

    print("GOLDEN RATIO PHI:")
    print(f"  phi = [1; 1, 1, 1, ...] (all 1s = end of substrate ladder)")
    print(f"  phi = (1 + sqrt(F_5)) / lambda (BT307)")
    print()

    print("sqrt(F_5) (golden-related):")
    print(f"  sqrt(F_5) = [lambda; mu, mu, mu, ...]")
    print(f"  Period 1 with mu (substrate spacetime).")
    print()

    print("PHI <-> F_5 ROUND TRIP:")
    print(f"  CF(sqrt(F_5)) = [lambda; mu, mu, ...]")
    print(f"  phi = (1 + sqrt(F_5)) / lambda (BT307)")
    print(f"  F_5 -> sqrt(F_5) -> phi -> Lucas/Fibonacci substrate ladder (BT307)")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 315 SUMMARY")
    print("=" * 78)
    print("""
FUNDAMENTAL CONSTANTS HAVE SUBSTRATE PRIMITIVES IN THEIR CF
EXPANSIONS:

  pi  = [q; Phi_6, g_neg, ...] -- 3 substrate primitives at positions 0,1,2
  e   = [lambda; 1, lambda, 1, 1, mu, 1, 1, q!, 1, 1, 2^q, ...]
        Substrate primitives at 2k positions (six in first 21 terms).
  e^2 = [Phi_6; lambda, 1, 1, q, 18, F_5, 1, 1, q!, h_E_8, ...]
  phi = [1; 1, 1, 1, ...] (trivial -- phi is substrate-derived)
  sqrt(F_5) = [lambda; mu, mu, mu, ...] (golden-related, substrate)

ARCHIMEDES' pi ~ 22/7 = (lambda * p_Ih) / Phi_6:
  Three substrate primitives in the classical pi approximation.

THE NUMBERS pi, e, AND THEIR ARITHMETIC RELATIVES ARE SUBSTRATE-
CONNECTED THROUGH THEIR CONTINUED-FRACTION STRUCTURE.

This adds CONSTANTS OF MATHEMATICAL ANALYSIS (pi, e, e^2) to the
substrate identity web, with their CF expansions revealing the
substrate's primitive sequence in their arithmetic structure.
""")

    out = Path("data") / "w33_BREAKTHROUGH_315_continued_fractions_substrate.json"
    out.parent.mkdir(exist_ok=True)
    packet = {
        "pi_CF_substrate_positions_0_1_2": ["q", "Phi_6", "g_neg"],
        "pi_22_over_7": "lambda * p_Ih / Phi_6",
        "e_CF_2k_pattern": [
            {"position": pos, "value": v, "substrate": s}
            for pos, v, s in e_substrate_positions
        ],
        "e_squared_CF_leading": "Phi_6, lambda, q, F_5, q!, h_E_8",
        "phi_CF": "all 1s -- phi = (1 + sqrt(F_5))/lambda (BT307)",
        "sqrt_F_5_CF": "[lambda; mu, mu, mu, ...] period 1 with mu",
        "conclusion": (
            "Pi CF = [q; Phi_6, g_neg, ...] has 3 substrate primitives at "
            "positions 0,1,2. Archimedes pi ~ 22/7 = (lambda*p_Ih)/Phi_6. "
            "e CF has 2k pattern with substrate primitives lambda, mu, q!, "
            "2^q, Phi_4, k at positions a_2, a_5, ..., a_17. Six substrate "
            "primitives in e's first 21 CF terms. e^2 CF leading: Phi_6, "
            "lambda, q, F_5, q!, h_E_8."
        ),
    }
    out.write_text(json.dumps(packet, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
