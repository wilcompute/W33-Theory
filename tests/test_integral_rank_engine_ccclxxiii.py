"""Regression tests for PART CCCLXXIII integral rank engine."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXXIII_SNF_TORSION_CERTIFICATE_ENGINE.py'
def load_module():
    spec=importlib.util.spec_from_file_location('rank_engine_ccclxxiii',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_ranks():
    mod=load_module(); r=mod.build_results(); assert r['rational_ranks']['rank_d1']==39; assert r['rational_ranks']['rank_d2']==120; assert r['rational_ranks']['beta1']==81
def test_prime_rank_agreement():
    mod=load_module(); r=mod.build_results(); assert all(v['rank_d1']==39 and v['rank_d2']==120 for v in r['modular_rank_checks'].values())
def test_optional_backend_status_recorded():
    mod=load_module(); r=mod.build_results(); assert r['optional_snf']['status'] in ('computed','not_computed','import_failed')
