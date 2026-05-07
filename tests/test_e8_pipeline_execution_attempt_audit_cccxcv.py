"""Regression tests for PART CCCXCV E8 pipeline execution attempt audit."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCXCV_E8_PIPELINE_EXECUTION_ATTEMPT_AUDIT.py'
def load_module():
    spec=importlib.util.spec_from_file_location('e8_execution_attempt_cccxcv',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_execution_attempt_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_commits_recorded():
    mod=load_module(); r=mod.build_results(); assert len(r['commits']['workflow_update'])==40; assert len(r['commits']['run_request'])==40
def test_status_is_request_not_success_claim():
    mod=load_module(); r=mod.build_results(); assert r['execution_status']=='REQUESTED_BUT_REMOTE_RUN_NOT_VISIBLE_THROUGH_CONNECTOR'; assert 'not a successful remote run log' in r['honesty_boundary']
def test_manual_steps_recorded():
    mod=load_module(); r=mod.build_results(); assert len(r['manual_verification_steps'])>=4
