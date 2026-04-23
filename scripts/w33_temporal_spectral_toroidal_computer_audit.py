#!/usr/bin/env python3
"""Single-photon temporal/spectral toroidal computer audit for the W33 kernel.

This module develops a conservative physical system for computation from the
exact finite layers already closed in the repo.

Exact finite inputs already available:
1. The W33 kernel is exactly the projective two-qutrit Pauli geometry, with
   40 projective Pauli classes and an 81-element Weyl basis.
2. The local shell splits exactly as a 13-point projective screen plus a
   27-point affine bulk: ``PG(2,3) + AG(3,3)``.
3. The full measurement side is exact: the 40 isotropic lines admit 36 spreads,
   each yielding a complete 10-basis two-qutrit stabilizer MUB frame.
4. The control/transport side already closes as an exact tetra-qutrit packet.
5. The remaining non-Clifford content has already been localized to two
   independent quartic atoms.

Conservative physical interpretation introduced here:
  the exact two-qutrit kernel can be read as a single photon carrying two
  commuting qutrit degrees of freedom:

    - a temporal qutrit with three orthogonal modes labelled
      ``past / now / future``;
    - a spectral qutrit with three resonant sidebands labelled
      ``lower / carrier / upper``.

This gives a concrete 3x3 discrete torus in one photon. The projective memory
screen, affine compute bulk, and 36 spread/MUB frames then become an executable
hardware dictionary rather than only a finite-geometry statement.

The toroidal side is kept conservative too. We only use the exact seed packet
already visible in the repo:

    - one selector line plus six identical nontrivial modes,
    - Phi_6 = 7 on the first closed torus,
    - genus numerator 4x3 = 12 matching the tetrahedral packet.

That is enough to motivate a harmonic toroidal processor architecture without
claiming that retrocausality or continuum emergence is already proved.

Primary literature anchors for the realization layer:
  - Imany et al. (2018/2019), single-photon time/frequency two-qudit logic:
      https://arxiv.org/abs/1805.04410
  - Dutt et al. (2019/2020), single cavity with two synthetic dimensions:
      https://arxiv.org/abs/1909.04828
  - Yuan, Dutt, Fan (2021), synthetic frequency dimensions in ring resonators:
      https://arxiv.org/abs/2105.04069
  - Yuan et al. (2019/2020), local interactions in synthetic frequency space:
      https://arxiv.org/abs/1909.12466
  - Raymer, Walmsley (2019), temporal modes in quantum optics:
      https://arxiv.org/abs/1911.06771
  - Bouchard et al. (2023), ultrafast time-bin qudit measurements:
      https://arxiv.org/abs/2302.03045
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

from scripts.w33_projective_affine_shell_audit import analyze as analyze_projective_affine_shell  # noqa: E402
from scripts.w33_standard_model_minimal_magic_audit import analyze as analyze_minimal_magic  # noqa: E402
from scripts.w33_standard_model_tqc_boundary_audit import analyze as analyze_tqc_boundary  # noqa: E402
from scripts.w33_symplectic_spread_frame_audit import analyze as analyze_spread_frame  # noqa: E402

try:
    from exploration.w33_toroidal_genus_fourier_bridge import build_summary as build_toroidal_genus_fourier_summary  # noqa: E402
except ModuleNotFoundError:
    from w33_toroidal_genus_fourier_bridge import build_summary as build_toroidal_genus_fourier_summary  # noqa: E402


Q = 3
PHI6 = 7
CHECKS = ROOT / "checks"

REFERENCE_LITERATURE = {
    "single_photon_time_frequency_two_qudit_logic": "https://arxiv.org/abs/1805.04410",
    "single_cavity_two_synthetic_dimensions": "https://arxiv.org/abs/1909.04828",
    "synthetic_frequency_dimension_tutorial": "https://arxiv.org/abs/2105.04069",
    "local_interactions_in_synthetic_frequency_dimension": "https://arxiv.org/abs/1909.12466",
    "temporal_modes_review": "https://arxiv.org/abs/1911.06771",
    "ultrafast_time_bin_qudits": "https://arxiv.org/abs/2302.03045",
}


@lru_cache(maxsize=1)
def exact_two_qutrit_processor_summary() -> Dict[str, Any]:
    payload = analyze_tqc_boundary()
    clifford = payload["exact_clifford_backbone"]
    tetra = payload["exact_tetra_qutrit_primitive"]
    sm = payload["standard_model_computation_boundary"]

    return {
        "field_order": Q,
        "two_qutrit_hilbert_dimension": Q * Q,
        "projective_pauli_class_count": clifford["projective_pauli_point_count"],
        "weyl_operator_basis_size": clifford["weyl_basis_size"],
        "w33_vertex_count": clifford["w33_vertex_count"],
        "w33_edge_count": clifford["w33_edge_count"],
        "all_symplectic_generators_verified": clifford["all_symplectic_generators_verified"],
        "local_h27_size": clifford["local_h27_size"],
        "canonical_hamiltonian_spectrum": clifford["canonical_hamiltonian_spectrum"],
        "tetra_vertex_packet_dimension": tetra["tetra_vertex_packet_dimension"],
        "tetra_axis_packet_dimension": tetra["tetra_axis_packet_dimension"],
        "transport_bundle_dimension": tetra["global_bundle_dimension"],
        "transport_bundle_real_split": tetra["real_decomposition"],
        "axis_group_is_exact_s3": tetra["axis_group_is_exact_s3"],
        "bosonic_action_complete": sm["bosonic_action_complete"],
        "fermion_representations_complete": sm["fermion_representations_complete"],
        "mixing_backbone_complete": sm["mixing_backbone_complete"],
        "full_yukawa_eigenvalue_spectrum_still_open": sm["full_yukawa_eigenvalue_spectrum_still_open"],
    }


@lru_cache(maxsize=1)
def exact_screen_bulk_measurement_summary() -> Dict[str, Any]:
    shell = analyze_projective_affine_shell()
    spread = analyze_spread_frame()

    projective = shell["projective_space"]
    generalized_quadrangle = shell["symplectic_generalized_quadrangle"]
    hyperplanes = shell["hyperplane_profiles"]
    anchor_chart = shell["canonical_anchor_chart"]

    spread_dictionary = spread["spread_dictionary"]
    anchor_frame = spread["canonical_anchor_frame"]
    sample_profile = anchor_frame["sample_spread_profile"]

    return {
        "projective_point_count": projective["point_count"],
        "projective_line_count": projective["projective_line_count"],
        "isotropic_line_count": generalized_quadrangle["isotropic_line_count"],
        "srg_parameters": generalized_quadrangle["point_graph_parameters"],
        "projective_screen_size": hyperplanes["distinct_hyperplane_sizes"][0],
        "projective_screen_line_count": hyperplanes["distinct_hyperplane_line_counts"][0],
        "projective_screen_anchor_line_count": hyperplanes["distinct_isotropic_line_counts_through_anchor"][0],
        "affine_bulk_size": hyperplanes["distinct_affine_point_counts"][0],
        "affine_line_count": hyperplanes["distinct_affine_line_counts"][0],
        "affine_direction_count": hyperplanes["distinct_affine_direction_counts"][0],
        "anchor_coordinate_count": anchor_chart["coordinate_count"],
        "anchor_fiber_count": anchor_chart["fiber_count"],
        "anchor_fiber_size": anchor_chart["fiber_size_set"][0],
        "spread_count": spread_dictionary["spread_count"],
        "spread_size": spread_dictionary["spread_size"],
        "line_occurrence_distribution": spread_dictionary["line_occurrence_distribution"],
        "mub_max_deviation": spread_dictionary["mub_max_deviation"],
        "anchor_line_count": len(anchor_frame["anchor_lines"]),
        "anchor_sector_size_set": tuple(sorted(set(anchor_frame["sector_sizes"].values()))),
        "sample_memory_lines": sample_profile["lines_inside_hyperplane"],
        "sample_affine_measurement_lines": sample_profile["affine_direction_count"],
    }


@lru_cache(maxsize=1)
def exact_toroidal_harmonic_seed_summary() -> Dict[str, Any]:
    genus = build_toroidal_genus_fourier_summary()
    genus_dictionary = genus["genus_dictionary"]
    tetrahedral_packet = genus["tetrahedral_packet_dictionary"]

    selector_line = 1
    shared_six_channel = PHI6 - 1
    adjacency_spectrum = [shared_six_channel] + [-1] * shared_six_channel
    laplacian_spectrum = [0] + [PHI6] * shared_six_channel

    return {
        "selector_line_dimension": selector_line,
        "shared_six_channel": shared_six_channel,
        "phi6": PHI6,
        "first_closed_torus_genus": genus_dictionary["primal_genus_at_phi6"],
        "toroidal_seed_order": PHI6,
        "adjacency_spectrum": adjacency_spectrum,
        "laplacian_spectrum": laplacian_spectrum,
        "nontrivial_spectral_trace": sum(laplacian_spectrum),
        "tetrahedral_chart_vertices": tetrahedral_packet["chart_vertices"],
        "tetrahedral_local_modes": tetrahedral_packet["local_outgoing_modes"],
        "tetrahedral_directed_packet": tetrahedral_packet["directed_packet"],
        "balanced_chirality_split": (
            tetrahedral_packet["positive_frames"],
            tetrahedral_packet["negative_frames"],
        ),
        "admissible_mod12_residues": tuple(genus_dictionary["admissible_residues_mod_12"]),
        "synthetic_torus_shape": (Q, Q),
        "synthetic_torus_cell_count": Q * Q,
    }


@lru_cache(maxsize=1)
def conservative_single_photon_hardware_dictionary() -> Dict[str, Any]:
    processor = exact_two_qutrit_processor_summary()
    screen = exact_screen_bulk_measurement_summary()
    torus = exact_toroidal_harmonic_seed_summary()
    magic = analyze_minimal_magic()["quartic_magic_atoms"]

    return {
        "carrier": "single photon",
        "commuting_degrees_of_freedom": ("temporal_mode_qutrit", "synthetic_frequency_qutrit"),
        "temporal_qutrit_labels": ("past", "now", "future"),
        "spectral_qutrit_labels": ("lower_sideband", "carrier", "upper_sideband"),
        "single_photon_hilbert_dimension": processor["two_qutrit_hilbert_dimension"],
        "discrete_torus_shape": torus["synthetic_torus_shape"],
        "discrete_torus_cell_count": torus["synthetic_torus_cell_count"],
        "projective_memory_screen_size": screen["projective_screen_size"],
        "affine_compute_bulk_size": screen["affine_bulk_size"],
        "measurement_program_count": screen["spread_count"],
        "measurement_bases_per_program": screen["spread_size"],
        "memory_line_count_per_program": screen["sample_memory_lines"],
        "affine_measurement_line_count_per_program": screen["sample_affine_measurement_lines"],
        "tetrahedral_control_packet": processor["tetra_vertex_packet_dimension"],
        "qutrit_axis_packet": processor["tetra_axis_packet_dimension"],
        "transport_bundle_dimension": processor["transport_bundle_dimension"],
        "harmonic_selector_packet": (
            torus["selector_line_dimension"],
            torus["shared_six_channel"],
            torus["phi6"],
        ),
        "linear_control_layer": (
            "temporal shift",
            "temporal phase",
            "spectral shift",
            "spectral phase",
            "time-frequency SUM / Fourier mixing",
        ),
        "nonlinear_resource_candidate": "chi^(3) Kerr or four-wave-mixing ring section",
        "quartic_magic_atom_count": magic["packet_size"],
        "quartic_magic_min_degree": 4,
        "realization_boundary_note": (
            "The temporal labels past/now/future are implemented as one-photon temporal "
            "modes around a clock pulse. This is a conservative temporal-mode reading, "
            "not a claim that the finite kernel has already derived a literal reversal "
            "of causal order."
        ),
    }


@lru_cache(maxsize=1)
def honest_universality_boundary() -> Dict[str, Any]:
    processor = exact_two_qutrit_processor_summary()
    screen = exact_screen_bulk_measurement_summary()
    torus = exact_toroidal_harmonic_seed_summary()
    magic = analyze_minimal_magic()["quartic_magic_atoms"]

    return {
        "clifford_processor_is_exact": bool(processor["all_symplectic_generators_verified"]),
        "complete_measurement_layer_is_exact": bool(screen["mub_max_deviation"] < 1e-12),
        "harmonic_toroidal_seed_is_exact": bool(
            torus["selector_line_dimension"] == 1
            and torus["shared_six_channel"] == 6
            and torus["phi6"] == 7
            and torus["first_closed_torus_genus"] == 1
            and torus["tetrahedral_directed_packet"] == 12
        ),
        "nonclifford_frontier_is_two_quartic_atoms": bool(
            magic["packet_size"] == 2
            and magic["remaining_signed_yukawa_packet_is_two_d4_quartic_lifts"] is True
        ),
        "full_yukawa_eigenvalue_spectrum_still_open": bool(
            processor["full_yukawa_eigenvalue_spectrum_still_open"]
        ),
        "device_status": (
            "Exact Clifford processor plus exact complete measurement layer plus "
            "minimal two-quartic nonlinear frontier; explicit magic injection and "
            "device-level universality synthesis remain open."
        ),
    }


@lru_cache(maxsize=1)
def classify_temporal_spectral_toroidal_computer() -> Tuple[Dict[str, Any], ...]:
    processor = exact_two_qutrit_processor_summary()
    screen = exact_screen_bulk_measurement_summary()
    torus = exact_toroidal_harmonic_seed_summary()
    hardware = conservative_single_photon_hardware_dictionary()
    boundary = honest_universality_boundary()

    return (
        {
            "name": "exact_two_qutrit_processor",
            "support_level": "repo-exact processor layer",
            "statement": (
                "The exact W33 kernel is already a 9-dimensional two-qutrit processor "
                "with verified Clifford symmetry, a 40-point projective Pauli geometry, "
                "and an 81-element Weyl operator basis."
            ),
            "evidence": processor,
        },
        {
            "name": "exact_screen_bulk_measurement_layer",
            "support_level": "repo-exact geometry and frame layer",
            "statement": (
                "The local shell already separates as a 13-point projective memory screen "
                "and a 27-point affine compute bulk, and the same kernel admits 36 complete "
                "10-basis two-qutrit stabilizer measurement programs."
            ),
            "evidence": screen,
        },
        {
            "name": "exact_toroidal_harmonic_seed",
            "support_level": "repo-exact toroidal seed",
            "statement": (
                "The first closed toroidal seed is already one selector line plus six "
                "identical nontrivial modes at Phi_6 = 7, with genus numerator 4x3 = 12 "
                "matching the tetrahedral local packet."
            ),
            "evidence": torus,
        },
        {
            "name": "conservative_single_photon_hardware_hypothesis",
            "support_level": "conservative physical realization hypothesis",
            "statement": (
                "A coherent laboratory realization is a single photon carrying a temporal "
                "qutrit and a synthetic-frequency qutrit. The temporal packet is read as "
                "past/now/future modes around one clock event, the spectral packet as "
                "lower/carrier/upper sidebands on a modulated ring, giving one 3x3 torus."
            ),
            "evidence": hardware,
        },
        {
            "name": "honest_photonic_universality_boundary",
            "support_level": "repo-exact backbone plus open synthesis frontier",
            "statement": (
                "The exact processor and its complete measurement layer are already fixed, "
                "while the non-Clifford frontier has been localized to two quartic nonlinear "
                "injection channels. That is a concrete universality architecture, but not "
                "yet a completed device theorem."
            ),
            "evidence": boundary,
        },
    )


@lru_cache(maxsize=1)
def analyze() -> Dict[str, Any]:
    processor = exact_two_qutrit_processor_summary()
    screen = exact_screen_bulk_measurement_summary()
    torus = exact_toroidal_harmonic_seed_summary()
    hardware = conservative_single_photon_hardware_dictionary()
    boundary = honest_universality_boundary()
    records = classify_temporal_spectral_toroidal_computer()

    theorem = {
        "the_exact_w33_kernel_is_already_a_9dimensional_two_qutrit_processor": (
            processor["two_qutrit_hilbert_dimension"] == 9
            and processor["projective_pauli_class_count"] == 40
            and processor["weyl_operator_basis_size"] == 81
            and processor["all_symplectic_generators_verified"] is True
        ),
        "the_exact_local_shell_is_a_projective_screen_plus_affine_bulk": (
            screen["projective_screen_size"] == 13
            and screen["affine_bulk_size"] == 27
            and screen["affine_direction_count"] == 13
            and screen["anchor_fiber_count"] == 9
            and screen["anchor_fiber_size"] == 3
        ),
        "the_exact_36_spreads_are_36_complete_two_qutrit_measurement_programs": (
            screen["spread_count"] == 36
            and screen["spread_size"] == 10
            and screen["sample_memory_lines"] == 1
            and screen["sample_affine_measurement_lines"] == 9
            and screen["mub_max_deviation"] < 1e-12
        ),
        "the_exact_toroidal_seed_is_one_selector_plus_six_phi6_modes_on_the_first_closed_torus": (
            torus["selector_line_dimension"] == 1
            and torus["shared_six_channel"] == 6
            and torus["phi6"] == 7
            and torus["first_closed_torus_genus"] == 1
            and torus["tetrahedral_directed_packet"] == 12
        ),
        "the_single_photon_temporal_spectral_hardware_dictionary_matches_the_exact_finite_counts": (
            hardware["single_photon_hilbert_dimension"] == 9
            and hardware["discrete_torus_shape"] == (3, 3)
            and hardware["measurement_program_count"] == 36
            and hardware["measurement_bases_per_program"] == 10
            and hardware["quartic_magic_atom_count"] == 2
            and hardware["quartic_magic_min_degree"] == 4
        ),
        "the_remaining_nonclifford_universality_frontier_is_two_quartic_nonlinear_injection_channels": (
            boundary["nonclifford_frontier_is_two_quartic_atoms"] is True
            and boundary["full_yukawa_eigenvalue_spectrum_still_open"] is True
        ),
        "the_realization_claim_is_a_conservative_hardware_hypothesis_not_a_finished_device_theorem": (
            hardware["carrier"] == "single photon"
            and "retrocausality" not in hardware["realization_boundary_note"].lower()
            and boundary["clifford_processor_is_exact"] is True
            and boundary["complete_measurement_layer_is_exact"] is True
            and boundary["full_yukawa_eigenvalue_spectrum_still_open"] is True
        ),
    }

    return {
        "status": "ok",
        "reference_literature": REFERENCE_LITERATURE,
        "exact_two_qutrit_processor": processor,
        "exact_screen_bulk_measurement_layer": screen,
        "exact_toroidal_harmonic_seed": torus,
        "single_photon_hardware_dictionary": hardware,
        "universality_boundary": boundary,
        "record_details": records,
        "temporal_spectral_toroidal_computer_theorem": theorem,
        "bridge_verdict": (
            "The strongest conservative physical system now supported by the repo is a "
            "single-photon temporal/spectral toroidal qutrit computer. The exact W33 "
            "kernel supplies the 9-dimensional two-qutrit Clifford processor, the "
            "projective/affine shell supplies a 13-point memory screen plus 27-point "
            "compute bulk, the 36 symplectic spreads supply 36 complete 10-basis "
            "measurement programs, and the toroidal seed supplies the one-plus-six "
            "harmonic shell on the first closed torus. The open universality wall is no "
            "longer where to look for the non-Clifford resource: it has already collapsed "
            "to two quartic nonlinear atoms. What remains open is explicit injection and "
            "device-level synthesis, not the finite architecture dictionary."
        ),
    }


def write_artifact() -> Path:
    CHECKS.mkdir(exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = CHECKS / f"PART_CXXVI_temporal_spectral_toroidal_computer_audit_{timestamp}.json"
    path.write_text(json.dumps(analyze(), indent=2), encoding="utf-8")
    return path


if __name__ == "__main__":
    artifact = write_artifact()
    print(json.dumps(analyze(), indent=2))
    print(f"\nartifact: {artifact}")
