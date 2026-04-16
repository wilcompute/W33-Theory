"""Boundary bridge at q^12 for the affine E8 character on the corrected W33 spine.

At q^12 the theta side becomes exceptionally rigid:

    Theta_{E8}[q^12] = 490560 = E * 2044 = E * sigma_3(k).

So the theta shell lands exactly on the sigma_3(k) packet itself.

But the oscillator coefficient no longer obeys the sparse exact packet laws
that were sufficient from q^7 through q^11.  Writing

    eta^{-8}[q^12] = 2418710,

an exhaustive search over the current exact packet dictionary shows that there
is no solution of either form

    a * sigma_3(k) + b * tau + c
or
    a * sigma_3(k) + b * tau + c * 168 + d,

with a,b,c,d in the committed packet set (plus zero).

So q^12 is the first one-sided mode:
    - theta side: still exact and maximally sharp,
    - oscillator side: no longer captured by the old sparse affine laws.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_affine_e8_twelfth_mode_boundary_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_affine_e8 import affine_e8_series, _series_inv, _series_pow
from w33_euler_pentagonal import euler_pentagonal_series
from w33_lattice_theta import e4_series


E = 240
SIGMA3_K = 2044
TAU = 252
DUAL_PAIR_FLAGS = 168
PACKET_SET = sorted(
    {
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 20, 24, 26,
        27, 30, 32, 36, 40, 44, 50, 52, 64, 72, 78, 80, 81, 84, 90, 96, 98,
        126, 168, 192, 204, 240, 248, 252, 273, 280, 336, 496, 720, 2044,
    }
)


def _search_sigma_tau_plus_packet(target: int) -> list[tuple[int, int, int]]:
    solutions: list[tuple[int, int, int]] = []
    for a in PACKET_SET:
        for b in PACKET_SET:
            rem = target - a * SIGMA3_K - b * TAU
            if rem in PACKET_SET:
                solutions.append((a, b, rem))
    return solutions


def _search_sigma_tau_dual_plus_packet(target: int) -> list[tuple[int, int, int, int]]:
    solutions: list[tuple[int, int, int, int]] = []
    for a in PACKET_SET:
        for b in PACKET_SET:
            for c in PACKET_SET:
                rem = target - a * SIGMA3_K - b * TAU - c * DUAL_PAIR_FLAGS
                if rem in PACKET_SET:
                    solutions.append((a, b, c, rem))
    return solutions


def build_summary() -> dict[str, Any]:
    affine = affine_e8_series(q_order=13)

    euler = euler_pentagonal_series(13)
    prod8 = _series_pow(euler, 8, 13)
    inv_prod8 = _series_inv(prod8, 13)
    e4 = e4_series(13)

    oscillator_q12 = inv_prod8[12]
    lattice_q12 = e4[12]
    affine_q12 = affine["series"][12]

    sparse_sigma_tau = _search_sigma_tau_plus_packet(oscillator_q12)
    sparse_sigma_tau_dual = _search_sigma_tau_dual_plus_packet(oscillator_q12)

    return {
        "affine_e8_twelfth_mode_dictionary": {
            "theta_e8_q12": lattice_q12,
            "eta_minus_8_q12": oscillator_q12,
            "affine_e8_q12": affine_q12,
            "theta_shell_factor": lattice_q12 // E,
        },
        "twelfth_mode_boundary_search": {
            "packet_set": PACKET_SET,
            "sigma_tau_plus_packet_solutions": sparse_sigma_tau,
            "sigma_tau_dual_plus_packet_solutions": sparse_sigma_tau_dual,
        },
        "affine_e8_twelfth_mode_boundary_theorem": {
            "the_theta_e8_twelfth_coefficient_is_exactly_490560_equals_E_times_sigma3_k": (
                lattice_q12 == E * SIGMA3_K
            ),
            "the_eta_minus_8_twelfth_excited_coefficient_is_exactly_2418710": oscillator_q12 == 2418710,
            "the_twelfth_mode_has_no_sparse_solution_of_the_form_a_sigma3_k_plus_b_tau_plus_c_with_a_b_c_in_the_current_packet_dictionary": (
                len(sparse_sigma_tau) == 0
            ),
            "the_twelfth_mode_has_no_sparse_solution_of_the_form_a_sigma3_k_plus_b_tau_plus_c_times_168_plus_d_with_a_b_c_d_in_the_current_packet_dictionary": (
                len(sparse_sigma_tau_dual) == 0
            ),
            "the_twelfth_mode_is_the_first_one_sided_affine_boundary_on_the_current_exact_w33_spine": (
                lattice_q12 == E * SIGMA3_K and len(sparse_sigma_tau) == 0 and len(sparse_sigma_tau_dual) == 0
            ),
        },
        "interpretation": (
            "At q^12 the theta side becomes maximally sharp as E*sigma_3(k), but "
            "the oscillator side no longer admits the sparse sigma/tau packet laws "
            "that were enough from q^7 through q^11. So q^12 is the first honest "
            "one-sided boundary on the current affine W33 spine."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 AFFINE E8 TWELFTH-MODE BOUNDARY BRIDGE")
    print("=" * 72)
    for key, value in summary["affine_e8_twelfth_mode_boundary_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
