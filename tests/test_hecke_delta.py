"""Pin the Hecke eigenform structure of Delta.

Three consequences:
  (1) Multiplicativity:      tau(mn) = tau(m) tau(n)     for gcd(m,n)=1.
  (2) Hecke recursion:       tau(p^{r+1}) = tau(p) tau(p^r) - p^11 tau(p^{r-1}).
  (3) Deligne bound:         |tau(p)| <= 2 p^{11/2}.

Together these reduce the infinite sequence {tau(n)} to {tau(p) : p prime},
each bounded by 2 p^{11/2}.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "exploration"))

from w33_hecke_delta import (  # noqa: E402
    derive_all_hecke,
    first_primes_up_to,
    reconstruct_tau_from_tau_p,
    tau,
    verify_deligne_bound,
    verify_hecke_recursion,
    verify_multiplicativity,
)


# ----------------------------------------------------------------------
# tau sanity: first values match published Ramanujan table.
# ----------------------------------------------------------------------
EXPECTED_TAU = {
    1:  1,
    2: -24,
    3:  252,
    4: -1472,
    5:  4830,
    6: -6048,
    7: -16744,
    8:  84480,
    9: -113643,
    10: -115920,
    11: 534612,
    12: -370944,
    13: -577738,
    14: 401856,
    15: 1217160,
}


@pytest.mark.parametrize("n,val", sorted(EXPECTED_TAU.items()))
def test_tau_of_n(n, val):
    assert tau(n) == val


# ----------------------------------------------------------------------
# (1) Multiplicativity on coprime arguments.
# ----------------------------------------------------------------------
COPRIME_PAIRS = [(2, 3), (2, 5), (3, 5), (3, 7), (2, 7), (5, 7),
                 (2, 9), (3, 4), (4, 9), (2, 15), (3, 20)]


@pytest.mark.parametrize("m,n", COPRIME_PAIRS)
def test_multiplicativity_on_coprime(m, n):
    r, = verify_multiplicativity([(m, n)])
    assert r["applicable"] is True
    assert r["match"] is True
    assert r["product"] == r["tau(mn)"]


def test_multiplicativity_not_applied_when_gcd_gt_1():
    """tau(2)*tau(4) != tau(8) because gcd(2,4) = 2, not coprime."""
    results = verify_multiplicativity([(2, 4)])
    r = results[0]
    assert r["applicable"] is False
    assert r["tau(mn)"] != r["product"]
    # Instead, Hecke recursion gives tau(4) = tau(2)^2 - 2^11 = 576 - 2048 = -1472.
    assert tau(2) ** 2 - 2 ** 11 == tau(4)


def test_tau_of_6_equals_tau_2_times_tau_3():
    """tau(6) = tau(2) * tau(3) = -24 * 252 = -6048."""
    assert tau(2) * tau(3) == tau(6)
    assert tau(6) == -6048


# ----------------------------------------------------------------------
# (2) Hecke recursion at prime powers.
#
# Choose r_max so p^{r+1} stays small (delta_qseries computation cost).
# ----------------------------------------------------------------------
@pytest.mark.parametrize("p,r_max", [(2, 7), (3, 4), (5, 2), (7, 2), (11, 1)])
def test_hecke_recursion_at_prime(p, r_max):
    results = verify_hecke_recursion(p, r_max=r_max)
    for r in results:
        assert r["match"] is True


def test_hecke_recursion_tau_4_equals_tau_2_squared_minus_2048():
    """The r=1 case at p=2:  tau(4) = tau(2)^2 - 2^11."""
    results = verify_hecke_recursion(2, r_max=1)
    r = results[0]
    assert r["r"] == 1
    assert r["tau(p^{r+1})"] == -1472
    assert r["predicted"] == tau(2) ** 2 - 2 ** 11
    assert r["match"] is True


def test_hecke_recursion_tau_9_from_tau_3():
    """At p=3, r=1:  tau(9) = tau(3)^2 - 3^11."""
    results = verify_hecke_recursion(3, r_max=1)
    r = results[0]
    assert r["tau(p^{r+1})"] == tau(9)
    assert r["predicted"] == 252 ** 2 - 3 ** 11
    assert tau(9) == 252 ** 2 - 3 ** 11


# ----------------------------------------------------------------------
# (3) Deligne bound:  |tau(p)| <= 2 p^{11/2}.
# ----------------------------------------------------------------------
@pytest.mark.parametrize("p", first_primes_up_to(30))
def test_deligne_bound(p):
    b = verify_deligne_bound(p)
    assert b["satisfies"] is True
    assert b["ratio"] <= 1.0
    assert b["|tau(p)|"] == abs(tau(p))


def test_deligne_ratios_nontrivial():
    """Ratios stay strictly below 1 and above 0."""
    for p in first_primes_up_to(30):
        b = verify_deligne_bound(p)
        assert 0.0 < b["ratio"] < 1.0


# ----------------------------------------------------------------------
# tau(n) reconstruction from {tau(p) : p prime} via Hecke.
# ----------------------------------------------------------------------
def test_reconstruction_n_up_to_20():
    primes = first_primes_up_to(20)
    recon = reconstruct_tau_from_tau_p(primes, n_max=20)
    for r in recon:
        assert r["match"] is True
        assert r["predicted"] == tau(r["n"])


def test_reconstruction_explicit_composites():
    """Spot-check composite reconstructions."""
    primes = first_primes_up_to(30)
    recon = reconstruct_tau_from_tau_p(primes, n_max=30)
    lookup = {r["n"]: r for r in recon}

    # n=12 = 2^2 * 3:  tau(12) = tau(4) * tau(3).
    r12 = lookup[12]
    assert r12["factorization"] == {2: 2, 3: 1}
    assert r12["predicted"] == tau(4) * tau(3)
    assert r12["predicted"] == -370944

    # n=25 = 5^2:  tau(25) = tau(5)^2 - 5^11.
    r25 = lookup[25]
    assert r25["factorization"] == {5: 2}
    assert r25["predicted"] == tau(5) ** 2 - 5 ** 11


def test_reconstruction_at_prime_returns_tau_p():
    primes = first_primes_up_to(30)
    recon = reconstruct_tau_from_tau_p(primes, n_max=30)
    lookup = {r["n"]: r for r in recon}
    for p in primes:
        r = lookup[p]
        assert r["factorization"] == {p: 1}
        assert r["predicted"] == tau(p)


# ----------------------------------------------------------------------
# Driver consistency.
# ----------------------------------------------------------------------
def test_driver_chain_all_match():
    chain = derive_all_hecke(n_max=30)
    assert chain["reconstruction_all_match"] is True
    assert chain["multiplicativity_all_match"] is True
    for _p, results in chain["hecke_recursion"].items():
        for r in results:
            assert r["match"] is True
    for _p, b in chain["deligne_bound"].items():
        assert b["satisfies"] is True


def test_first_primes_up_to_30():
    assert first_primes_up_to(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
