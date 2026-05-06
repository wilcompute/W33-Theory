"""Regression tests for PART CCCLXXXVII open-turn trace formula audit."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXXXVII_OPEN_TURN_TRACE_FORMULA_AUDIT.py'
def load_module():
    spec=importlib.util.spec_from_file_location('trace_formula_ccclxxxvii',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_moments():
    mod=load_module(); t=mod.formula_table(); assert t['base']['moments']==[0,0,0,12960,51840,518400]; assert t['paired']['moments']==[0,0,0,43200,51840,120960]
def test_formulas():
    assert 12960==27*480; assert 51840==108*480; assert 518400==1080*480; assert 43200==40*1080; assert 51840==48*1080; assert 120960==112*1080
def test_payload():
    mod=load_module(); r=mod.build_results(); assert 'first six moments' in r['honesty_boundary']; assert 'distinct closed-walk structure' in r['theorem']
