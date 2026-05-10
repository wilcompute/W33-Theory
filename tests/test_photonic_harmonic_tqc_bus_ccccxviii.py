"""Regression tests for PART CCCCXVIII photonic harmonic TQC bus."""

from __future__ import annotations

import importlib.util
import json
import sys
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCCXVIII_PHOTONIC_HARMONIC_TQC_BUS.py"
RESULTS_PATH = ROOT / "PART_CCCCXVIII_photonic_harmonic_tqc_bus_results.json"


@lru_cache(maxsize=1)
def load_module():
    spec = importlib.util.spec_from_file_location("photonic_harmonic_tqc_bus_ccccxviii", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def build_results():
    return load_module().build_results()


def test_all_photonic_harmonic_tqc_bus_checks_pass():
    results = build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"] == 36
    assert all(check["passed"] for check in results["checks"])


def test_probability_denominators_are_topological_harmonic_data():
    packet = build_results()["probability_to_topology"]
    assert packet["p_fusion"] == "1/2"
    assert packet["fusion_denominator"] == 2
    assert packet["fusion_denominator_read"] == "lambda=2 = toric logical qubits = harmonic frequency squared"
    assert packet["p_klm"] == "1/4"
    assert packet["klm_denominator"] == 4
    assert packet["klm_denominator_read"] == "mu=4 = toric GSD = toric stabilizer weight"


def test_harmonic_surface_packet_closes_the_12_shell():
    packet = build_results()["harmonic_surface_packet"]
    assert packet["csaszar"] == {"vertices": 7, "edges": 21, "faces": 14, "genus": 1}
    assert packet["heawood_oscillator"]["vertices"] == 14
    assert packet["heawood_oscillator"]["edges"] == 21
    assert packet["heawood_oscillator"]["cycle_rank"] == 8
    assert packet["heawood_oscillator"]["frequency_squared"] == 2
    assert packet["heawood_oscillator"]["middle_shell"] == 12
    assert packet["heawood_oscillator"]["branch_size"] == 6
    assert packet["heawood_gap_exact"] == "3 - sqrt(2)"
    assert packet["tetra_weight_for_same_gap_exact"] == "3/4 - sqrt(2)/4"
    assert packet["middle_shell_read"] == "12 = W33 degree = 6+6 harmonic branches = 3 toric weight-4 checks"


def test_protected_tqc_packet_keeps_q4_as_routing_and_steane_as_protection():
    packet = build_results()["protected_tqc_packet"]
    assert packet["base_css_code"] == "[[240,81,3]]"
    assert packet["q4_local_routing_code"] == "[[1296,81,4]]"
    assert packet["active_protection_code"] == "[[82320,81,>=81]]"
    assert packet["logical_sector"] == 81
    assert packet["correctable_weight"] == 40
    assert packet["selector_trits"] == 40


def test_bus_layers_are_ordered_from_photons_to_selector():
    layers = build_results()["bus_layers"]
    assert [layer["name"] for layer in layers] == [
        "photonic_denominator_bus",
        "heawood_harmonic_bus",
        "toric_surface_bus",
        "protected_qec_bus",
        "classical_selector_bus",
    ]
    assert "hardware randomness" in layers[0]["role"]
    assert "two Phi6 rails" in layers[1]["role"]
    assert "topological loop memory" in layers[2]["role"]
    assert "H1=81 tail" in layers[3]["role"]
    assert "protected acceptance" in layers[4]["role"]


def test_theorem_and_boundary_keep_claim_honest():
    results = build_results()
    assert "p_fusion=1/2" in results["theorem"]
    assert "p_KLM=1/4" in results["theorem"]
    assert "14=2*Phi6" in results["theorem"]
    assert "12=6+6" in results["theorem"]
    assert "[[82320,81,>=81]]" in results["theorem"]
    assert "Q4 remains local [[1296,81,4]]" in results["theorem"]
    assert "not claim a new optical threshold" in results["honesty_boundary"]
    assert "physical anyon implementation" in results["honesty_boundary"]


def test_result_artifact_is_present_and_current():
    artifact = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    live = build_results()
    assert artifact["part"] == "CCCCXVIII"
    assert artifact["verified"] is True
    assert artifact["checks_passed"] == artifact["checks_total"] == live["checks_total"]
    assert artifact["probability_to_topology"] == live["probability_to_topology"]
    assert artifact["protected_tqc_packet"] == live["protected_tqc_packet"]


def test_docs_index_exposes_photonic_harmonic_tqc_bus():
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "Photonic Harmonic TQC Bus" in text
    assert "PART_CCCCXVIII_PHOTONIC_HARMONIC_TQC_BUS.md" in text
    assert "fusion denominator <code>2</code>" in text
    assert "KLM denominator <code>4</code>" in text
    assert "Heawood <code>14=2&Phi;<sub>6</sub></code>" in text
    assert "middle shell <code>12=6+6</code>" in text
    assert "[[82320,81,&ge;81]]" in text
