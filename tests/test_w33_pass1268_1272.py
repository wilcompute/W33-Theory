#!/usr/bin/env python3
"""Tests for Passes 1268-1272."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from analysis.w33_pass1268_k9_coset_table_gap_plan import main as p1268
from analysis.w33_pass1269_exact_psp43_restriction_decomposition import main as p1269
from analysis.w33_pass1270_atlasrep_species20_basis_substitution import main as p1270
from analysis.w33_pass1271_27line_embedding_close import main as p1271
from analysis.w33_pass1272_theorem_ledger_v6 import main as p1272


def test_1268_gap_plan_has_commands():
    r = p1268()
    assert len(r['gap_commands']) > 5
    assert r['expected_outputs']['carrier_size'] == 432


def test_1269_three_exact():
    r = p1269()
    assert set(r['exact_known_restrictions'].keys()) == {'sp1', 'sp20', 'sp81'}


def test_1270_rank_ok():
    r = p1270()
    assert r['rank_check_ok'] is True
    assert r['orbit_basis_size'] == 20


def test_1271_partial_close():
    assert p1271()['closing_status'] == 'PARTIAL_CLOSE'


def test_1272_ledger_v6():
    counts = p1272()['ledger_counts']
    assert counts == {'EXACT': 10, 'PROVISIONAL': 7, 'OPEN': 3}


if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
