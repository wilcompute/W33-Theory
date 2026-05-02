"""
Regression tests for Part CXC — Riemann-Zeta Bridge.

Covers:
  - Z(x) zeros and normalization
  - Frobenius eigenvalues and multiplicities
  - Vieta's symmetric polynomials
  - α⁻¹ = 137 is the 33rd prime (core theorem)
  - String / M / F theory dimensions as W(3,3) parameters
  - Leading coefficient of Z(x)
  - Full audit dict structure and status
"""

import math
import sys
import os

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import PART_CXC_RIEMANN_ZETA_BRIDGE as cxc


# ── W(3,3) atoms ──────────────────────────────────────────────────────────────

class TestAtoms:
    def test_Q_is_3(self):
        assert cxc.Q == 3

    def test_LAM_is_2(self):
        assert cxc.LAM == 2

    def test_MU_is_4(self):
        assert cxc.MU == 4

    def test_V_is_40(self):
        assert cxc.V == 40

    def test_K_is_12(self):
        assert cxc.K == 12

    def test_PHI3_is_13(self):
        assert cxc.PHI3 == 13

    def test_PHI4_is_10(self):
        assert cxc.PHI4 == 10

    def test_PHI6_is_7(self):
        assert cxc.PHI6 == 7

    def test_PHI12_is_73(self):
        assert cxc.PHI12 == 73

    def test_ALPHA_INV_is_137(self):
        assert cxc.ALPHA_INV == 137

    def test_EIGENVALUES(self):
        assert cxc.EIGENVALUES == (5, -1, -7)

    def test_MULTIPLICITIES(self):
        assert cxc.MULTIPLICITIES == (10, 16, 6)

    def test_DEGREE_Z(self):
        assert cxc.DEGREE_Z == 32


# ── Utility functions ─────────────────────────────────────────────────────────

class TestIsPrime:
    def test_primes(self):
        for p in [2, 3, 5, 7, 11, 13, 137]:
            assert cxc.is_prime(p)

    def test_non_primes(self):
        for n in [0, 1, 4, 9, 10, 12]:
            assert not cxc.is_prime(n)


class TestNthPrime:
    def test_first_prime(self):
        assert cxc.nth_prime(1) == 2

    def test_fifth_prime(self):
        assert cxc.nth_prime(5) == 11

    def test_tenth_prime(self):
        assert cxc.nth_prime(10) == 29

    def test_33rd_prime(self):
        assert cxc.nth_prime(33) == 137


class TestPrimeIndexOf:
    def test_index_of_2(self):
        assert cxc.prime_index_of(2) == 1

    def test_index_of_5(self):
        assert cxc.prime_index_of(5) == 3

    def test_index_of_7(self):
        assert cxc.prime_index_of(7) == 4

    def test_index_of_13(self):
        assert cxc.prime_index_of(13) == 6

    def test_index_of_137(self):
        assert cxc.prime_index_of(137) == 33

    def test_non_prime_raises(self):
        with pytest.raises(ValueError):
            cxc.prime_index_of(10)


# ── eval_zeta_w33 ────────────────────────────────────────────────────────────

class TestEvalZetaW33:
    def test_at_zero(self):
        assert cxc.eval_zeta_w33(0.0) == 1.0

    def test_at_zero_of_first_factor(self):
        assert abs(cxc.eval_zeta_w33(1.0 / 5.0)) < 1e-12

    def test_at_minus_1(self):
        assert cxc.eval_zeta_w33(-1.0) == 0.0

    def test_at_zero_of_third_factor(self):
        assert abs(cxc.eval_zeta_w33(-1.0 / 7.0)) < 1e-12

    def test_positive_at_small_x(self):
        assert cxc.eval_zeta_w33(0.01) > 0

    def test_formula_at_minus_half(self):
        # Z(-0.5) = (1 - 5×(-0.5))^10 × (1 + (-0.5))^16 × (1 + 7×(-0.5))^6
        # = (3.5)^10 × (0.5)^16 × (-2.5)^6
        # = positive × positive × positive  (even power)
        assert cxc.eval_zeta_w33(-0.5) > 0


# ── vieta_symmetric ───────────────────────────────────────────────────────────

class TestVietaSymmetric:
    def setup_method(self):
        self.v = cxc.vieta_symmetric((5, -1, -7))

    def test_e1(self):
        assert self.v["e1"] == -3

    def test_e2_negative_33(self):
        assert self.v["e2"] == -33

    def test_e2_abs_33(self):
        assert abs(self.v["e2"]) == 33

    def test_e3(self):
        assert self.v["e3"] == 35


# ── leading_coeff_z ───────────────────────────────────────────────────────────

class TestLeadingCoeff:
    def test_positive(self):
        assert cxc.leading_coeff_z() > 0

    def test_value(self):
        assert cxc.leading_coeff_z() == 5**10 * 7**6

    def test_abs_value(self):
        assert abs(cxc.leading_coeff_z()) == 5**10 * 7**6


# ── String dimensions ─────────────────────────────────────────────────────────

class TestStringDimensions:
    def test_bosonic_26(self):
        assert cxc.zeta_minus_1_string() == 26

    def test_bosonic_equals_2_phi3(self):
        assert cxc.zeta_minus_1_string() == 2 * cxc.PHI3

    def test_superstring_10(self):
        assert cxc.dim_superstring() == 10

    def test_superstring_equals_phi4(self):
        assert cxc.dim_superstring() == cxc.PHI4

    def test_m_theory_11(self):
        assert cxc.dim_m_theory() == 11

    def test_m_theory_equals_k_minus_1(self):
        assert cxc.dim_m_theory() == cxc.K - 1

    def test_f_theory_12(self):
        assert cxc.dim_f_theory() == 12

    def test_f_theory_equals_k(self):
        assert cxc.dim_f_theory() == cxc.K


# ── ZetaCheck dataclass ───────────────────────────────────────────────────────

class TestZetaCheck:
    def test_exact_passes_equal_int(self):
        zc = cxc.ZetaCheck("t", "test", 33, 33, exact=True)
        assert zc.passes

    def test_exact_fails_not_equal(self):
        zc = cxc.ZetaCheck("t", "test", 32, 33, exact=True)
        assert not zc.passes

    def test_inexact_passes_within_tolerance(self):
        zc = cxc.ZetaCheck("t", "test", 1.000000000001, 1.0, exact=False)
        assert zc.passes

    def test_inexact_fails_outside_tolerance(self):
        zc = cxc.ZetaCheck("t", "test", 1.5, 1.0, exact=False)
        assert not zc.passes

    def test_bool_passes(self):
        zc = cxc.ZetaCheck("t", "test", True, True, exact=True)
        assert zc.passes

    def test_bool_fails(self):
        zc = cxc.ZetaCheck("t", "test", False, True, exact=True)
        assert not zc.passes


# ── Core theorem: 137 is the 33rd prime ──────────────────────────────────────

class TestAlphaPrimeTheorem:
    """The central result of Part CXC."""

    def test_137_is_prime(self):
        assert cxc.is_prime(137)

    def test_137_is_33rd_prime(self):
        assert cxc.prime_index_of(137) == 33

    def test_33rd_prime_is_137(self):
        assert cxc.nth_prime(33) == 137

    def test_vieta2_abs_equals_prime_index_of_alpha_inv(self):
        v = cxc.vieta_symmetric(cxc.EIGENVALUES)
        assert abs(v["e2"]) == cxc.prime_index_of(cxc.ALPHA_INV)

    def test_vieta2_abs_equals_33(self):
        v = cxc.vieta_symmetric(cxc.EIGENVALUES)
        assert abs(v["e2"]) == 33

    def test_theorem_chain(self):
        # Complete chain: |e₂(5,-1,-7)| = 33 → 33rd prime = 137 = α⁻¹
        v = cxc.vieta_symmetric(cxc.EIGENVALUES)
        prime_index = abs(v["e2"])
        assert cxc.nth_prime(prime_index) == cxc.ALPHA_INV


# ── _make_zeta_checks ─────────────────────────────────────────────────────────

class TestMakeZetaChecks:
    def test_count(self):
        checks = cxc._make_zeta_checks()
        assert len(checks) == 31

    def test_all_pass(self):
        checks = cxc._make_zeta_checks()
        failing = [c.name for c in checks if not c.passes]
        assert failing == [], f"Failing checks: {failing}"

    def test_z_at_zero_check_passes(self):
        checks = {c.name: c for c in cxc._make_zeta_checks()}
        assert checks["Z_at_0"].passes

    def test_z_at_minus1_check_passes(self):
        checks = {c.name: c for c in cxc._make_zeta_checks()}
        assert checks["Z_at_minus_1"].passes

    def test_137_is_33rd_prime_check_passes(self):
        checks = {c.name: c for c in cxc._make_zeta_checks()}
        assert checks["137_is_33rd_prime"].passes

    def test_vieta2_abs_33_check_passes(self):
        checks = {c.name: c for c in cxc._make_zeta_checks()}
        assert checks["vieta_e2_abs_33"].passes

    def test_bosonic_string_check_passes(self):
        checks = {c.name: c for c in cxc._make_zeta_checks()}
        assert checks["bosonic_string_26"].passes

    def test_superstring_check_passes(self):
        checks = {c.name: c for c in cxc._make_zeta_checks()}
        assert checks["superstring_10"].passes

    def test_m_theory_check_passes(self):
        checks = {c.name: c for c in cxc._make_zeta_checks()}
        assert checks["m_theory_11"].passes

    def test_f_theory_check_passes(self):
        checks = {c.name: c for c in cxc._make_zeta_checks()}
        assert checks["f_theory_12"].passes


# ── Full audit dict ───────────────────────────────────────────────────────────

class TestRiemannZetaBridgeAudit:
    def setup_method(self):
        self.result = cxc.riemann_zeta_bridge_audit()

    def test_status_pass(self):
        assert self.result["status"] == "PASS"

    def test_all_checks_pass(self):
        assert self.result["all_checks_pass"] is True

    def test_no_failed_checks(self):
        assert self.result["failed_checks"] == []

    def test_check_count(self):
        assert self.result["check_count"] == 31

    def test_checks_passing_equals_count(self):
        assert self.result["checks_passing"] == self.result["check_count"]

    def test_zeta_structure_z_at_0(self):
        assert self.result["zeta_structure"]["Z_at_0"] == 1.0

    def test_zeta_structure_z_at_minus1(self):
        assert self.result["zeta_structure"]["Z_at_minus1"] == 0.0

    def test_zeta_structure_frobenius_evs(self):
        assert self.result["zeta_structure"]["frobenius_eigenvalues"] == [5, -1, -7]

    def test_zeta_structure_multiplicities(self):
        assert self.result["zeta_structure"]["multiplicities"] == [10, 16, 6]

    def test_zeta_structure_degree(self):
        assert self.result["zeta_structure"]["degree"] == 32

    def test_zeta_structure_leading_coeff(self):
        assert self.result["zeta_structure"]["leading_coefficient"] == 5**10 * 7**6

    def test_vieta_e2(self):
        assert self.result["vieta"]["e2"] == -33

    def test_vieta_abs_e2(self):
        assert self.result["vieta"]["abs_e2"] == 33

    def test_alpha_prime_connection_prime_index(self):
        assert self.result["alpha_prime_connection"]["prime_index_1based"] == 33

    def test_alpha_prime_connection_is_prime(self):
        assert self.result["alpha_prime_connection"]["is_prime"] is True

    def test_alpha_prime_connection_vieta2_abs(self):
        assert self.result["alpha_prime_connection"]["vieta2_abs"] == 33

    def test_string_dimensions_bosonic(self):
        assert self.result["string_dimensions"]["bosonic_26"] == 26

    def test_string_dimensions_super(self):
        assert self.result["string_dimensions"]["superstring_10"] == 10

    def test_string_dimensions_m_theory(self):
        assert self.result["string_dimensions"]["m_theory_11"] == 11

    def test_string_dimensions_f_theory(self):
        assert self.result["string_dimensions"]["f_theory_12"] == 12

    def test_theorem_key_present(self):
        assert "theorem_cxc" in self.result

    def test_theorem_mentions_riemann(self):
        t = self.result["theorem_cxc"].lower()
        assert "riemann" in t or "zeta" in t or "137" in t

    def test_w33_atoms_present(self):
        atoms = self.result["w33_atoms"]
        assert atoms["ALPHA_INV"] == 137
        assert atoms["PHI3"] == 13
