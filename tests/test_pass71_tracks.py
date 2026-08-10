"""Pytest suite for Pass 71 Tracks D, E, F."""
from __future__ import annotations
import json
import math
import importlib
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _run(module: str, outfile: str) -> dict:
    mod = importlib.import_module(module)
    mod.main()
    return json.loads(Path(outfile).read_text(encoding="utf-8"))


def test_track_d_css_obstruction():
    data = _run("w33_pass71_trackD_css_matrices", "w33_pass71_trackD_css_matrices.json")
    assert data["audit_pass"] is True
    assert data["css_condition_satisfied"] is False
    assert data["css_product_equals_adjacency"] is True
    assert data["css_product_rank"] == 16
    assert data["css_product_weight"] == 480
    assert data["adjacency_square_zero_mod2"] is True
    assert data["claimed_code"] is None
    assert data["n_points"] == 40
    assert data["collinear_pairs"] == 240  # 40 * 12 / 2


def test_track_e_grh():
    data = _run("w33_pass71_trackE_ihara_zeta", "w33_pass71_trackE_ihara_zeta_poles.json")
    assert data["pole_classification_audit_pass"] is True
    assert data["perron_factor"] == "1 - 12u + 11u^2 = (1-u)(1-11u)"
    assert data["perron_trivial_poles"] == [1.0, 1.0 / 11.0]
    assert data["nontrivial_vertex_factor_root_count"] == 78
    assert abs(data["nontrivial_root_modulus_squared"] - 1.0 / 11.0) < 1e-12
    assert data["grh_satisfied"] is True
    assert data["grh_violations"] == 0
    expected_radius = 1.0 / math.sqrt(11)
    assert abs(data["grh_radius"] - expected_radius) < 1e-10
    assert data["n_edges"] == 240


def test_track_f_pmns_angles():
    data = _run("w33_pass71_trackF_pmns_angles", "w33_pass71_trackF_pmns_angles.json")
    assert "w33_predictions" in data
    assert "pdg_2024_values" in data
    assert 0.0 < data["w33_predictions"]["theta_12_deg"] < 90.0
    assert 0.0 < data["w33_predictions"]["theta_13_deg"] < 90.0


def test_cross_track_vertex_count():
    dD = json.loads(Path("w33_pass71_trackD_css_matrices.json").read_text(encoding="utf-8"))
    dE = json.loads(Path("w33_pass71_trackE_ihara_zeta_poles.json").read_text(encoding="utf-8"))
    dF = json.loads(Path("w33_pass71_trackF_pmns_angles.json").read_text(encoding="utf-8"))
    assert dD["n_points"] == dE["n_vertices"] == dF["spectral_parameters"]["k"] + 28
