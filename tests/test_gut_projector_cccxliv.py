"""
Tests for PART CCCXLIV -- Three-Idempotent GUT Projector Decomposition
"""
import json
import sys
from fractions import Fraction
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exploration"))
from PART_CCCXLIV_GUT_PROJECTOR_BRIDGE import (
    V, K, LAM, MU, R_EIG, S_EIG, ABS_S,
    MULT_R, MULT_S,
    EW_GAUGE_4, GENERATIONS, GUT_DIM, ALPHA,
    SU5_DIM, SU5_ADJ, SU5_MATTER_PER_GEN, SU5_TOTAL_MATTER,
    E0_I, E0_A, E0_J,
    E1_I, E1_A, E1_J,
    E2_I, E2_A, E2_J,
    _trace, rank_E0, rank_E1, rank_E2,
    eigenval_on, verify_all, build_cccxliv_summary,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def verify_result():
    return verify_all()


@pytest.fixture(scope="module")
def summary():
    return build_cccxliv_summary()


# ── Group 1: SU(5) GUT constants ─────────────────────────────────────────────

class TestGUTConstants:
    def test_su5_dim(self):
        assert SU5_DIM == 5

    def test_su5_adj_formula(self):
        assert SU5_ADJ == SU5_DIM ** 2 - 1

    def test_su5_adj_value(self):
        assert SU5_ADJ == 24

    def test_su5_matter_per_gen(self):
        assert SU5_MATTER_PER_GEN == 15

    def test_su5_total_matter(self):
        assert SU5_TOTAL_MATTER == GENERATIONS * SU5_MATTER_PER_GEN

    def test_su5_total_matter_value(self):
        assert SU5_TOTAL_MATTER == 45

    def test_gut_dim_minus_k(self):
        assert GUT_DIM - K == 15

    def test_gut_dim_minus_k_equals_matter(self):
        assert GUT_DIM - K == SU5_MATTER_PER_GEN


# ── Group 2: Idempotent coefficients ─────────────────────────────────────────

class TestIdempotentCoefficients:
    def test_E0_I_coeff(self):
        assert E0_I == Fraction(0)

    def test_E0_A_coeff(self):
        assert E0_A == Fraction(0)

    def test_E0_J_coeff(self):
        assert E0_J == Fraction(1, V)

    def test_E1_I_coeff(self):
        assert E1_I == Fraction(2, 3)

    def test_E1_A_coeff(self):
        assert E1_A == Fraction(1, 6)

    def test_E1_J_coeff(self):
        assert E1_J == Fraction(-1, 15)

    def test_E2_I_coeff(self):
        assert E2_I == Fraction(1, 3)

    def test_E2_A_coeff(self):
        assert E2_A == Fraction(-1, 6)

    def test_E2_J_coeff(self):
        assert E2_J == Fraction(1, 24)

    def test_all_coefficients_are_fractions(self):
        for val in [E0_I, E0_A, E0_J, E1_I, E1_A, E1_J, E2_I, E2_A, E2_J]:
            assert isinstance(val, Fraction)

    def test_A_coeff_antisymmetry(self):
        assert E1_A == -E2_A

    def test_I_coeff_ratio(self):
        assert E1_I / E2_I == Fraction(2, 1)


# ── Group 3: Trace and rank formulas ─────────────────────────────────────────

class TestTraceAndRank:
    def test_trace_E0(self):
        assert _trace(E0_I, E0_A, E0_J) == Fraction(1)

    def test_trace_E1(self):
        assert _trace(E1_I, E1_A, E1_J) == Fraction(24)

    def test_trace_E2(self):
        assert _trace(E2_I, E2_A, E2_J) == Fraction(15)

    def test_rank_E0_value(self):
        assert rank_E0() == 1

    def test_rank_E1_value(self):
        assert rank_E1() == 24

    def test_rank_E2_value(self):
        assert rank_E2() == 15

    def test_rank_E1_equals_MULT_R(self):
        assert rank_E1() == MULT_R

    def test_rank_E2_equals_MULT_S(self):
        assert rank_E2() == MULT_S

    def test_rank_sum_equals_V(self):
        assert rank_E0() + rank_E1() + rank_E2() == V

    def test_rank_ratio_E1_E2(self):
        assert Fraction(rank_E1(), rank_E2()) == Fraction(8, 5)


# ── Group 4: Eigenspace projections ──────────────────────────────────────────

class TestEigenspaceProjections:
    def test_E0_on_K_eigenspace(self):
        assert eigenval_on(E0_I, E0_A, E0_J, K) == Fraction(1)

    def test_E0_on_R_eigenspace(self):
        assert eigenval_on(E0_I, E0_A, E0_J, R_EIG) == Fraction(0)

    def test_E0_on_S_eigenspace(self):
        assert eigenval_on(E0_I, E0_A, E0_J, S_EIG) == Fraction(0)

    def test_E1_on_K_eigenspace(self):
        assert eigenval_on(E1_I, E1_A, E1_J, K) == Fraction(0)

    def test_E1_on_R_eigenspace(self):
        assert eigenval_on(E1_I, E1_A, E1_J, R_EIG) == Fraction(1)

    def test_E1_on_S_eigenspace(self):
        assert eigenval_on(E1_I, E1_A, E1_J, S_EIG) == Fraction(0)

    def test_E2_on_K_eigenspace(self):
        assert eigenval_on(E2_I, E2_A, E2_J, K) == Fraction(0)

    def test_E2_on_R_eigenspace(self):
        assert eigenval_on(E2_I, E2_A, E2_J, R_EIG) == Fraction(0)

    def test_E2_on_S_eigenspace(self):
        assert eigenval_on(E2_I, E2_A, E2_J, S_EIG) == Fraction(1)

    def test_projection_sum_on_K_eigenspace(self):
        total = (eigenval_on(E0_I, E0_A, E0_J, K)
                 + eigenval_on(E1_I, E1_A, E1_J, K)
                 + eigenval_on(E2_I, E2_A, E2_J, K))
        assert total == Fraction(1)

    def test_projection_sum_on_R_eigenspace(self):
        total = (eigenval_on(E0_I, E0_A, E0_J, R_EIG)
                 + eigenval_on(E1_I, E1_A, E1_J, R_EIG)
                 + eigenval_on(E2_I, E2_A, E2_J, R_EIG))
        assert total == Fraction(1)

    def test_projection_sum_on_S_eigenspace(self):
        total = (eigenval_on(E0_I, E0_A, E0_J, S_EIG)
                 + eigenval_on(E1_I, E1_A, E1_J, S_EIG)
                 + eigenval_on(E2_I, E2_A, E2_J, S_EIG))
        assert total == Fraction(1)

    def test_A_reconstruction_K_eigenspace(self):
        # k*E0 + r*E1 + s*E2 should equal A; on K-eigenspace: K*1 + R*0 + S*0 = K
        val = (K * eigenval_on(E0_I, E0_A, E0_J, K)
               + R_EIG * eigenval_on(E1_I, E1_A, E1_J, K)
               + S_EIG * eigenval_on(E2_I, E2_A, E2_J, K))
        assert val == K

    def test_A_reconstruction_R_eigenspace(self):
        val = (K * eigenval_on(E0_I, E0_A, E0_J, R_EIG)
               + R_EIG * eigenval_on(E1_I, E1_A, E1_J, R_EIG)
               + S_EIG * eigenval_on(E2_I, E2_A, E2_J, R_EIG))
        assert val == R_EIG

    def test_A_reconstruction_S_eigenspace(self):
        val = (K * eigenval_on(E0_I, E0_A, E0_J, S_EIG)
               + R_EIG * eigenval_on(E1_I, E1_A, E1_J, S_EIG)
               + S_EIG * eigenval_on(E2_I, E2_A, E2_J, S_EIG))
        assert val == S_EIG


# ── Group 5: GUT encoding ─────────────────────────────────────────────────────

class TestGUTEncoding:
    def test_rank_E1_equals_SU5_adj(self):
        assert rank_E1() == SU5_ADJ

    def test_rank_E2_equals_SU5_matter_per_gen(self):
        assert rank_E2() == SU5_MATTER_PER_GEN

    def test_rank_E2_equals_GUT_DIM_minus_K(self):
        assert rank_E2() == GUT_DIM - K

    def test_three_gens_times_rank_E2(self):
        assert GENERATIONS * rank_E2() == SU5_TOTAL_MATTER

    def test_rank_E1_plus_rank_E2_equals_V_minus_1(self):
        assert rank_E1() + rank_E2() == V - 1

    def test_rank_E2_is_5_plus_10(self):
        # SU(5) matter: 5-bar (5 components) + 10-dimensional antisymmetric
        assert SU5_MATTER_PER_GEN == 5 + 10

    def test_SU5_adj_equals_8_plus_3_plus_1_plus_12(self):
        # 8 gluons + 3 W/Z + 1 photon + 12 X/Y leptoquarks = 24
        assert SU5_ADJ == 8 + 3 + 1 + 12


# ── Group 6: Completeness identities ─────────────────────────────────────────

class TestCompletenessIdentities:
    def test_I_coeff_sum_equals_1(self):
        assert E0_I + E1_I + E2_I == Fraction(1)

    def test_A_coeff_sum_equals_0(self):
        assert E0_A + E1_A + E2_A == Fraction(0)

    def test_J_coeff_sum_equals_0(self):
        assert E0_J + E1_J + E2_J == Fraction(0)

    def test_J_coeff_sum_explicit(self):
        # 1/40 - 1/15 + 1/24 = 3/120 - 8/120 + 5/120 = 0
        assert Fraction(1, 40) - Fraction(1, 15) + Fraction(1, 24) == 0

    def test_non_trivial_I_span(self):
        assert E1_I + E2_I == Fraction(1)

    def test_A_antisymmetry(self):
        assert E1_A + E2_A == Fraction(0)

    def test_E1_A_coeff_equals_one_sixth(self):
        assert E1_A == Fraction(1, 6)

    def test_E2_A_coeff_equals_neg_one_sixth(self):
        assert E2_A == Fraction(-1, 6)


# ── Group 7: verify_all and summary ──────────────────────────────────────────

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
        assert summary["part"] == "CCCXLIV"

    def test_summary_has_fields(self, summary):
        assert "fields" in summary

    def test_summary_completeness_field(self, summary):
        assert summary["fields"]["completeness"] == V

    def test_summary_has_discoveries(self, summary):
        assert len(summary["discoveries"]) >= 5

    def test_json_output_exists(self):
        out = Path(__file__).resolve().parents[1] / "PART_CCCXLIV_gut_projector_results.json"
        assert out.exists()

    def test_json_output_valid(self):
        out = Path(__file__).resolve().parents[1] / "PART_CCCXLIV_gut_projector_results.json"
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["status"] == "PASS"
        assert data["checks_pass"] == 27
        assert data["fields"]["rank_E1"] == 24
        assert data["fields"]["rank_E2"] == 15
