"""Regression tests for PART CCCCI signed switching and triangle-face quotient."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCCI_SIGNED_SWITCHING_FACE_QUOTIENT.py'
def load_module():
    spec=importlib.util.spec_from_file_location('signed_switching_cccci',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_switching_exponent_correction():
    mod=load_module(); assert mod.graph_switching_orbit_exp()==39; assert mod.graph_switching_class_exp()==201; assert mod.cycle_space_dim()==201
def test_triangle_flat_exponent():
    mod=load_module(); assert mod.triangle_flat_cocycle_dim()==120; assert mod.triangle_flat_switching_class_exp()==81; assert mod.triangle_flat_switching_class_exp()==mod.H1_RANK
def test_payload():
    mod=load_module(); r=mod.build_results(); assert r['correction']['correct_switching_class_exponent']==201; assert r['sector_counts']['triangle_flat_switching_classes']=='2^81'
