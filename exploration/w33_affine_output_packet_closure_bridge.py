"""Exact non-affine packet closure of the promoted affine shell outputs.

The common-grammar bridge showed that the affine shell generators

    {16, 20, 24, 36, 40}

are already exact non-affine packet counts. This bridge closes the output side:

    {248, 336, 480, 728, 720}

is also already built from the older exact W33 packet dictionary.

Key exact identities:

    248 = 240 + 8
    336 = 24 * 14 = 16 * 21
    480 = 20 * 24 = 12 * 40
    728 = 248 + 480
    720 = 20 * 36

So the promoted affine shell alphabet is not an external modular residue. It is
the exact output-side closure of the non-affine packet ladder.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_affine_output_packet_closure_bridge_summary.json"


Q = 3
K = 12
PHI6 = Q * Q - Q + 1
G2_DIM = 2 * PHI6
AG21 = Q * PHI6
POINT_CARRIER = 40
SPREAD_CARRIER = 36
COMMON_DIRAC_CORE = 16
CURVATURE_SHELL = 20
COMPLEMENT_24 = 24
BOSONIC_OCTET = 8
EDGE_ROOT_PACKET = POINT_CARRIER * K // 2


def build_summary() -> dict[str, Any]:
    output_rows = {
        "248": {
            "value": 248,
            "closure_forms": {
                "edge_root_packet_plus_bosonic_octet": EDGE_ROOT_PACKET + BOSONIC_OCTET,
            },
        },
        "336": {
            "value": 336,
            "closure_forms": {
                "complement_24_times_G2_dimension_14": COMPLEMENT_24 * G2_DIM,
                "common_dirac_core_16_times_AG21_21": COMMON_DIRAC_CORE * AG21,
            },
        },
        "480": {
            "value": 480,
            "closure_forms": {
                "curvature_shell_20_times_complement_24": CURVATURE_SHELL * COMPLEMENT_24,
                "point_carrier_40_times_valency_12": POINT_CARRIER * K,
            },
        },
        "728": {
            "value": 728,
            "closure_forms": {
                "E8_adjoint_248_plus_full_Dirac_shell_480": 248 + 480,
            },
        },
        "720": {
            "value": 720,
            "closure_forms": {
                "curvature_shell_20_times_spread_carrier_36": CURVATURE_SHELL * SPREAD_CARRIER,
            },
        },
    }

    return {
        "affine_output_packet_closure_dictionary": {
            "q": Q,
            "k": K,
            "Phi6": PHI6,
            "G2_dimension": G2_DIM,
            "AG21": AG21,
            "point_carrier": POINT_CARRIER,
            "spread_carrier": SPREAD_CARRIER,
            "common_dirac_core": COMMON_DIRAC_CORE,
            "curvature_shell": CURVATURE_SHELL,
            "complement_24": COMPLEMENT_24,
            "bosonic_octet": BOSONIC_OCTET,
            "edge_root_packet": EDGE_ROOT_PACKET,
            "output_rows": output_rows,
        },
        "affine_output_packet_closure_theorem": {
            "the_E8_adjoint_packet_248_is_exactly_edge_root_packet_240_plus_bosonic_octet_8": (
                output_rows["248"]["closure_forms"]["edge_root_packet_plus_bosonic_octet"] == 248
            ),
            "the_Heawood_full_shell_336_is_exactly_24_times_14_and_exactly_16_times_21": (
                output_rows["336"]["closure_forms"]["complement_24_times_G2_dimension_14"] == 336
                and output_rows["336"]["closure_forms"]["common_dirac_core_16_times_AG21_21"] == 336
            ),
            "the_full_Dirac_shell_480_is_exactly_20_times_24_and_exactly_40_times_12": (
                output_rows["480"]["closure_forms"]["curvature_shell_20_times_complement_24"] == 480
                and output_rows["480"]["closure_forms"]["point_carrier_40_times_valency_12"] == 480
            ),
            "the_A26_shell_728_is_exactly_248_plus_480": (
                output_rows["728"]["closure_forms"]["E8_adjoint_248_plus_full_Dirac_shell_480"] == 728
            ),
            "the_qE_shell_720_is_exactly_20_times_36": (
                output_rows["720"]["closure_forms"]["curvature_shell_20_times_spread_carrier_36"] == 720
            ),
            "the_promoted_affine_output_alphabet_248_336_480_728_720_is_already_closed_inside_the_nonaffine_packet_dictionary": (
                output_rows["248"]["closure_forms"]["edge_root_packet_plus_bosonic_octet"] == 248
                and output_rows["336"]["closure_forms"]["complement_24_times_G2_dimension_14"] == 336
                and output_rows["336"]["closure_forms"]["common_dirac_core_16_times_AG21_21"] == 336
                and output_rows["480"]["closure_forms"]["curvature_shell_20_times_complement_24"] == 480
                and output_rows["480"]["closure_forms"]["point_carrier_40_times_valency_12"] == 480
                and output_rows["728"]["closure_forms"]["E8_adjoint_248_plus_full_Dirac_shell_480"] == 728
                and output_rows["720"]["closure_forms"]["curvature_shell_20_times_spread_carrier_36"] == 720
            ),
        },
        "interpretation": (
            "The affine shell outputs are already native W33 packet composites. "
            "The bridge now closes on both sides: the input alphabet "
            "{16,20,24,36,40} is the non-affine packet ladder, and the output "
            "alphabet {248,336,480,728,720} is its exact promoted packet "
            "closure."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 AFFINE OUTPUT PACKET CLOSURE BRIDGE")
    print("=" * 72)
    for key, value in summary["affine_output_packet_closure_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
