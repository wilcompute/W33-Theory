"""Pin the Rogers-Ramanujan identities.

Tests cover:
    (1) G_sum == G_product and H_sum == H_product as q-series
        (the two RR identities proper);
    (2) G(q) counts partitions with parts ≡ ±1 (mod 5) and partitions
        with consecutive parts differing by >= 2 (Schur);
    (3) H(q) counts partitions with parts ≡ ±2 (mod 5) and the
        difference-2, smallest-part->=2 interpretation;
    (4) G(q) * H(q) * phi(q) = phi(q^5) as an eta-quotient identity
        (closing the ring with Layer 48);
    (5) Known OEIS first-10 coefficients for G (A003114) and H (A003106).
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_rogers_ramanujan import (  # noqa: E402
    derive_all,
    euler_phi,
    euler_phi_at_q5,
    partitions_diff_2_smallest_2,
    partitions_parts_pm1_mod5,
    partitions_parts_pm2_mod5,
    partitions_with_diff_at_least_2,
    rogers_ramanujan_G_product,
    rogers_ramanujan_G_sum,
    rogers_ramanujan_H_product,
    rogers_ramanujan_H_sum,
    verify_G_identity,
    verify_GH_product_equals_eta_quotient,
    verify_H_identity,
    verify_partition_interpretation_G,
    verify_partition_interpretation_H,
)


# ----------------------------------------------------------------------
# First Rogers-Ramanujan identity: G(q).
# ----------------------------------------------------------------------
def test_G_sum_equals_G_product_up_to_q40():
    r = verify_G_identity(N=40)
    assert r["all_match"] is True


def test_G_first_10_coefficients_are_OEIS_A003114():
    """G(q) = 1, q, q^2, q^3, 2q^4, 2q^5, 3q^6, ...  (A003114)."""
    G = rogers_ramanujan_G_sum(10)
    assert G == [1, 1, 1, 1, 2, 2, 3, 3, 4, 5]


def test_G_product_matches_direct_sum_at_n_20():
    Gs = rogers_ramanujan_G_sum(20)
    Gp = rogers_ramanujan_G_product(20)
    assert Gs == Gp


# ----------------------------------------------------------------------
# Second Rogers-Ramanujan identity: H(q).
# ----------------------------------------------------------------------
def test_H_sum_equals_H_product_up_to_q40():
    r = verify_H_identity(N=40)
    assert r["all_match"] is True


def test_H_first_10_coefficients_are_OEIS_A003106():
    """H(q) = 1, 0, q^2, q^3, q^4, q^5, 2q^6, ... (A003106)."""
    H = rogers_ramanujan_H_sum(10)
    assert H == [1, 0, 1, 1, 1, 1, 2, 2, 3, 3]


def test_H_product_matches_direct_sum_at_n_20():
    Hs = rogers_ramanujan_H_sum(20)
    Hp = rogers_ramanujan_H_product(20)
    assert Hs == Hp


def test_H_coefficient_of_q_is_zero():
    """H counts partitions with smallest part >= 2, so H[1] = 0."""
    H = rogers_ramanujan_H_sum(10)
    assert H[1] == 0


# ----------------------------------------------------------------------
# Partition interpretations for G.
# ----------------------------------------------------------------------
def test_G_counts_partitions_pm1_mod5_equals_distinct_diff_2():
    r = verify_partition_interpretation_G(n_max=20)
    assert r["all_match"] is True
    assert r["diff_equals_mod5"] is True
    assert r["counts_equal_series"] is True


def test_p_G_of_4_equals_2():
    """Partitions of 4 with parts differing by >= 2: {4}, {3+1} = 2."""
    p = partitions_with_diff_at_least_2(4)
    assert p[4] == 2


def test_partitions_of_6_with_diff_2():
    """6 = 6 = 5+1 = 4+2: 3 partitions."""
    p = partitions_with_diff_at_least_2(6)
    assert p[6] == 3


def test_partitions_of_6_with_parts_pm1_mod5():
    """Parts in {1,4,6,9,...}: 6 = 6 = 4+1+1 = 1+1+1+1+1+1: 3."""
    p = partitions_parts_pm1_mod5(6)
    assert p[6] == 3


# ----------------------------------------------------------------------
# Partition interpretations for H.
# ----------------------------------------------------------------------
def test_H_counts_partitions_pm2_mod5_equals_diff_2_min_2():
    r = verify_partition_interpretation_H(n_max=20)
    assert r["all_match"] is True


def test_p_H_of_6_equals_2():
    """6 with smallest >= 2 and diffs >= 2: {6}, {4+2}: 2."""
    p = partitions_diff_2_smallest_2(6)
    assert p[6] == 2


def test_H_count_matches_parts_pm2_mod5():
    """Parts in {2,3,7,8,...}: 6 = 3+3 = 2+2+2: 2."""
    p = partitions_parts_pm2_mod5(6)
    assert p[6] == 2


# ----------------------------------------------------------------------
# Eta-quotient ring closure: G * H * phi = phi(q^5).
# ----------------------------------------------------------------------
def test_GH_phi_equals_phi_q5():
    r = verify_GH_product_equals_eta_quotient(N=30)
    assert r["all_match"] is True


def test_phi_q5_has_zero_coefficient_between_pentagonal_at_q5():
    """phi(q^5) = sum (-1)^k q^{5 k(3k-1)/2}; first nonzero exponents
    at q^0 = 1 and q^5 = -1."""
    phi5 = euler_phi_at_q5(10)
    assert phi5[0] == 1
    assert phi5[5] == -1
    for i in [1, 2, 3, 4, 6, 7, 8, 9]:
        assert phi5[i] == 0


def test_phi_q_first_coefficients_pentagonal():
    """phi(q) = 1 - q - q^2 + q^5 + q^7 - q^{12} - ...."""
    phi = euler_phi(15)
    assert phi[0] == 1
    assert phi[1] == -1
    assert phi[2] == -1
    assert phi[3] == 0
    assert phi[4] == 0
    assert phi[5] == 1
    assert phi[7] == 1
    assert phi[12] == -1


# ----------------------------------------------------------------------
# Product-formula structure — mod 5 parts directly.
# ----------------------------------------------------------------------
def test_G_product_uses_only_parts_1_or_4_mod_5():
    """Building G by multiplying in parts m with m mod 5 in {1,4}
    should yield the same series."""
    direct = [0] * 20
    direct[0] = 1
    for m in range(1, 20):
        if m % 5 in (1, 4):
            for i in range(m, 20):
                direct[i] += direct[i - m]
    assert direct == rogers_ramanujan_G_product(20)


def test_H_product_uses_only_parts_2_or_3_mod_5():
    direct = [0] * 20
    direct[0] = 1
    for m in range(1, 20):
        if m % 5 in (2, 3):
            for i in range(m, 20):
                direct[i] += direct[i - m]
    assert direct == rogers_ramanujan_H_product(20)


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def test_driver_all_pins_green():
    s = derive_all()
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"


def test_driver_includes_subresults():
    s = derive_all()
    for key in [
        "G_identity",
        "H_identity",
        "G_partition_interpretation",
        "H_partition_interpretation",
        "GH_eta_quotient",
        "summary_chain",
    ]:
        assert key in s


def test_summary_chain_has_five_pins():
    s = derive_all()
    assert len(s["summary_chain"]) == 5
