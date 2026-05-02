"""
Tests for PART_CC: Braid Groups Bridge
=======================================
Regression tests for all atom, generator, Burau, Catalan, Garside, and structural checks.
"""

import math
import pytest

from PART_CC_BRAID_GROUPS_BRIDGE import (
    Q, LAM, V, K, PHI3, PHI4, PHI6, J_INV, EDGES, EIG_MAX, MULT_K2,
    BRAID_FIRST_NONABELIAN,
    GEN_COUNT_B3, GEN_COUNT_B5, GEN_COUNT_B8, GEN_COUNT_B12, GEN_COUNT_B13,
    BURAU_DIM_B3, BURAU_DIM_B5, BURAU_DIM_B8,
    BURAU_FULL_DIM_B3, BURAU_FULL_DIM_B12,
    catalan, TL_DIM_2, TL_DIM_3, TL_DIM_4, TL_DIM_5,
    TL_Q_DIM_IS_EIG_MAX, TL_LAM_DIM_IS_LAM,
    garside_length, GARSIDE_B3, GARSIDE_B5, GARSIDE_B8, GARSIDE_B12,
    GARSIDE_B3_IS_Q, GARSIDE_B5_IS_PHI4,
    GARSIDE_B3_SQ_LENGTH, GARSIDE_B3_SQ_IS_MULT_K2,
    PERM_BRAIDS_B3, PERM_BRAIDS_B5, PERM_BRAIDS_B3_IS_MULT_K2,
    TORUS_T3_K, TORUS_T3_12_IS_Q,
    BRAID_RELS_B3, COMM_RELS_B3, BRAID_RELS_B3_CORRECT,
    GEN_COUNT_B5_IS_LAM_SQ, GEN_COUNT_B8_IS_PHI6, GEN_COUNT_B13_IS_K,
    TL_DELTA_AT_K, TL_DELTA_SQ,
    BraidCheck,
    _make_atom_checks, _make_generator_checks, _make_burau_checks,
    _make_catalan_checks, _make_garside_checks, _make_structural_checks,
    braid_groups_bridge_audit,
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


class TestGenerators:
    def test_b3_is_q(self): assert BRAID_FIRST_NONABELIAN == Q
    def test_gen_b3_lam(self): assert GEN_COUNT_B3 == LAM
    def test_gen_b3_value(self): assert GEN_COUNT_B3 == 2
    def test_gen_b5_lam_sq(self): assert GEN_COUNT_B5 == LAM**2
    def test_gen_b5_value(self): assert GEN_COUNT_B5 == 4
    def test_gen_b5_flag(self): assert GEN_COUNT_B5_IS_LAM_SQ is True
    def test_gen_b8_phi6(self): assert GEN_COUNT_B8 == PHI6
    def test_gen_b8_value(self): assert GEN_COUNT_B8 == 7
    def test_gen_b8_flag(self): assert GEN_COUNT_B8_IS_PHI6 is True
    def test_gen_b13_k(self): assert GEN_COUNT_B13 == K
    def test_gen_b13_flag(self): assert GEN_COUNT_B13_IS_K is True
    def test_gen_b12_value(self): assert GEN_COUNT_B12 == 11


class TestBurau:
    def test_reduced_b3_lam(self): assert BURAU_DIM_B3 == LAM
    def test_reduced_b3_value(self): assert BURAU_DIM_B3 == 2
    def test_reduced_b5_lam_sq(self): assert BURAU_DIM_B5 == LAM**2
    def test_reduced_b5_value(self): assert BURAU_DIM_B5 == 4
    def test_reduced_b8_phi6(self): assert BURAU_DIM_B8 == PHI6
    def test_full_b3_q_sq(self): assert BURAU_FULL_DIM_B3 == Q**2
    def test_full_b3_value(self): assert BURAU_FULL_DIM_B3 == 9
    def test_full_b12_value(self): assert BURAU_FULL_DIM_B12 == K**2


class TestCatalan:
    def test_catalan_2(self): assert catalan(2) == 2
    def test_catalan_3(self): assert catalan(3) == 5
    def test_catalan_4(self): assert catalan(4) == 14
    def test_catalan_5(self): assert catalan(5) == 42
    def test_tl2_lam(self): assert TL_DIM_2 == LAM
    def test_tl3_eig_max(self): assert TL_DIM_3 == EIG_MAX
    def test_tl3_value(self): assert TL_DIM_3 == 5
    def test_tl_q_flag(self): assert TL_Q_DIM_IS_EIG_MAX is True
    def test_tl_lam_flag(self): assert TL_LAM_DIM_IS_LAM is True
    def test_tl5_value(self): assert TL_DIM_5 == 42


class TestGarside:
    def test_garside_b3_q(self): assert GARSIDE_B3 == Q
    def test_garside_b3_value(self): assert GARSIDE_B3 == 3
    def test_garside_b5_phi4(self): assert GARSIDE_B5 == PHI4
    def test_garside_b5_value(self): assert GARSIDE_B5 == 10
    def test_garside_b3_flag(self): assert GARSIDE_B3_IS_Q is True
    def test_garside_b5_flag(self): assert GARSIDE_B5_IS_PHI4 is True
    def test_garside_b3_sq(self): assert GARSIDE_B3_SQ_LENGTH == MULT_K2
    def test_garside_b3_sq_flag(self): assert GARSIDE_B3_SQ_IS_MULT_K2 is True
    def test_garside_b8_value(self): assert GARSIDE_B8 == 28
    def test_garside_b12_value(self): assert GARSIDE_B12 == 66


class TestStructural:
    def test_perm_b3_mult_k2(self): assert PERM_BRAIDS_B3 == MULT_K2
    def test_perm_b3_value(self): assert PERM_BRAIDS_B3 == 6
    def test_perm_b3_flag(self): assert PERM_BRAIDS_B3_IS_MULT_K2 is True
    def test_perm_b5_value(self): assert PERM_BRAIDS_B5 == 120
    def test_torus_index_q(self): assert TORUS_T3_K == Q
    def test_torus_index_value(self): assert TORUS_T3_K == 3
    def test_torus_flag(self): assert TORUS_T3_12_IS_Q is True
    def test_braid_rels_b3(self): assert BRAID_RELS_B3 == 1
    def test_comm_rels_b3(self): assert COMM_RELS_B3 == 0
    def test_rels_correct_flag(self): assert BRAID_RELS_B3_CORRECT is True


class TestBraidCheck:
    def test_exact_pass(self):
        c = BraidCheck("t", "d", 5, 5)
        assert c.passes

    def test_exact_fail(self):
        c = BraidCheck("t", "d", 4, 5)
        assert not c.passes

    def test_inexact_pass(self):
        c = BraidCheck("t", "d", 1.0 + 1e-12, 1.0, exact=False)
        assert c.passes

    def test_inexact_fail(self):
        c = BraidCheck("t", "d", 1.0 + 1e-9, 1.0, exact=False)
        assert not c.passes

    def test_frozen(self):
        c = BraidCheck("t", "d", 1, 1)
        with pytest.raises((AttributeError, TypeError)):
            c.name = "x"  # type: ignore[misc]


class TestCheckFactories:
    def test_atom_count(self): assert len(_make_atom_checks()) == 9
    def test_atom_all_pass(self): assert all(c.passes for c in _make_atom_checks())
    def test_generator_count(self): assert len(_make_generator_checks()) == 9
    def test_generator_all_pass(self): assert all(c.passes for c in _make_generator_checks())
    def test_burau_count(self): assert len(_make_burau_checks()) == 6
    def test_burau_all_pass(self): assert all(c.passes for c in _make_burau_checks())
    def test_catalan_count(self): assert len(_make_catalan_checks()) == 6
    def test_catalan_all_pass(self): assert all(c.passes for c in _make_catalan_checks())
    def test_garside_count(self): assert len(_make_garside_checks()) == 8
    def test_garside_all_pass(self): assert all(c.passes for c in _make_garside_checks())
    def test_structural_count(self): assert len(_make_structural_checks()) == 10
    def test_structural_all_pass(self): assert all(c.passes for c in _make_structural_checks())


class TestAudit:
    def setup_method(self):
        self.result = braid_groups_bridge_audit()

    def test_status_pass(self): assert self.result["status"] == "PASS"
    def test_all_pass(self): assert self.result["all_checks_pass"] is True
    def test_no_failed(self): assert self.result["failed_checks"] == []
    def test_check_count(self): assert self.result["check_count"] == 48
    def test_checks_passing(self): assert self.result["checks_passing"] == 48

    def test_garside_lengths(self):
        g = self.result["garside_lengths"]
        assert g["B3"] == 3 and g["B5"] == 10 and g["B8"] == 28 and g["B12"] == 66

    def test_tl_dims(self):
        t = self.result["tl_dimensions"]
        assert t["TL2"] == 2 and t["TL3"] == 5 and t["TL5"] == 42

    def test_atoms_present(self):
        a = self.result["w33_atoms"]
        assert a["Q"] == 3 and a["EDGES"] == 240

    def test_theorem_key(self): assert "theorem_cc" in self.result

    def test_category_counts(self):
        c = self.result["category_counts"]
        assert c["atom_checks"] == 9
        assert c["generator_checks"] == 9
        assert c["burau_checks"] == 6
        assert c["catalan_checks"] == 6
        assert c["garside_checks"] == 8
        assert c["structural_checks"] == 10
