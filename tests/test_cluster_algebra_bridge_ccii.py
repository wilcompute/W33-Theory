"""
Tests for PART_CCII: Cluster Algebras / Fomin-Zelevinsky Bridge
================================================================
Regression tests for atom, type-A_Q, type-A_EIG, type-A_LAM, type-D, Catalan,
and structural checks.
"""

import pytest

from PART_CCII_CLUSTER_ALGEBRA_BRIDGE import (
    Q, LAM, V, K, PHI3, PHI4, PHI6, J_INV, EDGES, EIG_MAX, MULT_K2, LEECH_DIM,
    catalan, cluster_vars_A, cluster_count_A, frieze_period_A,
    positive_roots_A, positive_roots_D, cluster_vars_D, cluster_vars_E,
    A_Q_VARS, A_Q_CLUSTERS, A_Q_PERIOD, A_Q_POS_ROOTS,
    A_Q_VARS_IS_Q_SQ, A_Q_PERIOD_IS_MULT_K2, A_Q_POS_ROOTS_IS_MULT_K2,
    A_EIG_VARS, A_EIG_CLUSTERS, A_EIG_PERIOD, A_EIG_POS_ROOTS,
    A_EIG_VARS_IS_HALF_V, A_EIG_PERIOD_IS_J_INV, A_EIG_POS_ROOTS_IS_PHI4_PLUS_EIG,
    A_LAM_VARS, A_LAM_CLUSTERS, A_LAM_PERIOD, A_LAM_POS_ROOTS,
    A_LAM_VARS_IS_EIG_MAX, A_LAM_CLUSTERS_IS_EIG_MAX, A_LAM_PERIOD_IS_EIG_MAX, A_LAM_POS_ROOTS_IS_Q,
    D_Q_VARS, D_Q_POS_ROOTS, D_Q_VARS_IS_K, D_Q_POS_ROOTS_IS_MULT_K2,
    A_K_POS_ROOTS, A_K_POS_ROOTS_IS_MULT_K2_PHI3,
    CATALAN_2, CATALAN_3, CATALAN_4, CATALAN_5, CATALAN_6,
    CATALAN_2_IS_LAM, CATALAN_3_IS_EIG_MAX,
    E6_VARS, E6_VARS_IS_SUM,
    ClusterCheck,
    _make_atom_checks, _make_type_a_q_checks, _make_type_a_eig_checks,
    _make_type_a_lam_checks, _make_type_d_checks, _make_catalan_checks,
    _make_structural_checks,
    cluster_algebra_bridge_audit,
)


class TestAtoms:
    def test_Q(self): assert Q == 3
    def test_LAM(self): assert LAM == 2
    def test_K(self): assert K == 12
    def test_PHI3(self): assert PHI3 == 13
    def test_PHI4(self): assert PHI4 == 10
    def test_PHI6(self): assert PHI6 == 7
    def test_J_INV(self): assert J_INV == 8
    def test_EDGES(self): assert EDGES == 240
    def test_EIG_MAX(self): assert EIG_MAX == 5


class TestFunctions:
    def test_catalan_2(self): assert catalan(2) == 2
    def test_catalan_3(self): assert catalan(3) == 5
    def test_catalan_4(self): assert catalan(4) == 14
    def test_catalan_5(self): assert catalan(5) == 42
    def test_cluster_vars_a2(self): assert cluster_vars_A(2) == 5
    def test_cluster_vars_a3(self): assert cluster_vars_A(3) == 9
    def test_cluster_count_a3(self): assert cluster_count_A(3) == 14
    def test_frieze_period_a3(self): assert frieze_period_A(3) == 6
    def test_pos_roots_a2(self): assert positive_roots_A(2) == 3
    def test_pos_roots_a3(self): assert positive_roots_A(3) == 6
    def test_cluster_vars_d3(self): assert cluster_vars_D(3) == 12
    def test_pos_roots_d3(self): assert positive_roots_D(3) == 6
    def test_cluster_vars_e6(self): assert cluster_vars_E(6) == 36
    def test_cluster_vars_e8(self): assert cluster_vars_E(8) == 120


class TestTypeAQ:
    def test_vars_q_sq(self): assert A_Q_VARS == Q**2
    def test_vars_value(self): assert A_Q_VARS == 9
    def test_clusters(self): assert A_Q_CLUSTERS == 14
    def test_period_mult_k2(self): assert A_Q_PERIOD == MULT_K2
    def test_period_value(self): assert A_Q_PERIOD == 6
    def test_pos_roots_mult_k2(self): assert A_Q_POS_ROOTS == MULT_K2
    def test_vars_flag(self): assert A_Q_VARS_IS_Q_SQ is True
    def test_period_flag(self): assert A_Q_PERIOD_IS_MULT_K2 is True
    def test_roots_flag(self): assert A_Q_POS_ROOTS_IS_MULT_K2 is True


class TestTypeAEIG:
    def test_vars_half_v(self): assert A_EIG_VARS == V // 2
    def test_vars_value(self): assert A_EIG_VARS == 20
    def test_clusters(self): assert A_EIG_CLUSTERS == 132
    def test_period_j_inv(self): assert A_EIG_PERIOD == J_INV
    def test_period_value(self): assert A_EIG_PERIOD == 8
    def test_pos_roots(self): assert A_EIG_POS_ROOTS == PHI4 + EIG_MAX
    def test_vars_flag(self): assert A_EIG_VARS_IS_HALF_V is True
    def test_period_flag(self): assert A_EIG_PERIOD_IS_J_INV is True
    def test_roots_flag(self): assert A_EIG_POS_ROOTS_IS_PHI4_PLUS_EIG is True


class TestTypeALAM:
    def test_vars_eig(self): assert A_LAM_VARS == EIG_MAX
    def test_clusters_eig(self): assert A_LAM_CLUSTERS == EIG_MAX
    def test_period_eig(self): assert A_LAM_PERIOD == EIG_MAX
    def test_pos_roots_q(self): assert A_LAM_POS_ROOTS == Q
    def test_vars_flag(self): assert A_LAM_VARS_IS_EIG_MAX is True
    def test_clusters_flag(self): assert A_LAM_CLUSTERS_IS_EIG_MAX is True
    def test_period_flag(self): assert A_LAM_PERIOD_IS_EIG_MAX is True
    def test_roots_flag(self): assert A_LAM_POS_ROOTS_IS_Q is True


class TestTypeD:
    def test_dq_vars_k(self): assert D_Q_VARS == K
    def test_dq_vars_value(self): assert D_Q_VARS == 12
    def test_dq_pos_roots(self): assert D_Q_POS_ROOTS == MULT_K2
    def test_dq_vars_flag(self): assert D_Q_VARS_IS_K is True
    def test_dq_roots_flag(self): assert D_Q_POS_ROOTS_IS_MULT_K2 is True
    def test_ak_roots(self): assert A_K_POS_ROOTS == MULT_K2 * PHI3
    def test_ak_roots_flag(self): assert A_K_POS_ROOTS_IS_MULT_K2_PHI3 is True


class TestCatalan:
    def test_cat2_lam(self): assert CATALAN_2 == LAM
    def test_cat3_eig(self): assert CATALAN_3 == EIG_MAX
    def test_cat4(self): assert CATALAN_4 == 14
    def test_cat5(self): assert CATALAN_5 == 42
    def test_cat6(self): assert CATALAN_6 == 132
    def test_cat2_flag(self): assert CATALAN_2_IS_LAM is True
    def test_cat3_flag(self): assert CATALAN_3_IS_EIG_MAX is True


class TestStructural:
    def test_e6_sum(self): assert E6_VARS == LEECH_DIM + K
    def test_e6_value(self): assert E6_VARS == 36
    def test_e6_flag(self): assert E6_VARS_IS_SUM is True
    def test_e8_leech(self): assert cluster_vars_E(8) == EIG_MAX * LEECH_DIM
    def test_d4_roots_k(self): assert positive_roots_D(4) == K


class TestClusterCheck:
    def test_exact_pass(self):
        c = ClusterCheck("t", "d", 9, 9)
        assert c.passes

    def test_exact_fail(self):
        c = ClusterCheck("t", "d", 8, 9)
        assert not c.passes

    def test_inexact_pass(self):
        c = ClusterCheck("t", "d", 1.0 + 1e-12, 1.0, exact=False)
        assert c.passes

    def test_inexact_fail(self):
        c = ClusterCheck("t", "d", 1.0 + 1e-9, 1.0, exact=False)
        assert not c.passes

    def test_frozen(self):
        c = ClusterCheck("t", "d", 1, 1)
        with pytest.raises((AttributeError, TypeError)):
            c.name = "x"  # type: ignore[misc]


class TestCheckFactories:
    def test_atom_count(self): assert len(_make_atom_checks()) == 9
    def test_atom_all_pass(self): assert all(c.passes for c in _make_atom_checks())
    def test_aq_count(self): assert len(_make_type_a_q_checks()) == 9
    def test_aq_all_pass(self): assert all(c.passes for c in _make_type_a_q_checks())
    def test_aeig_count(self): assert len(_make_type_a_eig_checks()) == 9
    def test_aeig_all_pass(self): assert all(c.passes for c in _make_type_a_eig_checks())
    def test_alam_count(self): assert len(_make_type_a_lam_checks()) == 6
    def test_alam_all_pass(self): assert all(c.passes for c in _make_type_a_lam_checks())
    def test_d_count(self): assert len(_make_type_d_checks()) == 6
    def test_d_all_pass(self): assert all(c.passes for c in _make_type_d_checks())
    def test_catalan_count(self): assert len(_make_catalan_checks()) == 7
    def test_catalan_all_pass(self): assert all(c.passes for c in _make_catalan_checks())
    def test_structural_count(self): assert len(_make_structural_checks()) == 10
    def test_structural_all_pass(self): assert all(c.passes for c in _make_structural_checks())


class TestAudit:
    def setup_method(self):
        self.result = cluster_algebra_bridge_audit()

    def test_status_pass(self): assert self.result["status"] == "PASS"
    def test_all_pass(self): assert self.result["all_checks_pass"] is True
    def test_no_failed(self): assert self.result["failed_checks"] == []
    def test_check_count(self): assert self.result["check_count"] == 56
    def test_checks_passing(self): assert self.result["checks_passing"] == 56

    def test_cluster_vars(self):
        cv = self.result["cluster_vars"]
        assert cv["A_Q"] == 9 and cv["D_Q"] == 12 and cv["E_6"] == 36

    def test_frieze_periods(self):
        fp = self.result["frieze_periods"]
        assert fp["A_Q"] == 6 and fp["A_EIG_MAX"] == 8

    def test_atoms_present(self):
        a = self.result["w33_atoms"]
        assert a["Q"] == 3 and a["EDGES"] == 240

    def test_theorem_key(self): assert "theorem_ccii" in self.result

    def test_category_counts(self):
        c = self.result["category_counts"]
        assert c["atom_checks"] == 9
        assert c["type_a_q_checks"] == 9
        assert c["catalan_checks"] == 7
