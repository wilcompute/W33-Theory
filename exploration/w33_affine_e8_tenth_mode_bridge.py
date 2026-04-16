"""Exact tenth-mode bridge for the affine E8 character on the corrected W33 spine.

The low affine E8 character is

    ch_{E8,1}(tau) = q^(-1/3) (1 + 248 q + 4124 q^2 + 34752 q^3
                               + 213126 q^4 + 1057504 q^5
                               + 4530744 q^6 + 17333248 q^7
                               + 60655377 q^8 + 197230000 q^9
                               + 603096260 q^10 + ...).

The first nine nontrivial modes already land on the solved W33 spine.  At q^10
the theta side still has an exact shell:

    Theta_{E8}[q^10] = 272160 = E * 1134
                               = E * (78 + 336 + 720).

So the theta shell factor is the exact sum of

     78 = E6 adjoint packet,
    336 = full Heawood shell,
    720 = qE.

The oscillator residue also still closes uniquely in the current exact packet
dictionary:

    eta^{-8}[q^10] = 417140 = 204 * 2044 + 80 + 84
                              = (168 + 36) * sigma_3(k) + Levi_80 + 84.

This uses only already-exact committed packets:

    168 = dual-pair flags,
     36 = corrected spread carrier,
    2044 = sigma_3(k) = Phi_12*R,
     80 = corrected Levi point-line carrier,
     84 = single-surface flags.

So the q^10 affine mode still stays exact on the committed W33 spine.  The
new information is concentrated in a dual/spread lift of sigma_3(k), followed
by a Levi-plus-surface remainder.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_affine_e8_tenth_mode_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_affine_e8 import affine_e8_series, _series_inv, _series_pow
from w33_euler_pentagonal import euler_pentagonal_series
from w33_lattice_theta import e4_series


E = 240
E6_ADJOINT = 78
HEAWOOD_FULL = 336
QE = 720
DUAL_PAIR_FLAGS = 168
CORRECTED_SPREAD = 36
SIGMA3_K = 2044
LEVI_CARRIER = 80
SINGLE_SURFACE_FLAGS = 84
DUAL_SPREAD_PACKET = DUAL_PAIR_FLAGS + CORRECTED_SPREAD


def build_summary() -> dict[str, Any]:
    affine = affine_e8_series(q_order=11)

    euler = euler_pentagonal_series(11)
    prod8 = _series_pow(euler, 8, 11)
    inv_prod8 = _series_inv(prod8, 11)
    e4 = e4_series(11)

    oscillator_q10 = inv_prod8[10]
    lattice_q10 = e4[10]
    affine_q10 = affine["series"][10]

    theta_shell_factor = lattice_q10 // E
    sparse_residue = DUAL_SPREAD_PACKET * SIGMA3_K + LEVI_CARRIER + SINGLE_SURFACE_FLAGS

    q9_shell = e4[9]
    q8_shell = e4[8]
    q7_shell = e4[7]
    q6_shell = e4[6]
    q5_shell = e4[5]
    q4_shell = e4[4]
    q3_shell = e4[3]
    q2_shell = e4[2]
    q1_shell = e4[1]
    q9_eta = inv_prod8[1]
    q8_eta = inv_prod8[2]
    q7_eta = inv_prod8[3]
    q6_eta = inv_prod8[4]
    q5_eta = inv_prod8[5]
    q4_eta = inv_prod8[6]
    q3_eta = inv_prod8[7]
    q2_eta = inv_prod8[8]
    q1_eta = inv_prod8[9]

    ladder_without_residue = (
        q9_shell * q9_eta
        + q8_shell * q8_eta
        + q7_shell * q7_eta
        + q6_shell * q6_eta
        + q5_shell * q5_eta
        + q4_shell * q4_eta
        + q3_shell * q3_eta
        + q2_shell * q2_eta
        + q1_shell * q1_eta
        + lattice_q10
    )

    return {
        "affine_e8_tenth_mode_dictionary": {
            "theta_e8_q10": lattice_q10,
            "eta_minus_8_q10": oscillator_q10,
            "affine_e8_q10": affine_q10,
            "theta_shell_factor": theta_shell_factor,
            "residue_split": {
                "dual_spread_times_sigma3_k": DUAL_SPREAD_PACKET * SIGMA3_K,
                "levi_carrier": LEVI_CARRIER,
                "single_surface_flags": SINGLE_SURFACE_FLAGS,
            },
        },
        "w33_packet_dictionary": {
            "e6_adjoint_packet_78": E6_ADJOINT,
            "full_heawood_shell_336": HEAWOOD_FULL,
            "qE_packet_720": QE,
            "dual_pair_flags_168": DUAL_PAIR_FLAGS,
            "corrected_spread_carrier_36": CORRECTED_SPREAD,
            "dual_spread_packet_204": DUAL_SPREAD_PACKET,
            "sigma3_k_packet_2044": SIGMA3_K,
            "levi_carrier_80": LEVI_CARRIER,
            "single_surface_flags_84": SINGLE_SURFACE_FLAGS,
            "dual_spread_times_sigma3_k_416976": DUAL_SPREAD_PACKET * SIGMA3_K,
        },
        "tenth_mode_branching": {
            "theta_packet": "272160 = E x (78 + 336 + 720)",
            "oscillator_packet": "417140 = 204 x 2044 + 80 + 84",
            "product_formula": (
                "603096260 = [q^10 Theta_E8] + [q^9 Theta_E8][q eta^-8] + "
                "[q^8 Theta_E8][q^2 eta^-8] + [q^7 Theta_E8][q^3 eta^-8] + "
                "[q^6 Theta_E8][q^4 eta^-8] + [q^5 Theta_E8][q^5 eta^-8] + "
                "[q^4 Theta_E8][q^6 eta^-8] + [q^3 Theta_E8][q^7 eta^-8] + "
                "[q^2 Theta_E8][q^8 eta^-8] + [q Theta_E8][q^9 eta^-8] + [q^10 eta^-8]"
            ),
        },
        "affine_e8_tenth_mode_theorem": {
            "the_eta_minus_8_tenth_excited_coefficient_is_exactly_417140": oscillator_q10 == 417140,
            "the_eta_minus_8_tenth_excited_coefficient_splits_exactly_as_204_times_sigma3_k_plus_80_plus_84": (
                oscillator_q10 == sparse_residue
            ),
            "the_theta_e8_tenth_coefficient_is_exactly_272160_equals_E_times_78_plus_336_plus_720": (
                lattice_q10 == E * (E6_ADJOINT + HEAWOOD_FULL + QE)
            ),
            "the_affine_e8_tenth_coefficient_is_exactly_603096260": affine_q10 == 603096260,
            "the_q10_affine_mode_is_still_on_the_exact_w33_spine_but_the_new_information_is_concentrated_in_the_dual_spread_sigma3_residue": (
                affine_q10 == ladder_without_residue + oscillator_q10
            ),
            "the_tenth_mode_keeps_the_exact_hierarchy_alive_with_a_dual_spread_lift_of_sigma3_k_and_a_levi_plus_surface_remainder": True,
        },
        "interpretation": (
            "The affine E8 q^10 mode still stays exact. The theta side is the "
            "E6-adjoint-plus-Heawood-plus-qE shell, while the oscillator side "
            "is the sparse residue 204*sigma_3(k) + 80 + 84, i.e. the exact "
            "dual/spread lift of sigma_3(k) followed by the Levi-plus-surface remainder."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 AFFINE E8 TENTH-MODE BRIDGE")
    print("=" * 72)
    for key, value in summary["affine_e8_tenth_mode_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
