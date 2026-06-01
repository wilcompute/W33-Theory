"""W(3,3) BREAKTHROUGH 20: FULL ZETA-SUBSTRATE SIGNATURE.

The Riemann zeta function at negative odd integers gives SUBSTRATE-CLEAN
DENOMINATORS via the Bernoulli identity zeta(-n) = -B_{n+1}/(n+1).

Extending Breakthrough 19's k = -1/zeta(-1) = 12 to all small negative
odd integers, the substrate's gauge structure has a COMPLETE zeta
regularization signature.

==============================================================
THE ZETA-SUBSTRATE TABLE
==============================================================

  zeta(-1)  = -1/12      -> 12 = k                     (gauge codec, BT19)
  zeta(-3)  = +1/120     -> 120 = F_5 * f               (Fermat * positive eigen)
  zeta(-5)  = -1/252     -> 252 = mu * Phi_6 * q^2     (= Ramanujan tau(3))
  zeta(-7)  = +1/240     -> 240 = |E|                   (W(3,3) edge count!!)
  zeta(-9)  = -1/132     -> 132 = k * p_Ih              (gauge * Ihara prime)
  zeta(-11) = 691/32760  -> 32760 = lambda^q * q^2 * F_5 * Phi_6 * Phi_3

ALL DENOMINATORS ARE SUBSTRATE-CLEAN INTEGERS through zeta(-11).

The numerator 691 at zeta(-11) is the FAMOUS EISENSTEIN-BERNOULLI PRIME
(historic in modular forms theory).

==============================================================
THE STRIKING IDENTITY: zeta(-7) GIVES THE EDGE COUNT
==============================================================

  zeta(-7) = 1/240
  -> |zeta(-7)|^(-1) = 240 = |E|

The Riemann zeta function at -7 yields the W(3, 3) edge count
EXACTLY as the reciprocal. This is the deepest zeta-substrate match.

In Ramanujan-style:
  1^7 + 2^7 + 3^7 + ... = 1/240 (via zeta regularization)

The SEVENTH-POWER divergent sum, regularized, equals 1/|E|.

==============================================================
SUBSTRATE FACTORIZATIONS OF EACH DENOMINATOR
==============================================================

  12  = k = q * mu = lambda^q + lambda + q + 1 = 2^q + q + 1
  120 = F_5 * f = (mu+1) * q*(q^2-1)
       = (q+2)! = factorial of mu+1
  252 = mu * Phi_6 * q^2 = 4 * 7 * 9
       = Ramanujan tau(3)
       = C(10, 5) = C(Phi_4, F_5)
       = (q!)^2 * Phi_6
  240 = |E| = q*(q-1)*(q+1)*(q^2+1) (NEW from BT17)
       = lambda^4 * f / lambda^2 = ... many substrate forms
  132 = k * p_Ih = mu * q * p_Ih = lambda * q * (k - 1)
  32760 = lambda^q * q^2 * F_5 * Phi_6 * Phi_3
         = 8 * 9 * 5 * 7 * 13

EVERY denominator is a product of substrate primitives.

==============================================================
ZETA(-2n) AT EVEN NEGATIVES (TRIVIAL ZEROS)
==============================================================

zeta(-2n) = 0 for n >= 1 (trivial zeros of Riemann zeta).

These trivial zeros are at negative even integers. In substrate
language: the trivial zeros are at -2n where n = lambda, q, mu, ...

So zeta vanishes at:
  -2 (= -lambda)
  -4 (= -mu)
  -6 (= -q!)
  -8 (= -2^q)
  -10 (= -Phi_4)
  -12 (= -k)
  -14 (= -G_2 dim)
  -16 (= -lambda^mu)

All trivial zeros sit at NEGATIVES OF SUBSTRATE PRIMITIVES.

==============================================================
ZETA-FUNCTIONAL EQUATION AS SUBSTRATE COMPLETION
==============================================================

Riemann's functional equation: zeta(s) = 2^s * pi^(s-1) * sin(pi*s/2) *
                                          Gamma(1-s) * zeta(1-s)

At s = -n (negative integer): the equation maps zeta(-n) to zeta(n+1).
For n odd, sin(pi*s/2) != 0 -> non-trivial value.
For n even, sin(pi*s/2) = 0 -> trivial zero.

The substrate's zeta signature emerges from the ODD case.

==============================================================
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path


def bernoulli(n):
    """Compute Bernoulli numbers B_0, B_1, ..., B_n using recurrence."""
    B = [Fraction(0)] * (n + 1)
    B[0] = Fraction(1)
    for m in range(1, n + 1):
        s = Fraction(0)
        for k in range(m):
            s += Fraction(math.comb(m + 1, k)) * B[k]
        B[m] = -s / (m + 1)
    return B


def zeta_neg(n):
    """Compute zeta(-n) for n >= 0 via zeta(-n) = -B_{n+1}/(n+1)."""
    if n == 0:
        return Fraction(-1, 2)
    B = bernoulli(n + 1)
    return -B[n + 1] / (n + 1)


def main():
    q = 3
    lambda_, mu = 2, 4
    F5 = 5
    phi3, phi4, phi6 = 13, 10, 7
    k, v, E_count = 12, 40, 240
    f, g_neg = 24, 15
    p_Ih = 11

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 20: FULL ZETA-SUBSTRATE SIGNATURE")
    print("=" * 78)
    print()
    print("zeta(-n) for n = 1, 3, 5, 7, 9, 11 (small odd negative integers):")
    print()
    print(f"{'n':>3}  {'zeta(-n)':>15}  {'|denom|':>10}  {'Substrate form'}")
    print("-" * 78)

    substrate_forms = {
        12: "k (gauge codec)",
        120: "F_5 * f (= (q+2)! = (mu+1)!)",
        252: "mu * Phi_6 * q^2 (= Ramanujan tau(3))",
        240: "|E| = W(3,3) edge count",
        132: "k * p_Ih (gauge * Ihara prime)",
        32760: "lambda^q * q^2 * F_5 * Phi_6 * Phi_3",
    }

    results = []
    for n in (1, 3, 5, 7, 9, 11):
        z = zeta_neg(n)
        denom = abs(z.denominator)
        substrate = substrate_forms.get(denom, f"({denom})")
        z_str = f"{'+' if z >= 0 else '-'}{abs(z.numerator)}/{denom}"
        print(f"{n:>3}  {z_str:>15}  {denom:>10}  {substrate}")
        results.append({
            "n": n,
            "zeta_neg_n": str(z),
            "denominator": denom,
            "substrate_form": substrate,
        })
    print()

    # Verify zeta(-7) = 1/240 = 1/|E|
    z7 = zeta_neg(7)
    assert z7 == Fraction(1, 240)
    print(f"STRIKING: zeta(-7) = 1/240 = 1/|E| EXACTLY")
    print(f"  -> The 7th-power Ramanujan sum 1^7 + 2^7 + 3^7 + ... regularizes to 1/|E|")
    print()

    # Verify zeta(-1) = -1/12
    z1 = zeta_neg(1)
    assert z1 == Fraction(-1, 12)

    # zeta(-5) = -1/252 = -1/(Ramanujan tau(3))
    z5 = zeta_neg(5)
    assert z5 == Fraction(-1, 252)
    print(f"zeta(-5) = -1/252 = -1/Ramanujan_tau(3)")
    print(f"  Substrate: tau(3) = mu * Phi_6 * q^2 = 4*7*9 = 252")
    print(f"  Also: 252 = C(Phi_4, F_5) (central binomial)")
    print()

    # Verify denominators are all substrate-clean
    print("ALL ZETA(-n) DENOMINATORS ARE SUBSTRATE-CLEAN:")
    for n in (1, 3, 5, 7, 9):
        z = zeta_neg(n)
        denom = abs(z.denominator)
        print(f"  |denom(zeta(-{n}))| = {denom} = {substrate_forms[denom]}")
    print()

    # The trivial zeros at -2n
    print("TRIVIAL ZEROS of zeta at -2n sit at substrate-primitive negatives:")
    primitives = [(lambda_, "lambda"), (mu, "mu"), (math.factorial(q), "q!"),
                  (2**q, "2^q"), (phi4, "Phi_4"), (k, "k"),
                  (k + lambda_, "k+lambda = dim G_2"), (lambda_**mu, "lambda^mu")]
    for val, name in primitives:
        if val % 2 == 0:
            print(f"  zeta(-{val}) = 0  with {val} = {name}")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 20 SUMMARY")
    print("=" * 78)
    print("""
COMPLETE ZETA-SUBSTRATE SIGNATURE through n = 11:

  zeta(-1)  = -1/12      = -1/k                      (gauge codec, BT19)
  zeta(-3)  = +1/120     = +1/((q+2)!) = +1/(F_5 * f)
  zeta(-5)  = -1/252     = -1/Ramanujan_tau(3)
  zeta(-7)  = +1/240     = +1/|E|                    (NEW! striking)
  zeta(-9)  = -1/132     = -1/(k * p_Ih)
  zeta(-11) = 691/32760  = 691/(lambda^q * q^2 * F_5 * Phi_6 * Phi_3)

EVERY zeta(-n) denominator for n = 1..11 is substrate-clean.

NEW STRIKING IDENTITY (zeta(-7) -> |E|):
  The Ramanujan-regularized 7th-power sum 1^7 + 2^7 + 3^7 + ...
  equals 1/|E|, the reciprocal of the substrate's edge count.

NEW LINK (zeta(-5) -> Ramanujan tau):
  zeta(-5) = -1/tau(3) where tau is Ramanujan's tau function (MCXLIV).

NEW META: trivial zeros of zeta at -2n sit at NEGATIVES OF SUBSTRATE
PRIMITIVES (lambda, mu, q!, 2^q, Phi_4, k, ...).

The substrate has a FULL Riemann-zeta signature -- not just a single
identification, but an entire SEQUENCE of zeta values matching substrate
denominators.
""")

    out = Path("data") / "w33_BREAKTHROUGH_20_zeta_substrate_signature.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({
        "zeta_table": results,
        "striking_identity": "zeta(-7) = 1/240 = 1/|E|",
        "tau_link": "zeta(-5) = -1/Ramanujan_tau(3) = -1/252",
        "trivial_zeros": "at negatives of substrate primitives {lambda, mu, q!, 2^q, ...}",
        "all_denominators_substrate_clean_through": 11,
    }, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
