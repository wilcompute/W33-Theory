"""Regression tests for PART CCCXLVI profile likelihood/model comparison compiler."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCXLVI_PROFILE_LIKELIHOOD_MODEL_COMPARISON.py'
def load_module():
    spec=importlib.util.spec_from_file_location('profile_likelihood_cccxlvi',MODULE_PATH); mod=importlib.util.module_from_spec(spec); assert spec.loader is not None; spec.loader.exec_module(mod); return mod
def test_all_profile_likelihood_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=8
def test_clean_prefers_common_model_by_bic():
    mod=load_module(); r=mod.build_results(); assert r['clean_case']['best_bic']=='M0_common_scale'
def test_systematic_prefers_nuisance_and_recovers_theta():
    mod=load_module(); r=mod.build_results(); assert r['systematic_case']['best_bic']=='M1_scale_plus_nuisance'; assert abs(r['systematic_case']['models']['M1_scale_plus_nuisance']['beta'][1]-0.02)<1e-8
def test_bad_case_selects_broken_by_aic():
    mod=load_module(); r=mod.build_results(); assert r['bad_case']['best_aic']=='M2_free_channels'; assert r['bad_case']['models']['M1_scale_plus_nuisance']['reduced_chi_square']>3
def test_result_payload_model_comparison_layer():
    mod=load_module(); r=mod.build_results(); assert r['criteria']['aic']=='chi2+2k'; assert 'M2' in r['model_definitions']; assert 'profile' in r['architecture_upgrade']
