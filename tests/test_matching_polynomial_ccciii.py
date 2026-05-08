"""
Tests for CCCIII: Matching Polynomial and Matchings in W(3,3)
"""

import pytest
import sys
import pathlib

# Add exploration folder to path
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "exploration"))

from PART_CCCIII_MATCHING_POLYNOMIAL_BRIDGE import (
    matching_number_upper_bound,
    matching_number_from_regularity,
    max_matching_size,
    perfect_matching_exists,
    matching_poly_degree,
    edge_coloring_class,
    edge_coloring_perfect_matchings,
    matching_poly_m0,
    matching_poly_m1,
    matching_poly_m2,
    matching_poly_m3,
    matching_poly_derivative_at_0,
    matching_poly_at_1,
    matching_poly_at_minus_1,
    independence_poly_from_matching,
    number_of_perfect_matchings_estimate,
    matching_poly_sum_coeffs,
    sm_crosswalk,
    verify_all,
    build_ccciii_summary,
    V, K, EDGES, ALPHA,
)


class TestBasicMatchingProperties:
    """Test basic matching number properties."""

    def test_matching_number_upper_bound_20(self):
        assert matching_number_upper_bound() == 20

    def test_matching_number_from_regularity_20(self):
        assert matching_number_from_regularity() == 20

    def test_max_matching_size_20(self):
        assert max_matching_size() == 20

    def test_matching_number_le_v_over_2(self):
        assert max_matching_size() <= V // 2

    def test_perfect_matching_exists(self):
        assert perfect_matching_exists() is True

    def test_v_is_even(self):
        assert V % 2 == 0

    def test_matching_poly_degree_20(self):
        assert matching_poly_degree() == 20


class TestMatchingPolyCoefficients:
    """Test matching polynomial coefficients."""

    def test_m0_eq_1(self):
        assert matching_poly_m0() == 1

    def test_m1_eq_edges(self):
        assert matching_poly_m1() == EDGES

    def test_m1_eq_240(self):
        assert matching_poly_m1() == 240

    def test_m2_eq_26040(self):
        assert matching_poly_m2() == 26040

    def test_m2_gt_m1(self):
        assert matching_poly_m2() > matching_poly_m1()

    def test_m3_positive(self):
        assert matching_poly_m3() > 0

    def test_m_coeffs_form_sequence(self):
        """m_0 < m_1 < m_2 generally increasing at start."""
        assert matching_poly_m0() < matching_poly_m1() < matching_poly_m2()

    def test_m2_ne_m1(self):
        """m_2 significantly different from m_1."""
        assert matching_poly_m2() != matching_poly_m1()

    def test_m2_is_about_100x_m1(self):
        """m_2 ≈ 108 * m_1."""
        ratio = matching_poly_m2() / matching_poly_m1()
        assert 100 < ratio < 120


class TestMatchingPolyEvaluation:
    """Test matching polynomial at specific points."""

    def test_derivative_at_0_eq_edges(self):
        assert matching_poly_derivative_at_0() == EDGES

    def test_derivative_at_0_eq_240(self):
        assert matching_poly_derivative_at_0() == 240

    def test_poly_at_1_positive(self):
        assert matching_poly_at_1() > 0

    def test_poly_at_minus_1_negative(self):
        assert matching_poly_at_minus_1() < 0

    def test_poly_at_1_gt_poly_at_minus_1(self):
        assert matching_poly_at_1() > matching_poly_at_minus_1()

    def test_poly_at_minus_1_alternating_sum(self):
        """m(G, -1) = m_0 - m_1 + m_2 - m_3."""
        expected = matching_poly_m0() - matching_poly_m1() + matching_poly_m2() - matching_poly_m3()
        assert matching_poly_at_minus_1() == expected

    def test_sum_coeffs_positive(self):
        assert matching_poly_sum_coeffs() > 0


class TestEdgeColoring:
    """Test edge coloring properties."""

    def test_edge_coloring_chi_prime_K(self):
        assert edge_coloring_class() == K

    def test_edge_coloring_chi_prime_12(self):
        assert edge_coloring_class() == 12

    def test_edge_coloring_perfect_matchings_K(self):
        assert edge_coloring_perfect_matchings() == K

    def test_edge_coloring_perfect_matchings_12(self):
        assert edge_coloring_perfect_matchings() == 12

    def test_edge_coloring_decomposes_to_perfect_matchings(self):
        """Graph decomposes into K edge-disjoint perfect matchings."""
        chi_prime = edge_coloring_class()
        num_decomp = edge_coloring_perfect_matchings()
        assert chi_prime == num_decomp == K


class TestMatchingStructure:
    """Test matching structure and independence."""

    def test_independence_poly_alpha_10(self):
        assert independence_poly_from_matching() == ALPHA

    def test_number_perfect_matchings_positive(self):
        assert number_of_perfect_matchings_estimate() > 0

    def test_number_perfect_matchings_reasonable(self):
        """Estimate should be between 100 and 10000."""
        num = number_of_perfect_matchings_estimate()
        assert 100 < num < 10000

    def test_perfect_matching_estimate_about_1000(self):
        """Estimated ~1000 perfect matchings."""
        num = number_of_perfect_matchings_estimate()
        assert 500 < num < 2000


class TestSMCrosswalk:
    """Test Standard Model crosswalk."""

    def test_sm_crosswalk_has_7_entries(self):
        assert len(sm_crosswalk()) == 7

    def test_sm_crosswalk_has_required_keys(self):
        cw = sm_crosswalk()
        required_keys = [
            "matching_number_20",
            "matching_poly_degree",
            "m_0_eq_1",
            "m_1_eq_EDGES",
            "m_2_eq_26040",
            "edge_coloring_12_perfect_matchings",
            "perfect_matching_estimate",
        ]
        for key in required_keys:
            assert key in cw

    def test_sm_crosswalk_values_are_strings(self):
        cw = sm_crosswalk()
        for value in cw.values():
            assert isinstance(value, str)

    def test_sm_crosswalk_values_nonempty(self):
        cw = sm_crosswalk()
        for value in cw.values():
            assert len(value) > 0


class TestVerifyAll:
    """Test the verification suite."""

    def test_verify_all_27_checks(self):
        """verify_all should return (checks_list, passed, total=27)."""
        checks, passed, total = verify_all()
        assert total == 27

    def test_verify_all_all_pass(self):
        """All 27 checks should pass."""
        checks, passed, total = verify_all()
        assert passed == 27
        assert passed == total

    def test_verify_all_returns_tuple(self):
        result = verify_all()
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_verify_all_checks_is_list(self):
        checks, _, _ = verify_all()
        assert isinstance(checks, list)

    def test_verify_all_checks_have_name_and_bool(self):
        checks, _, _ = verify_all()
        for check in checks:
            assert isinstance(check, tuple)
            assert len(check) == 2
            assert isinstance(check[0], str)
            assert isinstance(check[1], bool)

    def test_verify_all_failed_count_zero(self):
        checks, passed, total = verify_all()
        assert passed == total == 27


class TestBuildSummary:
    """Test summary building."""

    def test_build_ccciii_summary_structure(self):
        summary = build_ccciii_summary()
        assert isinstance(summary, dict)

    def test_build_ccciii_summary_has_required_keys(self):
        summary = build_ccciii_summary()
        required_keys = [
            "part",
            "title",
            "checks_pass",
            "checks_total",
            "status",
            "fields",
            "discoveries",
            "sm_crosswalk",
            "failed_checks",
        ]
        for key in required_keys:
            assert key in summary

    def test_build_ccciii_part_is_ccciii(self):
        summary = build_ccciii_summary()
        assert summary["part"] == "CCCIII"

    def test_build_ccciii_status_pass(self):
        summary = build_ccciii_summary()
        assert summary["status"] == "PASS"

    def test_build_ccciii_checks_27_27(self):
        summary = build_ccciii_summary()
        assert summary["checks_pass"] == 27
        assert summary["checks_total"] == 27

    def test_build_ccciii_discoveries_list(self):
        summary = build_ccciii_summary()
        assert isinstance(summary["discoveries"], list)
        assert len(summary["discoveries"]) > 0

    def test_build_ccciii_discoveries_at_least_8(self):
        """At least 8 discoveries."""
        summary = build_ccciii_summary()
        assert len(summary["discoveries"]) >= 8

    def test_build_ccciii_failed_checks_empty(self):
        summary = build_ccciii_summary()
        assert len(summary["failed_checks"]) == 0

    def test_build_ccciii_fields_has_matching_numbers(self):
        summary = build_ccciii_summary()
        fields = summary["fields"]
        assert "matching_number" in fields
        assert fields["matching_number"] == 20

    def test_build_ccciii_json_written(self):
        """Summary should be written to JSON file."""
        import json
        summary = build_ccciii_summary()
        out_path = pathlib.Path(__file__).resolve().parents[1] / "PART_CCCIII_MATCHING_POLYNOMIAL_results.json"
        assert out_path.exists()
        with open(out_path) as fh:
            data = json.load(fh)
        assert data["part"] == "CCCIII"
        assert data["status"] == "PASS"
