#!/usr/bin/env python3
"""Tests for breakthrough Passes 1158-1162."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from analysis.w33_pass1158_kernel_residual_1952 import main as p1158, RESIDUAL, factorize
from analysis.w33_pass1159_hecke_structure_constants import main as p1159, WEDDERBURN_MULTS, SUBDEGREES, REL_COUNTS
from analysis.w33_pass1160_we6_character_bridge import main as p1160, WE6_IRREP_DIMS
from analysis.w33_pass1161_propagator_determinant_product import main as p1161
from analysis.w33_pass1162_corpus_full_sync import run_invariants

def test_residual_exact():
    assert RESIDUAL == 1952
    assert 2195 - 243 == 1952

def test_residual_prime_obstruction():
    f = factorize(RESIDUAL)
    assert 61 in f
    assert f[61] == 1
    assert RESIDUAL == 32 * 61

def test_residual_1920_plus_32():
    assert RESIDUAL - 1920 == 32
    assert RESIDUAL - 32 == 1920
    # 1920 = 2^7 * 3 * 5
    f = factorize(1920)
    assert f == {2: 7, 3: 1, 5: 1}

def test_hecke_algebra_invariants():
    assert sum(m**2 for m in WEDDERBURN_MULTS) == 26
    assert len(WEDDERBURN_MULTS) == 9
    assert sum(r*s for r,s in zip(REL_COUNTS, SUBDEGREES)) == 432

def test_we6_irrep_structure():
    assert len(WE6_IRREP_DIMS) == 25
    assert sum(d**2 for d in WE6_IRREP_DIMS) == 25920

def test_propagator_determinant():
    r = p1161()
    assert r['constant_term'] == '1'
    assert r['linear_coeff_check'] is True
    assert r['trace_D'] == -40

def test_corpus_sync_all_pass():
    checks, passed, failed = run_invariants()
    assert not failed, f'Failed invariants: {[c["name"] for c in failed]}'
    assert passed == len(checks)

if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
