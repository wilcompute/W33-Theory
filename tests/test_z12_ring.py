"""
test_z12_ring.py

Regression tests for the Z[zeta_12] unified ring sprint.
Locks in the core algebraic facts.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from z12_unified_ring_spectrum import (
    z12_mul, z12_norm, gaussian_norm, eisenstein_norm,
    _z12_power, _z12_add, _z12_scalar_mul
)
from z12_frobenius_table import prime_factorization_class
from z12_alpha_exact_fraction import factorize

import math

def close(a, b, tol=1e-6):
    return abs(a-b) < tol

# --- Ring arithmetic ---

def test_unity_mul():
    one = (1,0,0,0)
    z = (0,1,0,0)
    assert z12_mul(one, z) == z

def test_z4_reduction():
    # z^4 = z^2 - 1  =>  z12_mul((0,0,0,1),(0,1,0,0)) should give z^4 component
    z3 = (0,0,0,1)
    z1 = (0,1,0,0)
    z4 = z12_mul(z3, z1)  # z^4
    assert z4 == (-1,0,1,0), f"z^4 = {z4}, expected (-1,0,1,0)"

def test_norm_of_unity():
    one = (1,0,0,0)
    assert z12_norm(one) == 1

def test_gaussian_norm_of_gaussian_unit():
    # The element (1,0,0,0) = 1 should have Gaussian norm 1
    gn = gaussian_norm((1,0,0,0))
    assert close(gn, 1.0)

# --- Frobenius table ---

def test_137_gaussian_sheet():
    cls = prime_factorization_class(137)
    assert 'Gaussian' in cls, f"Expected Gaussian sheet for 137, got: {cls}"

def test_7_inert():
    cls = prime_factorization_class(7)
    assert 'inert' in cls.lower(), f"Expected inert for 7, got: {cls}"

def test_13_splits_completely():
    cls = prime_factorization_class(13)
    assert 'splits completely' in cls, f"Expected splits completely for 13, got: {cls}"

def test_2_ramified():
    cls = prime_factorization_class(2)
    assert 'ramified' in cls

def test_3_ramified():
    cls = prime_factorization_class(3)
    assert 'ramified' in cls

# --- Alpha exact fraction ---

def test_alpha_fraction_value():
    val = 669969 / 4889
    PDG = 137.035999084
    assert abs(val - PDG) < 0.1, f"Fraction {val} not close to PDG {PDG}"

def test_numerator_factors():
    f = factorize(669969)
    assert len(f) > 0

def test_denominator_factors():
    f = factorize(4889)
    assert len(f) > 0

if __name__ == '__main__':
    tests = [
        test_unity_mul, test_z4_reduction, test_norm_of_unity,
        test_gaussian_norm_of_gaussian_unit,
        test_137_gaussian_sheet, test_7_inert, test_13_splits_completely,
        test_2_ramified, test_3_ramified,
        test_alpha_fraction_value, test_numerator_factors, test_denominator_factors
    ]
    passed = 0
    for t in tests:
        try:
            t()
            print(f'  PASS  {t.__name__}')
            passed += 1
        except Exception as e:
            print(f'  FAIL  {t.__name__}: {e}')
    print(f'\n{passed}/{len(tests)} tests passed.')
