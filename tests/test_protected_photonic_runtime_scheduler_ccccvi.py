"""Regression tests for PART CCCCVI protected photonic runtime scheduler."""

from __future__ import annotations

import importlib.util
import json
import sys
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCCVI_PROTECTED_PHOTONIC_RUNTIME_SCHEDULER.py"
RESULTS_PATH = ROOT / "PART_CCCCVI_protected_photonic_runtime_scheduler_results.json"


@lru_cache(maxsize=1)
def load_module():
    spec = importlib.util.spec_from_file_location("protected_photonic_runtime_scheduler_ccccvi", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def build_results():
    return load_module().build_results()


def test_all_scheduler_checks_pass():
    results = build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 31
    assert all(check["passed"] for check in results["checks"])


def test_scheduler_stage_sequence_is_exact():
    stages = build_results()["scheduler_stages"]
    assert [stage["tick"] for stage in stages] == list(range(8))
    assert [stage["name"] for stage in stages] == [
        "projective_carrier",
        "heralded_fusion_assembly",
        "klm_primitive_budget",
        "css_resource_validation",
        "mbqc_feedforward",
        "steane_phi6_protection",
        "classical_selector_commit",
        "e8_z3_operation_gate",
    ]
    assert stages[1]["regime"] == stages[2]["regime"] == "probabilistic"
    assert stages[4]["regime"] == "deterministic"
    assert stages[6]["regime"] == "classical"


def test_controller_envelope_closes_on_w33_scales():
    envelope = build_results()["controller_envelope"]
    assert envelope["measurement_trits"] == 40
    assert envelope["controller_bits"] == 64
    assert envelope["pauli_frame_states"] == 81
    assert envelope["pauli_frame_bits"] == 7
    assert envelope["projective_frame_states"] == 40
    assert envelope["projective_frame_bits"] == 6
    assert 2**63 < int(envelope["measurement_states"]) < 2**64


def test_handoff_contract_names_all_layer_boundaries():
    contract = build_results()["handoff_contract"]
    assert set(contract) == {
        "probabilistic_to_quantum",
        "quantum_to_deterministic",
        "deterministic_to_protected",
        "protected_to_classical",
        "protected_to_operation",
    }
    assert "240 W33 bonds" in contract["probabilistic_to_quantum"]
    assert "81-state Pauli frame" in contract["quantum_to_deterministic"]
    assert "[[1680,81,9]]" in contract["deterministic_to_protected"]
    assert "[[82320,81,>=81]]" in contract["deterministic_to_protected"]
    assert "correcting 40 faults" in contract["deterministic_to_protected"]
    assert "64-bit-class" in contract["protected_to_classical"]
    assert "E8 Z3" in contract["protected_to_operation"]


def test_theorem_states_the_full_runtime_path():
    theorem = build_results()["theorem"]
    assert "eight-tick scheduler" in theorem
    assert "p_fusion=1/2" in theorem
    assert "p_KLM=1/4" in theorem
    assert "[[82320,81,>=81]]" in theorem
    assert "64-bit envelope" in theorem
    assert "E8 Z3 gate" in theorem


def test_scheduler_reconciles_upstream_distance_amplification():
    results = build_results()
    check_values = {check["name"]: check["value"] for check in results["checks"]}
    assert "upstream distance amplification artifact verified" in check_values
    assert check_values["upstream first Steane amplification is [[1680,81,9]]"]["n"] == 1680
    reconciliation = check_values["local three-lift protection matches upstream tower level 3"]
    assert reconciliation["upstream_level_3"]["n"] == 82320
    assert reconciliation["upstream_level_3"]["d"] == 81
    assert reconciliation["local_lift"]["distance_lower_bound"] == 81


def test_result_artifact_is_present_and_current():
    artifact = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    live = build_results()
    assert artifact["part"] == "CCCCVI"
    assert artifact["verified"] is True
    assert artifact["checks_passed"] == artifact["checks_total"] == live["checks_total"]
    assert artifact["controller_envelope"] == live["controller_envelope"]
    assert artifact["handoff_contract"] == live["handoff_contract"]


def test_docs_index_exposes_runtime_scheduler():
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "Protected Photonic Runtime Scheduler" in text
    assert "PART_CCCCVI_PROTECTED_PHOTONIC_RUNTIME_SCHEDULER.md" in text
    assert "eight-tick contract" in text
    assert "deterministic MBQC feed-forward" in text
    assert "64-bit-class selector commit" in text
    assert "[[1680,81,9]]" in text


def test_single_photon_paper_records_scheduler():
    text = (ROOT / "single_photon_universal_computation.tex").read_text(encoding="utf-8")
    assert "\\subsection{Protected Scheduler}" in text
    assert "[[240,81,3]]\\to[[82320,81,\\ge81]]" in text
    assert "Runtime scheduler ticks" in text
    assert "\\bibitem{Steane1996}" in text
    assert "listed cardinal numbers" in text
