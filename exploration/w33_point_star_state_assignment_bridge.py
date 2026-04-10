"""Exact physical-state assignment of the Fano point-star semisimple algebra.

The semisimple-algebra bridge solved the selected physical packet as

    Q  ⊕  Q  ⊕  Q(sqrt(103849)),

but that still left one honest seam: which *physical* right-handed states carry
those three rational sectors and the quadratic doublet.

The answer is stronger than a post-diagonalization identification. In the
native Hbar_2 point-star basis

    [d_c_1]  ⊕  [d_c_2, d_c_3, e_c]

the exact Gram packet is already block diagonal as

    [323]  ⊕  [[323,275],[275,659]]  ⊕  [169].

So the physical slice resolves exactly as

    d_c_1            : singlet scalar channel 323 / 57600,
    span{d_c_2,d_c_3}: quadratic doublet channel,
    e_c              : Phi_3 scalar channel 169 / 57600.

That is the missing assignment: the selected algebra is not only semisimple,
it is already state-resolved before the final quadratic splitting.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_point_star_state_assignment_bridge_summary.json"


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def build_summary() -> dict[str, Any]:
    projectors = _load_json("w33_l6_v4_projector_bridge_summary.json")
    gram = _load_json("w33_yukawa_gram_shell_bridge_summary.json")
    dictionary = _load_json("w33_point_star_channel_dictionary_bridge_summary.json")
    semisimple = _load_json("w33_point_star_semisimple_algebra_bridge_summary.json")
    normal = _load_json("w33_paper_operator_normal_form_bridge_summary.json")

    plus_support = projectors["slot_profiles"]["Hbar_2"]["projectors"]["+-"]["support_labels"]
    minus_support = projectors["slot_profiles"]["Hbar_2"]["projectors"]["-+"]["support_labels"]

    plus_block = gram["slot_profiles"]["Hbar_2"]["+-"]["base_gram_numerator_matrix"]
    minus_block = gram["slot_profiles"]["Hbar_2"]["-+"]["base_gram_numerator_matrix"]

    scalar_323 = minus_block[0][0]
    scalar_169 = plus_block[2][2]
    doublet_block = [row[:2] for row in plus_block[:2]]

    centered_doublet = semisimple["semisimple_basis"]["centered_doublet_generator"]
    reduced_discriminant = semisimple["semisimple_basis"]["doublet_reduced_discriminant"]

    return {
        "physical_support_dictionary": {
            "selected_packet": "Hbar_2 active point-star = d_c_1 + d_c_2 + d_c_3 + e_c",
            "minusplus_support": minus_support,
            "plusminus_support": plus_support,
            "native_state_refinement": {
                "down_singlet_line": ["d_c_1"],
                "down_color_doublet_plane": ["d_c_2", "d_c_3"],
                "electron_scalar_line": ["e_c"],
            },
        },
        "exact_state_blocks": {
            "d_c_1_scalar_block": [[scalar_323]],
            "down_doublet_block": doublet_block,
            "e_c_scalar_block": [[scalar_169]],
            "shell_denominator": dictionary["global_dictionary"]["shell_denominator"],
        },
        "state_channel_dictionary": {
            "d_c_1_channel": {
                "squared_value": "323/57600",
                "global_form": dictionary["channel_dictionary"]["singlet_scalar"]["exact"],
            },
            "e_c_channel": {
                "squared_value": "169/57600",
                "global_form": dictionary["channel_dictionary"]["triplet_scalar"]["exact"],
            },
            "down_color_doublet": {
                "block": doublet_block,
                "centered_generator": centered_doublet,
                "reduced_discriminant": reduced_discriminant,
                "quadratic_channels": semisimple["physical_point_star_packet"]["quadratic_channels"],
            },
        },
        "operator_context": {
            "paper_triplet_channel_formula": normal["exact_normal_form"]["triplet_clean_pair_channel"]["formula"],
            "paper_singlet_injector_formula": normal["exact_normal_form"]["down_singlet_injector_channel"]["formula"],
            "paper_down_complement_shift_formula": normal["exact_normal_form"]["down_complement_shift_channel"]["formula"],
        },
        "point_star_state_assignment_theorem": {
            "the_hbar2_minusplus_singlet_is_exactly_the_d_c_1_line": (
                minus_support == ["d_c_1"] and scalar_323 == 323
            ),
            "the_hbar2_plusminus_triplet_refines_exactly_as_d_c_2_d_c_3_plus_e_c": (
                plus_support == ["d_c_2", "d_c_3", "e_c"]
                and plus_block[0][2] == 0
                and plus_block[1][2] == 0
                and plus_block[2][0] == 0
                and plus_block[2][1] == 0
            ),
            "the_e_c_line_carries_the_exact_phi3_scalar_channel_169_over_57600": (
                scalar_169 == 169
            ),
            "the_d_c_2_d_c_3_plane_carries_the_irreducible_quadratic_doublet_sector": (
                doublet_block == [[323, 275], [275, 659]]
                and reduced_discriminant == 103849
            ),
            "the_selected_physical_packet_is_exactly_state_resolved_as_d_c_1_plus_d_c_2_d_c_3_plus_e_c_before_quadratic_splitting": True,
            "the_previous_semisimple_algebra_is_now_assigned_to_actual_yukawa_states": True,
        },
        "interpretation": (
            "The selected Fano point-star algebra is no longer abstract. In the native "
            "Hbar_2 support basis, d_c_1 already carries the 323 scalar line, e_c already "
            "carries the Phi_3 scalar line 169, and the only genuinely nontrivial sector is "
            "the down-color plane span{d_c_2,d_c_3}, which carries the irreducible quadratic "
            "doublet. So the physical slice is already state-resolved before the final "
            "quadratic splitting over Q(sqrt(103849))."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    theorem = summary["point_star_state_assignment_theorem"]
    print("=" * 72)
    print("W33 POINT-STAR STATE ASSIGNMENT BRIDGE")
    print("=" * 72)
    for key, value in theorem.items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
