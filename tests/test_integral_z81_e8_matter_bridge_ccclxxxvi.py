"""Regression tests for PART CCCLXXXVI integral Z81 E8 matter bridge."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXXXVI_INTEGRAL_Z81_E8_MATTER_BRIDGE.py'
def load_module():
    spec=importlib.util.spec_from_file_location('z81_e8_bridge_ccclxxxvi',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_rank_matches_matter_grades():
    mod=load_module(); r=mod.build_results(); assert r['h1_certificate']['rank']==81; assert r['e8_dims']['g1']==81; assert r['e8_dims']['g2']==81; assert r['e8_dims']['g0']==86
def test_payload():
    mod=load_module(); r=mod.build_results(); assert 'Z^81' in r['h1_certificate']['module'] if 'module' in r['h1_certificate'] else True; assert 'not a completed E8 representation' in r['honesty_boundary']
