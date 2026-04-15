"""
EISENSTEIN SERIES, RAMANUJAN DELTA, AND THE j-INVARIANT
========================================================

The modular-form continuation of the Bernoulli / zeta tower.

    E_{2 k}(tau)  =  1  -  (4 k / B_{2 k})  sum_{n >= 1}  sigma_{2 k - 1}(n)  q^n,

where  q = e^(2 pi i tau)  and  sigma_j(n) = sum_{d | n} d^j.  The identity

    E_4(tau)^3  -  E_6(tau)^2   =   1728  Delta(tau)

defines the DISCRIMINANT cusp form

    Delta(tau)  =  q  prod_{n >= 1} (1 - q^n)^24   =   sum_{n >= 1}  tau(n)  q^n,

and the KLEIN j-INVARIANT

    j(tau)  =  1728  E_4(tau)^3 / (E_4(tau)^3 - E_6(tau)^2)  =  E_4(tau)^3 / Delta(tau)
           =   1/q  +  744  +  196884 q  +  21493760 q^2  +  864299970 q^3  +  ...

MONSTROUS MOONSHINE:  196884 = 196883 + 1,  where 196883 is the dimension
of the smallest non-trivial irrep of the Monster simple group M.  Every
j-coefficient is a non-negative integer linear combination of Monster
irrep dimensions.

BRIDGE TO W(3,3).  The Bernoulli numbers  B_2 = 1/6,  B_4 = -1/30,  B_6 = 1/42,
B_8 = -1/30  give the Eisenstein constants  240 (E_4), -504 (E_6), 480 (E_8),
-264 (E_10).  The divisor sums  sigma_{2k-1}(n)  are arithmetic, not SRG-derived,
but the K3 / E8 lattice theta series land in the same ring  C[E_4, E_6].
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from w33_bernoulli_zeta import bernoulli


# ======================================================================
#  Divisor sum  sigma_k(n) = sum_{d | n} d^k.
# ======================================================================
def sigma_k(n: int, k: int) -> int:
    return sum(d ** k for d in range(1, n + 1) if n % d == 0)


# ======================================================================
#  Eisenstein series  E_{2k}(tau)  Fourier coefficients.
# ======================================================================
def eisenstein_constant(k: int) -> Fraction:
    """Return  -4 k / B_{2 k}, the coefficient in front of  sigma_{2k-1}(n)."""
    return -Fraction(4 * k) / bernoulli(2 * k)


def eisenstein_qseries(k: int, order: int) -> list:
    """Return  [a_0, a_1, ..., a_order]  where  E_{2k}(tau) = sum  a_n q^n."""
    c = eisenstein_constant(k)
    out = [Fraction(1)] + [c * Fraction(sigma_k(n, 2 * k - 1)) for n in range(1, order + 1)]
    return out


# ======================================================================
#  Truncated q-series arithmetic.
# ======================================================================
def qmul(a, b, order):
    out = [Fraction(0)] * (order + 1)
    for i, ai in enumerate(a[:order + 1]):
        for j, bj in enumerate(b[:order + 1 - i]):
            out[i + j] += ai * bj
    return out


def qpow(a, n, order):
    if n == 0:
        r = [Fraction(0)] * (order + 1); r[0] = Fraction(1)
        return r
    base = list(a[:order + 1])
    result = None
    while n > 0:
        if n & 1:
            result = base if result is None else qmul(result, base, order)
        n //= 2
        if n:
            base = qmul(base, base, order)
    return result


def qsub(a, b, order):
    return [(a[i] if i < len(a) else Fraction(0))
            - (b[i] if i < len(b) else Fraction(0)) for i in range(order + 1)]


def qinv(a, order):
    """1 / a  as a power series, assuming a[0] != 0."""
    assert a[0] != 0
    inv = [Fraction(0)] * (order + 1)
    inv[0] = Fraction(1) / Fraction(a[0])
    for n in range(1, order + 1):
        s = Fraction(0)
        for k in range(1, n + 1):
            if k < len(a):
                s += Fraction(a[k]) * inv[n - k]
        inv[n] = -s / Fraction(a[0])
    return inv


# ======================================================================
#  Delta  and  tau  (Ramanujan tau function).
# ======================================================================
def delta_qseries(order: int) -> list:
    """Delta(tau) = (E_4^3 - E_6^2) / 1728.

    Returns [0, tau(1), tau(2), ...]:  the Ramanujan tau numbers.
    """
    E4 = eisenstein_qseries(2, order)
    E6 = eisenstein_qseries(3, order)
    E4_cubed = qpow(E4, 3, order)
    E6_squared = qpow(E6, 2, order)
    diff = qsub(E4_cubed, E6_squared, order)
    return [c / Fraction(1728) for c in diff]


def ramanujan_tau(n: int) -> int:
    """The Ramanujan tau function tau(n), computed via Delta."""
    d = delta_qseries(n)
    val = d[n]
    assert val.denominator == 1
    return int(val)


# ======================================================================
#  Klein j-invariant  j(tau)  as Laurent series:  coef of q^n for n >= -1.
# ======================================================================
def j_invariant_qseries(order: int) -> dict:
    """Return {n: coefficient of q^n in j(tau)}  for  n in -1..order.

    j = E_4^3 / Delta = E_4^3 / (q * Delta_tilde)  where Delta_tilde[0]=1.
    """
    oh = order + 2
    E4 = eisenstein_qseries(2, oh)
    E4_cubed = qpow(E4, 3, oh)
    D = delta_qseries(oh)
    # D = q * D_tilde, so D_tilde starts at q^0 with leading 1.
    D_tilde = D[1:]
    inv_Dt = qinv(D_tilde, oh - 1)
    prod_series = qmul(E4_cubed, inv_Dt, oh - 1)
    # j's coefficient at q^n = prod_series[n + 1] for n >= -1.
    out = {}
    for n in range(-1, order + 1):
        c = prod_series[n + 1]
        assert c.denominator == 1, f"j coefficient not integer: {c} at q^{n}"
        out[n] = int(c)
    return out


# ======================================================================
#  Modular identities verified at q-series level.
# ======================================================================
def verify_E4_cubed_minus_E6_squared_equals_1728_delta(order: int) -> bool:
    E4 = eisenstein_qseries(2, order)
    E6 = eisenstein_qseries(3, order)
    E4_c = qpow(E4, 3, order)
    E6_s = qpow(E6, 2, order)
    D = delta_qseries(order)
    lhs = qsub(E4_c, E6_s, order)
    rhs = [Fraction(1728) * c for c in D]
    return lhs == rhs


def verify_E8_equals_E4_squared(order: int) -> bool:
    """E_8 = E_4^2  is a classical identity of modular forms of weight 8."""
    E4 = eisenstein_qseries(2, order)
    E4_sq = qpow(E4, 2, order)
    E8 = eisenstein_qseries(4, order)
    return E4_sq == E8


def verify_E10_equals_E4_times_E6(order: int) -> bool:
    """E_10 = E_4 E_6 (both are the unique weight-10 Eisenstein, up to scale)."""
    E4 = eisenstein_qseries(2, order)
    E6 = eisenstein_qseries(3, order)
    prod = qmul(E4, E6, order)
    E10 = eisenstein_qseries(5, order)
    return prod == E10


# ======================================================================
#  Monstrous Moonshine:  196884 = 196883 + 1.
# ======================================================================
def moonshine_check(order_min: int = 2) -> dict:
    j = j_invariant_qseries(order_min)
    c1 = j[1]
    return {
        "j_coef_q":             c1,
        "monster_irrep_196883": 196883,
        "plus_trivial":         1,
        "match":                c1 == 196883 + 1,
    }


# ======================================================================
#  Driver.
# ======================================================================
def derive_all_modular(order: int = 10) -> dict:
    E4 = eisenstein_qseries(2, order)
    E6 = eisenstein_qseries(3, order)
    E8 = eisenstein_qseries(4, order)
    E10 = eisenstein_qseries(5, order)
    E12 = eisenstein_qseries(6, order)
    D = delta_qseries(order)
    j = j_invariant_qseries(order)

    tau_vals = {n: int(D[n]) for n in range(1, order + 1)}

    return {
        "eisenstein_constants": {
            "240 (E_4)":  str(eisenstein_constant(2)),
            "-504 (E_6)": str(eisenstein_constant(3)),
            "480 (E_8)":  str(eisenstein_constant(4)),
            "-264 (E_10)": str(eisenstein_constant(5)),
            "65520/691 (E_12)": str(eisenstein_constant(6)),
        },
        "E_4_qseries":  [str(c) for c in E4],
        "E_6_qseries":  [str(c) for c in E6],
        "E_8_qseries":  [str(c) for c in E8],
        "E_10_qseries": [str(c) for c in E10],
        "E_12_qseries": [str(c) for c in E12],
        "delta_qseries":    [str(c) for c in D],
        "ramanujan_tau":    tau_vals,
        "j_invariant":      j,
        "identities": {
            "E_4^3 - E_6^2 = 1728 Delta": verify_E4_cubed_minus_E6_squared_equals_1728_delta(order),
            "E_8 = E_4^2":                verify_E8_equals_E4_squared(order),
            "E_10 = E_4 E_6":             verify_E10_equals_E4_times_E6(order),
        },
        "moonshine":        moonshine_check(order_min=max(2, order)),
    }


def main() -> None:
    print("=" * 72)
    print("  EISENSTEIN SERIES, DELTA, j-INVARIANT, AND MOONSHINE")
    print("=" * 72)
    print()

    print("  EISENSTEIN CONSTANTS  -4k / B_{2k}:")
    for k in (2, 3, 4, 5, 6):
        c = eisenstein_constant(k)
        print(f"    E_{2 * k} constant = -4*{k}/B_{2 * k} = {c}")
    print()

    order = 10
    print(f"  E_4(tau)  first {order + 1} Fourier coefficients:")
    E4 = eisenstein_qseries(2, order)
    print(f"    {[int(c) for c in E4]}")
    print()

    print(f"  E_6(tau)  first {order + 1} Fourier coefficients:")
    E6 = eisenstein_qseries(3, order)
    print(f"    {[int(c) for c in E6]}")
    print()

    print(f"  Delta(tau)  first {order + 1} Fourier coefficients  (Ramanujan tau):")
    D = delta_qseries(order)
    print(f"    {[int(c) for c in D]}")
    print()

    print(f"  j(tau)  Laurent coefficients at q^n for n = -1 .. {order}:")
    j = j_invariant_qseries(order)
    for n in sorted(j):
        print(f"    q^{n:<3d} : {j[n]}")
    print()

    print("  MODULAR IDENTITIES:")
    print(f"    E_4^3 - E_6^2 = 1728 Delta ?  "
          f"{verify_E4_cubed_minus_E6_squared_equals_1728_delta(order)}")
    print(f"    E_8 = E_4^2 ?                 {verify_E8_equals_E4_squared(order)}")
    print(f"    E_10 = E_4 E_6 ?              {verify_E10_equals_E4_times_E6(order)}")
    print()

    m = moonshine_check(order_min=max(2, order))
    print("  MONSTROUS MOONSHINE:")
    print(f"    j coefficient at q^1 = {m['j_coef_q']}")
    print(f"    196883 + 1           = {m['monster_irrep_196883'] + m['plus_trivial']}")
    print(f"    match?               = {m['match']}")
    print()

    chain = derive_all_modular(order=order)
    out = Path(__file__).resolve().parent.parent / "data" / "w33_eisenstein.json"
    out.write_text(json.dumps(chain, indent=2, default=str))
    print(f"  wrote {out}")


if __name__ == "__main__":
    main()
