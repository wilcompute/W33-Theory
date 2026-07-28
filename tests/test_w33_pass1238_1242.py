#!/usr/bin/env python3
"""Tests for Passes 1238-1242."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from analysis.w33_pass1238_sign_twist_81sector_test import main as p1238
from analysis.w33_pass1239_shifted_adjacency_delta_check import main as p1239
from analysis.w33_pass1240_hecke_multiplication_tables import main as p1240
from analysis.w33_pass1241_matrix_unit_species20_seed import main as p1241
from analysis.w33_pass1242_qutrit_kernel_bridge_probe import main as p1242


def test_1238_sign_twist_answer():
    assert p1238()['answer'] is True


def test_1239_constant_shift_false():
    r = p1239()
    assert 'FALSE' in r['verdict']


def test_1240_no_fusion():
    r = p1240()
    assert 'NO fusing' in r['fusion_verdict']
    assert r['hecke_basis_size'] == 5


def test_1241_five_steps():
    assert len(p1241()['construction_steps']) == 5


def test_1242_eigenspace_total():
    r = p1242()
    assert r['total_check'] == 480


if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
