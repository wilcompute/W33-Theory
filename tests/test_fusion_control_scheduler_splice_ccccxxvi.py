"""Regression tests for PART CCCCXXVI fusion-control scheduler splice."""

from __future__ import annotations

import importlib.util
import json
import sys
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCCXXVI_FUSION_CONTROL_SCHEDULER_SPLICE.py"
RESULTS_PATH = ROOT / "PART_CCCCXXVI_fusion_control_scheduler_splice_results.json"


@lru_cache(maxsize=1)
def load_module():
    spec = importlib.util.spec_from_file_location("fusion_control_scheduler_splice_ccccxxvi", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def build_results():
    return load_module().build_results()


def test_all_fusion_control_splice_checks_pass():
    results = build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"] == 29
    assert all(check["passed"] for check in results["checks"])


def test_probabilistic_budget_splits_refine_theta_transport_carrier():
    results = build_results()
    fusion = results["fusion_budget_split"]
    klm = results["klm_budget_split"]
    assert fusion["theta_expected_attempts"] == 210
    assert fusion["transport_expected_attempts"] == 270
    assert fusion["total_expected_attempts"] == 480
    assert klm["theta_expected_primitives"] == 420
    assert klm["transport_expected_primitives"] == 540
    assert klm["total_expected_primitives"] == 960
    assert "210 theta + 270 transport" in fusion["read"]
    assert "420 theta + 540 transport" in klm["read"]


def test_qec_tick_refines_scheduler_css_rank():
    qec = build_results()["qec_refinement"]
    assert qec["scheduler_css_tick"] == "39 X-rank + 120 Z-rank + 81 logical = 240"
    assert qec["theta_u5_refined_z_rank"] == "95 + 25 = 120"
    assert qec["full_refined_identity"] == "95 + 25 + 39 + 81 = 240"
    assert qec["active_code"] == "[[82320,81,>=81]]"


def test_snake_closure_keeps_h1_tail_and_classical_selector_distinct():
    snake = build_results()["snake_closure"]
    assert snake["head_projective_frame_states"] == 81
    assert snake["tail_logical_h1"] == 81
    assert snake["classical_selector_trits"] == 40
    assert snake["correctable_weight"] == 40
    assert snake["operation_input"] == "protected H1=81 matter sector"
    assert "starts and ends on the H1=81" in snake["read"]
    assert "V=40" in snake["read"]


def test_splice_layers_cover_probabilistic_qec_deterministic_classical():
    layers = build_results()["splice_layers"]
    assert [layer["name"] for layer in layers] == [
        "probabilistic_fusion_budget",
        "theta_u5_css_refinement",
        "deterministic_frame_lock",
        "classical_selector_commit",
    ]
    assert [layer["regime"] for layer in layers] == [
        "probabilistic",
        "quantum_error_correction",
        "deterministic",
        "classical",
    ]
    assert layers[0]["exact"] == "210+270=480 and 420+540=960"
    assert layers[1]["exact"] == "95+25=120; 120+39+81=240"
    assert layers[2]["exact"] == "3^4=81"
    assert layers[3]["exact"] == "2^63 < 3^40 < 2^64"


def test_theorem_and_boundary_state_the_runtime_splice_honestly():
    results = build_results()
    theorem = results["theorem"]
    assert "eight-tick protected photonic runtime" in theorem
    assert "four-layer theta/U(5) completion" in theorem
    assert "105+135=240" in theorem
    assert "210+270=480" in theorem
    assert "420+540=960" in theorem
    assert "95+25=120" in theorem
    assert "40 trits inside a 64-bit envelope" in theorem
    assert "finite scheduler splice and budget refinement" in results["honesty_boundary"]
    assert "does not simulate optical loss thresholds" in results["honesty_boundary"]


def test_result_artifact_is_present_and_current():
    artifact = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    live = build_results()
    assert artifact["part"] == "CCCCXXVI"
    assert artifact["verified"] is True
    assert artifact["checks_passed"] == artifact["checks_total"] == live["checks_total"]
    assert artifact["fusion_budget_split"] == live["fusion_budget_split"]
    assert artifact["klm_budget_split"] == live["klm_budget_split"]
    assert artifact["qec_refinement"] == live["qec_refinement"]
    assert artifact["snake_closure"] == live["snake_closure"]


def test_docs_index_exposes_fusion_control_scheduler_splice():
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "Fusion-Control Scheduler Splice" in text
    assert "PART_CCCCXXVI_FUSION_CONTROL_SCHEDULER_SPLICE.md" in text
    assert "210+270=480" in text
    assert "420+540=960" in text
    assert "95+25=120" in text
    assert "120+39+81=240" in text
    assert "H1=81" in text
    assert "40-trit selector" in text


def test_single_photon_paper_records_fusion_control_splice():
    text = (ROOT / "single_photon_universal_computation.tex").read_text(encoding="utf-8")
    assert "\\subsection{Fusion-Control Splice}" in text
    assert "5[[21,2,\\ge 3]]=[[105,10,\\ge 3]]" in text
    assert "95+25=120" in text
    assert "95+25+39+81=240" in text
    assert "210+270=480" in text
    assert "420+540=960" in text
    assert "photonic fusion-based fault tolerance~\\cite{Bartolucci2021}" in text
    assert "\\bibitem{Bartolucci2021}" in text
