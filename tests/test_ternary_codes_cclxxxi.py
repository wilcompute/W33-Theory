"""Tests for Part CCLXXXI: Ternary Codes, Perfect Codes over GF(3), and the W(3,3) Coding Bridge."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'exploration'))

from PART_CCLXXXI_TERNARY_CODES_BRIDGE import (
    build_cclxxxi_bridge_summary,
    verify_hamming_codes_gf3,
    verify_perfect_code_sphere_packing,
    verify_singleton_plotkin_bounds,
    verify_ternary_golay_code,
    verify_binary_golay_code,
    verify_reed_solomon_codes,
    verify_mds_codes,
    verify_self_dual_ternary_codes,
    verify_repetition_parity_codes,
    verify_code_bounds_atlas,
    verify_krawtchouk_polynomials,
    verify_transport_coding_bridge,
    verify_coset_decoding,
    verify_generator_matrix_properties,
    verify_coding_theory_identities,
    verify_linear_code_families,
    verify_w33_coding_atlas,
)


def test_hamming_codes_gf3():
    passed, count, failures = verify_hamming_codes_gf3()
    assert passed, f"hamming_codes_gf3 failed at indices {failures}"
    assert count > 0


def test_perfect_code_sphere_packing():
    passed, count, failures = verify_perfect_code_sphere_packing()
    assert passed, f"perfect_code_sphere_packing failed at indices {failures}"
    assert count > 0


def test_singleton_plotkin_bounds():
    passed, count, failures = verify_singleton_plotkin_bounds()
    assert passed, f"singleton_plotkin_bounds failed at indices {failures}"
    assert count > 0


def test_ternary_golay_code():
    passed, count, failures = verify_ternary_golay_code()
    assert passed, f"ternary_golay_code failed at indices {failures}"
    assert count > 0


def test_binary_golay_code():
    passed, count, failures = verify_binary_golay_code()
    assert passed, f"binary_golay_code failed at indices {failures}"
    assert count > 0


def test_reed_solomon_codes():
    passed, count, failures = verify_reed_solomon_codes()
    assert passed, f"reed_solomon_codes failed at indices {failures}"
    assert count > 0


def test_mds_codes():
    passed, count, failures = verify_mds_codes()
    assert passed, f"mds_codes failed at indices {failures}"
    assert count > 0


def test_self_dual_ternary_codes():
    passed, count, failures = verify_self_dual_ternary_codes()
    assert passed, f"self_dual_ternary_codes failed at indices {failures}"
    assert count > 0


def test_repetition_parity_codes():
    passed, count, failures = verify_repetition_parity_codes()
    assert passed, f"repetition_parity_codes failed at indices {failures}"
    assert count > 0


def test_code_bounds_atlas():
    passed, count, failures = verify_code_bounds_atlas()
    assert passed, f"code_bounds_atlas failed at indices {failures}"
    assert count > 0


def test_krawtchouk_polynomials():
    passed, count, failures = verify_krawtchouk_polynomials()
    assert passed, f"krawtchouk_polynomials failed at indices {failures}"
    assert count > 0


def test_transport_coding_bridge():
    passed, count, failures = verify_transport_coding_bridge()
    assert passed, f"transport_coding_bridge failed at indices {failures}"
    assert count > 0


def test_coset_decoding():
    passed, count, failures = verify_coset_decoding()
    assert passed, f"coset_decoding failed at indices {failures}"
    assert count > 0


def test_generator_matrix_properties():
    passed, count, failures = verify_generator_matrix_properties()
    assert passed, f"generator_matrix_properties failed at indices {failures}"
    assert count > 0


def test_coding_theory_identities():
    passed, count, failures = verify_coding_theory_identities()
    assert passed, f"coding_theory_identities failed at indices {failures}"
    assert count > 0


def test_linear_code_families():
    passed, count, failures = verify_linear_code_families()
    assert passed, f"linear_code_families failed at indices {failures}"
    assert count > 0


def test_w33_coding_atlas():
    passed, count, failures = verify_w33_coding_atlas()
    assert passed, f"w33_coding_atlas failed at indices {failures}"
    assert count > 0


def test_build_cclxxxi_bridge_summary():
    summary = build_cclxxxi_bridge_summary()
    assert summary["part"] == "CCLXXXI"
    assert summary["all_checks_pass"] is True
    assert summary["total_checks"] == 426
    assert summary["failed_checks"] == []
    assert len(summary["results"]) == 17
