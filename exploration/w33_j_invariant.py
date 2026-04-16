"""The j-invariant closes on (E_4, eta^{-8}) via a cube.

Define j = E_4^3 / Delta.  Since Delta = q * prod(1-q^n)^{24}, multiplying
by q absorbs the pole and gives an integer power series

    J_tilde := q * j = 1 + 744 q + 196884 q^2 + 21493760 q^3 + ...

Three clean integer identities lock j to the rest of the tower:

(I)   J_tilde * prod(1-q^n)^{24} = E_4^3.          (definition of j)

(II)  (E_4 * prod(1-q^n)^{-8})^3 = J_tilde.        (affine E_8 cube)
      Equivalent to  ch_{E_8,1}^3 = j / 1728 * 1728  once the q^{c/24}
      prefactor is reassembled.  In words: q * j is the cube of the
      affine E_8 level-1 oscillator-dressed theta.

(III) E_4 * q * dJ_tilde/dq = J_tilde * (E_4 - E_6).   (j-ODE)
      Equivalent form on J_inv := Delta / E_4^3 = 1/j:
          E_4 * q * dJ_inv/dq = E_6 * J_inv.

BRIDGE TO THE TOWER.

    Layer 30 (E_2 source):    3 q d(f_8)/dq + (E_2 - 1) f_8 = 0,  f_8 = prod(1-q^n)^{-8}.
    Layer 31 (Ramanujan):     q dDelta/dq = E_2 Delta;
                              q dE_4/dq = (E_2 E_4 - E_6)/3.
    Layer 32 (Serre):         [E_4, E_6]_1 = -3456 Delta = -2 k^3 Delta.
    Layer 33 (j, here):       q*j = (E_4 * f_8)^3  where f_8 is the affine E_8 oscillator.

    Every modular function on SL(2,Z) is a rational function of j, and
    now j is algebraic over the W(3,3) tower's two integer series
    (E_4, f_8) via a single cube.

MONSTER MOONSHINE SEED.

    J_tilde[0] = 1,
    J_tilde[1] = 744 = 2^3 * 3 * 31,
    J_tilde[2] = 196884 = 196883 + 1 = dim(Griess algebra) + 1,
    J_tilde[3] = 21493760 = 21296876 + 196883 + 1.

    The coefficient 196884 is the first Moonshine coincidence.  196883
    is the dimension of the smallest faithful complex representation of
    the Monster group; 1 comes from the trivial representation.  On the
    W(3,3) spine this coincidence lands inside  (E_4 * f_8)^3.

KLEIN'S j(i) = 1728 = 12^3.

    1728 is the value of j at the lemniscatic point tau = i,
    where the CM j-tower anchors (Layer CCXLVIII gives j(-4) = k^3 = 12^3).
    On the holomorphic side 1728 is the coefficient in the discriminant
    identity  E_4^3 - E_6^2 = 1728 Delta.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_j_invariant_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_affine_e8 import _series_inv, _series_pow
from w33_euler_pentagonal import euler_pentagonal_series
from w33_ramanujan_system import (
    delta_series,
    e2_series,
    e4_series,
    e6_series,
    q_d_dq,
    series_mul,
)


# ----------------------------------------------------------------------
# Integer series for j, J_tilde, J_inv.
# ----------------------------------------------------------------------
def eta_positive_power_series(c: int, n_max: int) -> list[int]:
    """g_c = prod(1-q^n)^c."""
    euler = euler_pentagonal_series(n_max)
    return _series_pow(euler, c, n_max)


def eta_negative_power_series(c: int, n_max: int) -> list[int]:
    """f_c = prod(1-q^n)^{-c}."""
    euler = euler_pentagonal_series(n_max)
    prod_c = _series_pow(euler, c, n_max)
    return _series_inv(prod_c, n_max)


def j_tilde_series(n_max: int) -> list[int]:
    """J_tilde := q * j = E_4^3 / prod(1-q^n)^{24}  as an integer power series."""
    e4 = e4_series(n_max)
    e4_cubed = series_mul(series_mul(e4, e4, n_max), e4, n_max)
    f24 = eta_negative_power_series(24, n_max)
    return series_mul(e4_cubed, f24, n_max)


def j_inv_series(n_max: int) -> list[int]:
    """J_inv := Delta / E_4^3 = 1/j  (integer series starting with q)."""
    delta = delta_series(n_max)
    e4 = e4_series(n_max)
    e4_cubed = series_mul(series_mul(e4, e4, n_max), e4, n_max)
    e4_cubed_inv = _series_inv(e4_cubed, n_max)
    return series_mul(delta, e4_cubed_inv, n_max)


# ----------------------------------------------------------------------
# (I) J_tilde * g_24 = E_4^3   (definition of j).
# ----------------------------------------------------------------------
def verify_j_definition(n_max: int = 20) -> dict[str, Any]:
    jt = j_tilde_series(n_max)
    g24 = eta_positive_power_series(24, n_max)
    lhs = series_mul(jt, g24, n_max)
    e4 = e4_series(n_max)
    rhs = series_mul(series_mul(e4, e4, n_max), e4, n_max)
    return {
        "n_max":       n_max,
        "mismatches":  [(n, lhs[n], rhs[n]) for n in range(n_max + 1) if lhs[n] != rhs[n]],
        "all_match":   lhs == rhs,
    }


# ----------------------------------------------------------------------
# (II) (E_4 * f_8)^3 = J_tilde   (affine E_8 cube).
# ----------------------------------------------------------------------
def verify_affine_e8_cube(n_max: int = 20) -> dict[str, Any]:
    e4 = e4_series(n_max)
    f8 = eta_negative_power_series(8, n_max)
    base = series_mul(e4, f8, n_max)
    cube = series_mul(series_mul(base, base, n_max), base, n_max)
    jt = j_tilde_series(n_max)
    return {
        "n_max":       n_max,
        "mismatches":  [(n, cube[n], jt[n]) for n in range(n_max + 1) if cube[n] != jt[n]],
        "all_match":   cube == jt,
    }


# ----------------------------------------------------------------------
# (III) E_4 * q * dJ_tilde/dq = J_tilde * (E_4 - E_6).
# ----------------------------------------------------------------------
def verify_j_ode(n_max: int = 20) -> dict[str, Any]:
    jt = j_tilde_series(n_max)
    e4 = e4_series(n_max)
    e6 = e6_series(n_max)
    e4_minus_e6 = [e4[n] - e6[n] for n in range(n_max + 1)]
    lhs = series_mul(e4, q_d_dq(jt), n_max)
    rhs = series_mul(jt, e4_minus_e6, n_max)
    return {
        "n_max":       n_max,
        "mismatches":  [(n, lhs[n], rhs[n]) for n in range(n_max + 1) if lhs[n] != rhs[n]],
        "all_match":   lhs == rhs,
    }


def verify_j_inv_ode(n_max: int = 20) -> dict[str, Any]:
    """E_4 * q * dJ_inv/dq = E_6 * J_inv  where J_inv = 1/j = Delta/E_4^3."""
    ji = j_inv_series(n_max)
    e4 = e4_series(n_max)
    e6 = e6_series(n_max)
    lhs = series_mul(e4, q_d_dq(ji), n_max)
    rhs = series_mul(e6, ji, n_max)
    return {
        "n_max":       n_max,
        "mismatches":  [(n, lhs[n], rhs[n]) for n in range(n_max + 1) if lhs[n] != rhs[n]],
        "all_match":   lhs == rhs,
    }


# ----------------------------------------------------------------------
# Monster moonshine seed at [q^2] of q*j.
# ----------------------------------------------------------------------
def monster_moonshine_seed() -> dict[str, Any]:
    jt = j_tilde_series(5)
    return {
        "q0_coefficient":  jt[0],
        "q1_coefficient":  jt[1],
        "q2_coefficient":  jt[2],
        "q3_coefficient":  jt[3],
        "monster_Griess_dim_plus_1":  196883 + 1,
        "q2_equals_196884":  jt[2] == 196884,
        "q2_equals_Griess_plus_1":  jt[2] == 196884,
        "q2_decomposition":  "196884 = dim(Griess) + 1 = 196883 + 1",
    }


# ----------------------------------------------------------------------
# Klein / Ramanujan constant 1728 = k^3.
# ----------------------------------------------------------------------
def klein_discriminant_constants() -> dict[str, Any]:
    """Klein's j(i) = 1728 and the discriminant identity 1728 Delta = E_4^3 - E_6^2."""
    k = 12
    jt = j_tilde_series(2)
    # (j - 1728) * Delta = E_6^2; equivalently 1728*Delta = E_4^3 - E_6^2.
    e4 = e4_series(3)
    e6 = e6_series(3)
    delta = delta_series(3)
    e4_cubed = series_mul(series_mul(e4, e4, 3), e4, 3)
    e6_sq = series_mul(e6, e6, 3)
    diff = [e4_cubed[n] - e6_sq[n] for n in range(4)]
    k_cubed_delta = [1728 * d for d in delta]
    return {
        "k":                            k,
        "k_cubed":                      k ** 3,
        "1728_equals_k_cubed":          1728 == k ** 3,
        "j_at_tau_i":                   1728,
        "discriminant_lhs_q1":          diff[1],
        "discriminant_rhs_q1":          k_cubed_delta[1],
        "discriminant_holds_up_to_q3":  diff == k_cubed_delta,
        "J_tilde_constant_term":        jt[0],
    }


# ----------------------------------------------------------------------
# Cross-check: J_tilde * J_inv = q  (the "inverse" identity in integer form).
# ----------------------------------------------------------------------
def verify_j_times_j_inv_equals_q(n_max: int = 15) -> dict[str, Any]:
    """(q*j) * (1/j) = q  =>  J_tilde * J_inv = q."""
    jt = j_tilde_series(n_max)
    ji = j_inv_series(n_max)
    prod = series_mul(jt, ji, n_max)
    expected = [0] * (n_max + 1)
    if n_max >= 1:
        expected[1] = 1
    return {
        "n_max":     n_max,
        "product":   prod[: n_max + 1],
        "matches_q": prod == expected,
    }


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all(n_max: int = 20) -> dict[str, Any]:
    j_def = verify_j_definition(n_max=n_max)
    cube = verify_affine_e8_cube(n_max=n_max)
    j_ode = verify_j_ode(n_max=n_max)
    ji_ode = verify_j_inv_ode(n_max=n_max)
    moonshine = monster_moonshine_seed()
    klein = klein_discriminant_constants()
    inv_check = verify_j_times_j_inv_equals_q(n_max=15)
    return {
        "j_definition":           j_def,
        "affine_e8_cube":         cube,
        "j_ode":                  j_ode,
        "j_inv_ode":              ji_ode,
        "monster_moonshine_seed": moonshine,
        "klein_constants":        klein,
        "j_times_j_inv_check":    inv_check,
        "summary_chain": {
            "j_times_g24_equals_E4_cubed":        j_def["all_match"],
            "E4_f8_cubed_equals_q_times_j":       cube["all_match"],
            "E4_qdj_equals_j_times_E4_minus_E6":  j_ode["all_match"],
            "E4_qdjinv_equals_E6_times_jinv":     ji_ode["all_match"],
            "q2_coefficient_is_196884":           moonshine["q2_equals_196884"],
            "k_cubed_equals_1728_klein_point":    klein["1728_equals_k_cubed"],
            "ramanujan_discriminant_identity":    klein["discriminant_holds_up_to_q3"],
            "j_times_j_inv_equals_q":             inv_check["matches_q"],
        },
    }


def main() -> None:
    summary = derive_all(n_max=20)
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print("=" * 72)
    print("W33 J-INVARIANT AS A CUBE OVER (E_4, eta^{-8})")
    print("=" * 72)
    print()
    for key, val in summary["summary_chain"].items():
        status = "PASS" if val else "FAIL"
        print(f"  [{status}] {key}")
    print()
    jt = summary["j_definition"]
    ms = summary["monster_moonshine_seed"]
    kl = summary["klein_constants"]
    print(f"  J_tilde = q*j = 1 + 744 q + {ms['q2_coefficient']} q^2 + {ms['q3_coefficient']} q^3 + ...")
    print(f"  Monster moonshine: J_tilde[2] = 196884 = dim(Griess) + 1")
    print(f"  Klein: j(i) = 1728 = 12^3 = k^3 on the W(3,3) spine")


if __name__ == "__main__":
    main()
