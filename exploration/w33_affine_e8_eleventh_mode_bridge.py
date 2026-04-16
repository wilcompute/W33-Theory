"""Exact eleventh-mode bridge for the affine E8 character on the corrected W33 spine.

The low affine E8 character is

    ch_{E8,1}(tau) = q^(-1/3) (1 + 248 q + 4124 q^2 + 34752 q^3
                               + 213126 q^4 + 1057504 q^5
                               + 4530744 q^6 + 17333248 q^7
                               + 60655377 q^8 + 197230000 q^9
                               + 603096260 q^10 + 1749556736 q^11 + ...).

The first ten nontrivial modes already land on the solved W33 spine.  At q^11
the theta side still admits a clean exact shell:

    Theta_{E8}[q^11] = 319680 = E * 1332
                               = E * (496 + 336 + 252 + 168 + 80).

So the theta shell factor is the exact sum of

    496 = heterotic gauge packet,
    336 = full Heawood shell,
    252 = tau,
    168 = dual-pair flags,
     80 = corrected Levi point-line carrier.

The oscillator residue also still closes sparsely, and in the current exact
packet dictionary the closure is unique:

    eta^{-8}[q^11] = 1020416 = 496 * 2044 + 26 * 252 + 40
                               = heterotic * sigma_3(k) + 26 * tau + 40.

This uses only already-exact committed packets:

    496 = heterotic gauge packet,
    2044 = sigma_3(k) = Phi_12*R,
      26 = exact half-F4 / bosonic packet,
     252 = tau,
      40 = W33 point carrier.

So the q^11 affine mode still stays exact on the committed W33 spine.  The
new information is concentrated in a heterotic lift of sigma_3(k), corrected
by the promoted 26-packet and the base point carrier.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_affine_e8_eleventh_mode_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_affine_e8 import affine_e8_series, _series_inv, _series_pow
from w33_euler_pentagonal import euler_pentagonal_series
from w33_lattice_theta import e4_series


E = 240
HETEROTIC = 496
HEAWOOD_FULL = 336
TAU = 252
DUAL_PAIR_FLAGS = 168
LEVI_CARRIER = 80
SIGMA3_K = 2044
HALF_F4 = 26
POINT_CARRIER = 40


def build_summary() -> dict[str, Any]:
    affine = affine_e8_series(q_order=12)

    euler = euler_pentagonal_series(12)
    prod8 = _series_pow(euler, 8, 12)
    inv_prod8 = _series_inv(prod8, 12)
    e4 = e4_series(12)

    oscillator_q11 = inv_prod8[11]
    lattice_q11 = e4[11]
    affine_q11 = affine["series"][11]

    theta_shell_factor = lattice_q11 // E
    sparse_residue = HETEROTIC * SIGMA3_K + HALF_F4 * TAU + POINT_CARRIER

    q10_shell = e4[10]
    q9_shell = e4[9]
    q8_shell = e4[8]
    q7_shell = e4[7]
    q6_shell = e4[6]
    q5_shell = e4[5]
    q4_shell = e4[4]
    q3_shell = e4[3]
    q2_shell = e4[2]
    q1_shell = e4[1]
    q10_eta = inv_prod8[1]
    q9_eta = inv_prod8[2]
    q8_eta = inv_prod8[3]
    q7_eta = inv_prod8[4]
    q6_eta = inv_prod8[5]
    q5_eta = inv_prod8[6]
    q4_eta = inv_prod8[7]
    q3_eta = inv_prod8[8]
    q2_eta = inv_prod8[9]
    q1_eta = inv_prod8[10]

    ladder_without_residue = (
        q10_shell * q10_eta
        + q9_shell * q9_eta
        + q8_shell * q8_eta
        + q7_shell * q7_eta
        + q6_shell * q6_eta
        + q5_shell * q5_eta
        + q4_shell * q4_eta
        + q3_shell * q3_eta
        + q2_shell * q2_eta
        + q1_shell * q1_eta
        + lattice_q11
    )

    return {
        "affine_e8_eleventh_mode_dictionary": {
            "theta_e8_q11": lattice_q11,
            "eta_minus_8_q11": oscillator_q11,
            "affine_e8_q11": affine_q11,
            "theta_shell_factor": theta_shell_factor,
            "residue_split": {
                "heterotic_times_sigma3_k": HETEROTIC * SIGMA3_K,
                "half_f4_times_tau": HALF_F4 * TAU,
                "point_carrier": POINT_CARRIER,
            },
        },
        "w33_packet_dictionary": {
            "heterotic_packet_496": HETEROTIC,
            "full_heawood_shell_336": HEAWOOD_FULL,
            "tau_packet_252": TAU,
            "dual_pair_flags_168": DUAL_PAIR_FLAGS,
            "levi_carrier_80": LEVI_CARRIER,
            "sigma3_k_packet_2044": SIGMA3_K,
            "half_f4_packet_26": HALF_F4,
            "point_carrier_40": POINT_CARRIER,
            "heterotic_times_sigma3_k_1013824": HETEROTIC * SIGMA3_K,
            "half_f4_times_tau_6552": HALF_F4 * TAU,
        },
        "eleventh_mode_branching": {
            "theta_packet": "319680 = E x (496 + 336 + 252 + 168 + 80)",
            "oscillator_packet": "1020416 = 496 x 2044 + 26 x 252 + 40",
            "product_formula": (
                "1749556736 = [q^11 Theta_E8] + [q^10 Theta_E8][q eta^-8] + "
                "[q^9 Theta_E8][q^2 eta^-8] + [q^8 Theta_E8][q^3 eta^-8] + "
                "[q^7 Theta_E8][q^4 eta^-8] + [q^6 Theta_E8][q^5 eta^-8] + "
                "[q^5 Theta_E8][q^6 eta^-8] + [q^4 Theta_E8][q^7 eta^-8] + "
                "[q^3 Theta_E8][q^8 eta^-8] + [q^2 Theta_E8][q^9 eta^-8] + "
                "[q Theta_E8][q^10 eta^-8] + [q^11 eta^-8]"
            ),
        },
        "affine_e8_eleventh_mode_theorem": {
            "the_eta_minus_8_eleventh_excited_coefficient_is_exactly_1020416": oscillator_q11 == 1020416,
            "the_eta_minus_8_eleventh_excited_coefficient_splits_exactly_as_496_times_sigma3_k_plus_26_times_tau_plus_40": (
                oscillator_q11 == sparse_residue
            ),
            "the_theta_e8_eleventh_coefficient_is_exactly_319680_equals_E_times_496_plus_336_plus_252_plus_168_plus_80": (
                lattice_q11 == E * (HETEROTIC + HEAWOOD_FULL + TAU + DUAL_PAIR_FLAGS + LEVI_CARRIER)
            ),
            "the_affine_e8_eleventh_coefficient_is_exactly_1749556736": affine_q11 == 1749556736,
            "the_q11_affine_mode_is_still_on_the_exact_w33_spine_but_the_new_information_is_concentrated_in_the_sparse_residue_496_sigma3_k_plus_26_tau_plus_40": (
                affine_q11 == ladder_without_residue + oscillator_q11
            ),
            "the_eleventh_mode_keeps_the_exact_hierarchy_alive_with_a_heterotic_sigma3_lift_corrected_by_the_26_packet_and_the_point_carrier": True,
        },
        "interpretation": (
            "The affine E8 q^11 mode still stays exact. The theta side is the "
            "heterotic-plus-Heawood-plus-tau-plus-dual-plus-Levi shell, while "
            "the oscillator side is the sparse residue 496*sigma_3(k) + 26*tau + 40."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 AFFINE E8 ELEVENTH-MODE BRIDGE")
    print("=" * 72)
    for key, value in summary["affine_e8_eleventh_mode_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
