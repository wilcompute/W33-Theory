from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "analysis" / filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_pass999_a5_double_class_census():
    m = load("pass999_test", "w33_pass999_a5_double_class_census.py")
    p = m.payload()
    assert p["status"] == "PASS"
    assert p["A5_census"]["total_subgroups"] == 432
    assert p["A5_census"]["class_sizes"] == [216, 216]


def test_pass1000_spectral_fingerprint():
    m = load("pass1000_test", "w33_pass1000_a5_signed_turn_spectral_fingerprint.py")
    p = m.payload()
    assert p["status"] == "PASS"
    assert p["fingerprint"]["distinguishing_trace"]["class_A"] == {
        "order3_on_K4": 3,
        "order3_on_K10": 0,
    }
    assert p["fingerprint"]["distinguishing_trace"]["class_B"] == {
        "order3_on_K4": 0,
        "order3_on_K10": 3,
    }


def test_pass1001_full_signed_equivariance():
    m = load("pass1001_test", "w33_pass1001_full_signed_edge_equivariance.py")
    p = m.payload()
    assert p["status"] == "PASS"
    assert p["signed_action"]["commuting_elements"] == 25920
    assert p["unsigned_action"]["commuting_elements"] == 3


def test_pass1002_ramified_kernel_growth():
    m = load("pass1002_test", "w33_pass1002_ramified_kernel_growth_gluing.py")
    p = m.payload()
    assert p["status"] == "PASS"
    cases = {c["name"]: c for c in p["cases"]}
    assert cases["W(3,3)"]["kernel_log2_growth"] == [40, 80, 119, 158, 182]
    assert cases["W(3,3)"]["two_primary_exponent_counts"] == {"1": 15, "3": 1}


def test_pass1003_clique_complex_separator():
    m = load("pass1003_test", "w33_pass1003_chang_clique_complex_separator.py")
    p = m.payload()
    assert p["status"] == "PASS"
    assert p["Euler_secret"]["Euler_characteristics"] == [36, 12, 4]
    assert p["Euler_secret"]["reduced_Euler_characteristics"] == [35, 11, 3]
