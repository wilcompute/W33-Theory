"""
Tests for PART CCC — Grand Synthesis: W(3,3) as Unique Combinatorial Backbone
of Standard Model Structure.
"""

import sys
import os
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from exploration.PART_CCC_GRAND_SYNTHESIS_BRIDGE import (
    V, K, K2, LAM, MU, EDGES,
    R_EIG, S_EIG, MULT_R, MULT_S,
    EW_GAUGE_4, ALPHA,
    GUT_DIM, GENERATIONS, CCC_PART,
    SPECTRAL_GAP, EDGE_DENSITY, GAUGE_PRODUCT, K2_CUBE_ROOT,
    EW_CUBE, MULT_SUM, PERIOD_300_FORMULA,
    GUT_SM_RATIO, KREIN_3Q2_11, KREIN_3Q2_22,
    E6_SPINOR, E6_CONJ, E6_TOTAL_SPINOR, E6_ADJOINT,
    COMPLEMENT_LAM, COMPLEMENT_MU,
    UNIQUENESS_PARAMETER_SET,
    verify_all, build_ccc_summary,
)


# ─────────────────────────────────────────────────────────────────────────────
class TestSRGConstants:
    """Baseline SRG parameters."""

    def test_V(self):
        assert V == 40

    def test_K(self):
        assert K == 12

    def test_K2(self):
        assert K2 == 27
        assert K2 == V - 1 - K

    def test_LAM(self):
        assert LAM == 2

    def test_MU(self):
        assert MU == 4

    def test_EDGES(self):
        assert EDGES == 240
        assert EDGES == V * K // 2

    def test_R_EIG(self):
        assert R_EIG == 2

    def test_S_EIG(self):
        assert S_EIG == -4

    def test_MULT_R(self):
        assert MULT_R == 24

    def test_MULT_S(self):
        assert MULT_S == 15

    def test_mult_sum(self):
        assert 1 + MULT_R + MULT_S == V


# ─────────────────────────────────────────────────────────────────────────────
class TestSMConstants:
    """SM / GUT constants."""

    def test_EW_GAUGE_4(self):
        assert EW_GAUGE_4 == 4

    def test_ALPHA(self):
        assert ALPHA == 10

    def test_GUT_DIM(self):
        assert GUT_DIM == 27
        assert GUT_DIM == K2

    def test_GENERATIONS(self):
        assert GENERATIONS == 3

    def test_CCC_PART(self):
        assert CCC_PART == 300


# ─────────────────────────────────────────────────────────────────────────────
class TestSpectralIdentities:
    """Spectral-gap and density identities."""

    def test_spectral_gap(self):
        assert SPECTRAL_GAP == 6
        assert SPECTRAL_GAP == R_EIG - S_EIG

    def test_edge_density(self):
        assert EDGE_DENSITY == Fraction(6)
        assert EDGE_DENSITY == Fraction(EDGES, V)

    def test_edge_density_equals_spectral_gap(self):
        assert EDGE_DENSITY == Fraction(SPECTRAL_GAP)

    def test_eigenvalue_product(self):
        assert R_EIG * S_EIG == MU - K   # = -8

    def test_eigenvalue_sum(self):
        assert R_EIG + S_EIG == LAM - MU  # = -2


# ─────────────────────────────────────────────────────────────────────────────
class TestE6GUTContent:
    """E6 matter-content encoding."""

    def test_gut_dim(self):
        assert GUT_DIM == 27

    def test_k2_cube(self):
        assert K2 == GENERATIONS ** 3    # 27 = 3^3

    def test_e6_spinor(self):
        assert E6_SPINOR == 27

    def test_e6_conj(self):
        assert E6_CONJ == 27

    def test_e6_total(self):
        assert E6_TOTAL_SPINOR == 54

    def test_e6_adjoint(self):
        assert E6_ADJOINT == 78

    def test_generations_times_gut(self):
        assert GENERATIONS * GUT_DIM == 81
        assert GENERATIONS * GUT_DIM == GENERATIONS ** 4   # 3^4


# ─────────────────────────────────────────────────────────────────────────────
class TestSMGaugeEncoding:
    """SM gauge-group encoding identities."""

    def test_gauge_product(self):
        assert GAUGE_PRODUCT == K            # EW*GENS = 12 = K
        assert GAUGE_PRODUCT == EW_GAUGE_4 * GENERATIONS

    def test_k2_cube_root(self):
        assert K2_CUBE_ROOT == GENERATIONS   # 3

    def test_ew_cube(self):
        assert EW_CUBE == 64
        assert EW_CUBE == EW_GAUGE_4 ** 3

    def test_ew_squared_equals_k_plus_mu(self):
        assert EW_GAUGE_4 ** 2 == K + MU    # 16 = 12 + 4

    def test_mult_s_equals_k_plus_generations(self):
        assert MULT_S == K + GENERATIONS    # 15 = 12 + 3


# ─────────────────────────────────────────────────────────────────────────────
class TestHoffmanKreinCoupling:
    """Hoffman bound and Krein coupling identities."""

    def test_alpha(self):
        assert ALPHA == 10

    def test_krein_3q2_22(self):
        assert KREIN_3Q2_22 == Fraction(ALPHA)

    def test_krein_3q2_11(self):
        assert KREIN_3Q2_11 == Fraction(V)


# ─────────────────────────────────────────────────────────────────────────────
class TestMultiplicityStructure:
    """Multiplicity encoding in SM."""

    def test_mult_sum_equals_v(self):
        assert MULT_SUM == V

    def test_mult_r_equals_v_minus_16(self):
        assert MULT_R == V - 16

    def test_mult_s_value(self):
        assert MULT_S == 15

    def test_mult_r_minus_mult_s_equals_9(self):
        assert MULT_R - MULT_S == GENERATIONS ** 2   # 9 = 3^2


# ─────────────────────────────────────────────────────────────────────────────
class TestCCCMilestone:
    """CCC = 300 milestone identities."""

    def test_ccc_value(self):
        assert CCC_PART == 300

    def test_period_formula(self):
        assert PERIOD_300_FORMULA == 300
        assert PERIOD_300_FORMULA == GENERATIONS * ALPHA * ALPHA

    def test_gut_sm_ratio(self):
        assert GUT_SM_RATIO == Fraction(9, 4)
        assert GUT_SM_RATIO == Fraction(K2, K)

    def test_complement_lam_mu(self):
        assert COMPLEMENT_LAM == 18
        assert COMPLEMENT_MU == 18
        assert COMPLEMENT_LAM == COMPLEMENT_MU

    def test_complement_conference_property(self):
        # A srg with λ = μ is called a conference graph
        assert COMPLEMENT_LAM == COMPLEMENT_MU


# ─────────────────────────────────────────────────────────────────────────────
class TestUniqueness:
    """Uniqueness parameter set."""

    def test_uniqueness_set(self):
        assert UNIQUENESS_PARAMETER_SET == (V, K, LAM, MU)
        assert UNIQUENESS_PARAMETER_SET == (40, 12, 2, 4)


# ─────────────────────────────────────────────────────────────────────────────
class TestVerifyAll:
    """verify_all() reports exactly 27/27."""

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

    def test_checks_all_ok(self):
        checks, _, _ = verify_all()
        for c in checks:
            assert c["ok"] is True

    def test_checks_have_name(self):
        checks, _, _ = verify_all()
        for c in checks:
            assert "name" in c
            assert isinstance(c["name"], str)


# ─────────────────────────────────────────────────────────────────────────────
class TestBuildSummary:
    """build_ccc_summary() structure and content."""

    def test_returns_dict(self):
        assert isinstance(build_ccc_summary(), dict)

    def test_part_key(self):
        assert build_ccc_summary()["part"] == "CCC"

    def test_title_contains_synthesis(self):
        assert "Synthesis" in build_ccc_summary()["title"] or "synthesis" in build_ccc_summary()["title"].lower()

    def test_checks_pass_27(self):
        assert build_ccc_summary()["checks_pass"] == 27

    def test_checks_total_27(self):
        assert build_ccc_summary()["checks_total"] == 27

    def test_status_pass(self):
        assert build_ccc_summary()["status"] == "PASS"

    def test_fields_present(self):
        fields = build_ccc_summary()["fields"]
        for key in ("V", "K", "K2", "MULT_R", "MULT_S", "ALPHA",
                    "GUT_DIM", "GENERATIONS", "CCC_PART", "SPECTRAL_GAP"):
            assert key in fields

    def test_ccc_part_in_fields(self):
        assert build_ccc_summary()["fields"]["CCC_PART"] == 300

    def test_discoveries_present(self):
        assert len(build_ccc_summary()["discoveries"]) >= 10

    def test_period_formula_in_fields(self):
        assert build_ccc_summary()["fields"]["PERIOD_300_FORMULA"] == 300
