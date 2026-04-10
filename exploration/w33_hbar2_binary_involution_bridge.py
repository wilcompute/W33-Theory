"""Explicit clean-pair binary/refinement involutions on the 162-state carrier.

The paper-sector bridges identified the asymmetric packet with the ``Hbar_2``
clean-pair octet.  This module turns that statement into an actual operator on
the live finite-triple carrier.

For ``Hbar_2``, the exact V4 characters have right-handed ranks

    (++,+-,-+,--) = (4,3,1,0).

Let ``A`` and ``B`` be the two commuting involutions from the V4 bridge.  Then

    P_trip  = (I - B)/2                  because (--)=0,
    P_down  = (I + B)/2 = P_++ + P_-+,
    P_quad  = (I + B)(I + A)/4 = P_++,
    P_sing  = (I + B)(I - A)/4 = P_-+.

So the paper sector law is literally:

  - binary sector switch: ``s = -B`` and ``eps = (I+B)/2``;
  - up/base sector:      ``P_trip`` of width 3;
  - down correction:     ``P_down`` of width 5 = 4+1;
  - down injector:       ``P_sing`` of width 1.

The lift to the live 162-state carrier is exact.  The lifted involutions
commute with ``Gamma``, ``J``, hypercharge, and the weak factor, but not with
the finite Dirac operator and not with non-Cartan color ladders.  So they are
not new gauge symmetries; they are exact internal sector operators at the
Yukawa frontier.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_hbar2_binary_involution_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _right_sign_operator_27(diagonal_signs: list[int]) -> np.ndarray:
    try:
        from exploration.w33_fermionic_connes_sector import right_spinor_basis
    except ModuleNotFoundError:
        from w33_fermionic_connes_sector import right_spinor_basis

    operator = np.eye(27, dtype=float)
    for state, sign in zip(right_spinor_basis(), diagonal_signs):
        operator[state.local_index, state.local_index] = float(sign)
    return operator


def _lift_27_to_81(operator_27: np.ndarray) -> np.ndarray:
    return np.kron(np.eye(3, dtype=float), operator_27)


def _lift_81_to_162(operator_81: np.ndarray) -> np.ndarray:
    zeros = np.zeros_like(operator_81)
    return np.block([[operator_81, zeros], [zeros, operator_81]])


def _commutator_norm(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.linalg.norm(left @ right - right @ left))


def build_summary() -> dict[str, Any]:
    try:
        from exploration.w33_finite_spectral_triple import (
            build_w33_finite_spectral_triple,
            color_factor_operator_27,
            hypercharge_operator_27,
            weak_factor_operator_27,
        )
    except ModuleNotFoundError:
        from w33_finite_spectral_triple import (
            build_w33_finite_spectral_triple,
            color_factor_operator_27,
            hypercharge_operator_27,
            weak_factor_operator_27,
        )

    v4 = _load_json("w33_l6_delta27_v4_bridge_summary.json")
    octet = _load_json("w33_clean_pair_octet_sector_bridge_summary.json")
    character = _load_json("w33_clean_pair_character_generation_bridge_summary.json")
    sector = _load_json("w33_paper_sector_selector_bridge_summary.json")

    profile = v4["slot_profiles"]["Hbar_2"]
    a8 = np.diag(np.array(profile["generator_a"], dtype=float))
    b8 = np.diag(np.array(profile["generator_b"], dtype=float))
    i8 = np.eye(8, dtype=float)
    a27 = _right_sign_operator_27(profile["generator_a"])
    b27 = _right_sign_operator_27(profile["generator_b"])
    i27 = np.eye(27, dtype=float)

    a81 = _lift_27_to_81(a27)
    b81 = _lift_27_to_81(b27)
    a162 = _lift_81_to_162(a81)
    b162 = _lift_81_to_162(b81)

    p_up_8 = (i8 - b8) / 2.0
    p_down_8 = (i8 + b8) / 2.0
    p_quad_8 = (i8 + b8) @ (i8 + a8) / 4.0
    p_sing_8 = (i8 + b8) @ (i8 - a8) / 4.0

    candidate = build_w33_finite_spectral_triple()
    hyper = hypercharge_operator_27()
    weak = weak_factor_operator_27(1 / np.sqrt(2), 1j / np.sqrt(2))
    color_cartan = color_factor_operator_27(np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex))
    color_ladder = color_factor_operator_27(np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex))

    p_up_rank = int(round(np.trace(p_up_8).real))
    p_down_rank = int(round(np.trace(p_down_8).real))
    p_quad_rank = int(round(np.trace(p_quad_8).real))
    p_sing_rank = int(round(np.trace(p_sing_8).real))

    return {
        "hbar2_v4_generators": {
            "A_diagonal": profile["generator_a"],
            "B_diagonal": profile["generator_b"],
            "A_flipped_labels": profile["generator_a_flipped_labels"],
            "B_flipped_labels": profile["generator_b_flipped_labels"],
        },
        "binary_and_refinement_projectors": {
            "up_projector_formula": "(I-B)/2",
            "down_projector_formula": "(I+B)/2",
            "quartet_refinement_formula": "(I+B)(I+A)/4",
            "singlet_refinement_formula": "(I+B)(I-A)/4",
            "right_packet_ranks": {
                "up_triplet_rank": p_up_rank,
                "down_complement_rank": p_down_rank,
                "down_quartet_rank": p_quad_rank,
                "down_singlet_rank": p_sing_rank,
            },
        },
        "paper_dictionary_from_involutions": {
            "binary_sector_sign": "s = -B on the active Hbar_2 packet",
            "binary_selector_eps": "eps = (I+B)/2",
            "up_base_from_triplet_width": octet["paper_sector_from_clean_pair_octet"]["shared_real_base_from_hbar2_triplet"],
            "down_shift_from_down_projector_width": octet["paper_sector_from_clean_pair_octet"]["down_correction_from_hbar2_quartet_plus_singlet"],
            "down_injector_from_singlet_width": octet["paper_sector_from_clean_pair_octet"]["down_only_generation_injector_from_hbar2_singlet"],
            "paper_up_y22": sector["sector_packets"]["up_sector_s_plus"]["y22_coefficient"],
            "paper_down_y22": sector["sector_packets"]["down_sector_s_minus"]["y22_coefficient"],
            "paper_down_y32": sector["sector_packets"]["down_sector_s_minus"]["y32_coefficient"],
        },
        "162_lift_properties": {
            "A162_involution_error": float(np.linalg.norm(a162 @ a162 - np.eye(162))),
            "B162_involution_error": float(np.linalg.norm(b162 @ b162 - np.eye(162))),
            "A162_commutes_with_gamma": _commutator_norm(a162, candidate.grading_162),
            "B162_commutes_with_gamma": _commutator_norm(b162, candidate.grading_162),
            "A162_commutes_with_J": _commutator_norm(a162, candidate.real_structure_162),
            "B162_commutes_with_J": _commutator_norm(b162, candidate.real_structure_162),
            "A27_commutes_with_hypercharge": _commutator_norm(a27, hyper),
            "B27_commutes_with_hypercharge": _commutator_norm(b27, hyper),
            "A27_commutes_with_weak": _commutator_norm(a27, weak),
            "B27_commutes_with_weak": _commutator_norm(b27, weak),
            "A27_commutes_with_color_cartan": _commutator_norm(a27, color_cartan),
            "B27_commutes_with_color_cartan": _commutator_norm(b27, color_cartan),
            "A27_breaks_color_ladder": _commutator_norm(a27, color_ladder),
            "B27_breaks_color_ladder": _commutator_norm(b27, color_ladder),
            "A162_breaks_dirac": _commutator_norm(a162, candidate.dirac_162),
            "B162_breaks_dirac": _commutator_norm(b162, candidate.dirac_162),
        },
        "cross_checks": {
            "clean_pair_octet_bridge_exact": (
                octet["clean_pair_octet_sector_theorem"]["the_paper_binary_sector_law_is_the_hbar2_clean_pair_octet_read_in_triality_coordinates"]
            ),
            "character_generation_bridge_exact": (
                character["clean_pair_character_generation_theorem"]["the_paper_binary_sector_law_is_exactly_the_hbar2_v4_character_width_law_on_top_of_the_universal_clean_pair_generation_algebra"]
            ),
        },
        "hbar2_binary_involution_theorem": {
            "b_is_the_exact_binary_sector_involution_on_the_hbar2_clean_packet": (
                p_up_rank == 3 and p_down_rank == 5
            ),
            "eps_equals_i_plus_b_over_2_is_exactly_the_down_sector_projector": (
                p_down_rank == 5 and p_quad_rank == 4 and p_sing_rank == 1
            ),
            "a_refines_the_down_sector_into_quartet_plus_singlet": (
                p_quad_rank == 4 and p_sing_rank == 1
            ),
            "the_shared_base_down_shift_and_down_injector_are_exactly_the_triplet_five_and_singlet_widths": (
                p_up_rank == 3 and p_down_rank == 5 and p_sing_rank == 1
            ),
            "the_lifted_involutions_are_exact_on_162_and_commute_with_gamma_and_j": (
                np.linalg.norm(a162 @ a162 - np.eye(162)) < 1e-12
                and np.linalg.norm(b162 @ b162 - np.eye(162)) < 1e-12
                and _commutator_norm(a162, candidate.grading_162) < 1e-12
                and _commutator_norm(b162, candidate.grading_162) < 1e-12
                and _commutator_norm(a162, candidate.real_structure_162) < 1e-12
                and _commutator_norm(b162, candidate.real_structure_162) < 1e-12
            ),
            "the_sector_involutions_are_cartan_compatible_but_not_full_gauge_symmetries_and_not_dirac_symmetries": (
                _commutator_norm(a27, hyper) < 1e-12
                and _commutator_norm(b27, hyper) < 1e-12
                and _commutator_norm(a27, weak) < 1e-12
                and _commutator_norm(b27, weak) < 1e-12
                and _commutator_norm(a27, color_cartan) < 1e-12
                and _commutator_norm(b27, color_cartan) < 1e-12
                and _commutator_norm(a27, color_ladder) > 1.0
                and _commutator_norm(b27, color_ladder) > 1.0
                and _commutator_norm(a162, candidate.dirac_162) > 1.0
                and _commutator_norm(b162, candidate.dirac_162) > 1.0
            ),
        },
        "interpretation": (
            "The paper binary selector is now an actual operator on the live finite "
            "carrier. The clean Hbar_2 packet comes with one exact binary involution "
            "B and one exact refinement involution A. B alone splits the packet into "
            "the shared triplet 3 and the down complement 4+1, so s=-B and "
            "eps=(I+B)/2 reproduce the paper sector switch. A then resolves the down "
            "complement into the quartet 4 and singlet 1, isolating the 1/q^3 "
            "injector. Lifted to 162, these involutions preserve reality and chirality "
            "and the Cartan/backbone data, but they do not preserve the finite Dirac "
            "operator or the full color ladder. So they live exactly where they "
            "should: at the Yukawa frontier between the solved gauge backbone and the "
            "unsolved mass spectrum."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    theorem = summary["hbar2_binary_involution_theorem"]
    print("=" * 72)
    print("W33 HBAR2 BINARY INVOLUTION BRIDGE")
    print("=" * 72)
    for key, value in theorem.items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
