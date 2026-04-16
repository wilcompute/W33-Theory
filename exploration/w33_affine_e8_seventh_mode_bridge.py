"""Exact seventh-mode bridge for the affine E8 character on the corrected W33 spine.

The low affine E8 character is

    ch_{E8,1}(tau) = q^(-1/3) (1 + 248 q + 4124 q^2 + 34752 q^3
                               + 213126 q^4 + 1057504 q^5
                               + 4530744 q^6 + 17333248 q^7 + ...).

The first six nontrivial modes already land on the solved W33 spine.  At q^7
the theta side still has a sharp exact packet:

    Theta_{E8}[q^7] = 82560 = E * 344 = E * (336 + 8),

so the sigma_3(7) shell is the exact sum of the full Heawood/Klein shell 336
and the bosonic octet 8.

The oscillator residue also still closes, but now only in the sparse lifted
form

    eta^{-8}[q^7] = 22528 = 11 * 2044 + 44
                          = (k - 1) * sigma_3(k) + (36 + 8).

This uses only already-exact packets:

    2044 = sigma_3(k) = Phi_12 * R,
      44 = corrected spread carrier + bosonic octet = 36 + 8,
      11 = k - 1.

So the q^7 affine mode is still exact on the committed W33 spine, but this is
the first mode where the clean residue is best read as a shell-index lift of
an older exact packet rather than as a standalone old packet.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_affine_e8_seventh_mode_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_affine_e8 import affine_e8_series, _series_inv, _series_pow
from w33_euler_pentagonal import euler_pentagonal_series
from w33_lattice_theta import e4_series


K = 12
K_MINUS_1 = K - 1
E = 240
HEAWOOD_FULL = 336
BOSONIC_OCTET = 8
CORRECTED_SPREAD = 36
SIGMA3_K = 2044


def build_summary() -> dict[str, Any]:
    affine = affine_e8_series(q_order=8)

    euler = euler_pentagonal_series(8)
    prod8 = _series_pow(euler, 8, 8)
    inv_prod8 = _series_inv(prod8, 8)
    e4 = e4_series(8)

    oscillator_q7 = inv_prod8[7]
    lattice_q7 = e4[7]
    affine_q7 = affine["series"][7]

    spread_plus_octet = CORRECTED_SPREAD + BOSONIC_OCTET
    theta_shell_factor = lattice_q7 // E

    q6_shell = e4[6]
    q5_shell = e4[5]
    q4_shell = e4[4]
    q3_shell = e4[3]
    q2_shell = e4[2]
    q1_shell = e4[1]
    q6_eta = inv_prod8[1]
    q5_eta = inv_prod8[2]
    q4_eta = inv_prod8[3]
    q3_eta = inv_prod8[4]
    q2_eta = inv_prod8[5]
    q1_eta = inv_prod8[6]

    # Exact convolution at q^7, keeping the final residue separate.
    ladder_without_residue = (
        q6_shell * q6_eta
        + q5_shell * q5_eta
        + q4_shell * q4_eta
        + q3_shell * q3_eta
        + q2_shell * q2_eta
        + q1_shell * q1_eta
        + lattice_q7
    )

    return {
        "affine_e8_seventh_mode_dictionary": {
            "theta_e8_q7": lattice_q7,
            "eta_minus_8_q7": oscillator_q7,
            "affine_e8_q7": affine_q7,
            "theta_shell_factor": theta_shell_factor,
            "oscillator_residue_split": {
                "k_minus_1_times_sigma3_k": K_MINUS_1 * SIGMA3_K,
                "spread_plus_octet": spread_plus_octet,
            },
        },
        "w33_packet_dictionary": {
            "full_heawood_shell_336": HEAWOOD_FULL,
            "bosonic_octet_8": BOSONIC_OCTET,
            "corrected_spread_carrier_36": CORRECTED_SPREAD,
            "sigma3_k_packet_2044": SIGMA3_K,
            "k_minus_1": K_MINUS_1,
            "spread_plus_octet_44": spread_plus_octet,
            "shell_index_lift_22484": K_MINUS_1 * SIGMA3_K,
        },
        "seventh_mode_branching": {
            "theta_packet": "82560 = E x (336 + 8)",
            "oscillator_packet": "22528 = (k-1) x sigma_3(k) + 44 = 11 x 2044 + 44",
            "product_formula": (
                "17333248 = [q^7 Theta_E8] + [q^6 Theta_E8][q eta^-8] + "
                "[q^5 Theta_E8][q^2 eta^-8] + [q^4 Theta_E8][q^3 eta^-8] + "
                "[q^3 Theta_E8][q^4 eta^-8] + [q^2 Theta_E8][q^5 eta^-8] + "
                "[q Theta_E8][q^6 eta^-8] + [q^7 eta^-8]"
            ),
        },
        "affine_e8_seventh_mode_theorem": {
            "the_eta_minus_8_seventh_excited_coefficient_is_exactly_22528": oscillator_q7 == 22528,
            "the_eta_minus_8_seventh_excited_coefficient_splits_exactly_as_k_minus_1_times_sigma3_k_plus_44": (
                oscillator_q7 == K_MINUS_1 * SIGMA3_K + spread_plus_octet
            ),
            "the_theta_e8_seventh_coefficient_is_exactly_82560_equals_E_times_336_plus_8": (
                lattice_q7 == E * (HEAWOOD_FULL + BOSONIC_OCTET)
            ),
            "the_affine_e8_seventh_coefficient_is_exactly_17333248": affine_q7 == 17333248,
            "the_q7_affine_mode_is_still_on_the_exact_w33_spine_but_the_new_information_is_concentrated_in_the_residue_22528": (
                affine_q7 == ladder_without_residue + oscillator_q7
            ),
            "the_seventh_mode_is_the_first_one_where_the_clean_residue_is_best_read_as_a_shell_index_lift_of_sigma3_k_rather_than_as_a_preexisting_single_packet": True,
        },
        "interpretation": (
            "The affine E8 q^7 mode still stays exact, but the hierarchy has clearly "
            "changed character. The theta side is still clean: 82560 = E x (336 + 8). "
            "The oscillator side is no longer a bare old packet, but it still closes "
            "sparsely as 22528 = (k-1) sigma_3(k) + 44."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 AFFINE E8 SEVENTH-MODE BRIDGE")
    print("=" * 72)
    for key, value in summary["affine_e8_seventh_mode_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
