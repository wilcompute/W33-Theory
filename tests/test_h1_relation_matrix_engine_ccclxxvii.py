"""Regression tests for PART CCCLXXVII H1 relation matrix engine."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXXVII_QUOTIENT_SNF_H1_ENGINE.py'
def load_module():
    spec=importlib.util.spec_from_file_location('h1_relation_ccclxxvii',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_shape_and_rank():
    mod=load_module(); r=mod.build_results(); assert r['R_shape']==[201,160]; assert r['rank_Q_R']==120; assert r['free_rank']==81
def test_prime_ranks():
    mod=load_module(); r=mod.build_results(); assert all(v==120 for v in r['modular_ranks'].values())
def test_backend_status():
    mod=load_module(); r=mod.build_results(); assert r['optional_snf']['status'] in ('computed','not_computed')
