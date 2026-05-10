"""Regression tests for PART CCCCXXIII A(7) representation / Csaszar CSS toric code."""

from __future__ import annotations

import importlib.util
import json
import sys
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCCXXIII_A7_REPRESENTATION_CSS_TORIC.py"
RESULTS_PATH = ROOT / "PART_CCCCXXIII_a7_representation_css_toric_results.json"


@lru_cache(maxsize=1)
def load_module():
    spec = importlib.util.spec_from_file_location("a7_representation_css_toric_ccccxxiii", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def build_results():
    return load_module().build_results()


def test_all_a7_css_toric_checks_pass():
    results = build_results()
    assert results["verified"] is True
    assert results["status"] == "PASS"
    assert results["checks_passed"] == results["checks_total"] == 48
    assert all(check["passed"] for check in results["checks"])


def test_a7_u7_su7_g2_algebra_chain():
    results = build_results()
    algebra = results["algebra"]
    assert algebra["modes"] == 7
    assert algebra["u7_dim"] == 49
    assert algebra["su7_dim"] == 48
    assert algebra["g2_dim"] == 14
    assert algebra["bond_g2_adj"] == 14
    assert algebra["bond_g2_fund"] == 7
    assert algebra["bond_g2_adj"] + algebra["bond_g2_fund"] == 21


def test_k7_single_particle_spectrum():
    spectrum = build_results()["k7_spectrum"]
    assert spectrum["max_eig"] == 6
    assert spectrum["min_eig"] == -1
    assert spectrum["spectral_gap"] == 7
    assert spectrum["ground_energy"] == -6
    assert spectrum["det_adj"] == 6


def test_fano_cubic_interaction_closes_g2_dimension():
    mod = load_module()
    counts = mod._mode_line_counts()
    assert len(mod.FANO_LINES) == mod.PHI6 == 7
    assert all(len(line) == mod.Q for line in mod.FANO_LINES)
    assert counts == [mod.Q] * mod.PHI6
    assert 2 * len(mod.FANO_LINES) == mod.G2_DIM == 14
    assert mod.PSL27_ORDER == 24 * mod.PHI6 == 168


def test_csaszar_k7_css_toric_code_parameters():
    results = build_results()
    css = results["css_code"]
    assert css["n"] == 21
    assert css["k"] == 2
    assert css["d_lower"] == 3
    assert css["gsd"] == 4
    assert css["rank_hz"] == 6
    assert css["rank_hx"] == 13
    assert css["n"] - css["rank_hz"] - css["rank_hx"] == css["k"]


def test_chain_complex_has_torus_betti_numbers():
    betti = build_results()["betti"]
    assert betti == {"beta_0": 1, "beta_1": 2, "beta_2": 1, "euler": 0}


def test_css_boundary_of_boundary_zero():
    mod = load_module()
    edges = mod._k7_edges()
    hz = mod._build_hz(edges)
    hx = mod._build_hx(edges, mod.CSASZAR_FACES)
    assert mod._check_css_condition(hx, hz) is True
    assert mod._gf2_rank(hz) == 6
    assert mod._gf2_rank(hx) == 13


def test_result_artifact_is_present_and_current():
    artifact = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    live = build_results()
    assert artifact["part"] == "CCCCXXIII"
    assert artifact["verified"] is True
    assert artifact["checks_passed"] == artifact["checks_total"] == live["checks_total"]
    assert artifact["algebra"] == live["algebra"]
    assert artifact["css_code"] == live["css_code"]
    assert artifact["betti"] == live["betti"]


def test_docs_index_exposes_a7_css_toric_bridge():
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "A(7) Representation Theory and Cs" in text
    assert "PART_CCCCXXIII_A7_REPRESENTATION_CSS_TORIC_BRIDGE.md" in text
    assert "U(7)=49" in text
    assert "SU(7)=48" in text
    assert "G<sub>2</sub>=14" in text
    assert "21=14+7" in text
    assert "[[21,2,&ge;3]]" in text
    assert "48 checks" in text
