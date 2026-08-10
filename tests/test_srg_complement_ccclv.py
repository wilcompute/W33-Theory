"""
Tests for PART CCCLV: Strongly Regular Complement of W(3,3).
91 tests across 8 classes.
"""

import json
import pathlib
import pytest
from fractions import Fraction

import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "exploration"))
from PART_CCCLV_SRG_COMPLEMENT_BRIDGE import (
    V, K, LAM, MU, EDGES, MULT_R, MULT_S, L,
    R_EIG, S_EIG, ABS_S,
    ALPHA, GUT_DIM, GENERATIONS, EW_GAUGE_4, SU5_ADJ, SU5_MATTER,
    kc, lamc, muc, edges_c, mult_rc, mult_sc,
    rc, sc, trace_complement, spectral_sum_sq_c,
    verify_all, build_ccclv_summary,
)

JSON_PATH = pathlib.Path(__file__).resolve().parents[1] / "PART_CCCLV_srg_complement_results.json"


# ── Class 1: SRG Constants ─────────────────────────────────────────────────

class TestSRGConstants:
    def test_V(self):          assert V == 40
    def test_K(self):          assert K == 12
    def test_LAM(self):        assert LAM == 2
    def test_MU(self):         assert MU == 4
    def test_EDGES(self):      assert EDGES == 240
    def test_MULT_R(self):     assert MULT_R == 24
    def test_MULT_S(self):     assert MULT_S == 15
    def test_L(self):          assert L == 27
    def test_R_EIG(self):      assert R_EIG == 2
    def test_S_EIG(self):      assert S_EIG == -4
    def test_GUT_DIM(self):    assert GUT_DIM == 27
    def test_GENERATIONS(self): assert GENERATIONS == 3
    def test_SU5_ADJ(self):    assert SU5_ADJ == 24
    def test_SU5_MATTER(self): assert SU5_MATTER == 15
    def test_ALPHA(self):      assert ALPHA == 10
    def test_total_edges(self): assert V * (V - 1) // 2 == EDGES + 540
    def test_V_minus_1(self):  assert V - 1 == K + kc()
    def test_V_k_lam_mu(self): assert V - 2 - 2 * K + MU == 18


# ── Class 2: Complement Parameters ────────────────────────────────────────

class TestComplementParameters:
    def test_kc_value(self):       assert kc() == 27
    def test_kc_eq_gut_dim(self):  assert kc() == GUT_DIM
    def test_kc_eq_L(self):        assert kc() == L
    def test_lamc_value(self):     assert lamc() == 18
    def test_muc_value(self):      assert muc() == 18
    def test_lamc_eq_muc(self):    assert lamc() == muc()
    def test_edges_c_value(self):  assert edges_c() == 540
    def test_edges_c_formula(self): assert edges_c() == V * (V - 1) // 2 - EDGES
    def test_edges_c_k_formula(self): assert edges_c() == V * kc() // 2
    def test_mult_rc_value(self):  assert mult_rc() == 15
    def test_mult_sc_value(self):  assert mult_sc() == 24
    def test_mult_rc_eq_mult_s(self): assert mult_rc() == MULT_S
    def test_mult_sc_eq_mult_r(self): assert mult_sc() == MULT_R
    def test_lamc_is_twice_gen_sq(self): assert lamc() == 2 * GENERATIONS ** 2
    def test_kc_minus_k(self):     assert kc() - K == MULT_S


# ── Class 3: Complement Eigenvalues ───────────────────────────────────────

class TestComplementEigenvalues:
    def test_rc_value(self):       assert rc() == 3
    def test_sc_value(self):       assert sc() == -3
    def test_rc_eq_generations(self): assert rc() == GENERATIONS
    def test_sc_eq_neg_generations(self): assert sc() == -GENERATIONS
    def test_rc_positive(self):    assert rc() > 0
    def test_sc_negative(self):    assert sc() < 0
    def test_rc_formula(self):     assert rc() == -1 - S_EIG
    def test_sc_formula(self):     assert sc() == -1 - R_EIG
    def test_eigenvalue_sum(self): assert rc() + sc() == 0
    def test_eigenvalue_product(self): assert rc() * sc() == -(GENERATIONS ** 2)
    def test_abs_sum(self):        assert abs(rc()) + abs(sc()) == 2 * GENERATIONS
    def test_rc_sq(self):          assert rc() ** 2 == GENERATIONS ** 2
    def test_sc_sq(self):          assert sc() ** 2 == GENERATIONS ** 2


# ── Class 4: Spectral Properties ──────────────────────────────────────────

class TestSpectralProperties:
    def test_trace_zero(self):     assert trace_complement() == 0
    def test_trace_formula(self):
        assert trace_complement() == kc() + mult_rc() * rc() + mult_sc() * sc()
    def test_spectral_sum_sq(self): assert spectral_sum_sq_c() == V * kc()
    def test_spectral_sum_sq_value(self): assert spectral_sum_sq_c() == 1080
    def test_spectral_sum_sq_eq_2edges(self): assert spectral_sum_sq_c() == 2 * edges_c()
    def test_kc_sq(self):          assert kc() ** 2 == 729
    def test_rc_sq_contrib(self):  assert mult_rc() * rc() ** 2 == 135
    def test_sc_sq_contrib(self):  assert mult_sc() * sc() ** 2 == 216
    def test_mult_sum(self):       assert 1 + mult_rc() + mult_sc() == V


# ── Class 5: Parameter Relations G <-> Complement ─────────────────────────

class TestParameterRelations:
    def test_k_plus_kc(self):      assert K + kc() == V - 1
    def test_k_times_kc(self):     assert K * kc() == lamc() ** 2
    def test_k_times_kc_value(self): assert K * kc() == 324
    def test_lamc_sq_value(self):  assert lamc() ** 2 == 324
    def test_eigenvalue_relation_rc(self): assert rc() == -1 - S_EIG
    def test_eigenvalue_relation_sc(self): assert sc() == -1 - R_EIG
    def test_mult_swap_r(self):    assert mult_rc() == MULT_S
    def test_mult_swap_s(self):    assert mult_sc() == MULT_R
    def test_rc_times_sc(self):    assert rc() * sc() == -9
    def test_rc_plus_sc(self):     assert rc() + sc() == 0
    def test_total_mult(self):     assert mult_rc() + mult_sc() == V - 1
    def test_lamc_ratio(self):
        assert Fraction(lamc(), kc()) == Fraction(2, 3)


# ── Class 6: Combinatorial Arithmetic ─────────────────────────────────────

class TestCombinatorial:
    def test_kc_minus_k_eq_mult_s(self):  assert kc() - K == MULT_S
    def test_kc_minus_k_value(self):      assert kc() - K == 15
    def test_edges_complement(self):      assert edges_c() == 540
    def test_total_edges_sum(self):       assert EDGES + edges_c() == V * (V - 1) // 2
    def test_kc_is_27(self):              assert kc() == 27
    def test_lamc_even(self):             assert lamc() % 2 == 0
    def test_muc_even(self):              assert muc() % 2 == 0
    def test_kc_divides_V_times_kc(self): assert (V * kc()) % 2 == 0
    def test_kc_equals_L(self):           assert kc() == L
    def test_lamc_gt_lam(self):           assert lamc() > LAM
    def test_muc_gt_mu(self):             assert muc() > MU
    def test_kc_gt_k(self):               assert kc() > K


# ── Class 7: Physics Connections ──────────────────────────────────────────

class TestPhysicsConnections:
    def test_kc_eq_gut_dim(self):          assert kc() == GUT_DIM
    def test_rc_eq_generations(self):      assert rc() == GENERATIONS
    def test_mult_rc_eq_su5_matter(self):  assert mult_rc() == SU5_MATTER
    def test_mult_sc_eq_su5_adj(self):     assert mult_sc() == SU5_ADJ
    def test_lamc_eq_2_gen_sq(self):       assert lamc() == 2 * GENERATIONS ** 2
    def test_muc_eq_2_gen_sq(self):        assert muc() == 2 * GENERATIONS ** 2
    def test_kc_eq_l_gut(self):            assert kc() == L == GUT_DIM
    def test_sc_negative_generations(self): assert sc() == -GENERATIONS
    def test_abs_rc_eq_generations(self):  assert abs(rc()) == GENERATIONS
    def test_edges_c_div_kc(self):         assert edges_c() // kc() == V // 2
    def test_kc_div_generations(self):     assert kc() % GENERATIONS == 0
    def test_mult_rc_plus_mult_sc(self):   assert mult_rc() + mult_sc() == MULT_R + MULT_S


# ── Class 8: VerifyAll and Summary ────────────────────────────────────────

class TestVerifyAllAndSummary:
    def test_verify_returns_tuple(self):
        result = verify_all()
        assert isinstance(result, tuple) and len(result) == 3

    def test_exactly_27_checks(self):
        _, _, total = verify_all()
        assert total == 27

    def test_all_27_pass(self):
        _, passed, total = verify_all()
        assert passed == total == 27

    def test_no_failed_check(self):
        checks, _, _ = verify_all()
        failed = [c["label"] for c in checks if not c["pass"]]
        assert failed == []

    def test_summary_part(self):
        s = build_ccclv_summary()
        assert s["part"] == "CCCLV"

    def test_summary_status_pass(self):
        s = build_ccclv_summary()
        assert s["status"] == "PASS"

    def test_summary_checks_pass_27(self):
        s = build_ccclv_summary()
        assert s["checks_pass"] == 27

    def test_summary_checks_total_27(self):
        s = build_ccclv_summary()
        assert s["checks_total"] == 27

    def test_summary_fields_kc(self):
        s = build_ccclv_summary()
        assert s["fields"]["K_c"] == 27

    def test_summary_fields_lamc(self):
        s = build_ccclv_summary()
        assert s["fields"]["LAM_c"] == 18

    def test_summary_fields_rc(self):
        s = build_ccclv_summary()
        assert s["fields"]["r_c"] == 3

    def test_summary_fields_sc(self):
        s = build_ccclv_summary()
        assert s["fields"]["s_c"] == -3

    def test_summary_discoveries_nonempty(self):
        s = build_ccclv_summary()
        assert len(s["discoveries"]) >= 1

    def test_json_exists(self):
        assert JSON_PATH.exists()

    def test_json_status_pass(self):
        data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        assert data["status"] == "PASS"

    def test_json_checks_pass_27(self):
        data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        assert data["checks_pass"] == 27
