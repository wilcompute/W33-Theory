"""Tests for PART CCCXVI — Seidel Matrix & Two-Graph for W(3,3)."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "exploration"))

from PART_CCCXVI_SEIDEL_MATRIX_BRIDGE import (
    V, K, LAM, MU, EDGES, MULT_R, MULT_S,
    R_EIG, S_EIG,
    EW_GAUGE_4, ALPHA, GUT_DIM, GENERATIONS,
    SEIDEL_EIG_1, SEIDEL_EIG_2, SEIDEL_EIG_3,
    MULT_SEIDEL_1, MULT_SEIDEL_2, MULT_SEIDEL_3,
    seidel_trace, seidel_trace_sq,
    verify_all, build_cccxvi_summary,
)


# ---------------------------------------------------------------------------
# TestSRGParameters
# ---------------------------------------------------------------------------
class TestSRGParameters:
    def test_V(self):
        assert V == 40

    def test_K(self):
        assert K == 12

    def test_LAM(self):
        assert LAM == 2

    def test_MU(self):
        assert MU == 4

    def test_EDGES(self):
        assert EDGES == 240

    def test_MULT_R(self):
        assert MULT_R == 24

    def test_MULT_S(self):
        assert MULT_S == 15

    def test_SRG_eigenvalue_r(self):
        assert R_EIG == 2

    def test_SRG_eigenvalue_s(self):
        assert S_EIG == -4

    def test_mult_sum_plus_one_equals_V(self):
        assert MULT_R + MULT_S + 1 == V


# ---------------------------------------------------------------------------
# TestSeidelEigenvalueFormulas
# ---------------------------------------------------------------------------
class TestSeidelEigenvalueFormulas:
    def test_sigma1_formula(self):
        assert SEIDEL_EIG_1 == V - 1 - 2 * K

    def test_sigma2_formula(self):
        assert SEIDEL_EIG_2 == -(1 + 2 * R_EIG)

    def test_sigma3_formula(self):
        assert SEIDEL_EIG_3 == -(1 + 2 * S_EIG)

    def test_sigma1_value(self):
        assert SEIDEL_EIG_1 == 15

    def test_sigma2_value(self):
        assert SEIDEL_EIG_2 == -5

    def test_sigma3_value(self):
        assert SEIDEL_EIG_3 == 7

    def test_sigma1_positive(self):
        assert SEIDEL_EIG_1 > 0

    def test_sigma2_negative(self):
        assert SEIDEL_EIG_2 < 0

    def test_sigma3_positive(self):
        assert SEIDEL_EIG_3 > 0

    def test_sigma1_is_largest(self):
        assert SEIDEL_EIG_1 > SEIDEL_EIG_3 > SEIDEL_EIG_2

    def test_all_three_distinct(self):
        assert len({SEIDEL_EIG_1, SEIDEL_EIG_2, SEIDEL_EIG_3}) == 3


# ---------------------------------------------------------------------------
# TestSeidelMultiplicities
# ---------------------------------------------------------------------------
class TestSeidelMultiplicities:
    def test_mult1_is_one(self):
        assert MULT_SEIDEL_1 == 1

    def test_mult2_equals_MULT_R(self):
        assert MULT_SEIDEL_2 == MULT_R

    def test_mult2_value(self):
        assert MULT_SEIDEL_2 == 24

    def test_mult3_equals_MULT_S(self):
        assert MULT_SEIDEL_3 == MULT_S

    def test_mult3_value(self):
        assert MULT_SEIDEL_3 == 15

    def test_mult_sum_equals_V(self):
        assert MULT_SEIDEL_1 + MULT_SEIDEL_2 + MULT_SEIDEL_3 == V

    def test_m2_plus_m3_equals_V_minus_1(self):
        assert MULT_SEIDEL_2 + MULT_SEIDEL_3 == V - 1


# ---------------------------------------------------------------------------
# TestSeidelSpectralProperties
# ---------------------------------------------------------------------------
class TestSeidelSpectralProperties:
    def test_trace_S_is_zero(self):
        assert seidel_trace() == 0

    def test_trace_S2_equals_V_times_Vm1(self):
        assert seidel_trace_sq() == V * (V - 1)

    def test_trace_S2_value(self):
        assert seidel_trace_sq() == 1560

    def test_trace_S_manual(self):
        t = 1 * SEIDEL_EIG_1 + 24 * SEIDEL_EIG_2 + 15 * SEIDEL_EIG_3
        assert t == 0

    def test_trace_S2_manual(self):
        t2 = 1 * 225 + 24 * 25 + 15 * 49
        assert t2 == 1560

    def test_sigma1_sq(self):
        assert SEIDEL_EIG_1 ** 2 == 225

    def test_sigma2_sq(self):
        assert SEIDEL_EIG_2 ** 2 == 25

    def test_sigma3_sq(self):
        assert SEIDEL_EIG_3 ** 2 == 49


# ---------------------------------------------------------------------------
# TestSMEncodings
# ---------------------------------------------------------------------------
class TestSMEncodings:
    def test_sigma1_plus_sigma2_equals_ALPHA(self):
        assert SEIDEL_EIG_1 + SEIDEL_EIG_2 == ALPHA

    def test_sigma3_minus_sigma2_equals_K(self):
        assert SEIDEL_EIG_3 - SEIDEL_EIG_2 == K

    def test_abs_sigma2_equals_GENERATIONS_plus_2(self):
        assert abs(SEIDEL_EIG_2) == GENERATIONS + 2

    def test_sigma3_equals_EW_plus_GENERATIONS(self):
        assert SEIDEL_EIG_3 == EW_GAUGE_4 + GENERATIONS

    def test_sigma1_equals_5_times_GENERATIONS(self):
        assert SEIDEL_EIG_1 == 5 * GENERATIONS

    def test_sigma1_equals_MULT_S(self):
        assert SEIDEL_EIG_1 == MULT_S

    def test_sigma2_times_sigma3_product(self):
        assert SEIDEL_EIG_2 * SEIDEL_EIG_3 == -(V - MU - 1)

    def test_sigma2_times_sigma3_value(self):
        assert SEIDEL_EIG_2 * SEIDEL_EIG_3 == -35

    def test_mult_gap_equals_GENERATIONS_sq(self):
        assert MULT_SEIDEL_2 - MULT_SEIDEL_3 == GENERATIONS ** 2

    def test_mult_gap_value(self):
        assert MULT_SEIDEL_2 - MULT_SEIDEL_3 == 9

    def test_sigma1_minus_sigma3_equals_2_EW(self):
        assert SEIDEL_EIG_1 - SEIDEL_EIG_3 == 2 * EW_GAUGE_4

    def test_sigma1_minus_sigma3_value(self):
        assert SEIDEL_EIG_1 - SEIDEL_EIG_3 == 8

    def test_sigma1_plus_sigma3_equals_K_plus_ALPHA(self):
        assert SEIDEL_EIG_1 + SEIDEL_EIG_3 == K + ALPHA

    def test_sigma1_plus_sigma3_value(self):
        assert SEIDEL_EIG_1 + SEIDEL_EIG_3 == 22

    def test_abs_sigma2_sq_equals_MULT_S_plus_ALPHA(self):
        assert abs(SEIDEL_EIG_2) ** 2 == MULT_S + ALPHA

    def test_abs_sigma2_sq_value(self):
        assert abs(SEIDEL_EIG_2) ** 2 == 25

    def test_sigma3_sq_encoding(self):
        assert SEIDEL_EIG_3 ** 2 == ALPHA * EW_GAUGE_4 + GENERATIONS ** 2

    def test_sigma3_sq_value(self):
        assert SEIDEL_EIG_3 ** 2 == 49


# ---------------------------------------------------------------------------
# TestSwitchingInvariants
# ---------------------------------------------------------------------------
class TestSwitchingInvariants:
    def test_seidel_spectrum_has_three_values(self):
        spectrum = {SEIDEL_EIG_1, SEIDEL_EIG_2, SEIDEL_EIG_3}
        assert len(spectrum) == 3

    def test_seidel_not_conference_graph(self):
        # Conference SRGs have s = -(r+1); W(3,3) does not
        assert S_EIG != -(R_EIG + 1)

    def test_neg_seidel_eig_formula_consistency(self):
        # sigma_2 = -(1 + 2r), sigma_3 = -(1 + 2s)
        # Difference sigma_3 - sigma_2 = -2s + 2r = 2(r - s)
        assert SEIDEL_EIG_3 - SEIDEL_EIG_2 == 2 * (R_EIG - S_EIG)

    def test_seidel_eig1_independent_of_r_s(self):
        # sigma_1 only depends on V and K
        assert SEIDEL_EIG_1 == V - 1 - 2 * K

    def test_seidel_sum_of_eigenvalues_no_mult(self):
        # Unweighted sum
        assert SEIDEL_EIG_1 + SEIDEL_EIG_2 + SEIDEL_EIG_3 == 17

    def test_K_over_abs_S_eig(self):
        assert K // abs(S_EIG) == GENERATIONS


# ---------------------------------------------------------------------------
# TestVerifyAll
# ---------------------------------------------------------------------------
class TestVerifyAll:
    def test_verify_all_returns_tuple(self):
        result = verify_all()
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_verify_all_27_checks(self):
        _, _, total = verify_all()
        assert total == 27

    def test_verify_all_all_pass(self):
        _, passed, total = verify_all()
        assert passed == total

    def test_verify_all_27_27(self):
        _, passed, total = verify_all()
        assert passed == 27
        assert total == 27

    def test_verify_all_checks_list_length(self):
        checks, _, _ = verify_all()
        assert len(checks) == 27

    def test_verify_all_no_failures(self):
        checks, _, _ = verify_all()
        failures = [(label, val, exp) for label, ok, val, exp in checks if not ok]
        assert failures == [], f"Failed checks: {failures}"

    def test_build_summary_part(self):
        s = build_cccxvi_summary()
        assert s["part"] == "CCCXVI"

    def test_build_summary_title(self):
        s = build_cccxvi_summary()
        assert "Seidel" in s["title"]

    def test_build_summary_status_pass(self):
        s = build_cccxvi_summary()
        assert s["status"] == "PASS"

    def test_build_summary_checks(self):
        s = build_cccxvi_summary()
        assert s["checks_pass"] == 27
        assert s["checks_total"] == 27

    def test_build_summary_fields(self):
        s = build_cccxvi_summary()
        assert "sigma_1" in s["fields"]
        assert "sigma_2" in s["fields"]
        assert "sigma_3" in s["fields"]
        assert s["fields"]["sigma_1"] == 15
        assert s["fields"]["sigma_2"] == -5
        assert s["fields"]["sigma_3"] == 7

    def test_build_summary_discoveries(self):
        s = build_cccxvi_summary()
        assert len(s["discoveries"]) >= 10
