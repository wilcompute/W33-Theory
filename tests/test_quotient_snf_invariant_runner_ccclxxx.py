"""Regression tests for PART CCCLXXX quotient SNF invariant runner."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXXX_QUOTIENT_SNF_INVARIANT_RUNNER.py'
def load_module():
    spec=importlib.util.spec_from_file_location('snf_runner_ccclxxx',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_runner_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_shape_rank_free():
    mod=load_module(); r=mod.build_results(); assert r['relation_matrix_shape']==[201,160]; assert r['invariant_report']['rank_Q']==120; assert r['invariant_report']['free_rank']==81
def test_modular_agreement():
    mod=load_module(); r=mod.build_results(); assert all(v==120 for v in r['invariant_report']['modular_ranks'].values())
def test_certificate_type_recorded():
    mod=load_module(); r=mod.build_results(); assert r['invariant_report']['certificate_type'] in ('complete_snf','rank_plus_sampled_modular_fallback','snf_computed_with_nonunit_or_rank_issue')
