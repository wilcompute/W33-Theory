#!/usr/bin/env python3
"""Tests for Passes 1263-1267."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from analysis.w33_pass1263_k9_coset_verification import main as p1263
from analysis.w33_pass1264_psp43_restriction_table import main as p1264
from analysis.w33_pass1265_species20_gap_execution import main as p1265
from analysis.w33_pass1266_theorem_ledger_v5 import main as p1266
from analysis.w33_pass1267_species_to_packet_dictionary import main as p1267


def test_1263_all_tests_pass():
    r = p1263()
    assert r['all_consistency_tests_pass'] is True
    assert r['k_single_orbits'] == '9'


def test_1264_ten_species():
    r = p1264()
    assert len(r['w_e6_species']) == 10
    assert len(r['hashimoto_packets']) == 5


def test_1265_no_violations():
    r = p1265()
    assert r['all_checks_passed'] is True
    assert r['total_exact_checks'] == 20**4


def test_1266_ledger_v5():
    counts = p1266()['ledger_counts']
    assert counts == {'EXACT': 9, 'PROVISIONAL': 7, 'OPEN': 3}


def test_1267_exact_assignments():
    r = p1267()
    assert 'sp1' in r['exact_assignments']
    assert 'sp81' in r['exact_assignments']
    assert r['total_species'] == 10


if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
