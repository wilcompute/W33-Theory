"""
Tests for PART_CCV: Tropical Geometry Bridge
=============================================
Regression tests for W(3,3) atom, tropical curve, Grassmannian,
Newton polytopes, moduli, Hurwitz numbers, fans/matroids,
Jacobian, and structural checks.
"""

import pytest

from PART_CCV_TROPICAL_BRIDGE import (
    Q, LAM, V, K, PHI3, PHI4, PHI6, J_INV, EDGES, EIG_MAX, MULT_K2, LEECH_DIM,
    TROP_GENUS, TROP_GENUS_IS_B1, TROP_EULER, TROP_EULER_IS_VE,
    TROP_RH_D, TROP_RH_G, TROP_RH_R, TROP_RH_R_IS_2G4,
    TROP_G2_N, TROP_G2_DIM, TROP_G2_DIM_IS_MULT,
    DOUBLE_FAC, DOUBLE_FAC_IS_EQ, DOUBLE_FAC_IS_PHI3_LAM_SUM,
    NEWTON_DEG, NEWTON_VARS, NEWTON_VERTS, NEWTON_VERTS_IS_EIG1,
    NEWTON_LPTS, NEWTON_LPTS_IS_PHI4, MIXED_VOL, MIXED_VOL_IS_LAM,
    BEZOUT, BEZOUT_IS_QSQ,
    MOD_G, MOD_N, MOD_DIM, MOD_DIM_IS_MULT,
    TRIV_TREE_EDGES, TRIV_TREE_IS_LAM,
    MOD2_G, MOD2_N, MOD2_DIM, MOD2_DIM_IS_VL,
    HURWITZ_VAL, HURWITZ_IS_Q, HURWITZ_G1, HURWITZ_G1_IS_K,
    SEC_FAN_CONES, SEC_FAN_IS_JL, SEC_FAN_RAYS, SEC_FAN_RAYS_IS_MULT,
    BERG_BASES, BERG_BASES_IS_PHI4, BERG_FLATS1, BERG_FLATS1_IS_EIG,
    BERG_FTOT, BERG_FTOT_IS_EQ,
    JAC_DIM, JAC_DIM_IS_B1, JAC_PERIOD_MOD, JAC_PERIOD_MOD_IS_Q4,
    TropCheck,
    _make_atom_checks, _make_tropical_curve_checks, _make_grassmannian_checks,
    _make_newton_checks, _make_moduli_checks, _make_hurwitz_checks,
    _make_fan_checks, _make_jacobian_checks, _make_structural_checks,
    tropical_bridge_audit,
)


class TestAtoms:
    def test_Q(self): assert Q == 3
    def test_LAM(self): assert LAM == 2
    def test_V(self): assert V == 40
    def test_K(self): assert K == 12
    def test_EIG_MAX(self): assert EIG_MAX == 5
    def test_MULT_K2(self): assert MULT_K2 == 6
    def test_EDGES(self): assert EDGES == 240
    def test_PHI4(self): assert PHI4 == 10
    def test_LEECH_DIM(self): assert LEECH_DIM == 24


class TestTropicalCurve:
    def test_trop_genus(self): assert TROP_GENUS == 201
    def test_trop_genus_formula(self): assert TROP_GENUS == EDGES - V + 1
    def test_trop_genus_flag(self): assert TROP_GENUS_IS_B1 is True
    def test_trop_euler(self): assert TROP_EULER == -200
    def test_trop_euler_formula(self): assert TROP_EULER == V - EDGES
    def test_trop_euler_flag(self): assert TROP_EULER_IS_VE is True
    def test_rh_d(self): assert TROP_RH_D == Q
    def test_rh_g(self): assert TROP_RH_G == 201
    def test_rh_r(self): assert TROP_RH_R == 406
    def test_rh_r_formula(self): assert TROP_RH_R == 2 * TROP_GENUS + 4
    def test_rh_flag(self): assert TROP_RH_R_IS_2G4 is True


class TestGrassmannian:
    def test_g2n(self): assert TROP_G2_N == EIG_MAX
    def test_g2_dim(self): assert TROP_G2_DIM == MULT_K2
    def test_g2_dim_value(self): assert TROP_G2_DIM == 6
    def test_g2_dim_flag(self): assert TROP_G2_DIM_IS_MULT is True
    def test_double_fac(self): assert DOUBLE_FAC == 15
    def test_double_fac_eq(self): assert DOUBLE_FAC == EIG_MAX * Q
    def test_double_fac_flag(self): assert DOUBLE_FAC_IS_EQ is True
    def test_double_fac_phi3_lam(self): assert DOUBLE_FAC == PHI3 + LAM
    def test_double_fac_phi3_flag(self): assert DOUBLE_FAC_IS_PHI3_LAM_SUM is True


class TestNewtonPolytope:
    def test_newton_deg(self): assert NEWTON_DEG == Q
    def test_newton_vars(self): assert NEWTON_VARS == LAM
    def test_newton_verts(self): assert NEWTON_VERTS == 4
    def test_newton_verts_eig1(self): assert NEWTON_VERTS == EIG_MAX - 1
    def test_newton_verts_flag(self): assert NEWTON_VERTS_IS_EIG1 is True
    def test_newton_lpts(self): assert NEWTON_LPTS == PHI4
    def test_newton_lpts_value(self): assert NEWTON_LPTS == 10
    def test_newton_lpts_flag(self): assert NEWTON_LPTS_IS_PHI4 is True
    def test_mixed_vol(self): assert MIXED_VOL == LAM
    def test_mixed_vol_flag(self): assert MIXED_VOL_IS_LAM is True
    def test_bezout(self): assert BEZOUT == Q * Q
    def test_bezout_value(self): assert BEZOUT == 9
    def test_bezout_flag(self): assert BEZOUT_IS_QSQ is True


class TestModuli:
    def test_mod_g(self): assert MOD_G == LAM
    def test_mod_n(self): assert MOD_N == Q
    def test_mod_dim(self): assert MOD_DIM == MULT_K2
    def test_mod_dim_value(self): assert MOD_DIM == 6
    def test_mod_dim_flag(self): assert MOD_DIM_IS_MULT is True
    def test_triv_tree_edges(self): assert TRIV_TREE_EDGES == LAM
    def test_triv_flag(self): assert TRIV_TREE_IS_LAM is True
    def test_mod2_g(self): assert MOD2_G == MULT_K2
    def test_mod2_n(self): assert MOD2_N == EIG_MAX
    def test_mod2_dim(self): assert MOD2_DIM == V // LAM
    def test_mod2_dim_value(self): assert MOD2_DIM == 20
    def test_mod2_flag(self): assert MOD2_DIM_IS_VL is True


class TestHurwitz:
    def test_hw_val(self): assert HURWITZ_VAL == Q
    def test_hw_flag(self): assert HURWITZ_IS_Q is True
    def test_hw_g1(self): assert HURWITZ_G1 == K
    def test_hw_g1_value(self): assert HURWITZ_G1 == 12
    def test_hw_g1_flag(self): assert HURWITZ_G1_IS_K is True
    def test_hw_product(self): assert HURWITZ_VAL * HURWITZ_G1 == Q * K


class TestFansMatroids:
    def test_sec_cones(self): assert SEC_FAN_CONES == 16
    def test_sec_cones_formula(self): assert SEC_FAN_CONES == (Q + 1) ** (Q - 1)
    def test_sec_jl(self): assert SEC_FAN_IS_JL is True
    def test_sec_rays(self): assert SEC_FAN_RAYS == MULT_K2
    def test_sec_rays_value(self): assert SEC_FAN_RAYS == 6
    def test_sec_rays_flag(self): assert SEC_FAN_RAYS_IS_MULT is True
    def test_berg_bases(self): assert BERG_BASES == PHI4
    def test_berg_bases_value(self): assert BERG_BASES == 10
    def test_berg_bases_flag(self): assert BERG_BASES_IS_PHI4 is True
    def test_berg_flats(self): assert BERG_FLATS1 == EIG_MAX
    def test_berg_flats_flag(self): assert BERG_FLATS1_IS_EIG is True
    def test_berg_ftot(self): assert BERG_FTOT == EIG_MAX * Q
    def test_berg_ftot_value(self): assert BERG_FTOT == 15
    def test_berg_ftot_flag(self): assert BERG_FTOT_IS_EQ is True


class TestJacobian:
    def test_jac_dim(self): assert JAC_DIM == 201
    def test_jac_b1(self): assert JAC_DIM_IS_B1 is True
    def test_jac_period_mod(self): assert JAC_PERIOD_MOD == 81
    def test_jac_q4(self): assert JAC_PERIOD_MOD == Q ** 4
    def test_jac_q4_flag(self): assert JAC_PERIOD_MOD_IS_Q4 is True


class TestStructural:
    def test_euler_betti(self): assert V - EDGES == 1 - TROP_GENUS
    def test_genus_from_euler(self): assert 1 - TROP_EULER == TROP_GENUS
    def test_lpts_comb(self): assert NEWTON_LPTS == PHI4
    def test_k_phi4(self): assert K + PHI4 == LAM * 11
    def test_mod_dim_rel(self): assert MOD_DIM == MULT_K2
    def test_df_eq(self): assert DOUBLE_FAC == EIG_MAX * Q
    def test_sec_cones_j(self): assert SEC_FAN_CONES == J_INV * LAM
    def test_berg_lam(self): assert BERG_BASES == PHI4
    def test_hw_product_rel(self): assert HURWITZ_VAL * HURWITZ_G1 == Q * K
    def test_mod2_dim_v(self): assert MOD2_DIM == V // LAM


class TestTropCheck:
    def test_exact_pass(self):
        c = TropCheck("t", "d", 7, 7)
        assert c.passes

    def test_exact_fail(self):
        c = TropCheck("t", "d", 6, 7)
        assert not c.passes

    def test_inexact_pass(self):
        c = TropCheck("t", "d", 1.0 + 1e-12, 1.0, exact=False)
        assert c.passes

    def test_inexact_fail(self):
        c = TropCheck("t", "d", 1.0 + 1e-9, 1.0, exact=False)
        assert not c.passes

    def test_frozen(self):
        c = TropCheck("t", "d", 1, 1)
        with pytest.raises((AttributeError, TypeError)):
            c.name = "x"  # type: ignore[misc]


class TestCheckFactories:
    def test_atom_count(self): assert len(_make_atom_checks()) == 9
    def test_atom_all_pass(self): assert all(c.passes for c in _make_atom_checks())
    def test_curve_count(self): assert len(_make_tropical_curve_checks()) == 8
    def test_curve_all_pass(self): assert all(c.passes for c in _make_tropical_curve_checks())
    def test_grass_count(self): assert len(_make_grassmannian_checks()) == 6
    def test_grass_all_pass(self): assert all(c.passes for c in _make_grassmannian_checks())
    def test_newton_count(self): assert len(_make_newton_checks()) == 10
    def test_newton_all_pass(self): assert all(c.passes for c in _make_newton_checks())
    def test_moduli_count(self): assert len(_make_moduli_checks()) == 10
    def test_moduli_all_pass(self): assert all(c.passes for c in _make_moduli_checks())
    def test_hurwitz_count(self): assert len(_make_hurwitz_checks()) == 4
    def test_hurwitz_all_pass(self): assert all(c.passes for c in _make_hurwitz_checks())
    def test_fan_count(self): assert len(_make_fan_checks()) == 9
    def test_fan_all_pass(self): assert all(c.passes for c in _make_fan_checks())
    def test_jac_count(self): assert len(_make_jacobian_checks()) == 4
    def test_jac_all_pass(self): assert all(c.passes for c in _make_jacobian_checks())
    def test_structural_count(self): assert len(_make_structural_checks()) == 10
    def test_structural_all_pass(self): assert all(c.passes for c in _make_structural_checks())


class TestAudit:
    def setup_method(self):
        self.result = tropical_bridge_audit()

    def test_status_pass(self): assert self.result["status"] == "PASS"
    def test_all_pass(self): assert self.result["all_checks_pass"] is True
    def test_no_failed(self): assert self.result["failed_checks"] == []
    def test_check_count(self): assert self.result["check_count"] == 70
    def test_checks_passing(self): assert self.result["checks_passing"] == 70

    def test_trop_invariants(self):
        ti = self.result["tropical_invariants"]
        assert ti["trop_genus"] == 201
        assert ti["trop_euler"] == -200
        assert ti["tg2_dim"] == 6
        assert ti["newton_lpts"] == 10

    def test_atoms_present(self):
        a = self.result["w33_atoms"]
        assert a["Q"] == 3 and a["V"] == 40

    def test_theorem_key(self): assert "theorem_ccv" in self.result

    def test_category_counts(self):
        c = self.result["category_counts"]
        assert c["atom_checks"] == 9
        assert c["hurwitz"] == 4
        assert c["structural"] == 10
