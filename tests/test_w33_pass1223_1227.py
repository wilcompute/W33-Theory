#!/usr/bin/env python3
"""Tests for Passes 1223-1227."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from analysis.w33_pass1223_parallel_commit_absorption_memo import main as p1223
from analysis.w33_pass1224_qutrit_phase_commutant_bridge_note import main as p1224
from analysis.w33_pass1225_shifted_adjacency_hashimoto_absorption import main as p1225
from analysis.w33_pass1226_five_track_unification_synthesis import main as p1226
from analysis.w33_pass1227_expanded_master_theorem_ledger import main as p1227


def test_1223_absorption_count():
    r = p1223()
    assert len(r['parallel_commits_absorbed']) == 2


def test_1224_bridge_hypothesis():
    r = p1224()
    assert 'qutrit' in r['bridge_hypothesis'].lower()


def test_1225_status():
    assert p1225()['status'] == 'PASS'


def test_1226_five_tracks():
    assert len(p1226()['tracks']) == 5


def test_1227_expanded_counts():
    counts = p1227()['ledger_counts']
    assert counts == {'EXACT': 5, 'PROVISIONAL': 5, 'OPEN': 4}


if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
