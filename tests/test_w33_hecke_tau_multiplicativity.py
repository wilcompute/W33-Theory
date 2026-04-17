"""Pin Delta as a Hecke eigenform and tau's multiplicativity.

Tests cover:
    (1) T_p Delta = tau(p) Delta for small primes;
    (2) tau(m n) = tau(m) tau(n) for coprime (m, n);
    (3) tau(p^{k+1}) = tau(p) tau(p^k) - p^{11} tau(p^{k-1});
    (4) Ramanujan--Petersson: |tau(p)| < 2 p^{11/2};
    (5) Euler factor expansion matches prime-power tau values.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_hecke_tau_multiplicativity import (  # noqa: E402
    derive_all,
    hecke_T_p,
    tau_prime_catalogue,
    verify_euler_factor_prime_power,
    verify_hecke_eigenform,
    verify_prime_power_recursion,
    verify_ramanujan_petersson,
    verify_tau_multiplicativity,
)
from w33_ramanujan_system import delta_series  # noqa: E402


# ----------------------------------------------------------------------
# Hecke operator acting on Delta.
# ----------------------------------------------------------------------
def test_T2_Delta_equals_minus_24_Delta():
    delta = delta_series(60)
    T2 = hecke_T_p(delta, 2, 12, 25)
    expected = [-24 * delta[n] for n in range(26)]
    assert T2 == expected


def test_T3_Delta_equals_252_Delta():
    delta = delta_series(90)
    T3 = hecke_T_p(delta, 3, 12, 25)
    expected = [252 * delta[n] for n in range(26)]
    assert T3 == expected


def test_T5_Delta_equals_4830_Delta():
    delta = delta_series(150)
    T5 = hecke_T_p(delta, 5, 12, 25)
    expected = [4830 * delta[n] for n in range(26)]
    assert T5 == expected


def test_hecke_eigenform_driver_passes():
    r = verify_hecke_eigenform([2, 3, 5, 7, 11, 13], n_max=20)
    assert r["all_match"] is True


def test_hecke_eigenform_tau_p_values():
    r = verify_hecke_eigenform([2, 3, 5, 7], n_max=20)
    assert r["per_prime"][2]["tau_p"] == -24
    assert r["per_prime"][3]["tau_p"] == 252
    assert r["per_prime"][5]["tau_p"] == 4830
    assert r["per_prime"][7]["tau_p"] == -16744


# ----------------------------------------------------------------------
# tau multiplicativity.
# ----------------------------------------------------------------------
def test_tau_multiplicativity_holds_up_to_30():
    r = verify_tau_multiplicativity(n_max=30)
    assert r["all_match"] is True
    assert r["discrepancies"] == []


def test_tau_6_equals_tau_2_times_tau_3():
    delta = delta_series(10)
    assert delta[6] == delta[2] * delta[3]
    assert delta[6] == -24 * 252
    assert delta[6] == -6048


def test_tau_10_equals_tau_2_times_tau_5():
    delta = delta_series(15)
    assert delta[10] == delta[2] * delta[5]
    assert delta[10] == -24 * 4830
    assert delta[10] == -115920


def test_tau_15_equals_tau_3_times_tau_5():
    delta = delta_series(20)
    assert delta[15] == delta[3] * delta[5]
    assert delta[15] == 252 * 4830
    assert delta[15] == 1217160


def test_tau_21_equals_tau_3_times_tau_7():
    delta = delta_series(25)
    assert delta[21] == delta[3] * delta[7]
    assert delta[21] == 252 * -16744


# ----------------------------------------------------------------------
# Prime power recursion tau(p^{k+1}) = tau(p) tau(p^k) - p^11 tau(p^{k-1}).
# ----------------------------------------------------------------------
def test_prime_power_recursion_holds():
    r = verify_prime_power_recursion([2, 3, 5], max_k=4)
    assert r["all_match"] is True


def test_tau_4_equals_tau_2_squared_minus_2_to_11():
    delta = delta_series(5)
    assert delta[4] == delta[2] ** 2 - 2 ** 11
    assert delta[4] == 576 - 2048
    assert delta[4] == -1472


def test_tau_8_recursion():
    """tau(8) = tau(2) tau(4) - 2^11 tau(2) = -24 * -1472 - 2048 * -24."""
    delta = delta_series(10)
    expected = delta[2] * delta[4] - 2 ** 11 * delta[2]
    assert delta[8] == expected
    assert expected == 84480


def test_tau_9_equals_tau_3_squared_minus_3_to_11():
    delta = delta_series(10)
    assert delta[9] == delta[3] ** 2 - 3 ** 11
    assert delta[9] == 63504 - 177147
    assert delta[9] == -113643


def test_tau_25_equals_tau_5_squared_minus_5_to_11():
    delta = delta_series(30)
    assert delta[25] == delta[5] ** 2 - 5 ** 11
    assert delta[25] == 23328900 - 48828125


# ----------------------------------------------------------------------
# Ramanujan--Petersson bound |tau(p)| < 2 p^{11/2}.
# ----------------------------------------------------------------------
def test_ramanujan_petersson_holds_for_small_primes():
    r = verify_ramanujan_petersson([2, 3, 5, 7, 11, 13, 17, 19, 23])
    assert r["all_bounded"] is True


def test_ramanujan_petersson_tau_2():
    """tau(2)^2 = 576 < 4 * 2^11 = 8192."""
    delta = delta_series(3)
    assert delta[2] ** 2 == 576
    assert 4 * 2 ** 11 == 8192
    assert 576 < 8192


def test_ramanujan_petersson_tau_3():
    """tau(3)^2 = 63504 < 4 * 3^11 = 708588."""
    delta = delta_series(4)
    assert delta[3] ** 2 == 63504
    assert 4 * 3 ** 11 == 708588
    assert 63504 < 708588


# ----------------------------------------------------------------------
# Euler factor expansion.
# ----------------------------------------------------------------------
def test_euler_factor_p2_matches():
    r = verify_euler_factor_prime_power(2, max_k=5)
    assert r["match"] is True


def test_euler_factor_p3_matches():
    r = verify_euler_factor_prime_power(3, max_k=5)
    assert r["match"] is True


def test_euler_factor_p5_matches():
    r = verify_euler_factor_prime_power(5, max_k=4)
    assert r["match"] is True


# ----------------------------------------------------------------------
# Tau catalogue sanity.
# ----------------------------------------------------------------------
def test_tau_catalogue_first_values():
    c = tau_prime_catalogue(6)
    assert c["tau_p"][2] == -24
    assert c["tau_p"][3] == 252
    assert c["tau_p"][5] == 4830
    assert c["tau_p"][7] == -16744
    assert c["tau_p"][11] == 534612
    assert c["tau_p"][13] == -577738


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_driver_all_six_pins():
    s = derive_all(n_max=15)
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"
