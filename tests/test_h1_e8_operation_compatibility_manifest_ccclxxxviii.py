"""Regression tests for PART CCCLXXXVIII H1/E8 operation compatibility manifest."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXXXVIII_H1_E8_OPERATION_COMPATIBILITY_MANIFEST.py'
def load_module():
    spec=importlib.util.spec_from_file_location('h1_e8_manifest_ccclxxxviii',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_manifest_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_dims_and_rules():
    mod=load_module(); r=mod.build_results(); assert r['h1_rank']==81; assert r['e8_dims']['g1']==81; assert r['e8_dims']['g2']==81; assert len(r['grade_rules'])==6
def test_manifest_is_honest_about_artifacts():
    mod=load_module(); r=mod.build_results(); assert 'required_artifact_statuses' in r; assert 'honesty_boundary' in r
def test_tasks():
    mod=load_module(); assert len(mod.compatibility_tasks())>=7
