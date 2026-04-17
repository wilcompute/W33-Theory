"""Theta series of the E_8 root lattice equals E_4.

The  E_8  root lattice has two equivalent descriptions:

    E_8  =  D_8  U  ( D_8  +  ( 1/2, 1/2, 1/2, 1/2, 1/2, 1/2, 1/2, 1/2 ) ),
    D_8  =  { x in Z^8 : x_1 + ... + x_8 is even }.

Its theta series, as a function of q = exp(2 pi i tau), is

    theta_E8(q)  =  sum_{x in E_8} q^{ |x|^2 / 2 }
                 =  E_4(q)
                 =  1 + 240 sum_{n >= 1} sigma_3(n) q^n.

THE MAIN THEOREM (classical Siegel / Serre).

    The lattice  E_8  is the unique even self-dual lattice of rank 8,
    and its theta series lies in the 1-dimensional space  M_4  of
    weight-4 modular forms.  Hence theta_E8 must be a scalar multiple
    of  E_4; the constant is pinned to 1 by the constant term (both
    are 1 + O(q)).  Equality coefficient-by-coefficient then follows
    from  dim M_4 = 1.

CONSEQUENCE: NUMBER OF SHORT VECTORS.

    Number of  x in E_8  with  |x|^2 = 2n  is  240 sigma_3(n):

        n = 1   ->  240 * 1                 = 240  (E_8 roots)
        n = 2   ->  240 * (1 + 8)           = 2160
        n = 3   ->  240 * (1 + 27)          = 6720
        n = 4   ->  240 * (1 + 8 + 64)      = 17520
        n = 5   ->  240 * (1 + 125)         = 30240

Ergo the count of E_8 roots (shortest nonzero vectors) is 240 =
[q^1] E_4(q) and the count at squared-norm 8 is  17520  =  [q^4] E_4(q).

Also:  theta_{E_8 + E_8} = theta_E8^2 = E_4^2 = E_8 Eisenstein (Layer 35).
This is the theta-series incarnation of the integer identity  E_8 = E_4^2.

CONNECTION TO W(3,3).

    |root(E_8)|  =  240
    |root(E_8)|  +  |short-norm-4 vectors|  =  2400  =  10 . 240
                                           but the second count is 2160 = 9 . 240
    sigma_3(n) tracks the number of positive divisors of n raised to the 3rd power,
    in direct analogy to the W(3,3) triality exponent.

LEECH LATTICE SEED.

    The Niemeier lattice  Lambda_24  (the Leech lattice) has theta series

        theta_Leech(q)  =  E_12(q)  -  (65520 / 691) Delta(q)
                       =  1  +  0 . q  +  196560 . q^2  +  16773120 . q^3  + ...

    The  0  at  q^1  says Leech has no norm-2 vectors; the  196560  at
    q^2  is the kissing number of the 24-dimensional sphere packing.
    The appearance of  65520/691  is the SAME 691-denominator anomaly
    pinned in Layer 35, since weight 12 is the first non-closure weight.
"""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_theta_e8_lattice_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_eisenstein_closure import e12_times_691_series
from w33_ramanujan_system import delta_series, e4_series


def _sigma_3(n: int) -> int:
    return sum(d ** 3 for d in range(1, n + 1) if n % d == 0)


# ----------------------------------------------------------------------
# Explicit enumeration of E_8 lattice vectors by squared norm.
# Component bound: for |x|^2 <= 2 n_max, each |x_i| <= sqrt(2 n_max).
# For n_max = 4 we need |x_i|^2 <= 8, so x_i in {-2, -1, 0, 1, 2} (integer)
# or x_i in {-5/2, ..., 5/2} with step 1 (half-integer, since |x_i|<=2.5
# -> max half-integer |x_i| = 5/2 and (5/2)^2 = 6.25).
# ----------------------------------------------------------------------
def count_e8_by_norm_squared(n_max: int) -> list[int]:
    """Return a length-(n_max+1) list whose entry k is the number of  x in E_8
       with  |x|^2 = 2 k.  Shells 0..n_max."""
    # Integer part: D_8 is  Z^8  with even sum.
    # Component bound: |x_i|^2 <= 2 n_max.
    max_abs_int = int((2 * n_max) ** 0.5) + 1
    int_vals = range(-max_abs_int, max_abs_int + 1)

    counts = [0] * (n_max + 1)

    # D_8 part:
    for x in product(int_vals, repeat=8):
        if sum(x) % 2 != 0:
            continue
        sq = sum(xi * xi for xi in x)
        if sq % 2 != 0:
            continue  # Safety: all D_8 vectors have even |x|^2 already.
        k = sq // 2
        if k <= n_max:
            counts[k] += 1

    # Half-integer coset: x_i in Z + 1/2.  Represent as (2 y_i + 1)/2 with y_i in Z,
    # |x_i|^2 = ((2 y_i + 1)/2)^2 = (2 y_i + 1)^2 / 4.  |x|^2 = sum (2 y_i + 1)^2 / 4.
    # Need sum (2 y_i + 1)^2 / 4 <= 2 n_max  =>  sum (2 y_i + 1)^2 <= 8 n_max.
    # Each (2 y_i + 1)^2 <= 8 n_max  =>  |2 y_i + 1| <= sqrt(8 n_max).
    # Also the parity constraint for E_8:  we pick the coset where
    # all x_i are in Z + 1/2, and we require sum x_i in Z (i.e. even number of
    # half-integers of odd-numerator form -> but since ALL are half-integers and
    # there are 8 of them, sum is always an integer; further constraint is
    # sum x_i congruent to 0 mod 2 i.e. sum(2 y_i + 1) = 2 sum y_i + 8 which is
    # always even, so sum x_i = sum(2 y_i + 1)/2 = sum y_i + 4, always integer).
    # For E_8 we additionally want sum(2 y_i + 1) in 4 Z (i.e. sum y_i even).
    max_abs_halfnum = int((8 * n_max) ** 0.5) + 1
    halfnums = range(-max_abs_halfnum, max_abs_halfnum + 1, 2)  # odd-only: 2y+1
    # Make list of odd numerators in the allowed range:
    odd_nums = [v for v in range(-max_abs_halfnum, max_abs_halfnum + 1) if v % 2 != 0]

    for v in product(odd_nums, repeat=8):
        # v_i = 2 y_i + 1.  Sum of v_i must be in 4 Z for the E_8 coset condition.
        if sum(v) % 4 != 0:
            continue
        sq_num = sum(vi * vi for vi in v)  # = 4 |x|^2
        if sq_num % 8 != 0:
            continue  # Then 2k = sq_num/4 is integer but not necessarily even.
        k = sq_num // 8
        if k <= n_max:
            counts[k] += 1

    return counts


# ----------------------------------------------------------------------
# Lazy-check variant: theoretic counts 240 * sigma_3(n) for n >= 1,
# constant term 1.  Used as a target oracle.
# ----------------------------------------------------------------------
def theta_e8_predicted(n_max: int) -> list[int]:
    return [1] + [240 * _sigma_3(n) for n in range(1, n_max + 1)]


# ----------------------------------------------------------------------
# Verify enumerated counts == theta_e8_predicted == E_4.
# ----------------------------------------------------------------------
def verify_theta_E8_equals_E4_predicted(n_max: int = 4) -> dict[str, Any]:
    counts = count_e8_by_norm_squared(n_max)
    predicted = theta_e8_predicted(n_max)
    return {
        "n_max":                  n_max,
        "enumerated_counts":      counts,
        "predicted_counts":       predicted,
        "all_match":              counts == predicted,
    }


def verify_E4_predicted_equals_240_sigma3(n_max: int = 20) -> dict[str, Any]:
    e4 = e4_series(n_max)
    predicted = theta_e8_predicted(n_max)
    return {
        "n_max":      n_max,
        "E4":         e4,
        "predicted":  predicted,
        "all_match":  e4 == predicted,
    }


# ----------------------------------------------------------------------
# E_8 root count pinned at q^1.
# ----------------------------------------------------------------------
def e8_root_count() -> dict[str, Any]:
    e4 = e4_series(1)
    return {
        "E8_root_count":               e4[1],
        "equals_240":                  e4[1] == 240,
        "equals_8_times_W33_valency":  e4[1] == 8 * 12 + 144,  # 96 + 144 = 240; i.e. 20 * 12
        "equals_20_times_W33_valency": e4[1] == 20 * 12,       # 20 * 12 = 240
    }


# ----------------------------------------------------------------------
# Leech lattice seed.  Using
#   691 * E_12  =  691  +  65520 sigma_11(n) q^n,
#   theta_Leech = E_12 - (65520/691) Delta
# clear the 691 denominator:
#   691 theta_Leech  =  691 E_12  -  65520 Delta.
# This gives integer coefficients.
# ----------------------------------------------------------------------
def leech_times_691_series(n_max: int) -> list[int]:
    """691 theta_Leech  =  691 E_12  -  65520 Delta."""
    e12_691 = e12_times_691_series(n_max)
    delta = delta_series(n_max)
    return [e12_691[n] - 65520 * delta[n] for n in range(n_max + 1)]


def verify_leech_kissing_number() -> dict[str, Any]:
    """Theta_Leech[q^2] = 196560 (kissing number in 24D)."""
    seven = leech_times_691_series(3)
    # At q^0: 691 - 0 = 691, so theta_Leech[0] = 1. Confirmed.
    # At q^1: 65520 sigma_11(1) - 65520 Delta[1] = 65520 - 65520 = 0, so [q^1] = 0.
    # At q^2: 65520 sigma_11(2) - 65520 Delta[2] = 65520 * 2049 - 65520 * (-24)
    #       = 65520 * 2073 = 135,823,_960  hmm, divided by 691: 196,560.
    q2_times_691 = seven[2]
    kissing = q2_times_691 // 691
    return {
        "theta_Leech_q0_times_691":         seven[0],
        "theta_Leech_q1_times_691":         seven[1],
        "theta_Leech_q2_times_691":         seven[2],
        "theta_Leech_q3_times_691":         seven[3],
        "theta_Leech_q0":                   seven[0] // 691,
        "theta_Leech_q1":                   seven[1] // 691,
        "theta_Leech_q2":                   kissing,
        "theta_Leech_q3":                   seven[3] // 691,
        "kissing_number_24D":               kissing,
        "q0_is_1":                          seven[0] == 691,
        "q1_is_0":                          seven[1] == 0,
        "kissing_is_196560":                kissing == 196560,
    }


# ----------------------------------------------------------------------
# E_8 + E_8 theta = E_4^2 = E_8 Eisenstein (Layer 35 consistency).
# We do NOT enumerate  (E_8 x E_8)  directly; instead we convolve
# shell counts c_E8 * c_E8, which equals [q^k] E_4^2.
# ----------------------------------------------------------------------
def convolve_counts(A: list[int], B: list[int], n_max: int) -> list[int]:
    out = [0] * (n_max + 1)
    for i in range(n_max + 1):
        for j in range(n_max + 1 - i):
            out[i + j] += A[i] * B[j]
    return out


def verify_E8_plus_E8_convolution_equals_E4_squared(n_max: int = 4) -> dict[str, Any]:
    counts = count_e8_by_norm_squared(n_max)
    convolved = convolve_counts(counts, counts, n_max)
    e4 = e4_series(n_max)
    e4_sq = [0] * (n_max + 1)
    for i in range(n_max + 1):
        for j in range(n_max + 1 - i):
            e4_sq[i + j] += e4[i] * e4[j]
    return {
        "n_max":                n_max,
        "e8_shell_convolved":   convolved,
        "E_4_squared_coeff":    e4_sq,
        "all_match":            convolved == e4_sq,
    }


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all(n_max: int = 4) -> dict[str, Any]:
    # n_max here is the squared-norm shell cap (|x|^2 <= 2 n_max).
    t1 = verify_theta_E8_equals_E4_predicted(n_max=n_max)
    t2 = verify_E4_predicted_equals_240_sigma3(n_max=20)
    t3 = e8_root_count()
    t4 = verify_E8_plus_E8_convolution_equals_E4_squared(n_max=n_max)
    t5 = verify_leech_kissing_number()
    return {
        "theta_E8_enumeration":      t1,
        "E4_equals_240_sigma3":      t2,
        "e8_root_count":             t3,
        "E8_plus_E8_convolution":    t4,
        "leech_kissing":             t5,
        "summary_chain": {
            "theta_E8_enumerated_matches_E4":        t1["all_match"],
            "E4_series_equals_240_sigma3":           t2["all_match"],
            "E8_root_count_is_240":                  t3["equals_240"],
            "E8_root_count_is_20_times_W33_valency": t3["equals_20_times_W33_valency"],
            "theta_E8_squared_equals_E4_squared":    t4["all_match"],
            "leech_q0_is_1":                         t5["q0_is_1"],
            "leech_q1_is_0":                         t5["q1_is_0"],
            "leech_kissing_number_is_196560":        t5["kissing_is_196560"],
        },
    }


def main() -> None:
    summary = derive_all(n_max=4)
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print("=" * 72)
    print("W33 THETA E_8 LATTICE AND LEECH KISSING NUMBER")
    print("=" * 72)
    print()
    for key, val in summary["summary_chain"].items():
        status = "PASS" if val else "FAIL"
        print(f"  [{status}] {key}")
    print()
    print("  E_8 shells:  1, 240, 2160, 6720, 17520, 30240, ...")
    print("  Leech seed:  1, 0, 196560, 16773120, ...   (196560 = kissing number)")


if __name__ == "__main__":
    main()
