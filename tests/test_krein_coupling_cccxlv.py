"""
Tests for PART CCCXLV -- Krein Coupling Constants: Dual Algebra Structure of W(3,3)
"""
import json
import sys
from fractions import Fraction
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exploration"))
from PART_CCCXLV_KREIN_COUPLING_BRIDGE import (
    V, K, LAM, MU, R_EIG, S_EIG, ABS_S,
    MULT_R, MULT_S, L,
    M_MULT, P_MAT, K_VAL,
    SU5_DIM, SU5_ADJ, SU5_MATTER_PER_GEN, GENERATIONS, GUT_DIM,
    compute_krein, krein, verify_all, build_cccxlv_summary,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def Q():
    return compute_krein()


@pytest.fixture(scope="module")
def verify_result():
    return verify_all()


@pytest.fixture(scope="module")
def summary():
    return build_cccxlv_summary()


# ── Group 1: Graph and scheme constants ──────────────────────────────────────

class TestConstants:
    def test_V(self):
        assert V == 40

    def test_K(self):
        assert K == 12

    def test_MULT_R(self):
        assert MULT_R == 24

    def test_MULT_S(self):
        assert MULT_S == 15

    def test_multiplicities_sum(self):
        assert 1 + MULT_R + MULT_S == V

    def test_L_complement_valency(self):
        assert L == V - K - 1

    def test_L_value(self):
        assert L == 27

    def test_R_EIG(self):
        assert R_EIG == 2

    def test_S_EIG(self):
        assert S_EIG == -4

    def test_ABS_S(self):
        assert ABS_S == 4

    def test_ABS_S_equals_neg_S_EIG(self):
        assert ABS_S == -S_EIG


# ── Group 2: P-matrix structure ───────────────────────────────────────────────

class TestPMatrix:
    def test_P_trivial_row(self):
        # All-ones row: eigenvalue of I on any eigenspace is 1
        assert all(P_MAT[0][j] == Fraction(1) for j in range(3))

    def test_P_adjacency_trivial(self):
        assert P_MAT[1][0] == Fraction(K)

    def test_P_adjacency_R(self):
        assert P_MAT[1][1] == Fraction(R_EIG)

    def test_P_adjacency_S(self):
        assert P_MAT[1][2] == Fraction(S_EIG)

    def test_P_complement_trivial(self):
        assert P_MAT[2][0] == Fraction(L)

    def test_P_complement_R(self):
        assert P_MAT[2][1] == Fraction(-R_EIG - 1)

    def test_P_complement_S(self):
        assert P_MAT[2][2] == Fraction(-S_EIG - 1)

    def test_P_complement_R_value(self):
        assert P_MAT[2][1] == Fraction(-3)

    def test_P_complement_S_value(self):
        assert P_MAT[2][2] == Fraction(3)


# ── Group 3: E_0 coupling (trivial idempotent acts as identity) ───────────────

class TestE0Coupling:
    def test_q_00_0(self):
        assert krein(0, 0, 0) == Fraction(1)

    def test_q_00_1(self):
        assert krein(0, 0, 1) == Fraction(0)

    def test_q_00_2(self):
        assert krein(0, 0, 2) == Fraction(0)

    def test_q_01_0(self):
        assert krein(0, 1, 0) == Fraction(0)

    def test_q_01_1(self):
        assert krein(0, 1, 1) == Fraction(1)

    def test_q_01_2(self):
        assert krein(0, 1, 2) == Fraction(0)

    def test_q_02_0(self):
        assert krein(0, 2, 0) == Fraction(0)

    def test_q_02_1(self):
        assert krein(0, 2, 1) == Fraction(0)

    def test_q_02_2(self):
        assert krein(0, 2, 2) == Fraction(1)

    def test_q0j_identity_R(self):
        # q[0][j][l] = delta_{jl}
        for l in range(3):
            assert krein(0, 1, l) == (Fraction(1) if l == 1 else Fraction(0))

    def test_q0j_identity_S(self):
        for l in range(3):
            assert krein(0, 2, l) == (Fraction(1) if l == 2 else Fraction(0))


# ── Group 4: Trivial-output self-couplings ────────────────────────────────────

class TestTrivialOutputs:
    def test_q_11_0_equals_MULT_R(self):
        assert krein(1, 1, 0) == Fraction(MULT_R)

    def test_q_22_0_equals_MULT_S(self):
        assert krein(2, 2, 0) == Fraction(MULT_S)

    def test_q_12_0_equals_zero(self):
        assert krein(1, 2, 0) == Fraction(0)

    def test_q_11_0_equals_SU5_ADJ(self):
        assert krein(1, 1, 0) == Fraction(SU5_ADJ)

    def test_q_22_0_equals_SU5_MATTER(self):
        assert krein(2, 2, 0) == Fraction(SU5_MATTER_PER_GEN)

    def test_q_11_0_plus_q_22_0(self):
        assert krein(1, 1, 0) + krein(2, 2, 0) == Fraction(V - 1)


# ── Group 5: Exact rational Krein values ─────────────────────────────────────

class TestRationalKreinValues:
    def test_q_11_1(self):
        assert krein(1, 1, 1) == Fraction(44, 3)

    def test_q_11_2(self):
        assert krein(1, 1, 2) == Fraction(40, 3)

    def test_q_12_1(self):
        assert krein(1, 2, 1) == Fraction(25, 3)

    def test_q_12_2(self):
        assert krein(1, 2, 2) == Fraction(32, 3)

    def test_q_22_1(self):
        assert krein(2, 2, 1) == Fraction(20, 3)

    def test_q_22_2(self):
        assert krein(2, 2, 2) == Fraction(10, 3)

    def test_all_nontrivial_denominators_are_3(self):
        for (i, j) in [(1, 1), (1, 2), (2, 2)]:
            for l in [1, 2]:
                assert krein(i, j, l).denominator == 3

    def test_all_values_are_fractions(self):
        for i in range(3):
            for j in range(3):
                for l in range(3):
                    assert isinstance(krein(i, j, l), Fraction)


# ── Group 6: Krein condition and symmetry ─────────────────────────────────────

class TestKreinConditionAndSymmetry:
    def test_all_nonnegative(self):
        for i in range(3):
            for j in range(3):
                for l in range(3):
                    assert krein(i, j, l) >= 0, f"q[{i}][{j}][{l}] < 0"

    def test_symmetry_ij(self):
        for i in range(3):
            for j in range(3):
                for l in range(3):
                    assert krein(i, j, l) == krein(j, i, l), \
                        f"q[{i}][{j}][{l}] != q[{j}][{i}][{l}]"

    def test_sum_rule_11(self):
        s = sum(krein(1, 1, l) * M_MULT[l] for l in range(3))
        assert s == Fraction(MULT_R ** 2)

    def test_sum_rule_12(self):
        s = sum(krein(1, 2, l) * M_MULT[l] for l in range(3))
        assert s == Fraction(MULT_R * MULT_S)

    def test_sum_rule_22(self):
        s = sum(krein(2, 2, l) * M_MULT[l] for l in range(3))
        assert s == Fraction(MULT_S ** 2)

    def test_sum_rule_00(self):
        s = sum(krein(0, 0, l) * M_MULT[l] for l in range(3))
        assert s == Fraction(1)  # m_0^2 = 1

    def test_sum_rule_01(self):
        s = sum(krein(0, 1, l) * M_MULT[l] for l in range(3))
        assert s == Fraction(MULT_R)  # m_0 * m_1


# ── Group 7: Physical ratio identities ───────────────────────────────────────

class TestPhysicalRatios:
    def test_eigenvalue_ratio_in_dual_algebra(self):
        # The SRG eigenvalue ratio |s|/r appears in the dual algebra
        assert krein(2, 2, 1) / krein(2, 2, 2) == Fraction(ABS_S, R_EIG)

    def test_eigenvalue_ratio_value(self):
        assert krein(2, 2, 1) / krein(2, 2, 2) == Fraction(2)

    def test_gauge_sector_sum(self):
        assert krein(1, 1, 1) + krein(1, 1, 2) == Fraction(V - K)

    def test_gauge_sector_sum_value(self):
        assert krein(1, 1, 1) + krein(1, 1, 2) == Fraction(28)

    def test_matter_sector_sum(self):
        assert krein(2, 2, 1) + krein(2, 2, 2) == Fraction(K - R_EIG)

    def test_matter_sector_sum_value(self):
        assert krein(2, 2, 1) + krein(2, 2, 2) == Fraction(10)

    def test_cross_sector_sum(self):
        assert krein(1, 2, 1) + krein(1, 2, 2) == Fraction(V - R_EIG, 2)

    def test_cross_sector_sum_value(self):
        assert krein(1, 2, 1) + krein(1, 2, 2) == Fraction(19)

    def test_cross_sum_is_arithmetic_mean(self):
        gauge = krein(1, 1, 1) + krein(1, 1, 2)
        matter = krein(2, 2, 1) + krein(2, 2, 2)
        cross = krein(1, 2, 1) + krein(1, 2, 2)
        assert cross == (gauge + matter) / 2

    def test_output_ratio_11_22(self):
        # q[1][1][2] / q[2][2][2] = V / (K - R_EIG) = 4
        assert krein(1, 1, 2) / krein(2, 2, 2) == Fraction(V, K - R_EIG)

    def test_output_ratio_value(self):
        assert krein(1, 1, 2) / krein(2, 2, 2) == Fraction(4)


# ── Group 8: verify_all and summary ──────────────────────────────────────────

class TestVerifyAll:
    def test_returns_tuple_of_three(self, verify_result):
        checks, passed, total = verify_result
        assert isinstance(checks, list)
        assert isinstance(passed, int)
        assert isinstance(total, int)

    def test_total_is_27(self, verify_result):
        _, _, total = verify_result
        assert total == 27

    def test_passed_is_27(self, verify_result):
        _, passed, _ = verify_result
        assert passed == 27

    def test_no_failures(self, verify_result):
        checks, _, _ = verify_result
        failures = [c["name"] for c in checks if not c["passed"]]
        assert failures == []

    def test_all_checks_have_name(self, verify_result):
        checks, _, _ = verify_result
        assert all("name" in c for c in checks)

    def test_all_checks_have_passed_field(self, verify_result):
        checks, _, _ = verify_result
        assert all("passed" in c for c in checks)

    def test_summary_status_pass(self, summary):
        assert summary["status"] == "PASS"

    def test_summary_checks_pass_27(self, summary):
        assert summary["checks_pass"] == 27

    def test_summary_checks_total_27(self, summary):
        assert summary["checks_total"] == 27

    def test_summary_part_label(self, summary):
        assert summary["part"] == "CCCXLV"

    def test_summary_has_fields(self, summary):
        assert "fields" in summary

    def test_summary_q_11_0(self, summary):
        assert summary["fields"]["q_11_0"] == "24"

    def test_summary_q_22_0(self, summary):
        assert summary["fields"]["q_22_0"] == "15"

    def test_summary_q_12_0(self, summary):
        assert summary["fields"]["q_12_0"] == "0"

    def test_summary_krein_ratio(self, summary):
        assert summary["fields"]["krein_ratio_22"] == "2"

    def test_summary_has_discoveries(self, summary):
        assert len(summary["discoveries"]) >= 5

    def test_json_output_exists(self):
        out = Path(__file__).resolve().parents[1] / "PART_CCCXLV_krein_coupling_results.json"
        assert out.exists()

    def test_json_output_valid(self):
        out = Path(__file__).resolve().parents[1] / "PART_CCCXLV_krein_coupling_results.json"
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["status"] == "PASS"
        assert data["checks_pass"] == 27
        assert data["fields"]["q_11_0"] == "24"
        assert data["fields"]["q_22_0"] == "15"
        assert data["fields"]["krein_ratio_22"] == "2"
