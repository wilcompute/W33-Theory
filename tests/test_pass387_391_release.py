from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_pass387_explicit_pluecker_duality():
    module = load_module(
        "w33_pass387",
        "analysis/w33_pass387_pluecker_duality_certificate.py",
    )
    cert = module.build_certificate()
    assert cert["verified"] is True
    assert cert["duality"]["incidence_reversing"] is True
    assert sorted(cert["duality"]["w_line_to_q_point"]) == list(range(40))
    assert sorted(cert["duality"]["w_point_to_q_line"]) == list(range(40))
    assert cert["models"]["W33"]["point_graph_independence_number"] == 7
    assert cert["models"]["Q43"]["point_graph_independence_number"] == 10


def test_pass388_matrix_release_lock(tmp_path: Path):
    module = load_module(
        "w33_pass388",
        "analysis/w33_pass388_css_matrix_release.py",
    )
    manifest = module.build_release(tmp_path)
    assert manifest["verified"] is True
    assert manifest["css"] == {
        "commuting": True,
        "n": 240,
        "k": 81,
        "dX": 3,
        "dZ": 4,
        "parameters": "[[240,81,3]]_3 with asymmetric distances dX=3,dZ=4",
    }
    assert manifest["matrices"]["HX"]["rank"] == 39
    assert manifest["matrices"]["HZ"]["rank"] == 120
    assert manifest["matrices"]["HX"]["nnz"] == 480
    assert manifest["matrices"]["HZ"]["nnz"] == 480


def test_pass390_is_blinded_dry_run_not_physical_data(tmp_path: Path):
    module = load_module(
        "w33_pass390",
        "analysis/w33_pass390_blinded_choi_visibility_dry_run.py",
    )
    raw, key, results = module.build_bundle(tmp_path)
    assert raw["blinded"] is True
    assert raw["gate_labels_present"] is False
    assert len(key["blind_key"]) == 4
    assert results["verified_dry_run"] is True
    assert results["physical_experiment_completed"] is False
    assert results["study_type"] == "synthetic_dry_run_not_physical_data"
    for gate_result in results["unblinded_results"].values():
        assert gate_result["within_preregistered_tolerance"] is True


def test_pass391_prediction_registry_is_frozen_and_honest():
    module = load_module(
        "w33_pass391",
        "analysis/w33_pass391_prediction_registry.py",
    )
    registry = module.build_registry()
    validation = module.validate_registry(registry)
    assert validation["verified"] is True
    assert validation["entry_count"] == 6
    assert validation["prospective_entry_count"] == 1
    alpha = next(entry for entry in registry["entries"] if entry["id"] == "ALPHA-STATIC-001")
    assert alpha["eligibility"] == "ineligible_for_out_of_sample_credit"
    choi = next(entry for entry in registry["entries"] if entry["id"] == "PHOTONIC-CHOI-001")
    assert choi["eligibility"] == "prospective"
    assert choi["observed_value"] is None


def test_committed_outputs_are_verified():
    pass387 = json.loads(
        (ROOT / "data/w33_pass387_pluecker_duality_certificate.json").read_text(encoding="utf-8")
    )
    pass388 = json.loads(
        (ROOT / "data/w33_pass388_css_matrix_release.json").read_text(encoding="utf-8")
    )
    pass390 = json.loads(
        (ROOT / "data/w33_pass390_choi_visibility_results.json").read_text(encoding="utf-8")
    )
    pass391 = json.loads(
        (ROOT / "data/w33_prediction_registry_v1.json").read_text(encoding="utf-8")
    )
    assert pass387["verified"] is True
    assert pass388["verified"] is True
    assert pass390["verified_dry_run"] is True
    assert pass390["physical_experiment_completed"] is False
    assert pass391["validation"]["verified"] is True
