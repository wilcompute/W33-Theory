"""Regression tests for PART CCCCVII cyclic cover low-weight logical audit."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCCVII_CYCLIC_COVER_LOW_WEIGHT_LOGICALS.py'
def load_module():
    spec=importlib.util.spec_from_file_location('cover_low_weight_ccccvii',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_cover_low_weight_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_l2_l3_distance_conclusion():
    mod=load_module(); a2=mod.audit_cover(2); a3=mod.audit_cover(3); assert a2['distance_conclusion']=='d=3 because d_X=3'; assert a3['distance_conclusion']=='d=3 because d_X=3'
def test_weight3_x_witnesses():
    mod=load_module(); assert mod.audit_cover(2)['x_weight3_logical']['found'] is True; assert mod.audit_cover(3)['x_weight3_logical']['found'] is True
def test_no_weight_1_2_logicals():
    mod=load_module(); a2=mod.audit_cover(2); assert a2['no_X_logicals_weight_1_2'] is True; assert a2['no_Z_logicals_weight_1_2'] is True
def test_payload():
    mod=load_module(); r=mod.build_results(); assert 'distance remains d=3' in r['theorem']; assert 'does not prove all possible cyclic voltage covers' in r['honesty_boundary']
