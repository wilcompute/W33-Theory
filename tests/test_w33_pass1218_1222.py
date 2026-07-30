#!/usr/bin/env python3
"""Tests for Passes 1218-1222."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from analysis.w33_pass1218_commutant_hashimoto_diagonal import main as p1218
from analysis.w33_pass1219_lcu_cost_ledger import main as p1219
from analysis.w33_pass1220_spectral_unification_memo import main as p1220
from analysis.w33_pass1221_tri_track_coherence_certificate import main as p1221
from analysis.w33_pass1222_master_theorem_ledger_stub import main as p1222


def test_1218_status():
    assert p1218()['status'] == 'PASS'


def test_1219_ready_moves():
    assert len(p1219()['best_cost_to_payoff_moves']) >= 4


def test_1220_status():
    assert p1220()['status'] == 'PASS'


def test_1221_status():
    assert p1221()['status'] == 'PASS'


def test_1222_counts():
    counts = p1222()['ledger_counts']
    assert counts == {'EXACT': 5, 'PROVISIONAL': 3, 'OPEN': 2}


if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
