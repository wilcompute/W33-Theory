"""
Tests for PART_CXCVIII: Riemann Zeta / GUE Bridge
===================================================
Regression tests for all atom checks, trivial zeros, Ramanujan sums,
Bernoulli denominators, GUE pair correlation, and the full audit.
"""

import math
import pytest

from PART_CXCVIII_RIEMANN_ZETA_GUE_BRIDGE import (
    Q, LAM, V, K, PHI3, PHI4, PHI6, PHI12, J_INV, EDGES, EIG_MAX, MULT_K2,
    TRIVIAL_ZERO_STEP, TRIVIAL_ZERO_FIRST, CRITICAL_LINE_DEN, RS_THETA_CONST_DEN,
    FIRST_PRIME, RAMANUJAN_Q, RAMANUJAN_NON_ZERO_VAL, RAMANUJAN_TRIVIAL_VAL,
    ZETA_NEG1_DEN, ZETA_NEG3_DEN, ZETA_NEG5_DEN, ZETA_0_DEN,
    ZETA_2_DEN, ZETA_4_DEN_FORMULA, ZETA_6_DEN_FORMULA,
    GUE_MATRIX_SIZE, GUE_LOG_SIZE, PAIR_CORR_PERIOD,
    PAIR_CORR_AT_1, PAIR_CORR_AT_HALF, PAIR_CORR_AT_HALF_FORMULA,
    XI_VALUE, N_ZEROS_FACTOR_DEN,
    ZERO_1, ZERO_2, ZERO_3, ZERO_4, ZERO_5, ZERO_GAP_12,
    montgomery_r,
    ZetaCheck,
    _make_atom_checks, _make_trivial_zero_checks, _make_ramanujan_checks,
    _make_bernoulli_checks, _make_gue_checks, _make_structural_checks,
    riemann_zeta_gue_bridge_audit,
)


class TestAtoms:
    def test_Q(self): assert Q == 3
    def test_LAM(self): assert LAM == 2
    def test_V(self): assert V == 40
    def test_K(self): assert K == 12
    def test_PHI3(self): assert PHI3 == 13
    def test_PHI6(self): assert PHI6 == 7
    def test_J_INV(self): assert J_INV == 8
    def test_EDGES(self): assert EDGES == 240
    def test_EIG_MAX(self): assert EIG_MAX == 5


class TestTrivialZeros:
    def test_step_is_lam(self): assert TRIVIAL_ZERO_STEP == LAM
    def test_step_value(self): assert TRIVIAL_ZERO_STEP == 2
    def test_first_is_neg_lam(self): assert TRIVIAL_ZERO_FIRST == -LAM
    def test_first_value(self): assert TRIVIAL_ZERO_FIRST == -2
    def test_critical_line_den(self): assert CRITICAL_LINE_DEN == LAM
    def test_rs_theta_den(self): assert RS_THETA_CONST_DEN == J_INV
    def test_first_prime(self): assert FIRST_PRIME == LAM


class TestRamanujan:
    def test_q_value(self): assert RAMANUJAN_Q == Q
    def test_nontrivial_is_lam(self): assert RAMANUJAN_NON_ZERO_VAL == LAM
    def test_nontrivial_value(self): assert RAMANUJAN_NON_ZERO_VAL == 2
    def test_trivial_value(self): assert RAMANUJAN_TRIVIAL_VAL == -1
    def test_sum_zero(self): assert RAMANUJAN_NON_ZERO_VAL + 2 * RAMANUJAN_TRIVIAL_VAL == 0


class TestBernoulliDenominators:
    def test_zeta_neg1_den_is_k(self): assert ZETA_NEG1_DEN == K
    def test_zeta_neg1_den_value(self): assert ZETA_NEG1_DEN == 12
    def test_zeta_neg3_den_is_120(self): assert ZETA_NEG3_DEN == 120
    def test_zeta_neg3_den_formula(self): assert ZETA_NEG3_DEN == math.factorial(EIG_MAX)
    def test_zeta_neg5_den_formula(self): assert ZETA_NEG5_DEN == K * (PHI3 + J_INV)
    def test_zeta_neg5_den_value(self): assert ZETA_NEG5_DEN == 252
    def test_zeta_0_den(self): assert ZETA_0_DEN == LAM
    def test_zeta_2_den_is_mult_k2(self): assert ZETA_2_DEN == MULT_K2
    def test_zeta_2_den_value(self): assert ZETA_2_DEN == 6
    def test_zeta_4_den_formula(self): assert ZETA_4_DEN_FORMULA == LAM * Q**2 * EIG_MAX
    def test_zeta_4_den_value(self): assert ZETA_4_DEN_FORMULA == 90
    def test_zeta_6_den_formula(self): assert ZETA_6_DEN_FORMULA == Q**2 * EIG_MAX * (PHI3 + J_INV)
    def test_zeta_6_den_value(self): assert ZETA_6_DEN_FORMULA == 945


class TestGUE:
    def test_matrix_size_is_edges(self): assert GUE_MATRIX_SIZE == EDGES
    def test_matrix_size_value(self): assert GUE_MATRIX_SIZE == 240
    def test_log_size_positive(self): assert GUE_LOG_SIZE > 0
    def test_pair_corr_period(self): assert abs(PAIR_CORR_PERIOD - 1.0 / LAM) < 1e-12
    def test_pair_corr_at_1(self): assert abs(PAIR_CORR_AT_1 - 1.0) < 1e-10
    def test_pair_corr_at_half_formula(self):
        assert abs(PAIR_CORR_AT_HALF - PAIR_CORR_AT_HALF_FORMULA) < 1e-12
    def test_pair_corr_at_half_value(self):
        assert abs(PAIR_CORR_AT_HALF - (1.0 - 4.0 / math.pi**2)) < 1e-10


class TestMontgomeryR:
    def test_r_at_0(self): assert abs(montgomery_r(1e-15)) < 1e-10
    def test_r_at_1(self): assert abs(montgomery_r(1.0) - 1.0) < 1e-10
    def test_r_at_2(self): assert abs(montgomery_r(2.0) - 1.0) < 1e-10
    def test_r_nonneg(self):
        for k in range(1, 200):
            assert montgomery_r(k / 100) >= -1e-12
    def test_r_symmetric(self):
        assert abs(montgomery_r(0.3) - montgomery_r(-0.3)) < 1e-10


class TestStructural:
    def test_n_zeros_factor_den(self): assert N_ZEROS_FACTOR_DEN == LAM
    def test_xi_value(self): assert abs(XI_VALUE - 0.5) < 1e-12
    def test_zeta_2_numeric(self): assert abs(math.pi**2 / 6 - 1.6449340668482264) < 1e-10
    def test_zeta_4_numeric(self): assert abs(math.pi**4 / 90 - 1.0823232337111381) < 1e-10
    def test_zeros_ordering(self): assert ZERO_1 < ZERO_2 < ZERO_3 < ZERO_4 < ZERO_5
    def test_gap_positive(self): assert ZERO_GAP_12 > 0
    def test_zeta_neg1_val(self): assert abs(-1.0 / 12 - (-1.0 / K)) < 1e-12


class TestZetaCheck:
    def test_exact_pass(self):
        c = ZetaCheck("t", "d", 5, 5)
        assert c.passes

    def test_exact_fail(self):
        c = ZetaCheck("t", "d", 5, 6)
        assert not c.passes

    def test_inexact_pass(self):
        c = ZetaCheck("t", "d", 1.0 + 1e-12, 1.0, exact=False)
        assert c.passes

    def test_inexact_fail(self):
        c = ZetaCheck("t", "d", 1.0 + 1e-9, 1.0, exact=False)
        assert not c.passes

    def test_frozen(self):
        c = ZetaCheck("t", "d", 1, 1)
        with pytest.raises((AttributeError, TypeError)):
            c.name = "x"  # type: ignore[misc]


class TestCheckFactories:
    def test_atom_count(self): assert len(_make_atom_checks()) == 9
    def test_atom_all_pass(self): assert all(c.passes for c in _make_atom_checks())
    def test_trivial_count(self): assert len(_make_trivial_zero_checks()) == 7
    def test_trivial_all_pass(self): assert all(c.passes for c in _make_trivial_zero_checks())
    def test_ramanujan_count(self): assert len(_make_ramanujan_checks()) == 5
    def test_ramanujan_all_pass(self): assert all(c.passes for c in _make_ramanujan_checks())
    def test_bernoulli_count(self): assert len(_make_bernoulli_checks()) == 13
    def test_bernoulli_all_pass(self): assert all(c.passes for c in _make_bernoulli_checks())
    def test_gue_count(self): assert len(_make_gue_checks()) == 8
    def test_gue_all_pass(self): assert all(c.passes for c in _make_gue_checks())
    def test_structural_count(self): assert len(_make_structural_checks()) == 9
    def test_structural_all_pass(self): assert all(c.passes for c in _make_structural_checks())


class TestAudit:
    def setup_method(self):
        self.result = riemann_zeta_gue_bridge_audit()

    def test_status_pass(self): assert self.result["status"] == "PASS"
    def test_all_checks_pass(self): assert self.result["all_checks_pass"] is True
    def test_no_failed(self): assert self.result["failed_checks"] == []
    def test_check_count(self): assert self.result["check_count"] == 51
    def test_checks_passing(self): assert self.result["checks_passing"] == 51

    def test_first_zeros_present(self):
        assert len(self.result["first_zeros"]) == 5

    def test_zeta_2_den_in_result(self): assert self.result["zeta_2_den"] == 6
    def test_zeta_4_den_in_result(self): assert self.result["zeta_4_den"] == 90
    def test_zeta_6_den_in_result(self): assert self.result["zeta_6_den"] == 945

    def test_w33_atoms_present(self):
        atoms = self.result["w33_atoms"]
        assert atoms["Q"] == 3
        assert atoms["EDGES"] == 240
        assert atoms["K"] == 12

    def test_theorem_key(self): assert "theorem_cxcviii" in self.result

    def test_category_counts(self):
        cats = self.result["category_counts"]
        assert cats["atom_checks"] == 9
        assert cats["trivial_zero_checks"] == 7
        assert cats["ramanujan_checks"] == 5
        assert cats["bernoulli_checks"] == 13
        assert cats["gue_checks"] == 8
        assert cats["structural_checks"] == 9
