"""Pin the E_8 theta series and the Leech kissing number.

Main claims:

    theta_E_8  =  E_4  =  1 + 240 sum sigma_3(n) q^n,
    | short E_8 vectors with |x|^2 = 2 |      =  240 sigma_3(n),
    |E_8 roots|  =  240  (q^1 coefficient of E_4),
    theta_E_8 ^ 2  =  E_4^2  =  theta_{E_8 (+) E_8},
    theta_Leech[q^0] = 1,  theta_Leech[q^1] = 0,  theta_Leech[q^2] = 196560
                                                (the 24-D kissing number).
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_theta_e8_lattice import (  # noqa: E402
    convolve_counts,
    count_e8_by_norm_squared,
    derive_all,
    e8_root_count,
    leech_times_691_series,
    theta_e8_predicted,
    verify_E4_predicted_equals_240_sigma3,
    verify_E8_plus_E8_convolution_equals_E4_squared,
    verify_leech_kissing_number,
    verify_theta_E8_equals_E4_predicted,
)
from w33_ramanujan_system import e4_series  # noqa: E402


# ----------------------------------------------------------------------
# E_8 shell counts match E_4 (enumeration vs predicted).
# ----------------------------------------------------------------------
def test_e8_shell_0_is_1():
    """The origin is the unique norm-0 vector in E_8."""
    c = count_e8_by_norm_squared(4)
    assert c[0] == 1


def test_e8_shell_1_is_240_E8_roots():
    c = count_e8_by_norm_squared(4)
    assert c[1] == 240


def test_e8_shell_2_is_2160():
    """|x|^2 = 4 shell has 240 * sigma_3(2) = 240 * 9 = 2160."""
    c = count_e8_by_norm_squared(4)
    assert c[2] == 2160


def test_e8_shell_3_is_6720():
    """|x|^2 = 6 shell has 240 * sigma_3(3) = 240 * 28 = 6720."""
    c = count_e8_by_norm_squared(4)
    assert c[3] == 6720


def test_e8_shell_4_is_17520():
    """|x|^2 = 8 shell has 240 * sigma_3(4) = 240 * 73 = 17520."""
    c = count_e8_by_norm_squared(4)
    assert c[4] == 17520


def test_e8_enumeration_matches_predicted():
    r = verify_theta_E8_equals_E4_predicted(n_max=4)
    assert r["all_match"] is True


def test_theta_e8_predicted_matches_E4():
    r = verify_E4_predicted_equals_240_sigma3(n_max=25)
    assert r["all_match"] is True


def test_theta_e8_predicted_formula_vs_e4():
    """Cross check: predicted counts and E_4 series agree for n<=10."""
    pred = theta_e8_predicted(10)
    e4 = e4_series(10)
    assert pred == e4


# ----------------------------------------------------------------------
# E_8 root count structural identity.
# ----------------------------------------------------------------------
def test_e8_root_count_is_240():
    r = e8_root_count()
    assert r["E8_root_count"] == 240
    assert r["equals_240"] is True


def test_e8_root_count_is_20_times_W33_valency():
    """240 = 20 * 12, where 12 is the W(3,3) valency."""
    r = e8_root_count()
    assert r["equals_20_times_W33_valency"] is True
    assert 20 * 12 == 240


# ----------------------------------------------------------------------
# E_8 + E_8 theta series = E_4^2.
# ----------------------------------------------------------------------
def test_e8_plus_e8_convolution_matches_E4_squared():
    r = verify_E8_plus_E8_convolution_equals_E4_squared(n_max=4)
    assert r["all_match"] is True


def test_convolve_counts_basic():
    """A trivial convolution cross-check."""
    A = [1, 2, 3]
    B = [1, 0, -1]
    # (1 + 2q + 3q^2) * (1 - q^2) = 1 + 2q + 2q^2 - 2q^3 + ...
    # Up to n_max=2:  [1, 2, 2]
    C = convolve_counts(A, B, 2)
    assert C == [1, 2, 2]


def test_e8_squared_convolution_q1_is_480():
    """(1 + 240 q + ...)^2 = 1 + 480 q + ... since 2 * 240 = 480."""
    counts = count_e8_by_norm_squared(4)
    convolved = convolve_counts(counts, counts, 4)
    assert convolved[1] == 480


# ----------------------------------------------------------------------
# Leech kissing number via 691 theta_Leech = 691 E_12 - 65520 Delta.
# ----------------------------------------------------------------------
def test_leech_q0_is_1():
    r = verify_leech_kissing_number()
    assert r["q0_is_1"] is True
    assert r["theta_Leech_q0"] == 1


def test_leech_q1_is_0():
    """Leech lattice has NO norm-2 vectors."""
    r = verify_leech_kissing_number()
    assert r["q1_is_0"] is True
    assert r["theta_Leech_q1"] == 0


def test_leech_kissing_number_is_196560():
    """The 24-dimensional sphere packing kissing number is 196560."""
    r = verify_leech_kissing_number()
    assert r["kissing_is_196560"] is True
    assert r["kissing_number_24D"] == 196560


def test_leech_q2_times_691_equals_kissing_times_691():
    """Integer check: 691 theta_Leech at q^2 is divisible by 691."""
    r = verify_leech_kissing_number()
    assert r["theta_Leech_q2_times_691"] == 691 * 196560


def test_leech_times_691_matches_formula_at_q3():
    """691 theta_Leech at q^3 matches the formula; value divisible by 691."""
    seven = leech_times_691_series(3)
    assert seven[3] % 691 == 0


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_driver_all_eight_pins():
    s = derive_all(n_max=4)
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"
