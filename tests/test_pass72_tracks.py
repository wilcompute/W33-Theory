"""Pytest suite for Pass 72 tracks G-I."""
from __future__ import annotations

import importlib
import json
from pathlib import Path
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _run(module: str, outfile: str) -> dict:
    mod = importlib.import_module(module)
    mod.main()
    return json.loads(Path(outfile).read_text(encoding="utf-8"))


def test_track_g_gap_positive() -> None:
    data = _run("w33_pass72_trackG_yang_mills_gap", "w33_pass72_trackG_yang_mills_gap.json")
    assert data["delta_graph_units"] == 6.0
    assert data["mass_gap_lower_natural_units"] > 0


def test_track_h_ckm_outputs() -> None:
    data = _run("w33_pass72_trackH_ckm_matrix", "w33_pass72_trackH_ckm_matrix.json")
    assert data["spread_decomposition"]["total_spreads"] == 27
    assert data["ckm_moduli"]["Vus"] > 0
    assert data["ckm_moduli"]["Vub"] > 0
    assert data["ckm_moduli"]["Vcb"] > 0


def test_track_i_koide_window() -> None:
    data = _run("w33_pass72_trackI_koide_formula", "w33_pass72_trackI_koide_formula.json")
    assert 0.0 < data["koide_Q"] < 1.0
    assert data["relative_error"] >= 0.0
