"""Pin the Rankin-Cohen bracket tower layer.

This layer shows two constructions of Delta:

    [E_4, E_6]_1 = -3456 * Delta  (weight-1 RC bracket),
    [E_4, E_4]_2 =  4800 * Delta  (weight-2 RC bracket).

The tests verify the coefficient identities, an explicit form for the
second bracket, and a short driver-chain that asserts all pins pass.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_rankin_cohen_tower import (
    derive_all,
    verify_rc_E4_E4_2,
    verify_rc_E4_E4_2_explicit_form,
    verify_rc_E4_E6_1,
    structural_interpretation,
    bracket_q1_calculations,
)


# ----------------------------------------------------------------------
# Rankin-Cohen bracket identities
# ----------------------------------------------------------------------
def test_rc_E4_E4_2_holds():
    r = verify_rc_E4_E4_2(n_max=25)
    assert r["all_match"] is True
    assert r["mismatches"] == []


def test_rc_E4_E4_2_explicit_form_holds():
    r = verify_rc_E4_E4_2_explicit_form(n_max=25)
    assert r["all_match"] is True


def test_rc_E4_E6_1_holds():
    r = verify_rc_E4_E6_1(n_max=25)
    assert r["all_match"] is True
    assert r["mismatches"] == []


def test_structural_interpretation():
    s = structural_interpretation()
    assert s["rc_2_equals_4800"] is True
    assert s["rc_1_equals_minus_3456"] is True


def test_q1_bracket_spot_checks():
    q = bracket_q1_calculations()
    assert q["[E_4,E_4]_2 at q1"] == 4800
    assert q["[E_4,E_6]_1 at q1"] == -3456


# ----------------------------------------------------------------------
# Driver chain
# ----------------------------------------------------------------------
def test_driver_all_eight_pins():
    s = derive_all(n_max=20)
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"
