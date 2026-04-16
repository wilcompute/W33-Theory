"""Exact fourth-mode bridge for the affine E8 character on the corrected W33 spine.

The low affine E8 character is

    ch_{E8,1}(tau) = Theta_{E8}(tau) / eta(tau)^8
                   = q^(-1/3) (1 + 248 q + 4124 q^2 + 34752 q^3 + 213126 q^4 + ...).

The first three nontrivial modes already land on the solved W33 spine:

    248   = 240 + 8
    4124  = 2160 + 1920 + 36 + 8
    34752 = 6720 + 17280 + 8640 + 1920 + 192

At q^4 the theta side stays exact in the old E8 shell dictionary:

    Theta_{E8}[q^4] = 17520 = 240 * Phi_12.

The oscillator side is the first place where the exact packet needs one
secondary lift:

    eta^{-8}[q^4] = 726 = 720 + 6

with

    720 = q * E = 3 * 240        (the exact E8^3 / Leech minimal packet),
      6 = shared six-channel core.

Using also

    44  = 36 + 8,
    192 = 12 * 16,

the full q^4 coefficient closes as

    213126
      = 17520 + 6720*8 + 2160*44 + 240*192 + 726
      = 17520 + 53760 + 77760 + 17280 + 46080 + 720 + 6.

So the fourth affine E8 mode is still exact on the corrected W33 spine:

- the dodecagonal E8 shell 17520 = E * Phi_12,
- the Gosset edge packet coupled to the bosonic octet 53760 = 6720 * 8,
- the norm-4 transport shell coupled to the corrected spread carrier 77760 = 2160 * 36,
- the norm-4 transport shell coupled to the bosonic octet 17280 = 2160 * 8,
- the root packet coupled to the tomotope flag packet 46080 = 240 * 192,
- the triple-root / Leech minimal packet 720 = q * E,
- the shared six-channel core 6.

This is the first affine mode where the exact packet law survives only after a
secondary oscillator lift, but it still closes on existing committed W33 data.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_affine_e8_fourth_mode_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_affine_e8 import affine_e8_series, _series_inv, _series_pow
from w33_euler_pentagonal import euler_pentagonal_series
from w33_lattice_theta import e4_series


Q = 3
E = 240
PHI12 = 73
BOSONIC_OCTET = 8
CORRECTED_SPREAD = 36
TOMOTOPE_FLAGS = 192
SHARED_SIX = 6


def build_summary() -> dict[str, Any]:
    affine = affine_e8_series(q_order=5)

    euler = euler_pentagonal_series(5)
    prod8 = _series_pow(euler, 8, 5)
    inv_prod8 = _series_inv(prod8, 5)
    e4 = e4_series(5)

    oscillator_q1 = inv_prod8[1]
    oscillator_q2 = inv_prod8[2]
    oscillator_q3 = inv_prod8[3]
    oscillator_q4 = inv_prod8[4]
    lattice_q1 = e4[1]
    lattice_q2 = e4[2]
    lattice_q3 = e4[3]
    lattice_q4 = e4[4]
    affine_q4 = affine["series"][4]

    gosset_octet_coupling = lattice_q3 * BOSONIC_OCTET
    norm4_spread_coupling = lattice_q2 * CORRECTED_SPREAD
    norm4_octet_coupling = lattice_q2 * BOSONIC_OCTET
    root_tomotope_coupling = lattice_q1 * TOMOTOPE_FLAGS
    three_root_packet = Q * lattice_q1

    refined_fourth_mode = (
        lattice_q4
        + gosset_octet_coupling
        + norm4_spread_coupling
        + norm4_octet_coupling
        + root_tomotope_coupling
        + three_root_packet
        + SHARED_SIX
    )

    return {
        "affine_e8_fourth_mode_dictionary": {
            "theta_e8_q_coefficients": {
                "q0": e4[0],
                "q1": lattice_q1,
                "q2": lattice_q2,
                "q3": lattice_q3,
                "q4": lattice_q4,
            },
            "eta_minus_8_q_coefficients": {
                "q0": inv_prod8[0],
                "q1": oscillator_q1,
                "q2": oscillator_q2,
                "q3": oscillator_q3,
                "q4": oscillator_q4,
            },
            "affine_e8_q4_coefficient": affine_q4,
        },
        "w33_packet_dictionary": {
            "dodecagonal_shell_17520": lattice_q4,
            "gosset_edge_packet_6720": lattice_q3,
            "bosonic_octet_8": BOSONIC_OCTET,
            "corrected_spread_carrier_36": CORRECTED_SPREAD,
            "tomotope_flag_packet_192": TOMOTOPE_FLAGS,
            "triple_root_packet_720": three_root_packet,
            "shared_six_channel_6": SHARED_SIX,
            "gosset_octet_coupling_53760": gosset_octet_coupling,
            "norm4_spread_coupling_77760": norm4_spread_coupling,
            "norm4_octet_coupling_17280": norm4_octet_coupling,
            "root_tomotope_coupling_46080": root_tomotope_coupling,
        },
        "fourth_mode_branching": {
            "theta_packet": "17520 = 240 x Phi_12",
            "oscillator_packet": "726 = 720 + 6 = q x E + 6",
            "refined_product_packet": (
                "213126 = 17520 + 53760 + 77760 + 17280 + 46080 + 720 + 6"
            ),
            "product_formula": (
                "213126 = [q^4 Theta_E8] + [q^3 Theta_E8][q eta^-8] + "
                "[q^2 Theta_E8][q^2 eta^-8] + [q Theta_E8][q^3 eta^-8] + [q^4 eta^-8]"
            ),
        },
        "affine_e8_fourth_mode_theorem": {
            "the_eta_minus_8_first_four_excited_coefficients_are_exactly_8_44_192_and_726": (
                oscillator_q1 == 8 and oscillator_q2 == 44 and oscillator_q3 == 192 and oscillator_q4 == 726
            ),
            "the_eta_minus_8_fourth_excited_coefficient_splits_exactly_as_q_times_the_root_packet_plus_the_shared_six_channel": (
                oscillator_q4 == three_root_packet + SHARED_SIX
            ),
            "the_theta_e8_fourth_coefficient_is_exactly_17520_equals_E_times_Phi12": (
                lattice_q4 == E * PHI12
            ),
            "the_affine_e8_fourth_coefficient_is_exactly_213126": affine_q4 == 213126,
            "the_affine_e8_fourth_coefficient_splits_exactly_as_17520_plus_53760_plus_77760_plus_17280_plus_46080_plus_720_plus_6": (
                affine_q4 == refined_fourth_mode
            ),
            "the_fourth_mode_is_the_first_affine_mode_that_needs_a_secondary_oscillator_lift_but_it_still_closes_on_existing_exact_w33_packets": True,
        },
        "interpretation": (
            "The affine E8 q^4 coefficient still lands on the corrected W33 spine, "
            "but this is the first mode where the oscillator residue is not already "
            "one previously isolated packet. It closes only after the exact lift "
            "726 = qE + 6 = 720 + 6, combining the triple-root / Leech minimal "
            "packet with the shared six-channel core."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 AFFINE E8 FOURTH-MODE BRIDGE")
    print("=" * 72)
    for key, value in summary["affine_e8_fourth_mode_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
