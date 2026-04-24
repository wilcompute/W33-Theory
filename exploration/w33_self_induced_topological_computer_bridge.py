"""Exact self-induced topological computer bridge for the W33 kernel.

This bridge promotes the existing qutrit/toroidal audits into one paper-facing
statement with the claim level kept honest.

The exact finite architecture already closed in the repo is:

1. Processor:
   the W33 kernel is exactly a 9-dimensional two-qutrit processor with
   projective Clifford layer ``25920`` and full graph-symmetry extension
   ``51840``.

2. Memory and compute geometry:
   the local shell splits exactly as a 13-point projective memory screen plus a
   27-point affine compute bulk.

3. Complete measurement layer:
   the exact 36 spreads furnish 36 complete 10-basis two-qutrit stabilizer
   measurement programs.

4. Topological/harmonic seed:
   the first closed toroidal seed is one selector line plus six identical
   nontrivial modes at ``Phi_6 = 7``, with directed packet ``12``.

5. Protection ladder:
   the same kernel carries the exact operator ladder

       sqrt(10)  ->  10  ->  100
         |D|        L       H_YM = L^2

   with normalized Laplacian gap ``5/6``.

6. Non-Clifford frontier:
   the remaining nonlinear resource has already collapsed to exactly two
   quartic atoms; explicit injection/synthesis remains open.

So the honest computational reading is:

    the W33 kernel is already a self-induced topological computer architecture,
    in the sense that the same finite object generates its processor, memory
    screen, measurement programs, toroidal protection seed, and localized
    nonlinear frontier internally.

What remains open is not where the architecture lives, but explicit device-level
non-Clifford injection and universality synthesis.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_self_induced_topological_computer_bridge_summary.json"

for candidate in (ROOT, ROOT / "scripts", ROOT / "exploration"):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from scripts.w33_standard_model_minimal_magic_audit import analyze as analyze_minimal_magic  # noqa: E402
from scripts.w33_temporal_spectral_toroidal_computer_audit import analyze as analyze_toroidal_computer  # noqa: E402
from w33_mass_gap_operator_ladder_bridge import build_mass_gap_operator_ladder_summary  # noqa: E402
from w33_qutrit_symmetry_ladder_bridge import build_qutrit_symmetry_ladder_summary  # noqa: E402


def build_self_induced_topological_computer_summary() -> dict[str, Any]:
    symmetry = build_qutrit_symmetry_ladder_summary()
    toroidal = analyze_toroidal_computer()
    mass_gap = build_mass_gap_operator_ladder_summary()
    magic = analyze_minimal_magic()

    processor = toroidal["exact_two_qutrit_processor"]
    screen = toroidal["exact_screen_bulk_measurement_layer"]
    torus = toroidal["exact_toroidal_harmonic_seed"]
    boundary = toroidal["universality_boundary"]
    quartic = magic["quartic_magic_atoms"]

    return {
        "self_induced_topological_computer_dictionary": {
            "processor_layer": {
                "two_qutrit_hilbert_dimension": processor["two_qutrit_hilbert_dimension"],
                "projective_pauli_class_count": processor["projective_pauli_class_count"],
                "weyl_operator_basis_size": processor["weyl_operator_basis_size"],
                "projective_clifford_order": symmetry["symmetry_ladder_dictionary"]["projective_layer"]["order"],
                "full_graph_symmetry_order": symmetry["symmetry_ladder_dictionary"]["full_graph_layer"]["order"],
                "neighbor_bus_order": symmetry["symmetry_ladder_dictionary"]["neighbor_bus_layer"]["induced_group_order"],
            },
            "memory_compute_layer": {
                "projective_screen_size": screen["projective_screen_size"],
                "affine_bulk_size": screen["affine_bulk_size"],
                "affine_direction_count": screen["affine_direction_count"],
                "anchor_fiber_count": screen["anchor_fiber_count"],
                "anchor_fiber_size": screen["anchor_fiber_size"],
            },
            "measurement_layer": {
                "spread_count": screen["spread_count"],
                "spread_size": screen["spread_size"],
                "sample_memory_lines": screen["sample_memory_lines"],
                "sample_affine_measurement_lines": screen["sample_affine_measurement_lines"],
                "mub_max_deviation": screen["mub_max_deviation"],
            },
            "toroidal_seed_layer": {
                "selector_line_dimension": torus["selector_line_dimension"],
                "shared_six_channel": torus["shared_six_channel"],
                "phi6": torus["phi6"],
                "first_closed_torus_genus": torus["first_closed_torus_genus"],
                "tetrahedral_directed_packet": torus["tetrahedral_directed_packet"],
                "synthetic_torus_shape": tuple(torus["synthetic_torus_shape"]),
                "synthetic_torus_cell_count": torus["synthetic_torus_cell_count"],
            },
            "protection_layer": {
                "dirac_gap_radicand": mass_gap["operator_ladder_dictionary"]["dirac_positive_scales"]["lowest_radicand"],
                "laplacian_gap": mass_gap["operator_ladder_dictionary"]["gap_dictionary"]["laplacian_gap"],
                "yang_mills_gap": mass_gap["operator_ladder_dictionary"]["gap_dictionary"]["yang_mills_gap"],
                "normalized_gap": mass_gap["operator_ladder_dictionary"]["gap_dictionary"]["normalized_gap"]["exact"],
            },
            "nonlinear_frontier_layer": {
                "quartic_magic_atom_count": quartic["packet_size"],
                "quartic_magic_min_degree": 4,
                "h2_galois_group_label": quartic["h2_galois_group_label"],
                "hbar2_galois_group_label": quartic["hbar2_galois_group_label"],
                "root_field_compositum_degree": quartic["quartic_root_field_compositum_degree"],
                "splitting_field_compositum_degree": quartic["quartic_splitting_field_compositum_degree"],
            },
        },
        "self_induced_topological_computer_theorem": {
            "the_processor_layer_is_exactly_a_two_qutrit_clifford_backbone": (
                processor["two_qutrit_hilbert_dimension"] == 9
                and processor["projective_pauli_class_count"] == 40
                and processor["weyl_operator_basis_size"] == 81
                and symmetry["symmetry_ladder_theorem"]["projective_clifford_order_is_25920"] is True
                and symmetry["symmetry_ladder_theorem"]["full_graph_symmetry_order_is_51840"] is True
                and symmetry["symmetry_ladder_theorem"]["the_12_neighbor_bus_is_the_exact_432_affine_layer"] is True
            ),
            "the_memory_and_compute_geometry_is_exactly_projective_13_plus_affine_27": (
                screen["projective_screen_size"] == 13
                and screen["affine_bulk_size"] == 27
                and screen["affine_direction_count"] == 13
                and screen["anchor_fiber_count"] == 9
                and screen["anchor_fiber_size"] == 3
            ),
            "the_measurement_layer_is_exactly_36_complete_two_qutrit_programs": (
                screen["spread_count"] == 36
                and screen["spread_size"] == 10
                and screen["sample_memory_lines"] == 1
                and screen["sample_affine_measurement_lines"] == 9
                and screen["mub_max_deviation"] < 1e-12
            ),
            "the_topological_seed_is_exactly_one_plus_six_at_phi6_on_a_3x3_torus": (
                torus["selector_line_dimension"] == 1
                and torus["shared_six_channel"] == 6
                and torus["phi6"] == 7
                and torus["first_closed_torus_genus"] == 1
                and tuple(torus["synthetic_torus_shape"]) == (3, 3)
                and torus["synthetic_torus_cell_count"] == 9
            ),
            "the_operator_protection_ladder_is_exactly_sqrt10_to_10_to_100": (
                mass_gap["exact_factorizations"]["dirac_gap_squared_equals_laplacian_gap"] is True
                and mass_gap["exact_factorizations"]["laplacian_gap_equals_phi4"] is True
                and mass_gap["exact_factorizations"]["yang_mills_gap_is_laplacian_gap_squared"] is True
                and mass_gap["operator_ladder_dictionary"]["gap_dictionary"]["normalized_gap"]["exact"] == "5/6"
            ),
            "the_nonclifford_frontier_is_localized_to_two_quartic_atoms": (
                quartic["packet_size"] == 2
                and quartic["remaining_signed_yukawa_packet_is_two_d4_quartic_lifts"] is True
                and quartic["mixed_product_degree"] == 8
                and quartic["mixed_ratio_degree"] == 8
            ),
            "the_architecture_is_self_induced_but_device_level_universality_is_still_open": (
                boundary["clifford_processor_is_exact"] is True
                and boundary["complete_measurement_layer_is_exact"] is True
                and boundary["harmonic_toroidal_seed_is_exact"] is True
                and boundary["nonclifford_frontier_is_two_quartic_atoms"] is True
                and boundary["full_yukawa_eigenvalue_spectrum_still_open"] is True
            ),
        },
        "boundary_note": (
            "This bridge is intentionally stronger than a boundary audit but weaker than a "
            "finished device theorem. It closes the exact endogenous architecture: "
            "processor, memory, measurement, toroidal protection, and nonlinear frontier "
            "all arise from the same W33 kernel. It does not claim that explicit "
            "quartic injection, braid density, or a laboratory photonic implementation "
            "has already been solved."
        ),
        "bridge_verdict": (
            "The exact computational core can now be stated cleanly: W33 is a "
            "self-induced topological computer architecture. Its two-qutrit Clifford "
            "processor, 13+27 memory/compute split, 36 complete measurement programs, "
            "one-plus-six toroidal protection seed, and two-quartic nonlinear frontier "
            "are all generated internally by the same finite kernel. The remaining open "
            "problem is explicit non-Clifford injection and device-level universality "
            "synthesis, not discovery of the architecture itself."
        ),
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_self_induced_topological_computer_summary(), indent=2),
        encoding="utf-8",
    )
    return path


if __name__ == "__main__":
    write_summary()
