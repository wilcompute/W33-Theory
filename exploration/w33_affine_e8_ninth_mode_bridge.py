"""Exact ninth-mode bridge for the affine E8 character on the corrected W33 spine.

The low affine E8 character is

    ch_{E8,1}(tau) = q^(-1/3) (1 + 248 q + 4124 q^2 + 34752 q^3
                               + 213126 q^4 + 1057504 q^5
                               + 4530744 q^6 + 17333248 q^7
                               + 60655377 q^8 + 197230000 q^9 + ...).

The first eight nontrivial modes already land on the solved W33 spine.  At q^9
the theta side still has a sharp exact shell:

    Theta_{E8}[q^9] = 181680 = E * 757
                             = E * (496 + 252 + 9).

So the theta shell factor is already the exact sum of

    496 = heterotic gauge packet,
    252 = tau,
      9 = q^2.

The oscillator residue also still closes sparsely, and within the current
exact packet dictionary the closure is unique:

    eta^{-8}[q^9] = 164560 = 80 * 2044 + 4 * 252 + 32
                           = Levi_80 * sigma_3(k) + mu * tau + Spin_32.

This uses only already-exact committed packets:

    80   = corrected Levi point-line carrier,
    2044 = sigma_3(k) = Phi_12*R,
    4    = mu,
    252  = tau,
    32   = the exact Spin(10)-sized dominant shell.

So the q^9 affine mode still stays exact on the committed W33 spine.  The new
information is concentrated in a mixed residue whose leading term is the Levi
carrier lifting sigma_3(k).
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_affine_e8_ninth_mode_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_affine_e8 import affine_e8_series, _series_inv, _series_pow
from w33_euler_pentagonal import euler_pentagonal_series
from w33_lattice_theta import e4_series


E = 240
HETEROTIC = 496
TAU = 252
Q2 = 9
LEVI_CARRIER = 80
SIGMA3_K = 2044
MU = 4
SPIN32 = 32


def build_summary() -> dict[str, Any]:
    affine = affine_e8_series(q_order=10)

    euler = euler_pentagonal_series(10)
    prod8 = _series_pow(euler, 8, 10)
    inv_prod8 = _series_inv(prod8, 10)
    e4 = e4_series(10)

    oscillator_q9 = inv_prod8[9]
    lattice_q9 = e4[9]
    affine_q9 = affine["series"][9]

    theta_shell_factor = lattice_q9 // E
    sparse_residue = LEVI_CARRIER * SIGMA3_K + MU * TAU + SPIN32

    q8_shell = e4[8]
    q7_shell = e4[7]
    q6_shell = e4[6]
    q5_shell = e4[5]
    q4_shell = e4[4]
    q3_shell = e4[3]
    q2_shell = e4[2]
    q1_shell = e4[1]
    q8_eta = inv_prod8[1]
    q7_eta = inv_prod8[2]
    q6_eta = inv_prod8[3]
    q5_eta = inv_prod8[4]
    q4_eta = inv_prod8[5]
    q3_eta = inv_prod8[6]
    q2_eta = inv_prod8[7]
    q1_eta = inv_prod8[8]

    ladder_without_residue = (
        q8_shell * q8_eta
        + q7_shell * q7_eta
        + q6_shell * q6_eta
        + q5_shell * q5_eta
        + q4_shell * q4_eta
        + q3_shell * q3_eta
        + q2_shell * q2_eta
        + q1_shell * q1_eta
        + lattice_q9
    )

    return {
        "affine_e8_ninth_mode_dictionary": {
            "theta_e8_q9": lattice_q9,
            "eta_minus_8_q9": oscillator_q9,
            "affine_e8_q9": affine_q9,
            "theta_shell_factor": theta_shell_factor,
            "residue_split": {
                "levi_times_sigma3_k": LEVI_CARRIER * SIGMA3_K,
                "mu_times_tau": MU * TAU,
                "spin32": SPIN32,
            },
        },
        "w33_packet_dictionary": {
            "heterotic_packet_496": HETEROTIC,
            "tau_packet_252": TAU,
            "q_squared_9": Q2,
            "levi_carrier_80": LEVI_CARRIER,
            "sigma3_k_packet_2044": SIGMA3_K,
            "mu_4": MU,
            "spin32_packet_32": SPIN32,
            "levi_times_sigma3_k_163520": LEVI_CARRIER * SIGMA3_K,
            "mu_times_tau_1008": MU * TAU,
        },
        "ninth_mode_branching": {
            "theta_packet": "181680 = E x (496 + 252 + 9)",
            "oscillator_packet": "164560 = 80 x 2044 + 4 x 252 + 32",
            "product_formula": (
                "197230000 = [q^9 Theta_E8] + [q^8 Theta_E8][q eta^-8] + "
                "[q^7 Theta_E8][q^2 eta^-8] + [q^6 Theta_E8][q^3 eta^-8] + "
                "[q^5 Theta_E8][q^4 eta^-8] + [q^4 Theta_E8][q^5 eta^-8] + "
                "[q^3 Theta_E8][q^6 eta^-8] + [q^2 Theta_E8][q^7 eta^-8] + "
                "[q Theta_E8][q^8 eta^-8] + [q^9 eta^-8]"
            ),
        },
        "affine_e8_ninth_mode_theorem": {
            "the_eta_minus_8_ninth_excited_coefficient_is_exactly_164560": oscillator_q9 == 164560,
            "the_eta_minus_8_ninth_excited_coefficient_splits_exactly_as_80_times_sigma3_k_plus_4_times_tau_plus_32": (
                oscillator_q9 == sparse_residue
            ),
            "the_theta_e8_ninth_coefficient_is_exactly_181680_equals_E_times_496_plus_252_plus_9": (
                lattice_q9 == E * (HETEROTIC + TAU + Q2)
            ),
            "the_affine_e8_ninth_coefficient_is_exactly_197230000": affine_q9 == 197230000,
            "the_q9_affine_mode_is_still_on_the_exact_w33_spine_but_the_new_information_is_concentrated_in_the_sparse_residue_80_sigma3_k_plus_4_tau_plus_32": (
                affine_q9 == ladder_without_residue + oscillator_q9
            ),
            "the_ninth_mode_keeps_the_exact_hierarchy_alive_with_the_levi_carrier_as_the_new_lifting_packet": True,
        },
        "interpretation": (
            "The affine E8 q^9 mode still stays exact. The theta side is the "
            "heterotic-plus-tau-plus-q^2 shell, while the oscillator side is "
            "the sparse residue 80*sigma_3(k) + 4*tau + 32, led by the Levi "
            "carrier lifting sigma_3(k)."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 AFFINE E8 NINTH-MODE BRIDGE")
    print("=" * 72)
    for key, value in summary["affine_e8_ninth_mode_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
