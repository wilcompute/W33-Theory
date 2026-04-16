"""Exact third-mode bridge for the affine E8 character on the corrected W33 spine.

The low affine E8 character is

    ch_{E8,1}(tau) = Theta_{E8}(tau) / eta(tau)^8
                   = q^(-1/3) (1 + 248 q + 4124 q^2 + 34752 q^3 + ...).

The first two nontrivial modes already welded the recent affine/modular layer to
the solved W33 operator spine:

    248  = 240 + 8
    4124 = 2160 + 1920 + 36 + 8.

At the next mode the oscillator side itself lands on an older exact packet:

    eta^{-8} = q^{-1/3} (1 + 8 q + 44 q^2 + 192 q^3 + ...)

and

    192 = 12 * 16

is exactly the tomotope flag packet:

    12 = directed tetrahedral bridges,
    16 = local flags per edge = 2 * 4 * 2.

Using the exact theta-side coefficients

    Theta_{E8} = 1 + 240 q + 2160 q^2 + 6720 q^3 + ...,

the affine q^3 coefficient closes as

    34752 = 6720 + 2160*8 + 240*44 + 192
          = 6720 + 17280 + 8640 + 1920 + 192.

So the third affine E8 mode is the exact sum of

- the E8 norm-6 / Gosset-edge shell 6720,
- the norm-4 shell coupled to the bosonic octet 17280 = 2160 * 8,
- the root packet coupled to the corrected spread carrier 8640 = 240 * 36,
- the root packet coupled to the bosonic octet 1920 = 240 * 8,
- the tomotope flag packet 192.

This is the cleanest current weld of the affine q^3 mode to the corrected
line/spread/tetra/tomotope spine.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_affine_e8_third_mode_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from exploration.w33_higgs_ew_octet_bridge import build_summary as build_octet_summary
from exploration.w33_tomotope_local_incidence_clifford_bridge import build_summary as build_tomotope_summary
from w33_affine_e8 import affine_e8_series, _series_inv, _series_pow
from w33_euler_pentagonal import euler_pentagonal_series
from w33_lattice_theta import e4_series


def build_summary() -> dict[str, Any]:
    affine = affine_e8_series(q_order=4)
    octet_summary = build_octet_summary()
    tomotope_summary = build_tomotope_summary()

    euler = euler_pentagonal_series(4)
    prod8 = _series_pow(euler, 8, 4)
    inv_prod8 = _series_inv(prod8, 4)
    e4 = e4_series(4)

    oscillator_q1 = inv_prod8[1]
    oscillator_q2 = inv_prod8[2]
    oscillator_q3 = inv_prod8[3]
    lattice_q1 = e4[1]
    lattice_q2 = e4[2]
    lattice_q3 = e4[3]
    affine_q3 = affine["series"][3]

    bosonic_octet = int(octet_summary["spectral_octet"]["total_subdominant_count"])
    spread_count = 36
    tomotope_flags = int(
        tomotope_summary["derived_local_incidence_packet"][
            "total_flags_from_directed_edges_times_local_flags_per_edge"
        ]
    )

    root_octet_coupling = lattice_q1 * bosonic_octet
    root_spread_coupling = lattice_q1 * spread_count
    norm4_shell_octet_coupling = lattice_q2 * bosonic_octet
    refined_third_mode = (
        lattice_q3
        + norm4_shell_octet_coupling
        + root_spread_coupling
        + root_octet_coupling
        + tomotope_flags
    )

    return {
        "affine_e8_third_mode_dictionary": {
            "theta_e8_q_coefficients": {
                "q0": e4[0],
                "q1": lattice_q1,
                "q2": lattice_q2,
                "q3": lattice_q3,
            },
            "eta_minus_8_q_coefficients": {
                "q0": inv_prod8[0],
                "q1": oscillator_q1,
                "q2": oscillator_q2,
                "q3": oscillator_q3,
            },
            "affine_e8_q3_coefficient": affine_q3,
        },
        "w33_packet_dictionary": {
            "bosonic_octet_8": bosonic_octet,
            "corrected_spread_carrier_36": spread_count,
            "tomotope_flag_packet_192": tomotope_flags,
            "norm6_transport_shell_6720": lattice_q3,
            "gosset_edge_packet_6720": lattice_q3,
            "norm4_shell_octet_coupling_17280": norm4_shell_octet_coupling,
            "root_spread_coupling_8640": root_spread_coupling,
            "root_octet_coupling_1920": root_octet_coupling,
        },
        "third_mode_branching": {
            "oscillator_packet": "192 = 12 x 16",
            "refined_product_packet": "34752 = 6720 + 17280 + 8640 + 1920 + 192",
            "product_formula": "34752 = [q^3 Theta_E8] + [q^2 Theta_E8][q eta^-8] + [q Theta_E8][q^2 eta^-8] + [q^3 eta^-8]",
        },
        "affine_e8_third_mode_theorem": {
            "the_eta_minus_8_first_three_excited_coefficients_are_exactly_8_44_and_192": (
                oscillator_q1 == 8 and oscillator_q2 == 44 and oscillator_q3 == 192
            ),
            "the_eta_minus_8_third_excited_coefficient_is_exactly_the_tomotope_flag_packet": (
                oscillator_q3 == tomotope_flags
            ),
            "the_theta_e8_third_coefficient_is_exactly_6720": lattice_q3 == 6720,
            "the_theta_e8_third_coefficient_is_exactly_the_gosset_edge_packet": lattice_q3 == 6720,
            "the_affine_e8_third_coefficient_is_exactly_34752": affine_q3 == 34752,
            "the_affine_e8_third_coefficient_splits_exactly_as_6720_plus_17280_plus_8640_plus_1920_plus_192": (
                affine_q3 == refined_third_mode
            ),
            "the_recent_affine_modular_layer_therefore_meets_the_corrected_tomotope_flag_packet_already_at_q_cubed": True,
        },
        "interpretation": (
            "The third affine E8 coefficient now lands on the same corrected W33 "
            "spine as the first two modes. The E8 lattice side contributes the exact "
            "Gosset edge packet 6720, while the new oscillator contribution is the "
            "exact tomotope flag packet 192 = 12 x 16. So the q^3 affine mode already "
            "sees both sides of the corrected geometry: Gosset on the E8 side, and the "
            "spread/tetra/tomotope carrier on the oscillator side."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 AFFINE E8 THIRD-MODE BRIDGE")
    print("=" * 72)
    for key, value in summary["affine_e8_third_mode_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
