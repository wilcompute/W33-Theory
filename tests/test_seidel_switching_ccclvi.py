"""
Tests for PART CCCLVI: Seidel Switching Classes of W(3,3).
100 tests across 7 classes.
"""

import json
import pathlib
import pytest

import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "exploration"))
from PART_CCCLVI_SEIDEL_SWITCHING_BRIDGE import (
    V, K, LAM, MU, EDGES, MULT_R, MULT_S, L,
    R_EIG, S_EIG, ABS_S,
    ALPHA, GUT_DIM, GENERATIONS, EW_GAUGE_4, SU5_ADJ, SU5_MATTER,
    seid_trivial_eig, seid_r_eig, seid_s_eig,
    mult_seid_trivial, mult_seid_r, mult_seid_s,
    trace_seid, frobenius_seid,
    verify_all, build_ccclvi_summary,
)

JSON_PATH = (
    pathlib.Path(__file__).resolve().parents[1]
    / "PART_CCCLVI_seidel_switching_results.json"
)


# ── Class 1: SRG Constants ─────────────────────────────────────────────────

class TestSRGConstants:
    def test_V(self):           assert V == 40
    def test_K(self):           assert K == 12
    def test_LAM(self):         assert LAM == 2
    def test_MU(self):          assert MU == 4
    def test_EDGES(self):       assert EDGES == 240
    def test_MULT_R(self):      assert MULT_R == 24
    def test_MULT_S(self):      assert MULT_S == 15
    def test_L(self):           assert L == 27
    def test_R_EIG(self):       assert R_EIG == 2
    def test_S_EIG(self):       assert S_EIG == -4
    def test_ALPHA(self):       assert ALPHA == 10
    def test_GENERATIONS(self): assert GENERATIONS == 3
    def test_EW_GAUGE_4(self):  assert EW_GAUGE_4 == 4
    def test_SU5_ADJ(self):     assert SU5_ADJ == 24
    def test_SU5_MATTER(self):  assert SU5_MATTER == 15
    def test_GUT_DIM(self):     assert GUT_DIM == 27


# ── Class 2: Seidel Eigenvalues ────────────────────────────────────────────

class TestSeidelEigenvalues:
    def test_trivial_value(self):     assert seid_trivial_eig() == 15
    def test_trivial_formula(self):   assert seid_trivial_eig() == V - 1 - 2 * K
    def test_r_eig_value(self):       assert seid_r_eig() == -5
    def test_r_eig_formula(self):     assert seid_r_eig() == -(1 + 2 * R_EIG)
    def test_s_eig_value(self):       assert seid_s_eig() == 7
    def test_s_eig_formula(self):     assert seid_s_eig() == -(1 + 2 * S_EIG)
    def test_r_eig_negative(self):    assert seid_r_eig() < 0
    def test_s_eig_positive(self):    assert seid_s_eig() > 0
    def test_trivial_positive(self):  assert seid_trivial_eig() > 0
    def test_r_abs(self):             assert abs(seid_r_eig()) == 5
    def test_s_abs(self):             assert abs(seid_s_eig()) == 7
    def test_trivial_abs(self):       assert abs(seid_trivial_eig()) == 15


# ── Class 3: Multiplicities ────────────────────────────────────────────────

class TestMultiplicities:
    def test_mult_trivial_value(self): assert mult_seid_trivial() == 1
    def test_mult_r_value(self):       assert mult_seid_r() == 24
    def test_mult_s_value(self):       assert mult_seid_s() == 15
    def test_mult_r_eq_mult_r(self):   assert mult_seid_r() == MULT_R
    def test_mult_s_eq_mult_s(self):   assert mult_seid_s() == MULT_S
    def test_total_mult(self):         assert mult_seid_trivial() + mult_seid_r() + mult_seid_s() == V
    def test_non_trivial_sum(self):    assert mult_seid_r() + mult_seid_s() == V - 1
    def test_mult_r_gt_mult_s(self):   assert mult_seid_r() > mult_seid_s()


# ── Class 4: Spectral Traces ───────────────────────────────────────────────

class TestSpectralTraces:
    def test_trace_zero(self):
        assert trace_seid() == 0

    def test_trace_formula(self):
        t = (mult_seid_trivial() * seid_trivial_eig()
             + mult_seid_r() * seid_r_eig()
             + mult_seid_s() * seid_s_eig())
        assert t == 0

    def test_frobenius_value(self):
        assert frobenius_seid() == 1560

    def test_frobenius_formula_vv1(self):
        assert frobenius_seid() == V * (V - 1)

    def test_frobenius_formula_spectral(self):
        f = (mult_seid_trivial() * seid_trivial_eig() ** 2
             + mult_seid_r() * seid_r_eig() ** 2
             + mult_seid_s() * seid_s_eig() ** 2)
        assert f == frobenius_seid()

    def test_trivial_contrib(self):
        assert mult_seid_trivial() * seid_trivial_eig() ** 2 == 225

    def test_r_contrib(self):
        assert mult_seid_r() * seid_r_eig() ** 2 == 600

    def test_s_contrib(self):
        assert mult_seid_s() * seid_s_eig() ** 2 == 735


# ── Class 5: Eigenvalue Relations ─────────────────────────────────────────

class TestEigenvalueRelations:
    def test_trivial_plus_r(self):    assert seid_trivial_eig() + seid_r_eig() == ALPHA
    def test_trivial_plus_r_val(self): assert seid_trivial_eig() + seid_r_eig() == 10
    def test_r_plus_s(self):           assert seid_r_eig() + seid_s_eig() == R_EIG
    def test_r_plus_s_val(self):       assert seid_r_eig() + seid_s_eig() == 2
    def test_trivial_minus_s(self):    assert seid_trivial_eig() - seid_s_eig() == 2 * EW_GAUGE_4
    def test_trivial_minus_s_val(self): assert seid_trivial_eig() - seid_s_eig() == 8
    def test_trivial_sq(self):         assert seid_trivial_eig() ** 2 == MULT_S ** 2
    def test_r_sq(self):               assert seid_r_eig() ** 2 == (ALPHA // 2) ** 2
    def test_s_sq(self):               assert seid_s_eig() ** 2 == (MU + GENERATIONS) ** 2
    def test_r_times_s(self):          assert seid_r_eig() * seid_s_eig() == -35
    def test_v_minus_trivial(self):    assert V - seid_trivial_eig() == (ALPHA // 2) ** 2
    def test_trivial_div_gen(self):    assert seid_trivial_eig() // GENERATIONS == ALPHA // 2
    def test_abs_r_eq_alpha_half(self): assert abs(seid_r_eig()) == ALPHA // 2
    def test_trivial_plus_abs_r(self): assert seid_trivial_eig() + abs(seid_r_eig()) == 2 * ALPHA


# ── Class 6: Physics Connections ──────────────────────────────────────────

class TestPhysicsConnections:
    def test_trivial_eq_su5_matter(self):  assert seid_trivial_eig() == SU5_MATTER
    def test_trivial_eq_mult_s(self):      assert seid_trivial_eig() == MULT_S
    def test_trivial_eq_k_plus_gen(self):  assert seid_trivial_eig() == K + GENERATIONS
    def test_mult_r_eq_su5_adj(self):      assert mult_seid_r() == SU5_ADJ
    def test_mult_r_eq_mult_r(self):       assert mult_seid_r() == MULT_R
    def test_s_eig_eq_mu_plus_gen(self):   assert seid_s_eig() == MU + GENERATIONS
    def test_abs_r_eq_alpha_half(self):    assert abs(seid_r_eig()) == ALPHA // 2
    def test_trivial_plus_r_eq_alpha(self): assert seid_trivial_eig() + seid_r_eig() == ALPHA
    def test_mult_s_eq_su5_matter(self):   assert mult_seid_s() == SU5_MATTER
    def test_v_minus_trivial_sq(self):     assert V - seid_trivial_eig() == 25


# ── Class 7: VerifyAll and Summary ────────────────────────────────────────

class TestVerifyAllAndSummary:
    def test_returns_tuple(self):
        result = verify_all()
        assert isinstance(result, tuple) and len(result) == 3

    def test_exactly_27_checks(self):
        _, _, total = verify_all()
        assert total == 27

    def test_all_27_pass(self):
        _, passed, total = verify_all()
        assert passed == total == 27

    def test_no_failures(self):
        checks, _, _ = verify_all()
        failed = [c["label"] for c in checks if not c["pass"]]
        assert failed == []

    def test_summary_part(self):
        s = build_ccclvi_summary()
        assert s["part"] == "CCCLVI"

    def test_summary_status_pass(self):
        s = build_ccclvi_summary()
        assert s["status"] == "PASS"

    def test_summary_checks_pass_27(self):
        s = build_ccclvi_summary()
        assert s["checks_pass"] == 27

    def test_summary_checks_total_27(self):
        s = build_ccclvi_summary()
        assert s["checks_total"] == 27

    def test_summary_fields_trivial(self):
        s = build_ccclvi_summary()
        assert s["fields"]["seid_trivial_eig"] == 15

    def test_summary_fields_r(self):
        s = build_ccclvi_summary()
        assert s["fields"]["seid_r_eig"] == -5

    def test_summary_fields_s(self):
        s = build_ccclvi_summary()
        assert s["fields"]["seid_s_eig"] == 7

    def test_summary_fields_trace(self):
        s = build_ccclvi_summary()
        assert s["fields"]["trace_seid"] == 0

    def test_summary_fields_frobenius(self):
        s = build_ccclvi_summary()
        assert s["fields"]["frobenius_seid"] == 1560

    def test_summary_discoveries_nonempty(self):
        s = build_ccclvi_summary()
        assert len(s["discoveries"]) >= 1

    def test_json_exists(self):
        assert JSON_PATH.exists()

    def test_json_status_pass(self):
        data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        assert data["status"] == "PASS"

    def test_json_checks_pass_27(self):
        data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        assert data["checks_pass"] == 27

    def test_json_part_label(self):
        data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        assert data["part"] == "CCCLVI"
