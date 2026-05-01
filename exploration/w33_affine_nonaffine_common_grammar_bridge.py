"""Common input grammar shared by the affine and non-affine W33 packet spines.

The recent affine bridges closed the canonical promoted shell generators as the
exact input grammar

    mu * {mu, mu+1, 2q, q^2, Theta}
      = {16, 20, 24, 36, 40}

with affine kernel outputs

    248, 336, 480, 728, 720.

This bridge lifts that same finite input grammar back into the non-affine W33
operator spine. The five input values are already exact packet counts there:

    16 = common Dirac core
    20 = 4D algebraic curvature shell = lambda * Phi4
    24 = corrected complement / 24-packet
    36 = spread carrier
    40 = point carrier

So the affine shell grammar is not a detached modular layer. It is the same
input grammar already present on the exact non-affine packet ladder.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    from exploration.w33_bridge_inputs import load_bridge_json
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    from w33_bridge_inputs import load_bridge_json


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = (
    DATA_DIR / "w33_affine_nonaffine_common_grammar_bridge_summary.json"
)


Q = 3
LAMBDA = 2
MU = 4
THETA = 10
PHI4 = Q * Q + 1


def _sigma1(n: int) -> int:
    return sum(d for d in range(1, n + 1) if n % d == 0)


def _kernel(n: int) -> int:
    return 8 * _sigma1(n)


def _riemann_algebraic_curvature_dim(n: int) -> int:
    return n * n * (n * n - 1) // 12


def _load_json(filename: str) -> dict[str, Any]:
    return load_bridge_json(filename, DATA_DIR)


NONAFFINE_PACKET_ROWS = {
    "mu": {
        "input_value": MU,
        "mu_times_input": MU * MU,
        "nonaffine_packet": "common_Dirac_core_16",
        "affine_packet": "E8_adjoint_248",
    },
    "mu_plus_1": {
        "input_value": MU + 1,
        "mu_times_input": MU * (MU + 1),
        "nonaffine_packet": "four_dimensional_algebraic_curvature_shell_20",
        "affine_packet": "Heawood_full_shell_336",
    },
    "2q": {
        "input_value": 2 * Q,
        "mu_times_input": MU * (2 * Q),
        "nonaffine_packet": "corrected_complement_24_packet",
        "affine_packet": "full_Dirac_shell_480",
    },
    "q_squared": {
        "input_value": Q * Q,
        "mu_times_input": MU * Q * Q,
        "nonaffine_packet": "spread_carrier_36",
        "affine_packet": "A26_ambient_shell_728",
    },
    "Theta": {
        "input_value": THETA,
        "mu_times_input": MU * THETA,
        "nonaffine_packet": "point_carrier_40",
        "affine_packet": "qE_shell_720",
    },
}


EXPECTED_AFFINE_OUTPUTS = {
    "mu": 248,
    "mu_plus_1": 336,
    "2q": 480,
    "q_squared": 728,
    "Theta": 720,
}


def build_summary() -> dict[str, Any]:
    gamma = _load_json("w33_gamma16_chirality_bridge_summary.json")
    quantum = _load_json("w33_quantum_split_operator_bridge_summary.json")
    spread = _load_json("w33_spread_overlap_algebra_bridge_summary.json")

    exact_common_16 = gamma["exact_packets"]["dominant_shell"]["16"]
    exact_complement_24 = quantum["quantum_split_dictionary"]["exact_complement_24"]
    exact_spread_36 = spread["spread_carrier_dictionary"]["spread_count"]
    exact_point_40 = spread["spread_carrier_dictionary"]["line_count"]
    exact_curvature_20 = _riemann_algebraic_curvature_dim(4)

    rows: dict[str, Any] = {}
    for key, base in NONAFFINE_PACKET_ROWS.items():
        index = base["mu_times_input"]
        if key == "mu":
            nonaffine_value = exact_common_16
        elif key == "mu_plus_1":
            nonaffine_value = exact_curvature_20
        elif key == "2q":
            nonaffine_value = exact_complement_24
        elif key == "q_squared":
            nonaffine_value = exact_spread_36
        else:
            nonaffine_value = exact_point_40

        rows[key] = {
            **base,
            "nonaffine_value": nonaffine_value,
            "affine_kernel_value": _kernel(index),
            "expected_affine_output": EXPECTED_AFFINE_OUTPUTS[key],
        }

    grammar_sequence = ["mu", "mu_plus_1", "2q", "q_squared", "Theta"]

    return {
        "affine_nonaffine_common_grammar_dictionary": {
            "q": Q,
            "lambda": LAMBDA,
            "mu": MU,
            "Phi4": PHI4,
            "Theta": THETA,
            "curvature_shell_formula": {
                "lambda_times_Phi4": LAMBDA * PHI4,
                "dim_Riem_alg_R4": exact_curvature_20,
            },
            "grammar_rows": rows,
            "common_input_grammar": [
                rows[key]["mu_times_input"] for key in grammar_sequence
            ],
            "common_affine_output_grammar": [
                rows[key]["affine_kernel_value"] for key in grammar_sequence
            ],
        },
        "affine_nonaffine_common_grammar_theorem": {
            "mu_squared_is_the_exact_common_dirac_core_16": (
                rows["mu"]["mu_times_input"] == 16
                and rows["mu"]["nonaffine_value"] == 16
            ),
            "mu_times_mu_plus_1_is_the_exact_4d_algebraic_curvature_shell_20": (
                rows["mu_plus_1"]["mu_times_input"] == 20
                and rows["mu_plus_1"]["nonaffine_value"] == 20
                and LAMBDA * PHI4 == exact_curvature_20
            ),
            "mu_times_2q_is_the_exact_corrected_24_packet": (
                rows["2q"]["mu_times_input"] == 24
                and rows["2q"]["nonaffine_value"] == 24
            ),
            "mu_times_q_squared_is_the_exact_spread_carrier_36": (
                rows["q_squared"]["mu_times_input"] == 36
                and rows["q_squared"]["nonaffine_value"] == 36
            ),
            "mu_times_Theta_is_the_exact_point_carrier_40": (
                rows["Theta"]["mu_times_input"] == 40
                and rows["Theta"]["nonaffine_value"] == 40
            ),
            "the_affine_mu_input_grammar_is_exactly_the_nonaffine_packet_ladder_16_20_24_36_40": (
                [rows[key]["mu_times_input"] for key in grammar_sequence]
                == [16, 20, 24, 36, 40]
                and [rows[key]["nonaffine_value"] for key in grammar_sequence]
                == [16, 20, 24, 36, 40]
            ),
            "the_shared_input_grammar_maps_under_the_affine_divisor_kernel_to_248_336_480_728_720": (
                [rows[key]["affine_kernel_value"] for key in grammar_sequence]
                == [248, 336, 480, 728, 720]
            ),
            "the_promoted_affine_shell_grammar_and_the_nonaffine_operator_spine_share_one_exact_input_grammar": (
                [rows[key]["mu_times_input"] for key in grammar_sequence]
                == [16, 20, 24, 36, 40]
                and [rows[key]["nonaffine_value"] for key in grammar_sequence]
                == [16, 20, 24, 36, 40]
                and [rows[key]["affine_kernel_value"] for key in grammar_sequence]
                == [248, 336, 480, 728, 720]
            ),
        },
        "interpretation": (
            "The affine shell grammar is already the native non-affine packet "
            "ladder. The same exact input values 16, 20, 24, 36, 40 are "
            "respectively the common Dirac core, the 4D algebraic curvature "
            "shell, the corrected 24-packet, the spread carrier, and the point "
            "carrier. The affine divisor kernel then lifts that same input "
            "grammar to the promoted shell outputs 248, 336, 480, 728, 720."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 AFFINE / NON-AFFINE COMMON GRAMMAR BRIDGE")
    print("=" * 72)
    for key, value in summary["affine_nonaffine_common_grammar_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
