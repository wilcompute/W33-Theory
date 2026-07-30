#!/usr/bin/env python3
"""Tests for Passes 1253-1257."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from analysis.w33_pass1253_apply_p1_projector_27line_frame import main as p1253
from analysis.w33_pass1254_scale_species20_matrix_units import main as p1254
from analysis.w33_pass1255_a5_orbit_enumeration_stub_432 import main as p1255
from analysis.w33_pass1256_shifted_adjacency_theorem_upgrade_pack import main as p1256
from analysis.w33_pass1257_theorem_ledger_v4 import main as p1257


def test_1253_rank_dichotomy():
    assert p1253()['exact_rank_dichotomy'] == [0, 27]


def test_1254_scaled_checks():
    r = p1254()
    assert r['dimension'] == 20
    assert r['all_sampled_checks_passed'] is True


def test_1255_carrier_formula():
    r = p1255()
    assert r['carrier_size'] == 432
    assert r['group_order'] == 60


def test_1256_exact_for_tested_deltas():
    assert p1256()['theorem_state'] == 'EXACT_FOR_TESTED_DELTAS'


def test_1257_counts():
    counts = p1257()['ledger_counts']
    assert counts == {'EXACT': 8, 'PROVISIONAL': 7, 'OPEN': 4}


if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
