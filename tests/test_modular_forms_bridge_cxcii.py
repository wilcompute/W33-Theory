"""
tests/test_modular_forms_bridge_cxcii.py

Regression tests for Part CXCII: Modular Forms (Ramanujan) Bridge.
"""

import pytest

from PART_CXCII_MODULAR_FORMS_BRIDGE import (
    Q, LAM, V, K, PHI3, PHI4, PHI6, PHI12, J_INV, ALPHA_INV, VIETA2,
    EDGES, MULTIPLICITIES, EIGENVALUES,
    WEIGHT_DELTA, ETA_EXPONENT, J_AT_I, J_CONSTANT_TERM,
    TAU_AT_2, TAU_AT_3, TAU_AT_6, BOSONIC_STRING,
    is_prime, nth_prime, sigma3, compute_tau,
    ModularCheck, modular_forms_bridge_audit,
)


# ─── Atom constants ──────────────────────────────────────────────────────────

class TestAtoms:
    def test_Q(self):    assert Q == 3
    def test_V(self):    assert V == 40
    def test_K(self):    assert K == 12
    def test_PHI3(self): assert PHI3 == 13
    def test_PHI6(self): assert PHI6 == 7
    def test_J_INV(self): assert J_INV == 8
    def test_EDGES(self): assert EDGES == 240


# ─── Modular forms constants ─────────────────────────────────────────────────

class TestModularFormsConstants:
    def test_weight_delta_is_K(self):     assert WEIGHT_DELTA == K
    def test_weight_delta_value(self):    assert WEIGHT_DELTA == 12
    def test_eta_exponent_is_2K(self):    assert ETA_EXPONENT == 2 * K
    def test_eta_exponent_value(self):    assert ETA_EXPONENT == 24
    def test_j_at_i_is_K3(self):          assert J_AT_I == K ** 3
    def test_j_at_i_value(self):          assert J_AT_I == 1728
    def test_j_constant_term_value(self): assert J_CONSTANT_TERM == 744
    def test_bosonic_string_is_2Phi3(self): assert BOSONIC_STRING == 2 * PHI3
    def test_bosonic_string_value(self):    assert BOSONIC_STRING == 26
    def test_tau_at_2_is_minus_2K(self):  assert TAU_AT_2 == -2 * K
    def test_tau_at_2_value(self):        assert TAU_AT_2 == -24
    def test_tau_at_3_is_QKPhi6(self):    assert TAU_AT_3 == Q * K * PHI6
    def test_tau_at_3_value(self):        assert TAU_AT_3 == 252
    def test_tau_at_6_is_tau2_times_tau3(self): assert TAU_AT_6 == TAU_AT_2 * TAU_AT_3
    def test_tau_at_6_value(self):        assert TAU_AT_6 == -6048


# ─── is_prime ─────────────────────────────────────────────────────────────────

class TestIsPrime:
    def test_1_not_prime(self):  assert not is_prime(1)
    def test_2_prime(self):      assert is_prime(2)
    def test_3_prime(self):      assert is_prime(3)
    def test_4_not_prime(self):  assert not is_prime(4)
    def test_11_prime(self):     assert is_prime(11)
    def test_31_prime(self):     assert is_prime(31)
    def test_137_prime(self):    assert is_prime(ALPHA_INV)


# ─── nth_prime ────────────────────────────────────────────────────────────────

class TestNthPrime:
    def test_prime_1(self):   assert nth_prime(1) == 2
    def test_prime_2(self):   assert nth_prime(2) == 3
    def test_prime_3(self):   assert nth_prime(3) == 5
    def test_prime_11(self):  assert nth_prime(11) == 31
    def test_prime_K_minus_1(self): assert nth_prime(K - 1) == 31
    def test_j_const_formula(self):
        # 744 = prime(K-1) * 2K = 31 * 24
        assert nth_prime(K - 1) * (2 * K) == J_CONSTANT_TERM


# ─── sigma3 ───────────────────────────────────────────────────────────────────

class TestSigma3:
    def test_sigma3_1(self):   assert sigma3(1) == 1
    def test_sigma3_2(self):   assert sigma3(2) == 9
    def test_sigma3_3(self):   assert sigma3(3) == 28
    def test_sigma3_2_is_Q2(self):      assert sigma3(2) == Q ** 2
    def test_sigma3_3_is_V_minus_K(self): assert sigma3(3) == V - K


# ─── compute_tau ─────────────────────────────────────────────────────────────

class TestComputeTau:
    @pytest.fixture(scope="class")
    def tau(self):
        return compute_tau(13)

    def test_tau_1(self, tau):   assert tau[1] == 1
    def test_tau_2(self, tau):   assert tau[2] == -24
    def test_tau_3(self, tau):   assert tau[3] == 252
    def test_tau_4(self, tau):   assert tau[4] == -1472
    def test_tau_5(self, tau):   assert tau[5] == 4830
    def test_tau_6(self, tau):   assert tau[6] == -6048
    def test_tau_7(self, tau):   assert tau[7] == -16744
    def test_tau_8(self, tau):   assert tau[8] == 84480

    def test_tau_2_minus_2K(self, tau):   assert tau[2] == -2 * K
    def test_tau_3_Q_K_Phi6(self, tau):   assert tau[3] == Q * K * PHI6
    def test_tau_6_multiplicative(self, tau):
        assert tau[6] == tau[2] * tau[3]

    def test_ramanujan_conjecture_p2(self, tau):
        assert abs(tau[2]) <= 2 * (2 ** 5.5)

    def test_ramanujan_conjecture_p3(self, tau):
        assert abs(tau[3]) <= 2 * (3 ** 5.5)

    def test_ramanujan_conjecture_p5(self, tau):
        assert abs(tau[5]) <= 2 * (5 ** 5.5)

    def test_ramanujan_conjecture_p7(self, tau):
        assert abs(tau[7]) <= 2 * (7 ** 5.5)

    def test_ramanujan_conjecture_p11(self, tau):
        assert abs(tau[11]) <= 2 * (11 ** 5.5)


# ─── ModularCheck dataclass ───────────────────────────────────────────────────

class TestModularCheck:
    def test_passes_exact(self):
        c = ModularCheck("t", "d", 42, 42)
        assert c.passes
    def test_fails_exact(self):
        c = ModularCheck("t", "d", 42, 43)
        assert not c.passes
    def test_passes_inexact(self):
        c = ModularCheck("t", "d", 1.000000000001, 1.0, exact=False)
        assert c.passes
    def test_fails_inexact(self):
        c = ModularCheck("t", "d", 1.5, 1.0, exact=False)
        assert not c.passes


# ─── E8 theta series ─────────────────────────────────────────────────────────

class TestE8Theta:
    def test_norm2_is_240(self):      assert 240 * sigma3(1) == 240
    def test_norm2_is_EDGES(self):    assert 240 * sigma3(1) == EDGES
    def test_norm4_is_2160(self):     assert 240 * sigma3(2) == 2160
    def test_norm4_formula(self):     assert 240 * sigma3(2) == EDGES * Q ** 2
    def test_norm6_formula(self):     assert 240 * sigma3(3) == EDGES * (V - K)


# ─── Full audit ───────────────────────────────────────────────────────────────

class TestModularFormsBridgeAudit:
    @pytest.fixture(scope="class")
    def result(self):
        return modular_forms_bridge_audit()

    def test_status_pass(self, result):
        assert result["status"] == "PASS"

    def test_all_checks_pass(self, result):
        assert result["all_checks_pass"]

    def test_no_failed_checks(self, result):
        assert result["failed_checks"] == []

    def test_check_count(self, result):
        assert result["check_count"] == 33

    def test_checks_passing(self, result):
        assert result["checks_passing"] == 33

    def test_tau_2_in_result(self, result):
        assert result["ramanujan_tau"][2] == -24

    def test_tau_3_in_result(self, result):
        assert result["ramanujan_tau"][3] == 252

    def test_j_at_i_in_result(self, result):
        assert result["j_invariant"]["j_at_i"] == 1728

    def test_j_at_i_is_K3(self, result):
        assert result["j_invariant"]["j_at_i_is_K3"]

    def test_j_constant_in_result(self, result):
        assert result["j_invariant"]["constant_term"] == 744

    def test_weight_delta_in_result(self, result):
        assert result["modular_forms_structure"]["weight_delta"] == 12

    def test_eta_exponent_in_result(self, result):
        assert result["modular_forms_structure"]["eta_exponent"] == 24

    def test_tau_3_formula_in_result(self, result):
        assert "Q*K*Phi6" in result["modular_forms_structure"]["tau_3_formula"]

    def test_theorem_string_present(self, result):
        assert "theorem_cxcii" in result
        assert len(result["theorem_cxcii"]) > 50
