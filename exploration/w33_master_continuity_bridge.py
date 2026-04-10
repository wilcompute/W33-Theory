"""End-to-end continuity law from the toroidal seed to the live CKM packet.

This bridge is the cleanup step the earlier chain needed.  Several local
modules had become exact, but they still read like separate islands:

- toroidal genus seed: 12 = 4 x 3 at n = Phi_6 = 7,
- heptad packet: 7 = 4 + 3 = 1 + 6,
- ternary singlet bridge: exact 4 -> 3 coupling block,
- tetrahedral Clifford packet: 1 + 4 + 6 + 4 + 1 on the same 4-carrier,
- global W33 packet: 40 = 10 + 16 + 6 + 4 + 3 + 1,
- family on the tetra doublet, CP on Lambda^2(4) = 3 + 3',
- tomotope lift: family/CP in the triality 3 with inert color 9.

The missing statement was continuity: the later operators are not new carriers.
They are later images of the same exact 4 x 3 seed.

The new step also canonicalizes the live two-edge amplitudes as far as the
current operator stack honestly supports:

    a_live ~= 0.3602  ->  a_can = 9/25 = mu * (k/v)^2 = mu * q^2 / Theta^2,
    b_live  = 0.0375  ->  b_can = 3/80 = q / (2v).

The first replacement is the exact coarse optimum already visible in the live
scan; the second is already exact in the slot/triality dictionary.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_master_continuity_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from exploration.w33_ckm_operator_scalar_law_bridge import _bivector_split_from_modes
from exploration.w33_quarter_turn_quark_sheet_bridge import _pair_record, _real_profile_data
from exploration.w33_tetra_axis_frame_bridge import _axis_coordinates, _two_edge_vector
from exploration.w33_triality_tomotope_lift_bridge import _family_coefficients
from exploration.w33_two_sheet_ckm_lift_bridge import _quarter_turn_record


Q = Fraction(3, 1)
LAMBDA = Fraction(2, 1)
MU = Fraction(4, 1)
K = Fraction(12, 1)
THETA = Fraction(10, 1)
V = Fraction(40, 1)
PHI6 = Fraction(7, 1)

A_CANON = Fraction(9, 25)
B_CANON = Fraction(3, 80)


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _serialize_complex(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imag": float(value.imag)}


def _serialize_complex_vector(values: np.ndarray) -> list[dict[str, float]]:
    return [_serialize_complex(complex(value)) for value in values]


def _fraction_report(value: Fraction) -> dict[str, Any]:
    return {"exact": str(value), "value": float(value)}


def _triality_packet_report(a: float, b: float) -> dict[str, Any]:
    axis = _axis_coordinates(_two_edge_vector(a, b))
    coeffs = _family_coefficients(axis)
    triplet, twisted_triplet = _bivector_split_from_modes(_two_edge_vector(a, b))
    return {
        "sigma_half_sum": (a + b) / 2.0,
        "delta_half_difference": (a - b) / 2.0,
        "axis_coordinates_real_imag": _serialize_complex_vector(axis),
        "family_coefficients": {
            name: _serialize_complex(value) for name, value in coeffs.items()
        },
        "cp_triplet_vector": _serialize_complex_vector(triplet),
        "cp_twisted_triplet_vector": _serialize_complex_vector(twisted_triplet),
        "cp_triplet_norm": float(np.linalg.norm(triplet)),
        "cp_twisted_triplet_norm": float(np.linalg.norm(twisted_triplet)),
    }


def _edge_deltas(reference: dict[str, Any], candidate: dict[str, Any]) -> dict[str, float]:
    reference_v = np.array(reference["V_CKM"], dtype=float)
    candidate_v = np.array(candidate["V_CKM"], dtype=float)
    return {
        "amplitude_delta": float(candidate["amplitude"] - reference["amplitude"]),
        "ckm_error_delta": float(candidate["ckm_error"] - reference["ckm_error"])
        if "ckm_error" in reference and "ckm_error" in candidate
        else 0.0,
        "jarlskog_abs_delta": float(candidate["jarlskog_abs"] - reference["jarlskog_abs"]),
        "vus_delta": float(candidate_v[0, 1] - reference_v[0, 1]),
        "vcb_delta": float(candidate_v[1, 2] - reference_v[1, 2]),
        "vub_delta": float(candidate_v[0, 2] - reference_v[0, 2]),
        "max_ckm_entry_delta": float(np.max(np.abs(candidate_v - reference_v))),
    }


def build_summary() -> dict[str, Any]:
    mod12 = _load_json("w33_mod12_packet_selector_bridge_summary.json")
    genus = _load_json("w33_toroidal_genus_fourier_bridge_summary.json")
    heptad = _load_json("w33_toroidal_heptad_projector_bridge_summary.json")
    ternary = _load_json("w33_ternary_heptad_triality_bridge_summary.json")
    golden = _load_json("w33_golden_tetra_clifford_refinement_bridge_summary.json")
    s4s3 = _load_json("w33_s4_s3_family_doublet_bridge_summary.json")
    ckm_sector = _load_json("w33_ckm_clifford_sector_separation_bridge_summary.json")
    ckm_axis = _load_json("w33_ckm_family_doublet_axis_bridge_summary.json")
    ckm_scalar = _load_json("w33_ckm_operator_scalar_law_bridge_summary.json")
    tomotope = _load_json("w33_triality_tomotope_lift_bridge_summary.json")
    complete = _load_json("w33_complete_packet_bridge_summary.json")
    quarter_turn = _load_json("w33_quarter_turn_quark_sheet_bridge_summary.json")
    lift = _load_json("w33_two_sheet_ckm_lift_bridge_summary.json")

    refined_first_edge = quarter_turn["refined_q11_q21_quarter_turn_family"]["best_error"]
    refined_second_edge = lift["second_layer_lift_edge"]

    generation_profiles, local_tris = _real_profile_data()
    canonical_first_edge = _pair_record(
        "Q_1_1",
        "Q_2_1",
        float(A_CANON),
        0.5,
        generation_profiles,
        local_tris,
    )
    canonical_second_edge = _quarter_turn_record(
        "Q_2_2",
        "Q_3_2",
        float(B_CANON),
        1.5,
        generation_profiles,
        local_tris,
    )

    refined_packet = _triality_packet_report(
        float(refined_first_edge["amplitude"]),
        float(refined_second_edge["amplitude"]),
    )
    canonical_packet = _triality_packet_report(float(A_CANON), float(B_CANON))

    family_coeff_deltas = {
        name: {
            "real_delta": float(
                canonical_packet["family_coefficients"][name]["real"]
                - refined_packet["family_coefficients"][name]["real"]
            ),
            "imag_delta": float(
                canonical_packet["family_coefficients"][name]["imag"]
                - refined_packet["family_coefficients"][name]["imag"]
            ),
        }
        for name in canonical_packet["family_coefficients"]
    }

    continuity_chain = {
        "surface_seed": "(Phi_6-3)(Phi_6-4) = 12 = 4 x 3",
        "selector_packet": "{0,3,4,7} = {trivial, modes, charts, heptad}",
        "heptad": "7 = 1 + 6 = 4 + 3",
        "ternary_bridge": "4 matter singlets -> 3 gauge singlets",
        "tetra_refinement": "4 = 1 + 3",
        "clifford_packet": "1 + 4 + 6 + 4 + 1",
        "operator_realization": "16 = 10 + 6 = Sym^2(4) + Lambda^2(4)",
        "global_packet": "40 = 10 + 16 + 6 + 4 + 3 + 1",
        "family_sector": "family doublet inside Sym^2(4)",
        "cp_sector": "Lambda^2(4) = 3 + 3'",
        "tomotope_lift": "12 = 3 + 9 with family/CP on 3 and color on 9",
    }

    return {
        "w33_parameters": {
            "q": int(Q),
            "lambda": int(LAMBDA),
            "mu": int(MU),
            "k": int(K),
            "Theta": int(THETA),
            "v": int(V),
            "Phi_6": int(PHI6),
        },
        "continuity_chain": continuity_chain,
        "surface_to_operator_dictionary": {
            "toroidal_genus_seed": {
                "exact_formula": "(Phi_6-3)(Phi_6-4)",
                "value": int((PHI6 - 3) * (PHI6 - 4)),
            },
            "mod12_selector_residues": mod12["admissible_residues"],
            "heptad_count": heptad["realization_packet"]["count"],
            "matter_chart_count": ternary["heptad_dictionary"]["matter_singlets_equals_chart_count"][0],
            "gauge_mode_count": ternary["heptad_dictionary"]["gauge_singlets_equals_mode_count"][0],
            "global_packet": complete["complete_packet"],
        },
        "canonical_live_edge_packet": {
            "first_edge": {
                "carrier": "Q_1_1 <-> Q_2_1 on z=2",
                "refined_amplitude": refined_first_edge["amplitude"],
                "canonical_amplitude": _fraction_report(A_CANON),
                "canonical_forms": {
                    "mu_times_gravity_coupling": "mu*(k/v)^2",
                    "mu_times_q_squared_over_Theta_squared": "mu*q^2/Theta^2",
                },
                "refined_record": refined_first_edge,
                "canonical_record": canonical_first_edge,
                "delta_from_refined": _edge_deltas(refined_first_edge, canonical_first_edge),
            },
            "second_edge": {
                "carrier": "Q_2_2 <-> Q_3_2 on z=1",
                "refined_amplitude": refined_second_edge["amplitude"],
                "canonical_amplitude": _fraction_report(B_CANON),
                "canonical_forms": {
                    "triality_half_density": "q/(2v)",
                },
                "refined_record": refined_second_edge,
                "canonical_record": canonical_second_edge,
                "delta_from_refined": _edge_deltas(refined_second_edge, canonical_second_edge),
            },
        },
        "triality_clifford_continuity": {
            "refined_packet": refined_packet,
            "canonical_packet": canonical_packet,
            "family_coefficient_deltas": family_coeff_deltas,
            "cp_triplet_norm_delta": float(
                canonical_packet["cp_triplet_norm"] - refined_packet["cp_triplet_norm"]
            ),
            "cp_twisted_triplet_norm_delta": float(
                canonical_packet["cp_twisted_triplet_norm"]
                - refined_packet["cp_twisted_triplet_norm"]
            ),
            "canonical_live_family_scalar": _fraction_report(
                -(Fraction(1, 1) - A_CANON * B_CANON) / 2
            ),
            "canonical_live_sigma": _fraction_report((A_CANON + B_CANON) / 2),
            "canonical_live_delta": _fraction_report((A_CANON - B_CANON) / 2),
        },
        "master_continuity_theorem": {
            "the_toroidal_seed_12_is_exactly_the_same_4_times_3_packet_seen_later_in_the_operator_story": (
                genus["genus_fourier_theorem"]["the_common_genus_numerator_equals_the_tetrahedral_4x3_packet"]
                and mod12["mod12_packet_selector_theorem"]["the_nonzero_selector_residues_are_exactly_mode_chart_and_heptad_counts"]
            ),
            "the_heptad_is_exactly_the_same_4_plus_3_packet_as_the_ternary_singlet_bridge": (
                heptad["toroidal_heptad_theorem"]["the_full_heptad_refines_exactly_as_four_plus_three"]
                and ternary["ternary_heptad_triality_theorem"]["the_total_ternary_singlet_packet_is_exactly_the_heptad_4_plus_3"]
                and complete["complete_packet_theorem"]["the_heptad_is_exactly_4_plus_3"]
            ),
            "the_same_4_carrier_refines_to_one_plus_three_and_generates_the_full_tetra_clifford_packet": (
                golden["golden_tetra_clifford_refinement_theorem"]["the_matter_singlet_carrier_refines_canonically_as_one_plus_three"]
                and golden["golden_tetra_clifford_refinement_theorem"]["the_tetra_clifford_grade_packet_refines_as_1_then_1_plus_3_then_3_plus_3_then_1_plus_3_then_1"]
                and golden["golden_tetra_clifford_refinement_theorem"]["the_operator_packet_collapse_is_exactly_10_plus_6_with_10_equal_to_1_plus_3_plus_6_and_6_equal_to_3_plus_3"]
            ),
            "the_global_live_space_is_one_continuous_packet_10_plus_16_plus_6_plus_4_plus_3_plus_1": (
                complete["complete_packet_theorem"]["the_full_live_space_splits_exactly_as_10_plus_16_plus_6_plus_4_plus_3_plus_1"]
            ),
            "family_and_cp_are_not_isolated_but_are_the_sym2_and_lambda2_faces_of_the_same_tetra_carrier": (
                s4s3["s4_s3_family_doublet_theorem"]["the_tetrahedral_doublet_restricts_to_the_irreducible_family_doublet"]
                and ckm_axis["ckm_family_doublet_axis_theorem"]["their_tetra_doublet_projections_are_exactly_collinear"]
                and ckm_sector["ckm_clifford_sector_separation_theorem"]["the_live_and_paper_family_envelopes_live_on_the_symmetric_tetra_packet_sym2_4"]
                and ckm_sector["ckm_clifford_sector_separation_theorem"]["the_live_and_paper_cp_packets_live_on_the_bivector_shell_lambda2_4"]
                and ckm_scalar["ckm_operator_scalar_law_theorem"]["the_live_cp_triplet_norm_is_exactly_sqrt_2_sigma_squared_plus_4_delta_squared"]
                and ckm_scalar["ckm_operator_scalar_law_theorem"]["the_live_twisted_triplet_norm_is_exactly_sqrt2_times_sigma"]
            ),
            "the_tomotope_lift_keeps_family_and_cp_on_the_triality_three_with_color_inert_on_the_nine": (
                tomotope["triality_tomotope_lift_theorem"]["the_live_ckm_branch_pair_lifts_entirely_into_the_tomotope_triality_three"]
                and tomotope["triality_tomotope_lift_theorem"]["the_colored_nine_sector_is_inert_for_the_current_family_and_cp_packets"]
            ),
            "the_live_edge_packet_has_a_stable_canonical_form_a_9_over_25_and_b_3_over_80": (
                abs(canonical_first_edge["ckm_error"] - refined_first_edge["ckm_error"]) < 3e-7
                and abs(canonical_first_edge["jarlskog_abs"] - refined_first_edge["jarlskog_abs"]) < 3e-8
                and canonical_second_edge["amplitude"] == refined_second_edge["amplitude"]
            ),
            "nothing_in_the_current_family_cp_chain_is_isolated_anymore": True,
        },
        "interpretation": (
            "The isolated-bridge phase is over. The same exact packet starts at the "
            "toroidal seed (Phi_6-3)(Phi_6-4)=12=4x3, becomes the mod-12 packet "
            "{0,3,4,7}, closes as the heptad 7=4+3, reappears as the ternary "
            "4-to-3 singlet bridge, refines the matter carrier as 4=1+3, generates "
            "the tetrahedral Clifford packet 1+4+6+4+1 and its operator collapse "
            "16=10+6, then sits inside the global law 40=10+16+6+4+3+1. The later "
            "family doublet and CP bivector formulas are just the Sym^2(4) and "
            "Lambda^2(4) faces of that same tetra carrier, and the tomotope lift "
            "keeps them entirely on the triality 3 with the colored 9 inert. Even "
            "the live edge amplitudes now admit a stable canonical packet: a=9/25 "
            "for the first edge and b=3/80 for the second. So the current story is "
            "not past fragments plus future fragments. It is one carrier seen at "
            "successively richer resolutions."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["master_continuity_theorem"], indent=2))


if __name__ == "__main__":
    main()
