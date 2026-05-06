"""Regression tests for PART CCCLVI E8/E6 grading alignment."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLVI_E8_E6_GRADING_ALIGNMENT.py'
def load_module():
    spec=importlib.util.spec_from_file_location('e8_alignment_ccclvi',MODULE_PATH); mod=importlib.util.module_from_spec(spec); assert spec.loader is not None; spec.loader.exec_module(mod); return mod
def test_all_e8_alignment_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=8
def test_dimensions():
    mod=load_module(); assert mod.E8_DIMS['g0']+mod.E8_DIMS['g1']+mod.E8_DIMS['g2']==248; assert mod.E8_DIMS['h1_w33']==mod.E8_DIMS['g1']
def test_target_equals_operator_core():
    mod=load_module(); assert mod.canonical_from_roles()==mod.maps()['operator_core']; assert mod.canonical_from_roles()==mod.maps()['grading_role']
def test_best_alignment():
    mod=load_module(); r=mod.build_results(); assert r['best_alignment'] in ['operator_core','grading_role']; assert r['sector_map_alignment_scores']['operator_core']==6
def test_result_payload_ccclvi():
    mod=load_module(); r=mod.build_results(); assert 'existing_repo_artifacts' in r; assert 'E8=g0(86)+g1(81)+g2(81)' in r['theorem']
