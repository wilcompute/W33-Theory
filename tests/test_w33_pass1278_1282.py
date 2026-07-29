#!/usr/bin/env python3
"""Tests for Passes 1278-1282."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from analysis.w33_pass1278_six_transport_channels import main as p1278
from analysis.w33_pass1279_26_hecke_matrix_units import main as p1279
from analysis.w33_pass1280_hashimoto_species20_eigenvalue import main as p1280
from analysis.w33_pass1281_linking_algebra_wedderburn import main as p1281
from analysis.w33_pass1282_theorem_ledger_v8 import main as p1282


def test_1278_six_channels_sum():
    r = p1278()
    assert r['hom_dim'] == 6
    assert r['total_sq_singular'] == 331776
    assert r['species_decomposition'] == '1 + 15_a + 3*20 + 60_a'


def test_1279_26_units_no_violations():
    r = p1279()
    assert r['total_hecke_units'] == 26
    assert r['noncomm_units'] == 21
    assert r['central_units'] == 5
    assert r['all_spot_checks_pass'] is True


def test_1280_eigenvalue_minus_one():
    r = p1280()
    assert r['hashimoto_eigenvalue_on_each_copy'] == -1
    assert r['all_copies_same_eigenvalue'] is True
    assert r['num_copies'] == 3


def test_1281_linking_dim_28():
    r = p1281()
    assert r['linking_algebra_dim'] == 28
    assert r['wedderburn_dim_check'] == 28


def test_1282_ledger_v8():
    counts = p1282()['ledger_counts']
    assert counts == {'EXACT': 17, 'PROVISIONAL': 4, 'OPEN': 3}


if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
