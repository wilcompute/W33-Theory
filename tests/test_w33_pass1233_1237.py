#!/usr/bin/env python3
"""Tests for Passes 1233-1237."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from analysis.w33_pass1233_ihara_degree40_theorem_upgrade import main as p1233
from analysis.w33_pass1234_81sector_obstruction_class import main as p1234
from analysis.w33_pass1235_hecke_coset_count_execution import main as p1235
from analysis.w33_pass1236_qutrit_we6_decomposition_probe import main as p1236
from analysis.w33_pass1237_theorem_ledger_v3 import main as p1237


def test_1233_checks_present():
    r = p1233()
    assert 'checks' in r
    assert r['checks']['dominant_ratio_n40_gt_1']


def test_1234_obstruction_candidates():
    assert len(p1234()['obstruction_candidates']) == 3


def test_1235_coset_size():
    assert p1235()['coset_space_size'] == 432


def test_1236_not_in_residual():
    assert p1236()['appears_in_residual_1952'] == False


def test_1237_ledger_totals():
    r = p1237()
    counts = r['ledger_counts']
    assert counts['OPEN'] == 4
    assert counts['PROVISIONAL'] >= 7


if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
