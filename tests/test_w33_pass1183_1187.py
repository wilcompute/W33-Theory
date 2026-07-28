#!/usr/bin/env python3
"""Tests for Passes 1183-1187."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from analysis.w33_pass1183_sym3_v24_fingerprint_table import main as p1183
from analysis.w33_pass1184_d5_image_verdict_memo import main as p1184
from analysis.w33_pass1185_meataxe_handoff_bundle import main as p1185
from analysis.w33_pass1186_manuscript_patch_queue import main as p1186
from analysis.w33_pass1187_ihara_degree40_worklist import main as p1187


def test_1183_status():
    assert p1183()['status'] == 'PASS'


def test_1184_split():
    assert p1184()['working_we6_split'] == [30, 15]


def test_1185_ready():
    assert p1185()['handoff_ready'] is True


def test_1186_has_high_priority():
    q = p1186()['patches']
    assert any(p['priority'] == 'HIGH' for p in q)


def test_1187_degree():
    assert p1187()['target_degree'] == 40


if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
