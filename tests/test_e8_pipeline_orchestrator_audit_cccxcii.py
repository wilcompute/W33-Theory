"""Regression tests for PART CCCXCII E8 pipeline orchestrator audit."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCXCII_E8_PIPELINE_ORCHESTRATOR_AUDIT.py'
def load_module():
    spec=importlib.util.spec_from_file_location('e8_pipeline_audit_cccxcii',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_orchestrator_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_runner_imports():
    mod=load_module(); runner=mod.load_runner(); assert len(runner.STEPS)==5; assert runner.STEPS[0].name=='build_root_metadata'
def test_preflight_shape():
    mod=load_module(); runner=mod.load_runner(); pf=runner.preflight(); assert 'first_blocked' in pf; assert 'ready_to_run_all' in pf; assert len(pf['steps'])==5
def test_commands_recorded():
    mod=load_module(); r=mod.build_results(); assert r['dry_run_command'].endswith('--dry-run'); assert r['run_command'].startswith('python tools/')
