from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_pass498_fitting_mechanism():
    m = load("p498", "analysis/w33_pass498_fitting_minimum_mechanism.py")
    r = m.main_payload()
    assert r["status"] == "PASS"
    assert r["checks"]["all_exact_high_conductor_points_fit"]
    assert "common quotient" in r["theorem"]


def test_pass499_product_ring_depth_24():
    m = load("p499", "analysis/w33_pass499_product_ring_discriminator.py")
    r = m.main_payload()
    assert r["status"] == "PASS"
    assert r["witness"]["depth"] == 24
    assert r["projective_budget"] == 120
    assert r["separable_slice"]["minimum"] == 60


def test_pass500_galois_cycle_recovers_four_depths():
    m = load("p500", "analysis/w33_pass500_galois_phase_cycle_compiler.py")
    r = m.main_payload()
    assert r["status"] == "PASS"
    assert [x["recovered_depth"] for x in r["synthetic_noisy_recovery"]] == [8, 12, 18, 24]
    assert r["actual_product_ring_witness"]["recovered_lambda_depth"] == 24
    assert [x["time_bin"] for x in r["overlay"]["phase_rows"]] == [2032, 2033, 2034]


def test_pass501_nonisomorphic_budget_collision():
    m = load("p501", "analysis/w33_pass501_small_frobenius_census.py")
    r = m.main_payload()
    assert r["status"] == "PASS"
    assert r["decisive_collision"]["embedding_dimensions"] == [1, 2]
    assert r["decisive_collision"]["witness_1"]["depth"] == 12
    assert r["decisive_collision"]["witness_2"]["depth"] == 12


def test_pass502_formal_support_sources():
    m = load("p502", "analysis/w33_pass502_formal_support.py")
    r = m.main_payload()
    assert r["status"] == "PASS"
    assert r["checks"]["no_sorry"]
    assert r["checks"]["all_gram_examples"]
    assert r["checks"]["all_paired_products_square"]


def test_static_certificates_are_current():
    modules = [
        ("p498c", "analysis/w33_pass498_fitting_minimum_mechanism.py"),
        ("p499c", "analysis/w33_pass499_product_ring_discriminator.py"),
        ("p500c", "analysis/w33_pass500_galois_phase_cycle_compiler.py"),
        ("p501c", "analysis/w33_pass501_small_frobenius_census.py"),
        ("p502c", "analysis/w33_pass502_formal_support.py"),
    ]
    for name, path in modules:
        mod = load(name, path)
        payload = mod.main_payload()
        assert payload["status"] == "PASS"
