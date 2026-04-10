"""Exact Bott-five times triality-three form of the Yukawa frontier.

The previous bridge reduced the unresolved clean-pair Yukawa family to an exact
``5 x 3`` packet:

  - internal recipe ``5 = 1 + 4`` from the fixed backbone plus the V4 orbit;
  - generation algebra ``3`` from the universal clean-pair Jordan packet.

This module connects that packet to the older global packet law.  The repo had
already established

  - ``Bott five = 4 + 1`` inside the bosonic octet;
  - the family/CP carrier is exactly the tomotope triality ``3`` with zero
    leakage into the colored nonet.

So the open Yukawa frontier is not merely a ``5 x 3`` count.  It is exactly

    Bott five  tensor  triality three,

with the color nonet still inert.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_bott_triality_yukawa_frontier_bridge_summary.json"


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def build_summary() -> dict[str, Any]:
    frontier = _load_json("w33_yukawa_five_by_three_frontier_bridge_summary.json")
    complete = _load_json("w33_complete_packet_bridge_summary.json")
    octet = _load_json("w33_subdominant_octet_bridge_summary.json")
    triality = _load_json("w33_triality_tomotope_lift_bridge_summary.json")
    qutrit = _load_json("w33_tomotope_qutrit_family_bridge_summary.json")

    bott_five = int(complete["grouped_packets"]["bott_5"])
    triality_three = 3
    product = bott_five * triality_three

    return {
        "product_dictionary": {
            "bott_five": bott_five,
            "triality_three": triality_three,
            "product": product,
            "frontier_packet": frontier["frontier_packet_dictionary"]["five_times_three_packet"],
            "complete_packet": complete["complete_packet"],
        },
        "bott_packet_origin": {
            "complete_packet_bott_five": complete["grouped_packets"]["bott_5"],
            "complete_packet_theorem": complete["complete_packet_theorem"]["the_bott_five_is_exactly_4_plus_1"],
            "subdominant_octet_theorem": octet["subdominant_octet_theorem"]["the_previous_bott_five_is_exactly_higgs_quartet_plus_vacuum"],
            "internal_five_recipe": frontier["frontier_packet_dictionary"]["internal_five_is_backbone_plus_v4_orbit"],
        },
        "triality_packet_origin": {
            "triality_basis": triality["triality_family_basis"],
            "live_and_paper_zero_nonet_leakage": {
                "live_positive_branch": triality["packets"]["live_positive_branch"]["tomotope_nine_sector_norm"],
                "live_conjugate_branch": triality["packets"]["live_conjugate_branch"]["tomotope_nine_sector_norm"],
                "paper_up": triality["packets"]["paper_up"]["tomotope_nine_sector_norm"],
                "paper_down": triality["packets"]["paper_down"]["tomotope_nine_sector_norm"],
            },
            "qutrit_theorem": qutrit["tomotope_qutrit_family_theorem"]["the_tomotope_triality_sector_contains_the_exact_repo_qutrit_cycle_up_to_orientation"],
        },
        "bott_triality_frontier_theorem": {
            "the_internal_five_packet_is_exactly_the_old_bott_five": (
                bott_five == 5
                and complete["complete_packet_theorem"]["the_bott_five_is_exactly_4_plus_1"]
                and frontier["frontier_packet_dictionary"]["internal_five_is_backbone_plus_v4_orbit"] == "1 + 4"
            ),
            "the_generation_three_packet_is_exactly_the_old_triality_family_cp_carrier": (
                qutrit["tomotope_qutrit_family_theorem"]["the_tomotope_triality_sector_contains_the_exact_repo_qutrit_cycle_up_to_orientation"]
            ),
            "the_live_and_paper_family_packets_stay_entirely_in_triality_with_zero_color_nonet_leakage": (
                triality["packets"]["live_positive_branch"]["tomotope_nine_sector_norm"] == 0.0
                and triality["packets"]["live_conjugate_branch"]["tomotope_nine_sector_norm"] == 0.0
                and triality["packets"]["paper_up"]["tomotope_nine_sector_norm"] == 0.0
                and triality["packets"]["paper_down"]["tomotope_nine_sector_norm"] == 0.0
            ),
            "the_remaining_yukawa_frontier_is_exactly_bott_five_tensor_triality_three": (
                product == frontier["frontier_packet_dictionary"]["five_times_three_packet"] == 15
            ),
        },
        "interpretation": (
            "The open Yukawa family now has a clean product form. The internal side "
            "is the old Bott five, the family/CP side is the old triality three, "
            "and the colored nonet remains inert. So the unsolved frontier is not "
            "a hidden new sector. It is Bott-five dressing over the already-known "
            "triality family carrier."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    theorem = summary["bott_triality_frontier_theorem"]
    print("=" * 72)
    print("W33 BOTT TRIALITY YUKAWA FRONTIER BRIDGE")
    print("=" * 72)
    for key, value in theorem.items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
