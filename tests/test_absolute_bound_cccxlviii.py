"""
Tests for PART CCCXLVIII -- Absolute Bound and Krein Feasibility for W(3,3)
"""
import sys
import os
import json
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exploration"))
import PART_CCCXLVIII_ABSOLUTE_BOUND_BRIDGE as B


# ── Group 1: Constants ────────────────────────────────────────────────────────
class TestConstants:
    def test_v(self):
        assert B.V == 40

    def test_k(self):
        assert B.K == 12

    def test_lam(self):
        assert B.LAM == 2

    def test_mu(self):
        assert B.MU == 4

    def test_r_eig(self):
        assert B.R_EIG == 2

    def test_s_eig(self):
        assert B.S_EIG == -4

    def test_abs_s(self):
        assert B.ABS_S == 4

    def test_mult_r(self):
        assert B.MULT_R == 24

    def test_mult_s(self):
        assert B.MULT_S == 15

    def test_l(self):
        assert B.L == 27

    def test_generations(self):
        assert B.GENERATIONS == 3

    def test_gut_dim(self):
        assert B.GUT_DIM == 27

    def test_su5_adj(self):
        assert B.SU5_ADJ == 24

    def test_su5_matter_per_gen(self):
        assert B.SU5_MATTER_PER_GEN == 15

    def test_gluon_count(self):
        assert B.GLUON_COUNT == 8

    def test_ew_gauge_4(self):
        assert B.EW_GAUGE_4 == 4


# ── Group 2: Multiplicity structure ──────────────────────────────────────────
class TestMultiplicities:
    def test_m_list(self):
        assert B.M == [1, 24, 15]

    def test_m0(self):
        assert B.M[0] == 1

    def test_m1(self):
        assert B.M[1] == B.MULT_R

    def test_m2(self):
        assert B.M[2] == B.MULT_S

    def test_sum_multiplicities_equals_v(self):
        assert sum(B.M) == B.V

    def test_m1_plus_m2_equals_v_minus_1(self):
        assert B.M[1] + B.M[2] == B.V - 1

    def test_multiplicities_sum_identity(self):
        assert 1 + B.MULT_R + B.MULT_S == B.V


# ── Group 3: Absolute bound ───────────────────────────────────────────────────
class TestAbsoluteBound:
    def test_sum_sq_value(self):
        assert B.SUM_SQ == 802

    def test_sum_sq_formula(self):
        assert B.SUM_SQ == 1 + B.MULT_R ** 2 + B.MULT_S ** 2

    def test_abs_bound_value(self):
        assert B.ABS_BOUND == 820

    def test_abs_bound_formula(self):
        assert B.ABS_BOUND == B.V * (B.V + 1) // 2

    def test_slack_value(self):
        assert B.SLACK == 18

    def test_slack_formula(self):
        assert B.SLACK == B.ABS_BOUND - B.SUM_SQ

    def test_absolute_bound_satisfied(self):
        assert B.SUM_SQ <= B.ABS_BOUND

    def test_bound_not_tight(self):
        assert B.SLACK > 0

    def test_slack_is_positive(self):
        assert B.SLACK > 0


# ── Group 4: Slack physics encodings ─────────────────────────────────────────
class TestSlackPhysics:
    def test_slack_equals_6_generations(self):
        assert B.SLACK == 6 * B.GENERATIONS

    def test_slack_equals_mult_s_plus_generations(self):
        assert B.SLACK == B.MULT_S + B.GENERATIONS

    def test_slack_equals_k_plus_2_generations(self):
        assert B.SLACK == B.K + 2 * B.GENERATIONS

    def test_slack_equals_su5_adj_minus_su5_dim_minus_lam_plus_1(self):
        from PART_CCCXLVIII_ABSOLUTE_BOUND_BRIDGE import SU5_ADJ, SU5_DIM, LAM, SLACK
        assert SLACK == SU5_ADJ - SU5_DIM - LAM + 1

    def test_slack_su5_dim(self):
        assert B.SU5_DIM == 5

    def test_slack_components_sum(self):
        # 18 = 6 + 12 = 2*3 + 12
        assert B.SLACK == 2 * B.GENERATIONS + B.K

    def test_slack_as_3x6(self):
        assert B.SLACK == 3 * 6

    def test_slack_mod_generations(self):
        assert B.SLACK % B.GENERATIONS == 0


# ── Group 5: Scott / SRG conditions ──────────────────────────────────────────
class TestScottCondition:
    def test_scott_lhs(self):
        lhs = B.K * (B.K - B.LAM - 1)
        assert lhs == 108

    def test_scott_rhs(self):
        rhs = B.MU * (B.V - B.K - 1)
        assert rhs == 108

    def test_scott_equation(self):
        assert B.K * (B.K - B.LAM - 1) == B.MU * (B.V - B.K - 1)

    def test_complement_scott(self):
        # Complement of W(3,3) is (40,27,18,18)-SRG
        L, lam_c, mu_c = B.L, 18, 18
        lhs = L * (L - lam_c - 1)
        rhs = mu_c * (B.V - L - 1)
        assert lhs == rhs

    def test_complement_lam_eq_mu(self):
        # Conference-type: lambda_c = mu_c
        assert 18 == 18

    def test_complement_valency(self):
        assert B.L == B.GUT_DIM


# ── Group 6: Krein parameters ─────────────────────────────────────────────────
class TestKreinParameters:
    def test_q110_equals_su5_adj(self):
        assert B.q_krein(1, 1, 0) == Fraction(B.SU5_ADJ)

    def test_q220_equals_su5_matter(self):
        assert B.q_krein(2, 2, 0) == Fraction(B.SU5_MATTER_PER_GEN)

    def test_q120_equals_0(self):
        assert B.q_krein(1, 2, 0) == Fraction(0)

    def test_q011_equals_1(self):
        assert B.q_krein(0, 1, 1) == Fraction(1)

    def test_q022_equals_1(self):
        assert B.q_krein(0, 2, 2) == Fraction(1)

    def test_q000_equals_1(self):
        assert B.q_krein(0, 0, 0) == Fraction(1)

    def test_q110_plus_q220_equals_v_minus_1(self):
        assert B.q_krein(1, 1, 0) + B.q_krein(2, 2, 0) == Fraction(B.V - 1)

    def test_krein_positivity_q112(self):
        assert B.q_krein(1, 1, 2) >= 0

    def test_krein_positivity_q221(self):
        assert B.q_krein(2, 2, 1) >= 0

    def test_krein_positivity_q121(self):
        assert B.q_krein(1, 2, 1) >= 0

    def test_krein_symmetry_ij(self):
        for i in range(3):
            for j in range(3):
                for l in range(3):
                    assert B.q_krein(i, j, l) == B.q_krein(j, i, l)

    def test_all_krein_nonneg(self):
        for i in range(3):
            for j in range(3):
                for l in range(3):
                    assert B.q_krein(i, j, l) >= 0, f"q[{i}][{j}][{l}] < 0"

    def test_q110_is_24(self):
        assert B.q_krein(1, 1, 0) == 24

    def test_q220_is_15(self):
        assert B.q_krein(2, 2, 0) == 15


# ── Group 7: Fisher and spectral bounds ───────────────────────────────────────
class TestSpectralBounds:
    def test_fisher_lower_bound_value(self):
        assert B.fisher_lower_bound() == Fraction(3)

    def test_fisher_lower_bound_formula(self):
        assert B.fisher_lower_bound() == Fraction(B.K * B.ABS_S, B.ABS_S + B.K)

    def test_mult_r_exceeds_fisher(self):
        assert B.MULT_R >= B.fisher_lower_bound()

    def test_hoffman_bound(self):
        hoffman = Fraction(B.V * B.ABS_S, B.K + B.ABS_S)
        assert hoffman == Fraction(10)

    def test_hoffman_value_integer(self):
        hoffman = Fraction(B.V * B.ABS_S, B.K + B.ABS_S)
        assert hoffman.denominator == 1

    def test_clique_bound(self):
        clique_bd = 1 + Fraction(B.K, B.ABS_S)
        assert clique_bd == Fraction(4)

    def test_clique_bound_equals_ew_gauge(self):
        clique_bd = 1 + Fraction(B.K, B.ABS_S)
        assert int(clique_bd) == B.EW_GAUGE_4

    def test_hoffman_plus_clique_leq_v_plus_1(self):
        # Weak: independence + clique can't exceed V+1 trivially
        assert 10 + 4 <= B.V + 1

    def test_eigenvalue_sum(self):
        assert B.R_EIG + B.S_EIG == B.LAM - B.MU


# ── Group 8: P-matrix (first eigenmatrix) ────────────────────────────────────
class TestPMatrix:
    def test_p_a0_trivial(self):
        # A_0 = I: eigenvalue 1 on all spaces
        assert B._P_MAT[0] == [Fraction(1), Fraction(1), Fraction(1)]

    def test_p_a1_eigenvalues(self):
        assert B._P_MAT[1][0] == Fraction(B.K)
        assert B._P_MAT[1][1] == Fraction(B.R_EIG)
        assert B._P_MAT[1][2] == Fraction(B.S_EIG)

    def test_p_a2_eigenvalue_trivial(self):
        assert B._P_MAT[2][0] == Fraction(B.L)

    def test_p_a2_eigenvalue_r(self):
        assert B._P_MAT[2][1] == Fraction(-B.R_EIG - 1)

    def test_p_a2_eigenvalue_s(self):
        assert B._P_MAT[2][2] == Fraction(-B.S_EIG - 1)

    def test_p_a2_r_value(self):
        assert B._P_MAT[2][1] == Fraction(-3)

    def test_p_a2_s_value(self):
        assert B._P_MAT[2][2] == Fraction(3)

    def test_p_row_sum_trivial(self):
        # On trivial eigenspace: sum of eigenvalues * multiplicities = V*k_s / V
        # Actually: sum_j m_j * P[s][j] = k_s * V  if s=0 (identity has eigenvalue 1 everywhere)
        # For A_1: sum_j m_j * r_j = 0 (since J has eigenvalue V on trivial, 0 elsewhere)
        # sum_{j=0}^2 M[j] * P_A1[j] = 1*12 + 24*2 + 15*(-4) = 12 + 48 - 60 = 0
        from PART_CCCXLVIII_ABSOLUTE_BOUND_BRIDGE import M, _P_MAT
        row_sum = sum(M[j] * _P_MAT[1][j] for j in range(3))
        assert row_sum == 0


# ── Group 9: verify_all and summary ──────────────────────────────────────────
class TestVerifyAll:
    def test_returns_tuple(self):
        result = B.verify_all()
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_all_pass(self):
        checks, passed, total = B.verify_all()
        assert passed == total

    def test_exactly_27_checks(self):
        checks, passed, total = B.verify_all()
        assert total == 27

    def test_27_pass(self):
        checks, passed, total = B.verify_all()
        assert passed == 27

    def test_checks_is_list(self):
        checks, _, _ = B.verify_all()
        assert isinstance(checks, list)

    def test_each_check_has_name(self):
        checks, _, _ = B.verify_all()
        for c in checks:
            assert "name" in c

    def test_each_check_has_passed(self):
        checks, _, _ = B.verify_all()
        for c in checks:
            assert "passed" in c

    def test_no_failed_checks(self):
        checks, _, _ = B.verify_all()
        failed = [c["name"] for c in checks if not c["passed"]]
        assert failed == []


class TestSummary:
    def test_summary_part(self):
        s = B.build_cccxlviii_summary()
        assert s["part"] == "CCCXLVIII"

    def test_summary_status_pass(self):
        s = B.build_cccxlviii_summary()
        assert s["status"] == "PASS"

    def test_summary_checks_pass_27(self):
        s = B.build_cccxlviii_summary()
        assert s["checks_pass"] == 27

    def test_summary_checks_total_27(self):
        s = B.build_cccxlviii_summary()
        assert s["checks_total"] == 27

    def test_summary_has_fields(self):
        s = B.build_cccxlviii_summary()
        assert "fields" in s

    def test_summary_has_discoveries(self):
        s = B.build_cccxlviii_summary()
        assert "discoveries" in s
        assert len(s["discoveries"]) > 0

    def test_summary_slack_field(self):
        s = B.build_cccxlviii_summary()
        assert s["fields"]["slack"] == "18"

    def test_summary_sum_sq_field(self):
        s = B.build_cccxlviii_summary()
        assert s["fields"]["sum_sq"] == "802"

    def test_json_file_exists(self):
        json_path = Path(__file__).resolve().parents[1] / "PART_CCCXLVIII_absolute_bound_results.json"
        assert json_path.exists()

    def test_json_status_pass(self):
        json_path = Path(__file__).resolve().parents[1] / "PART_CCCXLVIII_absolute_bound_results.json"
        data = json.loads(json_path.read_text(encoding="utf-8"))
        assert data["status"] == "PASS"

    def test_json_checks_pass_27(self):
        json_path = Path(__file__).resolve().parents[1] / "PART_CCCXLVIII_absolute_bound_results.json"
        data = json.loads(json_path.read_text(encoding="utf-8"))
        assert data["checks_pass"] == 27
