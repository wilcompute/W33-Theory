"""Pin Ramanujan's three partition congruences and Euler's recurrence.

Tests cover:
    (1) p(n) for n = 0..10 matches OEIS A000041;
    (2) Pentagonal-number recurrence matches OEIS table up to N = 200;
    (3) p(5n + 4)  ≡ 0 mod 5  for n = 0..500;
    (4) p(7n + 5)  ≡ 0 mod 7  for n = 0..500;
    (5) p(11n + 6) ≡ 0 mod 11 for n = 0..200;
    (6) No congruence at modulus 13: every residue class has nonvanishing;
    (7) Hardy-Ramanujan asymptotic at n = 1000 has relative error < 2%;
    (8) Specific p(100) = 190569292; p(200) = 3972999029388.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_partition_congruences import (  # noqa: E402
    derive_all,
    p,
    p_asymptotic,
    partition_table,
    pentagonals,
    verify_hardy_ramanujan_asymptotic,
    verify_pentagonal_recursion_against_standard,
    verify_p_small_values,
    verify_R5,
    verify_R5_first_spot_check,
    verify_R7,
    verify_R11,
    verify_R13_has_no_congruence,
)


# ----------------------------------------------------------------------
# Partition values.
# ----------------------------------------------------------------------
def test_p_0_is_1():
    assert p(0) == 1


def test_p_4_is_5():
    """Five partitions of 4: 4 | 3+1 | 2+2 | 2+1+1 | 1+1+1+1."""
    assert p(4) == 5


def test_p_10_is_42():
    """A famous number."""
    assert p(10) == 42


def test_p_100_is_190569292():
    assert p(100) == 190569292


def test_p_200_is_3972999029388():
    assert p(200) == 3972999029388


def test_small_values_verifier():
    r = verify_p_small_values()
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Pentagonal numbers and recurrence.
# ----------------------------------------------------------------------
def test_pentagonals_list():
    pairs = pentagonals(30)
    vals = sorted({g for _, g in pairs})
    # Generalised pentagonals up to 30: 1, 2, 5, 7, 12, 15, 22, 26
    assert vals[:8] == [1, 2, 5, 7, 12, 15, 22, 26]


def test_recursion_matches_OEIS():
    r = verify_pentagonal_recursion_against_standard(N=200)
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Ramanujan congruences.
# ----------------------------------------------------------------------
def test_R5_at_n_0():
    """p(4) = 5 ≡ 0 mod 5."""
    assert p(4) % 5 == 0


def test_R5_at_n_5():
    """p(29) = 4565 ≡ 0 mod 5."""
    assert p(29) == 4565
    assert p(29) % 5 == 0


def test_R5_full():
    r = verify_R5(N_max=500)
    assert r["all_match"] is True


def test_R7_at_n_0():
    """p(5) = 7 ≡ 0 mod 7."""
    assert p(5) == 7
    assert p(5) % 7 == 0


def test_R7_at_n_2():
    """p(19) = 490 = 7 * 70 ≡ 0 mod 7."""
    assert p(19) == 490
    assert p(19) % 7 == 0


def test_R7_full():
    r = verify_R7(N_max=500)
    assert r["all_match"] is True


def test_R11_at_n_0():
    """p(6) = 11 ≡ 0 mod 11."""
    assert p(6) == 11
    assert p(6) % 11 == 0


def test_R11_at_n_1():
    """p(17) = 297 = 11 * 27 ≡ 0 mod 11."""
    assert p(17) == 297
    assert p(17) % 11 == 0


def test_R11_full():
    r = verify_R11(N_max=200)
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Absence of mod-13 congruence.
# ----------------------------------------------------------------------
def test_no_mod_13_congruence():
    r = verify_R13_has_no_congruence()
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Hardy-Ramanujan asymptotic.
# ----------------------------------------------------------------------
def test_hardy_ramanujan_at_1000():
    r = verify_hardy_ramanujan_asymptotic(n_test=1000, tol_rel=0.02)
    assert r["match"] is True


def test_asymptotic_is_positive():
    assert p_asymptotic(100) > 0
    assert p_asymptotic(1000) > 0


# ----------------------------------------------------------------------
# R5 first spot checks.
# ----------------------------------------------------------------------
def test_R5_spot_check():
    r = verify_R5_first_spot_check()
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_driver_all_pins_green():
    s = derive_all()
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"


def test_driver_subresults():
    s = derive_all()
    for key in [
        "small_values",
        "recursion",
        "R5",
        "R7",
        "R11",
        "spot",
        "no_13_congruence",
        "hardy_ramanujan",
        "summary_chain",
    ]:
        assert key in s


def test_summary_chain_has_eight_pins():
    s = derive_all()
    assert len(s["summary_chain"]) == 8


def test_partition_table_length():
    tab = partition_table(50)
    assert len(tab) == 51  # 0..50 inclusive
