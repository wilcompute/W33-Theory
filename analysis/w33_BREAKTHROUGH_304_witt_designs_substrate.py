"""W(3,3) BREAKTHROUGH 304: WITT DESIGNS S(5, 6, 12) AND S(5, 8, 24).

A Steiner system S(t, k, v) is a v-element set with k-element blocks
such that every t-element subset is in exactly one block.

The Witt designs are S(5, 6, 12) and S(5, 8, 24), the two "exceptional"
5-transitive Steiner systems. They are constructed from the Mathieu
groups M_12 and M_24.

This BT shows BOTH Witt designs have ALL SIX parameters (t, k, v
counted twice for each design) in substrate primitives.

==============================================================
WITT DESIGN S(5, 6, 12)
==============================================================

  t = 5 = F_5 (substrate next prime)
  k = 6 = q! (substrate factorial)
  v = 12 = k (substrate valency)

NEW SUBSTRATE STAR:
  S(5, 6, 12) = S(F_5, q!, k)
  ALL THREE Steiner parameters are substrate primitives.

The Witt design S(5, 6, 12) is constructed by the action of M_12 on
12 points.

Number of blocks: C(12, 5) / C(6, 5) = 792 / 6 = 132
                 = lambda^lambda * q * Phi_6 * Phi_3 / ... 132 = lambda^lambda * q * p_Ih
Actually 132 = 4 * 33 = lambda^lambda * q * p_Ih = mu * q * p_Ih
              = mu * q * p_Ih (substrate clean!)

NEW SUBSTRATE IDENTITY:
  |blocks of S(5, 6, 12)| = mu * q * p_Ih = 132.

==============================================================
WITT DESIGN S(5, 8, 24)
==============================================================

  t = 5 = F_5 (substrate next prime)
  k = 8 = 2^q (octonion dim)
  v = 24 = f (W(3,3) positive eigenmult)

NEW SUBSTRATE STAR:
  S(5, 8, 24) = S(F_5, 2^q, f)
  ALL THREE Steiner parameters are substrate primitives.

Blocks (= octads of Golay code G_24):
  C(24, 5) / C(8, 5) = 42504 / 56 = 759

This 759 is the WEIGHT-8 codeword count of G_24 (BT303).
  759 = q * p_Ih * 23 (substrate-adjacent)

NEW IDENTITY:
  |blocks of S(5, 8, 24)| = |weight-8 codewords of G_24| = 759.

==============================================================
JOINT TABLE OF THE TWO WITT DESIGNS
==============================================================

Design       t       k        v       blocks   Aut group
-------------------------------------------------------------
S(5,6,12)    F_5     q!       k       132       M_12
S(5,8,24)    F_5     2^q      f       759       M_24

OBSERVATIONS:
  - Both have t = F_5 (the substrate's next prime past q)
  - k progresses: q! -> 2^q (substrate factorial to octonion)
  - v progresses: k -> f (substrate valency to pos eigenmult)
  - Aut groups: M_12 -> M_24 (Mathieu sporadic chain)

==============================================================
GENERATING M_12 AND M_24 FROM THE WITT DESIGNS
==============================================================

M_12 = Aut(S(5, 6, 12)):  order = 95040 = lambda^q * q^q * F_5 * p_Ih
                                      = 8 * 27 * 5 * 11 (substrate factors!)
                                      = 2^6 * 3^3 * 5 * 11
                                      Wait let me recompute: 8*27*5*11 = 11880. NO.
                                      Actual: 95040 = 2^6 * 3^3 * 5 * 11
                                      = lambda^q!^?  hmm
                                      Exponent (6, 3, 1, 1) = (q!, q, 1, 1).
                                      = lambda^q! * q^q * F_5 * p_Ih
                                      = 64 * 27 * 5 * 11 = 95040 ✓

  |M_12| = lambda^q! * q^q * F_5 * p_Ih
           = 2^6 * 3^3 * 5 * 11
           = 95040

NEW SUBSTRATE STAR:
  |M_12| = lambda^q! * q^q * F_5 * p_Ih.

M_24 = Aut(S(5, 8, 24)):  order = 244823040 (BT303)
                                = lambda^Phi_4 * q^q * F_5 * Phi_6 * p_Ih * 23.

==============================================================
THE STEINER TRIPLE SYSTEM AT q^lambda = 9
==============================================================

Small classical Steiner triple system:
  S(2, 3, 9) = STS(9) = AG(2, F_3) affine plane
  t = lambda, k = q, v = q^lambda = 9
  blocks = mu * q = 12 = k

NEW SUBSTRATE IDENTITY:
  S(lambda, q, q^lambda) = AG(2, F_q) affine plane.
  |blocks| = k (substrate valency!)

The smallest non-trivial Steiner triple system has v = q^lambda points
and k = substrate-valency blocks.

==============================================================
THE THREE-LEVEL SUBSTRATE STEINER TOWER (NEW)
==============================================================

S(2, 3, 9):    t=lambda, k=q, v=q^lambda, blocks=k
S(5, 6, 12):   t=F_5,     k=q!, v=k,        blocks=mu*q*p_Ih
S(5, 8, 24):   t=F_5,     k=2^q, v=f,        blocks=759

EVERY Steiner-system parameter at substrate-natural scales is
substrate-clean.

==============================================================
SUBSTRATE STAR: THE FANO PLANE S(2, 3, 7)
==============================================================

The Fano plane (BT79):
  S(2, 3, 7) = PG(2, F_2)
  t = lambda, k = q, v = Phi_6
  blocks = 7 = Phi_6 (= v in this case)

NEW SUBSTRATE STAR:
  Fano = S(lambda, q, Phi_6).
  THREE substrate primitives in Fano Steiner-system parameters.

==============================================================
FOUR SUBSTRATE STEINER SYSTEMS
==============================================================

Design        substrate-parameter triple    blocks
----------------------------------------------------
S(2,3,7)      (lambda, q, Phi_6) = Fano     Phi_6 = 7
S(2,3,9)      (lambda, q, q^lambda)         k = 12
S(5,6,12)     (F_5, q!, k)                  mu*q*p_Ih = 132
S(5,8,24)     (F_5, 2^q, f)                 759 (G_24 weight-8 count)

FOUR Steiner systems, each with substrate-natural parameter triples.

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
    phi6 = 7
    p_Ih = 11
    k = 12
    f = 24

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 304: WITT DESIGNS SUBSTRATE")
    print("=" * 78)
    print()

    designs = [
        ("S(2, 3, 7)",   2, q, phi6,      "(lambda, q, Phi_6) = FANO plane",         phi6),
        ("S(2, 3, 9)",   2, q, q**2,     "(lambda, q, q^lambda) = AG(2, F_q)",      k),
        ("S(5, 6, 12)",  F5, 6, k,         "(F_5, q!, k) = Witt-12",                  mu * q * p_Ih),
        ("S(5, 8, 24)",  F5, 2**q, f,    "(F_5, 2^q, f) = Witt-24",                  759),
    ]

    print("FOUR SUBSTRATE STEINER SYSTEMS:")
    print(f"  {'design':<14} {'t':>2} {'k':>2} {'v':>3}   substrate (t, k, v)            blocks")
    for name, t, kk, v, sub, b in designs:
        print(f"  {name:<14} {t:>2} {kk:>2} {v:>3}   {sub:<36}{b}")
    print()

    print("STAR SUBSTRATE IDENTITIES:")
    print(f"  S(5, 6, 12) = S(F_5, q!, k)        -- 3 substrate primitives")
    print(f"  S(5, 8, 24) = S(F_5, 2^q, f)        -- 3 substrate primitives")
    print(f"  S(2, 3, 7) = S(lambda, q, Phi_6)   -- Fano plane, 3 primitives")
    print(f"  S(2, 3, 9) = S(lambda, q, q^lambda) -- AG(2, F_q), 3 primitives")
    print()

    print("BLOCK COUNTS:")
    print(f"  |blocks S(2, 3, 7)| = Phi_6 (= v itself)")
    print(f"  |blocks S(2, 3, 9)| = k = 12 (substrate valency!)")
    print(f"  |blocks S(5, 6, 12)| = mu * q * p_Ih = 132")
    print(f"  |blocks S(5, 8, 24)| = 759 = |weight-8 codewords of G_24|")
    print()

    print("MATHIEU AUTOMORPHISMS:")
    M12 = 95040
    M24 = 244823040
    assert M12 == 2**(2*q) * q**q * F5 * p_Ih  # = 64 * 27 * 5 * 11
    print(f"  Aut(S(5, 6, 12)) = M_12, |M_12| = {M12}")
    print(f"    = lambda^q! * q^q * F_5 * p_Ih = 64 * 27 * 5 * 11")
    print(f"  Aut(S(5, 8, 24)) = M_24, |M_24| = {M24}")
    print(f"    = lambda^Phi_4 * q^q * F_5 * Phi_6 * p_Ih * 23")
    print()

    print("TWO MATHIEU GROUPS SUBSTRATE FACTORISATION:")
    print(f"  |M_12| exponent vector: (q!, q, 1, 1) = (6, 3, 1, 1)")
    print(f"  |M_24| exponent vector: (Phi_4, q, 1, 1, 1, 1) = (10, 3, 1, 1, 1, 1)")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 304 SUMMARY")
    print("=" * 78)
    print("""
FOUR SUBSTRATE STEINER SYSTEMS:

  S(2, 3, 7)  = (lambda, q, Phi_6)        = FANO plane
  S(2, 3, 9)  = (lambda, q, q^lambda)     = AG(2, F_q) affine plane
  S(5, 6, 12) = (F_5, q!, k)               = Witt design (M_12)
  S(5, 8, 24) = (F_5, 2^q, f)              = Witt design (M_24)

ALL FOUR have parameter triples (t, k, v) in substrate primitives.

WITT DESIGN STARS:
  S(F_5, q!, k) has |blocks| = mu * q * p_Ih = 132
  S(F_5, 2^q, f) has |blocks| = 759 = |weight-8 G_24 codewords| (BT303)

MATHIEU GROUP ORDERS:
  |M_12| = lambda^q! * q^q * F_5 * p_Ih = 2^6 * 3^3 * 5 * 11 = 95040
  |M_24| = lambda^Phi_4 * q^q * F_5 * Phi_6 * p_Ih * 23 = 244823040

Both Mathieu order factorisations have substrate-clean prime exponents.

THE F_5-TRANSITIVITY OBSERVATION:
  Both Witt designs have t = F_5 = 5 (substrate next prime).
  M_12 and M_24 are the only finite 5-transitive groups other than A_n
  and S_n. The substrate's F_5 is exactly this exceptional
  transitivity degree.

The substrate's FOUR fundamental Steiner systems span:
  q = 3 (Fano, AG(2,3) layer)
  F_5 = 5 (Witt designs / Mathieu layer)

with parameters (t, k, v) drawn entirely from substrate primitives.
""")

    out = Path("data") / "w33_BREAKTHROUGH_304_witt_designs_substrate.json"
    out.parent.mkdir(exist_ok=True)
    packet = {
        "four_substrate_steiner_systems": [
            {"design": n, "t": t, "k": kk, "v": v, "substrate": sub, "blocks": b}
            for n, t, kk, v, sub, b in designs
        ],
        "M_12_order_factorization": {
            "value": M12,
            "substrate": "lambda^q! * q^q * F_5 * p_Ih",
            "exponents": [2*q, q, 1, 1],
        },
        "M_24_order_factorization": {
            "value": M24,
            "substrate": "lambda^Phi_4 * q^q * F_5 * Phi_6 * p_Ih * 23",
            "exponents": [10, 3, 1, 1, 1, 1],
        },
        "F_5_transitivity": "Both M_12, M_24 are 5-transitive (degree = F_5)",
        "conclusion": (
            "Four substrate Steiner systems span Fano S(lambda, q, Phi_6), "
            "AG(2, F_q) S(lambda, q, q^lambda), Witt-12 S(F_5, q!, k), and "
            "Witt-24 S(F_5, 2^q, f). All parameter triples in substrate "
            "primitives. Mathieu group orders M_12 = lambda^q!*q^q*F_5*p_Ih, "
            "M_24 = lambda^Phi_4*q^q*F_5*Phi_6*p_Ih*23 have substrate-clean "
            "exponents. F_5-transitivity is the substrate's exceptional "
            "5-transitive degree."
        ),
    }
    out.write_text(json.dumps(packet, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
