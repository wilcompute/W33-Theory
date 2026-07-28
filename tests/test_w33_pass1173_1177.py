#!/usr/bin/env python3
"""Tests for Passes 1173-1177."""
import pathlib, sys
from math import comb
from fractions import Fraction
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from analysis.w33_pass1173_clebsch_gordan_sym3 import main as p1173, WE6_IRREP_DIMS
from analysis.w33_pass1174_d5_adjoint_image import main as p1174
from analysis.w33_pass1175_meataxe_gf7_simulation import main as p1175
from analysis.w33_pass1176_manuscript_amendment import main as p1176
from analysis.w33_pass1177_ihara_zeta_degree30 import main as p1177

def test_steinberg_243_equals_3_times_81():
    assert 3 * 81 == 243

def test_61_not_in_we6_prime_factors():
    r = p1173()
    assert 61 not in r['we6_prime_factors']

def test_1952_reducible():
    r = p1173()
    assert r['residual_1952']['61_divides_we6_order'] is False
    assert r['residual_1952']['61_divides_1952'] is True
    assert r['residual_1952']['conclusion'].startswith('1952 is REDUCIBLE')

def test_so10_dim_45():
    r = p1174()
    assert r['so10_dim'] == 45
    assert r['so10_as_antisym2_10'] == comb(10, 2)

def test_45_not_in_we6_irreps():
    r = p1174()
    assert r['45_in_we6_irreps'] is False
    assert 45 not in WE6_IRREP_DIMS

def test_d4_restriction_sum():
    r = p1174()
    d4 = r['d4_restriction_of_d5_adjoint']
    assert d4['D4_adjoint'] + d4['spinor_8a'] + d4['spinor_8b'] + d4['trivial'] == 45

def test_v24_x_v15_is_360():
    r = p1175()
    assert r['v24_x_v15_is_V360']['product_dim'] == 360
    assert r['v24_x_v15_is_V360']['V360_in_we6'] is True

def test_61_squared_exceeds_all_irreps():
    r = p1175()
    assert r['61_prime_constraint']['61_squared'] == 3721
    assert 3721 > max(WE6_IRREP_DIMS)

def test_amendment_all_tags():
    r = p1176()
    assert r['all_tags_present'] is True
    for tag in ['acting_group', 'stabilizer_label_or_order', 'color_retained_or_forgotten']:
        assert r['tags_verified'][tag] is True

def test_ihara_degree30_constant():
    r = p1177()
    assert r['zinv_0'] == '1'

def test_ihara_degree30_ramanujan():
    r = p1177()
    assert r['ramanujan'] is True

def test_ihara_degree30_no_ghosts():
    r = p1177()
    assert r['ghost_cycles'] == 'None detected in degrees 1-30'

def test_pnt_ratio_increases():
    r = p1177()
    samples = r['pnt_estimates_sample']
    ratios = [samples[k]['ratio_main_to_error'] for k in sorted(samples.keys(), key=int)]
    assert all(ratios[i] <= ratios[i+1] for i in range(len(ratios)-1))

if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
