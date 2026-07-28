#!/usr/bin/env python3
"""Tests for Passes 1273-1277."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from analysis.w33_pass1273_chi27_p1_multiplicity import main as p1273
from analysis.w33_pass1274_hecke_tensor_analytic import main as p1274
from analysis.w33_pass1275_seven_species_restrictions import main as p1275
from analysis.w33_pass1276_atlasrep_species20_substitution_execute import main as p1276
from analysis.w33_pass1277_theorem_ledger_v7 import main as p1277


def test_1273_decomp_sums_to_27():
    r = p1273()
    total = sum(c['dim'] for c in r['perm_char_27lines_decomposition'])
    assert total == 27
    assert r['packet_assignments']['chi_1']['packet'] == 'P0'
    assert r['packet_assignments']['chi_20']['packet'] == 'P1'


def test_1274_orbit_sizes_sum():
    r = p1274()
    assert r['orbit_sizes_sum'] == 432
    assert r['k'] == 9


def test_1275_restrictions_written():
    r = p1275()
    assert len(r['restrictions']) == 7


def test_1276_400_units_no_violations():
    r = p1276()
    assert r['total_matrix_units'] == 400
    assert r['all_spot_checks_passed'] is True


def test_1277_ledger_v7():
    counts = p1277()['ledger_counts']
    assert counts == {'EXACT': 13, 'PROVISIONAL': 6, 'OPEN': 3}


if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
