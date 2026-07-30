#!/usr/bin/env python3
"""Tests for Passes 1248-1252."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from analysis.w33_pass1248_intertwiner_solve import main as p1248
from analysis.w33_pass1249_p1_projector_polynomial import main as p1249
from analysis.w33_pass1250_species20_gap_seed_execution import main as p1250
from analysis.w33_pass1251_pair_orbit_hecke_constants import main as p1251
from analysis.w33_pass1252_shifted_adjacency_packet_decomposition import main as p1252


def test_1248_open1_resolved():
    r = p1248()
    assert 'RESOLVED' in r['theorem_upgrade']


def test_1249_projector_verified():
    r = p1249()
    assert r['verification']['correct'] is True


def test_1250_no_violations():
    r = p1250()
    assert r['recipe_verified'] is True
    assert r['matrix_unit_relation_violations'] == 0


def test_1251_carrier_size():
    assert p1251()['carrier_size'] == 432


def test_1252_independent_lane():
    r = p1252()
    assert r['independent_lane_confirmed'] is True


if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
