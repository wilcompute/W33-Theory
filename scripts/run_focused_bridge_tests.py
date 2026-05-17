#!/usr/bin/env python3
"""Run named focused theorem-test slices.

The repository is large enough that broad pytest collection can be slow on
Windows/WSL-mounted trees.  This helper runs curated file lists for the bridge
areas that are commonly touched during architecture work.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SUITES: dict[str, list[str]] = {
    "photonic-qec": [
        "tests/test_dccxiv_holonomy_signed_triad_a2_projection_bridge.py",
        "tests/test_dccxv_photonic_fusion_syndrome_qec_bridge.py",
        "tests/test_dccxvi_axis_syndrome_selector_codec_bridge.py",
        "tests/test_dcclxxv_photonic_retry_closure_kernel_bridge.py",
        "tests/test_dcclxvii_axis_syndrome_nilpotent_octahedral_bridge.py",
        "tests/test_dcclxviii_nilpotent_chain_lift_qec_bridge.py",
        "tests/test_cyclic_cayley_obstruction_ccccxxx.py",
        "tests/test_qec_ouroboros_stabilizer_loop_ccccxvii.py",
        "tests/test_fusion_control_scheduler_splice_ccccxxvi.py",
        "tests/test_photonic_harmonic_tqc_bus_ccccxviii.py",
    ],
    "dcc-weld": [
        "tests/test_dccx_holonomy_selector_carrier_weld_bridge.py",
        "tests/test_dccxi_holonomy_weld_associator_support_bridge.py",
        "tests/test_dccxiv_holonomy_signed_triad_a2_projection_bridge.py",
        "tests/test_dccxv_photonic_fusion_syndrome_qec_bridge.py",
        "tests/test_dccxvi_axis_syndrome_selector_codec_bridge.py",
    ],
    "tomotope-klitzing": [
        "tests/test_w33_tomotope_klitzing_partial_operation_commutation.py",
        "tests/test_w33_tomotope_klitzing_six_table_lock.py",
        "tests/test_tomotope_cover_convergence_ledger_cccccxc.py",
    ],
    "sector-split": [
        "tests/test_clifford_percolation_hole_oscillator_ccccclxxxi.py",
        "tests/test_e6_a2_root_refinement_ccccclxxxviii.py",
        "tests/test_tomotope_two_192_mechanisms_cccccxcII.py",
        "tests/test_we6_orbit_phase_shell_ccccclxxxvii.py",
    ],
    "closure-clock": [
        "tests/test_dccxxviii_ternary_quaternion_codec_tower.py",
        "tests/test_dccxxix_pauli_klitzing_codec_ladder_bridge.py",
        "tests/test_dccxxx_clifford_even_quaternion_pauli_bridge.py",
        "tests/test_dccxxxi_loop_closure_clock_bridge.py",
        "tests/test_dccxxxii_closure_clock_codec_flow_bridge.py",
        "tests/test_dccxxxiii_spatial_closure_time_bridge.py",
        "tests/test_dccxxxiv_proper_time_causal_order_bridge.py",
        "tests/test_dccxxxv_closure_interval_invariant_bridge.py",
        "tests/test_dccxxxvi_closure_action_weight_bridge.py",
        "tests/test_dccxxxvii_closure_geodesic_refinement_bridge.py",
        "tests/test_dccxxxviii_closure_bellman_principle_bridge.py",
        "tests/test_dccxxxix_closure_semigroup_propagator_bridge.py",
        "tests/test_dccxl_closure_jordan_resolvent_bridge.py",
        "tests/test_dccxli_closure_resolvent_kernel_bridge.py",
        "tests/test_dccxlii_closure_jordan_residue_bridge.py",
        "tests/test_dccxliii_nilpotent_logarithm_action_bridge.py",
        "tests/test_dccxliv_nilpotent_action_variation_bridge.py",
        "tests/test_dccxlv_nilpotent_hessian_convexity_bridge.py",
        "tests/test_dccxlvi_nilpotent_action_jet_tower_bridge.py",
        "tests/test_dccxlvii_nilpotent_ward_recursion_bridge.py",
        "tests/test_dccxlviii_retarded_green_uniqueness_bridge.py",
        "tests/test_dcclxxiv_closure_transfer_resolvent_equivalence_bridge.py",
    ],
    "pascal-ouroboros": [
        "tests/test_dccxlix_octahedron_closure_phase_space.py",
        "tests/test_dccl_pascal_synergetics_clifford_hierarchy.py",
        "tests/test_dccli_pascal_diagonal_w33_generator.py",
        "tests/test_dcclii_hyperbolic_pascal_600cell_e8.py",
        "tests/test_dccliii_monster_moonshine_w33_bridge.py",
        "tests/test_dccliv_frobenius_selection_and_ouroboros.py",
        "tests/test_dcclv_frobenius_octahedral_edge_phase_lift.py",
    ],
    "selection-tower": [
        "tests/test_dcclv_kissing_number_tower.py",
        "tests/test_dcclvi_sphere_packing_density_tower.py",
        "tests/test_dcclvii_periodic_table_from_w33.py",
        "tests/test_dcclviii_universal_overdetermination.py",
        "tests/test_dcclxvi_octahedral_matrix_tree_density_bridge.py",
    ],
    "audit-core": [
        "tests/test_reproduce_w33_core.py",
        "tests/test_dcclxxii_formula_regime_registry_bridge.py",
        "tests/test_dcccxiv_phenomenology_claim_ledger_audit.py",
        "tests/test_dcccxxvi_post_audit_reconciliation_ledger.py",
    ],
    "markov-e6-burden": [
        "tests/test_tomotope_toroidal_markov_algebraic_closure_bridge.py",
        "tests/test_tomotope_toroidal_markov_cubic_recurrence_bridge.py",
        "tests/test_tomotope_toroidal_markov_generating_function_bridge.py",
        "tests/test_tomotope_toroidal_markov_trace_generating_function_bridge.py",
        "tests/test_tomotope_toroidal_markov_trace_recurrence_bridge.py",
        "tests/test_w33_e6_so10_charge_moment_bridge.py",
        "tests/test_w33_e6_sm_burden_of_proof_bridge.py",
    ],
    "octahedral-dynamics": [
        "tests/test_dccl_octahedral_laplacian_heat_kernel_bridge.py",
        "tests/test_dccli_octahedral_spectral_projector_semigroup_bridge.py",
        "tests/test_dcclii_octahedral_poisson_green_bridge.py",
        "tests/test_dccliii_octahedral_effective_resistance_dirichlet_bridge.py",
        "tests/test_dccliv_octahedral_commute_hitting_time_bridge.py",
        "tests/test_dcclv_octahedral_transition_mixing_bridge.py",
        "tests/test_dcclvi_octahedral_entropy_contraction_bridge.py",
        "tests/test_dcclvii_octahedral_chi_square_contraction_bridge.py",
        "tests/test_dcclviii_octahedral_dobrushin_contraction_bridge.py",
        "tests/test_dcclix_octahedral_exact_mixing_time_bridge.py",
        "tests/test_dcclx_octahedral_return_recurrence_bridge.py",
        "tests/test_dcclxi_octahedral_first_return_renewal_bridge.py",
        "tests/test_dcclxii_octahedral_fundamental_matrix_hitting_bridge.py",
        "tests/test_dcclxiii_inverse_reciprocity_3_13_13_3_bridge.py",
        "tests/test_dcclxiv_reciprocity_rigidity_lazy_deformation_bridge.py",
        "tests/test_dcclxv_running_reciprocity_invariant_bridge.py",
        "tests/test_dcclxvi_octahedral_matrix_tree_density_bridge.py",
        "tests/test_dcclxvii_axis_syndrome_nilpotent_octahedral_bridge.py",
    ],
}

ALIASES = {
    "architecture": [
        "photonic-qec",
        "dcc-weld",
        "tomotope-klitzing",
        "sector-split",
        "closure-clock",
        "pascal-ouroboros",
        "selection-tower",
        "audit-core",
        "octahedral-dynamics",
    ],
}


def expand_suites(names: list[str]) -> list[str]:
    selected: list[str] = []
    for name in names:
        if name in ALIASES:
            selected.extend(expand_suites(ALIASES[name]))
            continue
        if name not in SUITES:
            known = sorted([*SUITES, *ALIASES])
            raise SystemExit(f"Unknown suite {name!r}. Known suites: {', '.join(known)}")
        selected.extend(SUITES[name])

    deduped: list[str] = []
    seen: set[str] = set()
    for path in selected:
        if path not in seen:
            seen.add(path)
            deduped.append(path)
    return deduped


def build_pytest_command(paths: list[str], extra_pytest_args: list[str]) -> list[str]:
    return [
        sys.executable,
        "-m",
        "pytest",
        "--noconftest",
        "-q",
        *paths,
        *extra_pytest_args,
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "suite",
        nargs="*",
        default=["photonic-qec"],
        help=(
            "Suite(s) to run. Known suites: "
            + ", ".join(sorted([*SUITES, *ALIASES]))
            + ". Default: photonic-qec."
        ),
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List suite names and test files without running pytest.",
    )
    args, extra_pytest_args = parser.parse_known_args(argv)
    if extra_pytest_args and extra_pytest_args[0] == "--":
        extra_pytest_args = extra_pytest_args[1:]

    if args.list:
        for name in sorted(SUITES):
            print(f"{name}:")
            for path in SUITES[name]:
                print(f"  {path}")
        for name in sorted(ALIASES):
            print(f"{name}: {', '.join(ALIASES[name])}")
        return 0

    paths = expand_suites(args.suite)
    missing = [path for path in paths if not (ROOT / path).exists()]
    if missing:
        raise SystemExit("Missing test files:\n" + "\n".join(f"  {path}" for path in missing))

    command = build_pytest_command(paths, extra_pytest_args)
    print("Running:", " ".join(command), flush=True)
    return subprocess.call(command, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
