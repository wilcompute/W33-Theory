#!/usr/bin/env python3
"""Tests for Passes 1228-1232."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from analysis.w33_pass1228_qutrit_27line_orthogonality_verification_plan import main as p1228
from analysis.w33_pass1229_shifted_adjacency_eigenvalue_check_plan import main as p1229
from analysis.w33_pass1230_eightyone_sector_intertwiner_construction_recipe import main as p1230
from analysis.w33_pass1231_hecke_double_coset_table_template import main as p1231
from analysis.w33_pass1232_degree40_ihara_exact_execution import main as p1232


def test_1228_target_species():
    assert '6' in p1228()['target_species']


def test_1229_has_hashimoto_spectrum():
    assert len(p1229()['exact_hashimoto_spectrum']) == 5


def test_1230_five_steps():
    assert len(p1230()['recipe']) == 5


def test_1231_coset_sizes():
    r = p1231()
    assert r['known_coset_size_1'] == 432
    assert r['known_coset_size_2'] == 432


def test_1232_trace_tower_length():
    r = p1232()
    assert len(r['trace_tower']) == 40
    assert len(r['spectral_prime_cycle_counts']) == 40


if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
