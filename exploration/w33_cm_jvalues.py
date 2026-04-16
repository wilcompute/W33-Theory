"""
CM j-VALUES AND RAMANUJAN CONSTANTS
======================================

The j-invariant at complex-multiplication points gives ALGEBRAIC INTEGERS
(and cubes of integers when the imaginary quadratic field has class
number 1).

THE HEEGNER NUMBERS.

The imaginary quadratic fields  Q(sqrt(-d))  with class number 1 are
exactly those for which  d  belongs to

    {1, 2, 3, 7, 11, 19, 43, 67, 163}.

For each such d (with d > 2), the CM point  tau_d = (1 + sqrt(-d))/2
has j-value equal to an integer cube:

    j(i)                         = 1728 = 12^3                (d=1)
    j(sqrt(-2) i)                = 8000 = 20^3                (d=2)
    j((1 + sqrt(-3))/2)          = 0                          (d=3)
    j((1 + sqrt(-7))/2)          = -3375 = -(15)^3            (d=7)
    j((1 + sqrt(-11))/2)         = -32768 = -(32)^3           (d=11)
    j((1 + sqrt(-19))/2)         = -884736 = -(96)^3          (d=19)
    j((1 + sqrt(-43))/2)         = -884736000 = -(960)^3      (d=43)
    j((1 + sqrt(-67))/2)         = -147197952000 = -(5280)^3  (d=67)
    j((1 + sqrt(-163))/2)        = -262537412640768000 = -(640320)^3  (d=163)

RAMANUJAN'S "ALMOST INTEGER".

Since  q = e^{2 pi i tau}  and  tau_d  has imaginary part sqrt(d)/2,
we have  q = -e^{-pi sqrt(d)}.  For large d this is tiny and negative.
The j-series

    j(tau) = 1/q + 744 + 196884 q + ...

gives  j(tau_d) approx -e^{pi sqrt(d)} + 744  for large d, so

    e^{pi sqrt(d)}  approx  -j(tau_d) + 744  =  |integer cube| + 744.

For d = 163 this gives the famous Ramanujan "almost integer":

    e^{pi sqrt(163)}  =  640320^3 + 744 - 196884 e^{-pi sqrt(163)} + ...
                     approx  262537412640768744  to 12 decimals.

BRIDGE TO W(3, 3).

    k = 12 = valency of W(3,3)
    j(i) = 1728 = 12^3 = k^3
    j-constant 744 = j(tau_d) + e^{pi sqrt(d)} + tiny  (at Heegner points)
    The "specialness" of k = 12 shows up as the natural value of j at tau = i.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path


# ======================================================================
#  Heegner numbers and their j-values.
# ======================================================================
HEEGNER_J_VALUES = {
    1:  (12, 1728),                    # j(i) = 12^3
    2:  (20, 8000),                    # j(sqrt(-2)*i) = 20^3
    3:  (0, 0),                        # j((1+sqrt(-3))/2) = 0
    7:  (-15, -3375),                   # -(15)^3
    11: (-32, -32768),                  # -(32)^3
    19: (-96, -884736),                 # -(96)^3
    43: (-960, -884736000),             # -(960)^3
    67: (-5280, -147197952000),         # -(5280)^3
    163: (-640320, -262537412640768000),  # -(640320)^3
}


def verify_j_values_are_cubes() -> dict:
    """Each Heegner j-value is the cube of an integer."""
    results = {}
    for d, (root, j_val) in HEEGNER_J_VALUES.items():
        cube = root ** 3
        results[d] = {
            "d":           d,
            "cube_root":   root,
            "cube":        cube,
            "j_value":     j_val,
            "match":       cube == j_val,
        }
    return results


# ======================================================================
#  j(i) = 1728 = 12^3 = k^3.
# ======================================================================
def j_of_i_equals_k_cubed(k: int = 12) -> dict:
    """The base j-value at tau = i is exactly k^3 = 1728."""
    j_i = HEEGNER_J_VALUES[1][1]     # 1728
    return {
        "j(i)":         j_i,
        "k":            k,
        "k^3":          k ** 3,
        "match":        j_i == k ** 3,
        "meaning":      "j(i) is the normalization constant for Delta",
        "delta_norm":   "Delta = (E_4^3 - E_6^2) / 1728",
    }


# ======================================================================
#  Ramanujan "almost integer":  e^{pi sqrt(d)} approx |j(tau_d)| + 744.
# ======================================================================
def ramanujan_almost_integer(d: int, precision_digits: int = 40) -> dict:
    """For large d, e^{pi sqrt(d)} is exceedingly close to -j(tau_d) + 744.

    Uses mpmath for arbitrary-precision arithmetic -- float64 breaks at d=163.
    """
    import mpmath
    mpmath.mp.dps = precision_digits

    _root, j_val = HEEGNER_J_VALUES[d]
    predicted = -j_val + 744
    actual = mpmath.exp(mpmath.pi * mpmath.sqrt(d))
    diff = actual - predicted
    # When d is large enough, diff ~ -196884 * e^{-pi sqrt(d)}
    correction = -196884 * mpmath.exp(-mpmath.pi * mpmath.sqrt(d))

    return {
        "d":                 d,
        "j(tau_d)":          j_val,
        "predicted_integer": predicted,
        "e^{pi*sqrt(d)}":    mpmath.nstr(actual, 30),
        "difference":        mpmath.nstr(diff, 15),
        "first_order_correction":  mpmath.nstr(correction, 15),
        "|diff - correction|":     mpmath.nstr(abs(diff - correction), 15),
        "_diff_float":       float(diff),
        "_corr_match":       abs(diff - correction) < abs(correction) * 1e-6 + mpmath.mpf(1e-20),
    }


# ======================================================================
#  The d = 163 "Ramanujan constant".
# ======================================================================
def the_ramanujan_constant() -> dict:
    """e^{pi sqrt(163)} ~ 262537412640768744 to 12 decimal places."""
    return ramanujan_almost_integer(163)


# ======================================================================
#  The j-values all lie in Z + Z*sqrt(d) / 2, but for class number 1 are in Z.
# ======================================================================
def heegner_cube_roots() -> dict:
    """The cube roots {-640320, -5280, -960, -96, -32, -15, 0, 12, 20} and
    their connection to k.  Notice 12 = k and 20 = k + 8."""
    cubes = {d: root for d, (root, _) in HEEGNER_J_VALUES.items()}
    return {
        "cube_roots":          cubes,
        "j(i)_root":           cubes[1],
        "j(i)_is_k":           cubes[1] == 12,
        "j(sqrt(-2)*i)_root":  cubes[2],
        "20 = k + 8":          cubes[2] == 12 + 8,
        "k + rank_E8":         12 + 8 == 20,
    }


# ======================================================================
#  Driver.
# ======================================================================
def derive_all_cm_jvalues() -> dict:
    cubes = verify_j_values_are_cubes()
    j_of_i = j_of_i_equals_k_cubed()
    ram = the_ramanujan_constant()
    roots = heegner_cube_roots()

    # Pick a few d to verify almost-integer property
    almost_ints = {
        d: ramanujan_almost_integer(d)
        for d in (19, 43, 67, 163)
    }

    return {
        "heegner_j_cubes":    cubes,
        "j_of_i_is_k_cubed":  j_of_i,
        "ramanujan_163":      ram,
        "heegner_cube_roots": roots,
        "almost_integers":    almost_ints,
        "summary_chain": {
            "all_heegner_j_are_cubes": all(r["match"] for r in cubes.values()),
            "j(i)_equals_12_cubed":    j_of_i["match"],
            "1728_is_k_cubed":         j_of_i["k^3"] == 1728,
            "j(sqrt(-2)*i)_is_(k+8)^3": roots["20 = k + 8"],
        },
    }


def main() -> None:
    print("=" * 72)
    print("  CM j-VALUES AND RAMANUJAN CONSTANTS")
    print("=" * 72)
    print()

    print("  HEEGNER NUMBERS AND j-VALUES (all cubes):")
    for d, r in verify_j_values_are_cubes().items():
        print(f"    d={d:>3d}:  j(tau_d) = {r['j_value']:>22d}  =  ({r['cube_root']:>7d})^3"
              f"  match={r['match']}")
    print()

    j_i = j_of_i_equals_k_cubed()
    print(f"  j(i) = {j_i['j(i)']} = {j_i['k']}^3 = k^3  (with k = 12 = W(3,3) valency)")
    print()

    print("  RAMANUJAN 'ALMOST INTEGER' e^{pi sqrt(d)}:")
    for d in (19, 43, 67, 163):
        r = ramanujan_almost_integer(d)
        print(f"    d={d:>3d}:  |j| + 744 = {r['predicted_integer']:>25d}")
        print(f"            e^{{pi sqrt(d)}} = {r['e^{pi*sqrt(d)}']}")
        print(f"            difference     = {r['difference']}")
        print(f"            |diff - corr| = {r['|diff - correction|']}")
    print()

    roots = heegner_cube_roots()
    print(f"  j(i) cube root = 12 = k:  {roots['j(i)_is_k']}")
    print(f"  j(sqrt(-2)*i) cube root = 20 = k + 8 (= k + rank(E_8)):  {roots['20 = k + 8']}")
    print()

    chain = derive_all_cm_jvalues()
    print("  SUMMARY CHAIN:")
    for key, val in chain["summary_chain"].items():
        print(f"    {key}: {val}")
    print()

    out = Path(__file__).resolve().parent.parent / "data" / "w33_cm_jvalues.json"
    out.write_text(json.dumps(chain, indent=2, default=str))
    print(f"  wrote {out}")


if __name__ == "__main__":
    main()
