"""Regression tests for Passes 11802-11807 (levels, charge quantisation, exotic obstruction, up texture, Z6-II scope)."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import w33_pass11802_11807_levels_charges_textures as L  # noqa: E402

DATA = ROOT / "data"


def test_flagship_from_frozen_input():
    mods = {m["label"]: m for m in L.load()}
    r = L.analyse(mods["SM_20260917_3"])
    assert r["sm_in_su9"] and abs(r["net_32"]) == 3 and r["net_32_untwisted"] == 3
    assert all("single level" in k for k in r["twisted_integral_profiles"])
    assert not any(eval(k)[0] and not eval(k)[1] for k in r["charge_census"])
    assert r["class_unbalanced_weights"] > 0
    assert list(r["up_cubics_allowed_by_plane_rule"]) == ["Q(1, 2) u(1, 2) Woo(3,)"]
    assert "0" in r["higgs_component_charges"]


def test_weinberg_and_benchmark():
    assert L.weinberg_level_trace() == "3/8"
    b = L.benchmark_classes()
    assert all(v == [84, 84] for k, v in b.items() if k != "reading")


def test_certificate():
    c = json.load(open(DATA / "w33_pass11802_11807_levels_charges_textures.json"))
    assert c["core_models"] == 33 and c["p11803_every_fractional_charge_has_fractional_occupation"]
    assert c["p11804_models_class_unbalanced"] == 33
    assert c["p11805_up_cubic_patterns"] == {'["Q(1, 2) u(1, 2) Woo(3,)"]': 31, "[]": 2}
    assert c["p11805_sin2_theta_w"] == "3/8"
    assert c["p11806_z6ii"]["a8_models"] == 13
    assert c["p11807_bracket"] == {"nonzero": 1680, "expected": 1680, "non_partition": 0, "coupling_over_sign": [1.0]}
