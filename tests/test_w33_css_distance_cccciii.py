"""Regression tests for PART CCCCIII W33 CSS code distance."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCCIII_W33_CSS_DISTANCE.py'
def load_module():
    spec=importlib.util.spec_from_file_location('w33_css_distance_cccciii',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_distance_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_css_distance_parameters():
    mod=load_module(); r=mod.build_results(); params=r['css_parameters']; assert params['n']==240; assert params['k']==81; assert params['d_X']==3; assert params['d_Z']==4; assert params['d']==3; assert params['notation']=='[[240,81,3]]'
def test_x_distance_certificate():
    mod=load_module(); r=mod.build_results(); dx=r['x_distance_certificate']; assert dx['d_X']==3; assert dx['weight3_kernel_count']==160; assert len(dx['witness_edges'])==3
def test_z_distance_certificate():
    mod=load_module(); r=mod.build_results(); dz=r['z_distance_certificate']; assert dz['d_Z']==4; assert dz['nontrivial_4_cycles']>0; assert len(dz['witness_edges'])==4
def test_payload():
    mod=load_module(); r=mod.build_results(); assert '[[240,81,3]]' in r['architecture_upgrade']; assert 'Distance 3 is exact' in r['honesty_boundary']
