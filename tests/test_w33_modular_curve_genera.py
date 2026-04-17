"""Pin modular curve genera g_0(p), g_0+(p), and Ogg's classification.

Tests cover:
    (1) genus formula  g_0(p) = 1 + (p+1)/12 - e_2/4 - e_3/3 - 1
        matches the standard reference table for primes up to 100;
    (2) elliptic-point counts e_2(p) = 1 + (-1/p), e_3(p) = 1 + (-3/p);
    (3) g_0+(p) = 0  iff  p in {15 Monster primes};
    (4) the first prime with g_0+(p) > 0 is p = 37, with g_0+(37) = 1;
    (5) the Heegner gap primes 43 and 67 have g_0+(43) = 1, g_0+(67) = 2;
    (6) Legendre symbol consistency: (-1/p) and (-3/p) for sample primes.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_modular_curve_genera import (  # noqa: E402
    GENUS_PLUS_TABLE,
    GENUS_X0_REFERENCE,
    _e2,
    _e3,
    _cusps,
    derive_all,
    elliptic_point_table,
    genus_X0p,
    legendre_symbol,
    ogg_gap_genera,
    supersingular_primes_via_genus,
    verify_genus_formula_matches_reference,
    verify_ogg_classification,
)
from w33_monster_ogg_supersingular import MONSTER_PRIMES  # noqa: E402


# ----------------------------------------------------------------------
# Legendre symbol sanity.
# ----------------------------------------------------------------------
def test_legendre_minus_1_at_5_is_plus_1():
    """5 ≡ 1 (mod 4) so (-1/5) = +1."""
    assert legendre_symbol(-1, 5) == 1


def test_legendre_minus_1_at_3_is_minus_1():
    """3 ≡ 3 (mod 4) so (-1/3) = -1."""
    assert legendre_symbol(-1, 3) == -1


def test_legendre_minus_1_at_13_is_plus_1():
    assert legendre_symbol(-1, 13) == 1


def test_legendre_minus_3_at_7_is_plus_1():
    """7 ≡ 1 (mod 3) so (-3/7) = +1."""
    assert legendre_symbol(-3, 7) == 1


def test_legendre_minus_3_at_5_is_minus_1():
    """5 ≡ 2 (mod 3) so (-3/5) = -1."""
    assert legendre_symbol(-3, 5) == -1


# ----------------------------------------------------------------------
# Elliptic-point counts.
# ----------------------------------------------------------------------
def test_e2_at_p_equals_1_plus_legendre():
    for p in (3, 5, 7, 11, 13, 17, 19, 23):
        assert _e2(p) == 1 + legendre_symbol(-1, p)


def test_e2_at_2_is_1():
    assert _e2(2) == 1


def test_e3_at_p_equals_1_plus_legendre():
    for p in (5, 7, 11, 13, 17, 19, 23, 29):
        assert _e3(p) == 1 + legendre_symbol(-3, p)


def test_e3_at_3_is_1():
    assert _e3(3) == 1


def test_e3_at_2_is_0():
    assert _e3(2) == 0


def test_cusps_is_always_2_for_prime_level():
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71):
        assert _cusps(p) == 2


# ----------------------------------------------------------------------
# Genus of X_0(p) via the explicit formula.
# ----------------------------------------------------------------------
def test_genus_X0_at_2_3_5_7_13_is_zero():
    for p in (2, 3, 5, 7, 13):
        assert genus_X0p(p) == 0


def test_genus_X0_at_11_is_1():
    assert genus_X0p(11) == 1


def test_genus_X0_at_37_is_2():
    """X_0(37) is the famous first elliptic curve modular curve."""
    assert genus_X0p(37) == 2


def test_genus_X0_at_71_is_6():
    assert genus_X0p(71) == 6


def test_genus_formula_matches_reference_table():
    r = verify_genus_formula_matches_reference()
    assert r["all_match"] is True
    assert r["discrepancies"] == []
    assert r["n_primes_checked"] == len(GENUS_X0_REFERENCE)


# ----------------------------------------------------------------------
# Ogg's classification.
# ----------------------------------------------------------------------
def test_g0_plus_eq_0_iff_monster_prime():
    r = verify_ogg_classification()
    assert r["matches"] is True
    assert r["count_via_genus"] == 15
    assert r["count_via_monster"] == 15


def test_supersingular_primes_via_genus_are_monster_primes():
    via_genus = supersingular_primes_via_genus()
    assert via_genus == sorted(MONSTER_PRIMES)
    assert len(via_genus) == 15


def test_supersingular_primes_set_pinned():
    via_genus = supersingular_primes_via_genus()
    assert via_genus == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71]


# ----------------------------------------------------------------------
# Ogg gap analysis.
# ----------------------------------------------------------------------
def test_first_prime_with_pos_g0_plus_is_37():
    assert GENUS_PLUS_TABLE[37] == 1
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31):
        assert GENUS_PLUS_TABLE[p] == 0


def test_g0_plus_at_43_is_1():
    """43 is a Heegner discriminant but NOT a Monster prime — g_0+(43) = 1."""
    assert GENUS_PLUS_TABLE[43] == 1


def test_g0_plus_at_67_is_2():
    """67 is a Heegner discriminant but NOT a Monster prime — g_0+(67) = 2."""
    assert GENUS_PLUS_TABLE[67] == 2


def test_ogg_gap_primes_are_37_43_53_61_67():
    g = ogg_gap_genera()
    assert g["ogg_gap_primes"] == [37, 43, 53, 61, 67]


def test_all_ogg_gap_primes_have_positive_g0_plus():
    g = ogg_gap_genera()
    assert g["all_gap_genera_pos"] is True
    for p, gp in g["g0_plus_at_gap"].items():
        assert gp >= 1, f"Ogg gap prime {p} has g_0+(p) = {gp}, not > 0"


# ----------------------------------------------------------------------
# Elliptic-point summary table.
# ----------------------------------------------------------------------
def test_elliptic_point_table_has_20_primes_up_to_71():
    t = elliptic_point_table(primes_up_to=71)
    assert len(t["rows"]) == 20  # primes 2..71


def test_elliptic_point_table_records_genus_correctly():
    t = elliptic_point_table(primes_up_to=71)
    by_p = {row["p"]: row for row in t["rows"]}
    assert by_p[71]["g_0(p)"] == 6
    assert by_p[71]["g_0+(p)"] == 0
    assert by_p[37]["g_0+(p)"] == 1


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_driver_all_six_pins():
    s = derive_all()
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"
