"""Dedekind eta transformation law, Dedekind sums, and the Rademacher exact
formula for p(n).

Closes a fundamental algebraic layer:

    (i)  Dedekind sum s(h, k) = sum_{a=1}^{k-1} (a/k) ((h a / k))
         where ((x)) = x - floor(x) - 1/2  if  x not in Z, else 0.

    (ii) Dedekind reciprocity:
            s(h, k) + s(k, h) = -1/4 + (1/12)(h/k + k/h + 1/(h k)).

    (iii) eta transformation under SL_2(Z):
            eta(tau + 1)  = exp(pi i / 12) . eta(tau),
            eta(-1/tau)   = sqrt(-i tau) . eta(tau).

    (iv) Rademacher exact formula:

            p(n) = (1 / (pi sqrt(2))) . sum_{k=1}^infinity
                    sqrt(k) . A_k(n) . d/dn [ sinh(C sqrt(n - 1/24)/k)
                                              / sqrt(n - 1/24) ]

         where  C = pi sqrt(2/3)  and
                A_k(n) = sum_{0 <= h < k, gcd(h,k)=1}
                         exp( pi i s(h,k) - 2 pi i n h / k ).

         Truncating the Rademacher sum to finite k and rounding to the
         nearest integer recovers the exact partition value p(n).

The 24 in the eta multiplier system is the same 24 driving the Leech
lattice rank, moonshine, and the bosonic-string critical dimension.
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd
from typing import Any

import mpmath as mp


# ----------------------------------------------------------------------
# Dedekind sum s(h, k).
# ----------------------------------------------------------------------
def _sawtooth(x: Fraction) -> Fraction:
    """((x)) = x - floor(x) - 1/2 if x not integer, else 0."""
    frac = x - int(x)
    if frac < 0:
        frac += 1
    if frac == 0:
        return Fraction(0)
    return frac - Fraction(1, 2)


def dedekind_sum(h: int, k: int) -> Fraction:
    """Exact Dedekind sum.  k > 0, any integer h; depends only on h mod k."""
    if k <= 0:
        raise ValueError("k must be positive")
    h = h % k
    total = Fraction(0)
    for a in range(1, k):
        total += _sawtooth(Fraction(a, k)) * _sawtooth(Fraction(h * a, k))
    return total


def dedekind_reciprocity_gap(h: int, k: int) -> Fraction:
    """Should be zero by the reciprocity law (for gcd(h,k) = 1)."""
    if gcd(h, k) != 1:
        raise ValueError("require gcd(h, k) = 1")
    lhs = dedekind_sum(h, k) + dedekind_sum(k, h)
    rhs = Fraction(-1, 4) + Fraction(1, 12) * (
        Fraction(h, k) + Fraction(k, h) + Fraction(1, h * k)
    )
    return lhs - rhs


# Tabulated special values for pinning.
DEDEKIND_SUM_TABLE: dict[tuple[int, int], Fraction] = {
    (1, 1): Fraction(0),
    (1, 2): Fraction(0),
    (1, 3): Fraction(1, 18),
    (1, 4): Fraction(1, 8),
    (1, 5): Fraction(1, 5),
    (1, 6): Fraction(5, 18),
    (1, 7): Fraction(5, 14),
    (1, 8): Fraction(7, 16),
    (1, 9): Fraction(14, 27),
    (1, 12): Fraction(55, 72),
    (2, 7): Fraction(1, 14),
    (3, 7): Fraction(-1, 14),
    (2, 9): Fraction(4, 27),
    (5, 12): Fraction(-1, 72),
}


def verify_dedekind_table() -> dict[str, Any]:
    fails: list[tuple[int, int, Fraction, Fraction]] = []
    for (h, k), expected in DEDEKIND_SUM_TABLE.items():
        got = dedekind_sum(h, k)
        if got != expected:
            fails.append((h, k, got, expected))
    return {"all_match": not fails, "failures": fails}


def verify_reciprocity(max_k: int = 20) -> dict[str, Any]:
    fails: list[tuple[int, int, Fraction]] = []
    for k in range(1, max_k + 1):
        for h in range(1, k):
            if gcd(h, k) != 1:
                continue
            gap = dedekind_reciprocity_gap(h, k)
            if gap != 0:
                fails.append((h, k, gap))
    return {"all_zero": not fails, "failures": fails}


# ----------------------------------------------------------------------
# eta transformation law.
# ----------------------------------------------------------------------
def eta_mpmath(tau: mp.mpc) -> mp.mpc:
    """Dedekind eta via the Euler product truncated to high precision.

    eta(tau) = q^{1/24} prod_{n>=1} (1 - q^n),  q = exp(2 pi i tau).
    """
    q = mp.exp(2j * mp.pi * tau)
    prod = mp.mpc(1)
    for n in range(1, 220):
        prod *= 1 - q**n
    return mp.exp(mp.mpc(0, 1) * mp.pi * tau / 12) * prod


def eta_translation_ratio(tau: mp.mpc) -> mp.mpc:
    """eta(tau + 1) / eta(tau).  Should be exp(i pi / 12)."""
    return eta_mpmath(tau + 1) / eta_mpmath(tau)


def eta_inversion_ratio(tau: mp.mpc) -> mp.mpc:
    """eta(-1/tau) / (sqrt(-i tau) . eta(tau)).  Should be 1."""
    return eta_mpmath(-1 / tau) / (mp.sqrt(-1j * tau) * eta_mpmath(tau))


def verify_eta_translation(points: list[complex]) -> dict[str, Any]:
    mp.mp.dps = 40
    expected = mp.exp(1j * mp.pi / 12)
    rows: list[dict[str, Any]] = []
    max_err = mp.mpf(0)
    for pt in points:
        tau = mp.mpc(pt)
        ratio = eta_translation_ratio(tau)
        err = abs(ratio - expected)
        if err > max_err:
            max_err = err
        rows.append({"tau": pt, "ratio_abs_err": float(err)})
    return {
        "expected_multiplier": {"re": float(expected.real), "im": float(expected.imag)},
        "max_abs_err": float(max_err),
        "rows": rows,
        "within_tol": bool(max_err < mp.mpf("1e-25")),
    }


def verify_eta_inversion(points: list[complex]) -> dict[str, Any]:
    mp.mp.dps = 40
    rows: list[dict[str, Any]] = []
    max_err = mp.mpf(0)
    for pt in points:
        tau = mp.mpc(pt)
        ratio = eta_inversion_ratio(tau)
        err = abs(ratio - 1)
        if err > max_err:
            max_err = err
        rows.append({"tau": pt, "deviation_from_1": float(err)})
    return {
        "max_abs_err": float(max_err),
        "rows": rows,
        "within_tol": bool(max_err < mp.mpf("1e-20")),
    }


# ----------------------------------------------------------------------
# A_k(n) Kloosterman-type sum.
# ----------------------------------------------------------------------
def A_k(k: int, n: int) -> mp.mpc:
    """A_k(n) = sum_{0<=h<k, gcd(h,k)=1} exp(pi i s(h,k) - 2 pi i n h / k)."""
    total = mp.mpc(0)
    for h in range(0, k):
        if gcd(h, k) != 1:
            continue
        s = dedekind_sum(h, k)
        phase = mp.mpc(0, 1) * (mp.pi * mp.mpf(s.numerator) / mp.mpf(s.denominator)
                                - 2 * mp.pi * n * h / k)
        total += mp.exp(phase)
    return total


# ----------------------------------------------------------------------
# Rademacher truncated series for p(n).
# ----------------------------------------------------------------------
def rademacher_partition(n: int, K: int = 25) -> mp.mpf:
    """Truncated Rademacher series for p(n).  Rounding to nearest int recovers
    the exact partition value as K grows (empirically K ~ sqrt(n) suffices)."""
    if n == 0:
        # Rademacher series at n=0 returns 1 cleanly at K>=1 with correct limit;
        # we just special-case to avoid 1/0 sqrt term.
        return mp.mpf(1)
    mp.mp.dps = 50
    C = mp.pi * mp.sqrt(mp.mpf(2) / 3)
    x = mp.mpf(n) - mp.mpf(1) / 24
    sqx = mp.sqrt(x)
    total = mp.mpf(0)
    for k in range(1, K + 1):
        ak = A_k(k, n)
        # d/dn of sinh(C sqx/k)/sqx  where sqx = sqrt(n - 1/24):
        #   = (1/(2 sqx)) d/dx [ sinh(C sqx/k)/sqx ]
        # Use closed form:
        #   d/dn[ sinh(z)/sqx ] with z = C sqx / k:
        #   let u = sqx => du/dn = 1/(2 sqx).
        #   f = sinh(C u / k) / u,
        #   df/du = (C/k) cosh(C u / k) / u - sinh(C u / k) / u^2
        #   df/dn = df/du * du/dn.
        u = sqx
        z = C * u / k
        df_du = (C / k) * mp.cosh(z) / u - mp.sinh(z) / (u * u)
        df_dn = df_du / (2 * u)
        total += mp.sqrt(mp.mpf(k)) * ak * df_dn
    total /= mp.pi * mp.sqrt(mp.mpf(2))
    # Imaginary part is truncation noise; take real part.
    return mp.re(total)


# ----------------------------------------------------------------------
# Reference partition values to pin the Rademacher series against.
# ----------------------------------------------------------------------
RADEMACHER_TARGETS: dict[int, int] = {
    1: 1,
    5: 7,
    10: 42,
    20: 627,
    50: 204226,
    100: 190569292,
}


def verify_rademacher(K: int = 25) -> dict[str, Any]:
    """Pin truncated Rademacher sums against known p(n)."""
    rows: list[dict[str, Any]] = []
    all_match = True
    for n, expected in RADEMACHER_TARGETS.items():
        approx = rademacher_partition(n, K=K)
        rounded = int(mp.nint(approx))
        match = rounded == expected
        all_match = all_match and match
        rows.append({
            "n": n,
            "expected": expected,
            "rademacher_approx": float(approx),
            "rounded": rounded,
            "match": match,
            "abs_err_pre_round": float(abs(approx - expected)),
        })
    return {"all_match": all_match, "rows": rows, "K_truncation": K}


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    table = verify_dedekind_table()
    recip = verify_reciprocity(max_k=20)
    points_T = [0.1 + 0.5j, -0.3 + 0.8j, 0.7 + 1.2j]
    points_S = [0.1 + 0.5j, 0.3 + 0.8j, 0.7 + 1.2j]
    trans = verify_eta_translation(points_T)
    inv = verify_eta_inversion(points_S)
    rade = verify_rademacher(K=25)
    chain = {
        "dedekind_table_match": table["all_match"],
        "reciprocity_holds": recip["all_zero"],
        "eta_translation_multiplier_is_exp_ipi_over_12": trans["within_tol"],
        "eta_inversion_multiplier_is_sqrt_minus_i_tau": inv["within_tol"],
        "rademacher_recovers_p_n": rade["all_match"],
    }
    return {
        "dedekind_table": table,
        "reciprocity": recip,
        "eta_translation": trans,
        "eta_inversion": inv,
        "rademacher": rade,
        "summary_chain": chain,
    }


if __name__ == "__main__":
    import json
    s = derive_all()
    # Summarise.
    print("summary_chain:")
    for k, v in s["summary_chain"].items():
        print(f"  {k}: {v}")
    print("\nreciprocity max_k=20:", s["reciprocity"]["all_zero"])
    print("eta translation max err:", s["eta_translation"]["max_abs_err"])
    print("eta inversion max err:", s["eta_inversion"]["max_abs_err"])
    print("rademacher K=25 row for n=100:")
    for row in s["rademacher"]["rows"]:
        if row["n"] == 100:
            print(" ", row)
