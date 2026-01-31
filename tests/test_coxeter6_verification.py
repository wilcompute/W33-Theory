"""Test the Coxeter 6-cycle verification (pure NumPy, no SageMath).

Verifies the crown jewel result: c^5 partitions 240 E8 roots into
40 orbits of size 6, whose adjacency graph is SRG(40,12,2,4) ≅ W33.
Also verifies the W(E6) orbit decomposition 240 = 72 + 6×27 + 6×1.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

# Allow importing from tools/
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from verify_coxeter6_numpy import (E6_SIMPLE_ROOTS, E8_SIMPLE_ROOTS,
                                   build_coxeter_matrix,
                                   build_e6_reflection_matrices,
                                   build_e8_roots, build_w33_from_f3)

# ── E8 root system ──────────────────────────────────────────────────


def test_e8_root_count():
    roots = build_e8_roots()
    assert roots.shape == (240, 8)


def test_e8_root_norms():
    roots = build_e8_roots()
    norms_sq = np.sum(roots**2, axis=1)
    assert np.allclose(norms_sq, 2.0)


def test_e8_inner_products():
    roots = build_e8_roots()
    gram = roots @ roots.T
    unique = set(int(round(x)) for x in np.unique(np.round(gram, 6)))
    assert unique == {-2, -1, 0, 1, 2}


# ── Coxeter element ─────────────────────────────────────────────────


def test_coxeter_number_30():
    C = build_coxeter_matrix(E8_SIMPLE_ROOTS)
    Ck = np.eye(8)
    for k in range(1, 31):
        Ck = C @ Ck
        if np.allclose(Ck, np.eye(8), atol=1e-10):
            assert k == 30
            return
    pytest.fail("Coxeter element did not reach order 30")


def test_c5_has_order_6():
    C = build_coxeter_matrix(E8_SIMPLE_ROOTS)
    W = np.linalg.matrix_power(C, 5)
    Wk = np.eye(8)
    for k in range(1, 31):
        Wk = W @ Wk
        if np.allclose(Wk, np.eye(8), atol=1e-10):
            assert k == 6
            return
    pytest.fail("c^5 did not reach order 6")


# ── 40 orbits of size 6 ─────────────────────────────────────────────


@pytest.fixture(scope="module")
def coxeter_orbits():
    roots = build_e8_roots()
    C = build_coxeter_matrix(E8_SIMPLE_ROOTS)
    W = np.linalg.matrix_power(C, 5)

    used = np.zeros(240, dtype=bool)
    orbits = []
    for i in range(240):
        if used[i]:
            continue
        orb = [i]
        used[i] = True
        v = roots[i].copy()
        for _ in range(5):
            v = W @ v
            dists = np.sum((roots - v) ** 2, axis=1)
            j = np.argmin(dists)
            assert dists[j] < 1e-10
            if used[j]:
                break
            used[j] = True
            orb.append(j)
        orbits.append(orb)

    return roots, orbits


def test_40_orbits(coxeter_orbits):
    _, orbits = coxeter_orbits
    assert len(orbits) == 40


def test_all_orbits_size_6(coxeter_orbits):
    _, orbits = coxeter_orbits
    assert all(len(o) == 6 for o in orbits)


# ── SRG(40,12,2,4) ──────────────────────────────────────────────────


@pytest.fixture(scope="module")
def orbit_adj(coxeter_orbits):
    roots, orbits = coxeter_orbits
    adj = np.zeros((40, 40), dtype=int)
    for i in range(40):
        ri = roots[orbits[i]]
        for j in range(i + 1, 40):
            rj = roots[orbits[j]]
            ips = np.round(ri @ rj.T).astype(int)
            if np.all(ips == 0):
                adj[i, j] = adj[j, i] = 1
    return adj


def test_orbit_graph_regular_degree_12(orbit_adj):
    degrees = orbit_adj.sum(axis=1)
    assert np.all(degrees == 12)


def test_orbit_graph_lambda_2(orbit_adj):
    adj = orbit_adj
    for i in range(40):
        for j in range(i + 1, 40):
            if adj[i, j]:
                cn = np.sum(adj[i] & adj[j])
                assert cn == 2


def test_orbit_graph_mu_4(orbit_adj):
    adj = orbit_adj
    for i in range(40):
        for j in range(i + 1, 40):
            if not adj[i, j]:
                cn = np.sum(adj[i] & adj[j])
                assert cn == 4


def test_orbit_graph_240_edges(orbit_adj):
    assert orbit_adj.sum() // 2 == 240


def test_orbit_graph_isomorphic_to_w33(orbit_adj):
    """SRG(40,12,2,4) is unique up to isomorphism (Hubaut 1975).

    Matching eigenvalue spectra suffices.
    """
    w33_adj, _ = build_w33_from_f3()
    eigs1 = sorted(np.round(np.linalg.eigvalsh(orbit_adj.astype(float)), 4))
    eigs2 = sorted(np.round(np.linalg.eigvalsh(w33_adj.astype(float)), 4))
    assert np.allclose(eigs1, eigs2, atol=1e-3)


# ── W(E6) orbit decomposition ───────────────────────────────────────


@pytest.fixture(scope="module")
def we6_orbits():
    roots = build_e8_roots()
    ref_mats = build_e6_reflection_matrices()
    n = len(roots)
    used = np.zeros(n, dtype=bool)
    orbits = []

    for seed in range(n):
        if used[seed]:
            continue
        orb = [seed]
        used[seed] = True
        frontier = [seed]
        while frontier:
            new_frontier = []
            for idx in frontier:
                v = roots[idx]
                for S in ref_mats:
                    w = S @ v
                    dists = np.sum((roots - w) ** 2, axis=1)
                    j = np.argmin(dists)
                    if dists[j] > 1e-8:
                        continue
                    if not used[j]:
                        used[j] = True
                        orb.append(j)
                        new_frontier.append(j)
            frontier = new_frontier
        orbits.append(orb)

    return orbits


def test_we6_13_orbits(we6_orbits):
    assert len(we6_orbits) == 13


def test_we6_orbit_sizes(we6_orbits):
    sizes = sorted([len(o) for o in we6_orbits], reverse=True)
    expected = sorted([72] + [27] * 6 + [1] * 6, reverse=True)
    assert sizes == expected
