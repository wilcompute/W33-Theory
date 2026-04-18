"""Pin the partition function p(n), eta^{-1} generating series, and Hardy-Ramanujan.

Tests cover:
    (1) classical partition values p(0)=1, p(5)=7, p(50)=204226, p(100)=190569292;
    (2) Euler pentagonal recursion gives the correct p(n);
    (3) the product  phi(q) . (1 / phi(q))  =  1  as formal power series;
    (4) Hardy-Ramanujan asymptotic ratio  p(n) / (exp(pi sqrt(2n/3)) / (4 n sqrt 3))
        approaches 1 monotonically;
    (5) Ramanujan congruences mod 5, 7, 11 hold for at least 20 residues each;
    (6) eta^{-1}(q) coefficients match p(n) directly.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_partition_eta_inverse import (  # noqa: E402
    CLASSICAL_PARTITIONS,
    derive_all,
    eta_inverse_q_series,
    hardy_ramanujan_leading,
    partition,
    partition_list,
    verify_classical_partitions,
    verify_hardy_ramanujan,
    verify_pentagonal_identity,
    verify_ramanujan_congruences,
)


# ----------------------------------------------------------------------
# Small partition values (classical).
# ----------------------------------------------------------------------
def test_p_0_is_1():
    assert partition(0) == 1


def test_p_1_is_1():
    assert partition(1) == 1


def test_p_first_ten():
    assert partition_list(10) == [1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42]


def test_p_20_is_627():
    assert partition(20) == 627


def test_p_50_is_204226():
    assert partition(50) == 204226


def test_p_100_is_190569292():
    """MacMahon's classical value."""
    assert partition(100) == 190569292


def test_p_200_is_3972999029388():
    assert partition(200) == 3972999029388


def test_classical_table_matches():
    r = verify_classical_partitions()
    assert r["all_match"] is True
    assert r["discrepancies"] == []


# ----------------------------------------------------------------------
# eta^{-1} = generating series for p(n).
# ----------------------------------------------------------------------
def test_eta_inverse_equals_partition_list():
    assert eta_inverse_q_series(30) == partition_list(30)


def test_eta_inverse_constant_is_p_0_is_1():
    series = eta_inverse_q_series(5)
    assert series[0] == 1


# ----------------------------------------------------------------------
# Pentagonal identity:  phi(q) * (1 / phi(q)) = 1.
# ----------------------------------------------------------------------
def test_pentagonal_identity_holds():
    r = verify_pentagonal_identity(N=80)
    assert r["is_delta_series"] is True
    assert r["prod_first"][0] == 1
    assert r["prod_first"][1] == 0
    assert r["prod_first"][2] == 0


# ----------------------------------------------------------------------
# Hardy-Ramanujan asymptotic.
# ----------------------------------------------------------------------
def test_hardy_ramanujan_approaches_one():
    r = verify_hardy_ramanujan([20, 50, 100, 200, 400])
    ratios = [row["ratio"] for row in r["rows"]]
    # Ratio < 1 (leading term overestimates; correction factor (1 - something/n^.5))
    for ratio in ratios:
        assert 0 < ratio < 1
    # Each successive ratio is larger (closer to 1).
    for i in range(len(ratios) - 1):
        assert ratios[i] < ratios[i + 1]


def test_hardy_ramanujan_ratio_at_200_within_5_percent():
    rr = verify_hardy_ramanujan([200])
    abs_dev = rr["rows"][0]["abs_1_minus_ratio"]
    assert abs_dev < 0.05


def test_hardy_ramanujan_magnitude_at_100():
    """p(100) = 190569292;  leading HR estimate should be within 5% of this."""
    exact = partition(100)
    asymp = hardy_ramanujan_leading(100)
    assert 0.90 < exact / asymp < 1.0


# ----------------------------------------------------------------------
# Ramanujan congruences  p(5n+4) ≡ 0 (mod 5),  p(7n+5) ≡ 0 (mod 7),
# p(11n+6) ≡ 0 (mod 11).
# ----------------------------------------------------------------------
def test_ramanujan_mod_5_congruence():
    r = verify_ramanujan_congruences(max_k=20)
    assert r["mod_5_holds"] is True


def test_ramanujan_mod_7_congruence():
    r = verify_ramanujan_congruences(max_k=20)
    assert r["mod_7_holds"] is True


def test_ramanujan_mod_11_congruence():
    r = verify_ramanujan_congruences(max_k=20)
    assert r["mod_11_holds"] is True


def test_ramanujan_congruences_specific_values():
    # p(4) = 5, divisible by 5.
    assert partition(4) % 5 == 0
    # p(9) = 30, divisible by 5.
    assert partition(9) % 5 == 0
    # p(5) = 7, divisible by 7.
    assert partition(5) % 7 == 0
    # p(6) = 11, divisible by 11.
    assert partition(6) % 11 == 0


def test_all_three_congruences_hold():
    r = verify_ramanujan_congruences(max_k=20)
    assert r["all_three_hold"] is True
    assert r["failures"] == []


# ----------------------------------------------------------------------
# Classical reference check.
# ----------------------------------------------------------------------
def test_classical_partition_table_has_expected_keys():
    keys = sorted(CLASSICAL_PARTITIONS.keys())
    assert 0 in keys
    assert 100 in keys
    assert 200 in keys


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_driver_all_five_pins():
    s = derive_all()
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"
