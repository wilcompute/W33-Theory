from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "PART_BT2847_BT2853_PROTECTED_OBSERVER_NOISY_M36_results.json"


def certificate() -> dict:
    return json.loads(CERT.read_text(encoding="utf-8"))


def test_exact_release_certificate() -> None:
    result = certificate()
    assert result["check_count"] == 8
    assert all(result["checks"].values())


def test_fixed_trajectory_and_feature_optima() -> None:
    result = certificate()
    assert result["pass2847_distance4_puncturing"]["minimum_over_family"] == 28
    assert result["pass2848_affine_square_feature_bank"]["distance4_integer_repetition_optimum"] == 24
    assert result["pass2848_affine_square_feature_bank"]["weighted_distance_histogram"]["4"] == 234


def test_symmetry_orders() -> None:
    result = certificate()["pass2849_observer_symmetry"]
    assert result["distance4_word_digraph"]["automorphism_order"] == 32
    assert result["minimal_fast_selector_hypergraph"]["automorphism_order"] == 6912
    assert result["minimal_fast_selector_hypergraph"]["block_orbits"] == 1


def test_noisy_m36_golden_boundary() -> None:
    boundary = certificate()["pass2851_noisy_m36"]["saddle_node"]
    assert abs(boundary["critical_g_decimal"] - 0.07294901687515773) < 1e-14
    assert abs(boundary["critical_p_decimal"] - 0.38196601125010515) < 1e-14


def test_adaptive_and_soft_decoder_boundaries() -> None:
    result = certificate()
    assert result["pass2852_adaptive_observer"]["worst_case_operations"] == 4
    assert result["pass2852_adaptive_observer"]["uniform_mean_exact"] == "94/27"
    scenarios = result["pass2850_soft_decoder"]["scenarios"]
    assert scenarios[0]["hamming_errors"] == scenarios[0]["ml_errors"]
    assert all(item["relative_error_reduction"] >= 0.70 for item in scenarios[1:])


def test_rtl_contracts_present() -> None:
    encoder = (ROOT / "rtl" / "w33_pass2848_affine_square_feature_encoder.sv").read_text(encoding="utf-8")
    decoder = (ROOT / "rtl" / "w33_pass2853_affine_square_nn_decoder.sv").read_text(encoding="utf-8")
    assert "feature[11]" in encoder and "code[2*i+1]" in encoder
    assert "candidate_index == 7'd80" in decoder
    assert "corrected_valid" in decoder
