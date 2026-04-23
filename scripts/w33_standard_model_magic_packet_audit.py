#!/usr/bin/env python3
"""Exact universality scaffold / magic-packet audit for the W33 Standard Model stack.

This audit packages the strongest computation-theoretic statement that the
tracked exact repo can currently support.

Exact finite architecture already present:
1. Qutrit Clifford processor:
   - W(3,3) is exactly the projective two-qutrit Pauli commutation geometry.
   - The exact symplectic generator set preserves that geometry.
   - The local carrier is the exact H27 = 3^3 shell.

2. Tetrahedral control / transport bus:
   - The 4-slot CKM/chart packet is the tetrahedron vertex packet.
   - The 3-state transport packet is the axis-side qutrit.
   - The global transport bundle is exactly 135 = 45 * 3, with a 45 + 90
     radial/tangential split.

3. Qutrit generation memory:
   - The reduced Yukawa generation algebra collapses modulo 3 to the regular
     C3 module.
   - Over C, the same packet splits into the qutrit eigencharacters
     1, omega, omega^2.

4. Minimal exact non-Clifford frontier:
   - The residual signed Yukawa packet is exactly two irreducible D4 quartic
     lifts.
   - Their quadratic subfield packets are disjoint.
   - The root fields and splitting fields are linearly disjoint, with
     splitting-field Galois group D4 x D4.

Conservative computational reading:
  the exact repo already gives a qutrit Clifford processor, a tetrahedral
  control bus, and a qutrit generation memory, while the non-Clifford content
  has collapsed to a minimal two-slot quartic magic candidate. What remains
  open is explicit injection / synthesis from that packet, not localization of
  where universality must enter.

Primary literature anchors for the interpretation layer:
  - Nayak, Simon, Stern, Freedman, Das Sarma (2008):
      https://arxiv.org/abs/0707.1889
  - Anwar, Campbell, Browne (2012), qutrit magic-state distillation:
      https://arxiv.org/abs/1202.2326
  - Campbell, Anwar, Browne (2012), prime-d qudit Reed-Muller:
      https://arxiv.org/abs/1205.3104
  - Howard, Vala (2012), qudit pi/8 gates:
      https://arxiv.org/abs/1206.1598
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys
import time
from typing import Any, Dict, Tuple


ROOT = Path(__file__).resolve().parents[1]
EXPLORATION = ROOT / "exploration"
SCRIPTS = ROOT / "scripts"
for candidate in (ROOT, EXPLORATION, SCRIPTS):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    from exploration.w33_qutrit_foundation_bridge import build_summary as build_qutrit_foundation_summary  # noqa: E402
except ModuleNotFoundError:
    from w33_qutrit_foundation_bridge import build_summary as build_qutrit_foundation_summary  # noqa: E402

try:
    from exploration.w33_standard_model_action_backbone_bridge import (  # noqa: E402
        build_standard_model_action_backbone_summary,
    )
except ModuleNotFoundError:
    from w33_standard_model_action_backbone_bridge import build_standard_model_action_backbone_summary  # noqa: E402

try:
    from exploration.w33_universal_tetra_qutrit_bridge import build_summary as build_universal_tetra_qutrit_summary  # noqa: E402
except ModuleNotFoundError:
    from w33_universal_tetra_qutrit_bridge import build_summary as build_universal_tetra_qutrit_summary  # noqa: E402

try:
    from exploration.w33_yukawa_qutrit_collapse_bridge import build_yukawa_qutrit_collapse_summary  # noqa: E402
except ModuleNotFoundError:
    from w33_yukawa_qutrit_collapse_bridge import build_yukawa_qutrit_collapse_summary  # noqa: E402

from scripts.w33_qutrit_operator_algebra import analyze as analyze_qutrit_operator_layer  # noqa: E402
from scripts.w33_yukawa_quartic_lift_audit import analyze as analyze_yukawa_quartic_lift  # noqa: E402


REFERENCE_LITERATURE = {
    "tqc_review": "https://arxiv.org/abs/0707.1889",
    "qutrit_magic_state_distillation": "https://arxiv.org/abs/1202.2326",
    "prime_dimension_reed_muller_magic": "https://arxiv.org/abs/1205.3104",
    "qudit_pi_over_eight_gate": "https://arxiv.org/abs/1206.1598",
}


@lru_cache(maxsize=1)
def qutrit_clifford_processor_summary() -> Dict[str, Any]:
    foundation = build_qutrit_foundation_summary()
    operator = analyze_qutrit_operator_layer()
    shell = foundation["qutrit_foundation_dictionary"]["local_shell_rows"][0]
    canonical_h = operator["canonical_hamiltonian"]

    return {
        "w33_vertex_count": foundation["qutrit_foundation_dictionary"]["n_vertices"],
        "w33_edge_count": foundation["qutrit_foundation_dictionary"]["n_edges"],
        "projective_pauli_point_count": operator["exact_pauli_algebra"]["projective_point_count"],
        "weyl_basis_size": operator["exact_pauli_algebra"]["weyl_basis_size"],
        "identity_isomorphism_holds": operator["exact_pauli_algebra"]["identity_isomorphism_holds"],
        "product_law_holds": operator["exact_pauli_algebra"]["product_law_holds"],
        "commutator_phase_matches_symplectic": operator["exact_pauli_algebra"][
            "commutator_phase_matches_symplectic"
        ],
        "all_symplectic_generators_verified": operator["symplectic_action"]["all_generators_verified"],
        "local_neighbor_count": shell["N12_size"],
        "local_h27_size": shell["H27_size"],
        "local_triangle_sizes": tuple(shell["triangle_sizes"]),
        "local_fiber_sizes": tuple(shell["fiber_sizes"]),
        "inter_fiber_counts": tuple(shell["inter_fiber_counts"]),
        "h27_internal_triangle_count": shell["h27_triangle_count"],
        "canonical_hamiltonian_spectrum": canonical_h["laplacian_eigenpairs"],
    }


@lru_cache(maxsize=1)
def tetra_qutrit_bus_summary() -> Dict[str, Any]:
    summary = build_universal_tetra_qutrit_summary()
    axis = summary["tetra_axis_symmetry"]
    qutrit = summary["qutrit_identification"]
    bundle = summary["transport_bundle_dictionary"]
    theorem = summary["universal_tetra_qutrit_theorem"]

    return {
        "axis_group_order": axis["induced_axis_group_order"],
        "axis_group_is_exact_s3": axis["axis_group_is_exact_s3"],
        "representative_transport_three_cycle": tuple(qutrit["representative_transport_three_cycle"]),
        "transport_three_cycle_equals_repo_qutrit_cycle": qutrit[
            "representative_transport_three_cycle_equals_repo_qutrit_cycle"
        ],
        "transport_three_cycle_inverse_equals_repo_qutrit_cycle": qutrit[
            "representative_transport_three_cycle_inverse_equals_repo_qutrit_cycle"
        ],
        "transport_cycle_diagonalizes_to_qutrit_packet_up_to_orientation": qutrit[
            "transport_cycle_diagonalizes_to_qutrit_packet_up_to_orientation"
        ],
        "local_axis_packet_dimension": bundle["local_axis_packet_dimension"],
        "real_decomposition": (
            bundle["real_decomposition"]["radial"],
            bundle["real_decomposition"]["tangential"],
        ),
        "global_bundle_dimension": bundle["global_bundle_dimension"],
        "global_radial_dimension": bundle["global_radial_dimension"],
        "global_tangential_dimension": bundle["global_tangential_dimension"],
        "all_six_axis_permutations_occur_on_transport_edges": bundle[
            "all_six_axis_permutations_occur_on_transport_edges"
        ],
        "vertex_four_packet_is_same_tetrahedron": theorem[
            "the_ckm_chart_four_packet_is_the_vertex_side_of_one_universal_tetrahedron"
        ],
        "axis_three_packet_is_same_tetrahedron": theorem[
            "the_transport_local_three_packet_is_the_axis_side_of_the_same_tetrahedron"
        ],
        "axis_packet_is_real_shadow_of_qutrit_triality": theorem[
            "the_axis_packet_is_exactly_the_real_shadow_one_plus_two_of_the_qutrit_triality_carrier"
        ],
        "transport_135_is_45_times_3": theorem[
            "the_transport_135_bundle_is_45_copies_of_the_tetra_axis_qutrit"
        ],
        "transport_90_is_45_times_2": theorem[
            "the_transport_90_sector_is_45_copies_of_the_tangential_qutrit_shell"
        ],
    }


@lru_cache(maxsize=1)
def qutrit_generation_memory_summary() -> Dict[str, Any]:
    summary = build_yukawa_qutrit_collapse_summary()
    theorem = summary["qutrit_collapse_theorem"]
    flag = summary["mod3_flag_identification"]

    return {
        "generation_reduces_to_one_c3_mod3": theorem[
            "universal_generation_algebra_reduces_to_one_c3_mod3"
        ],
        "generation_module_is_regular_c3_module": theorem[
            "mod3_generation_module_is_regular_c3_module"
        ],
        "repo_common_flag_matches_regular_module_loewy_flag": theorem[
            "repo_common_flag_matches_loewy_flag_of_regular_module"
        ],
        "complex_regular_module_splits_as_qutrit_packet": theorem[
            "complex_regular_module_splits_as_qutrit_packet"
        ],
        "repo_line_generator": tuple(flag["repo_line_generator"]),
        "line_in_cycle_basis": tuple(flag["line_in_cycle_basis"]),
        "plane_in_cycle_basis": tuple(tuple(row) for row in flag["plane_in_cycle_basis"]),
        "line_maps_to_fixed_line": flag["line_maps_to_fixed_line"],
        "plane_maps_to_augmentation_plane": flag["plane_maps_to_augmentation_plane"],
        "fixed_line_equals_kernel_of_cycle_minus_identity": flag[
            "fixed_line_equals_kernel_of_cycle_minus_identity"
        ],
        "augmentation_plane_equals_image_of_cycle_minus_identity": flag[
            "augmentation_plane_equals_image_of_cycle_minus_identity"
        ],
    }


@lru_cache(maxsize=1)
def exact_magic_packet_summary() -> Dict[str, Any]:
    summary = analyze_yukawa_quartic_lift()
    packet = summary["quartic_lift_packet"]
    theorem = summary["quartic_lift_theorem"]
    relation = summary["quartic_pair_relation"]
    root_fields = summary["quartic_root_field_relation"]
    splitting_fields = summary["quartic_splitting_field_relation"]
    records = packet["records"]

    return {
        "packet_size": packet["packet_size"],
        "scaled_signed_variable": packet["scaled_signed_variable"],
        "scaled_squared_variable": packet["scaled_squared_variable"],
        "h2_quartic_polynomial": records["H_2:-+"]["quartic_polynomial"],
        "hbar2_quartic_polynomial": records["Hbar_2:+-"]["quartic_polynomial"],
        "h2_galois_group_label": records["H_2:-+"]["galois_group_label"],
        "h2_galois_group_order": records["H_2:-+"]["galois_group_order"],
        "hbar2_galois_group_label": records["Hbar_2:+-"]["galois_group_label"],
        "hbar2_galois_group_order": records["Hbar_2:+-"]["galois_group_order"],
        "shared_quadratic_subfield_squarefree_parts": tuple(
            relation["shared_quadratic_subfield_squarefree_parts"]
        ),
        "quartic_root_fields_are_linearly_disjoint_over_q": root_fields["relation_theorem"][
            "quartic_root_fields_are_linearly_disjoint_over_q"
        ],
        "quartic_root_field_compositum_degree": root_fields["compositum_degree"],
        "d4_splitting_fields_are_linearly_disjoint_over_q": splitting_fields["relation_theorem"][
            "d4_splitting_fields_are_linearly_disjoint_over_q"
        ],
        "quartic_splitting_field_compositum_degree": splitting_fields["compositum_degree"],
        "quartic_splitting_field_galois_group": splitting_fields["compositum_galois_group"],
        "remaining_signed_yukawa_packet_is_two_d4_quartic_lifts": theorem[
            "remaining_signed_yukawa_packet_is_two_d4_quartic_lifts"
        ],
    }


@lru_cache(maxsize=1)
def standard_model_backbone_summary() -> Dict[str, Any]:
    summary = build_standard_model_action_backbone_summary()
    bosonic = summary["bosonic_action_backbone"]
    fermions = summary["fermion_representation_backbone"]
    mixing = summary["mixing_backbone"]
    anomaly = summary["anomaly_backbone"]
    frontier = summary["frontier_boundary"]

    return {
        "bosonic_action_fixed": bosonic["full_bosonic_action_fixed"],
        "fermion_representation_dimension": fermions["one_generation_spinor_dimension"],
        "three_generation_matter_dimension": fermions["three_generation_matter_dimension"],
        "decomposition_16_equals_6_3_3_2_1_1": fermions["decomposition_16_equals_6_3_3_2_1_1"],
        "mixing_tan_theta_c": mixing["tan_theta_c"]["exact"],
        "exact_pmns_12": mixing["sin2_theta_12"]["exact"],
        "exact_pmns_23": mixing["sin2_theta_23"]["exact"],
        "exact_pmns_13": mixing["sin2_theta_13"]["exact"],
        "all_anomalies_cancel": anomaly["all_anomalies_cancel"],
        "full_yukawa_eigenvalue_spectrum_still_open": frontier["full_yukawa_eigenvalue_spectrum_still_open"],
    }


@lru_cache(maxsize=1)
def classify_standard_model_magic_packet() -> Tuple[Dict[str, Any], ...]:
    processor = qutrit_clifford_processor_summary()
    bus = tetra_qutrit_bus_summary()
    memory = qutrit_generation_memory_summary()
    magic = exact_magic_packet_summary()
    sm = standard_model_backbone_summary()

    return (
        {
            "name": "qutrit_clifford_processor",
            "support_level": "repo-exact processor layer",
            "statement": (
                "The exact finite processor is already present: two-qutrit Pauli geometry, "
                "verified symplectic/Clifford generators, canonical Hamiltonian, and the "
                "exact H27 = 3^3 local carrier."
            ),
            "evidence": processor,
        },
        {
            "name": "tetra_qutrit_control_transport_bus",
            "support_level": "repo-exact control layer",
            "statement": (
                "The exact control/transport side closes as one tetra-qutrit bus: a "
                "4-slot vertex packet acting on a 3-state qutrit axis packet across the "
                "global 135 = 45 * 3 transport bundle."
            ),
            "evidence": bus,
        },
        {
            "name": "qutrit_generation_memory",
            "support_level": "repo-exact generation layer",
            "statement": (
                "The reduced Yukawa generation algebra is exactly the regular C3 module "
                "modulo 3 and splits as a qutrit packet over C, so the generation carrier "
                "is already ternary in the precise representation-theoretic sense."
            ),
            "evidence": memory,
        },
        {
            "name": "minimal_magic_packet_candidate",
            "support_level": "repo-exact non-Clifford frontier localization",
            "statement": (
                "The remaining signed Yukawa content has already collapsed to a minimal "
                "two-slot quartic packet: two irreducible D4 lifts with disjoint quadratic "
                "subfield packets and linearly disjoint root/splitting fields."
            ),
            "evidence": magic,
        },
        {
            "name": "honest_universality_boundary",
            "support_level": "exact architecture with open synthesis step",
            "statement": (
                "The exact repo therefore already fixes the processor, the control bus, "
                "and the ternary generation memory. What remains open is explicit "
                "non-Clifford injection/synthesis from the quartic magic packet, not the "
                "location of the universal-computation frontier itself."
            ),
            "evidence": {
                "bosonic_action_fixed": sm["bosonic_action_fixed"],
                "all_anomalies_cancel": sm["all_anomalies_cancel"],
                "full_yukawa_eigenvalue_spectrum_still_open": sm[
                    "full_yukawa_eigenvalue_spectrum_still_open"
                ],
                "remaining_signed_yukawa_packet_is_two_d4_quartic_lifts": magic[
                    "remaining_signed_yukawa_packet_is_two_d4_quartic_lifts"
                ],
            },
        },
    )


@lru_cache(maxsize=1)
def analyze() -> Dict[str, Any]:
    processor = qutrit_clifford_processor_summary()
    bus = tetra_qutrit_bus_summary()
    memory = qutrit_generation_memory_summary()
    magic = exact_magic_packet_summary()
    sm = standard_model_backbone_summary()
    records = classify_standard_model_magic_packet()

    theorem = {
        "the_exact_repo_already_contains_a_qutrit_clifford_processor": (
            processor["w33_vertex_count"] == 40
            and processor["w33_edge_count"] == 240
            and processor["projective_pauli_point_count"] == 40
            and processor["weyl_basis_size"] == 81
            and processor["identity_isomorphism_holds"] is True
            and processor["product_law_holds"] is True
            and processor["commutator_phase_matches_symplectic"] is True
            and processor["all_symplectic_generators_verified"] is True
            and processor["local_h27_size"] == 27
        ),
        "the_exact_repo_already_contains_a_tetra_qutrit_control_transport_bus": (
            bus["axis_group_order"] == 6
            and bus["axis_group_is_exact_s3"] is True
            and (
                bus["transport_three_cycle_equals_repo_qutrit_cycle"] is True
                or bus["transport_three_cycle_inverse_equals_repo_qutrit_cycle"] is True
            )
            and bus["transport_cycle_diagonalizes_to_qutrit_packet_up_to_orientation"] is True
            and bus["local_axis_packet_dimension"] == 3
            and bus["real_decomposition"] == (1, 2)
            and bus["global_bundle_dimension"] == 135
            and bus["global_radial_dimension"] == 45
            and bus["global_tangential_dimension"] == 90
            and bus["all_six_axis_permutations_occur_on_transport_edges"] is True
        ),
        "the_generation_algebra_is_already_an_exact_qutrit_memory_packet": (
            memory["generation_reduces_to_one_c3_mod3"] is True
            and memory["generation_module_is_regular_c3_module"] is True
            and memory["repo_common_flag_matches_regular_module_loewy_flag"] is True
            and memory["complex_regular_module_splits_as_qutrit_packet"] is True
            and memory["line_maps_to_fixed_line"] is True
            and memory["plane_maps_to_augmentation_plane"] is True
        ),
        "the_exact_nonclifford_frontier_has_collapsed_to_a_two_slot_quartic_magic_packet": (
            magic["packet_size"] == 2
            and magic["h2_quartic_polynomial"] == "x**4 - 542*x**2 + 61200"
            and magic["hbar2_quartic_polynomial"] == "x**4 - 982*x**2 + 137232"
            and magic["h2_galois_group_label"] == "D4"
            and magic["h2_galois_group_order"] == 8
            and magic["hbar2_galois_group_label"] == "D4"
            and magic["hbar2_galois_group_order"] == 8
            and magic["shared_quadratic_subfield_squarefree_parts"] == ()
            and magic["quartic_root_fields_are_linearly_disjoint_over_q"] is True
            and magic["quartic_root_field_compositum_degree"] == 16
            and magic["d4_splitting_fields_are_linearly_disjoint_over_q"] is True
            and magic["quartic_splitting_field_compositum_degree"] == 64
            and magic["quartic_splitting_field_galois_group"] == "D4 x D4"
            and magic["remaining_signed_yukawa_packet_is_two_d4_quartic_lifts"] is True
        ),
        "the_current_exact_universality_read_is_clifford_processor_plus_minimal_magic_packet_not_yet_explicit_injection": (
            sm["bosonic_action_fixed"] is True
            and sm["fermion_representation_dimension"] == 16
            and sm["three_generation_matter_dimension"] == 48
            and sm["decomposition_16_equals_6_3_3_2_1_1"] is True
            and sm["all_anomalies_cancel"] is True
            and sm["full_yukawa_eigenvalue_spectrum_still_open"] is True
            and magic["remaining_signed_yukawa_packet_is_two_d4_quartic_lifts"] is True
        ),
    }

    return {
        "status": "ok",
        "reference_literature": REFERENCE_LITERATURE,
        "qutrit_clifford_processor": processor,
        "tetra_qutrit_bus": bus,
        "qutrit_generation_memory": memory,
        "exact_magic_packet": magic,
        "standard_model_backbone": sm,
        "record_details": records,
        "standard_model_magic_packet_theorem": theorem,
        "bridge_verdict": (
            "The deeper exact computation-theoretic read is now sharper than a generic "
            "TQC analogy. The repo already contains a qutrit Clifford processor, a "
            "tetrahedral control/transport bus, and a qutrit generation memory. The "
            "remaining non-Clifford content is no longer a diffuse phenomenology layer: "
            "it has collapsed to a minimal two-slot quartic packet of linearly disjoint "
            "D4 lifts. So the exact Standard Model universality frontier is best read as "
            "Clifford processor plus minimal magic packet, with explicit state injection / "
            "gate synthesis still open."
        ),
    }


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXXII_standard_model_magic_packet_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("Standard Model magic-packet audit")
    for key, value in payload["standard_model_magic_packet_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")
    print(f"  Wrote: {output_path}")


if __name__ == "__main__":
    main()
