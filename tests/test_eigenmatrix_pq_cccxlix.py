"""
Tests for PART CCCXLIX -- First Eigenmatrix P and Dual Eigenmatrix Q of W(3,3)
"""
import sys
import json
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exploration"))
import PART_CCCXLIX_EIGENMATRIX_PQ_BRIDGE as B


class TestConstants:
    def test_v(self):
        assert B.V == 40

    def test_k(self):
        assert B.K == 12

    def test_l_complement_valency(self):
        assert B.L == 27

    def test_mult_r(self):
        assert B.MULT_R == 24

    def test_mult_s(self):
        assert B.MULT_S == 15

    def test_r_eig(self):
        assert B.R_EIG == 2

    def test_s_eig(self):
        assert B.S_EIG == -4

    def test_gut_dim(self):
        assert B.GUT_DIM == 27

    def test_alpha(self):
        assert B.ALPHA == 10

    def test_generations(self):
        assert B.GENERATIONS == 3

    def test_l_equals_gut_dim(self):
        assert B.L == B.GUT_DIM


class TestPMatrix:
    def test_p00(self):
        assert B.p_val(0, 0) == Fraction(1)

    def test_p01(self):
        assert B.p_val(0, 1) == Fraction(1)

    def test_p02(self):
        assert B.p_val(0, 2) == Fraction(1)

    def test_p10_equals_k(self):
        assert B.p_val(1, 0) == Fraction(B.K)

    def test_p11_equals_r_eig(self):
        assert B.p_val(1, 1) == Fraction(B.R_EIG)

    def test_p12_equals_s_eig(self):
        assert B.p_val(1, 2) == Fraction(B.S_EIG)

    def test_p20_equals_l(self):
        assert B.p_val(2, 0) == Fraction(B.L)

    def test_p21_equals_minus_r_minus_1(self):
        assert B.p_val(2, 1) == Fraction(-B.R_EIG - 1)

    def test_p21_value(self):
        assert B.p_val(2, 1) == Fraction(-3)

    def test_p22_equals_minus_s_minus_1(self):
        assert B.p_val(2, 2) == Fraction(-B.S_EIG - 1)

    def test_p22_value(self):
        assert B.p_val(2, 2) == Fraction(3)

    def test_row0_sum(self):
        assert B.p_row_sum(0) == Fraction(3)

    def test_weighted_row1_zero(self):
        assert B.weighted_row_sum(1) == Fraction(0)

    def test_weighted_row2_zero(self):
        assert B.weighted_row_sum(2) == Fraction(0)

    def test_col0_sum(self):
        # sum_s P[s][0] = 1 + K + L = 1 + 12 + 27 = 40 = V
        assert B.p_col_sum(0) == Fraction(B.V)

    def test_p10_plus_p20_equals_v_minus_1(self):
        assert B.p_val(1, 0) + B.p_val(2, 0) == Fraction(B.V - 1)


class TestQMatrix:
    def test_q00(self):
        assert B.q_val(0, 0) == Fraction(1)

    def test_q01(self):
        assert B.q_val(0, 1) == Fraction(1)

    def test_q02(self):
        assert B.q_val(0, 2) == Fraction(1)

    def test_q10_equals_mult_r(self):
        assert B.q_val(1, 0) == Fraction(B.MULT_R)

    def test_q20_equals_mult_s(self):
        assert B.q_val(2, 0) == Fraction(B.MULT_S)

    def test_q11_value(self):
        assert B.q_val(1, 1) == Fraction(B.MULT_R * B.R_EIG, B.K)

    def test_q11_equals_4(self):
        assert B.q_val(1, 1) == Fraction(4)

    def test_q22_value(self):
        assert B.q_val(2, 2) == Fraction(B.MULT_S * 3, B.L)

    def test_q22_equals_5_thirds(self):
        assert B.q_val(2, 2) == Fraction(5, 3)

    def test_q10_plus_q20_equals_v_minus_1(self):
        assert B.q_val(1, 0) + B.q_val(2, 0) == Fraction(B.V - 1)

    def test_q11_gt_0(self):
        assert B.q_val(1, 1) > 0

    def test_q21_value(self):
        # Q[2][1] = (MULT_S / K) * P[1][2] = (15/12)*(-4) = -5
        assert B.q_val(2, 1) == Fraction(-5)


class TestOrthogonality:
    def setup_method(self):
        self.pq = B.pq_product()

    def test_pq00_equals_v(self):
        assert self.pq[0][0] == Fraction(B.V)

    def test_pq11_equals_v(self):
        assert self.pq[1][1] == Fraction(B.V)

    def test_pq22_equals_v(self):
        assert self.pq[2][2] == Fraction(B.V)

    def test_pq01_zero(self):
        assert self.pq[0][1] == Fraction(0)

    def test_pq02_zero(self):
        assert self.pq[0][2] == Fraction(0)

    def test_pq10_zero(self):
        assert self.pq[1][0] == Fraction(0)

    def test_pq12_zero(self):
        assert self.pq[1][2] == Fraction(0)

    def test_pq20_zero(self):
        assert self.pq[2][0] == Fraction(0)

    def test_pq21_zero(self):
        assert self.pq[2][1] == Fraction(0)


class TestDeterminant:
    def test_det_p_value(self):
        assert B.p_det() == Fraction(-240)

    def test_abs_det_p_equals_edges(self):
        # W(3,3) has V*K/2 = 40*12/2 = 240 edges
        assert abs(B.p_det()) == Fraction(240)

    def test_abs_det_div_mult_r_equals_alpha(self):
        assert abs(B.p_det()) / Fraction(B.MULT_R) == Fraction(B.ALPHA)

    def test_det_q_value(self):
        det_q = B.q_det()
        # det(Q) = V^3 / det(P) = 64000 / (-240) = -800/3
        assert det_q == Fraction(B.V ** 3) / Fraction(-240)

    def test_det_p_negative(self):
        assert B.p_det() < 0


class TestTrace:
    def test_p_trace_value(self):
        assert B.p_trace() == Fraction(6)

    def test_p_trace_equals_2_generations(self):
        assert B.p_trace() == Fraction(2 * B.GENERATIONS)

    def test_p_trace_components(self):
        # 1 + 2 + 3 = 6
        assert B.p_val(0, 0) + B.p_val(1, 1) + B.p_val(2, 2) == Fraction(6)


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

    def test_no_failed_checks(self):
        checks, _, _ = B.verify_all()
        failed = [c["name"] for c in checks if not c["passed"]]
        assert failed == []


class TestSummary:
    def test_summary_part(self):
        s = B.build_cccxlix_summary()
        assert s["part"] == "CCCXLIX"

    def test_summary_status_pass(self):
        s = B.build_cccxlix_summary()
        assert s["status"] == "PASS"

    def test_summary_checks_pass_27(self):
        s = B.build_cccxlix_summary()
        assert s["checks_pass"] == 27

    def test_summary_checks_total_27(self):
        s = B.build_cccxlix_summary()
        assert s["checks_total"] == 27

    def test_summary_det_p(self):
        s = B.build_cccxlix_summary()
        assert s["fields"]["det_P"] == "-240"

    def test_summary_abs_det_p(self):
        s = B.build_cccxlix_summary()
        assert s["fields"]["abs_det_P"] == "240"

    def test_summary_trace_p(self):
        s = B.build_cccxlix_summary()
        assert s["fields"]["trace_P"] == "6"

    def test_json_file_exists(self):
        json_path = Path(__file__).resolve().parents[1] / "PART_CCCXLIX_eigenmatrix_pq_results.json"
        assert json_path.exists()

    def test_json_status_pass(self):
        json_path = Path(__file__).resolve().parents[1] / "PART_CCCXLIX_eigenmatrix_pq_results.json"
        data = json.loads(json_path.read_text(encoding="utf-8"))
        assert data["status"] == "PASS"

    def test_json_checks_pass_27(self):
        json_path = Path(__file__).resolve().parents[1] / "PART_CCCXLIX_eigenmatrix_pq_results.json"
        data = json.loads(json_path.read_text(encoding="utf-8"))
        assert data["checks_pass"] == 27
