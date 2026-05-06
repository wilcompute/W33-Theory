"""Regression tests for PART CCCLXXIX H1 / Triple-Albert interface."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXXIX_H1_TRIPLE_ALBERT_INTERFACE.py'
def load_module():
    spec=importlib.util.spec_from_file_location('h1_triple_albert_ccclxxix',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_interface_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=9
def test_slot_counts():
    mod=load_module(); r=mod.build_results(); assert r['sector_counts']=={'diagonal_fiber':9,'octonion_offdiagonal':72}; assert r['generation_counts']=={1:27,2:27,3:27}
def test_formula():
    mod=load_module(); assert mod.GENERATION_COUNT*mod.ALBERT_DIM==81; assert mod.TRIPLE_DIAGONAL+mod.TRIPLE_OFFDIAGONAL==81; assert mod.TRIPLE_OFFDIAGONAL==72
def test_payload_ccclxxix():
    mod=load_module(); r=mod.build_results(); assert r['source_artifact']=='PART_CLXXV_TRIPLE_ALBERT_E8_GRADING.py'; assert 'Triple-Albert' in r['architecture_upgrade']
