"""Regression tests for PART CCCXCI E8 artifact regeneration pipeline."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCXCI_E8_ARTIFACT_REGENERATION_PIPELINE.py'
def load_module():
    spec=importlib.util.spec_from_file_location('e8_regen_pipeline_cccxci',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_pipeline_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_pipeline_shape():
    mod=load_module(); assert len(mod.STEPS)==5; assert mod.STEPS[0]['name']=='build_root_metadata'; assert mod.STEPS[1]['name']=='export_structure_constants'
def test_preflight_shape():
    mod=load_module(); pf=mod.preflight(); assert len(pf)==5; assert all('ready' in st for st in pf)
def test_z3_manifest_output_contract_matches_verifier_script():
    mod=load_module(); assert mod.STEPS[2]['produces'][0]=='artifacts/verify_e8_z3grading_from_structure_constants.json'
def test_next_action_defined():
    mod=load_module(); na=mod.next_action(mod.preflight()); assert 'blocked_at_step' in na or na.get('state')=='ALL_STEPS_PREFLIGHT_READY'
