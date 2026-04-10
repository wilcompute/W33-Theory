"""Exact 5x3 packet reduction of the clean-pair Yukawa frontier.

Several previously separate exact bridges now interlock tightly:

1. Seed reconstruction:
   the canonical mixed clean-pair seed is reconstructed from
   - one fixed replicated diagonal backbone, and
   - one reference off-diagonal block twisted by the four V4 characters
     ``I, A, B, AB``.

   So the internal recipe is an exact ``1 + 4 = 5`` packet.

2. Universal generation algebra:
   the two active clean-pair generation matrices ``C_(+-), C_(-+)`` are
   commuting unipotent Jordan operators with the same nilpotent square.  The
   algebra they generate has exact linear rank ``3``.

So the unresolved clean-pair Yukawa frontier is no longer a generic ``24x24``
operator cloud.  It is an exact ``5 x 3`` packet:

    (one backbone + four V4 character twists)
    tensor
    (three-dimensional universal generation algebra).

That compressed frontier packet has size ``15``, matching the old exact W33
``V_15`` / adjoint count.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_yukawa_five_by_three_frontier_bridge_summary.json"


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def build_summary() -> dict[str, Any]:
    seed = _load_json("w33_l6_v4_seed_reconstruction_bridge_summary.json")
    v4 = _load_json("w33_l6_delta27_v4_bridge_summary.json")
    unipotent = _load_json("w33_yukawa_unipotent_reduction_bridge_summary.json")
    involution = _load_json("w33_hbar2_binary_involution_bridge_summary.json")
    complete = _load_json("w33_complete_packet_bridge_summary.json")
    dominant = _load_json("w33_dominant_32_dirac_refinement_bridge_summary.json")

    label_matrix = seed["seed_reconstruction_theorem"]["expected_label_matrix"]
    nonzero_labels = sorted(
        {
            label
            for row in label_matrix
            for label in row
            if label != "0"
        }
    )

    cp = np.array(unipotent["universal_generation_algebra"]["plus_minus_generation_matrix"], dtype=float)
    cm = np.array(unipotent["universal_generation_algebra"]["minus_plus_generation_matrix"], dtype=float)
    eye = np.eye(3, dtype=float)
    np_plus = cp - eye
    np_minus = cm - eye
    generation_basis = {
        "I": eye,
        "N_plus": np_plus,
        "N_minus": np_minus,
    }
    generation_rank = int(np.linalg.matrix_rank(np.stack([m.reshape(-1) for m in generation_basis.values()], axis=1)))

    enlarged_generation_family = {
        "N_plus_squared": np_plus @ np_plus,
        "N_minus_squared": np_minus @ np_minus,
        "N_plus_N_minus": np_plus @ np_minus,
        "N_minus_N_plus": np_minus @ np_plus,
    }
    enlarged_rank = int(
        np.linalg.matrix_rank(
            np.stack(
                [m.reshape(-1) for m in {**generation_basis, **enlarged_generation_family}.values()],
                axis=1,
            )
        )
    )

    internal_recipe_count = 1 + len(nonzero_labels)
    frontier_packet_size = internal_recipe_count * generation_rank

    return {
        "internal_recipe_packet": {
            "fixed_backbone_term": 1,
            "v4_character_orbit_labels": nonzero_labels,
            "v4_character_orbit_size": len(nonzero_labels),
            "internal_recipe_count": internal_recipe_count,
            "label_matrix": label_matrix,
        },
        "generation_algebra_packet": {
            "basis": {name: matrix.tolist() for name, matrix in generation_basis.items()},
            "linear_rank": generation_rank,
            "enlarged_family_rank": enlarged_rank,
            "nilpotent_square_shared_exactly": unipotent["universal_generation_algebra"]["nilpotent_squares_match_exactly"],
            "generation_matrices_commute_exactly": unipotent["universal_generation_algebra"]["generation_matrices_commute_exactly"],
            "characteristic_polynomials": {
                "plus_minus": unipotent["universal_generation_algebra"]["plus_minus_charpoly"],
                "minus_plus": unipotent["universal_generation_algebra"]["minus_plus_charpoly"],
            },
        },
        "frontier_packet_dictionary": {
            "five_times_three_packet": frontier_packet_size,
            "internal_five_is_backbone_plus_v4_orbit": "1 + 4",
            "generation_three_is_universal_clean_pair_algebra": generation_rank,
            "matches_v15_count": frontier_packet_size == 15,
            "complete_packet": complete["complete_packet"],
            "dominant_split": dominant["dirac_dominant_packet"]["split"],
            "hbar2_binary_ranks": involution["binary_and_refinement_projectors"]["right_packet_ranks"],
        },
        "yukawa_five_by_three_frontier_theorem": {
            "the_internal_clean_pair_seed_recipe_is_exactly_one_backbone_plus_four_v4_character_twists": (
                seed["seed_reconstruction_theorem"]["reconstructs_canonical_closure_exactly_for_both_slots"]
                and len(nonzero_labels) == 4
                and internal_recipe_count == 5
            ),
            "the_universal_clean_pair_generation_algebra_has_exact_linear_rank_three": (
                generation_rank == 3 and enlarged_rank == 3
            ),
            "the_generation_algebra_is_already_closed_by_i_nplus_nminus": (
                generation_rank == 3 and enlarged_rank == generation_rank
            ),
            "the_remaining_clean_pair_yukawa_frontier_collapses_to_an_exact_five_by_three_packet": (
                internal_recipe_count == 5 and generation_rank == 3 and frontier_packet_size == 15
            ),
            "the_resulting_frontier_packet_matches_the_exact_w33_v15_count": (
                frontier_packet_size == 15
            ),
        },
        "interpretation": (
            "The remaining Yukawa frontier is now much smaller than the older repo "
            "language suggested. The internal recipe is just one fixed diagonal "
            "backbone plus the four-element V4 orbit of one reference block, while "
            "the universal generation side is already a 3-dimensional unipotent "
            "Jordan algebra. So the live unsolved family is an exact 5x3 packet, "
            "not a generic 24x24 deformation cloud. Numerically that packet has "
            "size 15, which is the old exact V15/adjoint count."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    theorem = summary["yukawa_five_by_three_frontier_theorem"]
    print("=" * 72)
    print("W33 YUKAWA FIVE BY THREE FRONTIER BRIDGE")
    print("=" * 72)
    for key, value in theorem.items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
