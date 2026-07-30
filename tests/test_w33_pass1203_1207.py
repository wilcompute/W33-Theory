#!/usr/bin/env python3
"""Tests for Passes 1203-1207."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from analysis.w33_pass1203_residual_exact_factor_attack_plan import main as p1203
from analysis.w33_pass1204_sym3_v24_elimination_gate import main as p1204
from analysis.w33_pass1205_degree40_ihara_execution_plan import main as p1205
from analysis.w33_pass1206_manuscript_inline_application_checklist import main as p1206
from analysis.w33_pass1207_breakthrough_synthesis_release_trigger import main as p1207


def test_1203_status():
    assert p1203()['status'] == 'PASS'


def test_1204_target_dim():
    assert p1204()['target_dimension'] == 2600


def test_1205_degree():
    assert p1205()['target_degree'] == 40


def test_1206_priority():
    assert 'Pass 1158' in p1206()['highest_priority_edit']


def test_1207_has_four_preconditions():
    assert len(p1207()['required_preconditions']) == 4


if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
