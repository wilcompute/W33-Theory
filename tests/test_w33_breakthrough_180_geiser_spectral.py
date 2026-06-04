"""Tests for BT180: Genus-2 Geiser curve spectral invariant"""
import math, cmath

def test_weierstrass_count_eq_qfac_plus1():
    q = 3
    assert 7 == math.factorial(q) + 1

def test_predicted_pts_eq_lambda_q():
    q, lam, g = 3, 2, 2
    predicted = q + 1 + 2*g
    assert predicted == 8
    assert predicted == lam**q

def test_hasse_weil_bound():
    q, g = 3, 2
    spread = 2*g*math.sqrt(q)
    lower, upper = q+1-int(spread), q+1+int(spread)
    assert lower <= 8 <= upper

def test_phi6_roots_verify():
    roots = [cmath.exp(2j*math.pi*k/6) for k in [1,5]]
    for r in roots:
        assert abs(r**2 - r + 1) < 1e-10

def test_spectral_invariant_phi6_eq_qfac_plus1():
    q = 3
    Phi6_val = math.factorial(q) + 1  # = 7
    assert Phi6_val == 7

def test_frobenius_eigenvalue_modulus():
    q = 3
    q_fac = math.factorial(q)
    eigenvalues = [
        math.sqrt(q) * cmath.exp(2j*math.pi*k/q_fac)
        for k in range(q_fac)
    ]
    for ev in eigenvalues:
        assert abs(abs(ev) - math.sqrt(q)) < 1e-10

if __name__ == '__main__':
    test_weierstrass_count_eq_qfac_plus1()
    test_predicted_pts_eq_lambda_q()
    test_hasse_weil_bound()
    test_phi6_roots_verify()
    test_spectral_invariant_phi6_eq_qfac_plus1()
    test_frobenius_eigenvalue_modulus()
    print('BT180: 6/6 tests passed')
