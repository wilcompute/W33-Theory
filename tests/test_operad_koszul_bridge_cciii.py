"""
Tests for PART_CCIII: Operads / Koszul Duality Bridge
======================================================
Regression tests for atom, Ass, Lie, Stasheff, Bell, Catalan, structural checks.
"""

import pytest

from PART_CCIII_OPERAD_KOSZUL_BRIDGE import (
    Q, LAM, V, K, PHI3, PHI4, PHI6, J_INV, EDGES, EIG_MAX, MULT_K2, LEECH_DIM,
    factorial, catalan, assoc_operad_dim, comm_operad_dim, lie_operad_dim,
    planar_binary_trees, stasheff_vertices, partitions_of, free_lie_dim,
    ASS_Q, ASS_LAM, ASS_EIG,
    LIE_Q, LIE_LAM, LIE_EIG,
    COM_Q,
    ASS_Q_IS_MULT_K2, ASS_EIG_IS_EIG_LEECH, ASS_LAM_IS_LAM,
    LIE_Q_IS_LAM, LIE_EIG_IS_LEECH,
    SHUFFLE_Q, SHUFFLE_EIG, SHUFFLE_Q_IS_MULT_K2, SHUFFLE_EIG_IS_PROD,
    STASHEFF_K3, STASHEFF_K4, STASHEFF_K5,
    STASHEFF_K3_IS_LAM, STASHEFF_K4_IS_EIG,
    PBT_Q_LEAVES, PBT_Q1_LEAVES, PBT_EIG_LEAVES,
    PBT_Q_IS_LAM, PBT_Q1_IS_EIG,
    BELL_LAM, BELL_Q, BELL_EIG,
    BELL_LAM_IS_LAM, BELL_Q_IS_EIG,
    DENDRI_Q, DENDRI_LAM,
    DENDRI_Q_IS_EIG, DENDRI_LAM_IS_LAM,
    FREE_LIE_LAM, FREE_LIE_LAM_IS_Q,
    KOSZUL_ASS_SELF_DUAL_Q, KOSZUL_COM_DUAL_LIE_Q, KOSZUL_LIE_DUAL_COM_Q,
    PARENT_Q, PARENT_LAM, PARENT_Q_IS_EIG, PARENT_LAM_IS_LAM,
    OPETOPE_2_Q, OPETOPE_2_Q1, OPETOPE_2_Q_IS_LAM, OPETOPE_2_Q1_IS_EIG,
    OperadCheck,
    _make_atom_checks, _make_ass_checks, _make_lie_checks,
    _make_stasheff_checks, _make_bell_checks,
    _make_catalan_checks, _make_structural_checks,
    operad_koszul_bridge_audit,
)


class TestAtoms:
    def test_Q(self): assert Q == 3
    def test_LAM(self): assert LAM == 2
    def test_V(self): assert V == 40
    def test_K(self): assert K == 12
    def test_EIG_MAX(self): assert EIG_MAX == 5
    def test_MULT_K2(self): assert MULT_K2 == 6
    def test_PHI6(self): assert PHI6 == 7
    def test_J_INV(self): assert J_INV == 8
    def test_LEECH_DIM(self): assert LEECH_DIM == 24


class TestFunctions:
    def test_factorial_3(self): assert factorial(3) == 6
    def test_factorial_5(self): assert factorial(5) == 120
    def test_catalan_2(self): assert catalan(2) == 2
    def test_catalan_3(self): assert catalan(3) == 5
    def test_assoc_dim_3(self): assert assoc_operad_dim(3) == 6
    def test_comm_dim_3(self): assert comm_operad_dim(3) == 1
    def test_lie_dim_3(self): assert lie_operad_dim(3) == 2
    def test_lie_dim_5(self): assert lie_operad_dim(5) == 24
    def test_pbt_3(self): assert planar_binary_trees(3) == 2
    def test_pbt_4(self): assert planar_binary_trees(4) == 5
    def test_stasheff_4(self): assert stasheff_vertices(4) == 2
    def test_stasheff_5(self): assert stasheff_vertices(5) == 5
    def test_bell_2(self): assert partitions_of(2) == 2
    def test_bell_3(self): assert partitions_of(3) == 5
    def test_free_lie_2(self): assert free_lie_dim(2) == 3


class TestAssOperad:
    def test_ass_q_mult_k2(self): assert ASS_Q == MULT_K2
    def test_ass_q_value(self): assert ASS_Q == 6
    def test_ass_lam_lam(self): assert ASS_LAM == LAM
    def test_ass_lam_value(self): assert ASS_LAM == 2
    def test_ass_eig_value(self): assert ASS_EIG == 120
    def test_ass_eig_prod(self): assert ASS_EIG == EIG_MAX * LEECH_DIM
    def test_com_q(self): assert COM_Q == 1
    def test_shuffle_q(self): assert SHUFFLE_Q == MULT_K2
    def test_shuffle_eig(self): assert SHUFFLE_EIG == EIG_MAX * LEECH_DIM
    def test_flag_q(self): assert ASS_Q_IS_MULT_K2 is True
    def test_flag_eig(self): assert ASS_EIG_IS_EIG_LEECH is True
    def test_flag_lam(self): assert ASS_LAM_IS_LAM is True
    def test_shuffle_flag_q(self): assert SHUFFLE_Q_IS_MULT_K2 is True
    def test_shuffle_flag_eig(self): assert SHUFFLE_EIG_IS_PROD is True


class TestLieOperad:
    def test_lie_q_lam(self): assert LIE_Q == LAM
    def test_lie_q_value(self): assert LIE_Q == 2
    def test_lie_lam(self): assert LIE_LAM == 1
    def test_lie_eig_leech(self): assert LIE_EIG == LEECH_DIM
    def test_lie_eig_value(self): assert LIE_EIG == 24
    def test_free_lie_lam_q(self): assert FREE_LIE_LAM == Q
    def test_flag_q(self): assert LIE_Q_IS_LAM is True
    def test_flag_eig(self): assert LIE_EIG_IS_LEECH is True
    def test_flag_free_lie(self): assert FREE_LIE_LAM_IS_Q is True
    def test_koszul_self(self): assert KOSZUL_ASS_SELF_DUAL_Q is True
    def test_koszul_com_lie(self): assert KOSZUL_COM_DUAL_LIE_Q is True
    def test_koszul_lie_com(self): assert KOSZUL_LIE_DUAL_COM_Q is True


class TestStasheff:
    def test_k3_lam(self): assert STASHEFF_K3 == LAM
    def test_k4_eig(self): assert STASHEFF_K4 == EIG_MAX
    def test_k5(self): assert STASHEFF_K5 == 14
    def test_k3_flag(self): assert STASHEFF_K3_IS_LAM is True
    def test_k4_flag(self): assert STASHEFF_K4_IS_EIG is True
    def test_pbt_q_lam(self): assert PBT_Q_LEAVES == LAM
    def test_pbt_q1_eig(self): assert PBT_Q1_LEAVES == EIG_MAX
    def test_pbt_eig(self): assert PBT_EIG_LEAVES == 14
    def test_pbt_q_flag(self): assert PBT_Q_IS_LAM is True
    def test_pbt_q1_flag(self): assert PBT_Q1_IS_EIG is True


class TestBellDendri:
    def test_bell_lam(self): assert BELL_LAM == LAM
    def test_bell_q(self): assert BELL_Q == EIG_MAX
    def test_bell_eig(self): assert BELL_EIG == 52
    def test_bell_lam_flag(self): assert BELL_LAM_IS_LAM is True
    def test_bell_q_flag(self): assert BELL_Q_IS_EIG is True
    def test_dendri_q(self): assert DENDRI_Q == EIG_MAX
    def test_dendri_lam(self): assert DENDRI_LAM == LAM
    def test_dendri_q_flag(self): assert DENDRI_Q_IS_EIG is True
    def test_dendri_lam_flag(self): assert DENDRI_LAM_IS_LAM is True


class TestCatalan:
    def test_cat2_lam(self): assert catalan(2) == LAM
    def test_cat3_eig(self): assert catalan(3) == EIG_MAX
    def test_cat4(self): assert catalan(4) == 14
    def test_cat5(self): assert catalan(5) == 42
    def test_cat6(self): assert catalan(6) == 132
    def test_parent_q(self): assert PARENT_Q == EIG_MAX
    def test_parent_lam(self): assert PARENT_LAM == LAM
    def test_parent_q_flag(self): assert PARENT_Q_IS_EIG is True
    def test_parent_lam_flag(self): assert PARENT_LAM_IS_LAM is True
    def test_opetope_q(self): assert OPETOPE_2_Q == LAM
    def test_opetope_q1(self): assert OPETOPE_2_Q1 == EIG_MAX
    def test_opetope_q_flag(self): assert OPETOPE_2_Q_IS_LAM is True
    def test_opetope_q1_flag(self): assert OPETOPE_2_Q1_IS_EIG is True


class TestStructural:
    def test_ass_plus_lie_q(self): assert ASS_Q + LIE_Q == J_INV
    def test_cat_sum_phi6(self): assert catalan(2) + catalan(3) == PHI6
    def test_stasheff_sum_phi6(self): assert STASHEFF_K3 + STASHEFF_K4 == PHI6
    def test_bell_sum_phi6(self): assert BELL_LAM + BELL_Q == PHI6
    def test_pbt_sum_phi6(self): assert PBT_Q_LEAVES + PBT_Q1_LEAVES == PHI6
    def test_dendri_sum_phi6(self): assert DENDRI_Q + DENDRI_LAM == PHI6
    def test_lie_product(self): assert LIE_Q * LIE_EIG == LAM * LEECH_DIM


class TestOperadCheck:
    def test_exact_pass(self):
        c = OperadCheck("t", "d", 6, 6)
        assert c.passes

    def test_exact_fail(self):
        c = OperadCheck("t", "d", 5, 6)
        assert not c.passes

    def test_inexact_pass(self):
        c = OperadCheck("t", "d", 1.0 + 1e-12, 1.0, exact=False)
        assert c.passes

    def test_inexact_fail(self):
        c = OperadCheck("t", "d", 1.0 + 1e-9, 1.0, exact=False)
        assert not c.passes

    def test_frozen(self):
        c = OperadCheck("t", "d", 1, 1)
        with pytest.raises((AttributeError, TypeError)):
            c.name = "x"  # type: ignore[misc]


class TestCheckFactories:
    def test_atom_count(self): assert len(_make_atom_checks()) == 9
    def test_atom_all_pass(self): assert all(c.passes for c in _make_atom_checks())
    def test_ass_count(self): assert len(_make_ass_checks()) == 9
    def test_ass_all_pass(self): assert all(c.passes for c in _make_ass_checks())
    def test_lie_count(self): assert len(_make_lie_checks()) == 9
    def test_lie_all_pass(self): assert all(c.passes for c in _make_lie_checks())
    def test_stasheff_count(self): assert len(_make_stasheff_checks()) == 9
    def test_stasheff_all_pass(self): assert all(c.passes for c in _make_stasheff_checks())
    def test_bell_count(self): assert len(_make_bell_checks()) == 7
    def test_bell_all_pass(self): assert all(c.passes for c in _make_bell_checks())
    def test_catalan_count(self): assert len(_make_catalan_checks()) == 9
    def test_catalan_all_pass(self): assert all(c.passes for c in _make_catalan_checks())
    def test_structural_count(self): assert len(_make_structural_checks()) == 10
    def test_structural_all_pass(self): assert all(c.passes for c in _make_structural_checks())


class TestAudit:
    def setup_method(self):
        self.result = operad_koszul_bridge_audit()

    def test_status_pass(self): assert self.result["status"] == "PASS"
    def test_all_pass(self): assert self.result["all_checks_pass"] is True
    def test_no_failed(self): assert self.result["failed_checks"] == []
    def test_check_count(self): assert self.result["check_count"] == 62
    def test_checks_passing(self): assert self.result["checks_passing"] == 62

    def test_operad_dims(self):
        od = self.result["operad_dims"]
        assert od["Ass_Q"] == 6
        assert od["Lie_Q"] == 2
        assert od["Lie_EIG"] == 24

    def test_catalan_numbers(self):
        cn = self.result["catalan_numbers"]
        assert cn["C_2"] == 2
        assert cn["C_3"] == 5

    def test_bell_numbers(self):
        bn = self.result["bell_numbers"]
        assert bn["B_2"] == 2
        assert bn["B_3"] == 5

    def test_atoms_present(self):
        a = self.result["w33_atoms"]
        assert a["Q"] == 3 and a["EIG_MAX"] == 5

    def test_theorem_key(self): assert "theorem_cciii" in self.result

    def test_category_counts(self):
        c = self.result["category_counts"]
        assert c["atom_checks"] == 9
        assert c["ass_checks"] == 9
        assert c["catalan_checks"] == 9
