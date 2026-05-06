"""Tests for PART CCCLIII: Eigenspace Projectors and Gram Matrices in W(3,3)."""
import sys
from pathlib import Path
from fractions import Fraction

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exploration"))

from PART_CCCLIII_EIGENSPACE_PROJECTORS_BRIDGE import (
    V, K, LAM, MU, EDGES, R_EIG, S_EIG, ABS_S, MULT_R, MULT_S, MULT_0,
    ALPHA, SU5_ADJ, SU5_MATTER, GENERATIONS, GUT_DIM, EW_GAUGE_4,
    e0_diag, e0_adj, e0_non_adj,
    er_diag, er_adj, er_non_adj,
    es_diag, es_adj, es_non_adj,
    row_sum_er, row_sum_es, er_trace, es_trace,
    er_diag_numerator, er_diag_denominator, es_diag_numerator,
    angle_set_er, angle_set_es,
    partition_of_identity_diag, partition_of_identity_adj, partition_of_identity_non_adj,
    verify_all, build_cccliii_summary,
)


class TestSRGConstants:
    def test_V(self): assert V == 40
    def test_K(self): assert K == 12
    def test_MULT_R(self): assert MULT_R == 24
    def test_MULT_S(self): assert MULT_S == 15
    def test_R_EIG(self): assert R_EIG == 2
    def test_S_EIG(self): assert S_EIG == -4
    def test_multiplicity_sum(self): assert MULT_0 + MULT_R + MULT_S == V
    def test_SU5_ADJ(self): assert SU5_ADJ == MULT_R
    def test_SU5_MATTER(self): assert SU5_MATTER == MULT_S


class TestE0Entries:
    def test_e0_diag(self): assert e0_diag() == Fraction(1, 40)
    def test_e0_adj(self): assert e0_adj() == Fraction(1, 40)
    def test_e0_non_adj(self): assert e0_non_adj() == Fraction(1, 40)
    def test_e0_constant(self): assert e0_diag() == e0_adj() == e0_non_adj()
    def test_e0_diag_formula(self): assert e0_diag() == Fraction(1, V)


class TestErDiagonal:
    def test_er_diag_value(self): assert er_diag() == Fraction(3, 5)
    def test_er_diag_formula(self): assert er_diag() == Fraction(MULT_R, V)
    def test_er_diag_numerator(self): assert er_diag_numerator() == 3
    def test_er_diag_denominator(self): assert er_diag_denominator() == 5


class TestErOffDiag:
    def test_er_adj(self): assert er_adj() == Fraction(1, 10)
    def test_er_non_adj(self): assert er_non_adj() == Fraction(-1, 15)
    def test_er_non_adj_neg(self): assert er_non_adj() < 0
    def test_er_adj_pos(self): assert er_adj() > 0


class TestEsEntries:
    def test_es_diag(self): assert es_diag() == Fraction(3, 8)
    def test_es_diag_formula(self): assert es_diag() == Fraction(MULT_S, V)
    def test_es_adj(self): assert es_adj() == Fraction(-1, 8)
    def test_es_non_adj(self): assert es_non_adj() == Fraction(1, 24)
    def test_es_adj_neg(self): assert es_adj() < 0
    def test_es_diag_numerator(self): assert es_diag_numerator() == 3
    def test_es_non_adj_pos(self): assert es_non_adj() > 0


class TestPartitionOfIdentity:
    def test_diag_sums_to_1(self):
        assert partition_of_identity_diag() == Fraction(1)
    def test_adj_sums_to_0(self):
        assert partition_of_identity_adj() == Fraction(0)
    def test_non_adj_sums_to_0(self):
        assert partition_of_identity_non_adj() == Fraction(0)
    def test_er_plus_es_adj(self):
        assert er_adj() + es_adj() == Fraction(-1, V)
    def test_er_plus_es_non_adj(self):
        assert er_non_adj() + es_non_adj() == Fraction(-1, V)


class TestBoseMesnerReconstructionA:
    def test_A_adj_from_projectors(self):
        # A_{ij} = k*(E0)_adj + r*(Er)_adj + s*(Es)_adj = 1 for adjacent
        val = K * e0_adj() + R_EIG * er_adj() + S_EIG * es_adj()
        assert val == Fraction(1)

    def test_A_non_adj_from_projectors(self):
        # A_{ij} = k*(E0) + r*(Er) + s*(Es) = 0 for non-adjacent
        val = K * e0_non_adj() + R_EIG * er_non_adj() + S_EIG * es_non_adj()
        assert val == Fraction(0)

    def test_I_diag_from_projectors(self):
        # (I)_ii = (E0)_ii + (Er)_ii + (Es)_ii = 1
        val = e0_diag() + er_diag() + es_diag()
        assert val == Fraction(1)


class TestTracesAndRanks:
    def test_er_trace(self): assert er_trace() == Fraction(MULT_R)
    def test_es_trace(self): assert es_trace() == Fraction(MULT_S)
    def test_row_sum_er(self): assert row_sum_er() == Fraction(0)
    def test_row_sum_es(self): assert row_sum_es() == Fraction(0)


class TestAngleSets:
    def test_angle_set_er_length(self): assert len(angle_set_er()) == 3
    def test_angle_set_es_length(self): assert len(angle_set_es()) == 3
    def test_angle_set_er_distinct(self): assert len(set(angle_set_er())) == 3
    def test_angle_set_er_contains_diag(self): assert Fraction(3, 5) in angle_set_er()
    def test_angle_set_er_contains_adj(self): assert Fraction(1, 10) in angle_set_er()
    def test_angle_set_er_contains_non_adj(self): assert Fraction(-1, 15) in angle_set_er()


class TestPhysicsConnections:
    def test_MULT_R_SU5(self): assert MULT_R == SU5_ADJ
    def test_MULT_S_SU5(self): assert MULT_S == SU5_MATTER
    def test_er_adj_V_eq_MU(self): assert er_adj() * V == Fraction(MU)
    def test_er_non_adj_denom_eq_MULT_S(self):
        assert er_non_adj().denominator == MULT_S


class TestVerifyAll:
    def setup_method(self):
        self.checks, self.passed, self.total = verify_all()

    def test_total_is_27(self): assert self.total == 27
    def test_all_pass(self): assert self.passed == self.total
    def test_checks_list_length(self): assert len(self.checks) == 27
    def test_all_checks_passed(self):
        failed = [c for c in self.checks if not c["passed"]]
        assert failed == [], f"Failed: {[c['name'] for c in failed]}"


class TestSummary:
    def setup_method(self):
        self.s = build_cccliii_summary()

    def test_part(self): assert self.s["part"] == "CCCLIII"
    def test_status(self): assert self.s["status"] == "PASS"
    def test_checks_pass(self): assert self.s["checks_pass"] == 27
    def test_checks_total(self): assert self.s["checks_total"] == 27
    def test_er_diag_field(self): assert self.s["fields"]["er_diag"] == "3/5"
    def test_er_adj_field(self): assert self.s["fields"]["er_adj"] == "1/10"
    def test_er_non_adj_field(self): assert self.s["fields"]["er_non_adj"] == "-1/15"
    def test_discoveries_nonempty(self): assert len(self.s["discoveries"]) >= 3
    def test_title_contains_eigenspace(self): assert "Eigenspace" in self.s["title"]
