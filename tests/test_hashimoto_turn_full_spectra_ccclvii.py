"""Regression tests for PART CCCLVII Hashimoto / turn full spectra."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLVII_HASHIMOTO_TURN_FULL_SPECTRA.py'
def load_module():
    spec=importlib.util.spec_from_file_location('hashimoto_full_ccclvii',MODULE_PATH); mod=importlib.util.module_from_spec(spec); assert spec.loader is not None; spec.loader.exec_module(mod); return mod
def test_all_hashimoto_full_spectra_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=7
def test_exact_spectrum_multiplicity():
    mod=load_module(); summary=mod.exact_b_summary(); assert summary['dimension']==480; assert summary['total_multiplicity']==480
def test_spectral_radius():
    mod=load_module(); assert abs(mod.exact_b_summary()['spectral_radius']-11)<1e-12
def test_ihara_extra_multiplicities():
    mod=load_module(); entries=mod.exact_b_summary()['entries']; assert sum(e['multiplicity'] for e in entries if e['root_real']==1.0 and e['root_imag']==0.0)==201; assert sum(e['multiplicity'] for e in entries if e['root_real']==-1.0 and e['root_imag']==0.0)==200
def test_result_payload_ccclvii():
    mod=load_module(); r=mod.build_results(); assert 'Ihara--Bass' in r['architecture_upgrade']; assert r['exact_hashimoto_spectrum']['dimension']==480
