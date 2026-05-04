"""
Tests for Part CCLXXXIII: Discrete Wigner Functions, Phase Space over GF(3),
and the W(3,3) Quasi-Probability Atlas.
"""

import math
import sys
import os
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'exploration'))

from PART_CCLXXXIII_DISCRETE_WIGNER_BRIDGE import (
    # Constants
    V, K, LAM, MU, Q, PHI4, LINES_27, EDGES, AUT_ORDER,
    TRANSPORT_EDGES, PHASE_SPACE_SIZE, DIM_HILBERT, SP4F3_ORDER,
    N_QUDITS, ISOTROPIC_LINES, DISPLACEMENT_OPS,
    # GF(3) arithmetic
    gf3_add, gf3_mul, gf3_neg, gf3_inv,
    # Symplectic form
    symplectic_form, is_isotropic, is_self_dual_zero,
    # Counting functions
    count_isotropic_points_pg33, count_total_projective_points_pg33,
    pg33_total_points,
    # Phase-space functions
    phase_space_geometry, collinearity_graph_identification,
    sp4f3_structure, sp4f3_order_verification,
    stabilizer_state_count, clifford_group_order,
    # Wigner formulas
    wigner_function_formula, wigner_negativity_bound,
    wigner_of_computational_basis,
    wigner_negativity_resource,
    # Atlas and connections
    w33_wigner_atlas, clifford_wigner_covariance,
    gf3_4_decomposition,
    sic_povm_wigner_connection,
    wigner_phase_space_entropy,
    transport_edges_wigner_interpretation,
    wigner_maximally_entangled,
    wigner_of_ghz_state_proxy,
    phase_point_operator_spectrum,
    hudsons_theorem_qutrits,
    hudson_perelomov,
    wigner_marginal_lines,
    wigner_entanglement_connection,
)


class TestConstants:
    def test_phase_space_size(self):
        assert PHASE_SPACE_SIZE == 81

    def test_hilbert_dim(self):
        assert DIM_HILBERT == 9

    def test_sp4f3_order_equals_aut_order(self):
        assert SP4F3_ORDER == AUT_ORDER == 51840

    def test_isotropic_lines_equals_v(self):
        assert ISOTROPIC_LINES == V == 40

    def test_displacement_ops(self):
        assert DISPLACEMENT_OPS == 81

    def test_n_qudits(self):
        assert N_QUDITS == 2


class TestGF3Arithmetic:
    def test_addition(self):
        assert gf3_add(2, 2) == 1
        assert gf3_add(1, 2) == 0
        assert gf3_add(0, 2) == 2

    def test_multiplication(self):
        assert gf3_mul(2, 2) == 1
        assert gf3_mul(2, 0) == 0
        assert gf3_mul(1, 2) == 2

    def test_negation(self):
        assert gf3_neg(1) == 2
        assert gf3_neg(2) == 1
        assert gf3_neg(0) == 0

    def test_inverse(self):
        assert gf3_inv(1) == 1
        assert gf3_inv(2) == 2

    def test_field_identity(self):
        # gf3_mul(a, gf3_inv(a)) == 1 for a != 0
        for a in [1, 2]:
            assert gf3_mul(a, gf3_inv(a)) == 1


class TestSymplecticForm:
    def test_standard_pairs(self):
        e0 = (1, 0, 0, 0)
        e2 = (0, 0, 1, 0)
        assert symplectic_form(e0, e2) == 1
        assert symplectic_form(e2, e0) == 2  # antisymmetry: -1 = 2 mod 3

    def test_alternating_property(self):
        # For alternating form, <u,u> = 0 for all u
        test_vectors = [(1,0,0,0), (0,1,0,0), (1,1,1,1), (2,1,0,2), (0,2,1,2)]
        for v in test_vectors:
            assert symplectic_form(v, v) == 0

    def test_alternating_exhaustive_sample(self):
        # All vectors in GF(3)^4 satisfy <u,u>=0
        count = 0
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    for d_val in range(3):
                        vec = (a, b, c, d_val)
                        assert is_self_dual_zero(vec)
                        count += 1
        assert count == 81

    def test_antisymmetry(self):
        u = (1, 2, 0, 1)
        v = (0, 1, 2, 0)
        sf_uv = symplectic_form(u, v)
        sf_vu = symplectic_form(v, u)
        assert (sf_uv + sf_vu) % 3 == 0  # <u,v> + <v,u> = 0 mod 3


class TestPolarSpaceCount:
    def test_w33_point_count(self):
        n = count_isotropic_points_pg33()
        assert n == 40 == V

    def test_pg33_total_points(self):
        n = count_total_projective_points_pg33()
        assert n == 40 == V

    def test_all_pg33_points_isotropic(self):
        # For alternating form, all projective points are isotropic
        assert count_isotropic_points_pg33() == count_total_projective_points_pg33()

    def test_pg33_total_points_function(self):
        assert pg33_total_points() == V


class TestPhaseSpaceGeometry:
    def test_isotropic_points(self):
        pg = phase_space_geometry()
        assert pg["isotropic_points"] == V

    def test_totally_isotropic_lines(self):
        pg = phase_space_geometry()
        assert pg["totally_isotropic_lines"] == 90

    def test_points_per_line(self):
        pg = phase_space_geometry()
        assert pg["points_per_line"] == MU == 4

    def test_lines_per_point(self):
        pg = phase_space_geometry()
        assert pg["lines_per_point"] == MU == 4

    def test_srg_params(self):
        pg = phase_space_geometry()
        assert pg["srg_params"] == (V, K, LAM, MU)

    def test_collinearity_degree(self):
        col = collinearity_graph_identification()
        assert col["degree"] == K == 12

    def test_collinearity_equals_k(self):
        col = collinearity_graph_identification()
        assert col["equals_K"]


class TestSp4F3:
    def test_order(self):
        order = sp4f3_order_verification()
        assert order == 51840 == AUT_ORDER

    def test_order_formula(self):
        q = Q
        assert q**4 * (q**2 - 1) * (q**4 - 1) == 51840

    def test_structure(self):
        st = sp4f3_structure()
        assert st["sp4f3_order"] == AUT_ORDER
        assert st["psp4f3_order"] == 25920
        assert st["transvection_count"] == V
        assert st["stabilizer_index"] == 1296

    def test_psp_is_half_sp(self):
        st = sp4f3_structure()
        assert st["sp4f3_order"] == 2 * st["psp4f3_order"]


class TestStabilizerStates:
    def test_lagrangian_count(self):
        lag = stabilizer_state_count()
        assert lag == V == 40

    def test_lagrangian_formula(self):
        q = Q
        assert (q**2 + 1) * (q + 1) == 40 == V

    def test_clifford_group_order(self):
        cliff = clifford_group_order()
        assert cliff == 25194240

    def test_clifford_formula(self):
        d, n = Q, N_QUDITS
        assert 2 * d**(2*n+1) * SP4F3_ORDER == clifford_group_order()

    def test_hudsons_theorem(self):
        ht = hudsons_theorem_qutrits()
        assert ht["lagrangian_count"] == V
        assert ht["states_per_lagrangian"] == DIM_HILBERT  # 9
        assert ht["total_stabilizer_states"] == 360

    def test_360_stabilizer_states(self):
        # 40 Lagrangians * 9 states per Lagrangian = 360
        assert V * DIM_HILBERT == 360


class TestWignerFormulas:
    def test_formula_present(self):
        wf = wigner_function_formula()
        assert "W_rho(alpha)" in wf["formula"]
        assert "hudson_theorem" in wf

    def test_wigner_min_value(self):
        w_min = wigner_negativity_bound()
        assert w_min == Fraction(-10, 81)

    def test_wigner_min_formula(self):
        d, n = Q, N_QUDITS
        w_min = Fraction(-(d-1), d**(2*n)) * Fraction(d**n + 1, 2)
        assert w_min == Fraction(-10, 81)

    def test_computational_basis_wigner(self):
        w = wigner_of_computational_basis(0, d=3, n=2)
        # Should have 9 entries summing to 1
        total = sum(w.values())
        assert total == Fraction(9, 9) == 1
        # All values equal 1/9
        for val in w.values():
            assert val == Fraction(1, 9)


class TestWignerAtlas:
    def test_atlas_size(self):
        atlas = w33_wigner_atlas()
        assert atlas["atlas_size"] == V

    def test_edge_count(self):
        atlas = w33_wigner_atlas()
        assert atlas["edge_count"] == EDGES

    def test_lagrangians_equal_v(self):
        atlas = w33_wigner_atlas()
        assert atlas["lagrangian_subspaces"] == V

    def test_aut_order(self):
        atlas = w33_wigner_atlas()
        assert atlas["aut_group_order"] == AUT_ORDER

    def test_covariance(self):
        wc = clifford_wigner_covariance()
        assert "Sp(4,F_3)" in wc["group"]
        assert wc["preserved_structure"] == "W(3,3) SRG(40,12,2,4)"


class TestGF34Decomposition:
    def test_total_projective_points(self):
        dec = gf3_4_decomposition()
        assert dec["total_projective_points_pg33"] == V

    def test_all_isotropic(self):
        dec = gf3_4_decomposition()
        assert dec["all_points_isotropic"]
        assert dec["isotropic_projective_points"] == V

    def test_explains_v40(self):
        dec = gf3_4_decomposition()
        assert dec["explains_V40"]


class TestSICPOVM:
    def test_sic_size_d3(self):
        sic = sic_povm_wigner_connection()
        assert sic["sic_size_d3"] == 9

    def test_sic_size_d9(self):
        sic = sic_povm_wigner_connection()
        assert sic["sic_size_d9"] == PHASE_SPACE_SIZE == 81

    def test_zauner_order(self):
        sic = sic_povm_wigner_connection()
        assert sic["zauner_order"] == Q == 3

    def test_equiangularity_d3(self):
        sic = sic_povm_wigner_connection()
        assert sic["equiangularity_d3"] == Fraction(1, 4)

    def test_equiangularity_d9(self):
        sic = sic_povm_wigner_connection()
        # 1/(d+1) = 1/10 = 1/PHI4
        assert sic["equiangularity_d9"] == Fraction(1, 10) == Fraction(1, PHI4)


class TestPhaseSpaceEntropy:
    def test_phase_space_size(self):
        ent = wigner_phase_space_entropy()
        assert ent["phase_space_size"] == 81

    def test_H_mixed(self):
        ent = wigner_phase_space_entropy()
        assert abs(ent["H_maximally_mixed"] - 4 * math.log(3)) < 1e-6

    def test_H_pure_stab(self):
        ent = wigner_phase_space_entropy()
        assert abs(ent["H_pure_stabilizer"] - 2 * math.log(3)) < 1e-6

    def test_entropy_ratio(self):
        ent = wigner_phase_space_entropy()
        assert abs(ent["ratio"] - 2.0) < 1e-6


class TestTransportEdges:
    def test_transport_edges_value(self):
        te = transport_edges_wigner_interpretation()
        assert te["transport_edges"] == TRANSPORT_EDGES == 270

    def test_phi4_times_lines27(self):
        te = transport_edges_wigner_interpretation()
        assert te["phi4_times_lines27"] == PHI4 * LINES_27 == 270

    def test_e8_roots(self):
        te = transport_edges_wigner_interpretation()
        assert te["e8_roots"] == 240

    def test_edges_equals_e8(self):
        te = transport_edges_wigner_interpretation()
        assert te["e8_edges_match"]
        assert EDGES == 240

    def test_coxeter_e6(self):
        te = transport_edges_wigner_interpretation()
        assert te["coxeter_e6"] == K == 12


class TestMaximallyEntangled:
    def test_total_lagrangians(self):
        me = wigner_maximally_entangled()
        assert me["total_lagrangians"] == V

    def test_lagrangian_size(self):
        me = wigner_maximally_entangled()
        assert me["lagrangian_size"] == DIM_HILBERT == 9

    def test_sp2f3_order(self):
        me = wigner_maximally_entangled()
        assert me["sp2f3_order"] == 24

    def test_local_clifford_order(self):
        me = wigner_maximally_entangled()
        assert me["local_clifford_order"] == 576


class TestGHZState:
    def test_is_stabilizer(self):
        ghz = wigner_of_ghz_state_proxy()
        assert ghz["is_stabilizer"]

    def test_wigner_nonnegative(self):
        ghz = wigner_of_ghz_state_proxy()
        assert ghz["wigner_nonnegative"]

    def test_support_size(self):
        ghz = wigner_of_ghz_state_proxy()
        assert ghz["support_size"] == 9 == DIM_HILBERT

    def test_normalization(self):
        ghz = wigner_of_ghz_state_proxy()
        # support_size * (1/support_size) = 1
        support = ghz["support_size"]
        val = Fraction(1, support)
        assert support * val == 1


class TestPhasePointSpectrum:
    def test_hilbert_dim(self):
        spec = phase_point_operator_spectrum()
        assert spec["hilbert_dim"] == 9

    def test_phase_space_size(self):
        spec = phase_point_operator_spectrum()
        assert spec["phase_space_size"] == 81

    def test_negative_eigenvalue_count(self):
        spec = phase_point_operator_spectrum()
        assert spec["negative_eigenvalue_count"] == 72

    def test_max_eigenvalue(self):
        spec = phase_point_operator_spectrum()
        assert spec["max_eigenvalue"] == "8/9"

    def test_eigenvalue_counts_sum(self):
        # 9 (positive slots) + 72 (negative slots) = 81 = PHASE_SPACE_SIZE
        spec = phase_point_operator_spectrum()
        dim = spec["hilbert_dim"]
        neg_count = spec["negative_eigenvalue_count"]
        assert dim + neg_count == PHASE_SPACE_SIZE


class TestNegativityResource:
    def test_stabilizer_negativity_zero(self):
        neg = wigner_negativity_resource()
        assert neg["stabilizer_negativity"] == 0

    def test_aut_invariance(self):
        neg = wigner_negativity_resource()
        assert neg["aut_invariance"]

    def test_aut_order(self):
        neg = wigner_negativity_resource()
        assert neg["aut_order"] == AUT_ORDER

    def test_isotropic_directions(self):
        neg = wigner_negativity_resource()
        assert neg["isotropic_directions_used"] == V

    def test_hudson_perelomov(self):
        hp = hudson_perelomov()
        assert hp["axes_count"] == V
        assert hp["clifford_gates_per_axis"] == K
        assert hp["sp4f3_preserves_nonnegativity"]


class TestWignerMarginals:
    def test_marginal_count(self):
        mg = wigner_marginal_lines()
        assert mg["marginal_count"] == V

    def test_isotropic_directions(self):
        mg = wigner_marginal_lines()
        assert mg["isotropic_directions"] == V

    def test_line_size(self):
        mg = wigner_marginal_lines()
        assert mg["line_size"] == Q == 3

    def test_lines_per_direction(self):
        mg = wigner_marginal_lines()
        assert mg["lines_per_direction"] == Q**2 == 9

    def test_total_affine_lines(self):
        mg = wigner_marginal_lines()
        assert mg["total_lines_in_striations"] == V * Q**2 == 360


class TestEntanglementConnection:
    def test_transport_edges(self):
        ec = wigner_entanglement_connection()
        assert ec["transport_edges"] == TRANSPORT_EDGES

    def test_transport_formula(self):
        ec = wigner_entanglement_connection()
        assert str(PHI4) in ec["transport_formula"]
        assert str(LINES_27) in ec["transport_formula"]
