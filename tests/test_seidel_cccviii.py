"""Tests for PART CCCVIII — Seidel Matrix Spectrum of W(3,3)"""
import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'exploration'))

from PART_CCCVIII_SEIDEL_BRIDGE import (
    V, K, LAM, MU, EDGES, R_EIG, S_EIG, MULT_R, MULT_S,
    EW_GAUGE_4, ALPHA, GUT_DIM, GENERATIONS,
    SEI_EIG_0, SEI_EIG_1, SEI_EIG_2,
    SEI_MULT_0, SEI_MULT_1, SEI_MULT_2, SEI_MULT_SUM,
    SEI_SPEC_SUM,
    SEI_TRACE_SQ_EIG, SEI_TRACE_SQ_VM,
    SEI_EIG0_EQ_MULTS, SEI_MULTS_SUM_VM1,
    SEI_EIG0_SM, SEI_EIG1_SM, SEI_EIG2_SM_A, SEI_EIG2_SM_B,
    SEI_TRACE_SQ_SM1, SEI_TRACE_SQ_SM2,
    SEI_DIFF_01, SEI_DIFF_01_SM,
    SEI_SUM_02, SEI_SUM_02_SM,
    SEI_SUM_0ABS1, SEI_SUM_0ABS1_SM,
    SEI_DIFF_21, SEI_DIFF_21_SM,
    verify_all, build_cccviii_summary,
)


class TestSRGConstants:
    def test_V_K(self):
        assert V == 40 and K == 12

    def test_edges(self):
        assert EDGES == 240

    def test_adj_eigenvalues(self):
        assert R_EIG == 2 and S_EIG == -4

    def test_multiplicities(self):
        assert MULT_R == 24 and MULT_S == 15

    def test_sm_constants(self):
        assert ALPHA == 10 and MU == 4 and LAM == 2
        assert GENERATIONS == 3


class TestSeidelEigenvalues:
    def test_sei_eig_0(self):
        assert SEI_EIG_0 == 15
        assert SEI_EIG_0 == V - 1 - 2 * K

    def test_sei_eig_1(self):
        assert SEI_EIG_1 == -5
        assert SEI_EIG_1 == -(1 + 2 * R_EIG)

    def test_sei_eig_2(self):
        assert SEI_EIG_2 == 7
        assert SEI_EIG_2 == -(1 + 2 * S_EIG)

    def test_multiplicities(self):
        assert SEI_MULT_0 == 1
        assert SEI_MULT_1 == MULT_R == 24
        assert SEI_MULT_2 == MULT_S == 15

    def test_mult_sum(self):
        assert SEI_MULT_SUM == V == 40

    def test_trace_zero(self):
        assert SEI_SPEC_SUM == 0


class TestSpectralIdentities:
    def test_trace_sq_eig(self):
        assert SEI_TRACE_SQ_EIG == 1560

    def test_trace_sq_vm(self):
        assert SEI_TRACE_SQ_VM == 1560
        assert SEI_TRACE_SQ_VM == V * (V - 1)

    def test_trace_sq_agree(self):
        assert SEI_TRACE_SQ_EIG == SEI_TRACE_SQ_VM

    def test_eig0_eq_mults(self):
        assert SEI_EIG0_EQ_MULTS is True
        assert SEI_EIG_0 == MULT_S

    def test_mults_sum_vm1(self):
        assert SEI_MULTS_SUM_VM1 is True
        assert MULT_R + MULT_S == V - 1

    def test_ordering(self):
        # 15 > 7 > 0 > -5
        assert SEI_EIG_0 > SEI_EIG_2 > 0 > SEI_EIG_1


class TestSMEncodings:
    def test_eig0_sm(self):
        assert SEI_EIG0_SM is True
        assert SEI_EIG_0 == ALPHA + GENERATIONS + LAM

    def test_eig1_sm(self):
        assert SEI_EIG1_SM is True
        assert SEI_EIG_1 == -(MU + 1)

    def test_eig2_sm_a(self):
        assert SEI_EIG2_SM_A is True
        assert SEI_EIG_2 == LAM + MU + 1

    def test_eig2_sm_b(self):
        assert SEI_EIG2_SM_B is True
        assert SEI_EIG_2 == K // 2 + 1

    def test_trace_sq_sm1(self):
        assert SEI_TRACE_SQ_SM1 == 1560
        assert SEI_TRACE_SQ_SM1 == ALPHA * (V - 1) * MU


class TestSeidelSRGRelationships:
    def test_diff_01(self):
        assert SEI_DIFF_01 == 10
        assert SEI_DIFF_01 == SEI_EIG_0 - abs(SEI_EIG_1)

    def test_diff_01_sm(self):
        assert SEI_DIFF_01_SM is True
        assert SEI_DIFF_01 == ALPHA

    def test_sum_02(self):
        assert SEI_SUM_02 == 22
        assert SEI_SUM_02 == SEI_EIG_0 + SEI_EIG_2

    def test_sum_02_sm(self):
        assert SEI_SUM_02_SM is True
        assert SEI_SUM_02 == 2 * (K - 1)

    def test_sum_0abs1(self):
        assert SEI_SUM_0ABS1 == 20
        assert SEI_SUM_0ABS1 == SEI_EIG_0 + abs(SEI_EIG_1)

    def test_sum_0abs1_sm(self):
        assert SEI_SUM_0ABS1_SM is True
        assert SEI_SUM_0ABS1 == 2 * ALPHA

    def test_diff_21(self):
        assert SEI_DIFF_21 == 2
        assert SEI_DIFF_21 == SEI_EIG_2 - abs(SEI_EIG_1)

    def test_diff_21_sm(self):
        assert SEI_DIFF_21_SM is True
        assert SEI_DIFF_21 == LAM


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
        self.s = build_cccviii_summary()

    def test_part(self):
        assert self.s["part"] == "CCCVIII"

    def test_status(self):
        assert self.s["status"] == "PASS"

    def test_checks(self):
        assert self.s["checks_pass"] == 27
        assert self.s["checks_total"] == 27

    def test_title(self):
        assert "Seidel" in self.s["title"]

    def test_fields(self):
        f = self.s["fields"]
        assert f["SEI_EIG_0"] == 15
        assert f["SEI_EIG_1"] == -5
        assert f["SEI_EIG_2"] == 7
        assert f["SEI_TRACE_SQ_EIG"] == 1560

    def test_discoveries(self):
        assert len(self.s["discoveries"]) >= 5
