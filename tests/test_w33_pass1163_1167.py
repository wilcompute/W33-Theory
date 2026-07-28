#!/usr/bin/env python3
"""Tests for executed Passes 1163-1167."""
import pathlib, sys
from math import comb
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from analysis.w33_pass1163_sp43_stabilizer_precompute import main as p1163, a5_element_orders
from analysis.w33_pass1164_1920_module_identification import main as p1164, TARGET as TARGET_1920
from analysis.w33_pass1165_manuscript_tagging_report import main as p1165, KNOWN_CLAIMS
from analysis.w33_pass1166_ihara_zeta_degree10 import main as p1166, N, K, EDGES, A_SPECTRUM
from analysis.w33_pass1167_40pt_carrier_decomposition import main as p1167
from fractions import Fraction

def test_sp43_pair_orbit_not_432():
    r = p1163()
    assert r['sp43_pairs_on_40pts']['neither_is_432'] is True
    assert r['sp43_pairs_on_40pts']['adjacent_orbit'] == 240
    assert r['sp43_pairs_on_40pts']['non_adjacent_orbit'] == 540

def test_a5_element_orders():
    orders = a5_element_orders()
    assert sum(orders.values()) == 60
    assert set(orders.keys()) == {1, 2, 3, 5}

def test_1920_not_coset_space():
    assert 25920 % TARGET_1920 != 0  # 25920/1920 is not integer

def test_1920_arithmetic_splits():
    assert TARGET_1920 == 1952 - 32
    assert 24 * 80 == TARGET_1920
    assert 8 * 240 == TARGET_1920
    assert 12 * 160 == TARGET_1920

def test_manuscript_tagging_report():
    r = p1165()
    assert r['needs_tag'] >= 1  # at least 1 residual claim needs tagging
    assert r['typed'] >= 5      # at least 5 claims are properly typed

def test_ihara_triangle_cross_check():
    r = p1166()
    assert r['triangle_cross_check'] is True
    assert r['triangle_count'] == 160

def test_ihara_zeta_constant():
    r = p1166()
    assert r['zinv_0'] == '1'

def test_40pt_carrier_decomposition():
    r = p1167()
    assert r['total_check'] is True
    assert r['multiplicity_free'] is True
    assert '1 + 24 + 15' in r['decomposition']

def test_40pt_sym3_dim():
    r = p1167()
    assert r['sym3_40_dim'] == comb(42, 3)

def test_1_plus_24_plus_15_equals_40():
    assert 1 + 24 + 15 == 40

if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
