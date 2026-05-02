"""
Tests for PART_CCIV: Topological Data Analysis Bridge
======================================================
Regression tests for atom, graph homology, clique complex,
neighbourhood complex, barcodes, nerve, and structural checks.
"""

import pytest

from PART_CCIV_TDA_BRIDGE import (
    Q, LAM, V, K, PHI3, PHI4, PHI6, J_INV, EDGES, EIG_MAX, MULT_K2, LEECH_DIM,
    BETTI_0, BETTI_1, EULER_GRAPH, EULER_GRAPH_NEG,
    EULER_IS_V_EIG, EULER_IS_NEG,
    EDGES_COMPUTED, EDGES_IS_ATOM,
    CYCLE_RANK, CYCLE_IS_BETTI1,
    TRIANGLES, TRIANGLES_IS_EIG1_V,
    EULER_CLIQUE, EULER_CLIQUE_NEG, EULER_CLIQUE_IS_NEG_V,
    BETTI0_R0, MERGES_R1, MERGES_IS_PHI3Q,
    NBHD_VERTICES, NBHD_EDGES, NBHD_EDGE_IS_K,
    NBHD_TOT_DEG, NBHD_TOT_IS_LEECH,
    NBHD_COMPONENTS, NBHD_COMP_IS_EIG1,
    NBHD_BETTI0, NBHD_BETTI1,
    H0_FINITE_BARS, H0_INF_BARS, H0_BARS_TOTAL,
    H0_BARS_IS_V, H0_FINITE_PHI3Q,
    H1_BARS_R1, PERS_BORN_0, PERS_KILLED_1,
    COVER_SIZE, COVER_IS_PHI3,
    STAR_INTERSECT, STAR_INT_IS_EIG1,
    TDACheck,
    _make_atom_checks, _make_graph_homology_checks, _make_clique_complex_checks,
    _make_neighbourhood_checks, _make_barcode_checks,
    _make_nerve_checks, _make_structural_checks,
    tda_bridge_audit,
)


class TestAtoms:
    def test_Q(self): assert Q == 3
    def test_LAM(self): assert LAM == 2
    def test_V(self): assert V == 40
    def test_K(self): assert K == 12
    def test_EIG_MAX(self): assert EIG_MAX == 5
    def test_MULT_K2(self): assert MULT_K2 == 6
    def test_EDGES(self): assert EDGES == 240
    def test_PHI3(self): assert PHI3 == 13
    def test_LEECH_DIM(self): assert LEECH_DIM == 24


class TestGraphHomology:
    def test_betti0(self): assert BETTI_0 == 1
    def test_edges_computed(self): assert EDGES_COMPUTED == 240
    def test_edges_is_atom(self): assert EDGES_IS_ATOM is True
    def test_euler_graph(self): assert EULER_GRAPH == -200
    def test_euler_neg(self): assert EULER_GRAPH_NEG == V * EIG_MAX
    def test_euler_neg_value(self): assert EULER_GRAPH_NEG == 200
    def test_euler_flag(self): assert EULER_IS_V_EIG is True
    def test_betti1_value(self): assert BETTI_1 == 201
    def test_cycle_rank(self): assert CYCLE_RANK == 201
    def test_cycle_rank_formula(self): assert CYCLE_RANK == EDGES - V + 1
    def test_cycle_betti_flag(self): assert CYCLE_IS_BETTI1 is True


class TestCliqueComplex:
    def test_triangles(self): assert TRIANGLES == 160
    def test_triangles_formula(self): assert TRIANGLES == EDGES * LAM // Q
    def test_triangles_eig1_v(self): assert TRIANGLES == (EIG_MAX - 1) * V
    def test_triangles_flag(self): assert TRIANGLES_IS_EIG1_V is True
    def test_euler_clique(self): assert EULER_CLIQUE == -V
    def test_euler_clique_value(self): assert EULER_CLIQUE == -40
    def test_euler_clique_neg(self): assert EULER_CLIQUE_NEG == V
    def test_euler_clique_flag(self): assert EULER_CLIQUE_IS_NEG_V is True
    def test_betti0_r0(self): assert BETTI0_R0 == V
    def test_merges_r1(self): assert MERGES_R1 == 39
    def test_merges_phi3q(self): assert MERGES_R1 == PHI3 * Q
    def test_merges_flag(self): assert MERGES_IS_PHI3Q is True


class TestNeighbourhood:
    def test_nbhd_vertices(self): assert NBHD_VERTICES == K
    def test_nbhd_edges(self): assert NBHD_EDGES == K
    def test_nbhd_edges_value(self): assert NBHD_EDGES == 12
    def test_nbhd_edge_flag(self): assert NBHD_EDGE_IS_K is True
    def test_nbhd_tot_deg(self): assert NBHD_TOT_DEG == LEECH_DIM
    def test_nbhd_leech_flag(self): assert NBHD_TOT_IS_LEECH is True
    def test_nbhd_components(self): assert NBHD_COMPONENTS == 4
    def test_nbhd_comp_eig1(self): assert NBHD_COMPONENTS == EIG_MAX - 1
    def test_nbhd_comp_flag(self): assert NBHD_COMP_IS_EIG1 is True
    def test_nbhd_betti0(self): assert NBHD_BETTI0 == 4
    def test_nbhd_betti1(self): assert NBHD_BETTI1 == 4


class TestBarcodes:
    def test_h0_finite(self): assert H0_FINITE_BARS == 39
    def test_h0_finite_phi3q(self): assert H0_FINITE_BARS == PHI3 * Q
    def test_h0_inf(self): assert H0_INF_BARS == 1
    def test_h0_total(self): assert H0_BARS_TOTAL == V
    def test_h0_bars_v_flag(self): assert H0_BARS_IS_V is True
    def test_h0_phi3q_flag(self): assert H0_FINITE_PHI3Q is True
    def test_h1_bars(self): assert H1_BARS_R1 == 201
    def test_pers_born(self): assert PERS_BORN_0 == V
    def test_pers_killed(self): assert PERS_KILLED_1 == 39


class TestNerve:
    def test_cover_size(self): assert COVER_SIZE == PHI3
    def test_cover_value(self): assert COVER_SIZE == 13
    def test_cover_phi3_flag(self): assert COVER_IS_PHI3 is True
    def test_star_intersect(self): assert STAR_INTERSECT == EIG_MAX - 1
    def test_star_intersect_value(self): assert STAR_INTERSECT == 4
    def test_star_eig1_flag(self): assert STAR_INT_IS_EIG1 is True


class TestStructural:
    def test_euler_betti_relation(self): assert V - EDGES == BETTI_0 - BETTI_1
    def test_tri_edges_ratio(self): assert TRIANGLES * Q == EDGES * LAM
    def test_euler_sum(self): assert EULER_CLIQUE + EULER_GRAPH == -EDGES
    def test_nbhd_euler_zero(self): assert NBHD_VERTICES - NBHD_EDGES == 0
    def test_k_phi3_sq(self): assert K + PHI3 == EIG_MAX * EIG_MAX
    def test_cycle_plus_v(self): assert CYCLE_RANK + V == EDGES + 1
    def test_bars_sum(self): assert H0_FINITE_BARS + H0_INF_BARS == V
    def test_tri_j_inv(self): assert TRIANGLES == J_INV * (V // LAM)
    def test_betti_diff(self): assert BETTI_1 - BETTI_0 == V * EIG_MAX


class TestTDACheck:
    def test_exact_pass(self):
        c = TDACheck("t", "d", 5, 5)
        assert c.passes

    def test_exact_fail(self):
        c = TDACheck("t", "d", 4, 5)
        assert not c.passes

    def test_inexact_pass(self):
        c = TDACheck("t", "d", 1.0 + 1e-12, 1.0, exact=False)
        assert c.passes

    def test_inexact_fail(self):
        c = TDACheck("t", "d", 1.0 + 1e-9, 1.0, exact=False)
        assert not c.passes

    def test_frozen(self):
        c = TDACheck("t", "d", 1, 1)
        with pytest.raises((AttributeError, TypeError)):
            c.name = "x"  # type: ignore[misc]


class TestCheckFactories:
    def test_atom_count(self): assert len(_make_atom_checks()) == 9
    def test_atom_all_pass(self): assert all(c.passes for c in _make_atom_checks())
    def test_graph_count(self): assert len(_make_graph_homology_checks()) == 9
    def test_graph_all_pass(self): assert all(c.passes for c in _make_graph_homology_checks())
    def test_clique_count(self): assert len(_make_clique_complex_checks()) == 8
    def test_clique_all_pass(self): assert all(c.passes for c in _make_clique_complex_checks())
    def test_nbhd_count(self): assert len(_make_neighbourhood_checks()) == 9
    def test_nbhd_all_pass(self): assert all(c.passes for c in _make_neighbourhood_checks())
    def test_barcode_count(self): assert len(_make_barcode_checks()) == 8
    def test_barcode_all_pass(self): assert all(c.passes for c in _make_barcode_checks())
    def test_nerve_count(self): assert len(_make_nerve_checks()) == 4
    def test_nerve_all_pass(self): assert all(c.passes for c in _make_nerve_checks())
    def test_structural_count(self): assert len(_make_structural_checks()) == 10
    def test_structural_all_pass(self): assert all(c.passes for c in _make_structural_checks())


class TestAudit:
    def setup_method(self):
        self.result = tda_bridge_audit()

    def test_status_pass(self): assert self.result["status"] == "PASS"
    def test_all_pass(self): assert self.result["all_checks_pass"] is True
    def test_no_failed(self): assert self.result["failed_checks"] == []
    def test_check_count(self): assert self.result["check_count"] == 57
    def test_checks_passing(self): assert self.result["checks_passing"] == 57

    def test_betti_numbers(self):
        bn = self.result["betti_numbers"]
        assert bn["beta_0_graph"] == 1
        assert bn["beta_1_graph"] == 201

    def test_euler_chars(self):
        ec = self.result["euler_chars"]
        assert ec["graph"] == -200
        assert ec["clique"] == -40

    def test_simplices(self):
        s = self.result["simplices"]
        assert s["V"] == 40 and s["E"] == 240 and s["T"] == 160

    def test_atoms_present(self):
        a = self.result["w33_atoms"]
        assert a["Q"] == 3 and a["V"] == 40

    def test_theorem_key(self): assert "theorem_cciv" in self.result

    def test_category_counts(self):
        c = self.result["category_counts"]
        assert c["atom_checks"] == 9
        assert c["neighbourhood"] == 9
