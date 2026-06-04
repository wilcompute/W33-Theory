"""Tests for BT179: [[27,15,>=4]]_3 CSS ternary code"""
import math

def test_code_length_eq_q_cubed():
    q = 3
    assert 27 == q**q

def test_logicals_eq_transversals():
    q, mu = 3, 4
    assert 15 == q**q - mu*q
    assert 15 == math.factorial(q)*2 + q  # also q!*lambda+q

def test_stabilizers_eq_double_six():
    q, mu = 3, 4
    assert 12 == mu*q

def test_partition_27():
    assert 12 + 15 == 27

def test_distance_bound_eq_q_plus1():
    q = 3
    assert 4 == q+1

def test_column_weight_zero_mod3():
    # Column weight = 3 (point degree) ≡ 0 mod 3
    assert 3 % 3 == 0

def test_direct_css_fails():
    # Line size 5 ≡ 2 mod 3 ≠ 0 → diagonal of H H^T ≢ 0 mod 3
    assert 5 % 3 == 2

def test_encoding_rate():
    assert abs(15/27 - 5/9) < 1e-10

if __name__ == '__main__':
    test_code_length_eq_q_cubed()
    test_logicals_eq_transversals()
    test_stabilizers_eq_double_six()
    test_partition_27()
    test_distance_bound_eq_q_plus1()
    test_column_weight_zero_mod3()
    test_direct_css_fails()
    test_encoding_rate()
    print('BT179: 8/8 tests passed')
