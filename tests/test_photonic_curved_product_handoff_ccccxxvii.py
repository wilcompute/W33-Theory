"""Regression tests for PART CCCCXXVII photonic curved product handoff."""

from __future__ import annotations

import importlib.util
import json
import sys
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCCXXVII_PHOTONIC_CURVED_PRODUCT_HANDOFF.py"
RESULTS_PATH = ROOT / "PART_CCCCXXVII_photonic_curved_product_handoff_results.json"


@lru_cache(maxsize=1)
def load_module():
    spec = importlib.util.spec_from_file_location("photonic_curved_product_handoff_ccccxxvii", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def build_results():
    return load_module().build_results()


def test_all_photonic_curved_handoff_checks_pass():
    results = build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"] == 36
    assert all(check["passed"] for check in results["checks"])


def test_protected_finite_kernel_survives_curved_handoff():
    finite = build_results()["protected_finite_kernel"]
    assert finite["active_code"] == "[[82320,81,>=81]]"
    assert finite["h1_logical"] == 81
    assert finite["selector_trits"] == 40
    assert finite["edge_carrier"] == 240
    assert finite["fusion_budget"]["total_expected_attempts"] == 480
    assert finite["klm_budget"]["total_expected_primitives"] == 960


def test_curved_external_seeds_are_explicit_cp2_and_k3_packages():
    seeds = build_results()["curved_external_seeds"]
    assert seeds["CP2_9"]["vertices"] == 9
    assert seeds["CP2_9"]["betti_numbers"] == [1, 0, 1, 0, 1]
    assert seeds["CP2_9"]["harmonic_total"] == 3
    assert seeds["CP2_9"]["total_chain_dim"] == 255
    assert seeds["K3_16"]["vertices"] == 16
    assert seeds["K3_16"]["betti_numbers"] == [1, 0, 22, 0, 1]
    assert seeds["K3_16"]["harmonic_total"] == 24
    assert seeds["K3_16"]["total_chain_dim"] == 1704
    assert seeds["K3_16"]["h2_signature_split"] == [3, 19]


def test_h1_logical_tail_lifts_to_curved_harmonic_channels():
    channels = build_results()["logical_harmonic_channels"]
    assert channels["CP2_9_by_degree"] == [81, 0, 81, 0, 81]
    assert channels["CP2_9_total"] == 243
    assert channels["K3_16_by_degree"] == [81, 0, 1782, 0, 81]
    assert channels["K3_16_middle_h2"] == 1782
    assert channels["K3_16_total"] == 1944


def test_density_limits_and_a2_transport_product_are_exact():
    results = build_results()
    density = results["density_limits"]
    assert density["external_chain"] == "120/19"
    assert density["external_trace"] == "860/19"
    assert density["w33_product_chain"] == "19440/19"
    assert density["w33_product_trace"] == "7512120/19"
    assert density["a2_product_chain"] == "10800/19"
    assert density["a2_product_trace"] == "423000/19"

    a2 = results["a2_transport_product"]
    assert a2["internal_dimension"] == 90
    assert a2["positive_gap"] == 24
    assert a2["laplacian_spectrum"] == {"24": 20, "33": 64, "48": 6}
    assert a2["cp2_product_dimension"] == 22950
    assert a2["k3_product_dimension"] == 153360
    assert a2["product_zero_modes_vanish_exactly"] is True


def test_handoff_read_keeps_external_4d_scale_explicit():
    handoff = build_results()["handoff_read"]
    assert handoff["finite_runtime_degree"] == 12
    assert handoff["external_dimension"] == 4
    assert handoff["finite_plus_external"] == 16
    assert handoff["k3_seed_vertices"] == 16
    assert "genuine curved factor supplies dimension 4" in handoff["read"]
    assert "K3_16 seed scale" in handoff["read"]


def test_theorem_and_boundary_do_not_overclaim_continuum_gravity():
    results = build_results()
    theorem = results["theorem"]
    assert "almost-commutative product" in theorem
    assert "H1=81 logical tail lifts to 243 and 1944" in theorem
    assert "Product heat traces factorize" in theorem
    assert "positive gap 24" in theorem
    assert "finite-to-curved product handoff" in results["honesty_boundary"]
    assert "not the final Einstein-Hilbert spectral-action asymptotic theorem" in results["honesty_boundary"]
    assert "finite kernel does not by itself create a 4D Weyl law" in results["honesty_boundary"]


def test_result_artifact_is_present_and_current():
    artifact = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    live = build_results()
    assert artifact["part"] == "CCCCXXVII"
    assert artifact["verified"] is True
    assert artifact["checks_passed"] == artifact["checks_total"] == live["checks_total"]
    assert artifact["protected_finite_kernel"] == live["protected_finite_kernel"]
    assert artifact["curved_external_seeds"] == live["curved_external_seeds"]
    assert artifact["logical_harmonic_channels"] == live["logical_harmonic_channels"]
    assert artifact["density_limits"] == live["density_limits"]


def test_docs_index_exposes_photonic_curved_product_handoff():
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "Photonic Curved Product Handoff" in text
    assert "PART_CCCCXXVII_PHOTONIC_CURVED_PRODUCT_HANDOFF.md" in text
    assert "CP2_9" in text
    assert "K3_16" in text
    assert "243" in text
    assert "1944" in text
    assert "120/19" in text
    assert "860/19" in text
    assert "gap 24" in text
