"""Exact graded Levi/Clifford pair on the point-line carrier.

The twin-V15 bridge shows that the 80-vertex Levi graph splits as

    80 = (1_p + 1_l) + (24_p + 24_l) + (15_p + 15_l),

with the 30-dimensional nullspace equal to the twin fifteens.

This script promotes that decomposition to an exact graded operator algebra:

  - the Levi adjacency L is odd with respect to the point/line grading Γ,
  - on the non-null image, L is just two exchange blocks with speeds 4 and √6,
  - after normalizing those two blocks separately, one gets an exact involution K,
  - Γ and K generate a clean Clifford pair on the live geometric carrier.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
import sys

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from exploration.w33_twin_v15_levi_null_bridge import _build_lines_and_spreads
from tools.analyze_balanced_orbit_stabilizer import build_w33


DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_levi_clifford_pair_bridge_summary.json"


def build_summary() -> dict[str, object]:
    _points, adjacency, _edges = build_w33()
    A_point = np.asarray(adjacency, dtype=float)
    _lines, H, _B = _build_lines_and_spreads(np.asarray(adjacency, dtype=int))
    H = H.astype(float)
    A_line = H.T @ H - 4.0 * np.eye(40)

    I40 = np.eye(40)
    J40 = np.ones((40, 40))

    P1_point = J40 / 40.0
    P24_point = (A_point + 4.0 * I40) / 6.0 - J40 / 15.0
    P15_point = I40 - P1_point - P24_point

    P1_line = J40 / 40.0
    P24_line = (A_line + 4.0 * I40) / 6.0 - J40 / 15.0
    P15_line = I40 - P1_line - P24_line

    P1_levi = np.block([[P1_point, np.zeros((40, 40))], [np.zeros((40, 40)), P1_line]])
    P24_levi = np.block([[P24_point, np.zeros((40, 40))], [np.zeros((40, 40)), P24_line]])
    P30_levi = np.block([[P15_point, np.zeros((40, 40))], [np.zeros((40, 40)), P15_line]])
    Pimg_levi = P1_levi + P24_levi

    L = np.block([[np.zeros((40, 40)), H], [H.T, np.zeros((40, 40))]])
    Gamma = np.block([[I40, np.zeros((40, 40))], [np.zeros((40, 40)), -I40]])

    K = (L @ P1_levi) / 4.0 + (L @ P24_levi) / np.sqrt(6.0)

    eigs = np.linalg.eigvalsh(L)
    rounded = []
    for value in eigs:
        if abs(value) < 1e-10:
            rounded.append(0.0)
        elif abs(abs(value) - 4.0) < 1e-10:
            rounded.append(4.0 if value > 0 else -4.0)
        elif abs(abs(value) - np.sqrt(6.0)) < 1e-10:
            rounded.append(float(np.sqrt(6.0)) if value > 0 else float(-np.sqrt(6.0)))
        else:
            rounded.append(float(value))

    hist: dict[str, int] = {}
    for value in rounded:
        key = f"{value:.12g}"
        hist[key] = hist.get(key, 0) + 1

    return {
        "carrier_dictionary": {
            "levi_split": "80 = (1_p + 1_l) + (24_p + 24_l) + (15_p + 15_l)",
            "nonnull_image": "50 = 2 + 48",
            "nullspace": "30 = 15_p + 15_l",
        },
        "exact_operators": {
            "L": "Levi adjacency [[0,H],[H^T,0]]",
            "Gamma": "point/line grading diag(I,-I)",
            "K": "normalized Levi exchange on (1+24)-image",
            "minimal_polynomial": "x (x^2 - 16) (x^2 - 6)",
        },
        "levi_spectrum_histogram": hist,
        "levi_clifford_theorem": {
            "the_levi_spectrum_is_exactly_pm4_once_pm_sqrt6_24_times_and_0_30_times": hist
            == {
                "-4": 1,
                f"{-np.sqrt(6.0):.12g}": 24,
                "0": 30,
                f"{np.sqrt(6.0):.12g}": 24,
                "4": 1,
            },
            "the_point_line_grading_squares_to_identity": bool(
                np.linalg.norm(Gamma @ Gamma - np.eye(80)) < 1e-12
            ),
            "the_levi_adjacency_is_odd_for_the_grading": bool(
                np.linalg.norm(Gamma @ L + L @ Gamma) < 1e-12
            ),
            "the_levi_nullspace_is_exactly_the_twin_15_block": bool(
                np.linalg.matrix_rank(P30_levi) == 30 and np.linalg.norm(L @ P30_levi) < 1e-12
            ),
            "the_levi_square_is_16_on_the_trivial_doublet_and_6_on_the_24_doublet": bool(
                np.linalg.norm((L @ L - 16.0 * np.eye(80)) @ P1_levi) < 1e-12
                and np.linalg.norm((L @ L - 6.0 * np.eye(80)) @ P24_levi) < 1e-12
            ),
            "the_normalized_exchange_K_is_an_exact_involution_on_the_nonnull_image": bool(
                np.linalg.norm(K @ K - Pimg_levi) < 1e-12
            ),
            "the_grading_and_normalized_exchange_generate_a_clifford_pair_on_the_nonnull_image": bool(
                np.linalg.norm(Gamma @ K + K @ Gamma) < 1e-12
            ),
        },
        "interpretation": (
            "The Levi carrier is not just another graph. It is an exact graded exchange algebra. "
            "The grading Gamma distinguishes points from lines, the Levi adjacency L is odd for that grading, "
            "and after normalizing the two nonzero speed blocks one gets an involution K that anticommutes with Gamma. "
            "So the live geometric carrier supports a genuine two-speed Clifford pair on the 1+24 image, while the "
            "twin 15_p + 15_l sector is the exact 30-dimensional null block."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("=" * 72)
    print("W33 LEVI CLIFFORD PAIR BRIDGE")
    print("=" * 72)
    for key, value in summary["levi_clifford_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
