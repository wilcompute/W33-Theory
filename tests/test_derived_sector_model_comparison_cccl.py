"""Regression tests for PART CCCL derived sector model comparison."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCL_DERIVED_SECTOR_MODEL_COMPARISON.py'
def load_module():
    spec=importlib.util.spec_from_file_location('derived_sector_cccl',MODULE_PATH); mod=importlib.util.module_from_spec(spec); assert spec.loader is not None; spec.loader.exec_module(mod); return mod
def test_all_derived_sector_comparison_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=8
def test_generated_maps_are_selected():
    mod=load_module(); r=mod.build_results(); assert r['comparisons']['operator_core']['best_bic']=='operator_core'; assert r['comparisons']['trace_flag']['best_bic']=='trace_flag'; assert r['comparisons']['minimal_bridge']['best_bic']=='minimal_bridge'; assert r['comparisons']['transform_class']['best_bic']=='transform_class'
def test_one_sector_and_free_channel_cases():
    mod=load_module(); r=mod.build_results(); assert r['comparisons']['one_sector']['best_bic']=='one_sector'; assert r['unstructured_comparison']['best_aic']=='free_channel'
def test_operator_core_matches_parity():
    mod=load_module(); maps=mod.derived_maps(); assert maps['operator_core']==maps['order_parity']
def test_result_payload_cccl():
    mod=load_module(); r=mod.build_results(); assert 'minimal_bridge' in r['derived_maps']; assert 'statistical model hypotheses' in r['architecture_upgrade']
