from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_focused_bridge_tests import (  # noqa: E402
    SUITES,
    build_pytest_command,
    expand_suites,
)


def test_focused_bridge_runner_has_expected_core_suites() -> None:
    assert {
        "photonic-qec",
        "dcc-weld",
        "tomotope-klitzing",
        "sector-split",
        "closure-clock",
        "pascal-ouroboros",
        "selection-tower",
        "audit-core",
        "markov-e6-burden",
        "octahedral-dynamics",
    } <= set(SUITES)
    assert "tests/test_dccxv_photonic_fusion_syndrome_qec_bridge.py" in SUITES["photonic-qec"]
    assert "tests/test_dcclxxv_photonic_retry_closure_kernel_bridge.py" in SUITES["photonic-qec"]
    assert "tests/test_dcmii_projective_screen_bulk_qec_bridge.py" in SUITES["photonic-qec"]
    assert "tests/test_dccxl_closure_jordan_resolvent_bridge.py" in SUITES["closure-clock"]
    assert "tests/test_dccxliv_nilpotent_action_variation_bridge.py" in SUITES["closure-clock"]
    assert "tests/test_dccxlv_nilpotent_hessian_convexity_bridge.py" in SUITES["closure-clock"]
    assert "tests/test_dccxlvi_nilpotent_action_jet_tower_bridge.py" in SUITES["closure-clock"]
    assert "tests/test_dccxlvii_nilpotent_ward_recursion_bridge.py" in SUITES["closure-clock"]
    assert "tests/test_dccxlviii_retarded_green_uniqueness_bridge.py" in SUITES["closure-clock"]
    assert "tests/test_dcclxxiv_closure_transfer_resolvent_equivalence_bridge.py" in SUITES["closure-clock"]
    assert "tests/test_dcclv_frobenius_octahedral_edge_phase_lift.py" in SUITES["pascal-ouroboros"]
    assert "tests/test_dcclviii_universal_overdetermination.py" in SUITES["selection-tower"]
    assert "tests/test_reproduce_w33_core.py" in SUITES["audit-core"]
    assert "tests/test_dcclxxii_formula_regime_registry_bridge.py" in SUITES["audit-core"]
    assert "tests/test_dcccxiv_phenomenology_claim_ledger_audit.py" in SUITES["audit-core"]
    assert "tests/test_dccclxxi_frontier_result_ledger_repair.py" in SUITES["audit-core"]
    assert "tests/test_w33_for_everyone_consistency_bridge.py" in SUITES["audit-core"]
    assert "tests/test_dcmi_sub_distinction_boundary_audit.py" in SUITES["audit-core"]
    assert "tests/test_dcmii_projective_screen_bulk_qec_bridge.py" in SUITES["audit-core"]
    assert "tests/test_dcmlxxix_ihara_parameter_reconciliation.py" in SUITES["audit-core"]
    assert (
        "tests/test_tomotope_toroidal_markov_trace_recurrence_bridge.py"
        in SUITES["markov-e6-burden"]
    )
    assert "tests/test_w33_e6_sm_burden_of_proof_bridge.py" in SUITES["markov-e6-burden"]
    assert "tests/test_dcclxvi_octahedral_matrix_tree_density_bridge.py" in SUITES["octahedral-dynamics"]
    assert "tests/test_dcclxvii_axis_syndrome_nilpotent_octahedral_bridge.py" in SUITES["photonic-qec"]
    assert "tests/test_dcclxvii_axis_syndrome_nilpotent_octahedral_bridge.py" in SUITES["octahedral-dynamics"]
    assert "tests/test_dcclxviii_nilpotent_chain_lift_qec_bridge.py" in SUITES["photonic-qec"]


def test_focused_bridge_runner_architecture_alias_dedupes_paths() -> None:
    paths = expand_suites(["architecture"])

    assert "tests/test_dccxv_photonic_fusion_syndrome_qec_bridge.py" in paths
    assert "tests/test_dcclxxv_photonic_retry_closure_kernel_bridge.py" in paths
    assert "tests/test_dccxl_closure_jordan_resolvent_bridge.py" in paths
    assert "tests/test_dccxliv_nilpotent_action_variation_bridge.py" in paths
    assert "tests/test_dccxlv_nilpotent_hessian_convexity_bridge.py" in paths
    assert "tests/test_dccxlvi_nilpotent_action_jet_tower_bridge.py" in paths
    assert "tests/test_dccxlvii_nilpotent_ward_recursion_bridge.py" in paths
    assert "tests/test_dccxlviii_retarded_green_uniqueness_bridge.py" in paths
    assert "tests/test_dcclxxiv_closure_transfer_resolvent_equivalence_bridge.py" in paths
    assert "tests/test_dcclv_frobenius_octahedral_edge_phase_lift.py" in paths
    assert "tests/test_dcclviii_universal_overdetermination.py" in paths
    assert "tests/test_reproduce_w33_core.py" in paths
    assert "tests/test_dcclxxii_formula_regime_registry_bridge.py" in paths
    assert "tests/test_dcccxiv_phenomenology_claim_ledger_audit.py" in paths
    assert "tests/test_dccclxxi_frontier_result_ledger_repair.py" in paths
    assert "tests/test_w33_for_everyone_consistency_bridge.py" in paths
    assert "tests/test_dcmi_sub_distinction_boundary_audit.py" in paths
    assert "tests/test_dcmii_projective_screen_bulk_qec_bridge.py" in paths
    assert "tests/test_dcmlxxix_ihara_parameter_reconciliation.py" in paths
    assert "tests/test_dcclxvi_octahedral_matrix_tree_density_bridge.py" in paths
    assert "tests/test_dcclxvii_axis_syndrome_nilpotent_octahedral_bridge.py" in paths
    assert "tests/test_dcclxviii_nilpotent_chain_lift_qec_bridge.py" in paths
    assert len(paths) == len(set(paths))
    assert len(paths) >= 60


def test_focused_bridge_runner_builds_noconftest_command() -> None:
    command = build_pytest_command(["tests/test_dccxv_photonic_fusion_syndrome_qec_bridge.py"], ["-k", "qec"])

    assert command[:4] == [sys.executable, "-m", "pytest", "--noconftest"]
    assert "-q" in command
    assert command[-2:] == ["-k", "qec"]
