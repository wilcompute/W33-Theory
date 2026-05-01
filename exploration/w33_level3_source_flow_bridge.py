"""Exact level-3 source flow behind the toroidal theta lift.

The toroidal/Elkies bridge and the level-3 -> level-1 condensation bridge
closed the static algebra.  This module closes the first genuine dynamics
statement.

On Gamma_1(3), Elkies identifies the weight-2 modular generator as

    E2^(3) := theta_A2^2 = (3 E2(3z) - E2(z)) / 2
           = 1 + sum_{n>=1} (12 sigma_1(n) - 36 sigma_1(n/3)) q^n.

So before condensation to level 1, the toroidal A2 seed already has an honest
continuous weight-2 source. The first coefficient is

    [q] E2^(3) = 12,

which is exactly the Heawood middle-shell dimension and the toroidal genus
numerator.

The first level-3 cusp Delta(3) = eta(z)^6 eta(3z)^6 then evolves by the exact
mixed-source flow

    2 q dDelta(3)/dq = (E2 + E2^(3)) Delta(3).

This is the clean differential bridge:

    - E2^(3) is the honest modular source on Gamma_1(3);
    - E2 is the level-1 quasi-modular source;
    - Delta(3) feels their exact arithmetic mean.

So the anomaly does not exist at the first continuous lift. It appears only
after condensation from the level-3 theta tower to the full level-1 plane.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

try:
    from exploration.w33_bridge_inputs import load_bridge_json
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    from w33_bridge_inputs import load_bridge_json


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_level3_source_flow_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_ramanujan_system import e2_series, q_d_dq, series_mul
from w33_toroidal_elkies_theta_heat_bridge import delta3_series, theta_a2_series

N_MAX = 12


def _sigma1(n: int) -> int:
    return sum(d for d in range(1, n + 1) if n % d == 0)


def e2_level3_series(n_max: int = N_MAX) -> list[int]:
    theta_a2 = theta_a2_series(n_max)
    return series_mul(theta_a2, theta_a2, n_max)


def e2_3z_series(n_max: int = N_MAX) -> list[int]:
    e2 = e2_series(n_max)
    return [e2[n // 3] if n % 3 == 0 else 0 for n in range(n_max + 1)]


def e2_level3_divisor_series(n_max: int = N_MAX) -> list[int]:
    return [
        (
            1
            if n == 0
            else (
                12 * _sigma1(n) - 36 * _sigma1(n // 3)
                if n % 3 == 0
                else 12 * _sigma1(n)
            )
        )
        for n in range(n_max + 1)
    ]


def _load_json(filename: str) -> dict[str, Any]:
    return load_bridge_json(filename, DATA_DIR)


def build_summary(n_max: int = N_MAX) -> dict[str, Any]:
    e2 = e2_series(n_max)
    e2_3 = e2_3z_series(n_max)
    e2_lvl3 = e2_level3_series(n_max)
    e2_lvl3_div = e2_level3_divisor_series(n_max)
    delta3 = delta3_series(n_max)
    qd_delta3 = q_d_dq(delta3)

    e2_lvl3_from_e2 = [(3 * e2_3[n] - e2[n]) // 2 for n in range(n_max + 1)]
    mixed_rhs = series_mul(
        [e2[n] + e2_lvl3[n] for n in range(n_max + 1)], delta3, n_max
    )

    mod12 = _load_json("w33_mod12_packet_selector_bridge_summary.json")
    heawood = _load_json("w33_heawood_tetra_radical_bridge_summary.json")

    middle_shell_dim = heawood["heawood_middle_shell"]["middle_shell_dimension"]
    genus_num = mod12["modulus"]
    cumulative_ladder = [8 * _sigma1(n) for n in range(1, 9)]

    return {
        "level3_source_dictionary": {
            "E2_level3_coefficients": e2_lvl3,
            "E2_level3_from_E2_and_E2_3z": e2_lvl3_from_e2,
            "E2_level3_divisor_formula": e2_lvl3_div,
            "Delta3_coefficients": delta3,
            "E2_coefficients": e2,
            "E2_3z_coefficients": e2_3,
        },
        "level3_source_flow_theorem": {
            "theta_A2_squared_is_exactly_the_level3_weight2_source": e2_lvl3
            == e2_lvl3_div,
            "theta_A2_squared_equals_3E2_3z_minus_E2_over_2_exactly": e2_lvl3
            == e2_lvl3_from_e2,
            "the_first_level3_source_coefficient_is_exactly_12": e2_lvl3[1] == 12,
            "the_first_level3_source_coefficient_matches_the_Heawood_middle_shell_dimension": (
                e2_lvl3[1] == middle_shell_dim == 12
            ),
            "the_first_level3_source_coefficient_matches_the_toroidal_modulus": e2_lvl3[
                1
            ]
            == genus_num
            == 12,
            "the_first_level3_cusp_obeys_the_exact_mixed_source_flow_2qdDelta3_equals_E2_plus_E2level3_times_Delta3": (
                [2 * qd_delta3[n] for n in range(n_max + 1)] == mixed_rhs
            ),
            "the_level1_quasimodular_source_can_be_recovered_as_3E2_3z_minus_2E2level3": (
                e2 == [3 * e2_3[n] - 2 * e2_lvl3[n] for n in range(n_max + 1)]
            ),
            "the_old_post_q11_cumulative_ladder_starts_with_the_level3_source_shell_12_before_the_level1_E2_ladder_8_24_32_56": (
                e2_lvl3[1] == 12 and cumulative_ladder[:4] == [8, 24, 32, 56]
            ),
        },
        "exact_flow_chain": {
            "discrete_seed": "Heawood middle shell: x^2 - 6x + 7 with 12-dimensional middle packet",
            "first_continuous_source": "E2^(3) = theta_A2^2 = (3 E2(3z) - E2(z))/2",
            "first_cusp_flow": "2 q dDelta(3)/dq = (E2 + E2^(3)) Delta(3)",
            "condensed_anomaly": "E2 = 3 E2(3z) - 2 E2^(3)",
        },
        "interpretation": (
            "The first continuous source above the toroidal oscillator is not the level-1 quasi-modular "
            "anomaly E2. It is the honest level-3 modular form E2^(3)=theta_A2^2. The anomaly only appears "
            "after condensation to level 1. In that sense the discrete-to-continuous lift is cleaner than the "
            "later affine cumulative regime: the first flow law is modular, and the quasi-modular correction is "
            "a downstream shadow of collapsing the level-3 tower onto the full modular plane."
        ),
        "sources": {
            "elkies_level3_lattices": "https://people.math.harvard.edu/~elkies/M272.19/nov25.pdf",
            "ramanujan_system_local": str(
                (ROOT / "exploration" / "w33_ramanujan_system.py").resolve()
            ),
            "affine_E2_boundary_local": str(
                (ROOT / "exploration" / "w33_affine_e8_e2_source.py").resolve()
            ),
        },
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 LEVEL-3 SOURCE FLOW BRIDGE")
    print("=" * 72)
    for key, value in summary["level3_source_flow_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
