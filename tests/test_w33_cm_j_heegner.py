"""Pin CM j-invariant values at Heegner points and the
e^{pi sqrt(d)}-near-integer phenomenon.

Tests cover:
    (1) j(tau_d) evaluates to the classical integer for each of the
        nine Heegner numbers;
    (2) each j(tau_d) equals H_d^3 for the known integer H_d;
    (3) e^{pi sqrt(163)} is within 1e-12 of 640320^3 + 744
        (Ramanujan's almost-integer);
    (4) smaller near-integer deviations for d = 67, 43 within expected
        magnitudes.
"""

from __future__ import annotations

import sys
from pathlib import Path

import mpmath as mp


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_cm_j_heegner import (  # noqa: E402
    HEEGNER_CUBE_ROOTS,
    HEEGNER_J_VALUES,
    HEEGNER_NUMBERS,
    derive_all,
    heegner_q,
    heegner_tau,
    j_at_heegner,
    near_integer_ramanujan,
    verify_heegner_cubes,
    verify_heegner_j_values,
    verify_ramanujan_163_almost_integer,
)


# ----------------------------------------------------------------------
# Heegner number metadata.
# ----------------------------------------------------------------------
def test_heegner_numbers_are_the_classical_nine():
    assert HEEGNER_NUMBERS == [1, 2, 3, 7, 11, 19, 43, 67, 163]


def test_j_at_i_is_1728():
    assert HEEGNER_J_VALUES[1] == 1728 == 12 ** 3


def test_j_at_rho_is_0():
    assert HEEGNER_J_VALUES[3] == 0


def test_j_at_tau_163_is_minus_640320_cubed():
    assert HEEGNER_J_VALUES[163] == -(640320 ** 3)
    assert HEEGNER_J_VALUES[163] == -262537412640768000


# ----------------------------------------------------------------------
# Cube structure.
# ----------------------------------------------------------------------
def test_all_heegner_j_are_cubes():
    r = verify_heegner_cubes()
    assert r["all_match"] is True
    for row in r["rows"]:
        assert row["match"] is True


def test_heegner_cube_roots_squarefree_pattern():
    """Each |H_d| has a factorisation pattern tied to class-field theory."""
    assert HEEGNER_CUBE_ROOTS[1] == 12      # 2^2 . 3
    assert HEEGNER_CUBE_ROOTS[7] == -15     # -(3 . 5)
    assert HEEGNER_CUBE_ROOTS[11] == -32    # -(2^5)
    assert HEEGNER_CUBE_ROOTS[19] == -96    # -(2^5 . 3)
    assert HEEGNER_CUBE_ROOTS[43] == -960   # -(2^6 . 15) = -(2^6 . 3 . 5)
    assert HEEGNER_CUBE_ROOTS[67] == -5280  # -(2^5 . 3 . 5 . 11)
    assert HEEGNER_CUBE_ROOTS[163] == -640320  # -(2^6 . 3 . 5 . 23 . 29)


# ----------------------------------------------------------------------
# Numerical evaluation at Heegner points.
# ----------------------------------------------------------------------
def test_j_at_i_numerically_rounds_to_1728():
    mp.mp.dps = 50
    j = j_at_heegner(1)
    assert abs(j.real - 1728) < 1e-20
    assert abs(j.imag) < 1e-20


def test_j_at_heegner_7_rounds_to_minus_3375():
    mp.mp.dps = 50
    j = j_at_heegner(7)
    assert abs(j.real - (-3375)) < 1e-20
    assert abs(j.imag) < 1e-10


def test_j_at_heegner_163_rounds_to_minus_640320_cubed():
    mp.mp.dps = 60
    j = j_at_heegner(163)
    assert abs(j.real - HEEGNER_J_VALUES[163]) < 1  # integer match


def test_all_heegner_j_evaluate_correctly():
    r = verify_heegner_j_values(dps=60)
    assert r["all_match"] is True
    for row in r["rows"]:
        assert row["match"] is True, f"d={row['d']} failed"


# ----------------------------------------------------------------------
# tau_d and q_d.
# ----------------------------------------------------------------------
def test_tau_1_is_i():
    mp.mp.dps = 30
    tau = heegner_tau(1)
    assert abs(tau.real) < 1e-25
    assert abs(tau.imag - 1) < 1e-25


def test_tau_3_is_half_plus_i_sqrt3_over_2():
    mp.mp.dps = 30
    tau = heegner_tau(3)
    assert abs(tau.real - 0.5) < 1e-25
    assert abs(tau.imag - mp.sqrt(3) / 2) < 1e-25


def test_q_163_is_tiny_negative_real():
    """For d = 163, q = -exp(-pi sqrt(163)) ~ -3e-18."""
    mp.mp.dps = 40
    q = heegner_q(163)
    assert q.real < 0
    assert abs(q.real) < 1e-15
    assert abs(q.imag) < 1e-15


# ----------------------------------------------------------------------
# Ramanujan's e^{pi sqrt 163} almost-integer.
# ----------------------------------------------------------------------
def test_ramanujan_163_deviation_within_1e_12():
    r = verify_ramanujan_163_almost_integer(dps=40)
    assert r["within_1e_12"] is True
    assert r["within_1e_9"] is True


def test_ramanujan_163_deviation_is_negative():
    """e^{pi sqrt 163} < 640320^3 + 744 by ~7.5e-13."""
    r = verify_ramanujan_163_almost_integer(dps=40)
    assert r["deviation"] < 0


def test_ramanujan_67_deviation_within_1e_5():
    """e^{pi sqrt 67} ~ 5280^3 + 744 to ~1e-6."""
    mp.mp.dps = 40
    nr = near_integer_ramanujan(67, dps=40)
    dev = float(nr["deviation"]) if isinstance(nr["deviation"], (int, float)) else float(mp.mpf(nr["deviation"]))
    assert abs(dev) < 1e-5


def test_ramanujan_43_deviation_within_1e_3():
    """e^{pi sqrt 43} ~ 960^3 + 744 to ~2e-4."""
    mp.mp.dps = 40
    nr = near_integer_ramanujan(43, dps=40)
    dev = float(nr["deviation"]) if isinstance(nr["deviation"], (int, float)) else float(mp.mpf(nr["deviation"]))
    assert abs(dev) < 1e-3


# ----------------------------------------------------------------------
# Class-number-one exhaustion.
# ----------------------------------------------------------------------
def test_heegner_numbers_form_the_complete_list():
    """Heegner-Stark theorem: these are the only class-number-1
    imaginary quadratic fields."""
    assert len(HEEGNER_NUMBERS) == 9
    assert 163 == max(HEEGNER_NUMBERS)


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
        "heegner_j_evaluation",
        "heegner_cubes",
        "ramanujan_163",
        "near_integer_rows",
        "summary_chain",
    ]:
        assert key in s
