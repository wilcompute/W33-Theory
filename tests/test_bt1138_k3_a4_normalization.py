"""BT1138 regression tests for the K3 A4 normalization lane."""

from fractions import Fraction


def test_k3_topological_normalization():
    chi = 24
    signature = -16
    b2 = 22
    p, n = 3, 19
    assert p + n == b2
    assert p - n == signature
    assert 2 + b2 == chi


def test_ricci_flat_unit_volume_product_coefficients():
    N = 440
    F2 = 1920
    F4_over_2 = 8160
    A0 = 1
    A2 = 0
    A4_norm = 24
    assert N * A0 == 440
    assert N * A2 - F2 * A0 == -1920
    assert N * A4_norm - F2 * A2 + F4_over_2 * A0 == 18720


def test_c4_normalized_integer_closure():
    q_factorial = 6
    Phi3 = 13
    E = 240
    C4_norm = 18720
    assert Fraction(C4_norm, E) == q_factorial * Phi3
    assert C4_norm == E * q_factorial * Phi3
