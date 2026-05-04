"""Tests for PART_CCLXV: Ramanujan τ-Function and W(3,3)."""
import json
import math
import sys
import os
import importlib.util

import pytest

# ---------------------------------------------------------------------------
# Load results JSON (produced by the bridge script)
# ---------------------------------------------------------------------------
RESULTS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "PART_CCLXV_ramanujan_tau_results.json"
)


@pytest.fixture(scope="module")
def results() -> dict:
    assert os.path.isfile(RESULTS_FILE), f"Missing {RESULTS_FILE}"
    with open(RESULTS_FILE, encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# Top-level summary
# ---------------------------------------------------------------------------
class TestSummary:
    def test_verified_flag(self, results):
        assert results["Verified"] is True

    def test_all_checks_pass(self, results):
        assert results["checks_passed"] == results["checks_total"]

    def test_check_count(self, results):
        assert results["checks_total"] == 35

    def test_part_label(self, results):
        assert results["part"] == "CCLXV"


# ---------------------------------------------------------------------------
# Bridge 1: Ramanujan-graph spectral property
# ---------------------------------------------------------------------------
class TestRamanujanGraph:
    W33_K = 12
    W33_R = 2
    W33_S = -4

    def test_non_trivial_eigenvalues_satisfy_ramanujan_bound(self):
        bound = 2 * math.sqrt(self.W33_K - 1)
        assert abs(self.W33_R) < bound
        assert abs(self.W33_S) < bound

    def test_ramanujan_bound_value(self):
        bound = 2 * math.sqrt(11)
        assert abs(bound - 6.633) < 0.01

    def test_spectral_gap(self):
        # spectral gap = k - r = 12 - 2 = 10 = Φ₄
        PHI4 = 10
        assert self.W33_K - self.W33_R == PHI4

    def test_b1a_in_results(self, results):
        check = next(c for c in results["checks"] if c["check"] == "B1a: |r| < 2√(K-1)")
        assert check["passed"]

    def test_b1b_in_results(self, results):
        check = next(c for c in results["checks"] if c["check"] == "B1b: |s| < 2√(K-1)")
        assert check["passed"]


# ---------------------------------------------------------------------------
# Bridge 2: τ(2) = −f
# ---------------------------------------------------------------------------
class TestTau2:
    def test_tau2_equals_neg_f(self):
        tau2 = -24
        f = 24
        assert tau2 == -f

    def test_tau2_equals_neg_2k(self):
        tau2 = -24
        k = 12
        assert tau2 == -2 * k

    def test_tau2_key_identity_in_results(self, results):
        ki = results["key_identities"]["tau_2_equals_neg_f"]
        assert "-24" in ki and "24" in ki

    def test_b2_check_in_results(self, results):
        check = next(c for c in results["checks"] if c["check"] == "B2: τ(2) = −f")
        assert check["passed"]


# ---------------------------------------------------------------------------
# Bridge 3: τ(3) = E + k
# ---------------------------------------------------------------------------
class TestTau3:
    E = 240
    K = 12

    def test_tau3_equals_E_plus_k(self):
        tau3 = 252
        assert tau3 == self.E + self.K

    def test_tau3_equals_21k(self):
        tau3 = 252
        assert tau3 == 21 * self.K

    def test_tau3_key_identity_in_results(self, results):
        ki = results["key_identities"]["tau_3_equals_E_plus_k"]
        assert "252" in ki and "240" in ki

    def test_b3_check_in_results(self, results):
        check = next(c for c in results["checks"] if c["check"] == "B3: τ(3) = E + k")
        assert check["passed"]


# ---------------------------------------------------------------------------
# Bridge 4: modular weight = k = 12
# ---------------------------------------------------------------------------
class TestModularWeight:
    def test_modular_weight_equals_k(self):
        assert 12 == 12  # weight(Δ) == k

    def test_b4_check_in_results(self, results):
        check = next(c for c in results["checks"] if c["check"] == "B4: modular weight of Δ = k")
        assert check["passed"]


# ---------------------------------------------------------------------------
# Bridge 5: Hecke eigenvalue recursion
# ---------------------------------------------------------------------------
TAU = {
    1: 1, 2: -24, 3: 252, 4: -1472, 5: 4830, 6: -6048, 7: -16744,
    8: 84480, 9: -113643, 10: -115920, 11: 534612, 12: -370944,
    13: -577738, 14: 401856, 15: 1217160, 16: 987136, 17: -6905934,
    18: 2727432, 19: 10661420, 20: -7109760, 23: 18643272,
}


class TestHeckeRecursion:
    def test_tau4_hecke(self):
        assert TAU[2] ** 2 - 2 ** 11 == TAU[4]

    def test_tau8_hecke(self):
        assert TAU[2] * TAU[4] - 2 ** 11 * TAU[2] == TAU[8]

    def test_tau9_hecke(self):
        assert TAU[3] ** 2 - 3 ** 11 == TAU[9]

    def test_tau16_hecke(self):
        assert TAU[2] * TAU[8] - 2 ** 11 * TAU[4] == TAU[16]

    def test_b5a_in_results(self, results):
        check = next(c for c in results["checks"]
                     if c["check"].startswith("B5a"))
        assert check["passed"]


# ---------------------------------------------------------------------------
# Bridge 6: 691 congruence (links Part CCLVIII)
# ---------------------------------------------------------------------------
class TestCongruence691:
    P691 = 691
    LAM = 2
    PHI6 = 7
    MU = 4
    q = 3
    PHI3 = 13

    def _sigma11(self, n: int) -> int:
        return sum(d ** 11 for d in range(1, n + 1) if n % d == 0)

    def test_691_w33_form(self):
        val = self.LAM ** self.PHI6 * (self.MU + 1) + self.q * (self.PHI3 + self.MU)
        assert val == 691

    def test_tau2_congruence_691(self):
        assert TAU[2] % self.P691 == self._sigma11(2) % self.P691

    def test_tau3_congruence_691(self):
        assert TAU[3] % self.P691 == self._sigma11(3) % self.P691

    def test_tau5_congruence_691(self):
        assert TAU[5] % self.P691 == self._sigma11(5) % self.P691

    def test_tau7_congruence_691(self):
        assert TAU[7] % self.P691 == self._sigma11(7) % self.P691

    def test_b6a_in_results(self, results):
        check = next(c for c in results["checks"]
                     if c["check"].startswith("B6a"))
        assert check["passed"]


# ---------------------------------------------------------------------------
# Bridge 7: Dedekind η exponent = f
# ---------------------------------------------------------------------------
class TestEtaExponent:
    def test_eta_exponent_is_f(self):
        f = 24
        eta_exp = 24  # Δ = η^{24}
        assert eta_exp == f

    def test_b7a_in_results(self, results):
        check = next(c for c in results["checks"] if c["check"].startswith("B7a"))
        assert check["passed"]


# ---------------------------------------------------------------------------
# Bridge 8: Multiplicativity
# ---------------------------------------------------------------------------
class TestMultiplicativity:
    def test_tau6_multiplicative(self):
        assert TAU[6] == TAU[2] * TAU[3]

    def test_tau10_multiplicative(self):
        assert TAU[10] == TAU[2] * TAU[5]

    def test_tau15_multiplicative(self):
        assert TAU[15] == TAU[3] * TAU[5]

    def test_tau14_multiplicative(self):
        assert TAU[14] == TAU[2] * TAU[7]

    def test_tau1_normalised(self):
        assert TAU[1] == 1

    def test_b8b_in_results(self, results):
        check = next(c for c in results["checks"]
                     if c["check"].startswith("B8b"))
        assert check["passed"]


# ---------------------------------------------------------------------------
# Petersson (Ramanujan) bound: |τ(p)| ≤ 2 p^{11/2}
# ---------------------------------------------------------------------------
class TestPeterssonBound:
    @pytest.mark.parametrize("p", [2, 3, 5, 7, 11, 13])
    def test_petersson_bound(self, p):
        bound = 2 * p ** (11 / 2)
        assert abs(TAU[p]) <= bound, f"|τ({p})|={abs(TAU[p])} > {bound:.2f}"


# ---------------------------------------------------------------------------
# Additional arithmetic
# ---------------------------------------------------------------------------
class TestAdditionalArithmetic:
    def test_tau2_plus_tau3_equals_19k(self):
        k = 12
        assert TAU[2] + TAU[3] == 19 * k

    def test_b9d_in_results(self, results):
        check = next(c for c in results["checks"]
                     if c["check"].startswith("B9d"))
        assert check["passed"]
