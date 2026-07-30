#!/usr/bin/env python3
"""Tests for Passes 1213-1217."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from analysis.w33_pass1213_residual_commutant_geometry_memo import main as p1213
from analysis.w33_pass1214_residual_species_prioritization_table import main as p1214
from analysis.w33_pass1215_projector_fingerprint_atlas import main as p1215
from analysis.w33_pass1216_exact_closure_scoreboard import main as p1216
from analysis.w33_pass1217_breakthrough_map import main as p1217


def test_1213_status():
    assert p1213()['status'] == 'PASS'


def test_1214_targets_present():
    r = p1214()
    assert len(r['by_rank']) == 10
    assert len(r['by_commutant_leverage']) == 10


def test_1215_has_ten_fingerprints():
    assert len(p1215()['fingerprints']) == 10


def test_1216_exact_now_nonempty():
    assert len(p1216()['exact_now']) > 0


def test_1217_status():
    assert p1217()['status'] == 'PASS'


if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
