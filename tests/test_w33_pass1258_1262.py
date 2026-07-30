#!/usr/bin/env python3
"""Tests for Passes 1258-1262."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from analysis.w33_pass1258_27line_embedding_construction import main as p1258
from analysis.w33_pass1259_species20_atlasrep_scaffold import main as p1259
from analysis.w33_pass1260_a5_fixed_point_counts import main as p1260
from analysis.w33_pass1261_exact_hecke_constants import main as p1261
from analysis.w33_pass1262_universal_shifted_adjacency_theorem import main as p1262


def test_1258_five_steps():
    assert len(p1258()['embedding_steps']) == 5


def test_1259_matrix_unit_count():
    assert p1259()['estimated_matrix_unit_count'] == 400


def test_1260_burnside_verified():
    r = p1260()
    assert r['burnside_verified'] is True
    assert r['candidate_solution']['num_orbits'] == 9


def test_1261_integer_orbits():
    r = p1261()
    assert r['single_is_integer'] is True


def test_1262_exact_theorem():
    r = p1262()
    assert r['theorem_state'] == 'EXACT'
    assert r['delta_sample_verification'][0]['matches_original'] is True
    assert r['delta_sample_verification'][1]['matches_original'] is False


if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
