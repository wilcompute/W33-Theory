"""Pin the nine Heegner discriminants and their CM j-values.

Tests cover:
    (1) the nine values { -3, -4, -7, -8, -11, -19, -43, -67, -163 }
        and their j-values (all integer cubes);
    (2) j(i) = 1728 = 12^3 = k_W33^3;
    (3) j((1+sqrt(-163))/2) = -640320^3 = -262537412640768000;
    (4) numeric q-series evaluation matches the algebraic integer for each D;
    (5) Ramanujan's near-integer  | e^{pi sqrt(163)} - (640320^3 + 744) | < 1e-9.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


import mpmath as mp  # noqa: E402

from w33_cm_j_values_heegner import (  # noqa: E402
    HEEGNER_TABLE,
    cube_structure_pins,
    derive_all,
    heegner_table,
    numerical_j_at_CM,
    verify_j_values_are_perfect_cubes,
    verify_low_D_numeric_matches,
    verify_ramanujan_constant,
)


# ----------------------------------------------------------------------
# Heegner discriminant table sanity.
# ----------------------------------------------------------------------
def test_heegner_count_is_nine():
    t = heegner_table()
    assert t["count"] == 9


def test_heegner_discriminants_match_classical():
    t = heegner_table()
    assert t["discriminants"] == [-3, -4, -7, -8, -11, -19, -43, -67, -163]


def test_heegner_table_j_values_match_classical():
    t = heegner_table()
    assert t["j_values"] == [
        0, 1728, -3375, 8000, -32768, -884736,
        -884736000, -147197952000, -262537412640768000,
    ]


def test_heegner_cube_roots_match_classical():
    t = heegner_table()
    assert t["cube_roots"] == [0, 12, -15, 20, -32, -96, -960, -5280, -640320]


# ----------------------------------------------------------------------
# Each j-value is the cube of the tabulated integer.
# ----------------------------------------------------------------------
def test_all_j_values_are_perfect_cubes():
    r = verify_j_values_are_perfect_cubes()
    assert r["all_match"] is True
    assert r["discrepancies"] == []


def test_j_at_i_is_12_cubed():
    """j(i) = 1728 = 12^3 = k_W33^3."""
    assert 1728 == 12 ** 3
    table = dict((D, j) for D, j, _ in HEEGNER_TABLE)
    assert table[-4] == 1728


def test_j_at_minus_163_is_minus_640320_cubed():
    table = dict((D, j) for D, j, _ in HEEGNER_TABLE)
    assert table[-163] == -262537412640768000
    assert -640320 ** 3 == -262537412640768000


def test_j_at_minus_67_is_minus_5280_cubed():
    table = dict((D, j) for D, j, _ in HEEGNER_TABLE)
    assert table[-67] == -5280 ** 3
    assert table[-67] == -147197952000


def test_j_at_minus_43_is_minus_960_cubed():
    table = dict((D, j) for D, j, _ in HEEGNER_TABLE)
    assert table[-43] == -960 ** 3


def test_j_at_minus_11_is_minus_32_cubed():
    table = dict((D, j) for D, j, _ in HEEGNER_TABLE)
    assert table[-11] == -32 ** 3
    assert table[-11] == -32768


def test_j_at_minus_8_is_20_cubed():
    table = dict((D, j) for D, j, _ in HEEGNER_TABLE)
    assert table[-8] == 20 ** 3
    assert table[-8] == 8000


def test_j_at_minus_7_is_minus_15_cubed():
    table = dict((D, j) for D, j, _ in HEEGNER_TABLE)
    assert table[-7] == -15 ** 3


def test_j_at_minus_3_is_zero():
    """j(rho) = 0, where rho = (1 + sqrt(-3))/2 is a primitive sixth root of unity."""
    table = dict((D, j) for D, j, _ in HEEGNER_TABLE)
    assert table[-3] == 0


# ----------------------------------------------------------------------
# Numeric q-series evaluation matches the algebraic integer.
# ----------------------------------------------------------------------
def test_numeric_j_matches_for_all_nine():
    r = verify_low_D_numeric_matches(threshold=1e-3)
    assert r["all_close"] is True


def test_numeric_j_at_minus_4_close_to_1728():
    """j(i) computed from q-series should match 1728."""
    j_num = numerical_j_at_CM(-4, dps=40, n_terms=7)
    diff = abs(j_num - 1728)
    assert float(diff) < 1e-3


def test_numeric_j_at_minus_163_close_to_target():
    """Tight check at -163 with high precision."""
    j_num = numerical_j_at_CM(-163, dps=80, n_terms=4)
    target = mp.mpf(-262537412640768000)
    diff = abs(j_num - target)
    assert float(diff / abs(target)) < 1e-15


# ----------------------------------------------------------------------
# Ramanujan's near-integer.
# ----------------------------------------------------------------------
def test_ramanujan_near_integer_within_1e_minus_9():
    r = verify_ramanujan_constant(dps=50)
    assert r["diff_lt_1e_minus_9"] is True


def test_ramanujan_near_integer_within_1e_minus_11():
    r = verify_ramanujan_constant(dps=50)
    assert r["diff_lt_1e_minus_11"] is True


def test_ramanujan_target_is_640320_cubed_plus_744():
    r = verify_ramanujan_constant(dps=50)
    assert r["target_640320_cubed_p744"] == 640320 ** 3 + 744
    assert r["target_640320_cubed_p744"] == 262537412640768744


# ----------------------------------------------------------------------
# Cube structure pins.
# ----------------------------------------------------------------------
def test_640320_cubed_value():
    s = cube_structure_pins()
    assert s["640320_cubed"] == 262537412640768000


def test_class_number_one_list_matches():
    s = cube_structure_pins()
    assert s["all_class_number_1_imag_quad"] == [-3, -4, -7, -8, -11, -19, -43, -67, -163]


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_driver_all_five_pins():
    s = derive_all()
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"
