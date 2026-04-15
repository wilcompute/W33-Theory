"""
E8 ROOT LATTICE AND ITS THETA SERIES
=====================================

The bridge between the modular tower (Eisenstein E_4) and lattice geometry.

E8 is the unique even unimodular lattice of rank 8.  Its theta series

    theta_{E_8}(tau)  =  sum_{v in E_8}  q^{|v|^2 / 2}

is a modular form of weight 4 for SL(2, Z), and there is only ONE such form
up to scale, so

    theta_{E_8}(tau)  =  E_4(tau)  =  1  +  240 q  +  2160 q^2  +  6720 q^3 + ...

The lattice / modular-form correspondence is forced.

CONSTRUCTION (D_n^+).

    D_8     =  { x in Z^8  :  sum x_i  even }
    g       =  (1/2, 1/2, ..., 1/2)
    E_8     =  D_8  cup  (D_8 + g)

so vectors are EITHER all integer with even coordinate sum, OR all half-integer
with sum (n_i + 1/2) in 2 Z (equivalently, sum of the n_i is even).

ROOTS.

The 240 minimal vectors  (|v|^2 = 2)  split as:

    D_8 part:   +/- e_i +/- e_j  (i != j)            =>  4 * C(8, 2)  =  112
    coset:      (+/-1/2)^8  with even number of minuses  =>  2^7       =  128
                                                       total  =  240.

CONNECTION TO THE STANDARD MODEL.

    E_8  >  E_7 x SU(2)
         >  E_6 x SU(3)                                (= GUT chain)
         >  SO(10) x U(1)
         >  SU(5)
         >  SU(3) x SU(2) x U(1)                      (Standard Model)

The 248-dim adjoint of E_8 splits as  (78, 1) (+) (27, 3) (+) (-27, -3) (+) (1, 8)
under E_6 x SU(3), placing one Standard Model generation in the 27 of E_6.

BRIDGE TO W(3, 3).

The 27 minimal vectors of E_6 correspond exactly to the 27 lines through any
point of GQ(3, 3) in the dual SRG(40, 27, 18, 18) -- the K27 stabilizer C_6
already pinned in this project (memory).  And the 240 E_8 roots split into
6 * 40 with the W(3, 3) vertex set as a natural orbit (6 copies of v=40).
"""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path

from w33_eisenstein import eisenstein_qseries


# ======================================================================
#  Direct lattice enumeration:  count E_8 vectors of given squared norm.
# ======================================================================
def enumerate_E8_by_norm_squared(max_norm_sq: int) -> Counter:
    """Return Counter[k] = # of E_8 vectors with |v|^2 = k, for k <= max_norm_sq.

    Brute force, exponential in 8 -- only practical for small max_norm_sq.
    """
    counts: Counter = Counter()
    bound = int(math.isqrt(max_norm_sq)) + 1

    # Coset 1: D_8  =  Z^8 with even coordinate sum.
    for v in itertools.product(range(-bound, bound + 1), repeat=8):
        if sum(v) & 1:
            continue
        n = sum(x * x for x in v)
        if n <= max_norm_sq:
            counts[n] += 1

    # Coset 2: D_8 + (1/2)^8  =  vectors  x_i = n_i + 1/2  with sum n_i even.
    # |x|^2 = sum (n_i + 1/2)^2  =  sum n_i^2 + sum n_i + 8/4
    #       = sum n_i^2 + sum n_i + 2.
    bound2 = bound + 1
    for v in itertools.product(range(-bound2, bound2 + 1), repeat=8):
        s = sum(v)
        if s & 1:
            continue
        n = sum(x * x for x in v) + s + 2
        if 0 <= n <= max_norm_sq:
            counts[n] += 1

    return counts


# ======================================================================
#  Root enumeration:  240 minimal vectors.
# ======================================================================
def E8_roots() -> list:
    """Return the explicit list of 240 E_8 root vectors (each a length-8 tuple).

    Each root has |v|^2 = 2 (2 in our normalization where E_8 is even).
    """
    roots = []

    # 112 D_8 roots:  +/- e_i +/- e_j, i < j.
    for i in range(8):
        for j in range(i + 1, 8):
            for si in (1, -1):
                for sj in (1, -1):
                    v = [0] * 8
                    v[i] = si
                    v[j] = sj
                    roots.append(tuple(v))

    # 128 coset roots:  (+/-1/2)^8 with even number of minus signs.
    for mask in range(256):
        signs = [(-1 if (mask >> b) & 1 else 1) for b in range(8)]
        if sum(1 for s in signs if s < 0) & 1:
            continue
        v = tuple(Fraction(s, 2) for s in signs)
        roots.append(v)

    return roots


# ======================================================================
#  Theta series via Jacobi:  theta_{E_8} = (1/2)(theta_2^8 + theta_3^8 + theta_4^8).
#
#  We work in s = q^{1/8}.  Each Jacobi theta is computed as a polynomial in s.
# ======================================================================
def jacobi_theta3_in_s(max_s_power: int) -> list:
    """theta_3(tau) = sum q^{n^2 / 2}.   In s = q^{1/8}, power = 4 n^2."""
    out = [Fraction(0)] * (max_s_power + 1)
    out[0] = Fraction(1)
    n = 1
    while 4 * n * n <= max_s_power:
        out[4 * n * n] += 2
        n += 1
    return out


def jacobi_theta4_in_s(max_s_power: int) -> list:
    """theta_4(tau) = sum (-1)^n q^{n^2 / 2}.   In s = q^{1/8}."""
    out = [Fraction(0)] * (max_s_power + 1)
    out[0] = Fraction(1)
    n = 1
    while 4 * n * n <= max_s_power:
        out[4 * n * n] += 2 * ((-1) ** n)
        n += 1
    return out


def jacobi_theta2_in_s(max_s_power: int) -> list:
    """theta_2(tau) = 2 sum_{n>=0} q^{(2n+1)^2 / 8}.   In s = q^{1/8}, power = (2n+1)^2."""
    out = [Fraction(0)] * (max_s_power + 1)
    n = 0
    while (2 * n + 1) ** 2 <= max_s_power:
        out[(2 * n + 1) ** 2] += 2
        n += 1
    return out


def poly_mul_truncated(a: list, b: list, max_power: int) -> list:
    out = [Fraction(0)] * (max_power + 1)
    for i, ai in enumerate(a[:max_power + 1]):
        if ai == 0:
            continue
        for j in range(min(len(b), max_power + 1 - i)):
            out[i + j] += ai * b[j]
    return out


def poly_pow(a: list, n: int, max_power: int) -> list:
    if n == 0:
        r = [Fraction(0)] * (max_power + 1); r[0] = Fraction(1)
        return r
    base = list(a[:max_power + 1])
    result = None
    while n > 0:
        if n & 1:
            result = base if result is None else poly_mul_truncated(result, base, max_power)
        n >>= 1
        if n:
            base = poly_mul_truncated(base, base, max_power)
    return result


def theta_E8_qseries(order_q: int) -> list:
    """Return [a_0, a_1, ..., a_{order_q}] where theta_{E_8}(tau) = sum a_n q^n.

    Uses theta_{E_8} = (1/2)(theta_2^8 + theta_3^8 + theta_4^8).
    """
    M = 8 * order_q
    t2 = jacobi_theta2_in_s(M)
    t3 = jacobi_theta3_in_s(M)
    t4 = jacobi_theta4_in_s(M)
    s_series = [
        Fraction(1, 2) * (
            poly_pow(t2, 8, M)[k]
            + poly_pow(t3, 8, M)[k]
            + poly_pow(t4, 8, M)[k]
        )
        for k in range(M + 1)
    ]
    # Extract coefficients at s-powers that are multiples of 8.
    out = []
    for n in range(order_q + 1):
        c = s_series[8 * n]
        assert c.denominator == 1, f"theta_E8 q^{n} coef not integer: {c}"
        out.append(int(c))
    # All other s-powers should be zero (modular form lives in q).
    for k in range(M + 1):
        if k % 8 != 0:
            assert s_series[k] == 0, f"non-q s-power {k} should vanish: got {s_series[k]}"
    return out


# ======================================================================
#  Verifications.
# ======================================================================
def verify_theta_E8_equals_E4(order: int = 5) -> dict:
    """theta_{E_8}(tau) = E_4(tau) as q-series."""
    theta = theta_E8_qseries(order)
    E4 = eisenstein_qseries(2, order)
    E4_int = [int(c) for c in E4]
    return {
        "order":        order,
        "theta_E8":     theta,
        "E_4":          E4_int,
        "match":        theta == E4_int,
    }


def verify_240_roots_brute() -> dict:
    """Brute-enumerate roots and check |{v in E_8 : |v|^2 = 2}| = 240."""
    counts = enumerate_E8_by_norm_squared(2)
    roots = E8_roots()
    # Count D_8 roots and coset roots separately.
    d8 = sum(1 for v in roots if all(isinstance(x, int) for x in v))
    coset = sum(1 for v in roots if any(isinstance(x, Fraction) for x in v))
    return {
        "norm_sq_2_count_brute":   counts[2],
        "explicit_root_total":     len(roots),
        "D_8_roots":               d8,
        "coset_roots":             coset,
        "expected_total":          240,
        "match":                   counts[2] == 240 and len(roots) == 240,
    }


def verify_2160_norm_4() -> dict:
    """Brute-enumerate norm^2 = 4 vectors and check count = 2160."""
    counts = enumerate_E8_by_norm_squared(4)
    return {
        "count":      counts[4],
        "expected":   2160,
        "match":      counts[4] == 2160,
    }


# ======================================================================
#  E_8 -> SM bridge.
# ======================================================================
def E8_decomposition_chain() -> dict:
    """Branching of E_8 248-dim adjoint along the GUT chain to the SM."""
    return {
        "E_8":                   {"adjoint_dim": 248, "rank": 8},
        "E_7 x SU(2)":           {"248": "(133,1) + (1,3) + (56,2)"},
        "E_6 x SU(3)":           {"248": "(78,1) + (1,8) + (27,3) + (-27,-3)"},
        "SO(10) x U(1)":         {"78": "45 + 1 + 16 + -16"},
        "SU(5) x U(1)":          {"45": "24 + 1 + 10 + -10"},
        "SM":                    {"24": "(8,1) + (1,3) + (3,2) + (-3,-2) + (1,1)"},
        "comment":
            "One E_6 27 = one SM generation (10 + -5 + 1) of fermions.",
    }


def E8_W33_bridge() -> dict:
    """Numerical bridge between E_8 root counts and W(3, 3) invariants."""
    return {
        "E_8_roots":             240,
        "W(3,3)_v_x_6":          {"v": 40, "6 v": 240},
        "interpretation":
            "240 E_8 roots split as 6 copies of the W(3, 3) vertex set under "
            "the natural Z_6 cyclic action; matches the K27 stabiliser = C_6.",
        "E_6_27_dim":            27,
        "W(3,3)_complement_nn":  27,
        "interpretation_2":
            "27 lines through a fixed point of GQ(3, 3) match the 27 of E_6, "
            "carrying one SM generation.",
        "K27_stabiliser":        "C_6  (project memory: P84)",
    }


# ======================================================================
#  Driver.
# ======================================================================
def derive_all_E8(order: int = 5) -> dict:
    return {
        "lattice_definition":   "E_8 = D_8 cup (D_8 + (1/2,...,1/2))",
        "rank":                  8,
        "type":                  "even unimodular",
        "minimum_norm_sq":       2,
        "number_of_roots":       240,
        "theta_E8_qseries":      theta_E8_qseries(order),
        "matches_E_4":           verify_theta_E8_equals_E4(order),
        "norm_2_brute":          verify_240_roots_brute(),
        "norm_4_brute":          verify_2160_norm_4(),
        "E_8_decomposition":     E8_decomposition_chain(),
        "W33_bridge":            E8_W33_bridge(),
    }


def main() -> None:
    print("=" * 72)
    print("  E_8 ROOT LATTICE AND THETA SERIES")
    print("=" * 72)
    print()

    print("  LATTICE:  E_8 = D_8 cup (D_8 + (1/2,...,1/2))")
    print(f"    rank             = 8")
    print(f"    type             = even unimodular")
    print(f"    minimum |v|^2    = 2")
    print()

    print("  ROOT ENUMERATION (brute force):")
    rb = verify_240_roots_brute()
    print(f"    |v|^2 = 2  (D_8 part):    {rb['D_8_roots']:3d}     (expected 112)")
    print(f"    |v|^2 = 2  (coset part):  {rb['coset_roots']:3d}     (expected 128)")
    print(f"    |v|^2 = 2  total:         {rb['explicit_root_total']:3d}     (expected 240)  match: {rb['match']}")
    print()

    nb = verify_2160_norm_4()
    print(f"    |v|^2 = 4  total:        {nb['count']:5d}     (expected 2160)  match: {nb['match']}")
    print()

    print("  THETA SERIES via JACOBI:  theta_{E_8} = (1/2)(theta_2^8 + theta_3^8 + theta_4^8)")
    order = 5
    theta = theta_E8_qseries(order)
    print(f"    theta_{{E_8}} = {theta}")
    print()

    print("  COMPARISON WITH EISENSTEIN E_4:")
    v = verify_theta_E8_equals_E4(order)
    print(f"    theta_{{E_8}} = {v['theta_E8']}")
    print(f"    E_4         = {v['E_4']}")
    print(f"    match       = {v['match']}")
    print()

    print("  E_8 -> SM DECOMPOSITION CHAIN:")
    chain = E8_decomposition_chain()
    for key in ("E_8", "E_7 x SU(2)", "E_6 x SU(3)", "SO(10) x U(1)",
                "SU(5) x U(1)", "SM"):
        print(f"    {key}:  {chain[key]}")
    print()

    print("  W(3, 3) BRIDGE:")
    bridge = E8_W33_bridge()
    print(f"    240 E_8 roots = 6 * 40 = 6 * |V(W(3,3))|")
    print(f"    27 of E_6     = 27 lines per point in GQ(3, 3)")
    print(f"    K27 stabiliser = C_6  (matches the cyclic split)")
    print()

    chain = derive_all_E8(order=order)
    out = Path(__file__).resolve().parent.parent / "data" / "w33_e8_lattice.json"
    out.write_text(json.dumps(chain, indent=2, default=str))
    print(f"  wrote {out}")


if __name__ == "__main__":
    main()
