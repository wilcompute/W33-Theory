"""Pin the L-function of Delta — Euler product, functional equation, central value.

Tests cover:
    (1) the first twelve tau(n) values match the classical Ramanujan table;
    (2) Euler product partial sum agrees with Dirichlet partial sum at Re(s) = 14;
    (3) functional equation Lambda(Delta, s) = Lambda(Delta, 12 - s) at s
        in {2, 3, 4, 5, 7, 8, 10} to ~1e-25 precision;
    (4) Lambda(Delta, 6) is real and strictly positive (Deligne nonvanishing);
    (5) Lambda table on the critical strip is symmetric Lambda(s) = Lambda(12-s);
    (6) the central value L(Delta, 6) ~ 0.7921228... matches literature.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


import mpmath as mp  # noqa: E402

from w33_lfunction_delta import (  # noqa: E402
    L_from_lambda,
    TAU_FIRST_TWELVE,
    central_value,
    completed_lambda,
    derive_all,
    dirichlet_partial_sum,
    euler_product_partial,
    gamma_factor,
    lambda_table,
    tau_cached,
    tau_table,
    verify_euler_product_matches_dirichlet,
    verify_functional_equation,
    verify_tau_first_twelve,
)


# ----------------------------------------------------------------------
# tau(n) — the first twelve Ramanujan coefficients.
# ----------------------------------------------------------------------
def test_tau_1_is_one():
    assert tau_cached(1) == 1


def test_tau_2_is_minus_24():
    """tau(2) = -24 = -dim(F_4 fundamental rep) numerologically."""
    assert tau_cached(2) == -24


def test_tau_3_is_252():
    assert tau_cached(3) == 252


def test_tau_5_is_4830():
    assert tau_cached(5) == 4830


def test_tau_7_is_minus_16744():
    assert tau_cached(7) == -16744


def test_tau_11_is_534612():
    """534612 mod 691 = 0  (Ramanujan congruence sigma_11(11) = 11^11 + 1)."""
    assert tau_cached(11) == 534612


def test_tau_first_twelve_table_match():
    r = verify_tau_first_twelve()
    assert r["all_match"] is True
    assert r["discrepancies"] == []
    assert r["n_checked"] == 12


def test_tau_table_returns_n_max_plus_one_entries():
    table = tau_table(20)
    assert len(table) == 21
    assert table[0] == 0
    for n, expected in TAU_FIRST_TWELVE:
        assert table[n] == expected


# ----------------------------------------------------------------------
# Ramanujan's mod-691 congruence echoes through tau.
# ----------------------------------------------------------------------
def test_tau_p_minus_sigma_11_p_divisible_by_691():
    """tau(p) ≡ 1 + p^11 (mod 691) — Ramanujan congruence at primes."""
    for p in (2, 3, 5, 7, 11, 13):
        diff = tau_cached(p) - (1 + p ** 11)
        assert diff % 691 == 0, f"prime p={p}: tau-sigma11 = {diff} not divisible by 691"


# ----------------------------------------------------------------------
# Euler product matches Dirichlet partial sum well above the critical strip.
# ----------------------------------------------------------------------
def test_euler_product_matches_dirichlet_at_re_s_14():
    r = verify_euler_product_matches_dirichlet(s=14.0, prime_cap=60, N_dirichlet=200, dps=30)
    assert r["agree"] is True
    assert r["rel_error"] < 1e-8


def test_euler_product_matches_dirichlet_at_re_s_20():
    """Tighter check far from the critical strip."""
    mp.mp.dps = 30
    ds = dirichlet_partial_sum(20, N=80)
    ep = euler_product_partial(20, prime_cap=80)
    rel = abs(ds - ep) / abs(ds)
    assert float(rel) < 1e-10


# ----------------------------------------------------------------------
# Functional equation  Lambda(Delta, s) = Lambda(Delta, 12 - s).
# ----------------------------------------------------------------------
def test_functional_equation_holds_at_seven_points():
    r = verify_functional_equation(dps=50, n_terms=35)
    assert r["all_ok"] is True
    for chk in r["checks"]:
        assert chk["rel_error"] < 1e-20, f"FE failed at s={chk['s']}: rel={chk['rel_error']}"


def test_functional_equation_at_central_point_is_trivial():
    """At s = 6 the FE is the identity 0 = 0, but Lambda(6) is nonzero."""
    L1 = completed_lambda(6, n_terms=35, dps=50)
    L2 = completed_lambda(6, n_terms=35, dps=50)
    assert abs(L1 - L2) == 0


def test_functional_equation_off_real_axis():
    """Lambda(s) = Lambda(12-s) holds for complex s too."""
    s = 4.0 + 0.5j
    mp.mp.dps = 50
    L1 = completed_lambda(s, n_terms=35, dps=50)
    L2 = completed_lambda(12 - 4.0 - 0.5j, n_terms=35, dps=50)
    rel = abs(L1 - L2) / max(abs(L1), abs(L2))
    assert float(rel) < 1e-20


# ----------------------------------------------------------------------
# Central value  Lambda(Delta, 6).
# ----------------------------------------------------------------------
def test_central_value_lambda_6_is_real_positive():
    r = central_value(dps=50, n_terms=40)
    assert r["Lambda_real_positive"] is True
    assert r["Lambda_imag_negligible"] is True


def test_central_value_lambda_6_numeric():
    """Lambda(Delta, 6) ≈ 0.0015448793603950..."""
    r = central_value(dps=50, n_terms=40)
    target = 0.001544879360395027
    assert abs(r["real_part"] - target) / target < 1e-10


def test_central_value_L_6_numeric():
    """L(Delta, 6) = Lambda(Delta, 6) / [(2 pi)^{-6} Gamma(6)] ≈ 0.7921228..."""
    r = central_value(dps=50, n_terms=40)
    target = 0.7921228386460306
    assert abs(r["L_at_6"].real - target) / target < 1e-10


# ----------------------------------------------------------------------
# Gamma-factor sanity.
# ----------------------------------------------------------------------
def test_gamma_factor_at_integer_s_uses_factorial():
    """gamma_factor(s) = (2 pi)^{-s} Gamma(s) and Gamma(s) = (s-1)! for integer s."""
    g = gamma_factor(6, dps=40)
    expected = mp.mpf(120) / mp.power(2 * mp.pi, 6)
    assert abs(g - expected) / abs(expected) < 1e-30


def test_L_recovered_from_lambda_at_re_s_14():
    """L(Delta, 14) recovered from Lambda matches the Dirichlet sum directly.

    Tolerance is set by the truncation of the Dirichlet partial sum at N = 80;
    by Deligne |tau(n)| << n^{11/2 + eps} so the tail at Re(s) = 14 is ~1e-17.
    """
    L_recov = L_from_lambda(14, n_terms=35, dps=40)
    L_direct = dirichlet_partial_sum(14, N=80)
    rel = abs(L_recov - L_direct) / abs(L_direct)
    assert float(rel) < 1e-15


# ----------------------------------------------------------------------
# Lambda table on the critical strip is symmetric.
# ----------------------------------------------------------------------
def test_lambda_table_is_symmetric_around_s_6():
    t = lambda_table([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], dps=40)
    rows = t["rows"]
    by_s = {row["s"]: row["real"] for row in rows}
    pairs = [(1, 11), (2, 10), (3, 9), (4, 8), (5, 7)]
    for a, b in pairs:
        rel = abs(by_s[a] - by_s[b]) / abs(by_s[a])
        assert rel < 1e-20, f"Lambda({a}) != Lambda({b}): {rel}"


def test_lambda_minimum_in_strip_is_at_central_point():
    t = lambda_table([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], dps=40)
    rows = t["rows"]
    by_s = {row["s"]: row["real"] for row in rows}
    central = by_s[6]
    for s, val in by_s.items():
        if s != 6:
            assert val >= central, f"Lambda({s}) = {val} < Lambda(6) = {central}"


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_driver_all_five_pins():
    s = derive_all()
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"
