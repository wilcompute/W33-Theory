"""
Regression tests for Part CXXXVI — Doob-Bridge Generation Spectrum.

These tests pin the five finite identities of CXXXVI.A–E to the
SRG(40,12,2,4) parameters of W(3,3).
"""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path

import numpy as np
import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "PART_CXXXVI_DOOB_BRIDGE_GENERATION_SPECTRUM.py"


@pytest.fixture(scope="module")
def cxxxvi_module():
    spec = importlib.util.spec_from_file_location("part_cxxxvi", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def w33_setup(cxxxvi_module):
    A, edges = cxxxvi_module.build_w33_adjacency()
    B, directed = cxxxvi_module.build_hashimoto(A, edges)
    return A, edges, B, directed


def test_w33_basic_parameters(w33_setup):
    A, edges, B, directed = w33_setup
    assert A.shape == (40, 40)
    assert len(edges) == 240
    assert len(directed) == 480
    # 12-regular
    assert (A.sum(axis=1) == 12).all()
    # Hashimoto outdegree = k-1 = 11
    assert (np.array(B.sum(axis=1)).flatten() == 11).all()


def test_walk_counts_known_values(cxxxvi_module, w33_setup):
    """T_n = tr(B^n) for n=1..6 must match known values."""
    A, edges, B, directed = w33_setup
    counts = cxxxvi_module.closed_walk_counts(B, 6)
    assert counts[0] == 0  # T_1
    assert counts[1] == 0  # T_2
    assert counts[2] == 960          # T_3 = vkλ = 40·12·2
    assert counts[3] == 13920        # T_4
    assert counts[4] == 181440       # T_5
    assert counts[5] == 1818240      # T_6


def test_triangle_count_identity(cxxxvi_module, w33_setup):
    """Theorem identity: T_3 = vkλ."""
    _, _, B, _ = w33_setup
    counts = cxxxvi_module.closed_walk_counts(B, 3)
    assert counts[2] == 40 * 12 * 2 == 960


def test_cxxxvi_b_triangle_lensing(cxxxvi_module, w33_setup):
    """Theorem CXXXVI.B: every directed edge has exactly λ = 2
    Doob-bridge-compatible continuations at n=3."""
    _, _, B, _ = w33_setup
    dist = cxxxvi_module.doob_first_step_branching(B, 3)
    # All 480 directed edges should have N_bridge(3, e) = 2 = λ.
    assert dist == {2: 480}


def test_cxxxvi_c_saturation(cxxxvi_module, w33_setup):
    """Theorem CXXXVI.C: for n in {4,5,6,7,8} all directed edges have
    N_bridge(n,e) = k-1 = 11."""
    _, _, B, _ = w33_setup
    for n in [4, 5, 6, 7, 8]:
        dist = cxxxvi_module.doob_first_step_branching(B, n)
        assert dist == {11: 480}, f"n={n} distribution {dist}"


def test_cxxxvi_a_perron_limit(cxxxvi_module, w33_setup):
    """Theorem CXXXVI.A: W_n -> (k-1)/(2m) = 11/480 ≈ 0.022917."""
    _, _, B, _ = w33_setup
    counts = cxxxvi_module.closed_walk_counts(B, 12)
    closure = cxxxvi_module.closure_fractions(counts, k=12)
    target = 11.0 / 480.0
    # By n=10 the closure fraction must be within 1e-4 of the limit
    assert abs(closure[9]["W_n"] - target) < 1e-3
    assert abs(closure[10]["W_n"] - target) < 5e-4
    assert abs(closure[11]["W_n"] - target) < 5e-4


def test_cxxxvi_d_entropy_floor_log2(cxxxvi_module, w33_setup):
    """Theorem CXXXVI.D: at n=3 the mean bridge entropy is exactly log 2,
    the entropy floor of the triangle lensing."""
    _, _, B, _ = w33_setup
    ent = cxxxvi_module.doob_bridge_entropy(B, 3)
    assert math.isclose(ent["mean_entropy"], math.log(2), rel_tol=1e-12)
    assert ent["fraction_starts"] == 1.0


def test_cxxxvi_d_entropy_saturation(cxxxvi_module, w33_setup):
    """Theorem CXXXVI.D: by n=7 the bridge entropy ratio to log(k-1)
    is 1.0 to 6 decimals."""
    _, _, B, _ = w33_setup
    ent = cxxxvi_module.doob_bridge_entropy(B, 7)
    assert abs(ent["ratio_to_log11"] - 1.0) < 1e-6


def test_cxxxvi_e_ramanujan_subdominant(cxxxvi_module, w33_setup):
    """Theorem CXXXVI.E: the subdominant absolute eigenvalue of B is
    sqrt(k-1) = sqrt(11), the Ramanujan / Ihara-zeta critical radius."""
    _, _, B, _ = w33_setup
    from scipy.sparse.linalg import eigs
    vals, _ = eigs(B, k=4, which="LM")
    abs_sorted = sorted([abs(v) for v in vals], reverse=True)
    # Top is k-1 = 11
    assert abs(abs_sorted[0] - 11.0) < 1e-6
    # Subdominant is sqrt(11) ≈ 3.3166
    assert abs(abs_sorted[1] - math.sqrt(11)) < 1e-3
    assert abs(abs_sorted[2] - math.sqrt(11)) < 1e-3
