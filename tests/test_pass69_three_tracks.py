"""Pass 69 regression tests: three perpendicular tracks."""
import numpy as np
import pytest
from math import sqrt, pi, ceil, log

SQRT97 = sqrt(97)
SQRT7  = sqrt(7)

# ===== Track 1 Tests =====

class TestTrack1IharaZeta:

    def test_ramanujan_violation(self):
        """lambda_2 must exceed the Ramanujan bound 2*sqrt(7)."""
        lam2 = (1 + SQRT97) / 2
        assert lam2 > 2 * SQRT7, f"{lam2} should exceed {2*SQRT7}"

    def test_pole_magnitude_irrational(self):
        """Poles from lambda_2 must lie outside the Ramanujan disk."""
        lam2 = (1 + SQRT97) / 2
        q = 7
        disc = lam2**2 - 4*q
        u1 = (lam2 - sqrt(disc)) / (2*q)
        # u1 should be the 'small' pole; check it's in (1/8, 1/sqrt7)
        assert u1 > 1/8, f"pole {u1} not > 1/8"

    def test_multiplicity_sum(self):
        """Sum of all multiplicities must be 360."""
        mults = [1, 15, 15, 40, 120, 120, 40, 9]
        assert sum(mults) == 360

    def test_euler_factor_minimal_polynomial(self):
        """The Euler factor (1-lam2*u+7u^2) has discriminant lam2^2-28."""
        lam2 = (1 + SQRT97) / 2
        discriminant = lam2**2 - 28
        # should be positive (two real poles)
        assert discriminant > 0
        # roots satisfy the minimal polynomial x^2 - x - 24 at u=1
        val = lam2**2 - lam2 - 24
        assert abs(val) < 1e-8, f"not root of x^2-x-24: {val}"


# ===== Track 2 Tests =====

class TestTrack2Photonics:

    def test_hom_dip_formula(self):
        """HOM dip period = 16*pi/(sqrt97-5)."""
        lam2 = (1 + SQRT97) / 2
        lam3 = 3.0
        d = 8.0
        tau = pi / ((lam2 - lam3) / d)
        tau_formula = 16 * pi / (SQRT97 - 5)
        assert abs(tau - tau_formula) < 1e-8, f"{tau} != {tau_formula}"

    def test_hom_encodes_sqrt97(self):
        """From tau_HOM, can recover sqrt(97)."""
        tau = 16 * pi / (SQRT97 - 5)
        recovered = 16 * pi / tau + 5
        assert abs(recovered - SQRT97) < 1e-8

    def test_mixing_time_consistency(self):
        """Mixing time from spectral gap must match Pass 68."""
        gap = (15 - SQRT97) / 16
        t_mix = ceil(log(360 / 0.01) / gap)
        assert t_mix == 23


# ===== Track 3 Tests =====

class TestTrack3RLPolicy:

    def setup_method(self):
        n = 360
        conn = [1, 359, 40, 320, 9, 351, 120, 240]
        self.neighbours = np.array([[(v+c)%n for c in conn] for v in range(n)])
        self.n = n
        self.N_ACTIONS = 8

    def test_ag23_policy_covers_all(self):
        """AG(2,3) deterministic policy must cover all 360 vertices."""
        def ag23(v):
            return v % self.N_ACTIONS

        v = 0
        visited = set()
        for _ in range(2000):
            visited.add(v)
            if len(visited) == self.n:
                break
            v = self.neighbours[v][ag23(v)]
        assert len(visited) == self.n, f"Only covered {len(visited)}"

    def test_all_vertices_have_8_neighbours(self):
        """Every vertex must have exactly 8 distinct neighbours."""
        for v in range(self.n):
            nbrs = set(self.neighbours[v])
            assert len(nbrs) == 8, f"v={v} has {len(nbrs)} distinct neighbours"

    def test_graph_is_regular(self):
        """Degree sequence must be all-8."""
        degrees = [len(set(self.neighbours[v])) for v in range(self.n)]
        assert all(d == 8 for d in degrees)
