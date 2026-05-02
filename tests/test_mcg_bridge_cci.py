"""
Tests for PART_CCI: Mapping Class Groups Bridge
================================================
Regression tests for atom, homology, DLH, SL(2,Z), Teichmüller, and structural checks.
"""

import math
import pytest

from PART_CCI_MCG_BRIDGE import (
    Q, LAM, V, K, PHI3, PHI4, PHI6, J_INV, EDGES, EIG_MAX, MULT_K2, LEECH_DIM,
    GENUS_1, GENUS_LAM, GENUS_Q, GENUS_HALF_K,
    homology_dim, HOMOLOGY_DIM_G1, HOMOLOGY_DIM_G2, HOMOLOGY_DIM_G3,
    HOMOLOGY_G1_IS_LAM, HOMOLOGY_G3_IS_MULT_K2,
    dlh_generators, DLH_G1, DLH_G2, DLH_G3, DLH_G6,
    DLH_G1_IS_Q, DLH_G2_IS_EIG_MAX, DLH_G3_IS_PHI6, DLH_G6_IS_PHI3,
    SL2Z_ORDER_S, SL2Z_ORDER_ST, SL2Z_S_IS_LAM_SQ, SL2Z_ST_IS_MULT_K2,
    teich_real_dim, teich_complex_dim,
    TEICH_DIM_G1, TEICH_DIM_G2, TEICH_DIM_G3, TEICH_DIM_G5,
    TEICH_G1_IS_LAM, TEICH_G2_IS_MULT_K2, TEICH_G3_IS_K, TEICH_G5_IS_LEECH,
    TEICH_COMPLEX_DIM_G2, TEICH_COMPLEX_G2_IS_Q,
    sp_dim, SP_DIM_G1, SP_DIM_G3, SP_DIM_G6,
    SP_DIM_G1_IS_LAM, SP_DIM_G3_IS_MULT_K2, SP_DIM_G6_IS_K,
    EULER_CHAR_M1_DEN, EULER_CHAR_M1,
    PANTS_CURVES_G2, PANTS_CURVES_G3, PANTS_CURVES_G5,
    PANTS_G2_IS_Q, PANTS_G3_IS_MULT_K2, PANTS_G5_IS_K,
    MCGCheck,
    _make_atom_checks, _make_homology_checks, _make_dlh_checks,
    _make_sl2z_checks, _make_teich_checks, _make_structural_checks,
    mcg_bridge_audit,
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


class TestHomology:
    def test_hom_g1_lam(self): assert HOMOLOGY_DIM_G1 == LAM
    def test_hom_g1_value(self): assert HOMOLOGY_DIM_G1 == 2
    def test_hom_g2_lam_sq(self): assert HOMOLOGY_DIM_G2 == LAM**2
    def test_hom_g3_mult_k2(self): assert HOMOLOGY_DIM_G3 == MULT_K2
    def test_hom_g1_flag(self): assert HOMOLOGY_G1_IS_LAM is True
    def test_hom_g3_flag(self): assert HOMOLOGY_G3_IS_MULT_K2 is True
    def test_homology_fn(self): assert homology_dim(5) == 10


class TestDLH:
    def test_dlh_g1_q(self): assert DLH_G1 == Q
    def test_dlh_g1_value(self): assert DLH_G1 == 3
    def test_dlh_g2_eig(self): assert DLH_G2 == EIG_MAX
    def test_dlh_g2_value(self): assert DLH_G2 == 5
    def test_dlh_g3_phi6(self): assert DLH_G3 == PHI6
    def test_dlh_g3_value(self): assert DLH_G3 == 7
    def test_dlh_g6_phi3(self): assert DLH_G6 == PHI3
    def test_dlh_g1_flag(self): assert DLH_G1_IS_Q is True
    def test_dlh_g2_flag(self): assert DLH_G2_IS_EIG_MAX is True
    def test_dlh_g3_flag(self): assert DLH_G3_IS_PHI6 is True
    def test_dlh_g6_flag(self): assert DLH_G6_IS_PHI3 is True
    def test_dlh_fn(self): assert dlh_generators(4) == 9


class TestSL2Z:
    def test_s_order_lam_sq(self): assert SL2Z_ORDER_S == LAM**2
    def test_s_order_value(self): assert SL2Z_ORDER_S == 4
    def test_st_order_mult_k2(self): assert SL2Z_ORDER_ST == MULT_K2
    def test_st_order_value(self): assert SL2Z_ORDER_ST == 6
    def test_s_flag(self): assert SL2Z_S_IS_LAM_SQ is True
    def test_st_flag(self): assert SL2Z_ST_IS_MULT_K2 is True


class TestTeich:
    def test_g1_lam(self): assert TEICH_DIM_G1 == LAM
    def test_g2_mult_k2(self): assert TEICH_DIM_G2 == MULT_K2
    def test_g2_value(self): assert TEICH_DIM_G2 == 6
    def test_g3_k(self): assert TEICH_DIM_G3 == K
    def test_g3_value(self): assert TEICH_DIM_G3 == 12
    def test_g5_leech(self): assert TEICH_DIM_G5 == LEECH_DIM
    def test_g5_value(self): assert TEICH_DIM_G5 == 24
    def test_g1_flag(self): assert TEICH_G1_IS_LAM is True
    def test_g2_flag(self): assert TEICH_G2_IS_MULT_K2 is True
    def test_g3_flag(self): assert TEICH_G3_IS_K is True
    def test_g5_flag(self): assert TEICH_G5_IS_LEECH is True
    def test_complex_g2_q(self): assert TEICH_COMPLEX_DIM_G2 == Q
    def test_complex_g2_flag(self): assert TEICH_COMPLEX_G2_IS_Q is True


class TestStructural:
    def test_sp_g1_lam(self): assert SP_DIM_G1 == LAM
    def test_sp_g3_mult_k2(self): assert SP_DIM_G3 == MULT_K2
    def test_sp_g6_k(self): assert SP_DIM_G6 == K
    def test_sp_g1_flag(self): assert SP_DIM_G1_IS_LAM is True
    def test_sp_g3_flag(self): assert SP_DIM_G3_IS_MULT_K2 is True
    def test_sp_g6_flag(self): assert SP_DIM_G6_IS_K is True
    def test_euler_den(self): assert EULER_CHAR_M1_DEN == K
    def test_euler_value(self): assert abs(EULER_CHAR_M1 - (-1/12)) < 1e-12
    def test_pants_g2(self): assert PANTS_CURVES_G2 == Q
    def test_pants_g3(self): assert PANTS_CURVES_G3 == MULT_K2
    def test_pants_g5(self): assert PANTS_CURVES_G5 == K
    def test_pants_g2_flag(self): assert PANTS_G2_IS_Q is True
    def test_pants_g3_flag(self): assert PANTS_G3_IS_MULT_K2 is True
    def test_pants_g5_flag(self): assert PANTS_G5_IS_K is True


class TestMCGCheck:
    def test_exact_pass(self):
        c = MCGCheck("t", "d", 7, 7)
        assert c.passes

    def test_exact_fail(self):
        c = MCGCheck("t", "d", 6, 7)
        assert not c.passes

    def test_inexact_pass(self):
        c = MCGCheck("t", "d", 1.0 + 1e-12, 1.0, exact=False)
        assert c.passes

    def test_inexact_fail(self):
        c = MCGCheck("t", "d", 1.0 + 1e-9, 1.0, exact=False)
        assert not c.passes

    def test_frozen(self):
        c = MCGCheck("t", "d", 1, 1)
        with pytest.raises((AttributeError, TypeError)):
            c.name = "x"  # type: ignore[misc]


class TestCheckFactories:
    def test_atom_count(self): assert len(_make_atom_checks()) == 9
    def test_atom_all_pass(self): assert all(c.passes for c in _make_atom_checks())
    def test_homology_count(self): assert len(_make_homology_checks()) == 6
    def test_homology_all_pass(self): assert all(c.passes for c in _make_homology_checks())
    def test_dlh_count(self): assert len(_make_dlh_checks()) == 8
    def test_dlh_all_pass(self): assert all(c.passes for c in _make_dlh_checks())
    def test_sl2z_count(self): assert len(_make_sl2z_checks()) == 6
    def test_sl2z_all_pass(self): assert all(c.passes for c in _make_sl2z_checks())
    def test_teich_count(self): assert len(_make_teich_checks()) == 10
    def test_teich_all_pass(self): assert all(c.passes for c in _make_teich_checks())
    def test_structural_count(self): assert len(_make_structural_checks()) == 10
    def test_structural_all_pass(self): assert all(c.passes for c in _make_structural_checks())


class TestAudit:
    def setup_method(self):
        self.result = mcg_bridge_audit()

    def test_status_pass(self): assert self.result["status"] == "PASS"
    def test_all_pass(self): assert self.result["all_checks_pass"] is True
    def test_no_failed(self): assert self.result["failed_checks"] == []
    def test_check_count(self): assert self.result["check_count"] == 49
    def test_checks_passing(self): assert self.result["checks_passing"] == 49

    def test_teich_dims(self):
        t = self.result["teichmuller_dims"]
        assert t["genus_2"] == 6 and t["genus_3"] == 12 and t["genus_5"] == 24

    def test_dlh_gens(self):
        d = self.result["dlh_generators"]
        assert d["genus_1"] == 3 and d["genus_2"] == 5

    def test_atoms_present(self):
        a = self.result["w33_atoms"]
        assert a["Q"] == 3 and a["EDGES"] == 240

    def test_theorem_key(self): assert "theorem_cci" in self.result

    def test_category_counts(self):
        c = self.result["category_counts"]
        assert c["atom_checks"] == 9
        assert c["homology_checks"] == 6
        assert c["dlh_checks"] == 8
        assert c["sl2z_checks"] == 6
        assert c["teich_checks"] == 10
        assert c["structural_checks"] == 10
