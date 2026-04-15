"""
BERNOULLI NUMBERS AND THE RIEMANN ZETA TOWER
=============================================

The natural INFINITE continuation of the cyclotomic/trig closure surface.

THE CHAIN.

From the Weinberg identity  q + Phi_4(q) = Phi_3(q)  we built a rational
closure surface for the Standard Model at q=3.  Extend it:

    zeta_n = e^(2 pi i / n)             (cyclotomic roots of unity)
          |                              (real/imag: cos, sin)
          v
    cot(pi x) = (i) (e^(i pi x) + e^(-i pi x)) / (e^(i pi x) - e^(-i pi x))
          |
          v   Mittag-Leffler :   cot(pi x) = 1/(pi x) + (2 x / pi) sum_{n>=1} 1/(x^2 - n^2)
          |
    Taylor:  pi x cot(pi x)  =  1  -  2 sum_{k>=1}  zeta(2 k)  x^(2 k)
          |
          v   Cross with   x/(e^x - 1) = sum_n B_n x^n / n!
          |
    zeta(2 n)  =  (2 pi)^(2 n)  |B_{2 n}|  /  (2 (2 n)!).

ANALYTIC CONTINUATION gives, for n >= 1,

    zeta(1 - 2 n)  =  - B_{2 n} / (2 n),        zeta(-2 n)  =  0   (trivial zeros),
    zeta(0)  =  -1/2.

PHYSICS.

    Casimir energy (per unit area, parallel plates)     ~  -  pi^2 / 720  (zeta(4) related)
    Stefan-Boltzmann constant                           ~  zeta(4)
    Photon number density  n_gamma = (2 zeta(3) / pi^2) (k T / h c)^3
    Planck energy spectrum moments                      involve  zeta(3), zeta(4)
    QED vacuum polarization                              involves  zeta(3)
    Anomalous magnetic moment  a_e                       is a polynomial in zeta(3), zeta(5)
"""
from __future__ import annotations

import json
from fractions import Fraction
from math import comb, factorial, pi
from pathlib import Path


# ======================================================================
#  Bernoulli numbers.
#
#      z / (e^z - 1)  =  sum_{n >= 0}  B_n z^n / n!.
#
#  Recursion: sum_{j=0}^{m} C(m+1, j) B_j = [m == 0].
#  For m >= 1 :    (m + 1) B_m  =  -  sum_{j=0}^{m-1} C(m+1, j) B_j.
# ======================================================================
_BERN_CACHE: dict = {0: Fraction(1)}


def bernoulli(n: int) -> Fraction:
    """Return B_n.  Convention: B_1 = -1/2 (positive form)."""
    if n in _BERN_CACHE:
        return _BERN_CACHE[n]
    for m in range(max(_BERN_CACHE) + 1, n + 1):
        s = Fraction(0)
        for j in range(m):
            s += Fraction(comb(m + 1, j)) * _BERN_CACHE[j]
        _BERN_CACHE[m] = -s / Fraction(m + 1)
    return _BERN_CACHE[n]


# ======================================================================
#  Riemann zeta at positive even integers.
#
#      zeta(2 n)  =  (2 pi)^(2 n)  |B_{2 n}|  /  (2 (2 n)!).
# ======================================================================
def zeta_even_pi_coefficient(n: int) -> Fraction:
    """Return the rational c such that  zeta(2 n) = c * pi^(2 n)."""
    assert n >= 1
    B_2n = bernoulli(2 * n)
    # (2 pi)^(2 n) = 4^n * pi^(2 n), so coefficient of pi^(2 n) is:
    #   4^n * |B_{2n}| / (2 (2 n)!)
    return Fraction(4 ** n) * abs(B_2n) / Fraction(2 * factorial(2 * n))


def zeta_even_as_rational_times_pi_power(n: int) -> tuple:
    """Return (c, 2*n) where zeta(2 n) = c * pi^(2 n)."""
    return zeta_even_pi_coefficient(n), 2 * n


# ======================================================================
#  Riemann zeta at negative odd integers  (non-trivial).
#
#      zeta(1 - 2 n)  =  - B_{2 n} / (2 n).
# ======================================================================
def zeta_negative_odd(n: int) -> Fraction:
    """Return zeta(1 - 2 n) for n >= 1."""
    assert n >= 1
    return -bernoulli(2 * n) / Fraction(2 * n)


# ======================================================================
#  Riemann zeta at negative even integers  =  0  (trivial zeros).
#
#  These come from B_{2 n + 1} = 0 for n >= 1.
# ======================================================================
def zeta_negative_even(n: int) -> Fraction:
    """Return zeta(-2 n) for n >= 1.  Always 0."""
    assert n >= 1
    return Fraction(0)


# ======================================================================
#  Numerical verification: partial sums  sum_{k=1}^{N} 1/k^s.
# ======================================================================
def zeta_partial_sum(s: float, N: int = 20000) -> float:
    out = 0.0
    for k in range(1, N + 1):
        out += 1.0 / k ** s
    return out


# ======================================================================
#  Cot / Bernoulli bridge:  pi x cot(pi x)  -  1  =  -2 sum  zeta(2 k) x^(2 k).
# ======================================================================
def cot_taylor_coefficients_from_bernoulli(order: int) -> list:
    """Return Taylor coefficients of  pi x cot(pi x)  up to  x^(2 * order).

    pi x cot(pi x)  =  1 + sum_{k >= 1} (-1)^k (2 pi)^(2 k) B_{2 k} / (2 k)!  x^(2 k).

    Each coefficient equals  -2 pi^(2 k) c_k  where  zeta(2 k) = c_k pi^(2 k).
    """
    out = [Fraction(1)]
    for k in range(1, order + 1):
        # coefficient of x^(2k) in pi x cot(pi x)
        Bk = bernoulli(2 * k)
        coef = Fraction((-1) ** k) * Fraction(4 ** k) * Bk / Fraction(factorial(2 * k))
        # Encode as rational multiple of pi^(2 k): coefficient = coef_rational * pi^(2 k)
        out.append(coef)
    return out


# ======================================================================
#  The W(3,3) bridge.
# ======================================================================
def w33_bridge() -> dict:
    """Connect the finite Phi_n(3) denominators to the infinite zeta tower.

    The SM closure denominators are cyclotomic evaluations at q=3:
        Phi_3(3) = 13,   Phi_4(3) = 10,   Phi_6(3) = 7.
    The ROOTS of each Phi_n give cos/sin at 2 pi / n.  The OO-limit of those
    angles (via cot partial-fraction sum over ALL integer multiples) gives
    the zeta tower:  zeta(2 k) = (2 pi)^(2 k) |B_{2 k}| / (2 (2 k)!).
    """
    return {
        "finite_slots_at_q=3":   {"Phi_3(3)": 13, "Phi_4(3)": 10, "Phi_6(3)": 7},
        "infinite_zeta_tower":   {
            "zeta(2)": "pi^2 / 6",
            "zeta(4)": "pi^4 / 90",
            "zeta(6)": "pi^6 / 945",
            "zeta(8)": "pi^8 / 9450",
            "zeta(10)": "pi^10 / 93555",
        },
        "bridge_identity":
            "cot(pi x) = 1/(pi x) - (2/pi) sum_{k>=1} zeta(2 k) x^(2 k - 1)",
    }


# ======================================================================
#  Physics: blackbody / Casimir / CMB photon density.
# ======================================================================
def stefan_boltzmann_pi4_coefficient() -> Fraction:
    """Stefan-Boltzmann:  sigma = (pi^2 / 60)  * k^4 / (hbar^3 c^2).

    The dimensionless factor is  pi^2 / 60  =  (pi^2 / 6) * (1/10) = zeta(2) / 10.
    Actually the integral gives sigma proportional to  zeta(4) * 6/pi^4 = ...
    The coefficient of T^4 in the Stefan-Boltzmann law is  pi^2/60 in natural units.
    """
    return Fraction(1, 60)


def cmb_photon_number_density_coefficient() -> str:
    """n_gamma / T^3   ~   (2 zeta(3) / pi^2)  (natural units).

    zeta(3) is irrational (Apery's constant, 1.2020569...) so we cannot
    express it as a Fraction * pi^n.  But we CAN pin the coefficient
    formula symbolically.
    """
    return "n_gamma / T^3 = 2 zeta(3) / pi^2  (Planck blackbody)"


# ======================================================================
#  Driver.
# ======================================================================
def derive_all_zeta(max_even: int = 6, max_neg_odd: int = 6) -> dict:
    bern = {n: str(bernoulli(n)) for n in range(0, 2 * max_even + 1)}

    zeta_even = {}
    for n in range(1, max_even + 1):
        c = zeta_even_pi_coefficient(n)
        zeta_even[f"zeta({2 * n})"] = {
            "coefficient_of_pi^{2n}": str(c),
            "pretty": f"pi^{2 * n} * {c}" if c != 0 else "0",
            "numeric": float(c) * pi ** (2 * n),
        }

    zeta_neg_odd = {}
    for n in range(1, max_neg_odd + 1):
        zeta_neg_odd[f"zeta({1 - 2 * n})"] = str(zeta_negative_odd(n))

    zeta_trivial = {f"zeta(-{2 * n})": "0" for n in range(1, 4)}

    # Verify zeta(2n) numerically against partial sum for small n.
    checks = {}
    for n in (1, 2, 3):
        exact = float(zeta_even_pi_coefficient(n)) * pi ** (2 * n)
        approx = zeta_partial_sum(2 * n, N=50000)
        checks[f"zeta({2 * n})"] = {
            "exact_from_Bernoulli": exact,
            "partial_sum_N=50000":  approx,
            "rel_error":            abs(exact - approx) / exact,
        }

    # Cot Taylor coefficients.
    cot_coefs = cot_taylor_coefficients_from_bernoulli(order=5)

    return {
        "bernoulli_numbers":         bern,
        "zeta_even_positive":        zeta_even,
        "zeta_negative_odd":         zeta_neg_odd,
        "zeta_negative_even_trivial": zeta_trivial,
        "zeta(0)":                   "-1/2",
        "cot_taylor_coefficients":   [str(c) for c in cot_coefs],
        "numerical_verification":    checks,
        "w33_bridge":                w33_bridge(),
        "physics": {
            "stefan_boltzmann_coefficient_of_pi2": str(stefan_boltzmann_pi4_coefficient()),
            "cmb_photon_density":  cmb_photon_number_density_coefficient(),
        },
    }


def main() -> None:
    print("=" * 72)
    print("  BERNOULLI NUMBERS & RIEMANN ZETA TOWER")
    print("=" * 72)
    print()

    print("  BERNOULLI NUMBERS  B_n   (from the recursion):")
    for n in range(0, 13):
        print(f"    B_{n:<2d} = {bernoulli(n)}")
    print()

    print("  ZETA AT POSITIVE EVEN INTEGERS   zeta(2 n)  =  c * pi^{2 n}:")
    for n in range(1, 7):
        c = zeta_even_pi_coefficient(n)
        print(f"    zeta({2 * n:<2d}) = ({c}) * pi^{2 * n}   =   {float(c) * pi ** (2 * n):.10f}")
    print()

    print("  ZETA AT NEGATIVE ODD INTEGERS   zeta(1 - 2 n)  =  - B_{2 n} / (2 n):")
    for n in range(1, 6):
        v = zeta_negative_odd(n)
        print(f"    zeta({1 - 2 * n:<3d}) = {v}")
    print()

    print("  ZETA AT NEGATIVE EVEN INTEGERS   (trivial zeros):")
    for n in range(1, 4):
        print(f"    zeta(-{2 * n}) = 0")
    print()

    print("  zeta(0) = -1/2")
    print()

    print("  COT TAYLOR EXPANSION  pi x cot(pi x) = 1 - 2 sum zeta(2 k) x^{2 k}:")
    coefs = cot_taylor_coefficients_from_bernoulli(order=5)
    for k, c in enumerate(coefs):
        if k == 0:
            print(f"    constant = {c}")
        else:
            # coefficient times pi^(2k) should equal -2 * zeta_even_coeff(k)
            zk = zeta_even_pi_coefficient(k)
            print(f"    x^{2 * k:<2d} coef = ({c}) * pi^{2 * k} ;  matches  -2 * zeta({2 * k})/pi^{2 * k} = {-2 * zk}")
    print()

    print("  NUMERICAL VERIFICATION (partial sum vs exact):")
    for n in (1, 2, 3):
        exact = float(zeta_even_pi_coefficient(n)) * pi ** (2 * n)
        approx = zeta_partial_sum(2 * n, N=50000)
        print(f"    zeta({2 * n}): exact = {exact:.12f},  partial = {approx:.12f},"
              f"  rel err = {abs(exact - approx) / exact:.2e}")
    print()

    print("  W(3,3) BRIDGE:")
    bridge = w33_bridge()
    print(f"    finite slots at q=3 : {bridge['finite_slots_at_q=3']}")
    print(f"    infinite zeta tower : pi^2/6, pi^4/90, pi^6/945, pi^8/9450, pi^10/93555, ...")
    print(f"    bridge identity     : {bridge['bridge_identity']}")
    print()

    chain = derive_all_zeta()
    out = Path(__file__).resolve().parent.parent / "data" / "w33_bernoulli_zeta.json"
    out.write_text(json.dumps(chain, indent=2, default=str))
    print(f"  wrote {out}")


if __name__ == "__main__":
    main()
