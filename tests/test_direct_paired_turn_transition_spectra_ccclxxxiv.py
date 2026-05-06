"""Regression tests for PART CCCLXXXIV direct / paired turn-transition spectra."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXXXIV_DIRECT_PAIRED_TURN_TRANSITION_SPECTRA.py'
def load_module():
    spec=importlib.util.spec_from_file_location('turn_spectra_ccclxxxiv',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_turn_spectra_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=11
def test_counts_and_row_sums():
    mod=load_module(); r=mod.build_results(); assert r['base_operator']['directed_edge_states']==480; assert r['paired_operator']['directed_edge_states']==1080; assert r['base_operator']['row_sum_set']==[9]; assert r['paired_operator']['row_sum_set']==[8]
def test_trace_moments():
    mod=load_module(); r=mod.build_results(); assert r['base_operator']['trace_moments']['4']==12960; assert r['paired_operator']['trace_moments']['4']==43200
def test_rank_contrast():
    mod=load_module(); r=mod.build_results(); assert r['base_operator']['rank_mod_1000003']==160; assert r['paired_operator']['rank_mod_1000003']==1080
def test_payload_ccclxxxiv():
    mod=load_module(); r=mod.build_results(); assert 'moment_contrast' in r['comparison']; assert 'not merely a doubled copy' in r['theorem']
