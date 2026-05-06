"""Regression tests for PART CCCLXXXIII complete SNF H1 certificate."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXXXIII_COMPLETE_SNF_H1_CERTIFICATE.py'
def load_module():
    spec=importlib.util.spec_from_file_location('complete_snf_ccclxxxiii',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_snf_certificate_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_shape_rank_free():
    mod=load_module(); r=mod.build_results(); assert r['relation_matrix_shape']==[201,160]; assert r['rank_Q']==120; assert r['free_rank']==81
def test_smith_status():
    mod=load_module(); r=mod.build_results(); assert r['smith_report']['status'] in ('computed','unavailable')
def test_complete_certificate_if_computed():
    mod=load_module(); r=mod.build_results();
    if r['smith_report']['status']=='computed':
        assert r['complete_certificate'] is True
        assert r['smith_report']['nonzero_count']==120
        assert r['smith_report']['nonunit_factors']==[]
