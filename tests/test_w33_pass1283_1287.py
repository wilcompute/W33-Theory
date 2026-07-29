#!/usr/bin/env python3
"""Tests for Passes 1283-1287."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from analysis.w33_pass1283_m3_primitive_idempotents import main as p1283
from analysis.w33_pass1284_m4_wedderburn_basis import main as p1284
from analysis.w33_pass1285_morita_psp43_bridge import main as p1285
from analysis.w33_pass1286_levi_incidence_absorption import main as p1286
from analysis.w33_pass1287_theorem_ledger_v9 import main as p1287


def test_1283_three_idempotents():
    r = p1283()
    assert len(r['idempotents']) == 3
    assert all(e['verified'] for e in r['idempotents'])
    assert r['sum_is_identity'] is True


def test_1284_m4_dim_16():
    r = p1284()
    assert r['m4_block']['total_dim_check'] == 16
    assert len(r['m4_units']) == 16


def test_1285_z2_decomp_sums_to_3():
    r = p1285()
    total = sum(c['dim'] for c in r['z2_decomposition'])
    assert total == 3


def test_1286_levi_80_eigenvalues():
    r = p1286()
    assert r['total_eigenvalue_count'] == 80
    assert r['levi_graph']['vertices'] == 80


def test_1287_ledger_v9():
    counts = p1287()['ledger_counts']
    assert counts == {'EXACT': 20, 'PROVISIONAL': 4, 'OPEN': 3}


if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
