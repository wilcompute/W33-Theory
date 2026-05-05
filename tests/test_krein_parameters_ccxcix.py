"""
Tests for PART CCXCIX — Krein Parameters of the W(3,3) Bose-Mesner Algebra.

Covers:
  - First eigenmatrix P structure and determinant
  - P-inverse and idempotent coefficient extraction
  - Idempotent self-consistency (eigenvalue checks)
  - Trivial Krein parameters (q^0 family)
  - Non-trivial Krein parameters (q^1 and q^2 families, exact rational values)
  - SM / combinatorial identities encoded in the Krein parameters
  - verify_all() reporting and build_ccxcix_summary() structure
"""

import sys
import os
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from exploration.PART_CCXCIX_KREIN_PARAMETERS_BRIDGE import (
    V, K, K2, LAM, MU, EDGES,
    R_EIG, S_EIG, MULT_R, MULT_S,
    EW_GAUGE_4, ALPHA,
    _P, P_INV, Q_MAT, P_DET,
    E0_COEFF, E1_COEFF, E2_COEFF,
    Q0_11, Q1_11, Q2_11,
    Q0_12, Q1_12, Q2_12,
    Q0_22, Q1_22, Q2_22,
    KREIN_Q00, KREIN_Q11, KREIN_Q12, KREIN_Q22,
    ALL_KREIN_NONNEG,
    verify_all, build_ccxcix_summary,
)


# ─────────────────────────────────────────────────────────────────────────────
class TestSRGConstants:
    """Baseline W(3,3) SRG parameters carried into this part."""

    def test_vertex_count(self):
        assert V == 40

    def test_valency(self):
        assert K == 12

    def test_complement_valency(self):
        assert K2 == 27
        assert K2 == V - 1 - K

    def test_edge_count(self):
        assert EDGES == 240
        assert EDGES == V * K // 2

    def test_r_eig(self):
        assert R_EIG == 2

    def test_s_eig(self):
        assert S_EIG == -4

    def test_mult_r(self):
        assert MULT_R == 24

    def test_mult_s(self):
        assert MULT_S == 15

    def test_mult_sum(self):
        assert 1 + MULT_R + MULT_S == V

    def test_alpha(self):
        assert ALPHA == 10

    def test_ew_gauge(self):
        assert EW_GAUGE_4 == 4


# ─────────────────────────────────────────────────────────────────────────────
class TestPMatrix:
    """First eigenmatrix P of the association scheme."""

    def test_p_shape(self):
        assert len(_P) == 3
        assert all(len(row) == 3 for row in _P)

    def test_p_trivial_column(self):
        # All entries in column 0 (A_0 = I) equal 1
        for i in range(3):
            assert _P[i][0] == Fraction(1)

    def test_p_adjacency_eigenvalues(self):
        assert _P[0][1] == Fraction(K)      # trivial eigenspace
        assert _P[1][1] == Fraction(R_EIG)  # r-eigenspace
        assert _P[2][1] == Fraction(S_EIG)  # s-eigenspace

    def test_p_non_adj_eigenvalues(self):
        # A_2 eigenvalue = -1 - (A_1 eigenvalue) on same eigenspace
        assert _P[0][2] == Fraction(K2)
        assert _P[1][2] == Fraction(-1 - R_EIG)
        assert _P[2][2] == Fraction(-1 - S_EIG)

    def test_p_non_adj_explicit(self):
        assert _P[1][2] == Fraction(-3)
        assert _P[2][2] == Fraction(3)

    def test_p_det(self):
        assert P_DET == Fraction(-EDGES)
        assert P_DET == Fraction(-240)

    def test_p_det_nonzero(self):
        assert P_DET != 0

    def test_p_row_sum_trivial(self):
        # Sum of row 0 = 1 + K + K2 = V
        row_sum = sum(_P[0])
        assert row_sum == Fraction(V)

    def test_p_row_sum_r(self):
        # Sum of row 1 = 1 + R_EIG + (-1-R_EIG) = 0
        row_sum = sum(_P[1])
        assert row_sum == Fraction(0)

    def test_p_row_sum_s(self):
        # Sum of row 2 = 1 + S_EIG + (-1-S_EIG) = 0
        row_sum = sum(_P[2])
        assert row_sum == Fraction(0)


# ─────────────────────────────────────────────────────────────────────────────
class TestPInverse:
    """P^{-1} entries and idempotent coefficient extraction."""

    def test_p_inv_col0_sums_to_reciprocal_v(self):
        # Column 0 of P^{-1} should have all entries = 1/v (E_0 coefficients)
        col0 = [P_INV[i][0] for i in range(3)]
        assert all(c == Fraction(1, V) for c in col0)

    def test_e1_coeff_a0(self):
        assert E1_COEFF[0] == Fraction(3, 5)

    def test_e1_coeff_a1(self):
        assert E1_COEFF[1] == Fraction(1, 10)

    def test_e1_coeff_a2(self):
        assert E1_COEFF[2] == Fraction(-1, 15)

    def test_e2_coeff_a0(self):
        assert E2_COEFF[0] == Fraction(3, 8)

    def test_e2_coeff_a1(self):
        assert E2_COEFF[1] == Fraction(-1, 8)

    def test_e2_coeff_a2(self):
        assert E2_COEFF[2] == Fraction(1, 24)

    def test_e0_coeff_sums_to_1_over_v(self):
        # E_0 = (1/v)(I + A + A_2) → all coefficients = 1/v
        assert all(c == Fraction(1, V) for c in E0_COEFF)


# ─────────────────────────────────────────────────────────────────────────────
class TestIdempotentSelfConsistency:
    """
    E_i must have eigenvalue 1 on its own eigenspace and 0 on others.
    Checked via:  sum_j E_i_COEFF[j] * P[eigenspace][j]
    """

    def test_e1_eigenvalue_on_r_space(self):
        val = sum(E1_COEFF[j] * _P[1][j] for j in range(3))
        assert val == Fraction(1)

    def test_e1_eigenvalue_on_s_space(self):
        val = sum(E1_COEFF[j] * _P[2][j] for j in range(3))
        assert val == Fraction(0)

    def test_e1_eigenvalue_on_trivial(self):
        val = sum(E1_COEFF[j] * _P[0][j] for j in range(3))
        assert val == Fraction(0)

    def test_e2_eigenvalue_on_s_space(self):
        val = sum(E2_COEFF[j] * _P[2][j] for j in range(3))
        assert val == Fraction(1)

    def test_e2_eigenvalue_on_r_space(self):
        val = sum(E2_COEFF[j] * _P[1][j] for j in range(3))
        assert val == Fraction(0)

    def test_e2_eigenvalue_on_trivial(self):
        val = sum(E2_COEFF[j] * _P[0][j] for j in range(3))
        assert val == Fraction(0)

    def test_e0_eigenvalue_on_trivial(self):
        val = sum(E0_COEFF[j] * _P[0][j] for j in range(3))
        assert val == Fraction(1)


# ─────────────────────────────────────────────────────────────────────────────
class TestTrivialKreinParams:
    """q^0 Krein parameters (from E_0 orthogonality)."""

    def test_q0_00_is_one(self):
        assert KREIN_Q00[0] == Fraction(1)

    def test_q0_11_equals_mult_r(self):
        assert Q0_11 == Fraction(MULT_R)

    def test_q0_12_zero(self):
        assert Q0_12 == Fraction(0)

    def test_q0_22_equals_mult_s(self):
        assert Q0_22 == Fraction(MULT_S)

    def test_q0_mult_sum(self):
        # q^0_{00} + q^0_{11} + q^0_{22} = 1 + MULT_R + MULT_S = V
        total = KREIN_Q00[0] + Q0_11 + Q0_22
        assert total == Fraction(V)

    def test_q1_00_and_q2_00_zero(self):
        # On the trivial pair, only q^0 is non-zero
        assert KREIN_Q00[1] == Fraction(0)
        assert KREIN_Q00[2] == Fraction(0)


# ─────────────────────────────────────────────────────────────────────────────
class TestKreinQ11:
    """Non-trivial Krein parameters for the (E_1, E_1) pair."""

    def test_3q0_11(self):
        assert 3 * Q0_11 == Fraction(3 * MULT_R)

    def test_3q1_11(self):
        assert 3 * Q1_11 == Fraction(44)

    def test_3q2_11(self):
        assert 3 * Q2_11 == Fraction(V)  # = 40

    def test_q1_11_exact(self):
        assert Q1_11 == Fraction(44, 3)

    def test_q2_11_exact(self):
        assert Q2_11 == Fraction(40, 3)

    def test_q1_11_positive(self):
        assert Q1_11 > 0

    def test_q2_11_positive(self):
        assert Q2_11 > 0


# ─────────────────────────────────────────────────────────────────────────────
class TestKreinQ12:
    """Non-trivial Krein parameters for the (E_1, E_2) pair."""

    def test_q0_12_zero(self):
        assert Q0_12 == Fraction(0)

    def test_3q1_12(self):
        assert 3 * Q1_12 == Fraction(25)

    def test_3q2_12(self):
        assert 3 * Q2_12 == Fraction(32)

    def test_q1_12_exact(self):
        assert Q1_12 == Fraction(25, 3)

    def test_q2_12_exact(self):
        assert Q2_12 == Fraction(32, 3)

    def test_q1_12_positive(self):
        assert Q1_12 > 0

    def test_q2_12_positive(self):
        assert Q2_12 > 0


# ─────────────────────────────────────────────────────────────────────────────
class TestKreinQ22:
    """Non-trivial Krein parameters for the (E_2, E_2) pair."""

    def test_3q0_22(self):
        assert 3 * Q0_22 == Fraction(3 * MULT_S)

    def test_3q1_22(self):
        assert 3 * Q1_22 == Fraction(20)

    def test_3q2_22(self):
        assert 3 * Q2_22 == Fraction(ALPHA)  # = 10

    def test_q1_22_exact(self):
        assert Q1_22 == Fraction(20, 3)

    def test_q2_22_exact(self):
        assert Q2_22 == Fraction(10, 3)

    def test_q1_22_positive(self):
        assert Q1_22 > 0

    def test_q2_22_positive(self):
        assert Q2_22 > 0


# ─────────────────────────────────────────────────────────────────────────────
class TestKreinConditions:
    """Delsarte–Krein non-negativity conditions."""

    def test_all_krein_nonneg(self):
        assert ALL_KREIN_NONNEG is True

    def test_each_q11_nonneg(self):
        for val in KREIN_Q11:
            assert val >= 0

    def test_each_q12_nonneg(self):
        for val in KREIN_Q12:
            assert val >= 0

    def test_each_q22_nonneg(self):
        for val in KREIN_Q22:
            assert val >= 0


# ─────────────────────────────────────────────────────────────────────────────
class TestSMIdentities:
    """
    SM-connected identities encoded in the Krein parameter structure.
    """

    def test_3q2_11_equals_V(self):
        """3·q^2_{11} = V = 40: Krein parameter encodes vertex count."""
        assert 3 * Q2_11 == Fraction(V)

    def test_3q2_22_equals_alpha(self):
        """3·q^2_{22} = α = 10: Krein parameter equals Hoffman bound."""
        assert 3 * Q2_22 == Fraction(ALPHA)

    def test_q1_q2_11_sum_complement_valency(self):
        """q^1_{11} + q^2_{11} = V - K = 28."""
        assert Q1_11 + Q2_11 == Fraction(V - K)

    def test_q1_q2_22_sum_alpha(self):
        """q^1_{22} + q^2_{22} = α = 10."""
        assert Q1_22 + Q2_22 == Fraction(ALPHA)

    def test_3q1_12_equals_alpha_plus_mult_s(self):
        """3·q^1_{12} = α + MULT_S = 25."""
        assert 3 * Q1_12 == Fraction(ALPHA + MULT_S)

    def test_3q2_12_equals_mult_r_plus_2mu(self):
        """3·q^2_{12} = MULT_R + 2·MU = 32."""
        assert 3 * Q2_12 == Fraction(MULT_R + 2 * MU)

    def test_3_q1_11_plus_q1_22_equals_ew_cube(self):
        """3·(q^1_{11} + q^1_{22}) = EW_GAUGE_4^3 = 64."""
        assert 3 * (Q1_11 + Q1_22) == Fraction(EW_GAUGE_4 ** 3)

    def test_ew_cube_value(self):
        assert EW_GAUGE_4 ** 3 == 64

    def test_q0_11_equals_mult_r(self):
        """q^0_{11} = MULT_R = 24: trivial Krein parameter is multiplicity."""
        assert Q0_11 == Fraction(MULT_R)

    def test_q0_22_equals_mult_s(self):
        """q^0_{22} = MULT_S = 15: trivial Krein parameter is multiplicity."""
        assert Q0_22 == Fraction(MULT_S)


# ─────────────────────────────────────────────────────────────────────────────
class TestVerifyAll:
    """verify_all() must return exactly 27 checks, all passing."""

    def test_returns_triple(self):
        result = verify_all()
        assert len(result) == 3

    def test_total_is_27(self):
        _, _, total = verify_all()
        assert total == 27

    def test_all_pass(self):
        _, passed, total = verify_all()
        assert passed == total

    def test_passed_count(self):
        _, passed, _ = verify_all()
        assert passed == 27

    def test_checks_list_length(self):
        checks, _, _ = verify_all()
        assert len(checks) == 27

    def test_checks_have_ok_key(self):
        checks, _, _ = verify_all()
        for c in checks:
            assert "ok" in c
            assert c["ok"] is True

    def test_checks_have_name_key(self):
        checks, _, _ = verify_all()
        for c in checks:
            assert "name" in c
            assert isinstance(c["name"], str)


# ─────────────────────────────────────────────────────────────────────────────
class TestBuildSummary:
    """build_ccxcix_summary() structure and content."""

    def test_returns_dict(self):
        s = build_ccxcix_summary()
        assert isinstance(s, dict)

    def test_part_key(self):
        s = build_ccxcix_summary()
        assert s["part"] == "CCXCIX"

    def test_title_contains_krein(self):
        s = build_ccxcix_summary()
        assert "Krein" in s["title"]

    def test_checks_pass_27(self):
        s = build_ccxcix_summary()
        assert s["checks_pass"] == 27

    def test_checks_total_27(self):
        s = build_ccxcix_summary()
        assert s["checks_total"] == 27

    def test_status_pass(self):
        s = build_ccxcix_summary()
        assert s["status"] == "PASS"

    def test_fields_present(self):
        s = build_ccxcix_summary()
        for key in ("V", "K", "MULT_R", "MULT_S", "ALPHA",
                    "P_DET", "ALL_KREIN_NONNEG"):
            assert key in s["fields"]

    def test_p_det_in_fields(self):
        s = build_ccxcix_summary()
        assert s["fields"]["P_DET"] == -EDGES

    def test_discoveries_present(self):
        s = build_ccxcix_summary()
        assert "discoveries" in s
        assert len(s["discoveries"]) >= 5

    def test_all_krein_nonneg_in_fields(self):
        s = build_ccxcix_summary()
        assert s["fields"]["ALL_KREIN_NONNEG"] is True
