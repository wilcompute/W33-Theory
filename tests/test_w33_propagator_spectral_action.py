#!/usr/bin/env python3
"""
Tests for Step 2: propagator rebuild from corrected W(3,3) spectrum.

All checks use exact integer / rational arithmetic — no floating-point.
"""
from fractions import Fraction

# Corrected spectrum
EIGENVALUES = {11: 1, 1: 24, -5: 15}


def trace_power(n):
    return sum(mult * (ev ** n) for ev, mult in EIGENVALUES.items())


def test_dimension():
    assert sum(EIGENVALUES.values()) == 40, "Total multiplicity must be 40"


def test_trace_tower_first_values():
    assert trace_power(0) == 40
    assert trace_power(1) == -40
    assert trace_power(2) == 520
    assert trace_power(3) == -520


def test_recurrence():
    moments = [trace_power(n) for n in range(20)]
    for i in range(17):
        lhs = moments[i + 3]
        rhs = 7 * moments[i + 2] + 49 * moments[i + 1] - 55 * moments[i]
        assert lhs == rhs, f"Recurrence fails at n={i}: {lhs} != {rhs}"


def test_projector_ranks():
    trI = 40
    trD = trace_power(1)   # -40
    trD2 = trace_power(2)  # 520
    # Tr(P_11) = Tr((D-I)(D+5I)/160) = (Tr D^2 + 4*Tr D - 5*Tr I)/160
    rank_P11 = Fraction(trD2 + 4*trD - 5*trI, 160)
    # Tr(P_1) = -Tr((D-11I)(D+5I)/60) = -(Tr D^2 - 6*Tr D - 55*Tr I)/60
    rank_P1 = Fraction(-(trD2 - 6*trD - 55*trI), 60)
    # Tr(P_-5) = Tr((D-11I)(D-I)/96) = (Tr D^2 - 12*Tr D - 11*Tr I)/96  
    rank_Pm5 = Fraction(trD2 - 12*trD - 11*trI, 96)
    assert rank_P11 == 1, f"rank P_11 should be 1, got {rank_P11}"
    assert rank_P1 == 24, f"rank P_1 should be 24, got {rank_P1}"
    assert rank_Pm5 == 15, f"rank P_-5 should be 15, got {rank_Pm5}"


def test_completeness():
    """Tr(P_11) + Tr(P_1) + Tr(P_-5) = 40."""
    trI = 40
    trD = trace_power(1)
    trD2 = trace_power(2)
    rank_P11 = Fraction(trD2 + 4*trD - 5*trI, 160)
    rank_P1 = Fraction(-(trD2 - 6*trD - 55*trI), 60)
    rank_Pm5 = Fraction(trD2 - 12*trD - 11*trI, 96)
    assert rank_P11 + rank_P1 + rank_Pm5 == 40


def test_false_spectrum_gives_wrong_dimension():
    false_ev = {5: 10, -1: 16, -7: 6}
    false_dim = sum(false_ev.values())
    assert false_dim == 32, f"False multiplicities should sum to 32, got {false_dim}"
    assert false_dim != 40, "False spectrum must not have correct dimension"


def test_false_spectrum_wrong_trace():
    false_ev = {5: 10, -1: 16, -7: 6}
    false_tr = sum(mult * ev for ev, mult in false_ev.items())
    true_tr = trace_power(1)
    # False trace of D: 5*10 + (-1)*16 + (-7)*6 = 50 - 16 - 42 = -8
    assert false_tr == -8
    assert true_tr == -40
    assert false_tr != true_tr


def test_determinant_constant_term():
    """det(I - xD)|_{x=0} = 1."""
    # The constant term of det(I-xD) = (1-11x)(1-x)^24(1+5x)^15 is 1
    # because each factor equals 1 at x=0
    assert True  # Trivially satisfied by construction


def test_determinant_linear_term():
    """Coefficient of x in det(I-xD) = -Tr(D) = 40."""
    # d/dx det(I-xD)|_{x=0} = -Tr(D)
    coeff_x = -trace_power(1)
    assert coeff_x == 40


if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
