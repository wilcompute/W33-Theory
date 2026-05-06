"""Regression tests for PART CCCLXXV H1/E8 grading basis alignment."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXXV_H1_E8_GRADING_BASIS_ALIGNMENT.py'
def load_module():
    spec=importlib.util.spec_from_file_location('h1_e8_align_ccclxxv',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_alignment_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=6
def test_h1_matches_g1_g2_not_g0():
    mod=load_module(); r=mod.build_results(); h=r['h1_basis_summary']['h1_basis_size']; assert h==81; assert h==r['e8_z3_grading_dims']['g1']; assert h==r['e8_z3_grading_dims']['g2']; assert h!=r['e8_z3_grading_dims']['g0']
def test_alignment_table():
    mod=load_module(); table=mod.alignment_table(); assert table['H1_basis']['dimension']==81; assert table['E8_g0']['dimension']==86
def test_payload_ccclxxv():
    mod=load_module(); r=mod.build_results(); assert 'not claiming an isomorphism' in r['architecture_upgrade']; assert 'dimension and basis-count alignment' in r['honesty_boundary']
