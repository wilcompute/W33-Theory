"""Regression tests for Part CCCCCXXIV: Millennium Prize attack surfaces.

These tests verify finite W(3,3) analogues and status bookkeeping only.
They do not claim proofs of the six open Clay Millennium Prize Problems.
"""
from fractions import Fraction
import math


def atoms():
    q = 3
    lam = 2
    mu = 4
    k = q * (q + 1)
    v = (q + 1) * (q*q + 1)
    E = v*k//2
    r = lam
    s = -mu
    f = 24
    g = 15
    Phi3 = q*q + q + 1
    Phi4 = q*q + 1
    Phi6 = q*q - q + 1
    return q, lam, mu, k, v, E, r, s, f, g, Phi3, Phi4, Phi6


def test_status_count_compression():
    q, lam, mu, k, v, E, r, s, f, g, Phi3, Phi4, Phi6 = atoms()
    assert Phi6 == 7
    assert math.factorial(q) == 2*q == r-s == 6
    assert 1 + (r-s) == Phi6


def test_riemann_finite_ramanujan_surface():
    q, lam, mu, k, v, E, r, s, f, g, Phi3, Phi4, Phi6 = atoms()
    assert max(r*r, s*s) == 16
    assert 4*(k-1) == 44
    assert max(r*r, s*s) <= 4*(k-1)
    assert E - v == 200


def test_yang_mills_finite_gap_surface():
    q, lam, mu, k, v, E, r, s, f, g, Phi3, Phi4, Phi6 = atoms()
    assert k-r == Phi4 == 10
    assert mu == 4
    assert q*q - 1 == lam**q == 8


def test_navier_stokes_finite_dissipation_surface():
    q, lam, mu, k, v, E, r, s, f, g, Phi3, Phi4, Phi6 = atoms()
    assert k-r == 10
    assert Fraction(mu+1, q) == Fraction(5, 3)
    assert q == 3


def test_p_vs_np_finite_certificate_surface():
    q, lam, mu, k, v, E, r, s, f, g, Phi3, Phi4, Phi6 = atoms()
    assert v == 40
    assert lam > 0 and mu > 0  # diameter 2 for the SRG
    assert v + E == 280


def test_hodge_finite_cycle_surface():
    q, lam, mu, k, v, E, r, s, f, g, Phi3, Phi4, Phi6 = atoms()
    assert v - k - 1 == q**q == 27
    assert 2*f + 2*g == 78


def test_bsd_finite_arithmetic_surface():
    q, lam, mu, k, v, E, r, s, f, g, Phi3, Phi4, Phi6 = atoms()
    assert q**4 * (q**4 - 1) * (q**2 - 1) == 51840
    assert (k-1)**2 + mu**2 == Phi3*Phi4 + Phi6 == 137
    assert lam*q == 6


def test_poincare_topology_seed():
    q, lam, mu, k, v, E, r, s, f, g, Phi3, Phi4, Phi6 = atoms()
    assert q == 3
    assert lam**q == 8
    assert q + 1 == 4


def test_pair_partition():
    open_pairs = {
        "arithmetic_zeta": ["Riemann", "Birch-Swinnerton-Dyer"],
        "pde_gap_dissipation": ["Yang-Mills", "Navier-Stokes"],
        "certificate_cycle": ["P vs NP", "Hodge"],
    }
    all_open = sorted(sum(open_pairs.values(), []))
    assert len(all_open) == 6
    assert all_open == sorted(["Riemann", "Birch-Swinnerton-Dyer", "Yang-Mills", "Navier-Stokes", "P vs NP", "Hodge"])
