#!/usr/bin/env python3
"""Tests for Passes 1178-1182."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from analysis.w33_pass1178_sym3_v24_plethysm_search import main as p1178
from analysis.w33_pass1179_d5_image_split_checker import main as p1179
from analysis.w33_pass1180_meataxe_kernel_manifest import main as p1180
from analysis.w33_pass1181_manuscript_inline_patch_plan import main as p1181
from analysis.w33_pass1182_ihara_degree40_scaffold import main as p1182


def test_1178_target():
    r = p1178()
    assert r['target'] == 2600
    assert r['status'] == 'PASS'


def test_1179_best_split():
    r = p1179()
    assert r['best_candidate'] == [30, 15]


def test_1180_prime():
    r = p1180()
    assert r['prime'] == 7
    assert r['module_total_dim'] == 2195


def test_1181_target_file():
    r = p1181()
    assert r['target_file'] == 'PASS1158_1162_BREAKTHROUGH_RELEASE.md'


def test_1182_next_degree():
    r = p1182()
    assert r['next_degree'] == 40
    assert r['degree40_ratio_estimate'] > 1


if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
