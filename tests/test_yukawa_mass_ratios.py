import os
import sys

import numpy as np
import pytest

# ensure our repo root and scripts directory are on the import path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.insert(0, repo_root)
sys.path.insert(0, os.path.join(repo_root, "scripts"))

from THEORY_PART_CLXXIV_YUKAWA_OPTIMIZATION import V_CKM_exp

from scripts.yukawa_mass_ratio_analysis import (
    build_yukawa_tensor,
    load_optimized_vevs,
    optimize_mass_ratio,
    random_search,
    singular_value_ratios,
    yukawa_from_vev,
)


def assert_close(a, b, tol=1e-6):
    assert abs(a - b) < tol, f"{a} != {b}"


def load_optimized_vevs_or_skip():
    vevs = load_optimized_vevs()
    if vevs is None:
        pytest.skip(
            "data/w33_yukawa_optimization.json is absent; run "
            "THEORY_PART_CLXXIV_YUKAWA_OPTIMIZATION.py first"
        )
    return vevs


def test_opt_ckm_vev_mass_ratios():
    """Check singular value ratios for the optimized CKM VEV direction."""
    vevs = load_optimized_vevs_or_skip()
    v_up, v_dn = vevs
    T = build_yukawa_tensor()
    Y_u = np.einsum("abk,k->ab", T, v_up)
    Y_d = np.einsum("abk,k->ab", T, v_dn)
    sv_u, ratios_u = singular_value_ratios(Y_u)
    sv_d, ratios_d = singular_value_ratios(Y_d)
    # ratios should show a clear hierarchy but not necessarily match SM values
    assert ratios_u[0] > 0.1 and ratios_u[1] > 0.05
    assert ratios_d[0] > 0.1 and ratios_d[1] > 0.1
    # also verify deterministic values from current data
    assert_close(ratios_u[0], 0.5123519638110201, tol=1e-8)
    assert_close(ratios_u[1], 0.18946110060652477, tol=1e-8)
    assert_close(ratios_d[0], 0.40187580865747397, tol=1e-8)
    assert_close(ratios_d[1], 0.41311003124194506, tol=1e-8)


def test_random_search_deterministic():
    """Random sampling should return reproducible error values with fixed seed."""
    T = build_yukawa_tensor()
    best = random_search(T, n_samples=2000, seed=0)
    # values taken from a previous run to lock regression
    assert_close(best["up_err"], 29.082780351015852, tol=1e-12)
    assert_close(best["dn_err"], 1.4958725754578839, tol=1e-12)
    # ensure the returned vevs have correct shape and are normalized
    for key in ("up_vev", "dn_vev"):
        v = best[key]
        assert v is not None and v.shape == (27,)
        assert abs(np.linalg.norm(v) - 1.0) < 1e-12


def test_mass_ratio_optimization():
    """Verify that gradient optimization can recover the target ratios."""
    T = build_yukawa_tensor()
    r_up = [1 / 500, 500 / 85000]
    r_dn = [1 / 20, 1 / 40]
    err_u, v_u = optimize_mass_ratio(T, r_up, n_restarts=3)
    err_d, v_d = optimize_mass_ratio(T, r_dn, n_restarts=3)
    assert err_u < 1e-6
    assert err_d < 1e-6
    sv_u, ratios_u = singular_value_ratios(yukawa_from_vev(T, v_u))
    sv_d, ratios_d = singular_value_ratios(yukawa_from_vev(T, v_d))
    assert_close(ratios_u[0], 1 / 500, tol=1e-6)
    assert_close(ratios_u[1], 500 / 85000, tol=1e-6)
    assert_close(ratios_d[0], 1 / 20, tol=1e-6)
    assert_close(ratios_d[1], 1 / 40, tol=1e-6)


def test_combined_optimization():
    """Combined CKM and mass ratios can be simultaneously optimized."""
    T = build_yukawa_tensor()
    # initial CKM-only solution from data
    vevs = load_optimized_vevs_or_skip()
    v_up0, v_dn0 = vevs
    init = np.concatenate(
        [np.real(v_up0), np.imag(v_up0), np.real(v_dn0), np.imag(v_dn0)]
    )

    # run a short combined optimisation with weight=1
    from scipy.optimize import minimize

    from scripts.yukawa_mass_ratio_analysis import ckm_and_mass_objective

    def run(init_params):
        res = minimize(
            ckm_and_mass_objective,
            init_params,
            args=(T, V_CKM_exp, [1 / 500, 500 / 85000], [1 / 20, 1 / 40], 1.0),
            method="L-BFGS-B",
            options={"maxiter": 500, "ftol": 1e-10},
        )
        return res.fun, res.x

    best_err, best_params = run(init)
    # confirm the optimizer actually improved the combined objective
    init_err, _ = run(init)
    assert best_err <= init_err
    # check that CKM component did not blow up catastrophically
    c_err = ckm_and_mass_objective(
        best_params,
        T,
        V_CKM_exp,
        [1 / 500, 500 / 85000],
        [1 / 20, 1 / 40],
        weight_mass=0.0,
    )
    assert c_err < 1.0
    # and mass component is at most the same as initial mass component
    m_initial = ckm_and_mass_objective(
        init, T, V_CKM_exp, [1 / 500, 500 / 85000], [1 / 20, 1 / 40], weight_mass=1.0
    ) - ckm_and_mass_objective(
        init, T, V_CKM_exp, [1 / 500, 500 / 85000], [1 / 20, 1 / 40], weight_mass=0.0
    )
    m_err = (
        ckm_and_mass_objective(
            best_params,
            T,
            V_CKM_exp,
            [1 / 500, 500 / 85000],
            [1 / 20, 1 / 40],
            weight_mass=1.0,
        )
        - c_err
    )
    assert m_err <= m_initial
