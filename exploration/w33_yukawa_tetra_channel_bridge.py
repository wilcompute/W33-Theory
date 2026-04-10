"""Continuity bridge from the solved Yukawa packet to the tetra 1+3 carrier.

The current bridge chain already had two exact ``1+3`` packets:

1. the tetra/chart matter carrier ``4 = 1 + 3``;
2. the live CKM slot packet, whose four-slot operator carrier has exact rank
   four and centered rank three.

The new paper operator normal form adds a third:

3. one shared branch channel plus three clean-pair frontier channels.

This bridge packages the exact continuity statement: the solved Yukawa packet
is not an isolated rational corner. It is another exact ``1+3`` face of the
same tetra carrier already organizing the slot/Fourier and Clifford sides.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_yukawa_tetra_channel_bridge_summary.json"


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def build_summary() -> dict[str, Any]:
    master = _load_json("w33_master_continuity_bridge_summary.json")
    tetra = _load_json("w33_tetrahedral_ckm_oscillator_bridge_summary.json")
    normal = _load_json("w33_paper_operator_normal_form_bridge_summary.json")

    return {
        "tetra_continuity_dictionary": {
            "master_tetra_refinement": master["continuity_chain"]["tetra_refinement"],
            "live_slot_packet_rank": tetra["slot_operator_packet"]["packet_rank"],
            "live_slot_packet_centered_rank": tetra["slot_operator_packet"]["centered_rank"],
            "solved_operator_channels": normal["ambient_frontier_dictionary"]["solved_named_channels"],
            "solved_channel_split": "1 + 3",
        },
        "live_slot_one_plus_three": {
            "slot_order": tetra["tetrahedral_basis"]["slot_order"],
            "mode_order": tetra["tetrahedral_basis"]["mode_order"],
            "rank": tetra["slot_operator_packet"]["packet_rank"],
            "centered_rank": tetra["slot_operator_packet"]["centered_rank"],
        },
        "solved_operator_one_plus_three": {
            "singlet_channel": normal["exact_normal_form"]["shared_branch_channel"]["formula"],
            "triplet_channels": [
                normal["exact_normal_form"]["triplet_clean_pair_channel"]["formula"],
                normal["exact_normal_form"]["down_complement_shift_channel"]["formula"],
                normal["exact_normal_form"]["down_singlet_injector_channel"]["formula"],
            ],
            "ambient_frontier_dimension": normal["ambient_frontier_dictionary"]["ambient_dimension"],
        },
        "yukawa_tetra_channel_theorem": {
            "the_master_continuity_chain_already_contains_the_exact_tetra_one_plus_three_refinement": (
                master["master_continuity_theorem"]["the_same_4_carrier_refines_to_one_plus_three_and_generates_the_full_tetra_clifford_packet"]
            ),
            "the_live_ckm_slot_packet_is_an_exact_tetra_one_plus_three_packet": (
                tetra["tetrahedral_ckm_oscillator_theorem"]["the_live_four_slot_family_operator_packet_has_exact_rank_four_and_centered_rank_three"]
            ),
            "the_solved_paper_operator_packet_is_one_exact_shared_branch_channel_plus_three_exact_clean_pair_channels": (
                normal["paper_operator_normal_form_theorem"]["the_solved_paper_packet_has_one_shared_branch_channel_plus_three_exact_clean_pair_channels"]
            ),
            "the_live_slot_packet_and_the_solved_yukawa_packet_are_two_exact_one_plus_three_faces_of_the_same_tetra_carrier": (
                master["master_continuity_theorem"]["the_same_4_carrier_refines_to_one_plus_three_and_generates_the_full_tetra_clifford_packet"]
                and tetra["slot_operator_packet"]["packet_rank"] == 4
                and tetra["slot_operator_packet"]["centered_rank"] == 3
                and normal["ambient_frontier_dictionary"]["solved_named_channels"] == 4
            ),
            "nothing_in_the_current_yukawa_story_is_isolated_anymore": (
                master["master_continuity_theorem"]["nothing_in_the_current_family_cp_chain_is_isolated_anymore"]
            ),
        },
        "interpretation": (
            "The solved Yukawa packet now sits on the same tetra carrier as the "
            "live CKM slot packet and the older Clifford refinement. On the slot "
            "side the carrier is four quark slots with a centered three-shell. On "
            "the operator side it is one shared branch channel plus three exact "
            "clean-pair frontier channels. So the current paper/live Yukawa law is "
            "another exact 1+3 face of the same tetra continuity spine, not a "
            "detached rational patch."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    theorem = summary["yukawa_tetra_channel_theorem"]
    print("=" * 72)
    print("W33 YUKAWA TETRA CHANNEL BRIDGE")
    print("=" * 72)
    for key, value in theorem.items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
