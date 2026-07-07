"""Pass 68 regression tests: spectral transport operator."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import numpy as np
import pytest

SQRT97 = math.sqrt(97)

def build_cheap_channel_adj():
    """360-vertex Cayley graph on Z9 x Z40."""
    n = 360
    conn = [1, 359, 40, 320, 9, 351, 120, 240]
    A = np.zeros((n, n), dtype=float)
    for v in range(n):
        for d in conn:
            w = (v + d) % n
            A[v][w] = 1.0
    return A


class TestPass68:

    def test_graph_regularity(self):
        """Graph must be exactly 8-regular."""
        A = build_cheap_channel_adj()
        degrees = A.sum(axis=1)
        assert np.allclose(degrees, 8.0), "Not 8-regular"

    def test_lambda_max(self):
        """Largest eigenvalue must be exactly 8."""
        A = build_cheap_channel_adj()
        eigs = np.sort(np.linalg.eigvalsh(A))[::-1]
        assert abs(eigs[0] - 8.0) < 1e-6, f"lambda_max = {eigs[0]}"

    def test_spectral_gap_exact(self):
        """Spectral gap must equal (15 - sqrt(97)) / 16."""
        A = build_cheap_channel_adj()
        eigs = np.sort(np.linalg.eigvalsh(A))[::-1]
        gap_computed = (eigs[0] - eigs[1]) / eigs[0]
        gap_exact = (15 - SQRT97) / 16
        assert abs(gap_computed - gap_exact) < 1e-5, (
            f"gap={gap_computed:.8f} != {gap_exact:.8f}"
        )

    def test_mixing_time_formula(self):
        """Mixing time formula at eps=0.01 must give 23 steps."""
        from math import log, ceil
        gap = (15 - SQRT97) / 16
        t_mix = ceil(log(360 / 0.01) / gap)
        assert t_mix == 23, f"t_mix = {t_mix} (expected 23)"

    def test_multiplicity_counts(self):
        """Irrational eigenvalues must each have multiplicity 15."""
        A = build_cheap_channel_adj()
        eigs = np.linalg.eigvalsh(A)
        tol = 1e-3
        lam2  = (1 + SQRT97) / 2
        lam_m = (1 - SQRT97) / 2
        mult2 = sum(1 for e in eigs if abs(e - lam2) < tol)
        multm = sum(1 for e in eigs if abs(e - lam_m) < tol)
        assert mult2 == 15, f"mult(lambda_2) = {mult2}"
        assert multm == 15, f"mult(lambda_-) = {multm}"
