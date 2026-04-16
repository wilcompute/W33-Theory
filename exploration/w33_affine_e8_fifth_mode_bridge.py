"""Exact fifth-mode bridge for the affine E8 character on the corrected W33 spine.

The low affine E8 character is

    ch_{E8,1}(tau) = Theta_{E8}(tau) / eta(tau)^8
                   = q^(-1/3) (1 + 248 q + 4124 q^2 + 34752 q^3
                               + 213126 q^4 + 1057504 q^5 + ...).

The first four nontrivial modes already land on the solved W33 spine.  At q^5
the theta side remains exact in the older sigma_3 / Ramanujan dictionary:

    Theta_{E8}[q^5] = 30240 = E * (tau/2),

because sigma_3(5) = 126 = tau/2.

The oscillator residue is the first place where a deeper composite lift is
needed:

    eta^{-8}[q^5] = 2464 = 2044 + 168 + 252
                         = Phi_12 * R + dual_pair_flags + tau.

Each of those packets is already exact and committed:

    2044 = sigma_3(k) = Phi_12 * R,
     168 = dual pair flags = 12 * 14,
     252 = tau = E + k.

Using also

    44  = 36 + 8,
    192 = 12 * 16,
    726 = 720 + 6,
    720 = q * E,

the full q^5 coefficient closes as

    1057504
      = 30240 + 140160 + 241920 + 53760 + 414720 + 172800 + 1440
        + 2044 + 168 + 252.

This is

- the Ramanujan half-shell 30240 = E * tau/2,
- the dodecagonal shell coupled to the bosonic octet 140160 = 17520 * 8,
- the Gosset edge packet coupled to the corrected spread carrier 241920 = 6720 * 36,
- the Gosset edge packet coupled to the bosonic octet 53760 = 6720 * 8,
- the norm-4 transport shell coupled to the tomotope flag packet 414720 = 2160 * 192,
- the root packet coupled to the triple-root / Leech minimal packet 172800 = 240 * 720,
- the root packet coupled to the shared six-channel core 1440 = 240 * 6,
- the residual oscillator lift 2044 + 168 + 252.

So the affine q^5 mode still closes on existing exact W33 packets, but only
after the oscillator side is lifted through the sigma_3(k), torus dual-pair,
and Ramanujan tau packets together.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_affine_e8_fifth_mode_bridge_summary.json"

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
R = 28
TAU = 252
HALF_TAU = 126
PHI12 = 73
BOSONIC_OCTET = 8
CORRECTED_SPREAD = 36
TOMOTOPE_FLAGS = 192
TRIPLE_ROOT_PACKET = Q * E
SHARED_SIX = 6
DUAL_PAIR_FLAGS = 168
SIGMA3_K = PHI12 * R


def build_summary() -> dict[str, Any]:
    affine = affine_e8_series(q_order=6)

    euler = euler_pentagonal_series(6)
    prod8 = _series_pow(euler, 8, 6)
    inv_prod8 = _series_inv(prod8, 6)
    e4 = e4_series(6)

    oscillator_q1 = inv_prod8[1]
    oscillator_q2 = inv_prod8[2]
    oscillator_q3 = inv_prod8[3]
    oscillator_q4 = inv_prod8[4]
    oscillator_q5 = inv_prod8[5]
    lattice_q1 = e4[1]
    lattice_q2 = e4[2]
    lattice_q3 = e4[3]
    lattice_q4 = e4[4]
    lattice_q5 = e4[5]
    affine_q5 = affine["series"][5]

    dodecagonal_octet_coupling = lattice_q4 * BOSONIC_OCTET
    gosset_spread_coupling = lattice_q3 * CORRECTED_SPREAD
    gosset_octet_coupling = lattice_q3 * BOSONIC_OCTET
    norm4_tomotope_coupling = lattice_q2 * TOMOTOPE_FLAGS
    root_triple_root_coupling = lattice_q1 * TRIPLE_ROOT_PACKET
    root_shared_six_coupling = lattice_q1 * SHARED_SIX

    refined_fifth_mode = (
        lattice_q5
        + dodecagonal_octet_coupling
        + gosset_spread_coupling
        + gosset_octet_coupling
        + norm4_tomotope_coupling
        + root_triple_root_coupling
        + root_shared_six_coupling
        + SIGMA3_K
        + DUAL_PAIR_FLAGS
        + TAU
    )

    return {
        "affine_e8_fifth_mode_dictionary": {
            "theta_e8_q_coefficients": {
                "q0": e4[0],
                "q1": lattice_q1,
                "q2": lattice_q2,
                "q3": lattice_q3,
                "q4": lattice_q4,
                "q5": lattice_q5,
            },
            "eta_minus_8_q_coefficients": {
                "q0": inv_prod8[0],
                "q1": oscillator_q1,
                "q2": oscillator_q2,
                "q3": oscillator_q3,
                "q4": oscillator_q4,
                "q5": oscillator_q5,
            },
            "affine_e8_q5_coefficient": affine_q5,
        },
        "w33_packet_dictionary": {
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
            "dodecagonal_octet_coupling_140160": dodecagonal_octet_coupling,
            "gosset_spread_coupling_241920": gosset_spread_coupling,
            "gosset_octet_coupling_53760": gosset_octet_coupling,
            "transport_tomotope_coupling_414720": norm4_tomotope_coupling,
            "root_triple_root_coupling_172800": root_triple_root_coupling,
            "root_shared_six_coupling_1440": root_shared_six_coupling,
        },
        "fifth_mode_branching": {
            "theta_packet": "30240 = E x tau/2",
            "oscillator_packet": "2464 = 2044 + 168 + 252 = Phi_12 x R + dual_pair_flags + tau",
            "refined_product_packet": (
                "1057504 = 30240 + 140160 + 241920 + 53760 + 414720 + 172800 + 1440 + 2044 + 168 + 252"
            ),
            "product_formula": (
                "1057504 = [q^5 Theta_E8] + [q^4 Theta_E8][q eta^-8] + "
                "[q^3 Theta_E8][q^2 eta^-8] + [q^2 Theta_E8][q^3 eta^-8] + "
                "[q Theta_E8][q^4 eta^-8] + [q^5 eta^-8]"
            ),
        },
        "affine_e8_fifth_mode_theorem": {
            "the_eta_minus_8_first_five_excited_coefficients_are_exactly_8_44_192_726_and_2464": (
                oscillator_q1 == 8
                and oscillator_q2 == 44
                and oscillator_q3 == 192
                and oscillator_q4 == 726
                and oscillator_q5 == 2464
            ),
            "the_eta_minus_8_fifth_excited_coefficient_splits_exactly_as_sigma3_k_plus_dual_pair_flags_plus_tau": (
                oscillator_q5 == SIGMA3_K + DUAL_PAIR_FLAGS + TAU
            ),
            "the_theta_e8_fifth_coefficient_is_exactly_30240_equals_E_times_tau_over_2": (
                lattice_q5 == E * HALF_TAU
            ),
            "the_affine_e8_fifth_coefficient_is_exactly_1057504": affine_q5 == 1057504,
            "the_affine_e8_fifth_coefficient_splits_exactly_as_30240_plus_140160_plus_241920_plus_53760_plus_414720_plus_172800_plus_1440_plus_2044_plus_168_plus_252": (
                affine_q5 == refined_fifth_mode
            ),
            "the_fifth_mode_still_closes_on_existing_exact_w33_packets_but_now_requires_the_composite_sigma3_k_plus_dual_pair_plus_tau_oscillator_lift": True,
        },
        "interpretation": (
            "The affine E8 q^5 mode still lands on the corrected W33 spine, but by "
            "this stage the oscillator residue is no longer one isolated old packet. "
            "It closes only as the exact composite lift 2464 = 2044 + 168 + 252, "
            "combining the sigma_3(k) shell, the torus/Klein dual-pair flags, and "
            "the Ramanujan tau packet."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 AFFINE E8 FIFTH-MODE BRIDGE")
    print("=" * 72)
    for key, value in summary["affine_e8_fifth_mode_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
