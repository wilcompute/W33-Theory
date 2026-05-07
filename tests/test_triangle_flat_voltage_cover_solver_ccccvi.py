"""Regression tests for PART CCCCVI triangle-flat voltage cover solver."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCCVI_TRIANGLE_FLAT_VOLTAGE_COVER_SOLVER.py'
def load_module():
    spec=importlib.util.spec_from_file_location('triangle_flat_cover_ccccvi',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_voltage_cover_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_cover_sizes_and_commutation():
    mod=load_module(); s2=mod.cover_summary(2); s3=mod.cover_summary(3); assert s2['n']==480 and s3['n']==720; assert s2['commutes'] is True; assert s3['commutes'] is True
def test_nontrivial_voltage():
    mod=load_module(); s2=mod.cover_summary(2); s3=mod.cover_summary(3); assert s2['voltage_meta']['noncoboundary'] is True; assert s3['voltage_meta']['noncoboundary'] is True; assert s2['voltage_weight']>0 and s3['voltage_weight']>0
def test_check_weights():
    mod=load_module(); s2=mod.cover_summary(2); assert s2['check_weights']=={'X':[12],'Z':[3]}
def test_payload():
    mod=load_module(); r=mod.build_results(); assert 'triangle-flat cocycle voltages' in r['architecture_upgrade']; assert 'does not yet optimize distance' in r['honesty_boundary']
