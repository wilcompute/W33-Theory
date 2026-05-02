"""
Tests for PART_CXCVI: Mathieu Groups Bridge
"""

import pytest
from PART_CXCVI_MATHIEU_GROUPS_BRIDGE import (
    Q, LAM, V, K, PHI3, PHI4, PHI6, J_INV, EDGES, EIG_MAX, MULT_K2,
    MATHIEU_STEINER,
    M11_P_ADIC, M12_P_ADIC, M22_P_ADIC, M23_P_ADIC, M24_P_ADIC,
    GOLAY_PRIME,
    MathCheck,
    _make_atom_checks,
    _make_degree_checks,
    _make_steiner_t_checks,
    _make_steiner_k_checks,
    _make_steiner_n_checks,
    _make_group_order_valuation_checks,
    _make_structural_checks,
    mathieu_groups_bridge_audit,
)


# ---------------------------------------------------------------------------
# Atom tests
# ---------------------------------------------------------------------------
class TestAtoms:
    def test_Q(self):
        assert Q == 3

    def test_LAM(self):
        assert LAM == 2

    def test_V(self):
        assert V == 40

    def test_K(self):
        assert K == 12

    def test_PHI3(self):
        assert PHI3 == Q**2 + Q + 1 == 13

    def test_PHI4(self):
        assert PHI4 == Q**2 + 1 == 10

    def test_PHI6(self):
        assert PHI6 == Q**2 - Q + 1 == 7

    def test_J_INV(self):
        assert J_INV == 8

    def test_EIG_MAX(self):
        assert EIG_MAX == 5

    def test_MULT_K2(self):
        assert MULT_K2 == K // 2 == 6


# ---------------------------------------------------------------------------
# Steiner data
# ---------------------------------------------------------------------------
class TestMathieuSteinerData:
    def test_five_groups(self):
        assert len(MATHIEU_STEINER) == 5

    def test_groups_present(self):
        for name in ("M11", "M12", "M22", "M23", "M24"):
            assert name in MATHIEU_STEINER

    def test_M11_steiner(self):
        deg, t, k, n = MATHIEU_STEINER["M11"]
        assert (deg, t, k, n) == (11, 4, 5, 11)

    def test_M12_steiner(self):
        deg, t, k, n = MATHIEU_STEINER["M12"]
        assert (deg, t, k, n) == (12, 5, 6, 12)

    def test_M22_steiner(self):
        deg, t, k, n = MATHIEU_STEINER["M22"]
        assert (deg, t, k, n) == (22, 3, 6, 22)

    def test_M23_steiner(self):
        deg, t, k, n = MATHIEU_STEINER["M23"]
        assert (deg, t, k, n) == (23, 4, 7, 23)

    def test_M24_steiner(self):
        deg, t, k, n = MATHIEU_STEINER["M24"]
        assert (deg, t, k, n) == (24, 5, 8, 24)

    def test_n_equals_degree(self):
        """For each Mathieu group the n-parameter equals the degree."""
        for name, (deg, t, k, n) in MATHIEU_STEINER.items():
            assert deg == n, f"{name}: degree {deg} != n {n}"


# ---------------------------------------------------------------------------
# Group order data
# ---------------------------------------------------------------------------
class TestGroupOrderData:
    def test_m11_v2(self):
        assert M11_P_ADIC[2] == 4

    def test_m11_v3(self):
        assert M11_P_ADIC[3] == 2

    def test_m12_v2(self):
        assert M12_P_ADIC[2] == 6

    def test_m12_v3(self):
        assert M12_P_ADIC[3] == 3

    def test_m22_v2(self):
        assert M22_P_ADIC[2] == 7

    def test_m22_v3(self):
        assert M22_P_ADIC[3] == 2

    def test_m23_v2(self):
        assert M23_P_ADIC[2] == 7

    def test_m23_v3(self):
        assert M23_P_ADIC[3] == 2

    def test_m24_v2(self):
        assert M24_P_ADIC[2] == 10

    def test_m24_v3(self):
        assert M24_P_ADIC[3] == 3

    def test_golay_prime_value(self):
        assert GOLAY_PRIME == 23


# ---------------------------------------------------------------------------
# MathCheck dataclass
# ---------------------------------------------------------------------------
class TestMathCheck:
    def test_exact_pass(self):
        c = MathCheck("t", "d", 7, 7)
        assert c.passes

    def test_exact_fail(self):
        c = MathCheck("t", "d", 7, 8)
        assert not c.passes

    def test_inexact_pass(self):
        c = MathCheck("t", "d", 1.000000000001, 1.0, exact=False)
        assert c.passes

    def test_inexact_fail(self):
        c = MathCheck("t", "d", 1.001, 1.0, exact=False)
        assert not c.passes


# ---------------------------------------------------------------------------
# Degree checks
# ---------------------------------------------------------------------------
class TestDegreeChecks:
    def setup_method(self):
        self.checks = _make_degree_checks()

    def test_count(self):
        assert len(self.checks) == 5

    def test_all_pass(self):
        failed = [c for c in self.checks if not c.passes]
        assert not failed, [c.name for c in failed]

    def test_m11_degree_formula(self):
        assert MATHIEU_STEINER["M11"][0] == K - 1  # 11

    def test_m12_degree_formula(self):
        assert MATHIEU_STEINER["M12"][0] == K  # 12

    def test_m22_degree_formula(self):
        assert MATHIEU_STEINER["M22"][0] == 2 * (K - 1)  # 22

    def test_m23_degree_formula(self):
        assert MATHIEU_STEINER["M23"][0] == K + PHI3 - 2  # 23

    def test_m24_degree_formula(self):
        assert MATHIEU_STEINER["M24"][0] == 2 * K  # 24


# ---------------------------------------------------------------------------
# Steiner t-parameter checks
# ---------------------------------------------------------------------------
class TestSteinerTChecks:
    def setup_method(self):
        self.checks = _make_steiner_t_checks()

    def test_count(self):
        assert len(self.checks) == 5

    def test_all_pass(self):
        failed = [c for c in self.checks if not c.passes]
        assert not failed, [c.name for c in failed]

    def test_m11_t(self):
        assert MATHIEU_STEINER["M11"][1] == J_INV // 2  # 4

    def test_m12_t(self):
        assert MATHIEU_STEINER["M12"][1] == EIG_MAX  # 5

    def test_m22_t(self):
        assert MATHIEU_STEINER["M22"][1] == Q  # 3

    def test_m23_t(self):
        assert MATHIEU_STEINER["M23"][1] == J_INV // 2  # 4

    def test_m24_t(self):
        assert MATHIEU_STEINER["M24"][1] == EIG_MAX  # 5


# ---------------------------------------------------------------------------
# Steiner k-parameter checks
# ---------------------------------------------------------------------------
class TestSteinerKChecks:
    def setup_method(self):
        self.checks = _make_steiner_k_checks()

    def test_count(self):
        assert len(self.checks) == 5

    def test_all_pass(self):
        failed = [c for c in self.checks if not c.passes]
        assert not failed, [c.name for c in failed]

    def test_m11_k(self):
        assert MATHIEU_STEINER["M11"][2] == EIG_MAX  # 5

    def test_m12_k(self):
        assert MATHIEU_STEINER["M12"][2] == K // 2  # 6

    def test_m22_k(self):
        assert MATHIEU_STEINER["M22"][2] == K // 2  # 6

    def test_m23_k(self):
        assert MATHIEU_STEINER["M23"][2] == PHI6  # 7

    def test_m24_k(self):
        assert MATHIEU_STEINER["M24"][2] == J_INV  # 8


# ---------------------------------------------------------------------------
# Steiner n-parameter checks
# ---------------------------------------------------------------------------
class TestSteinerNChecks:
    def setup_method(self):
        self.checks = _make_steiner_n_checks()

    def test_count(self):
        assert len(self.checks) == 5

    def test_all_pass(self):
        failed = [c for c in self.checks if not c.passes]
        assert not failed, [c.name for c in failed]

    def test_m11_n(self):
        assert MATHIEU_STEINER["M11"][3] == K - 1  # 11

    def test_m12_n(self):
        assert MATHIEU_STEINER["M12"][3] == K  # 12

    def test_m22_n(self):
        assert MATHIEU_STEINER["M22"][3] == 2 * (K - 1)  # 22

    def test_m23_n(self):
        assert MATHIEU_STEINER["M23"][3] == K + PHI3 - 2  # 23

    def test_m24_n(self):
        assert MATHIEU_STEINER["M24"][3] == 2 * K  # 24


# ---------------------------------------------------------------------------
# Group order valuation checks
# ---------------------------------------------------------------------------
class TestGroupOrderValuationChecks:
    def setup_method(self):
        self.checks = _make_group_order_valuation_checks()

    def test_count(self):
        assert len(self.checks) == 10

    def test_all_pass(self):
        failed = [c for c in self.checks if not c.passes]
        assert not failed, [c.name for c in failed]

    def test_m11_v2_formula(self):
        assert M11_P_ADIC[2] == J_INV // 2  # 4

    def test_m11_v3_formula(self):
        assert M11_P_ADIC[3] == LAM  # 2

    def test_m12_v2_formula(self):
        assert M12_P_ADIC[2] == K // 2  # 6

    def test_m12_v3_formula(self):
        assert M12_P_ADIC[3] == Q  # 3

    def test_m22_v2_formula(self):
        assert M22_P_ADIC[2] == PHI6  # 7

    def test_m22_v3_formula(self):
        assert M22_P_ADIC[3] == LAM  # 2

    def test_m23_v2_formula(self):
        assert M23_P_ADIC[2] == PHI6  # 7

    def test_m23_v3_formula(self):
        assert M23_P_ADIC[3] == LAM  # 2

    def test_m24_v2_formula(self):
        assert M24_P_ADIC[2] == PHI4  # 10

    def test_m24_v3_formula(self):
        assert M24_P_ADIC[3] == Q  # 3


# ---------------------------------------------------------------------------
# Structural checks
# ---------------------------------------------------------------------------
class TestStructuralChecks:
    def setup_method(self):
        self.checks = _make_structural_checks()

    def test_count(self):
        assert len(self.checks) == 8

    def test_all_pass(self):
        failed = [c for c in self.checks if not c.passes]
        assert not failed, [c.name for c in failed]

    def test_mathieu_count(self):
        assert len(MATHIEU_STEINER) == EIG_MAX  # 5

    def test_m11_param_sum(self):
        _, t, k, n = MATHIEU_STEINER["M11"]
        assert t + k + n == V // 2  # 4+5+11 = 20

    def test_m12_param_sum(self):
        _, t, k, n = MATHIEU_STEINER["M12"]
        assert t + k + n == K + PHI3 - 2  # 5+6+12 = 23

    def test_m24_acts_on_2k(self):
        assert MATHIEU_STEINER["M24"][3] == 2 * K  # 24

    def test_golay_prime_in_m23(self):
        assert 23 in M23_P_ADIC

    def test_golay_prime_in_m24(self):
        assert 23 in M24_P_ADIC

    def test_golay_prime_formula(self):
        assert GOLAY_PRIME == K + PHI3 - 2  # 23


# ---------------------------------------------------------------------------
# Full audit
# ---------------------------------------------------------------------------
class TestMathieuAudit:
    def setup_method(self):
        self.result = mathieu_groups_bridge_audit()

    def test_status_pass(self):
        assert self.result["status"] == "PASS"

    def test_all_checks_pass(self):
        assert self.result["all_checks_pass"] is True

    def test_check_count(self):
        assert self.result["check_count"] == 47

    def test_checks_passing(self):
        assert self.result["checks_passing"] == 47

    def test_no_failed_checks(self):
        assert self.result["failed_checks"] == []

    def test_category_atom_count(self):
        assert self.result["category_counts"]["atom_checks"] == 9

    def test_category_degree_count(self):
        assert self.result["category_counts"]["degree_checks"] == 5

    def test_category_steiner_t_count(self):
        assert self.result["category_counts"]["steiner_t_checks"] == 5

    def test_category_steiner_k_count(self):
        assert self.result["category_counts"]["steiner_k_checks"] == 5

    def test_category_steiner_n_count(self):
        assert self.result["category_counts"]["steiner_n_checks"] == 5

    def test_category_valuation_count(self):
        assert self.result["category_counts"]["group_order_valuation_checks"] == 10

    def test_category_structural_count(self):
        assert self.result["category_counts"]["structural_checks"] == 8

    def test_steiner_in_result(self):
        steiner = self.result["mathieu_steiner"]
        assert "M11" in steiner
        assert steiner["M24"]["steiner_system"] == "S(5,8,24)"

    def test_w33_atoms_in_result(self):
        atoms = self.result["w33_atoms"]
        assert atoms["Q"] == 3
        assert atoms["K"] == 12

    def test_theorem_present(self):
        assert "theorem_cxcvi" in self.result
        assert len(self.result["theorem_cxcvi"]) > 50

    def test_category_counts_sum(self):
        total = sum(self.result["category_counts"].values())
        assert total == 47
