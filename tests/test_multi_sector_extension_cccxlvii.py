"""Regression tests for PART CCCXLVII multi-sector extension compiler."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCXLVII_MULTI_SECTOR_EXTENSION.py'
def load_module():
    spec=importlib.util.spec_from_file_location('multi_sector_cccxlvii',MODULE_PATH); mod=importlib.util.module_from_spec(spec); assert spec.loader is not None; spec.loader.exec_module(mod); return mod
def test_all_multi_sector_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=7
def test_one_sector_case_selects_one_sector():
    mod=load_module(); r=mod.build_results(); assert r['one_sector_case']['best_bic']=='one_sector'
def test_two_sector_case_selects_structured_split():
    mod=load_module(); r=mod.build_results(); assert r['two_sector_case']['best_bic']=='two_sector_geometry_response'; assert r['two_sector_case']['models']['one_sector']['reduced_chi_square']>3
def test_two_sector_scales_recovered():
    mod=load_module(); r=mod.build_results(); X0=r['sample_scales']['X0']; X1=r['sample_scales']['X1']; scales=r['two_sector_case']['models']['two_sector_geometry_response']['sector_scales']; assert abs(scales[0]-X0)<1e-8; assert abs(scales[1]-X1)<1e-8
def test_result_payload_multi_sector_layer():
    mod=load_module(); r=mod.build_results(); assert r['model_formulas']['multi_sector']=='X_i=X_{a(i)}+noise_i'; assert 'multiple spectral sectors' in r['architecture_upgrade']
