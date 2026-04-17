r"""The modular-form dimension formula is 12-periodic.

For  SL(2, Z), let  M_k  be the complex vector space of holomorphic modular
forms of weight  k, and  S_k  the subspace of cusp forms.

DIMENSION FORMULA (classical, proved via Riemann--Roch on X(1) = P^1).

    dim M_k  =  0                         if k < 0 or k is odd,
    dim M_0  =  1                         (constants),
    dim M_2  =  0                         (no holomorphic weight-2 forms),
    dim M_k  =  floor(k / 12) + 1         if k even, k >= 4, k mod 12 != 2,
    dim M_k  =  floor(k / 12)             if k even, k mod 12 == 2.

    dim S_k  =  dim M_k  -  1             if k >= 4 even,
                                          (the -1 kills the Eisenstein direction).

The formula is 12-PERIODIC: dim M_{k+12} = dim M_k + 1 for all even k >= 4.
Multiplication by  Delta  is the isomorphism

    M_{k-12}  ---->  S_k,     f  ---->  f . Delta.

LOW-WEIGHT TABLE.

    k :    0  2  4  6  8 10 12 14 16 18 20 22 24 26 28 ...
    M_k:   1  0  1  1  1  1  2  1  2  2  2  2  3  2  3 ...
    S_k:   0  0  0  0  0  0  1  0  1  1  1  1  2  1  2 ...
    gens:       E_4 E_6 E_4^2 E_4 E_6  E_4^3/ E_4^2 E_6 (...)
                                       Delta

CONSEQUENCES PINNED BY THIS LAYER.

    1. (W_TWO_EXCEPTION)  dim M_2 = 0  =>  E_2 is quasi-modular, not modular
       (Layer 30 anomaly).
    2. (UNIQUE_CUSP_FORM) dim S_12 = 1, spanned by Delta => every weight-12
       cusp form is a scalar multiple of Delta (used in the Rankin-Cohen
       computations, Layer 34, and the 691 pin, Layer 35).
    3. (MONOMIAL_WEIGHTS)  dim M_k = 1 for k in {4, 6, 8, 10, 14} =>
       E_8 = E_4^2, E_10 = E_4 E_6, E_14 = E_4^2 E_6 (Layer 35).
    4. (DELTA_ISOMORPHISM) dim M_{k-12} = dim S_k forces  S_k = Delta * M_{k-12}.
    5. (691_ANOMALY_ROOT)  Weight 12 is the FIRST weight where dim M_k = 2,
       so E_12 requires a rational linear combination of E_4^3 and Delta,
       producing the 691 denominator of Layer 35.

PROOF SKETCH.

On the compactified modular curve  X(1) = bar H / SL(2, Z) \\cup { i infty },
holomorphic modular forms of weight k correspond to global sections of a
line bundle whose degree is  k/12, minus contributions from the two elliptic
points  i  (order 2) and  rho = e^{2 pi i / 6}  (order 3).  Riemann-Roch gives

    dim M_k  =  floor(k/4) + floor(k/3) - floor(k/2) + 1 (for k >= 0, k even)
             =  floor(k/12) + epsilon_k

where  epsilon_k  is 0 if k mod 12 = 2, else 1.

The periodicity is the "12-period" of the SL(2, Z) action, directly
tied to the W(3,3) valency:

    12  =  k_W33  =  weight of Delta  =  order of [D_4, D_4, D_4] orbit on 27,
    12  =  order of j meromorphic automorphism cycle,
    12  =  the universal anomaly period.
"""

from __future__ import annotations

import json
from math import floor
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_modular_dimension_formula_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))


# ----------------------------------------------------------------------
# Dimension formulas.
# ----------------------------------------------------------------------
def dim_M(k: int) -> int:
    """dim M_k for SL(2, Z)."""
    if k < 0:
        return 0
    if k % 2 != 0:
        return 0
    if k == 0:
        return 1
    if k == 2:
        return 0
    if k % 12 == 2:
        return k // 12
    return k // 12 + 1


def dim_S(k: int) -> int:
    """dim S_k.  S_k = M_k minus the 1-dim Eisenstein subspace (for k >= 4 even)."""
    if k < 4 or k % 2 != 0:
        return 0
    return max(dim_M(k) - 1, 0)


# ----------------------------------------------------------------------
# Closed-form Riemann-Roch check.
# ----------------------------------------------------------------------
def dim_M_via_RR(k: int) -> int:
    """Riemann-Roch check for k even, k >= 0:
         dim M_k = floor(k/4) + floor(k/3) - floor(k/2) + 1
    Note: the elliptic-point/cusp contribution summations yield this
    identity after simplification."""
    if k < 0 or k % 2 != 0:
        return 0
    # This closed form holds for k even, k >= 4 actually; k = 0 gives 1 which
    # agrees with the formula.  k = 2 is the lone exception:
    # floor(2/4) + floor(2/3) - floor(2/2) + 1 = 0 + 0 - 1 + 1 = 0.
    # So it DOES work even at k = 2.
    return floor(k / 4) + floor(k / 3) - floor(k / 2) + 1


def verify_dim_M_closed_form_matches_tabulated(k_max: int = 60) -> dict[str, Any]:
    discrepancies = []
    for k in range(0, k_max + 1, 2):
        a = dim_M(k)
        b = dim_M_via_RR(k)
        if a != b:
            discrepancies.append({"k": k, "tabulated": a, "RR": b})
    return {
        "k_max":         k_max,
        "discrepancies": discrepancies,
        "all_match":     discrepancies == [],
    }


# ----------------------------------------------------------------------
# 12-periodicity: dim M_{k+12} = dim M_k + 1 for k even, k >= 4.
# ----------------------------------------------------------------------
def verify_12_periodicity(k_max: int = 120) -> dict[str, Any]:
    discrepancies = []
    for k in range(4, k_max + 1, 2):
        left = dim_M(k + 12)
        right = dim_M(k) + 1
        if left != right:
            discrepancies.append({"k": k, "dim_M_k_plus_12": left, "dim_M_k_plus_1": right})
    return {
        "k_max":         k_max,
        "discrepancies": discrepancies,
        "all_match":     discrepancies == [],
    }


# ----------------------------------------------------------------------
# Delta-multiplication: S_k = Delta * M_{k-12} for k even, k >= 4.
# ----------------------------------------------------------------------
def verify_delta_isomorphism(k_max: int = 120) -> dict[str, Any]:
    discrepancies = []
    for k in range(4, k_max + 1, 2):
        s_k = dim_S(k)
        m_prev = dim_M(k - 12)
        if s_k != m_prev:
            discrepancies.append({"k": k, "dim_S_k": s_k, "dim_M_k_minus_12": m_prev})
    return {
        "k_max":         k_max,
        "discrepancies": discrepancies,
        "all_match":     discrepancies == [],
    }


# ----------------------------------------------------------------------
# Low-weight table check.
# ----------------------------------------------------------------------
def low_weight_table() -> dict[str, Any]:
    weights = list(range(0, 29, 2))
    return {
        "weights":  weights,
        "dim_M_k":  [dim_M(k) for k in weights],
        "dim_S_k":  [dim_S(k) for k in weights],
    }


def verify_low_weight_matches_known() -> dict[str, Any]:
    """Known values for small k: dim M = [1,0,1,1,1,1,2,1,2,2,2,2,3,2,3] for k=0..28."""
    known_M = [1, 0, 1, 1, 1, 1, 2, 1, 2, 2, 2, 2, 3, 2, 3]
    known_S = [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 2, 1, 2]
    computed_M = [dim_M(k) for k in range(0, 29, 2)]
    computed_S = [dim_S(k) for k in range(0, 29, 2)]
    return {
        "known_M":     known_M,
        "computed_M":  computed_M,
        "known_S":     known_S,
        "computed_S":  computed_S,
        "M_matches":   known_M == computed_M,
        "S_matches":   known_S == computed_S,
    }


# ----------------------------------------------------------------------
# Five consequences pinned in previous layers.
# ----------------------------------------------------------------------
def five_consequences() -> dict[str, Any]:
    return {
        "W_TWO_EXCEPTION":       {"dim_M_2": dim_M(2), "is_zero": dim_M(2) == 0},
        "UNIQUE_CUSP_FORM_12":   {"dim_S_12": dim_S(12), "equals_1": dim_S(12) == 1},
        "MONOMIAL_WEIGHTS":      {
            "dim_M_4":  dim_M(4),
            "dim_M_6":  dim_M(6),
            "dim_M_8":  dim_M(8),
            "dim_M_10": dim_M(10),
            "dim_M_14": dim_M(14),
            "all_one":  all(dim_M(k) == 1 for k in (4, 6, 8, 10, 14)),
        },
        "DELTA_ISOMORPHISM_12":  {
            "dim_S_12":              dim_S(12),
            "dim_M_0":               dim_M(0),
            "S_12_is_Delta_times_M0": dim_S(12) == dim_M(0),
        },
        "691_ANOMALY_ROOT":      {
            "first_k_with_dim_M_geq_2": 12,
            "dim_M_12":                 dim_M(12),
            "equals_2":                 dim_M(12) == 2,
            "B_12_numerator":           691,
        },
    }


# ----------------------------------------------------------------------
# The dimension generating function.
#   Sum_k dim(M_k) t^k  =  1 / ((1 - t^4)(1 - t^6))   (as a formal power series in t).
# ----------------------------------------------------------------------
def verify_hilbert_series(k_max: int = 60) -> dict[str, Any]:
    """Compare dim M_k against the coefficient of t^k in 1 / ((1-t^4)(1-t^6))."""
    N = k_max + 1
    # Build (1 - t^4)^(-1) * (1 - t^6)^(-1) by convolution.
    inv_4 = [1 if n % 4 == 0 else 0 for n in range(N)]
    inv_6 = [1 if n % 6 == 0 else 0 for n in range(N)]
    prod = [0] * N
    for i in range(N):
        if inv_4[i] == 0:
            continue
        for j in range(N - i):
            prod[i + j] += inv_4[i] * inv_6[j]
    discrepancies = []
    for k in range(0, N, 2):
        a = dim_M(k)
        b = prod[k]
        if a != b:
            discrepancies.append({"k": k, "dim_M_k": a, "hilbert": b})
    return {
        "k_max":         k_max,
        "discrepancies": discrepancies,
        "all_match":     discrepancies == [],
    }


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    rr = verify_dim_M_closed_form_matches_tabulated(k_max=60)
    per = verify_12_periodicity(k_max=120)
    iso = verify_delta_isomorphism(k_max=120)
    table = low_weight_table()
    known = verify_low_weight_matches_known()
    cons = five_consequences()
    hilb = verify_hilbert_series(k_max=60)
    return {
        "riemann_roch_check":    rr,
        "twelve_periodicity":    per,
        "delta_isomorphism":     iso,
        "low_weight_table":      table,
        "low_weight_known":      known,
        "five_consequences":     cons,
        "hilbert_series":        hilb,
        "summary_chain": {
            "dim_M_closed_form_matches_tabulated":        rr["all_match"],
            "dim_M_is_12_periodic_with_offset_1":         per["all_match"],
            "dim_S_k_equals_dim_M_k_minus_12":            iso["all_match"],
            "low_weight_dim_M_matches_known":             known["M_matches"],
            "low_weight_dim_S_matches_known":             known["S_matches"],
            "W_TWO_EXCEPTION_dim_M_2_is_zero":            cons["W_TWO_EXCEPTION"]["is_zero"],
            "UNIQUE_CUSP_dim_S_12_is_one":                cons["UNIQUE_CUSP_FORM_12"]["equals_1"],
            "MONOMIAL_WEIGHTS_4_6_8_10_14_all_dim_one":   cons["MONOMIAL_WEIGHTS"]["all_one"],
            "first_k_with_dim_M_at_least_2_is_12":        cons["691_ANOMALY_ROOT"]["equals_2"],
            "hilbert_series_matches_1_over_1mt4_1mt6":    hilb["all_match"],
        },
    }


def main() -> None:
    summary = derive_all()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print("=" * 72)
    print("W33 MODULAR-FORM DIMENSION FORMULA (12-PERIODIC)")
    print("=" * 72)
    print()
    for key, val in summary["summary_chain"].items():
        status = "PASS" if val else "FAIL"
        print(f"  [{status}] {key}")
    print()
    table = summary["low_weight_table"]
    print("  k      : " + " ".join(f"{k:3d}" for k in table["weights"]))
    print("  dim M_k: " + " ".join(f"{d:3d}" for d in table["dim_M_k"]))
    print("  dim S_k: " + " ".join(f"{d:3d}" for d in table["dim_S_k"]))


if __name__ == "__main__":
    main()
