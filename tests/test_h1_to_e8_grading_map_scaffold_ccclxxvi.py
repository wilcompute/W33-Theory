"""Regression tests for PART CCCLXXVI H1 to E8 grading map scaffold."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXXVI_H1_TO_E8_GRADING_MAP_SCAFFOLD.py'
def load_module():
    spec=importlib.util.spec_from_file_location('h1_e8_scaffold_ccclxxvi',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_scaffold_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=8
def test_slot_map_size():
    mod=load_module(); r=mod.build_results(); assert r['h1_basis_size']==81; assert len(r['slot_map_samples'])==10
def test_requirements_prevent_overclaim():
    mod=load_module(); req=mod.requirements_for_verified_representation(); assert any('bracket' in x for x in req); assert any('covariance' in x for x in req)
def test_payload_ccclxxvi():
    mod=load_module(); r=mod.build_results(); assert 'scaffold' in r['honesty_boundary']; assert 'g1_slot' in r['slot_map_rule']
