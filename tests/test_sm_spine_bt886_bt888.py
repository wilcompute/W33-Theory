#!/usr/bin/env python3
"""Regression test locking in the BT858-888 Standard-Model spine.

Protects the master theorem (BT886: the discrete SM is the long-root
transvection geometry of W(3,3)) and the deepest unification
(BT888: color is the matter-shell Heisenberg group) against future
changes.  Runs the witness scripts and asserts their JSON outputs.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run_script(rel):
    subprocess.run([sys.executable, str(ROOT / rel)], cwd=ROOT, check=True)


def load(rel):
    with (ROOT / rel).open() as f:
        return json.load(f)


def test_bt886_standard_model_spine():
    run_script("analysis/bt886_standard_model_spine.py")
    d = load("data/bt886_standard_model_spine.json")
    assert d["PSp"] == 25920
    assert d["R_fixed"] == 13 and d["R_shell_orbits"] == 9
    assert d["gauge_order"] == 648 and d["gauge_rank"] == 3
    assert d["gauge_module"] == "1+3+8"
    assert d["generations_eq_center"] is True
    assert d["matter_grading"] == [9, 9, 9]
    assert d["flat_holonomy"] == 9 and d["curved_holonomy"] == 24


def test_bt888_color_is_matter_heisenberg():
    run_script("analysis/bt888_color_is_matter_heisenberg.py")
    d = load("data/bt888_color_is_matter_heisenberg.json")
    assert d["N_order"] == 27 and d["N_heisenberg"] is True
    assert d["regular_on_matter_shell"] is True
    assert d["color_radical_electroweak_invariant_dim"] == 4
    assert d["gluon_octet_dim"] == 8


def test_bt887_color_electroweak_factorization():
    run_script("analysis/bt887_color_electroweak_factorization.py")
    d = load("data/bt887_color_electroweak_factorization.json")
    assert d["gauge_order"] == 648
    assert d["colour_radical_order"] == 27
    assert d["electroweak_levi_order"] == 24
    assert d["electroweak_invariant_dim"] == 4
    assert d["gluon_octet_dim"] == 8


def test_bt880_generation_is_gauge_center():
    run_script("analysis/bt880_generation_is_gauge_center.py")
    d = load("data/bt880_generation_is_gauge_center.json")
    assert d["gauge_order"] == 648
    assert d["Z_equals_R_Z3"] is True
    assert d["R_trivial_on_gauge_bosons"] is True


if __name__ == "__main__":
    test_bt886_standard_model_spine()
    test_bt888_color_is_matter_heisenberg()
    test_bt887_color_electroweak_factorization()
    test_bt880_generation_is_gauge_center()
    print("all SM-spine regression tests pass")
