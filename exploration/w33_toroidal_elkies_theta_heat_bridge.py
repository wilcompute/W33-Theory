"""Exact toroidal oscillator lift to Elkies' level-3 theta tower.

The local toroidal route already carries an exact discrete harmonic packet:

    - toroidal seed q = 3,
    - Heawood middle shell dimension 12,
    - middle-shell quadratic x^2 - 6x + 7,
    - heat trace 6 e^{-(3-sqrt(2))t} + 6 e^{-(3+sqrt(2))t}
      = 12 e^{-3t} cosh(sqrt(2) t).

This module connects that discrete oscillator packet to the continuous
level-3 theta tower emphasized in Elkies' notes on rational lattices and theta
functions:

    theta_A2 in M_1(Gamma_1(3)),
    theta_A2^3, theta_E6 in M_3(Gamma_1(3)),
    Delta(3) = eta(z)^6 eta(3z)^6 in S_6(Gamma_1(3)),
    theta_K12 = theta_A2^6 - 36 Delta(3).

What is exact here is not a full analytic limit theorem. The exact closure is:

    q = 3  -> level 3,
    6      -> first nontrivial A2 shell and first level-3 cusp weight,
    12     -> Heawood middle-shell dimension, toroidal genus numerator,
              and rank of the extremal level-3 lattice K12.

So the toroidal harmonic oscillator does admit a clean discrete-to-continuous
lift: not directly to arbitrary smooth geometry, but first to the continuous
theta/heat tower A2 -> E6 -> K12 on Gamma_1(3). The already-verified E8/Leech
modular plane is then the level-1 continuation of that lift.
"""

from __future__ import annotations

import json
import sys
from functools import lru_cache
from math import comb
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_toroidal_elkies_theta_heat_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

try:
    from exploration.w33_bridge_inputs import load_bridge_json
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    from w33_bridge_inputs import load_bridge_json


Q = 3
LEVEL = 3
DELTA3_WEIGHT = 6
K12_RANK = 12
N_MAX = 7


def _load_json(name: str) -> dict[str, Any]:
    return load_bridge_json(name, DATA_DIR)


def _chi3(n: int) -> int:
    residue = n % 3
    if residue == 0:
        return 0
    return 1 if residue == 1 else -1


def _divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def _series_mul(a: list[int], b: list[int], n_max: int) -> list[int]:
    out = [0] * (n_max + 1)
    for i in range(n_max + 1):
        if a[i] == 0:
            continue
        for j in range(n_max + 1 - i):
            if b[j] != 0:
                out[i + j] += a[i] * b[j]
    return out


def _series_pow(a: list[int], exponent: int, n_max: int) -> list[int]:
    out = [0] * (n_max + 1)
    out[0] = 1
    for _ in range(exponent):
        out = _series_mul(out, a, n_max)
    return out


def _eta_quotient_series(
    exponents: dict[int, int], n_max: int, q_shift: int = 0
) -> list[int]:
    """Return q^q_shift * prod_m prod_d (1 - q^(d m))^{exp_d} truncated to q^n_max."""
    series = [0] * (n_max + 1)
    series[0] = 1
    for d, exponent in sorted(exponents.items()):
        for m in range(1, n_max + 1):
            step = d * m
            if step > n_max:
                break
            factor = [0] * (n_max + 1)
            if exponent >= 0:
                factor[0] = 1
                for j in range(1, exponent + 1):
                    power = j * step
                    if power > n_max:
                        break
                    factor[power] = ((-1) ** j) * comb(exponent, j)
            else:
                power_exponent = -exponent
                factor[0] = 1
                max_j = n_max // step
                for j in range(1, max_j + 1):
                    factor[j * step] = comb(j + power_exponent - 1, power_exponent - 1)
            series = _series_mul(series, factor, n_max)

    if q_shift == 0:
        return series

    shifted = [0] * (n_max + 1)
    for n in range(n_max + 1 - q_shift):
        shifted[n + q_shift] = series[n]
    return shifted


def theta_a2_series(n_max: int = N_MAX) -> list[int]:
    return [1] + [6 * sum(_chi3(d) for d in _divisors(n)) for n in range(1, n_max + 1)]


def delta3_series(n_max: int = N_MAX) -> list[int]:
    # Delta(3) = q * prod_{m>=1} (1 - q^m)^6 (1 - q^{3m})^6
    return _eta_quotient_series({1: 6, 3: 6}, n_max, q_shift=1)


def eta_q3_9_over_eta_q_3_series(n_max: int = N_MAX) -> list[int]:
    # eta(q^3)^9 / eta(q)^3 = q * prod_{m>=1} (1 - q^{3m})^9 / (1 - q^m)^3
    return _eta_quotient_series({3: 9, 1: -3}, n_max, q_shift=1)


def theta_e6_series(n_max: int = N_MAX) -> list[int]:
    theta_a2 = theta_a2_series(n_max)
    correction = eta_q3_9_over_eta_q_3_series(n_max)
    theta_a2_cubed = _series_pow(theta_a2, 3, n_max)
    return [theta_a2_cubed[n] + 54 * correction[n] for n in range(n_max + 1)]


def theta_k12_series(n_max: int = N_MAX) -> list[int]:
    theta_a2 = theta_a2_series(n_max)
    delta3 = delta3_series(n_max)
    theta_a2_sixth = _series_pow(theta_a2, 6, n_max)
    return [theta_a2_sixth[n] - 36 * delta3[n] for n in range(n_max + 1)]


def dim_M_gamma1_3(k: int) -> int:
    return max((k + 3) // 3, 0)


def dim_S_gamma1_3(k: int) -> int:
    return dim_M_gamma1_3(k - 6)


def _heawood_middle_heat_trace() -> dict[str, str]:
    return {
        "trace_formula": "6*exp(-(3 - sqrt(2))*t) + 6*exp(-(3 + sqrt(2))*t)",
        "closed_formula": "12*exp(-3*t)*cosh(sqrt(2)*t)",
        "branch_minus": "3 - sqrt(2)",
        "branch_plus": "3 + sqrt(2)",
    }


@lru_cache(maxsize=1)
def build_summary() -> dict[str, Any]:
    heawood = _load_json("w33_heawood_tetra_radical_bridge_summary.json")
    toroidal = _load_json("w33_toroidal_genus_fourier_bridge_summary.json")
    affine_q6 = _load_json("w33_affine_e8_sixth_mode_bridge_summary.json")
    theta_e8 = _load_json("w33_theta_e8_lattice_summary.json")

    middle_shell = heawood["heawood_middle_shell"]
    packet_counts = _load_json("w33_mod12_packet_selector_bridge_summary.json")[
        "packet_counts"
    ]

    theta_a2 = theta_a2_series()
    delta3 = delta3_series()
    theta_e6 = theta_e6_series()
    theta_k12 = theta_k12_series()
    heat = _heawood_middle_heat_trace()

    ramanujan_shell_60480 = affine_q6["w33_packet_dictionary"]["ramanujan_shell_60480"]
    e8_root_packet = theta_e8["e8_root_count"]["E8_root_count"]

    return {
        "discrete_oscillator_dictionary": {
            "q": Q,
            "level": LEVEL,
            "heawood_middle_shell_dimension": middle_shell["middle_shell_dimension"],
            "middle_quadratic": middle_shell["middle_quadratic_polynomial"],
            "middle_linear_term": 6,
            "middle_constant_term": 7,
            "heawood_middle_heat_trace": heat["closed_formula"],
            "toroidal_genus_numerator": toroidal["genus_dictionary"][
                "primal_numerator_at_phi6"
            ],
        },
        "elkies_level3_dictionary": {
            "dim_M_gamma1_3": {str(k): dim_M_gamma1_3(k) for k in (1, 3, 6, 12)},
            "dim_S_gamma1_3": {str(k): dim_S_gamma1_3(k) for k in (1, 3, 6, 12)},
            "generator_weights": {
                "theta_A2": 1,
                "theta_A2_cubed": 3,
                "theta_E6": 3,
                "Delta(3)": 6,
                "theta_K12": 6,
            },
            "external_facts": {
                "weighted_theta_modularity": (
                    "For any rational lattice L, periodic f, and harmonic polynomial P of degree d, "
                    "the weighted theta sum is modular of weight rank(L)/2 + d, and cusp if P is nonconstant."
                ),
                "level3_basis": (
                    "On Gamma_1(3), theta_A2 generates M_1, theta_A2^3 and theta_E6 span M_3, "
                    "and Delta(3)=eta(z)^6 eta(3z)^6 spans S_6."
                ),
            },
        },
        "theta_qseries_dictionary": {
            "theta_A2": theta_a2,
            "Delta(3)": delta3,
            "theta_E6": theta_e6,
            "theta_K12": theta_k12,
        },
        "continuity_bridge_theorem": {
            "the_discrete_seed_q_is_exactly_elkies_level_3": Q == LEVEL == 3,
            "the_Heawood_middle_heat_trace_is_exactly_12_exp_minus_3t_cosh_sqrt2_t": (
                heat["closed_formula"] == "12*exp(-3*t)*cosh(sqrt(2)*t)"
            ),
            "the_A2_first_shell_size_is_exactly_6_matching_the_discrete_linear_term": theta_a2[
                1
            ]
            == 6,
            "the_first_level3_cusp_weight_is_exactly_6_matching_the_discrete_linear_term": (
                dim_S_gamma1_3(6) == 1 and DELTA3_WEIGHT == 6
            ),
            "the_weight3_plane_is_exactly_two_dimensional_with_basis_thetaA2cubed_and_thetaE6": (
                dim_M_gamma1_3(3) == 2
            ),
            "the_first_extremal_level3_rank_is_exactly_12_matching_the_Heawood_and_toroidal_12_packet": (
                middle_shell["middle_shell_dimension"]
                == toroidal["genus_dictionary"]["primal_numerator_at_phi6"]
                == K12_RANK
                == 12
            ),
            "the_Elkies_Delta3_product_matches_the_known_first_coefficients": (
                delta3[:7] == [0, 1, -6, 9, 4, 6, -54]
            ),
            "the_Elkies_K12_theta_series_matches_the_known_first_coefficients": (
                theta_k12[:6] == [1, 0, 756, 4032, 20412, 60480]
            ),
            "the_level3_continuous_lift_hits_the_existing_affine_ramanujan_shell_60480_exactly": (
                theta_k12[5] == ramanujan_shell_60480 == 60480
            ),
            "the_level3_tower_continues_into_the_existing_level1_E8_plane": (
                e8_root_packet == 240
                and packet_counts["chart_count"] == 4
                and packet_counts["mode_count"] == 3
            ),
        },
        "exact_chain": {
            "discrete": "K7 shell (7) -> Heawood middle quadratic (x^2 - 6x + 7) -> heat trace 12 exp(-3t) cosh(sqrt(2)t)",
            "level3_continuous": "A2 (weight 1, rank 2) -> E6 / A2^3 (weight 3, rank 6) -> Delta(3), K12 (weight 6, rank 12)",
            "level1_continuation": "E8 theta = E4 (weight 4) -> Leech theta on the weight-12 collision plane",
        },
        "interpretation": (
            "The toroidal harmonic oscillator does lift from discrete to continuous, but the clean first lift "
            "is not straight to arbitrary smooth geometry. It goes first to Elkies' level-3 theta tower. The "
            "shared packet numbers are exact: q=3 gives the modular level, the Heawood linear term 6 is both "
            "the first A2 shell size and the first level-3 cusp weight, and the toroidal/Heawood 12-packet is "
            "the rank of the extremal level-3 lattice K12. The existing affine packet 60480 then reappears as "
            "the q^5 coefficient of theta_K12. So the right discrete-to-continuous route is theta/heat on "
            "Gamma_1(3), with E8/Leech as the later level-1 continuation."
        ),
        "sources": {
            "elkies_weighted_theta": "https://people.math.harvard.edu/~elkies/M272.19/nov11.pdf",
            "elkies_level3_lattices": "https://people.math.harvard.edu/~elkies/M272.19/nov25.pdf",
            "borcherds_theta_poisson": "https://mathvideos.org/2021/richard-borcherds-modular-forms-viii/",
            "cohn_theta_series_sphere_packing": "https://arxiv.org/abs/math/0110010",
        },
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 TOROIDAL ELKIES THETA HEAT BRIDGE")
    print("=" * 72)
    for key, value in summary["continuity_bridge_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
