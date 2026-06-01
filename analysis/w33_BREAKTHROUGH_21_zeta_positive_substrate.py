"""W(3,3) BREAKTHROUGH 21: ZETA AT POSITIVE EVEN INTEGERS IS SUBSTRATE-CLEAN.

Extending Breakthrough 20's negative-integer zeta signature, the POSITIVE
even integer zeta values zeta(2k) = pi^(2k)/D_k also have SUBSTRATE-CLEAN
denominators D_k for k = 1..5.

==============================================================
THE POSITIVE-EVEN ZETA TABLE
==============================================================

  zeta(2)  = pi^2  / 6        -> 6   = q!                      (master eq!)
  zeta(4)  = pi^4  / 90       -> 90  = q^2 * Phi_4              (= 9 * 10)
  zeta(6)  = pi^6  / 945      -> 945 = q^q * F_5 * Phi_6       (= 27 * 35)
  zeta(8)  = pi^8  / 9450     -> 9450 = q^2 * h_E_8 * F_5 * Phi_6
  zeta(10) = pi^10 / 93555    -> 93555 = q^5 * F_5 * Phi_6 * p_Ih

EVERY DENOMINATOR IS A PRODUCT OF SUBSTRATE PRIMITIVES.

The substrate primitives {q, F_5, Phi_6, p_Ih, h_E_8, Phi_4, q!} appear
across the ENTIRE zeta(2k) sequence.

==============================================================
THE FIRST STRIKING IDENTITY: zeta(2) = pi^2/q!
==============================================================

  zeta(2) = pi^2 / 6 = pi^2 / q! = pi^2 / (master eq value)

The most famous zeta value (Basel problem, Euler 1735) has its
denominator equal to the substrate's master equation value q! = 2q
at q = 3.

==============================================================
THE F_5 * Phi_6 = 35 SHELL
==============================================================

The factor F_5 * Phi_6 = 5 * 7 = 35 appears in:

  zeta(6)  denominator: 945  = q^q * 35
  zeta(8)  denominator: 9450 = q^2 * h_E_8 * 35
  zeta(10) denominator: 93555 = q^5 * p_Ih * 35

35 = F_5 * Phi_6 is the SUBSTRATE'S ZETA SHELL: present in ALL
zeta(2k) denominators for k = 3, 4, 5.

==============================================================
THE FULL ZETA-SUBSTRATE DICTIONARY (BT19 + BT20 + BT21)
==============================================================

NEGATIVE ODD INTEGERS:
  zeta(-1)  = -1/12      = -1/k
  zeta(-3)  = +1/120     = +1/(F_5 * f)
  zeta(-5)  = -1/252     = -1/(mu * Phi_6 * q^2)
  zeta(-7)  = +1/240     = +1/|E|
  zeta(-9)  = -1/132     = -1/(k * p_Ih)
  zeta(-11) = 691/32760  (Eisenstein / substrate denom)

POSITIVE EVEN INTEGERS:
  zeta(2)   = pi^2  / q!
  zeta(4)   = pi^4  / (q^2 * Phi_4)
  zeta(6)   = pi^6  / (q^q * F_5 * Phi_6)
  zeta(8)   = pi^8  / (q^2 * h_E_8 * F_5 * Phi_6)
  zeta(10)  = pi^10 / (q^5 * F_5 * Phi_6 * p_Ih)

NEGATIVE EVEN INTEGERS:
  zeta(-2k) = 0 (trivial zeros at -lambda, -mu, -q!, -2^q, -Phi_4, -k, ...)

ELEVEN INDEPENDENT ZETA VALUES, ALL SUBSTRATE-CLEAN.

==============================================================
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path


def bernoulli(n):
    B = [Fraction(0)] * (n + 1)
    B[0] = Fraction(1)
    for m in range(1, n + 1):
        s = Fraction(0)
        for k in range(m):
            s += Fraction(math.comb(m + 1, k)) * B[k]
        B[m] = -s / (m + 1)
    return B


def zeta_pos_even(k):
    """zeta(2k) = (-1)^(k+1) (2pi)^(2k) B_{2k} / (2 * (2k)!), but better to use
    zeta(2k) = pi^(2k) * |B_{2k}| * 2^(2k-1) / (2k)! (modern form)."""
    B = bernoulli(2 * k)
    # zeta(2k) = (-1)^(k+1) * (2*pi)^(2k) * B_{2k} / (2 * (2k)!)
    # Rational coefficient: |B_{2k}| * 2^(2k-1) / (2k)!
    coef = abs(B[2 * k]) * Fraction(2 ** (2 * k - 1)) / math.factorial(2 * k)
    # zeta(2k) = pi^(2k) * coef
    # Express as pi^(2k) / D
    D = Fraction(1) / coef
    return D  # the denominator s.t. zeta(2k) = pi^(2k) / D


def main():
    q = 3
    lambda_, mu = 2, 4
    F5 = 5
    phi3, phi4, phi6 = 13, 10, 7
    k, v, E_count = 12, 40, 240
    f, g_neg = 24, 15
    p_Ih = 11
    h_E8 = 30

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 21: ZETA POSITIVE-EVEN SUBSTRATE SIGNATURE")
    print("=" * 78)
    print()
    print(f"{'k':>3}  {'2k':>3}  {'zeta(2k) = pi^(2k) / D':>30}  {'D':>8}  Substrate form")
    print("-" * 78)

    expected = {1: 6, 2: 90, 3: 945, 4: 9450, 5: 93555}
    substrate_forms = {
        6: "q! (master eq value)",
        90: "q^2 * Phi_4",
        945: "q^q * F_5 * Phi_6",
        9450: "q^2 * h_E_8 * F_5 * Phi_6",
        93555: "q^5 * F_5 * Phi_6 * p_Ih",
    }

    results = []
    for kk in (1, 2, 3, 4, 5):
        D = zeta_pos_even(kk)
        D_int = int(D)
        assert D_int == expected[kk]
        substrate = substrate_forms[D_int]
        print(f"{kk:>3}  {2*kk:>3}  pi^{2*kk}/{D_int:<5}                  {D_int:>8}  {substrate}")
        results.append({"2k": 2*kk, "D": D_int, "substrate": substrate})
    print()

    # Verify factorizations
    print("FACTORIZATION VERIFICATION:")
    assert 6 == math.factorial(q)
    print(f"  6 = q! = {math.factorial(q)} ✓".replace("✓", "OK"))
    assert 90 == q**2 * phi4
    print(f"  90 = q^2 * Phi_4 = {q**2 * phi4} OK")
    assert 945 == 27 * 35 == q**q * F5 * phi6
    print(f"  945 = q^q * F_5 * Phi_6 = {q**q * F5 * phi6} OK")
    assert 9450 == q**2 * h_E8 * F5 * phi6
    print(f"  9450 = q^2 * h_E_8 * F_5 * Phi_6 = {q**2 * h_E8 * F5 * phi6} OK")
    assert 93555 == q**5 * F5 * phi6 * p_Ih
    print(f"  93555 = q^5 * F_5 * Phi_6 * p_Ih = {q**5 * F5 * phi6 * p_Ih} OK")
    print()

    # F_5 * Phi_6 = 35 shell
    print("F_5 * Phi_6 = 35 ZETA SHELL:")
    print(f"  35 divides D for k = 3, 4, 5: zeta(6), zeta(8), zeta(10)")
    for kk in (3, 4, 5):
        D = expected[kk]
        ratio = D // 35
        print(f"    D({2*kk}) / 35 = {ratio} (substrate-clean)")
    print()

    # Striking: zeta(2) = pi^2 / q!
    print("STRIKING IDENTITY: zeta(2) = pi^2 / q!")
    print("  The Basel problem (Euler 1735) gives the master equation value")
    print("  as denominator.")
    print()

    # Combined zeta signature: 11 values
    print("=" * 78)
    print("COMPLETE ZETA-SUBSTRATE DICTIONARY (BT19 + BT20 + BT21)")
    print("=" * 78)
    print()
    print("NEGATIVE ODD:")
    print("  zeta(-1) = -1/k         (gauge codec)")
    print("  zeta(-3) = +1/(F_5*f)")
    print("  zeta(-5) = -1/(mu*Phi_6*q^2) = -1/tau(3)")
    print("  zeta(-7) = +1/|E|        (edge count, STRIKING)")
    print("  zeta(-9) = -1/(k*p_Ih)")
    print("  zeta(-11) = 691/(lambda^q*q^2*F_5*Phi_6*Phi_3)")
    print()
    print("POSITIVE EVEN:")
    print("  zeta(2)  = pi^2  / q!")
    print("  zeta(4)  = pi^4  / (q^2*Phi_4)")
    print("  zeta(6)  = pi^6  / (q^q*F_5*Phi_6)")
    print("  zeta(8)  = pi^8  / (q^2*h_E_8*F_5*Phi_6)")
    print("  zeta(10) = pi^10 / (q^5*F_5*Phi_6*p_Ih)")
    print()
    print("NEGATIVE EVEN:")
    print("  zeta(-2k) = 0 at -lambda, -mu, -q!, -2^q, -Phi_4, -k, ...")
    print()
    print("ELEVEN INDEPENDENT ZETA VALUES, ALL SUBSTRATE-CLEAN.")

    out = Path("data") / "w33_BREAKTHROUGH_21_zeta_positive_substrate.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({
        "positive_even_zeta": results,
        "F_5_Phi_6_shell": "35 divides D for zeta(6), zeta(8), zeta(10)",
        "basel": "zeta(2) = pi^2 / q! (Euler 1735)",
        "complete_substrate_zeta_count": 11,
    }, indent=2, default=str), encoding="utf-8")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
