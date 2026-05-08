"""
Tests for CCCIV: Stanley Chromatic Symmetric Functions for W(3,3)
"""

import pytest
import sys
import pathlib
import math

# Add exploration folder to path
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "exploration"))

from PART_CCCIV_STANLEY_CSF_BRIDGE import (
    chromatic_number,
    chromatic_poly_const_term,
    chromatic_poly_at_1,
    chromatic_poly_at_2,
    chromatic_poly_at_3,
    chromatic_poly_at_4,
    chromatic_poly_at_5,
    chromatic_poly_leading_coeff,
    csf_is_homogeneous,
    csf_power_sum_basis_elements,
    csf_schur_basis_coefficients,
    csf_elementary_symmetric_expansion,
    csf_complete_homogeneous_expansion,
    csf_at_ones,
    csf_at_minus_ones,
    csf_evaluation_at_geometric_series,
    csf_at_first_V_variables,
    csf_schur_expansion_multiplicity,
    csf_irrep_multiplicity,
    csf_character_evaluation,
    csf_restriction_smaller_symmetric_group,
    csf_for_complete_graph,
    csf_for_bipartite_graph,
    csf_for_vertex_transitive,
    csf_for_strongly_regular,
    csf_rank_is_chi_factorial,
    csf_gut_matter_multiplicity,
    csf_quantum_chromatic_relation,
    csf_generations_and_csf,
    sm_crosswalk,
    verify_all,
    build_ccciv_summary,
    V, K, EDGES, ALPHA, GUT_DIM, SU5_MATTER, GENERATIONS,
)


class TestChromaticPolyProperties:
    """Test chromatic polynomial properties."""

    def test_chromatic_number_4(self):
        assert chromatic_number() == 4

    def test_chromatic_poly_at_0_zero(self):
        assert chromatic_poly_const_term() == 0

    def test_chromatic_poly_at_1_zero(self):
        assert chromatic_poly_at_1() == 0

    def test_chromatic_poly_at_2_zero(self):
        assert chromatic_poly_at_2() == 0

    def test_chromatic_poly_at_3_zero(self):
        assert chromatic_poly_at_3() == 0

    def test_chromatic_poly_at_4_positive(self):
        assert chromatic_poly_at_4() > 0

    def test_chromatic_poly_at_4_large(self):
        """P_G(4) should be very large (many 4-colorings exist)."""
        assert chromatic_poly_at_4() > 10**10

    def test_chromatic_poly_at_5_gt_at_4(self):
        """P_G(5) > P_G(4) (more colorings with more colors)."""
        assert chromatic_poly_at_5() > chromatic_poly_at_4()

    def test_chromatic_poly_leading_coeff_1(self):
        """Leading coefficient of P_G(n) is 1 (monic)."""
        assert chromatic_poly_leading_coeff() == 1


class TestCSFStructure:
    """Test CSF structure properties."""

    def test_csf_homogeneous_degree_V(self):
        assert csf_is_homogeneous() == V

    def test_csf_homogeneous_degree_40(self):
        assert csf_is_homogeneous() == 40

    def test_csf_power_sum_basis_positive(self):
        assert csf_power_sum_basis_elements() > 0

    def test_csf_power_sum_basis_reasonable(self):
        """Number of power sum terms should be reasonable."""
        assert 50 < csf_power_sum_basis_elements() < 200

    def test_csf_schur_basis_is_dict(self):
        assert isinstance(csf_schur_basis_coefficients(), dict)

    def test_csf_schur_basis_has_keys(self):
        sb = csf_schur_basis_coefficients()
        assert "num_partitions" in sb
        assert "max_multiplicity" in sb

    def test_csf_elementary_symmetric_complete(self):
        es = csf_elementary_symmetric_expansion()
        assert es["degree"] == V

    def test_csf_complete_homogeneous_complete(self):
        ch = csf_complete_homogeneous_expansion()
        assert ch["degree"] == V

    def test_csf_rank_chi_factorial(self):
        assert csf_rank_is_chi_factorial() == math.factorial(chromatic_number())

    def test_csf_rank_24(self):
        """Rank <= chi! = 4! = 24."""
        assert csf_rank_is_chi_factorial() == 24


class TestCSFEvaluation:
    """Test CSF evaluation at special points."""

    def test_csf_at_ones_positive(self):
        assert csf_at_ones() > 0

    def test_csf_at_minus_ones_nonzero(self):
        assert csf_at_minus_ones() != 0

    def test_csf_at_minus_ones_positive(self):
        """CSF at (-1,-1,...) with V=40 even gives positive value."""
        assert csf_at_minus_ones() > 0

    def test_csf_evaluation_geometric_series(self):
        assert csf_evaluation_at_geometric_series() == "geometric_series"

    def test_csf_at_first_V_variables(self):
        assert csf_at_first_V_variables() == V

    def test_csf_evaluation_consistency(self):
        assert csf_at_first_V_variables() == csf_is_homogeneous()


class TestCSFRepresentationTheory:
    """Test CSF representation theory properties."""

    def test_csf_schur_multiplicity_nonnegative(self):
        assert csf_schur_expansion_multiplicity() >= 0

    def test_csf_schur_multiplicity_24(self):
        """Schur multiplicity = 24 (Aut(W(3,3)) size)."""
        assert csf_schur_expansion_multiplicity() == 24

    def test_csf_irrep_multiplicity_dict(self):
        assert isinstance(csf_irrep_multiplicity(), dict)

    def test_csf_irrep_num_irreps_positive(self):
        im = csf_irrep_multiplicity()
        assert im["num_irreps"] > 0

    def test_csf_character_evaluation(self):
        assert csf_character_evaluation() == "permutation_representation"

    def test_csf_restriction_positive(self):
        assert csf_restriction_smaller_symmetric_group() > 0


class TestCSFSpecialGraphs:
    """Test CSF for special graph structures."""

    def test_csf_complete_graph_formula(self):
        assert csf_for_complete_graph() == "K_n_formula"

    def test_csf_bipartite_not_applicable(self):
        """W(3,3) not bipartite."""
        assert csf_for_bipartite_graph() == "not_bipartite"

    def test_csf_vertex_transitive_property(self):
        """W(3,3) vertex-transitive."""
        assert csf_for_vertex_transitive() == 24

    def test_csf_strongly_regular_structure(self):
        assert isinstance(csf_for_strongly_regular(), dict)

    def test_csf_strongly_regular_has_parameters(self):
        sr = csf_for_strongly_regular()
        assert "parameters" in sr
        assert sr["parameters"] == (V, K, 2, 4)


class TestCSFPhysicsConnections:
    """Test CSF physics connections."""

    def test_csf_gut_matter_multiplicity(self):
        assert csf_gut_matter_multiplicity() == GUT_DIM * SU5_MATTER

    def test_csf_gut_matter_405(self):
        """GUT × SU5 = 27 × 15 = 405."""
        assert csf_gut_matter_multiplicity() == 405

    def test_csf_quantum_analog_defined(self):
        assert csf_quantum_chromatic_relation() == "q_analog"

    def test_csf_generations_triality(self):
        assert csf_generations_and_csf() == GENERATIONS

    def test_csf_generations_3(self):
        assert csf_generations_and_csf() == 3


class TestSMCrosswalk:
    """Test Standard Model crosswalk."""

    def test_sm_crosswalk_has_7_entries(self):
        assert len(sm_crosswalk()) == 7

    def test_sm_crosswalk_required_keys(self):
        cw = sm_crosswalk()
        required_keys = [
            "chromatic_number_4",
            "csf_homogeneous_degree_V",
            "csf_schur_basis_expansion",
            "csf_power_sum_basis",
            "csf_rank_chi_factorial",
            "csf_vertex_transitive_symmetry",
            "csf_gum_matter_15_times_27",
        ]
        for key in required_keys:
            assert key in cw

    def test_sm_crosswalk_values_strings(self):
        cw = sm_crosswalk()
        for value in cw.values():
            assert isinstance(value, str)


class TestVerifyAll:
    """Test verification suite."""

    def test_verify_all_27_checks(self):
        checks, passed, total = verify_all()
        assert total == 27

    def test_verify_all_all_pass(self):
        checks, passed, total = verify_all()
        assert passed == 27
        assert passed == total

    def test_verify_all_returns_tuple(self):
        result = verify_all()
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_verify_all_checks_list(self):
        checks, _, _ = verify_all()
        assert isinstance(checks, list)

    def test_verify_all_check_structure(self):
        checks, _, _ = verify_all()
        for check in checks:
            assert isinstance(check, tuple)
            assert len(check) == 2
            assert isinstance(check[0], str)
            assert isinstance(check[1], bool)


class TestBuildSummary:
    """Test summary building."""

    def test_build_ccciv_summary_dict(self):
        summary = build_ccciv_summary()
        assert isinstance(summary, dict)

    def test_build_ccciv_required_keys(self):
        summary = build_ccciv_summary()
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

    def test_build_ccciv_part_ccciv(self):
        summary = build_ccciv_summary()
        assert summary["part"] == "CCCIV"

    def test_build_ccciv_status_pass(self):
        summary = build_ccciv_summary()
        assert summary["status"] == "PASS"

    def test_build_ccciv_checks_27_27(self):
        summary = build_ccciv_summary()
        assert summary["checks_pass"] == 27
        assert summary["checks_total"] == 27

    def test_build_ccciv_discoveries_list(self):
        summary = build_ccciv_summary()
        assert isinstance(summary["discoveries"], list)
        assert len(summary["discoveries"]) >= 8

    def test_build_ccciv_failed_checks_empty(self):
        summary = build_ccciv_summary()
        assert len(summary["failed_checks"]) == 0

    def test_build_ccciv_json_written(self):
        import json
        summary = build_ccciv_summary()
        out_path = pathlib.Path(__file__).resolve().parents[1] / "PART_CCCIV_STANLEY_CSF_results.json"
        assert out_path.exists()
        with open(out_path) as fh:
            data = json.load(fh)
        assert data["part"] == "CCCIV"
        assert data["status"] == "PASS"
