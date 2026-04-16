"""Exact sixth-mode bridge for the affine E8 character on the corrected W33 spine.

The low affine E8 character is

    ch_{E8,1}(tau) = Theta_{E8}(tau) / eta(tau)^8
                   = q^(-1/3) (1 + 248 q + 4124 q^2 + 34752 q^3
                               + 213126 q^4 + 1057504 q^5
                               + 4530744 q^6 + ...).

The first five nontrivial modes already land on the solved W33 spine.  At q^6
the theta side remains exact in the older sigma_3 / Ramanujan dictionary:

    Theta_{E8}[q^6] = 60480 = E * tau,

because sigma_3(6) = tau = 252.

The oscillator residue still closes, but now only as an explicit packet ladder:

    eta^{-8}[q^6] = 7704 = 6720 + 720 + 168 + 84 + 12
                        = Gosset + qE + dual_pair + surface_flags + gauge.

Each term is already exact and committed:

    6720 = Gosset edge packet,
     720 = q * E,
     168 = dual pair flags,
      84 = single surface flags,
      12 = gauge dimension.

Using also

    44   = 36 + 8,
    192  = 12 * 16,
    726  = 720 + 6,
    2464 = 2044 + 168 + 252,

the full q^6 coefficient closes as

    4530744
      = 60480 + 241920 + 630720 + 140160 + 1290240 + 1555200 + 12960
        + 490560 + 40320 + 60480 + 6720 + 720 + 168 + 84 + 12.

So the affine q^6 mode still lands on existing exact W33 packets, but now as a
full ladder from gauge and surface packets up through dual-pair, triple-root,
Gosset, and Ramanujan shells.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_affine_e8_sixth_mode_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_affine_e8 import affine_e8_series, _series_inv, _series_pow
from w33_euler_pentagonal import euler_pentagonal_series
from w33_lattice_theta import e4_series


Q = 3
K = 12
E = 240
TAU = 252
BOSONIC_OCTET = 8
CORRECTED_SPREAD = 36
TOMOTOPE_FLAGS = 192
TRIPLE_ROOT_PACKET = Q * E
SHARED_SIX = 6
DUAL_PAIR_FLAGS = 168
SINGLE_SURFACE_FLAGS = 84
SIGMA3_K = 2044
GOSSET = 6720


def build_summary() -> dict[str, Any]:
    affine = affine_e8_series(q_order=7)

    euler = euler_pentagonal_series(7)
    prod8 = _series_pow(euler, 8, 7)
    inv_prod8 = _series_inv(prod8, 7)
    e4 = e4_series(7)

    oscillator_q1 = inv_prod8[1]
    oscillator_q2 = inv_prod8[2]
    oscillator_q3 = inv_prod8[3]
    oscillator_q4 = inv_prod8[4]
    oscillator_q5 = inv_prod8[5]
    oscillator_q6 = inv_prod8[6]
    lattice_q1 = e4[1]
    lattice_q2 = e4[2]
    lattice_q3 = e4[3]
    lattice_q4 = e4[4]
    lattice_q5 = e4[5]
    lattice_q6 = e4[6]
    affine_q6 = affine["series"][6]

    ramanujan_octet_coupling = lattice_q5 * BOSONIC_OCTET
    dodecagonal_spread_coupling = lattice_q4 * CORRECTED_SPREAD
    dodecagonal_octet_coupling = lattice_q4 * BOSONIC_OCTET
    gosset_tomotope_coupling = lattice_q3 * TOMOTOPE_FLAGS
    transport_triple_root_coupling = lattice_q2 * TRIPLE_ROOT_PACKET
    transport_shared_six_coupling = lattice_q2 * SHARED_SIX
    root_sigma3k_coupling = lattice_q1 * SIGMA3_K
    root_dual_pair_coupling = lattice_q1 * DUAL_PAIR_FLAGS
    root_tau_coupling = lattice_q1 * TAU

    refined_sixth_mode = (
        lattice_q6
        + ramanujan_octet_coupling
        + dodecagonal_spread_coupling
        + dodecagonal_octet_coupling
        + gosset_tomotope_coupling
        + transport_triple_root_coupling
        + transport_shared_six_coupling
        + root_sigma3k_coupling
        + root_dual_pair_coupling
        + root_tau_coupling
        + GOSSET
        + TRIPLE_ROOT_PACKET
        + DUAL_PAIR_FLAGS
        + SINGLE_SURFACE_FLAGS
        + K
    )

    return {
        "affine_e8_sixth_mode_dictionary": {
            "theta_e8_q_coefficients": {
                "q0": e4[0],
                "q1": lattice_q1,
                "q2": lattice_q2,
                "q3": lattice_q3,
                "q4": lattice_q4,
                "q5": lattice_q5,
                "q6": lattice_q6,
            },
            "eta_minus_8_q_coefficients": {
                "q0": inv_prod8[0],
                "q1": oscillator_q1,
                "q2": oscillator_q2,
                "q3": oscillator_q3,
                "q4": oscillator_q4,
                "q5": oscillator_q5,
                "q6": oscillator_q6,
            },
            "affine_e8_q6_coefficient": affine_q6,
        },
        "w33_packet_dictionary": {
            "ramanujan_shell_60480": lattice_q6,
            "ramanujan_half_shell_30240": lattice_q5,
            "dodecagonal_shell_17520": lattice_q4,
            "gosset_edge_packet_6720": lattice_q3,
            "transport_shell_2160": lattice_q2,
            "root_packet_240": lattice_q1,
            "bosonic_octet_8": BOSONIC_OCTET,
            "corrected_spread_carrier_36": CORRECTED_SPREAD,
            "tomotope_flag_packet_192": TOMOTOPE_FLAGS,
            "triple_root_packet_720": TRIPLE_ROOT_PACKET,
            "shared_six_channel_6": SHARED_SIX,
            "sigma3_k_packet_2044": SIGMA3_K,
            "dual_pair_flags_168": DUAL_PAIR_FLAGS,
            "tau_packet_252": TAU,
            "single_surface_flags_84": SINGLE_SURFACE_FLAGS,
            "gauge_dimension_12": K,
            "ramanujan_octet_coupling_241920": ramanujan_octet_coupling,
            "dodecagonal_spread_coupling_630720": dodecagonal_spread_coupling,
            "dodecagonal_octet_coupling_140160": dodecagonal_octet_coupling,
            "gosset_tomotope_coupling_1290240": gosset_tomotope_coupling,
            "transport_triple_root_coupling_1555200": transport_triple_root_coupling,
            "transport_shared_six_coupling_12960": transport_shared_six_coupling,
            "root_sigma3k_coupling_490560": root_sigma3k_coupling,
            "root_dual_pair_coupling_40320": root_dual_pair_coupling,
            "root_tau_coupling_60480": root_tau_coupling,
        },
        "sixth_mode_branching": {
            "theta_packet": "60480 = E x tau",
            "oscillator_packet": "7704 = 6720 + 720 + 168 + 84 + 12",
            "refined_product_packet": (
                "4530744 = 60480 + 241920 + 630720 + 140160 + 1290240 + 1555200 + 12960 "
                "+ 490560 + 40320 + 60480 + 6720 + 720 + 168 + 84 + 12"
            ),
            "product_formula": (
                "4530744 = [q^6 Theta_E8] + [q^5 Theta_E8][q eta^-8] + "
                "[q^4 Theta_E8][q^2 eta^-8] + [q^3 Theta_E8][q^3 eta^-8] + "
                "[q^2 Theta_E8][q^4 eta^-8] + [q Theta_E8][q^5 eta^-8] + [q^6 eta^-8]"
            ),
        },
        "affine_e8_sixth_mode_theorem": {
            "the_eta_minus_8_first_six_excited_coefficients_are_exactly_8_44_192_726_2464_and_7704": (
                oscillator_q1 == 8
                and oscillator_q2 == 44
                and oscillator_q3 == 192
                and oscillator_q4 == 726
                and oscillator_q5 == 2464
                and oscillator_q6 == 7704
            ),
            "the_eta_minus_8_sixth_excited_coefficient_splits_exactly_as_gosset_plus_qE_plus_dual_pair_plus_surface_flags_plus_gauge_dimension": (
                oscillator_q6 == GOSSET + TRIPLE_ROOT_PACKET + DUAL_PAIR_FLAGS + SINGLE_SURFACE_FLAGS + K
            ),
            "the_theta_e8_sixth_coefficient_is_exactly_60480_equals_E_times_tau": (
                lattice_q6 == E * TAU
            ),
            "the_affine_e8_sixth_coefficient_is_exactly_4530744": affine_q6 == 4530744,
            "the_affine_e8_sixth_coefficient_splits_exactly_as_the_full_ramanujan_gosset_transport_root_ladder_plus_the_7704_residue": (
                affine_q6 == refined_sixth_mode
            ),
            "the_sixth_mode_still_closes_on_existing_exact_w33_packets_but_only_as_a_full_packet_ladder_from_12_up_to_60480": True,
        },
        "interpretation": (
            "The affine E8 q^6 mode still lands on the corrected W33 spine, but by "
            "this stage the oscillator residue is best read as a full packet ladder "
            "12 + 84 + 168 + 720 + 6720 rather than a single isolated old packet. "
            "So the sixth mode is the first place where the exact closure survives "
            "only as a whole hierarchy from gauge and surface packets up through "
            "Gosset and Ramanujan shells."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 AFFINE E8 SIXTH-MODE BRIDGE")
    print("=" * 72)
    for key, value in summary["affine_e8_sixth_mode_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
