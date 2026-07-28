#!/usr/bin/env python3
"""Tests for Passes 1168-1172."""
import pathlib, sys
from math import comb
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from analysis.w33_pass1168_sym3_decomposition import main as p1168
from analysis.w33_pass1169_sp43_432_orbit_source import main as p1169
from analysis.w33_pass1170_meataxe_kernel_plan import main as p1170, WE6_IRREP_DIMS
from analysis.w33_pass1171_needs_tag_fix import main as p1171, ERRATUM
from analysis.w33_pass1172_ihara_zeta_degree20 import main as p1172

def test_sym3_total_dim():
    r = p1168()
    assert r['sym3_total_dim'] == 11480
    assert r['sym3_total_check'] is True

def test_rank_equals_so10():
    r = p1168()
    assert r['cubic_map']['rank'] == 45
    assert r['cubic_map']['rank_equals_so10_dim'] is True

def test_we6_order_corrected():
    r = p1169()
    assert r['we6_order_corrected'] == 51840
    assert r['ratio'] == 2

def test_orbit_sizes_consistent():
    r = p1169()
    assert r['we6_s5_orbit']['orbit_size'] == 432
    assert r['sp43_a5_orbit']['orbit_size'] == 432

def test_we6_sq_sum_corrected():
    assert sum(d**2 for d in WE6_IRREP_DIMS) == 51840

def test_erratum_all_tags():
    required = ['acting_group', 'stabilizer_label_or_order', 'color_retained_or_forgotten']
    for tag in required:
        assert tag in ERRATUM['tags_now_present']

def test_erratum_filed():
    r = p1171()
    assert r['all_tags_present'] is True
    assert r['status'] == 'PASS'

def test_ihara_degree20_constant():
    r = p1172()
    assert r['zinv_coefficients'][0] == '1'

def test_ihara_ramanujan():
    r = p1172()
    assert r['ramanujan_check']['is_ramanujan'] is True

def test_ihara_triangle_crosscheck():
    r = p1172()
    assert r['triangle_cross_check'] is True
    assert r['triangle_count'] == 160

def test_ihara_4cycle_crosscheck():
    r = p1172()
    assert r['4cycle_cross_check'] is True

def test_sym3_key_pieces():
    r = p1168()
    assert r['key_sym3_pieces']['Sym3_V24'] == comb(26,3)
    assert r['key_sym3_pieces']['Sym3_V15'] == comb(17,3)

if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
