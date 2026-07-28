#!/usr/bin/env python3
"""Tests for Passes 1208-1212."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from analysis.w33_pass1208_eightyone_sector_bridge_workbench import main as p1208
from analysis.w33_pass1209_matrix_unit_refinement_plan import main as p1209
from analysis.w33_pass1210_hecke_comparison_launch_memo import main as p1210
from analysis.w33_pass1211_literal_orbit_extension_engine_plan import main as p1211
from analysis.w33_pass1212_external_s3_triality_test_plan import main as p1212


def test_1208_status():
    assert p1208()['status'] == 'PASS'


def test_1209_has_m3():
    assert any(b['matrix_algebra'] == 'M_3' for b in p1209()['starting_blocks'])


def test_1210_pair_names():
    r = p1210()
    assert 'A5' in r['pair_1'] and 'S5' in r['pair_2']


def test_1211_lengths():
    assert p1211()['target_lengths'] == [7, 8]


def test_1212_goal():
    assert 'triality torsor' in p1212()['goal']


if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
