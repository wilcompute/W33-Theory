#!/usr/bin/env python3
"""Focused direct test for BT827 photonic holonet architecture."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def run_script(relpath: str) -> None:
    subprocess.run([sys.executable, str(ROOT / relpath)], cwd=ROOT, check=True)


def load_json(relpath: str) -> dict:
    with (ROOT / relpath).open() as f:
        return json.load(f)


def test_bt827_fractal_architecture_scaling():
    run_script("analysis/bt827_holonet_fractal_architecture.py")
    data = load_json("data/bt827_holonet_fractal_architecture.json")
    assert data["single_core"]["runtime_factorization"] == "24 * 2160 = 24 * 45 * 48"
    assert data["single_core"]["mirror_slots"] == 2160
    assert data["single_core"]["tomotope_middle_blocks"] == 48
    assert data["fractal_scaling"]["reversible_route_bound"] == "8n = 8 log_40(N)"
    assert data["fractal_scaling"]["persistent_commit_ticks"] == "T(0)=1, T(g)=4(7^g-1) for g>=1"

    levels = data["fractal_scaling"]["levels"]
    assert levels[0]["level"] == 1
    assert levels[0]["leaf_photonic_cores"] == 40
    assert levels[0]["w33_instances_total"] == 1
    assert levels[0]["reversible_route_hops_bound"] == 8
    assert levels[1]["leaf_photonic_cores"] == 1600
    assert levels[1]["w33_instances_total"] == 41
    assert levels[1]["reversible_route_hops_bound"] == 16

    checks = data["checks"]
    assert all(checks.values())
    assert data["universal_computation"]["minimal_classical_signature"] == "lambda states, q symbols = (2,3)"


if __name__ == "__main__":
    test_bt827_fractal_architecture_scaling()
    print("BT827 photonic holonet architecture test passed")
