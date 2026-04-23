#!/usr/bin/env python3
"""Conservative TQC / universality boundary for the exact W33 Standard Model spine.

This audit packages the strongest computation-theoretic statement that the
current exact repo can support without overclaiming a full braid-universal
topological quantum computer:

1. Exact stabilizer / Clifford backbone:
   - W(3,3) is exactly the projective two-qutrit Pauli commutation geometry.
   - The projective symplectic generators preserve that geometry.
   - The local shell already contains an exact 27 = 3^3 Heisenberg carrier.

2. Exact tetra-qutrit control / transport primitive:
   - The 4-slot CKM/chart packet is the vertex side of one tetrahedron.
   - The 3-state transport packet is the axis side of that same tetrahedron.
   - The 135 = 45 * 3 transport bundle is 45 copies of the same qutrit axis
     primitive, with a 45 + 90 = 45 * (1 + 2) decomposition.

3. Conservative computational reading:
   - The exact Standard Model backbone already fixes the Clifford/stabilizer
     side (gauge, kinematics, exact mixing backbone, anomaly cancellation).
   - The full Yukawa eigenvalue spectrum remains open.
   - So the honest universality read is not "braiding universality is solved,"
     but "the repo now has an exact qutrit Clifford processor with an exact
     tetrahedral control/transport primitive, while the non-Clifford Yukawa
     resource required for full universality remains the live frontier."

Primary literature anchors for the interpretation layer:
  - Nayak, Simon, Stern, Freedman, Das Sarma (2008):
      https://arxiv.org/abs/0707.1889
  - Anwar, Campbell, Browne (2012), qutrit magic-state distillation:
      https://arxiv.org/abs/1202.2326
  - Campbell, Anwar, Browne (2012), prime-d qudit Reed-Muller:
      https://arxiv.org/abs/1205.3104
  - Howard, Vala (2012), prime-d qudit pi/8 gates:
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

from scripts.w33_qutrit_operator_algebra import analyze as analyze_qutrit_operator_layer  # noqa: E402


REFERENCE_LITERATURE = {
    "tqc_review": "https://arxiv.org/abs/0707.1889",
    "qutrit_magic_state_distillation": "https://arxiv.org/abs/1202.2326",
    "prime_dimension_reed_muller_magic": "https://arxiv.org/abs/1205.3104",
    "qudit_pi_over_eight_gate": "https://arxiv.org/abs/1206.1598",
}


@lru_cache(maxsize=1)
def exact_clifford_backbone_summary() -> Dict[str, Any]:
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
        "symplectic_generator_names": operator["symplectic_action"]["generator_names"],
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
def exact_tetra_qutrit_primitive_summary() -> Dict[str, Any]:
    summary = build_universal_tetra_qutrit_summary()
    vertex_axis = summary["tetra_vertex_axis_dictionary"]
    axis = summary["tetra_axis_symmetry"]
    qutrit = summary["qutrit_identification"]
    bundle = summary["transport_bundle_dictionary"]
    theorem = summary["universal_tetra_qutrit_theorem"]

    return {
        "tetra_vertex_packet_dimension": len(vertex_axis["tetra_hadamard_basis"]),
        "tetra_axis_packet_dimension": len(vertex_axis["canonical_axis_sign_matrix"][0]),
        "chart_axis_matches_canonical_tetra_axis_up_to_relabels": bool(
            vertex_axis["chart_axis_matches_canonical_tetra_axis_up_to_relabels"]["matches"]
        ),
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
def standard_model_computation_boundary_summary() -> Dict[str, Any]:
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
        "clean_higgs_pair": tuple(fermions["clean_higgs_slots"]),
        "mixing_tan_theta_c": mixing["tan_theta_c"]["exact"],
        "exact_pmns_12": mixing["sin2_theta_12"]["exact"],
        "exact_pmns_23": mixing["sin2_theta_23"]["exact"],
        "exact_pmns_13": mixing["sin2_theta_13"]["exact"],
        "all_anomalies_cancel": anomaly["all_anomalies_cancel"],
        "bosonic_action_complete": frontier["bosonic_action_complete"],
        "fermion_representations_complete": frontier["fermion_representations_complete"],
        "mixing_backbone_complete": frontier["mixing_backbone_complete"],
        "anomaly_backbone_complete": frontier["anomaly_backbone_complete"],
        "full_yukawa_eigenvalue_spectrum_still_open": frontier["full_yukawa_eigenvalue_spectrum_still_open"],
    }


@lru_cache(maxsize=1)
def classify_tqc_standard_model_boundary() -> Tuple[Dict[str, Any], ...]:
    clifford = exact_clifford_backbone_summary()
    tetra = exact_tetra_qutrit_primitive_summary()
    sm = standard_model_computation_boundary_summary()

    return (
        {
            "name": "exact_qutrit_clifford_backbone",
            "support_level": "repo-exact qutrit kernel",
            "statement": (
                "The exact W33 finite kernel already provides a stabilizer/Clifford "
                "backbone: projective two-qutrit Pauli geometry, verified symplectic "
                "generators, the canonical quadratic Hamiltonian, and an exact local "
                "27 = 3^3 Heisenberg carrier."
            ),
            "evidence": clifford,
        },
        {
            "name": "exact_tetra_qutrit_control_transport_primitive",
            "support_level": "repo-exact control / transport primitive",
            "statement": (
                "The exact transport/control side closes as one tetra-qutrit object: "
                "the 4-slot CKM/chart packet is the vertex side of a tetrahedron, the "
                "3-state transport packet is the axis side, and the 135 bundle is 45 "
                "copies of that same qutrit primitive."
            ),
            "evidence": tetra,
        },
        {
            "name": "exact_standard_model_action_backbone",
            "support_level": "repo-exact Standard Model backbone",
            "statement": (
                "On the Standard Model side, the bosonic action, fermion content, exact "
                "mixing backbone, and anomaly cancellation are fixed exactly."
            ),
            "evidence": sm,
        },
        {
            "name": "honest_universality_boundary",
            "support_level": "repo-exact backbone with open non-Clifford frontier",
            "statement": (
                "The exact repo already fixes the qutrit Clifford processor and its "
                "tetrahedral control/transport bus, but the full Yukawa spectrum is "
                "still open. So the conservative TQC reading stops short of a full "
                "braiding-universal theorem and leaves the non-Clifford resource on the "
                "Yukawa frontier."
            ),
            "evidence": {
                "all_symplectic_generators_verified": clifford["all_symplectic_generators_verified"],
                "axis_group_is_exact_s3": tetra["axis_group_is_exact_s3"],
                "transport_cycle_diagonalizes_to_qutrit_packet_up_to_orientation": tetra[
                    "transport_cycle_diagonalizes_to_qutrit_packet_up_to_orientation"
                ],
                "full_yukawa_eigenvalue_spectrum_still_open": sm[
                    "full_yukawa_eigenvalue_spectrum_still_open"
                ],
            },
        },
    )


@lru_cache(maxsize=1)
def analyze() -> Dict[str, Any]:
    clifford = exact_clifford_backbone_summary()
    tetra = exact_tetra_qutrit_primitive_summary()
    sm = standard_model_computation_boundary_summary()
    records = classify_tqc_standard_model_boundary()

    theorem = {
        "the_exact_repo_contains_a_two_qutrit_pauli_clifford_backbone": (
            clifford["w33_vertex_count"] == 40
            and clifford["w33_edge_count"] == 240
            and clifford["projective_pauli_point_count"] == 40
            and clifford["weyl_basis_size"] == 81
            and clifford["identity_isomorphism_holds"] is True
            and clifford["product_law_holds"] is True
            and clifford["commutator_phase_matches_symplectic"] is True
            and clifford["all_symplectic_generators_verified"] is True
        ),
        "the_local_standard_model_carrier_is_exactly_a_three_qutrit_shell": (
            clifford["local_h27_size"] == 27
            and clifford["local_neighbor_count"] == 12
            and clifford["local_triangle_sizes"] == (3, 3, 3, 3)
            and clifford["local_fiber_sizes"] == (3, 3, 3, 3, 3, 3, 3, 3, 3)
            and clifford["inter_fiber_counts"] == (3,)
            and clifford["h27_internal_triangle_count"] == 36
        ),
        "the_transport_and_control_packet_close_as_one_exact_tetra_qutrit_primitive": (
            tetra["tetra_vertex_packet_dimension"] == 4
            and tetra["tetra_axis_packet_dimension"] == 3
            and tetra["chart_axis_matches_canonical_tetra_axis_up_to_relabels"] is True
            and tetra["axis_group_order"] == 6
            and tetra["axis_group_is_exact_s3"] is True
            and (
                tetra["transport_three_cycle_equals_repo_qutrit_cycle"] is True
                or tetra["transport_three_cycle_inverse_equals_repo_qutrit_cycle"] is True
            )
            and tetra["transport_cycle_diagonalizes_to_qutrit_packet_up_to_orientation"] is True
            and tetra["local_axis_packet_dimension"] == 3
            and tetra["real_decomposition"] == (1, 2)
            and tetra["global_bundle_dimension"] == 135
            and tetra["global_radial_dimension"] == 45
            and tetra["global_tangential_dimension"] == 90
            and tetra["all_six_axis_permutations_occur_on_transport_edges"] is True
            and tetra["transport_135_is_45_times_3"] is True
            and tetra["transport_90_is_45_times_2"] is True
        ),
        "the_exact_standard_model_backbone_is_fixed_while_the_yukawa_nonclifford_resource_remains_open": (
            sm["bosonic_action_fixed"] is True
            and sm["fermion_representation_dimension"] == 16
            and sm["three_generation_matter_dimension"] == 48
            and sm["decomposition_16_equals_6_3_3_2_1_1"] is True
            and sm["all_anomalies_cancel"] is True
            and sm["full_yukawa_eigenvalue_spectrum_still_open"] is True
        ),
        "the_current_exact_tqc_read_is_qutrit_clifford_plus_tetra_control_transport_not_yet_braiding_universal": (
            clifford["all_symplectic_generators_verified"] is True
            and tetra["axis_group_is_exact_s3"] is True
            and tetra["transport_cycle_diagonalizes_to_qutrit_packet_up_to_orientation"] is True
            and sm["full_yukawa_eigenvalue_spectrum_still_open"] is True
        ),
    }

    return {
        "status": "ok",
        "reference_literature": REFERENCE_LITERATURE,
        "exact_clifford_backbone": clifford,
        "exact_tetra_qutrit_primitive": tetra,
        "standard_model_computation_boundary": sm,
        "record_details": records,
        "tqc_standard_model_boundary_theorem": theorem,
        "bridge_verdict": (
            "The deeper exact computational read of the repo is now clearer. The W33 "
            "kernel already fixes a qutrit stabilizer/Clifford backbone, and the "
            "transport/CKM side closes as one exact tetra-qutrit control primitive: a "
            "4-slot vertex packet acting on a 3-state axis qutrit, replicated across "
            "the 135 = 45 * 3 transport bundle. So the most honest universal-"
            "computation statement is not that the repo already has a braid-density "
            "theorem for Standard Model physics; it is that the repo now has an exact "
            "qutrit Clifford processor plus an exact tetrahedral control/transport bus, "
            "while the non-Clifford Yukawa resource required for full universality "
            "remains open."
        ),
    }


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXXI_standard_model_tqc_boundary_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("Standard Model TQC boundary audit")
    for key, value in payload["tqc_standard_model_boundary_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")
    print(f"  Wrote: {output_path}")


if __name__ == "__main__":
    main()
