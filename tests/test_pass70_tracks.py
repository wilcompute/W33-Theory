"""Pytest suite for Pass 70 tracks A-C."""
from __future__ import annotations

import json
import math
from pathlib import Path
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _run_and_load(module_name: str, output_file: str) -> dict:
    import importlib
    mod = importlib.import_module(module_name)
    mod.main()
    return json.loads(Path(output_file).read_text(encoding="utf-8"))


def test_track_a_ramanujan() -> None:
    data = _run_and_load("w33_pass70_trackA_ramanujan", "w33_pass70_trackA_ramanujan.json")
    assert data["is_ramanujan"] is False
    expected_bound = 2 * math.sqrt(7)
    assert abs(data["ramanujan_bound"] - expected_bound) < 1e-12
    assert data["lambda2"] > data["ramanujan_bound"]


def test_track_b_qec() -> None:
    data = _run_and_load("w33_pass70_trackB_qec", "w33_pass70_trackB_qec.json")
    assert data["length_n"] == 360
    assert data["logical_dimension_k"] == 9
    assert data["distance_lower_bound"] >= 1


def test_track_c_partition() -> None:
    data = _run_and_load("w33_pass70_trackC_partition", "w33_pass70_trackC_partition.json")
    assert data["beta_c"] > 0
    assert data["T_c"] > 0
    expected_lambda2 = (1 + math.sqrt(97)) / 2
    assert abs(data["lambda2"] - expected_lambda2) < 1e-12


def test_cross_track_lambda2_consistency() -> None:
    dataA = json.loads(Path("w33_pass70_trackA_ramanujan.json").read_text(encoding="utf-8"))
    dataC = json.loads(Path("w33_pass70_trackC_partition.json").read_text(encoding="utf-8"))
    assert abs(dataA["lambda2"] - dataC["lambda2"]) < 1e-12
