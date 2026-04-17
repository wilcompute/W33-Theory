"""Pin Ogg's coincidence: Monster primes = supersingular primes.

Tests cover:
    (1) |M| factorization equals the classical 5.4e53 value;
    (2) the 15 prime divisors of |M| are exactly Ogg's 15 supersingular primes;
    (3) McKay's observation: 196884 = 1 + 196883;
    (4) the first four moonshine coefficients are sums of dim(M-irrep);
    (5) k_W33 = 12 sits between two Monster primes 11 and 13;
    (6) 2 k_W33 - 1 = 23 is a Monster prime.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_monster_ogg_supersingular import (  # noqa: E402
    MONSTER_ORDER_CLASSICAL,
    MONSTER_PRIME_POWERS,
    MONSTER_PRIMES,
    OGG_PRIMES,
    compare_with_heegner,
    derive_all,
    mckay_observation,
    monster_order_from_factorization,
    verify_monster_order_matches_classical,
    verify_monster_primes_equal_ogg_primes,
    verify_moonshine_decomposition,
    w33_k_signatures,
)


# ----------------------------------------------------------------------
# Monster order.
# ----------------------------------------------------------------------
def test_monster_order_classical_value():
    assert MONSTER_ORDER_CLASSICAL == 808017424794512875886459904961710757005754368000000000


def test_monster_order_from_factorization_matches():
    assert monster_order_from_factorization() == MONSTER_ORDER_CLASSICAL


def test_monster_order_driver():
    r = verify_monster_order_matches_classical()
    assert r["matches"] is True


def test_monster_order_log10_is_54_digits():
    """|M| ~ 8.08e53, so 54 decimal digits."""
    r = verify_monster_order_matches_classical()
    assert r["log10_approx"] == 54


# ----------------------------------------------------------------------
# Prime factorization.
# ----------------------------------------------------------------------
def test_monster_prime_powers_table():
    assert MONSTER_PRIME_POWERS == [
        (2, 46), (3, 20), (5, 9), (7, 6), (11, 2), (13, 3),
        (17, 1), (19, 1), (23, 1), (29, 1), (31, 1),
        (41, 1), (47, 1), (59, 1), (71, 1),
    ]


def test_monster_has_15_primes():
    assert len(MONSTER_PRIMES) == 15


def test_largest_monster_prime_is_71():
    assert max(MONSTER_PRIMES) == 71


def test_smallest_monster_prime_is_2():
    assert min(MONSTER_PRIMES) == 2


# ----------------------------------------------------------------------
# Ogg coincidence.
# ----------------------------------------------------------------------
def test_monster_primes_equal_ogg_primes():
    r = verify_monster_primes_equal_ogg_primes()
    assert r["matches"] is True
    assert r["count"] == 15


def test_ogg_primes_classical_list():
    assert OGG_PRIMES == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71]


def test_ogg_gaps_up_to_71():
    """Primes <= 71 NOT in Monster: {37, 43, 53, 61, 67}."""
    primes_to_71 = [p for p in range(2, 72) if all(p % d != 0 for d in range(2, p))]
    gaps = [p for p in primes_to_71 if p not in MONSTER_PRIMES]
    assert gaps == [37, 43, 53, 61, 67]


# ----------------------------------------------------------------------
# Moonshine decomposition.
# ----------------------------------------------------------------------
def test_moonshine_decomposition_holds():
    r = verify_moonshine_decomposition()
    assert r["all_match"] is True
    assert r["discrepancies"] == []


def test_mckay_observation_holds():
    m = mckay_observation()
    assert m["1_plus_196883_equals_196884"] is True
    assert m["smallest_faithful_M_rep_dim"] == 196883


def test_q2_coefficient_decomposition():
    """196884 = 1 + 196883."""
    assert 1 + 196883 == 196884


def test_q3_coefficient_decomposition():
    """21493760 = 1 + 196883 + 21296876."""
    assert 1 + 196883 + 21296876 == 21493760


def test_q4_coefficient_decomposition():
    """864299970 = 2 + 2*196883 + 21296876 + 842609326."""
    assert 2 + 2 * 196883 + 21296876 + 842609326 == 864299970


# ----------------------------------------------------------------------
# Heegner intersection.
# ----------------------------------------------------------------------
def test_heegner_monster_intersection():
    h = compare_with_heegner()
    expected = sorted(set([3, 7, 11, 19, 43, 67, 163]) & set(MONSTER_PRIMES))
    assert h["intersection"] == expected
    assert h["intersection"] == [3, 7, 11, 19]


def test_43_and_67_are_heegner_but_not_monster():
    """The Ogg gap primes 43 and 67 ARE Heegner |D|s, illustrating the
    Heegner / Monster duality."""
    h = compare_with_heegner()
    assert 43 in h["ogg_gap_primes_up_to_71_in_heegner"]
    assert 67 in h["ogg_gap_primes_up_to_71_in_heegner"]


# ----------------------------------------------------------------------
# k_W33 = 12 signatures.
# ----------------------------------------------------------------------
def test_k_W33_minus_1_and_plus_1_both_Monster_primes():
    w = w33_k_signatures()
    assert w["11_in_Monster_primes"] is True
    assert w["13_in_Monster_primes"] is True


def test_two_k_W33_minus_1_is_Monster_prime():
    w = w33_k_signatures()
    assert w["23_in_Monster_primes"] is True


def test_k_W33_itself_is_not_prime():
    """12 is composite, so it is NOT in the Monster prime list."""
    w = w33_k_signatures()
    assert w["k_W33_in_Monster_primes"] is False


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_driver_all_seven_pins():
    s = derive_all()
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"
