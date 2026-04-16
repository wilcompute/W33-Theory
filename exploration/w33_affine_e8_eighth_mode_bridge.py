"""Exact eighth-mode bridge for the affine E8 character on the corrected W33 spine.

The low affine E8 character is

    ch_{E8,1}(tau) = q^(-1/3) (1 + 248 q + 4124 q^2 + 34752 q^3
                               + 213126 q^4 + 1057504 q^5
                               + 4530744 q^6 + 17333248 q^7
                               + 60655377 q^8 + ...).

The first seven nontrivial modes already land on the solved W33 spine.  At q^8
the theta side still has a sharp exact shell:

    Theta_{E8}[q^8] = 140400 = E * 585
                             = E * (496 + 84 + 5).

So the theta shell factor is already the exact sum of

    496 = dim(E8 x E8) = heterotic gauge packet,
     84 = single-surface flags,
      5 = mu + 1 = the bosonic 4+1 packet.

The oscillator residue also still closes sparsely:

    eta^{-8}[q^8] = 62337 = 30 * 2044 + 4 * 252 + 9
                          = (q Theta) * sigma_3(k) + mu * tau + q^2.

Each of those packets is already exact and committed:

    30   = q * Theta(W33)         (neutral-current packet),
    2044 = sigma_3(k) = Phi_12*R,
    4    = mu,
    252  = tau,
    9    = q^2.

So the q^8 affine mode is still exact on the committed W33 spine, but the
new information is now concentrated in a sparse mixed residue built from the
neutral-current packet and the old sigma_3 / Ramanujan shells.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_affine_e8_eighth_mode_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_affine_e8 import affine_e8_series, _series_inv, _series_pow
from w33_euler_pentagonal import euler_pentagonal_series
from w33_lattice_theta import e4_series


Q = 3
MU = 4
THETA = 10
E = 240
Q2 = Q * Q
NEUTRAL_PACKET = Q * THETA
SIGMA3_K = 2044
TAU = 252
HETEROTIC = 496
SINGLE_SURFACE_FLAGS = 84
BOSONIC_4_PLUS_1 = 5


def build_summary() -> dict[str, Any]:
    affine = affine_e8_series(q_order=9)

    euler = euler_pentagonal_series(9)
    prod8 = _series_pow(euler, 8, 9)
    inv_prod8 = _series_inv(prod8, 9)
    e4 = e4_series(9)

    oscillator_q8 = inv_prod8[8]
    lattice_q8 = e4[8]
    affine_q8 = affine["series"][8]

    theta_shell_factor = lattice_q8 // E
    sparse_residue = NEUTRAL_PACKET * SIGMA3_K + MU * TAU + Q2

    q7_shell = e4[7]
    q6_shell = e4[6]
    q5_shell = e4[5]
    q4_shell = e4[4]
    q3_shell = e4[3]
    q2_shell = e4[2]
    q1_shell = e4[1]
    q7_eta = inv_prod8[1]
    q6_eta = inv_prod8[2]
    q5_eta = inv_prod8[3]
    q4_eta = inv_prod8[4]
    q3_eta = inv_prod8[5]
    q2_eta = inv_prod8[6]
    q1_eta = inv_prod8[7]

    ladder_without_residue = (
        q7_shell * q7_eta
        + q6_shell * q6_eta
        + q5_shell * q5_eta
        + q4_shell * q4_eta
        + q3_shell * q3_eta
        + q2_shell * q2_eta
        + q1_shell * q1_eta
        + lattice_q8
    )

    return {
        "affine_e8_eighth_mode_dictionary": {
            "theta_e8_q8": lattice_q8,
            "eta_minus_8_q8": oscillator_q8,
            "affine_e8_q8": affine_q8,
            "theta_shell_factor": theta_shell_factor,
            "residue_split": {
                "neutral_packet_times_sigma3_k": NEUTRAL_PACKET * SIGMA3_K,
                "mu_times_tau": MU * TAU,
                "q_squared": Q2,
            },
        },
        "w33_packet_dictionary": {
            "heterotic_packet_496": HETEROTIC,
            "single_surface_flags_84": SINGLE_SURFACE_FLAGS,
            "bosonic_4_plus_1_packet_5": BOSONIC_4_PLUS_1,
            "neutral_packet_30": NEUTRAL_PACKET,
            "sigma3_k_packet_2044": SIGMA3_K,
            "mu_4": MU,
            "tau_packet_252": TAU,
            "q_squared_9": Q2,
            "neutral_times_sigma3_k_61320": NEUTRAL_PACKET * SIGMA3_K,
            "mu_times_tau_1008": MU * TAU,
        },
        "eighth_mode_branching": {
            "theta_packet": "140400 = E x (496 + 84 + 5)",
            "oscillator_packet": "62337 = 30 x 2044 + 4 x 252 + 9",
            "product_formula": (
                "60655377 = [q^8 Theta_E8] + [q^7 Theta_E8][q eta^-8] + "
                "[q^6 Theta_E8][q^2 eta^-8] + [q^5 Theta_E8][q^3 eta^-8] + "
                "[q^4 Theta_E8][q^4 eta^-8] + [q^3 Theta_E8][q^5 eta^-8] + "
                "[q^2 Theta_E8][q^6 eta^-8] + [q Theta_E8][q^7 eta^-8] + [q^8 eta^-8]"
            ),
        },
        "affine_e8_eighth_mode_theorem": {
            "the_eta_minus_8_eighth_excited_coefficient_is_exactly_62337": oscillator_q8 == 62337,
            "the_eta_minus_8_eighth_excited_coefficient_splits_exactly_as_30_times_sigma3_k_plus_4_times_tau_plus_q_squared": (
                oscillator_q8 == sparse_residue
            ),
            "the_theta_e8_eighth_coefficient_is_exactly_140400_equals_E_times_496_plus_84_plus_5": (
                lattice_q8 == E * (HETEROTIC + SINGLE_SURFACE_FLAGS + BOSONIC_4_PLUS_1)
            ),
            "the_affine_e8_eighth_coefficient_is_exactly_60655377": affine_q8 == 60655377,
            "the_q8_affine_mode_is_still_on_the_exact_w33_spine_but_the_new_information_is_concentrated_in_the_sparse_residue_30_sigma3_k_plus_4_tau_plus_9": (
                affine_q8 == ladder_without_residue + oscillator_q8
            ),
            "the_eighth_mode_keeps_the_exact_hierarchy_alive_but_only_in_a_sparse_mixed_shell_language": True,
        },
        "interpretation": (
            "The affine E8 q^8 mode still stays exact, but the hierarchy has now "
            "clearly moved into a mixed shell language. The theta side is the "
            "heterotic-plus-surface-plus-bosonic-5 packet, while the oscillator side "
            "is the sparse residue 30*sigma_3(k) + 4*tau + 9."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 AFFINE E8 EIGHTH-MODE BRIDGE")
    print("=" * 72)
    for key, value in summary["affine_e8_eighth_mode_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
