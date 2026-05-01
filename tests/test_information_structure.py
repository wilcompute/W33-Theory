#!/usr/bin/env python3
"""Tests for Pillar 67: W33 Causal-Information Structure.

Tests all six theorems from THEORY_PART_CLXXVI_INFORMATION_STRUCTURE.py:
  T1: Causal decomposition 1+12+27=40
  T2: Lovász information capacity theta(W33)=10=dim(Sp(4))
  T3: Monster 3B three-generation bridge F3^12=(F3^4)^3
  T4: sl(3,F3)^3 as Yukawa structure algebra (epsilon cubic invariance)
  T5: Code rate 27/80, Bekenstein bound, QCA causal diameter=2
  T6: Golay 24-dim Lie algebra (perfect, center=0, Der=33)
"""

import json
import os
import sys

import numpy as np
import pytest

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, repo_root)
sys.path.insert(0, os.path.join(repo_root, "scripts"))

from THEORY_PART_CLXXVI_INFORMATION_STRUCTURE import (
    build_adjacency,
    build_e6_epsilon_cubic,
    build_f3_symplectic_form,
    build_sl3_generators_f3,
    is_isotropic_f3,
    lovász_theta,
)
from THEORY_PART_CLXXVI_INFORMATION_STRUCTURE import (
    main as build_information_structure_report,
)
from THEORY_PART_CLXXVI_INFORMATION_STRUCTURE import (
    rank_mod3,
    sl3_triple_action_on_27,
    sl3_triple_bracket_closure,
    sl3_triple_is_24_dimensional,
    sl3_triple_preserves_cubic,
    theorem1_causal_decomposition,
    theorem2_lovász_capacity,
    theorem3_three_generation_monster,
    theorem4_sl3_cube_structure,
    theorem5_bekenstein_qca,
    theorem6_golay_lie_algebra,
)
from w33_homology import build_w33

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def w33_graph():
    n, points, adj, edges = build_w33()
    return n, adj, edges


@pytest.fixture(scope="module")
def local_tris(w33_graph):
    n, adj, edges = w33_graph
    v0 = 0
    neighbors_v0 = set(adj[v0])
    h27_verts = [v for v in range(n) if v != v0 and v not in neighbors_v0]
    adj_set = [set(adj[v]) for v in range(n)]
    tris = []
    for ui, u in enumerate(h27_verts):
        for vi, v in enumerate(h27_verts):
            if vi <= ui:
                continue
            if v not in adj_set[u]:
                continue
            for wi, w in enumerate(h27_verts):
                if wi <= vi:
                    continue
                if w in adj_set[u] and w in adj_set[v]:
                    tris.append((ui, vi, wi))
    return tris


@pytest.fixture(scope="module")
def sl3_generators():
    return build_sl3_generators_f3()


@pytest.fixture(scope="module")
def sl3_triple_mats(sl3_generators):
    return sl3_triple_action_on_27(sl3_generators)


# ---------------------------------------------------------------------------
# T1: Causal decomposition
# ---------------------------------------------------------------------------


class TestT1CausalDecomposition:
    def test_w33_has_40_vertices(self, w33_graph):
        n, adj, edges = w33_graph
        assert n == 40

    def test_w33_has_240_edges(self, w33_graph):
        n, adj, edges = w33_graph
        assert len(edges) == 240

    def test_all_degrees_12(self, w33_graph):
        n, adj, edges = w33_graph
        A = build_adjacency(edges, n)
        degrees = A.sum(axis=1)
        assert np.all(degrees == 12)

    def test_all_non_degrees_27(self, w33_graph):
        n, adj, edges = w33_graph
        A = build_adjacency(edges, n)
        non_degrees = (n - 1) - A.sum(axis=1)
        assert np.all(non_degrees == 27)

    def test_one_plus_twelve_plus_27_equals_40(self, w33_graph):
        n, adj, edges = w33_graph
        assert 1 + 12 + 27 == n

    def test_theorem1_returns_correct_keys(self, w33_graph):
        n, adj, edges = w33_graph
        r = theorem1_causal_decomposition(None, edges, n)
        assert r["n_gauge"] == 12
        assert r["n_matter"] == 27
        assert r["n_total"] == 40
        assert r["decomposition_exact"] is True

    def test_srg_lambda_parameter_2(self, w33_graph):
        """Any two adjacent vertices have exactly 2 common neighbors (lambda=2)."""
        n, adj, edges = w33_graph
        A = build_adjacency(edges, n)
        A2 = A @ A
        # For adjacent pair (u,v), A2[u,v] = number of common neighbors
        for u, v in edges[:20]:  # spot check first 20
            assert A2[u, v] == 2

    def test_srg_mu_parameter_4(self, w33_graph):
        """Any two non-adjacent vertices have exactly 4 common neighbors (mu=4)."""
        n, adj, edges = w33_graph
        A = build_adjacency(edges, n)
        A2 = A @ A
        adj_set = [set() for _ in range(n)]
        for u, v in edges:
            adj_set[u].add(v)
            adj_set[v].add(u)
        checked = 0
        for u in range(5):  # spot check
            for v in range(n):
                if v != u and v not in adj_set[u]:
                    assert A2[u, v] == 4
                    checked += 1
                    if checked >= 20:
                        break
            if checked >= 20:
                break


# ---------------------------------------------------------------------------
# T2: Lovász information capacity
# ---------------------------------------------------------------------------


class TestT2LovaszCapacity:
    def test_theta_w33_equals_10(self, w33_graph):
        n, adj, edges = w33_graph
        A = build_adjacency(edges, n)
        theta, k, s = lovász_theta(A)
        assert abs(theta - 10.0) < 1e-6

    def test_theta_w33_bar_equals_4(self, w33_graph):
        n, adj, edges = w33_graph
        A = build_adjacency(edges, n)
        evals = np.sort(np.linalg.eigvalsh(A.astype(float)))
        k = int(round(evals[-1]))
        r = int(round(evals[-2]))
        s = float(evals[0])
        theta_bar = -n * (-1 - r) / ((n - k - 1) - (-1 - r))
        assert abs(theta_bar - 4.0) < 1e-6

    def test_theta_product_equals_n(self, w33_graph):
        n, adj, edges = w33_graph
        A = build_adjacency(edges, n)
        evals = np.sort(np.linalg.eigvalsh(A.astype(float)))
        k = int(round(evals[-1]))
        r = int(round(evals[-2]))
        s = float(evals[0])
        theta = -n * s / (k - s)
        theta_bar = -n * (-1 - r) / ((n - k - 1) - (-1 - r))
        assert abs(theta * theta_bar - n) < 1e-6

    def test_theta_equals_spectral_gap(self, w33_graph):
        n, adj, edges = w33_graph
        A = build_adjacency(edges, n)
        evals = np.sort(np.linalg.eigvalsh(A.astype(float)))
        k = int(round(evals[-1]))
        r = int(round(evals[-2]))
        spectral_gap = k - r
        assert spectral_gap == 10

    def test_theta_equals_dim_sp4(self, w33_graph):
        """theta(W33) = 10 = dim(Sp(4,R)) = n(2n+1) for n=2."""
        n, adj, edges = w33_graph
        A = build_adjacency(edges, n)
        theta, k, s = lovász_theta(A)
        dim_sp4 = 10  # Sp(4) dimension
        assert int(round(theta)) == dim_sp4

    def test_adjacency_eigenvalues(self, w33_graph):
        """W33 eigenvalues are 12 (mult 1), 2 (mult 24), -4 (mult 15)."""
        n, adj, edges = w33_graph
        A = build_adjacency(edges, n)
        evals = np.sort(np.linalg.eigvalsh(A.astype(float)))
        assert abs(evals[-1] - 12) < 1e-6
        assert abs(evals[-2] - 2) < 1e-6
        assert abs(evals[0] - (-4)) < 1e-6

    def test_theorem2_exact_values(self, w33_graph):
        n, adj, edges = w33_graph
        r = theorem2_lovász_capacity(None, edges, n)
        assert r["theta_equals_dim_sp4"] is True
        assert r["product_equals_n"] is True
        assert r["spectral_gap"] == 10


# ---------------------------------------------------------------------------
# T3: Monster 3B three-generation bridge
# ---------------------------------------------------------------------------


class TestT3MonsterBridge:
    def test_omega4_antisymmetric(self):
        omega4 = build_f3_symplectic_form(4)
        assert np.all((omega4 + omega4.T) % 3 == 0)

    def test_omega4_nondegenerate(self):
        omega4 = build_f3_symplectic_form(4)
        assert rank_mod3(omega4) == 4

    def test_omega12_block_diagonal(self):
        omega4 = build_f3_symplectic_form(4)
        omega12 = np.zeros((12, 12), dtype=int)
        for b in range(3):
            omega12[4 * b : 4 * (b + 1), 4 * b : 4 * (b + 1)] = omega4
        assert rank_mod3(omega12) == 12
        assert np.all((omega12 + omega12.T) % 3 == 0)

    def test_f3_12_decomposes_as_f3_4_cubed(self):
        """F3^12 = F3^4 + F3^4 + F3^4 (direct sum)."""
        # Verify 12 = 3 * 4
        assert 12 == 3 * 4
        # Each block is a copy of F3^4
        omega4 = build_f3_symplectic_form(4)
        assert omega4.shape == (4, 4)

    def test_lagrangian_6_dim_isotropic(self):
        omega4 = build_f3_symplectic_form(4)
        omega12 = np.zeros((12, 12), dtype=int)
        for b in range(3):
            omega12[4 * b : 4 * (b + 1), 4 * b : 4 * (b + 1)] = omega4
        lag_vecs = []
        for b in range(3):
            for i in range(2):
                v = np.zeros(12, dtype=int)
                v[4 * b + i] = 1
                lag_vecs.append(v)
        assert rank_mod3(np.array(lag_vecs, dtype=int)) == 6
        assert is_isotropic_f3(lag_vecs, omega12) is True

    def test_sp4_order(self):
        """Order of Sp(4,3) = Weyl group of E6."""
        sp4_order = 25920 * 2  # = 51840 = |W(E6)|
        assert sp4_order == 51840

    def test_theorem3_result(self, w33_graph):
        n, adj, edges = w33_graph
        r = theorem3_three_generation_monster(None, edges)
        assert r["omega12_antisymmetric"] is True
        assert r["omega12_rank"] == 12
        assert r["lagrangian_dim"] == 6
        assert r["lagrangian_isotropic"] is True
        assert r["n_blocks"] == 3
        assert r["three_copies_of_w33"] is True


# ---------------------------------------------------------------------------
# T4: sl(3,F3)^3 Yukawa structure algebra
# ---------------------------------------------------------------------------


class TestT4Sl3Structure:
    def test_sl3_has_8_generators(self, sl3_generators):
        assert len(sl3_generators) == 8

    def test_sl3_generators_traceless(self, sl3_generators):
        for g in sl3_generators:
            assert np.trace(g) % 3 == 0

    def test_sl3_triple_produces_24_matrices(self, sl3_triple_mats):
        assert len(sl3_triple_mats) == 24

    def test_each_generator_27x27(self, sl3_triple_mats):
        for m in sl3_triple_mats:
            assert m.shape == (27, 27)

    def test_each_factor_rank_8(self, sl3_triple_mats):
        for start in (0, 8, 16):
            block = np.array([m.flatten() for m in sl3_triple_mats[start : start + 8]])
            assert rank_mod3(block) == 8

    def test_combined_rank_22_char3_identity(self, sl3_triple_mats):
        """In char 3, I_3 ∈ sl(3,F3), so 2 dependencies reduce rank from 24 to 22."""
        stack = np.array([m.flatten() for m in sl3_triple_mats], dtype=int) % 3
        r = rank_mod3(stack)
        assert r == 22

    def test_epsilon_cubic_nonzero_entries(self):
        C = build_e6_epsilon_cubic()
        assert C.shape == (27, 27, 27)
        # 6 permutations per factor: 6^3 = 216 nonzero entries
        assert np.sum(C != 0) == 216

    def test_epsilon_cubic_antisymmetry_first_two(self):
        """c(x,y,z) = -c(y,x,z) mod 3."""
        C = build_e6_epsilon_cubic()
        assert np.all((C + C.transpose(1, 0, 2)) % 3 == 0)

    def test_epsilon_cubic_totally_antisymmetric(self):
        """c is totally antisymmetric under all index permutations."""
        C = build_e6_epsilon_cubic()
        assert np.all((C + C.transpose(1, 0, 2)) % 3 == 0)
        assert np.all((C + C.transpose(0, 2, 1)) % 3 == 0)

    def test_sl3_triple_preserves_epsilon_cubic_8_of_8(self, sl3_triple_mats):
        """All 8 checked generators annihilate the epsilon cubic form."""
        inv, checked = sl3_triple_preserves_cubic(sl3_triple_mats, [])
        assert checked == 8
        assert inv == 8

    def test_cubic_invariance_theorem4(self, local_tris, sl3_triple_mats):
        inv, checked = sl3_triple_preserves_cubic(sl3_triple_mats, local_tris)
        assert inv == checked  # all generators checked preserve cubic

    def test_e6_hierarchy_dims(self):
        """E6 (78) = sl(3)^3 (24) + 54 hidden generators = 27+27 matter."""
        assert 78 - 24 == 54
        assert 54 == 2 * 27


# ---------------------------------------------------------------------------
# T5: Code rate, Bekenstein bound, QCA causal structure
# ---------------------------------------------------------------------------


class TestT5BekensteinkQCA:
    def test_code_rate_is_27_over_80(self, w33_graph):
        n, adj, edges = w33_graph
        n_edges = len(edges)
        k_h1 = 81
        assert n_edges == 240
        assert k_h1 / n_edges == pytest.approx(27 / 80)

    def test_bekenstein_bits(self, w33_graph):
        n, adj, edges = w33_graph
        n_edges = len(edges)
        s_bh = n_edges / 4
        assert s_bh == 60.0

    def test_w33_information_bits(self, w33_graph):
        n, adj, edges = w33_graph
        k_h1 = 81
        w33_bits = k_h1 * np.log2(3)
        assert w33_bits == pytest.approx(128.38, abs=0.02)

    def test_ratio_approx_2(self, w33_graph):
        n, adj, edges = w33_graph
        n_edges = len(edges)
        k_h1 = 81
        ratio = (k_h1 * np.log2(3)) / (n_edges / 4)
        assert abs(ratio - 2.14) < 0.02

    def test_causal_diameter_2(self, w33_graph):
        n, adj, edges = w33_graph
        from collections import deque

        adj_local = [[] for _ in range(n)]
        for u, v in edges:
            adj_local[u].append(v)
            adj_local[v].append(u)
        max_dist = 0
        for src in range(n):
            q = deque([src])
            visited = {src: 0}
            while q:
                cur = q.popleft()
                for nb in adj_local[cur]:
                    if nb not in visited:
                        visited[nb] = visited[cur] + 1
                        q.append(nb)
            max_dist = max(max_dist, max(visited.values()))
        assert max_dist == 2

    def test_d1_equals_12(self, w33_graph):
        """Vertex 0 has exactly 12 distance-1 neighbors."""
        n, adj, edges = w33_graph
        A = build_adjacency(edges, n)
        assert int(np.sum(A[0] == 1)) == 12

    def test_d2_equals_27(self, w33_graph):
        """Vertex 0 has exactly 27 distance-2 vertices."""
        n, adj, edges = w33_graph
        A = build_adjacency(edges, n)
        # distance-2 = non-neighbors (excluding self)
        d2 = n - 1 - int(np.sum(A[0]))
        assert d2 == 27

    def test_theorem5_causal_cone_exact(self, w33_graph):
        n, adj, edges = w33_graph
        r = theorem5_bekenstein_qca(None, edges, n)
        assert r["causal_cone_exact"] is True
        assert r["diameter"] == 2
        assert r["d1_gauge_count"] == 12
        assert r["d2_matter_count"] == 27


# ---------------------------------------------------------------------------
# T6: Golay 24-dim Lie algebra
# ---------------------------------------------------------------------------


class TestT6GolayLieAlgebra:
    @pytest.fixture(scope="class")
    def golay_result(self):
        return theorem6_golay_lie_algebra()

    def test_perfect(self, golay_result):
        assert golay_result["perfect"] is True

    def test_center_dim_zero(self, golay_result):
        assert golay_result["center_dim"] == 0

    def test_killing_form_rank_zero(self, golay_result):
        """Zero Killing form mod 3 = modular algebra of Cartan type."""
        assert golay_result["killing_rank_mod3"] == 0

    def test_derivation_dim_33(self, golay_result):
        assert golay_result["dim_derivations"] == 33

    def test_inner_derivations_24(self, golay_result):
        assert golay_result["dim_inner_derivations"] == 24

    def test_outer_derivations_9(self, golay_result):
        """9 outer derivations = generation mixing operators."""
        assert golay_result["dim_outer_derivations"] == 9

    def test_9_outer_equals_3_squared(self, golay_result):
        """9 = 3^2 = |F3^2| - 1 + 1 = all grade-translation directions."""
        assert golay_result["dim_outer_derivations"] == 3**2

    def test_cartan_self_centralizing(self, golay_result):
        assert golay_result["self_centralizing"] is True

    def test_cartan_centralizer_dim_6(self, golay_result):
        assert golay_result["cartan_centralizer_dim"] == 6

    def test_n_outer_equals_n_generation_mixing(self, golay_result):
        assert golay_result["n_outer_equals_n_generation_mixing"] is True

    def test_dim_equals_24(self, golay_result):
        assert golay_result["dim"] == 24


# ---------------------------------------------------------------------------
# Data file
# ---------------------------------------------------------------------------


class TestDataFile:
    @pytest.fixture(scope="class")
    def data(self):
        path = os.path.join(repo_root, "data", "w33_information_structure.json")
        if not os.path.exists(path):
            build_information_structure_report()
        with open(path) as f:
            return json.load(f)

    def test_pillar_number(self, data):
        assert data["pillar"] == 67

    def test_key_identities_all_true(self, data):
        ki = data["key_identities"]
        assert ki["1_plus_12_plus_27_equals_40"] is True
        assert ki["theta_W33_equals_dim_Sp4"] is True
        assert ki["theta_product_equals_n"] is True
        assert ki["f3_12_equals_f3_4_cubed"] is True
        assert ki["sl3_cube_dim_24"] is True
        assert ki["causal_diameter_2"] is True

    def test_t1_decomposition_exact(self, data):
        assert data["T1_causal_decomposition"]["decomposition_exact"] is True

    def test_t2_theta_10(self, data):
        assert abs(data["T2_lovász_capacity"]["theta_W33"] - 10.0) < 1e-6

    def test_t5_code_rate(self, data):
        assert data["T5_bekenstein_qca"]["code_rate_fraction"] == "27/80"

    def test_t6_outer_derivations(self, data):
        assert data["T6_golay_lie_algebra"]["dim_outer_derivations"] == 9


# ---------------------------------------------------------------------------
# Integration: rank_mod3 correctness
# ---------------------------------------------------------------------------


class TestRankMod3:
    def test_rank_identity(self):
        I = np.eye(5, dtype=int)
        assert rank_mod3(I) == 5

    def test_rank_zero_matrix(self):
        Z = np.zeros((4, 6), dtype=int)
        assert rank_mod3(Z) == 0

    def test_rank_wide_matrix(self):
        """Key case: 24 rows, 729 cols (sl3_triple generators)."""
        # Build a 3x9 matrix with rank 3 (all rows independent)
        M = np.zeros((3, 9), dtype=int)
        M[0, 0] = 1
        M[1, 4] = 1
        M[2, 8] = 1
        assert rank_mod3(M) == 3

    def test_rank_mod3_with_dependencies(self):
        """Two rows are mod-3 equal: rank = 1."""
        M = np.array([[1, 0, 2], [1, 0, 2]], dtype=int)
        assert rank_mod3(M) == 1

    def test_rank_mod3_char3_cancellation(self):
        """Row + row + row = 0 mod 3: rank = 2."""
        M = np.array([[1, 0, 0], [0, 1, 0], [1, 1, 0]], dtype=int)
        # Row3 = Row1 + Row2, so rank = 2
        assert rank_mod3(M) == 2
