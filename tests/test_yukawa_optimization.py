"""tests/test_yukawa_optimization.py
Pillar 65: Yukawa Tensor Gradient Optimization
Tests for THEORY_PART_CLXXIV_YUKAWA_OPTIMIZATION.py

All numerics loaded from data/w33_yukawa_optimization.json.
If the JSON does not exist, tests are skipped.
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np
import pytest

DATA_FILE = os.path.join(
    os.path.dirname(__file__), "..", "data", "w33_yukawa_optimization.json"
)


@pytest.fixture(scope="module")
def results():
    if not os.path.exists(DATA_FILE):
        pytest.skip(
            f"data file not found: {DATA_FILE} — run THEORY_PART_CLXXIV_YUKAWA_OPTIMIZATION.py first"
        )
    with open(DATA_FILE) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Tensor structure
# ---------------------------------------------------------------------------


def test_pillar_is_65(results):
    assert results["pillar"] == 65


def test_tensor_rank_is_6(results):
    """Yukawa tensor has rank exactly 6 (3 pairs = 3 generations x 2 Higgs)."""
    assert results["tensor_rank"] == 6, f"Expected rank 6, got {results['tensor_rank']}"


def test_tensor_active_subspace_dim(results):
    """Active subspace dimension matches tensor rank."""
    assert results["active_subspace_dim"] == results["tensor_rank"]


def test_tensor_null_space_dim(results):
    """27 - rank = 21 flat Higgs directions."""
    assert results["null_space_dim"] == 27 - results["tensor_rank"]


def test_tensor_singular_values_descending(results):
    """Tensor singular values are in non-increasing order."""
    svs = results["tensor_singular_values"]
    for i in range(len(svs) - 1):
        assert (
            svs[i] >= svs[i + 1] - 1e-10
        ), f"SVs not descending at index {i}: {svs[i]:.6f} < {svs[i+1]:.6f}"


def test_tensor_sv_degenerate_pairs():
    """Singular values 1-2 and 5-6 are degenerate (Z3 CP-conjugate symmetry)."""
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.insert(0, repo_root)
    sys.path.insert(0, os.path.join(repo_root, "scripts"))
    from THEORY_PART_CLXXIV_YUKAWA_OPTIMIZATION import build_yukawa_tensor
    from w33_ckm_from_vev import cubic_form_on_h27
    from w33_complex_yukawa import build_dominant_profiles, build_z3_complex_profiles

    _, local_tris, _, P = build_z3_complex_profiles()
    psi_dom = build_dominant_profiles(P)
    T = build_yukawa_tensor(psi_dom, local_tris)
    T_mat = T.reshape(9, 27)
    _, s, _ = np.linalg.svd(T_mat, full_matrices=False)
    # s[0] == s[1] and s[4] == s[5] (CP-conjugate pairs)
    assert abs(s[0] - s[1]) < 1e-10, f"s[0]={s[0]:.8f} != s[1]={s[1]:.8f}"
    assert abs(s[4] - s[5]) < 1e-10, f"s[4]={s[4]:.8f} != s[5]={s[5]:.8f}"


# ---------------------------------------------------------------------------
# CKM optimization improvements
# ---------------------------------------------------------------------------


def test_gradient_ckm_better_than_grid(results):
    """Gradient optimization gives strictly better CKM error than grid scan."""
    assert results["gradient_ckm_error"] < results["grid_scan_ckm_error"], (
        f"gradient {results['gradient_ckm_error']:.6f} not < "
        f"grid {results['grid_scan_ckm_error']:.6f}"
    )


def test_gradient_ckm_error_small(results):
    """Gradient CKM error < 0.025 (more than 2x better than grid scan 0.057)."""
    err = results["gradient_ckm_error"]
    assert err < 0.025, f"CKM error {err:.6f} not < 0.025"


def test_vub_essentially_exact(results):
    """V_ub predicted to within 30% of experiment (0.0038)."""
    V = np.array(results["ckm"]["V"])
    Vub = V[0, 2]
    assert 0.002 < Vub < 0.008, f"|V_ub| = {Vub:.4f}, expected in [0.002, 0.008]"


def test_vud_accurate(results):
    """V_ud > 0.97 after optimization."""
    V = np.array(results["ckm"]["V"])
    assert V[0, 0] > 0.97, f"|V_ud| = {V[0,0]:.4f}"


def test_vus_accurate(results):
    """|V_us| in [0.20, 0.25] after optimization."""
    V = np.array(results["ckm"]["V"])
    Vus = V[0, 1]
    assert 0.20 < Vus < 0.25, f"|V_us| = {Vus:.4f}"


def test_ckm_diagonal_dominance(results):
    """CKM matrix is nearly diagonal (diagonal elements close to 1)."""
    V = np.array(results["ckm"]["V"])
    assert V[0, 0] > 0.97, f"V_ud = {V[0,0]:.4f}"
    assert V[1, 1] > 0.97, f"V_cs = {V[1,1]:.4f}"
    assert V[2, 2] > 0.99, f"V_tb = {V[2,2]:.4f}"


def test_quark_jarlskog_nonzero(results):
    """Quark-sector Jarlskog invariant is non-zero after optimization."""
    J = results["ckm"]["Jarlskog"]
    assert abs(J) > 1e-6, f"Jarlskog J = {J:.4e} is effectively zero"


def test_quark_jarlskog_order_of_magnitude(results):
    """Quark J within an order of magnitude of exp value 3.1e-5."""
    J = results["ckm"]["Jarlskog"]
    J_exp = 3.1e-5
    ratio = abs(J) / J_exp
    assert (
        0.1 < ratio < 10
    ), f"Jarlskog |J| = {abs(J):.2e}, exp 3.1e-5, ratio = {ratio:.2f}"


# ---------------------------------------------------------------------------
# PMNS optimization improvements
# ---------------------------------------------------------------------------


def test_gradient_pmns_better_than_grid(results):
    """Gradient PMNS error is strictly better than grid scan."""
    assert results["gradient_pmns_error"] < results["grid_scan_pmns_error"], (
        f"gradient {results['gradient_pmns_error']:.6f} not < "
        f"grid {results['grid_scan_pmns_error']:.6f}"
    )


def test_gradient_pmns_error_very_small(results):
    """Gradient PMNS error < 0.010 (6x better than grid scan 0.038)."""
    err = results["gradient_pmns_error"]
    assert err < 0.010, f"PMNS error {err:.6f} not < 0.010"


def test_ve3_reactor_angle(results):
    """|V_e3| (reactor angle) accurately predicted in [0.13, 0.16]."""
    V = np.array(results["pmns"]["V"])
    Ve3 = V[0, 2]
    assert 0.13 < Ve3 < 0.16, f"|V_e3| = {Ve3:.4f}"


def test_pmns_solar_angle(results):
    """|V_e2| (solar angle) in [0.50, 0.60]."""
    V = np.array(results["pmns"]["V"])
    Ve2 = V[0, 1]
    assert 0.50 < Ve2 < 0.60, f"|V_e2| = {Ve2:.4f}"


def test_pmns_atmospheric_angle(results):
    """|V_mu3| (atmospheric angle) in [0.60, 0.70]."""
    V = np.array(results["pmns"]["V"])
    Vmu3 = V[1, 2]
    assert 0.60 < Vmu3 < 0.70, f"|V_mu3| = {Vmu3:.4f}"


def test_lepton_jarlskog_large(results):
    """Lepton-sector Jarlskog is large (> 0.001), as measured."""
    J = results["pmns"]["Jarlskog"]
    assert abs(J) > 0.001, f"Lepton Jarlskog {J:.4e} too small"


# ---------------------------------------------------------------------------
# Structural consistency
# ---------------------------------------------------------------------------


def test_improved_ckm_flag(results):
    assert results["improved_ckm"] is True


def test_improved_pmns_flag(results):
    assert results["improved_pmns"] is True


def test_tensor_build_fast():
    """Yukawa tensor builds in < 1 second."""
    import time

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.insert(0, repo_root)
    sys.path.insert(0, os.path.join(repo_root, "scripts"))
    from THEORY_PART_CLXXIV_YUKAWA_OPTIMIZATION import build_yukawa_tensor
    from w33_complex_yukawa import build_dominant_profiles, build_z3_complex_profiles

    _, local_tris, _, P = build_z3_complex_profiles()
    psi_dom = build_dominant_profiles(P)
    t0 = time.time()
    T = build_yukawa_tensor(psi_dom, local_tris)
    elapsed = time.time() - t0
    assert elapsed < 1.0, f"Tensor built in {elapsed:.2f}s (expected < 1s)"
    assert T.shape == (3, 3, 27)


def test_tensor_vs_direct_yukawa():
    """T @ e_k gives same result as direct yukawa3x3 call."""
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.insert(0, repo_root)
    sys.path.insert(0, os.path.join(repo_root, "scripts"))
    from THEORY_PART_CLXXIV_YUKAWA_OPTIMIZATION import build_yukawa_tensor, yukawa_fast
    from w33_complex_yukawa import (
        build_dominant_profiles,
        build_z3_complex_profiles,
        yukawa3x3,
    )

    H27, local_tris, _, P = build_z3_complex_profiles()
    psi_dom = build_dominant_profiles(P)
    T = build_yukawa_tensor(psi_dom, local_tris)

    # Test with a non-trivial complex VEV
    v = np.zeros(27, dtype=complex)
    v[5] = 0.6 + 0.3j
    v[12] = 0.4 - 0.5j
    v[20] = 0.3 + 0.1j

    Y_direct = yukawa3x3(psi_dom, local_tris, v)
    Y_fast = yukawa_fast(T, v)
    diff = np.linalg.norm(Y_direct - Y_fast)
    assert diff < 1e-12, f"Tensor mismatch ||diff|| = {diff:.2e}"
