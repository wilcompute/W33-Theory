"""Tests for PART CCCIII — Algebraic Connectivity (Fiedler Value) of W(3,3)"""
import pytest
from fractions import Fraction
import math
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'exploration'))

from PART_CCCIII_ALGEBRAIC_CONNECTIVITY_BRIDGE import (
    V, K, K2, LAM, MU, EDGES, R_EIG, S_EIG, MULT_R, MULT_S,
    EW_GAUGE_4, ALPHA, GUT_DIM, GENERATIONS,
    LAP_EIG_0, LAP_EIG_1, LAP_EIG_2,
    LAP_MULT_0, LAP_MULT_1, LAP_MULT_2,
    ALGEBRAIC_CONNECTIVITY, FIEDLER_VALUE, LAP_SPEC_RADIUS,
    LAP_SPECTRAL_GAP, LAP_SPECTRAL_GAP_EQUALS_ALPHA,
    NORM_LAP_EIG_0, NORM_LAP_EIG_1, NORM_LAP_EIG_2,
    NORM_LAP_SUM, NORM_LAP_SUM_EQ_V,
    KIRCHHOFF_SUM, KIRCHHOFF_INDEX, KIRCHHOFF_EXACT,
    CONNECTIVITY_RATIO,
    CHEEGER_LOWER, CHEEGER_UPPER_SQ, CHEEGER_UPPER_FLOAT,
    CHEEGER_UPPER_SQ_EQUALS_EDGES,
    LAP_EIG_1_EQUALS_ALPHA, LAP_EIG_2_EQUALS_EW_SQ,
    LAP_EIG_DIFF, LAP_EIG_DIFF_EQ_K_HALF,
    LAP_EIG_SUM, LAP_EIG_TOTAL_SUM,
    LAP_EIG_PROD, LAP_EIG_PROD_EQ_V_EW,
    verify_all, build_ccciii_summary,
)


class TestSRGConstants:
    def test_V(self):
        assert V == 40

    def test_K(self):
        assert K == 12

    def test_edges(self):
        assert EDGES == 240

    def test_eigenvalues(self):
        assert R_EIG == 2 and S_EIG == -4

    def test_multiplicities(self):
        assert MULT_R == 24 and MULT_S == 15
        assert 1 + MULT_R + MULT_S == V

    def test_sm_constants(self):
        assert ALPHA == 10 and EW_GAUGE_4 == 4


class TestLaplacianEigenvalues:
    def test_eig_0(self):
        assert LAP_EIG_0 == 0

    def test_eig_1(self):
        assert LAP_EIG_1 == Fraction(K - R_EIG)
        assert LAP_EIG_1 == Fraction(10)

    def test_eig_2(self):
        assert LAP_EIG_2 == Fraction(K - S_EIG)
        assert LAP_EIG_2 == Fraction(16)

    def test_multiplicities_sum_to_V(self):
        assert LAP_MULT_0 + LAP_MULT_1 + LAP_MULT_2 == V

    def test_eigenvalue_sum(self):
        # Sum of all Laplacian eigenvalues (with multiplicity) = K*V for k-regular
        total = (Fraction(LAP_EIG_0) * LAP_MULT_0
                 + LAP_EIG_1 * LAP_MULT_1
                 + LAP_EIG_2 * LAP_MULT_2)
        assert total == Fraction(K * V)

    def test_sorted_ascending(self):
        assert LAP_EIG_0 < int(LAP_EIG_1) < int(LAP_EIG_2)


class TestAlgebraicConnectivity:
    def test_fiedler_equals_eig1(self):
        assert ALGEBRAIC_CONNECTIVITY == LAP_EIG_1

    def test_fiedler_equals_fiedler_value(self):
        assert FIEDLER_VALUE == ALGEBRAIC_CONNECTIVITY

    def test_fiedler_value(self):
        assert ALGEBRAIC_CONNECTIVITY == Fraction(10)

    def test_fiedler_equals_alpha(self):
        assert LAP_EIG_1_EQUALS_ALPHA is True
        assert ALGEBRAIC_CONNECTIVITY == Fraction(ALPHA)

    def test_spectral_gap(self):
        assert LAP_SPECTRAL_GAP == LAP_EIG_1
        assert LAP_SPECTRAL_GAP_EQUALS_ALPHA is True

    def test_spectral_radius(self):
        assert LAP_SPEC_RADIUS == Fraction(16)
        assert LAP_SPEC_RADIUS == Fraction(K - S_EIG)

    def test_eig2_equals_ew_squared(self):
        assert LAP_EIG_2_EQUALS_EW_SQ is True
        assert LAP_EIG_2 == Fraction(EW_GAUGE_4 ** 2)


class TestNormalisedLaplacian:
    def test_norm_eig_0(self):
        assert NORM_LAP_EIG_0 == Fraction(0)

    def test_norm_eig_1(self):
        assert NORM_LAP_EIG_1 == Fraction(K - R_EIG, K)
        assert NORM_LAP_EIG_1 == Fraction(5, 6)

    def test_norm_eig_2(self):
        assert NORM_LAP_EIG_2 == Fraction(K - S_EIG, K)
        assert NORM_LAP_EIG_2 == Fraction(4, 3)

    def test_norm_weighted_sum_equals_V(self):
        assert NORM_LAP_SUM_EQ_V is True
        assert NORM_LAP_SUM == Fraction(V)

    def test_norm_eig_ordering(self):
        assert NORM_LAP_EIG_0 < NORM_LAP_EIG_1 < NORM_LAP_EIG_2


class TestKirchhoffIndex:
    def test_kirchhoff_sum_exact(self):
        expected = Fraction(MULT_R, int(LAP_EIG_1)) + Fraction(MULT_S, int(LAP_EIG_2))
        assert KIRCHHOFF_SUM == expected

    def test_kirchhoff_index_rational(self):
        assert isinstance(KIRCHHOFF_EXACT, Fraction)

    def test_kirchhoff_index_value(self):
        # 40 * (24/10 + 15/16) = 40 * (12/5 + 15/16) = 40 * 267/80 = 267/2
        assert KIRCHHOFF_EXACT == Fraction(267, 2)

    def test_kirchhoff_matches_index(self):
        assert KIRCHHOFF_EXACT == KIRCHHOFF_INDEX


class TestConnectivityAndCheeger:
    def test_connectivity_ratio(self):
        assert CONNECTIVITY_RATIO == Fraction(10, 16)
        assert CONNECTIVITY_RATIO == Fraction(5, 8)

    def test_cheeger_lower(self):
        assert CHEEGER_LOWER == Fraction(5)
        assert CHEEGER_LOWER == ALGEBRAIC_CONNECTIVITY / 2

    def test_cheeger_upper_sq(self):
        assert CHEEGER_UPPER_SQ == 2 * K * int(ALGEBRAIC_CONNECTIVITY)
        assert CHEEGER_UPPER_SQ == 240

    def test_cheeger_upper_sq_equals_edges(self):
        assert CHEEGER_UPPER_SQ_EQUALS_EDGES is True

    def test_cheeger_upper_float(self):
        assert abs(CHEEGER_UPPER_FLOAT - math.sqrt(240)) < 1e-10


class TestEigenvalueArithmetic:
    def test_eig_diff(self):
        assert LAP_EIG_DIFF == LAP_EIG_2 - LAP_EIG_1
        assert LAP_EIG_DIFF == Fraction(6)

    def test_eig_diff_k_half(self):
        assert LAP_EIG_DIFF_EQ_K_HALF is True
        assert LAP_EIG_DIFF == Fraction(K // 2)

    def test_eig_sum_distinct(self):
        assert LAP_EIG_SUM == LAP_EIG_1 + LAP_EIG_2
        assert LAP_EIG_SUM == Fraction(26)

    def test_eig_sum_total(self):
        assert LAP_EIG_TOTAL_SUM is True
        assert LAP_EIG_SUM == Fraction(2 * K + 2)

    def test_eig_product(self):
        assert LAP_EIG_PROD == LAP_EIG_1 * LAP_EIG_2
        assert LAP_EIG_PROD == Fraction(160)

    def test_eig_product_eq_v_ew(self):
        assert LAP_EIG_PROD_EQ_V_EW is True
        assert LAP_EIG_PROD == Fraction(V * EW_GAUGE_4)


class TestVerifyAll:
    def test_returns_tuple(self):
        result = verify_all()
        assert isinstance(result, tuple) and len(result) == 3

    def test_total_27(self):
        _, _, total = verify_all()
        assert total == 27

    def test_all_pass(self):
        checks, passed, total = verify_all()
        assert passed == total == 27

    def test_each_check_ok(self):
        checks, _, _ = verify_all()
        for c in checks:
            assert c["ok"] is True, f"Failed: {c['name']}"


class TestBuildSummary:
    def setup_method(self):
        self.s = build_ccciii_summary()

    def test_part(self):
        assert self.s["part"] == "CCCIII"

    def test_status(self):
        assert self.s["status"] == "PASS"

    def test_checks(self):
        assert self.s["checks_pass"] == 27
        assert self.s["checks_total"] == 27

    def test_title(self):
        assert "Algebraic" in self.s["title"]

    def test_fields_present(self):
        f = self.s["fields"]
        assert f["ALGEBRAIC_CONNECTIVITY"] == "10"
        assert f["LAP_SPEC_RADIUS"] == "16"

    def test_discoveries(self):
        assert len(self.s["discoveries"]) >= 5
