"""TOE63 regression: exact spectral matrix and native winding census."""
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_20261013_toe63_spectral_flux_disorder import analytic_bounds, gap_matrix, certificate


def test_winding_counts_and_matrix_are_native():
    c, D, M, r, eps, old = analytic_bounds()
    assert sum(c.values()) == 238
    assert np.array_equal(np.diag(D), np.array([79, 77, 77]))
    assert np.array_equal(M, np.array([[2, 1, 1], [1, 4, 3], [1, 3, 4]]))
    assert abs((77 - r) * (12 * r*r - 707*r + 6083)) < 1e-8


def test_strict_spectral_improvement():
    c, D, M, r, eps, old = analytic_bounds()
    assert .145 < eps < .146
    assert .140 < old < .141
    assert eps > old
    assert np.linalg.eigvalsh(gap_matrix(.145, D, M))[0] > 0
    assert np.linalg.eigvalsh(gap_matrix(.146, D, M))[0] < 0


def test_coefficient_and_torus_stress():
    c = certificate()
    assert c["status"] == "PASS_TOE63_SPECTRAL_DISORDER_SUFFICIENT_BOUND"
    assert c["independent_coefficient_random_trials"] == 600
    assert c["winding_octagon_count"] == 238
    assert len(c["eigenvalue_stress_checks"]) == 5
