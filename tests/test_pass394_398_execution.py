from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, relative: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_pass394_cover_theorem():
    module = load("pass394", "analysis/w33_pass394_antipodal_cover_theorem.py")
    payload = module.build_certificate()
    assert payload["status"] == "PASS"
    assert [rung["q"] for rung in payload["rungs"]] == [3, 5, 7]
    assert all(rung["checks"]["distance_three_classes_are_phase_fibres"] for rung in payload["rungs"])
    assert module.predicted(7)["intersection"] == {
        1: (1, 5, 42),
        2: (7, 40, 1),
        3: (48, 0, 0),
    }


def test_pass395_section_classification():
    module = load("pass395", "analysis/w33_pass395_cayley_section_classification.py")
    payload = module.build_certificate()
    assert payload["status"] == "PASS"
    assert payload["section_space"]["orbit_sizes"] == [9, 72]
    assert payload["canonical_orbit"]["stabilizer_order"] == 48
    assert payload["canonical_orbit"]["graph"]["distance_regular"] is True
    assert payload["nonlinear_orbit"]["graph"]["distance_regular"] is False


def test_pass396_chain_dirac_lift():
    module = load("pass396", "analysis/w33_pass396_pluecker_chain_dirac_lift.py")
    payload = module.build_certificate()
    assert payload["status"] == "PASS"
    assert payload["characteristic_two"]["homology_dimensions"] == {"H_W": 8, "H_Q": 20}
    assert payload["characteristic_two"]["Jordan_type"] == {"J4": 2, "J3": 22, "J2": 0, "J1": 6}
    assert payload["checks"]["Dirac_intertwiner_exact"] is True


def test_pass397_sealed_lab_contract(tmp_path: Path):
    module = load("pass397", "analysis/w33_pass397_sealed_lab_ingestion.py")
    payload = module.contract_test(tmp_path / "contract.json")
    assert payload["status"] == "PASS"
    assert payload["production_has_synthetic_fallback"] is False
    assert all(payload["checks"].values())


def test_pass398_formula_universe_scanner():
    module = load("pass398", "analysis/w33_pass398_formula_search_universe.py")
    payload = module.self_test()
    assert payload["status"] == "PASS"
    assert all(payload["checks"].values())
