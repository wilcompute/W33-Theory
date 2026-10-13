"""TOE63: spectral robustness criterion for the native W33 winding flux.

A strengthening of TOE62's *sufficient* hopping-disorder bound, not a new
physical phase transition or a claim about all temperatures.

For u_i=sqrt(1-cos(delta_i)), 1-cos(delta_i +/- delta_j)
 <= (u_i+u_j)^2.  The six positive Fourier coefficients are bounded
individually using the native length-eight winding-cycle counts.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_20261013_toe62_global_flat_flux_proof import folded, get_coefficients


def analytic_bounds():
    c = get_coefficients()
    singles = np.asarray(
        [c[folded(tuple(int(i == j) for i in range(3)))] for j in range(3)],
        dtype=float,
    )
    crosses = {
        (0, 1): c[folded((1, 1, 0))],
        (0, 2): c[folded((1, 0, 1))],
        (1, 2): c[folded((0, 1, -1))],
    }
    assert singles.tolist() == [79, 77, 77]
    assert crosses == {(0, 1): 1, (0, 2): 1, (1, 2): 3}
    D = np.diag(singles)
    M = np.zeros((3, 3), dtype=float)
    for (i, j), n in crosses.items():
        v = np.zeros(3)
        v[i] = v[j] = 1
        M += n * np.outer(v, v)
    assert np.array_equal(M, np.asarray([[2, 1, 1], [1, 4, 3], [1, 3, 4]]))
    # The antisymmetric 2--3 mode has eigenvalue 77-r.
    # The symmetric two-dimensional block determinant is
    # (79-2r)(77-7r)-2r^2 = 6083-707r+12r^2.
    discriminant = 707 * 707 - 4 * 12 * 6083
    assert discriminant == 207865
    r_star = (707 - math.sqrt(discriminant)) / 24
    assert 1 < r_star < 77
    assert abs(np.linalg.det(D - r_star * M)) < 1e-8
    epsilon_star = (r_star ** (1 / 8) - 1) / (r_star ** (1 / 8) + 1)
    old_ratio = 77 / 8
    old_epsilon = (old_ratio ** (1 / 8) - 1) / (old_ratio ** (1 / 8) + 1)
    assert epsilon_star > old_epsilon
    return c, D, M, r_star, epsilon_star, old_epsilon


def gap_matrix(eps, D, M):
    if not (0 <= eps < 1):
        raise ValueError("Positive hopping lower bound requires 0 <= eps < 1")
    return (1 - eps) ** 8 * D - (1 + eps) ** 8 * M


def certificate():
    c, D, M, r_star, threshold, previous = analytic_bounds()
    rng = np.random.default_rng(631013)
    checks = []
    for eps in (0, previous, 0.145, threshold * (1 - 1e-6), threshold + 0.0001):
        eigs = np.linalg.eigvalsh(gap_matrix(eps, D, M))
        expected_positive = eps < threshold
        assert (min(eigs) > 0) == expected_positive
        checks.append({"epsilon": float(eps), "eigenvalues": eigs.tolist(),
                       "positive_definite": bool(min(eigs) > 0)})
    # Stronger independent stress-test: sample six independent positive
    # Fourier coefficients within the *full* octagon-product intervals.
    # Real edge-product coefficients form a subset of these choices.
    for eps in (0.10, 0.14, 0.145):
        lower = (1 - eps) ** 8
        upper = (1 + eps) ** 8
        mat = gap_matrix(eps, D, M)
        for _ in range(200):
            a = np.array([79, 77, 77]) * rng.uniform(lower, upper, 3)
            z = np.array([1, 1, 3]) * rng.uniform(lower, upper, 3)
            theta = rng.uniform(-math.pi, math.pi, 3)
            u = np.sqrt(1 - np.cos(theta))
            actual = float(np.sum(a * (1 - np.cos(theta))) -
                           z[0] * (1 - np.cos(theta[0] + theta[1])) -
                           z[1] * (1 - np.cos(theta[0] + theta[2])) -
                           z[2] * (1 - np.cos(theta[1] - theta[2])))
            bound = float(u @ mat @ u)
            assert actual + 1e-9 >= bound, (eps, actual, bound)
            assert bound >= -1e-9
    return {
        "status": "PASS_TOE63_SPECTRAL_DISORDER_SUFFICIENT_BOUND",
        "winding_octagon_count": int(sum(c.values())),
        "single_axis_counts": [79, 77, 77],
        "cross_axis_counts": [1, 1, 3],
        "cross_incidence_matrix": M.astype(int).tolist(),
        "diagonal_single_matrix": D.astype(int).tolist(),
        "positive_definiteness_polynomial": "(77-r)*(12*r^2-707*r+6083)",
        "critical_ratio_exact": "(707-sqrt(207865))/24",
        "critical_ratio": float(r_star),
        "old_sufficient_epsilon": float(previous),
        "improved_sufficient_epsilon": float(threshold),
        "eigenvalue_stress_checks": checks,
        "independent_coefficient_random_trials": 600,
        "theorem": "For any independent positive native W33 link magnitudes in [1-e,1+e], the leading beta^7 flat U(1)^3 fermion free-energy term has unique global minimum (pi,pi,pi) whenever e < (([707-sqrt(207865)]/24)^(1/8)-1)/(([707-sqrt(207865)]/24)^(1/8)+1).",
        "scope": "Sufficient worst-case mathematical bound only, not optimal tolerance, all-temperature ordering, interacting gauge selection, physical CP or empirical TOE.",
    }


if __name__ == "__main__":
    out = ROOT / "data/w33_20261013_toe63_spectral_flux_disorder.json"
    c = certificate()
    out.write_text(json.dumps(c, indent=2) + "\n", encoding="utf-8")
    print(c["status"], c["improved_sufficient_epsilon"])
