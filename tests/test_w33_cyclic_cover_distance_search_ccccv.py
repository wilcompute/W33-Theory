"""Regression tests for PART CCCCV W33 cyclic cover distance search."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCCV_W33_CYCLIC_COVER_DISTANCE_SEARCH.py'
def load_module():
    spec=importlib.util.spec_from_file_location('w33_cover_search_ccccv',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_cover_search_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_cover_sizes():
    mod=load_module(); assert mod.analyze_cover(2,3)['n']==480; assert mod.analyze_cover(3,3)['n']==720
def test_check_weights_preserved():
    mod=load_module(); a=mod.analyze_cover(2,3); assert a['check_weights']['X']==[12]; assert a['check_weights']['Z']==[3]
def test_payload():
    mod=load_module(); r=mod.build_results(); assert 'cover/lift search harness' in r['architecture_upgrade']; assert 'not an optimized' in r['honesty_boundary']
