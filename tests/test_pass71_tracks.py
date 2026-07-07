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
    return json.loads(Path(outfile).read_text())


def test_track_d_css_condition():
    data = _run("w33_pass71_trackD_css_matrices", "w33_pass71_trackD_css_matrices.json")
    assert data["css_condition_satisfied"] is True
    assert data["n_points"] == 40
    assert data["collinear_pairs"] == 240  # 40 * 12 / 2


def test_track_e_grh():
    data = _run("w33_pass71_trackE_ihara_zeta", "w33_pass71_trackE_ihara_zeta_poles.json")
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
    dD = json.loads(Path("w33_pass71_trackD_css_matrices.json").read_text())
    dE = json.loads(Path("w33_pass71_trackE_ihara_zeta_poles.json").read_text())
    dF = json.loads(Path("w33_pass71_trackF_pmns_angles.json").read_text())
    assert dD["n_points"] == dE["n_vertices"] == dF["spectral_parameters"]["k"] + 28
