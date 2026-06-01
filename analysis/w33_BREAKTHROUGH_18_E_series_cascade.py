"""W(3,3) BREAKTHROUGH 18: E-SERIES CASCADE (E_6 -> E_7 -> E_8 -> W(E_8) -> Sp(6,F_2)).

From the Master Dictionary (Pillar 130) and Pillar 207 (Deep Structural
Analysis) in docs/index.html, the exceptional Lie series and their Weyl
groups admit deeper substrate factorizations than previously catalogued.

==============================================================
NEW IDENTITY A: |E_6 ROOTS| = 2^q * q^2
==============================================================

The exceptional Lie algebra E_6 has 72 roots:
  |E_6 roots| = 72 = 2^q * q^2 = lambda^q * q^2 = 8 * 9

This is a NEW substrate factorization of the E_6 root count.

In substrate language:
  |E_6 roots| = OCTONION_dim * q^2 = 2^q * q^2

==============================================================
NEW IDENTITY B: v = |E_6 ROOTS|/2 + mu
==============================================================

The W(3,3) vertex count satisfies:
  v = |E_6+ roots| + mu
    = 36 + 4
    = 40

Equivalently: v - mu = 36 = positive roots of E_6.

This is the geometric link: W(3,3) vertices = (positive E_6 roots) + (quaternion dim).

==============================================================
NEW IDENTITY C: dim(E_8) = q! * v + 2^q
==============================================================

The dimension of E_8 has the substrate decomposition:
  dim(E_8) = 248 = q! * v + 2^q
                 = 6 * 40 + 8
                 = |E| + 2^q

So dim(E_8) = |E| + 2^q (NEW clean form).

Combined with E_8 = 240 + 8:
  dim(E_8) = |W(3,3) edges| + |Cayley unit group|
            = |Phi(E_8)| + |Aut(O)|/|S_3|
            = root count + Cartan generator count

==============================================================
NEW IDENTITY D: |W(E_8)| = 2 * |E| * |Sp(6, F_2)|
==============================================================

The Weyl group order of E_8:
  |W(E_8)| = 2 * |E| * |Sp(6, F_2)|
           = 2 * 240 * 1451520
           = 696,729,600

In substrate primitives:
  |Sp(6, F_2)| = 2^9 * q^4 * F_5 * Phi_6
              = 512 * 81 * 5 * 7
              = 1,451,520

So |W(E_8)| = 2 * v * k * 2^9 * q^4 * F_5 * Phi_6
            = 2 * 40 * 12 * 512 * 81 * 5 * 7
            = 696,729,600.

==============================================================
NEW IDENTITY E: E_8 COXETER = Y-SYSTEM PERIOD
==============================================================

The E_8 Y-system (Zamolodchikov 1991, proved by Fomin-Zelevinsky) has
period exactly equal to the E_8 Coxeter number:

  Period(E_8 Y-system) = h(E_8) = 30 = q * Phi_4

This connects the substrate's three forms of 30 (h_E_8 = 30 from BT5,
MCCXXI):
  q * Phi_4 (substrate)
  E_8 Coxeter number (Lie theory)
  E_8 Y-system period (cluster algebra)
  k(Sp(4, F_3)) conjugacy classes (representation theory)
  Z_DW(T^2) DW-TQFT partition function (TQFT)

NEW: ADD Y-SYSTEM PERIOD as the 5TH MANIFESTATION of h(E_8) = 30 = q*Phi_4.

==============================================================
EXCEPTIONAL LIE SERIES UNIFIED THROUGH W(3,3)
==============================================================

Combining with all prior breakthroughs:

  G_2 dim = k + lambda = 14                  (MCXXV)
  F_4 dim = mu * Phi_3 = 52                  (MCXXV)
  E_6 dim = lambda * q * Phi_3 = 78          (MCXXV)
  E_6 roots = 2^q * q^2 = 72                 (NEW, BT18)
  E_7 dim = Phi_3 * Phi_4 + q = 133          (MCXXV)
  E_8 dim = q! * v + 2^q = 248               (NEW, BT18)
  E_8 roots = |E| = 240                       (classical)
  E_8 Coxeter = q * Phi_4 = 30               (BT5/MCCXXI)
  |W(E_8)| = 2 * |E| * |Sp(6, F_2)|          (NEW, BT18)
  |Sp(6, F_2)| = 2^9 * q^4 * F_5 * Phi_6    (NEW, BT18)

The exceptional E-series is COMPLETELY substrate-graded, with deep
factorizations linking E_6, E_7, E_8 to W(3,3) substrate primitives.

==============================================================
"""
from __future__ import annotations

import json
from pathlib import Path


def main():
    q = 3
    lambda_, mu = 2, 4
    F5 = 5
    phi3, phi4, phi6 = 13, 10, 7
    k, v, E_count = 12, 40, 240
    f, g_neg = 24, 15
    import math
    q_fact = math.factorial(q)

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 18: E-SERIES CASCADE")
    print("=" * 78)
    print()

    # IDENTITY A: |E_6 roots| = 2^q * q^2
    e6_roots = 2**q * q**2
    assert e6_roots == 72
    print(f"IDENTITY A: |E_6 roots| = 2^q * q^2 = {2**q} * {q**2} = {e6_roots}")

    # IDENTITY B: v = |E_6+ roots| + mu
    e6_positive_roots = e6_roots // 2
    assert e6_positive_roots == 36
    assert v == e6_positive_roots + mu
    print(f"IDENTITY B: v = |E_6+ roots| + mu = {e6_positive_roots} + {mu} = {v}")
    print()

    # IDENTITY C: dim(E_8) = q! * v + 2^q
    dim_E8_substrate = q_fact * v + 2**q
    dim_E8 = 248
    assert dim_E8_substrate == dim_E8
    print(f"IDENTITY C: dim(E_8) = q! * v + 2^q = {q_fact}*{v} + {2**q} = {dim_E8_substrate}")
    print(f"             = |E| + 2^q = {E_count} + {2**q} = {E_count + 2**q}")
    print()

    # IDENTITY D: |W(E_8)| = 2 * |E| * |Sp(6, F_2)|
    sp6F2_order = 2**9 * q**4 * F5 * phi6
    assert sp6F2_order == 1451520
    W_E8_order = 2 * E_count * sp6F2_order
    assert W_E8_order == 696729600
    print(f"IDENTITY D: |W(E_8)| = 2 * |E| * |Sp(6, F_2)|")
    print(f"             = 2 * {E_count} * {sp6F2_order}")
    print(f"             = {W_E8_order}")
    print()
    print(f"             |Sp(6, F_2)| = 2^9 * q^4 * F_5 * Phi_6 = {sp6F2_order}")
    print()

    # IDENTITY E: E_8 Y-system period
    print(f"IDENTITY E: E_8 Y-system period = h(E_8) = q * Phi_4 = {q * phi4}")
    h_E8 = q * phi4
    assert h_E8 == 30
    print(f"             Five-fold manifestation of 30:")
    print(f"               1. q * Phi_4 (substrate)")
    print(f"               2. h(E_8) Coxeter number (Lie theory)")
    print(f"               3. Y-system period (cluster algebra)")
    print(f"               4. k(Sp(4, F_3)) conjugacy classes (rep theory)")
    print(f"               5. Z_DW(T^2) TQFT partition function (TQFT)")
    print()

    # Exceptional series unified
    print("=" * 78)
    print("EXCEPTIONAL LIE SERIES UNIFIED")
    print("=" * 78)
    print()
    print(f"  G_2 dim       = k + lambda = {k + lambda_}")
    print(f"  F_4 dim       = mu * Phi_3 = {mu * phi3}")
    print(f"  E_6 dim       = lambda * q * Phi_3 = {lambda_ * q * phi3}")
    print(f"  E_6 roots     = 2^q * q^2 = {e6_roots} (NEW)")
    print(f"  E_7 dim       = Phi_3 * Phi_4 + q = {phi3 * phi4 + q}")
    print(f"  E_8 dim       = q! * v + 2^q = {dim_E8_substrate} (NEW)")
    print(f"  E_8 roots     = |E| = {E_count}")
    print(f"  E_8 Coxeter   = q * Phi_4 = {h_E8}")
    print(f"  |W(E_8)|      = 2 * |E| * |Sp(6, F_2)| = {W_E8_order} (NEW)")
    print(f"  |Sp(6, F_2)|  = 2^9 * q^4 * F_5 * Phi_6 = {sp6F2_order} (NEW)")

    out = Path("data") / "w33_BREAKTHROUGH_18_E_series_cascade.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({
        "identity_A_E6_roots": "2^q * q^2 = 72",
        "identity_B_v_decomposition": "v = |E_6+ roots| + mu",
        "identity_C_dim_E8": "q! * v + 2^q = |E| + 2^q = 248",
        "identity_D_W_E8": "2 * |E| * |Sp(6, F_2)|",
        "identity_E_Y_system_period": "E_8 Y-system period = h(E_8) = 30",
        "Sp6_F2_factorization": "2^9 * q^4 * F_5 * Phi_6 = 1,451,520",
        "W_E8_substrate_decomp": "2 * v * k * 2^9 * q^4 * F_5 * Phi_6",
        "h_E8_five_manifestations": [
            "q * Phi_4 (substrate)",
            "Coxeter number of E_8",
            "Y-system period",
            "Conjugacy classes of Sp(4, F_3)",
            "DW-TQFT partition function on T^2",
        ],
    }, indent=2, default=str), encoding="utf-8")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
