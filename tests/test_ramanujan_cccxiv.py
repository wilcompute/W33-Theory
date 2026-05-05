"""Tests for PART CCCXIV — Ramanujan Property & Spectral Expanders of W(3,3)."""
import sys, os, pytest
from fractions import Fraction
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "exploration"))
from PART_CCCXIV_RAMANUJAN_BRIDGE import (
    V, K, R_EIG, S_EIG, ALPHA, GUT_DIM, GENERATIONS,
    RAMANUJAN_BOUND, ABS_R, ABS_S, IS_RAMANUJAN,
    SPECTRAL_GAP, verify_all, build_cccxiv_summary,
)

class TestRamanujan:
    def test_K_12(self): assert K == 12
    def test_R_EIG_2(self): assert R_EIG == 2
    def test_S_EIG_minus4(self): assert S_EIG == -4
    def test_is_ramanujan(self): assert IS_RAMANUJAN
    def test_spectral_gap_10(self): assert SPECTRAL_GAP == 10
    def test_abs_R_le_bound(self): assert ABS_R <= RAMANUJAN_BOUND
    def test_abs_S_le_bound(self): assert ABS_S <= RAMANUJAN_BOUND
    def test_spectral_gap_eq_alpha(self): assert SPECTRAL_GAP == ALPHA

class TestVerifyAll:
    def test_total_27(self):
        _, _, total = verify_all()
        assert total == 27
    def test_all_pass(self):
        checks, passed, total = verify_all()
        assert passed == total

class TestBuildSummary:
    def test_part_cccxiv(self):
        s = build_cccxiv_summary()
        assert s["part"] == "CCCXIV"
        assert s["status"] == "PASS"
