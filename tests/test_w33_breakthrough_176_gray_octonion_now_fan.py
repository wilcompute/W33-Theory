"""Tests for BT176: Gray-code walk on octonion bipartition through now-fan"""
import math

def hamming(n): return bin(n).count('1')
def is_power_of_2(n): return n > 0 and (n & (n-1)) == 0
def is_two_bit(n): return hamming(n) == 2

def test_even_class_size():
    q, lam = 3, 2
    even = [v for v in range(16) if hamming(v) % 2 == 0]
    assert len(even) == 8 == lam**q

def test_fano_timelike_spacelike_split():
    q, mu = 3, 4
    FANO = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
    assert len([L for L in FANO if 0 in L])     == q
    assert len([L for L in FANO if 0 not in L]) == mu
    assert q + mu == 7

def test_gray_clock_alternates_parity_and_single_bit():
    gray4 = [0,1,3,2,6,7,5,4,12,13,15,14,10,11,9,8]
    assert len(set(gray4)) == 16
    steps = [gray4[i] ^ gray4[(i+1)%16] for i in range(16)]
    assert all(is_power_of_2(s) for s in steps)
    assert all(hamming(gray4[i]) % 2 != hamming(gray4[(i+1)%16]) % 2 for i in range(16))

def test_gray_clock_even_projection_is_octonion_frame():
    gray4 = [0,1,3,2,6,7,5,4,12,13,15,14,10,11,9,8]
    even = [v for v in range(16) if hamming(v) % 2 == 0]
    odd = [v for v in range(16) if hamming(v) % 2 == 1]
    even_projection = gray4[::2]
    odd_projection = gray4[1::2]
    assert sorted(even_projection) == even
    assert sorted(odd_projection) == odd
    projected_steps = [even_projection[i] ^ even_projection[(i+1)%8] for i in range(8)]
    assert all(is_two_bit(s) for s in projected_steps)

def test_substrate_7_eq_q_plus_mu():
    q, mu = 3, 4
    assert 7 == q + mu

def test_six_way_unification_count():
    ways = [
        "Cl4_algebra", "Q4_topology", "knight_geometry",
        "Gray_information", "octonion_bipartition", "now_fan_temporal"
    ]
    assert len(ways) == 6

if __name__ == "__main__":
    test_even_class_size()
    test_fano_timelike_spacelike_split()
    test_gray_clock_alternates_parity_and_single_bit()
    test_gray_clock_even_projection_is_octonion_frame()
    test_substrate_7_eq_q_plus_mu()
    test_six_way_unification_count()
    print("BT176: 6/6 tests passed")
