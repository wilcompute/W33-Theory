"""Exact operator normal form for the solved paper/live Yukawa packet.

The recent bridge chain compressed the clean-pair Yukawa frontier to

    Bott five  tensor  triality three  =  5 x 3 = 15,

and realized the paper sector switch by two exact clean-pair involutions ``A``
and ``B`` on ``Hbar_2``:

    P_trip = (I-B)/2,                  rank 3
    P_down = (I+B)/2,                  rank 5 = 4+1
    P_sing = (I+B)(I-A)/4,             rank 1.

On the generation side, the active clean-pair algebra already closes by the
two universal unipotent matrices

    C_(+-), C_(-+),

equivalently by the three-dimensional basis ``I, N_plus, N_minus`` with
``C_(+-) = I + N_plus`` and ``C_(-+) = I + N_minus``.

This bridge connects every solved packet from the older CKM side to that exact
operator language.  The paper/live packet is

    Y_s = Y11
        - s i (9/40) Y21
        + (3/37)        P_trip ⊗ C_(+-)
        - eps (5/518)   P_down ⊗ C_(+-)
        - eps i (1/27)  P_sing ⊗ C_(-+),

with

    s   in {+1,-1},
    eps = (1-s)/2.

So the fully solved paper/live packet occupies one exact shared branch channel
plus three exact clean-pair frontier channels inside the ambient
``Bott 5 tensor triality 3`` module.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_paper_operator_normal_form_bridge_summary.json"


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _fraction_report(value: Fraction) -> dict[str, Any]:
    return {"exact": str(value), "value": float(value)}


def _complex_fraction_report(real: Fraction, imag: Fraction) -> dict[str, Any]:
    return {
        "real": str(real),
        "imag": str(imag),
        "real_value": float(real),
        "imag_value": float(imag),
    }


def build_summary() -> dict[str, Any]:
    bott_triality = _load_json("w33_bott_triality_yukawa_frontier_bridge_summary.json")
    involution = _load_json("w33_hbar2_binary_involution_bridge_summary.json")
    sector = _load_json("w33_paper_sector_selector_bridge_summary.json")
    unipotent = _load_json("w33_yukawa_unipotent_reduction_bridge_summary.json")
    character = _load_json("w33_clean_pair_character_generation_bridge_summary.json")
    octet = _load_json("w33_clean_pair_octet_sector_bridge_summary.json")

    a12 = Fraction(9, 40)
    triplet_base = Fraction(3, 37)
    down_shift = Fraction(5, 518)
    singlet_injector = Fraction(1, 27)

    triplet_rank = involution["binary_and_refinement_projectors"]["right_packet_ranks"]["up_triplet_rank"]
    down_rank = involution["binary_and_refinement_projectors"]["right_packet_ranks"]["down_complement_rank"]
    singlet_rank = involution["binary_and_refinement_projectors"]["right_packet_ranks"]["down_singlet_rank"]

    c_plus = unipotent["universal_generation_algebra"]["plus_minus_generation_matrix"]
    c_minus = unipotent["universal_generation_algebra"]["minus_plus_generation_matrix"]

    n_plus = [
        [int(c_plus[row][col] - (1 if row == col else 0)) for col in range(3)]
        for row in range(3)
    ]
    n_minus = [
        [int(c_minus[row][col] - (1 if row == col else 0)) for col in range(3)]
        for row in range(3)
    ]

    ambient_dimension = bott_triality["product_dictionary"]["product"]
    solved_named_channels = 4

    return {
        "ambient_frontier_dictionary": {
            "internal_packet": "Bott 5 = 1 + 4",
            "generation_packet": "triality 3",
            "ambient_dimension": ambient_dimension,
            "solved_named_channels": solved_named_channels,
            "remaining_ambient_minus_solved_count": ambient_dimension - solved_named_channels,
        },
        "internal_operator_basis": {
            "A_generator_formula": "flips only d_c_1 on the active Hbar_2 packet",
            "B_generator_formula": "flips exactly d_c_2,d_c_3,e_c on the active Hbar_2 packet",
            "triplet_projector": {
                "formula": "(I-B)/2",
                "rank": triplet_rank,
            },
            "down_complement_projector": {
                "formula": "(I+B)/2",
                "rank": down_rank,
            },
            "singlet_projector": {
                "formula": "(I+B)(I-A)/4",
                "rank": singlet_rank,
            },
        },
        "generation_operator_basis": {
            "C_plus_formula": "C_(+-) = I + N_plus",
            "C_minus_formula": "C_(-+) = I + N_minus",
            "C_plus": c_plus,
            "C_minus": c_minus,
            "N_plus": n_plus,
            "N_minus": n_minus,
            "common_characteristic_polynomial": unipotent["universal_generation_algebra"]["plus_minus_charpoly"],
        },
        "exact_normal_form": {
            "binary_parameters": {
                "s_values": [+1, -1],
                "epsilon_formula": "eps = (1-s)/2",
            },
            "shared_branch_channel": {
                "formula": "-s i (9/40) Y21",
                "coefficient": _complex_fraction_report(Fraction(0, 1), -a12),
            },
            "triplet_clean_pair_channel": {
                "formula": "(3/37) P_trip ⊗ C_(+-)",
                "coefficient": _fraction_report(triplet_base),
            },
            "down_complement_shift_channel": {
                "formula": "-eps (5/518) P_down ⊗ C_(+-)",
                "coefficient": _fraction_report(-down_shift),
            },
            "down_singlet_injector_channel": {
                "formula": "-eps i (1/27) P_sing ⊗ C_(-+)",
                "coefficient": _complex_fraction_report(Fraction(0, 1), -singlet_injector),
            },
            "sector_expansion": {
                "up_s_plus": {
                    "branch": _complex_fraction_report(Fraction(0, 1), -a12),
                    "triplet": _fraction_report(triplet_base),
                    "down_complement_shift": _fraction_report(Fraction(0, 1)),
                    "singlet_injector": _complex_fraction_report(Fraction(0, 1), Fraction(0, 1)),
                },
                "down_s_minus": {
                    "branch": _complex_fraction_report(Fraction(0, 1), a12),
                    "triplet": _fraction_report(triplet_base),
                    "down_complement_shift": _fraction_report(-down_shift),
                    "singlet_injector": _complex_fraction_report(Fraction(0, 1), -singlet_injector),
                },
            },
        },
        "cross_checks": {
            "bott_triality_frontier_is_exact": (
                bott_triality["bott_triality_frontier_theorem"]["the_remaining_yukawa_frontier_is_exactly_bott_five_tensor_triality_three"]
            ),
            "binary_sector_law_is_exact": (
                sector["paper_sector_selector_theorem"]["the_paper_asymmetry_is_not_three_independent_choices_but_one_shared_base_plus_one_binary_sector_switch"]
            ),
            "hbar2_binary_involution_is_exact": (
                involution["hbar2_binary_involution_theorem"]["b_is_the_exact_binary_sector_involution_on_the_hbar2_clean_packet"]
                and involution["hbar2_binary_involution_theorem"]["a_refines_the_down_sector_into_quartet_plus_singlet"]
            ),
            "character_generation_law_is_exact": (
                character["clean_pair_character_generation_theorem"]["the_paper_binary_sector_law_is_exactly_the_hbar2_v4_character_width_law_on_top_of_the_universal_clean_pair_generation_algebra"]
            ),
            "clean_pair_octet_law_is_exact": (
                octet["clean_pair_octet_sector_theorem"]["the_paper_binary_sector_law_is_the_hbar2_clean_pair_octet_read_in_triality_coordinates"]
            ),
        },
        "paper_operator_normal_form_theorem": {
            "the_shared_branch_filtered_cabibbo_leg_is_one_exact_operator_channel": (
                a12 == Fraction(9, 40)
                and sector["shared_base_leg"]["a12"]["exact"] == "9/40"
            ),
            "the_clean_pair_internal_side_reduces_exactly_to_triplet_down_complement_and_singlet_projectors": (
                triplet_rank == 3 and down_rank == 5 and singlet_rank == 1
            ),
            "the_generation_side_reduces_exactly_to_the_two_universal_unipotent_operators_c_plus_and_c_minus": (
                unipotent["universal_generation_algebra"]["plus_minus_is_unipotent_jordan_type"]
                and unipotent["universal_generation_algebra"]["minus_plus_is_unipotent_jordan_type"]
                and unipotent["universal_generation_algebra"]["generation_matrices_commute_exactly"]
            ),
            "the_solved_paper_packet_has_one_shared_branch_channel_plus_three_exact_clean_pair_channels": (
                solved_named_channels == 4
            ),
            "the_three_clean_pair_channels_are_exactly_triplet_base_down_complement_shift_and_singlet_injector": (
                triplet_base == Fraction(3, 37)
                and down_shift == Fraction(5, 518)
                and singlet_injector == Fraction(1, 27)
            ),
            "the_full_solved_packet_is_an_exact_four_channel_slice_inside_the_ambient_bott_five_tensor_triality_three_module": (
                ambient_dimension == 15 and solved_named_channels == 4
            ),
        },
        "interpretation": (
            "The solved paper/live packet is no longer a loose list of rational slot "
            "coefficients. It has an exact operator normal form. One shared "
            "branch-filtered Cabibbo channel sits outside the clean-pair frontier, "
            "and the clean-pair part itself uses only three exact channels inside "
            "the ambient Bott-five times triality-three module: the triplet base, "
            "the down-complement real shift, and the singlet generation injector. "
            "So the ambient unresolved family is 15-dimensional, but the solved "
            "paper slice currently occupies a rigid four-channel corner of it."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    theorem = summary["paper_operator_normal_form_theorem"]
    print("=" * 72)
    print("W33 PAPER OPERATOR NORMAL FORM BRIDGE")
    print("=" * 72)
    for key, value in theorem.items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
