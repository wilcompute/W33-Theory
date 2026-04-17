"""Pin the 24 Niemeier lattices and the rank-12 theta collapse.

Tests cover:
    (1) exactly 24 Niemeier lattices, each of rank 24 (Leech rank 0 / no roots);
    (2) ADE root counts: |A_n|=n(n+1), |D_n|=2n(n-1), |E_6|=72, |E_7|=126, |E_8|=240;
    (3) theta_L = E_4^3 + (h - 720) Delta for each Niemeier with root count h;
    (4) the 24 lattices have only 19 distinct theta series (5 collision pairs);
    (5) theta_{E_8^3} = E_4^3, theta_{Leech} = E_4^3 - 720 Delta;
    (6) Layer 37 cross-check: theta_{Leech}[q^2] = 196560 (kissing number).
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_niemeier_lattices import (  # noqa: E402
    NIEMEIER,
    derive_all,
    niemeier_root_table,
    root_count,
    roots_A,
    roots_D,
    roots_E,
    theta_collisions,
    theta_niemeier,
    total_rank,
    verify_E8_cubed_theta_equals_E4_cubed,
    verify_all_have_rank_24,
    verify_leech_theta_matches_layer_37,
    verify_theta_root_count_pin,
    verify_total_count_is_24,
)
from w33_ramanujan_system import e4_series, series_mul  # noqa: E402


# ----------------------------------------------------------------------
# Counting and rank checks.
# ----------------------------------------------------------------------
def test_total_count_is_24():
    r = verify_total_count_is_24()
    assert r["equals_24"] is True


def test_all_have_rank_24():
    r = verify_all_have_rank_24()
    assert r["all_match"] is True


def test_leech_has_rank_0_no_root_data():
    """Leech has no roots; we encode this as an empty root system / rank 0."""
    label, decomp = NIEMEIER[0]
    assert label == "Leech"
    assert total_rank(decomp) == 0
    assert root_count(decomp) == 0


def test_24_lattices_in_table():
    assert len(NIEMEIER) == 24


# ----------------------------------------------------------------------
# ADE root counts.
# ----------------------------------------------------------------------
def test_roots_A_formula():
    assert roots_A(1) == 2
    assert roots_A(2) == 6
    assert roots_A(8) == 72
    assert roots_A(24) == 600


def test_roots_D_formula():
    assert roots_D(4) == 24
    assert roots_D(8) == 112
    assert roots_D(24) == 1104


def test_roots_E_lookup():
    assert roots_E(6) == 72
    assert roots_E(7) == 126
    assert roots_E(8) == 240


# ----------------------------------------------------------------------
# Specific Niemeier root counts.
# ----------------------------------------------------------------------
def test_A1_24_has_48_roots():
    """A_1^24 has 24 * 2 = 48 roots."""
    decomp = [("A", 1, 24)]
    assert root_count(decomp) == 48


def test_E8_cubed_has_720_roots():
    decomp = [("E", 8, 3)]
    assert root_count(decomp) == 720


def test_D24_has_1104_roots():
    decomp = [("D", 24, 1)]
    assert root_count(decomp) == 1104


def test_A24_has_600_roots():
    decomp = [("A", 24, 1)]
    assert root_count(decomp) == 600


def test_leech_has_0_roots():
    assert root_count([]) == 0


# ----------------------------------------------------------------------
# Theta-series formula.
# ----------------------------------------------------------------------
def test_theta_root_count_pin_holds():
    r = verify_theta_root_count_pin(n_max=8)
    assert r["all_match"] is True


def test_theta_niemeier_constant_term_is_1():
    for h in (0, 48, 240, 720, 1104):
        th = theta_niemeier(h, 5)
        assert th[0] == 1


def test_theta_niemeier_q1_equals_h():
    for h in (0, 48, 72, 240, 720, 1104):
        th = theta_niemeier(h, 5)
        assert th[1] == h


def test_theta_E8_cubed_equals_E4_cubed():
    r = verify_E8_cubed_theta_equals_E4_cubed(n_max=8)
    assert r["all_match"] is True


def test_theta_E8_cubed_q1_is_720():
    e4 = e4_series(3)
    e4_cubed = series_mul(series_mul(e4, e4, 3), e4, 3)
    assert e4_cubed[1] == 720


# ----------------------------------------------------------------------
# Leech consistency with Layer 37.
# ----------------------------------------------------------------------
def test_leech_q1_is_zero_no_norm_2_vectors():
    th = theta_niemeier(0, 5)
    assert th[1] == 0


def test_leech_q2_is_kissing_196560():
    th = theta_niemeier(0, 5)
    assert th[2] == 196560


def test_leech_pin_driver():
    r = verify_leech_theta_matches_layer_37(n_max=4)
    assert r["matches_layer_37"] is True


# ----------------------------------------------------------------------
# Theta collisions: 24 → 19.
# ----------------------------------------------------------------------
def test_theta_collisions_collapse_24_to_19():
    c = theta_collisions()
    assert c["collapse_24_to_19"] is True
    assert c["n_distinct_thetas"] == 19
    assert c["n_lattices"] == 24


def test_five_collision_pairs():
    c = theta_collisions()
    expected_pairs = {
        144: ["D4^6", "A5^4 D4"],
        240: ["A9^2 D6", "D6^4"],
        288: ["E6^4", "A11 D7 E6"],
        432: ["A17 E7", "D10 E7^2"],
        720: ["E8^3", "D16 E8"],
    }
    for h, labels in expected_pairs.items():
        assert h in c["collisions"]
        # Order can differ; compare as sets.
        assert set(c["collisions"][h]) == set(labels)


def test_collision_h_values():
    c = theta_collisions()
    assert c["collision_root_counts"] == [144, 240, 288, 432, 720]


# ----------------------------------------------------------------------
# Niemeier root table extremes.
# ----------------------------------------------------------------------
def test_min_root_count_is_0_leech():
    t = niemeier_root_table()
    assert t["extremes"]["leech_h_0"] == 0


def test_max_root_count_is_1104_D24():
    t = niemeier_root_table()
    assert t["extremes"]["max_h_1104"] == 1104


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_driver_all_six_pins():
    s = derive_all()
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"
