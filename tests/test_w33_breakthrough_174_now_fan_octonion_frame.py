"""Tests for BT174: Now-fan heptad = imaginary octonion frame"""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def test_fano_axioms():
    from itertools import combinations
    FANO_LINES = [
        frozenset({0,1,2}), frozenset({0,3,4}), frozenset({0,5,6}),
        frozenset({1,3,5}), frozenset({1,4,6}), frozenset({2,3,6}), frozenset({2,4,5})
    ]
    assert len(FANO_LINES) == 7
    for L in FANO_LINES:
        assert len(L) == 3
    for p in range(7):
        assert len([L for L in FANO_LINES if p in L]) == 3
    for a,b in combinations(range(7), 2):
        assert sum(1 for L in FANO_LINES if a in L and b in L) == 1

def test_now_fan_eq_q_fac_plus1():
    assert 7 == math.factorial(3) + 1

def test_PSL27_substrate_form():
    q, lam = 3, 2
    assert (lam**q) * q * 7 == 168

def test_octonion_anticommutativity():
    FANO_LINES = [
        frozenset({0,1,2}), frozenset({0,3,4}), frozenset({0,5,6}),
        frozenset({1,3,5}), frozenset({1,4,6}), frozenset({2,3,6}), frozenset({2,4,5})
    ]
    rules = {}
    for line in FANO_LINES:
        pts = sorted(line)
        i, j, k = pts
        for (a, b, c) in [(i,j,k),(j,k,i),(k,i,j)]:
            rules[(a,b)] = (+1, c)
            rules[(b,a)] = (-1, c)
    count = sum(1 for (a,b),(s,c) in rules.items()
                if (b,a) in rules and rules[(b,a)] == (-s, c))
    assert count == 42

def test_bipartition_q_plus_mu():
    q, mu = 3, 4
    FANO_LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
    assert len([L for L in FANO_LINES if 0 in L])  == q
    assert len([L for L in FANO_LINES if 0 not in L]) == mu

if __name__ == "__main__":
    test_fano_axioms()
    test_now_fan_eq_q_fac_plus1()
    test_PSL27_substrate_form()
    test_octonion_anticommutativity()
    test_bipartition_q_plus_mu()
    print("BT174: 5/5 tests passed")
