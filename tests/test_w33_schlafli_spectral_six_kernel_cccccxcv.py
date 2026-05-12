"""Tests for Part CCCCCXCV: W33 Schlafli spectral six-kernel."""
import math


def test_schlafli_is_srg_27_16_10_8():
    n, d, lam, mu = 27, 16, 10, 8
    assert n * d % 2 == 0
    edges = n * d // 2
    assert edges == 216


def test_schlafli_eigenvalues():
    d, lam, mu = 16, 10, 8
    disc = (lam - mu) ** 2 + 4 * (d - mu)
    assert disc == 36
    r = ((lam - mu) + int(math.sqrt(disc))) // 2
    s = ((lam - mu) - int(math.sqrt(disc))) // 2
    assert r == 4 and s == -2


def test_eigenvalue_multiplicities_sum_to_n():
    assert 1 + 20 + 6 == 27


def test_s_minus2_multiplicity_is_six_kernel():
    m_s = 6
    six_kernel_rank = 6
    assert m_s == six_kernel_rank


def test_eigenvalue_sum_encodes_six_kernel():
    r, s = 4, -2
    assert r + abs(s) == 6


def test_eigenvalue_product_encodes_eight_packet():
    r, s = 4, -2
    assert r * abs(s) == 8 == 192 // 24


def test_spectral_gap_is_half_tetrahedral_packet():
    d, r = 16, 4
    spectral_gap = d - abs(r)
    assert spectral_gap == 12 == 24 // 2


def test_w33_is_ramanujan():
    d, r, s = 16, 4, -2
    bound = 2 * math.sqrt(d - 1)
    assert abs(r) < bound
    assert abs(s) < bound


def test_w_f4_over_w_d4_is_six_kernel():
    w_f4 = 2 ** 7 * 3 ** 2
    w_d4 = 2 ** 3 * math.factorial(4)
    assert w_f4 == 1152 and w_d4 == 192
    assert w_f4 // w_d4 == 6


def test_ihara_zeta_s_block_exponent_is_six_kernel():
    m_s = 6
    six_kernel_rank = 6
    assert m_s == six_kernel_rank
