"""Pin Dedekind sums, the eta transformation law on SL_2(Z), and the
Rademacher exact formula for p(n).

Tests cover:
    (1) Dedekind sum tabulated values;
    (2) Dedekind reciprocity for all coprime (h,k) up to k=20;
    (3) eta(tau+1) = exp(i pi/12) eta(tau)  numerically;
    (4) eta(-1/tau) = sqrt(-i tau) eta(tau)  numerically;
    (5) Truncated Rademacher series (K=25) rounds to the exact p(n);
    (6) Kloosterman-type A_1(n) = 1 for all n.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_dedekind_eta_transform import (  # noqa: E402
    A_k,
    DEDEKIND_SUM_TABLE,
    RADEMACHER_TARGETS,
    dedekind_reciprocity_gap,
    dedekind_sum,
    derive_all,
    rademacher_partition,
    verify_dedekind_table,
    verify_eta_inversion,
    verify_eta_translation,
    verify_rademacher,
    verify_reciprocity,
)


# ----------------------------------------------------------------------
# Dedekind sum tabulated values.
# ----------------------------------------------------------------------
def test_dedekind_s_1_1_is_0():
    assert dedekind_sum(1, 1) == 0


def test_dedekind_s_1_2_is_0():
    assert dedekind_sum(1, 2) == 0


def test_dedekind_s_1_3_is_1_over_18():
    assert dedekind_sum(1, 3) == Fraction(1, 18)


def test_dedekind_s_1_4_is_1_over_8():
    assert dedekind_sum(1, 4) == Fraction(1, 8)


def test_dedekind_s_1_5_is_1_over_5():
    assert dedekind_sum(1, 5) == Fraction(1, 5)


def test_dedekind_s_1_12_is_55_over_72():
    """Derived from reciprocity with s(12,1) = 0:
    s(1,12) = -1/4 + (1/12)(1/12 + 12 + 1/12) = 55/72."""
    assert dedekind_sum(1, 12) == Fraction(55, 72)


def test_dedekind_s_2_7_is_1_over_14():
    assert dedekind_sum(2, 7) == Fraction(1, 14)


def test_dedekind_s_3_7_is_minus_1_over_14():
    assert dedekind_sum(3, 7) == Fraction(-1, 14)


def test_dedekind_full_table_matches():
    r = verify_dedekind_table()
    assert r["all_match"] is True
    assert r["failures"] == []


# ----------------------------------------------------------------------
# Reciprocity s(h,k) + s(k,h) = -1/4 + (h/k + k/h + 1/(hk))/12.
# ----------------------------------------------------------------------
def test_reciprocity_small_example():
    # (h,k) = (2,5), coprime
    gap = dedekind_reciprocity_gap(2, 5)
    assert gap == 0


def test_reciprocity_all_coprime_up_to_k_20():
    r = verify_reciprocity(max_k=20)
    assert r["all_zero"] is True
    assert r["failures"] == []


def test_reciprocity_large_coprime():
    # Coprime (7, 11)
    assert dedekind_reciprocity_gap(7, 11) == 0


# ----------------------------------------------------------------------
# eta transformation: translation T: tau -> tau + 1.
# ----------------------------------------------------------------------
def test_eta_translation_multiplier():
    r = verify_eta_translation([0.1 + 0.5j, -0.3 + 0.8j, 0.7 + 1.2j])
    assert r["within_tol"] is True
    assert r["max_abs_err"] < 1e-25


def test_eta_translation_at_i():
    r = verify_eta_translation([1j])
    assert r["max_abs_err"] < 1e-25


# ----------------------------------------------------------------------
# eta transformation: inversion S: tau -> -1/tau.
# ----------------------------------------------------------------------
def test_eta_inversion_multiplier():
    r = verify_eta_inversion([0.1 + 0.5j, 0.3 + 0.8j, 0.7 + 1.2j])
    assert r["within_tol"] is True
    assert r["max_abs_err"] < 1e-20


def test_eta_inversion_at_i():
    """At tau = i: eta(i)/[sqrt(1) eta(i)] = 1 trivially; this is the
    fixed point of S, so a non-trivial check uses other points too."""
    r = verify_eta_inversion([1j])
    assert r["max_abs_err"] < 1e-20


# ----------------------------------------------------------------------
# Multiplier 24th-root structure: exp(i pi / 12) has order 24.
# ----------------------------------------------------------------------
def test_eta_translation_has_24th_order():
    """exp(i pi/12)^24 = exp(2 pi i) = 1.  This is THE 24 of moonshine."""
    import mpmath as mp
    mp.mp.dps = 40
    mult = mp.exp(1j * mp.pi / 12)
    assert abs(mult ** 24 - 1) < 1e-30
    # And no smaller n < 24 gives 1:
    for n in range(1, 24):
        assert abs(mult ** n - 1) > 1e-3


# ----------------------------------------------------------------------
# A_k(n) Kloosterman sum.
# ----------------------------------------------------------------------
def test_A_1_is_1():
    """A_1(n) = exp(0) = 1 for all n (only h=0)."""
    import mpmath as mp
    for n in [1, 5, 10, 50, 100]:
        assert abs(A_k(1, n) - 1) < mp.mpf("1e-30")


def test_A_2_n_is_real():
    """A_2(n) = exp(pi i s(1,2) - pi i n) = exp(-pi i n) = (-1)^n (since s(1,2)=0)."""
    import mpmath as mp
    for n in [1, 2, 3, 4, 5]:
        expected = (-1) ** n
        assert abs(A_k(2, n) - expected) < mp.mpf("1e-30")


# ----------------------------------------------------------------------
# Rademacher exact formula for p(n).
# ----------------------------------------------------------------------
def test_rademacher_p_5():
    approx = rademacher_partition(5, K=10)
    assert abs(float(approx) - 7) < 0.01


def test_rademacher_p_20():
    approx = rademacher_partition(20, K=15)
    assert int(round(float(approx))) == 627


def test_rademacher_p_100_exact():
    """p(100) = 190569292 recovered from K=25 Rademacher truncation."""
    approx = rademacher_partition(100, K=25)
    assert int(round(float(approx))) == 190569292


def test_rademacher_all_targets_match():
    r = verify_rademacher(K=25)
    assert r["all_match"] is True
    for row in r["rows"]:
        assert row["match"] is True


def test_rademacher_reference_targets_include_p_100():
    assert 100 in RADEMACHER_TARGETS
    assert RADEMACHER_TARGETS[100] == 190569292


# ----------------------------------------------------------------------
# Driver chain — all five pins green.
# ----------------------------------------------------------------------
def test_driver_five_pins_all_true():
    s = derive_all()
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"


def test_driver_includes_all_subresults():
    s = derive_all()
    for key in [
        "dedekind_table",
        "reciprocity",
        "eta_translation",
        "eta_inversion",
        "rademacher",
        "summary_chain",
    ]:
        assert key in s


# ----------------------------------------------------------------------
# Sanity: DEDEKIND_SUM_TABLE has expected entries.
# ----------------------------------------------------------------------
def test_dedekind_table_has_expected_keys():
    assert (1, 1) in DEDEKIND_SUM_TABLE
    assert (1, 12) in DEDEKIND_SUM_TABLE
    assert (5, 12) in DEDEKIND_SUM_TABLE
