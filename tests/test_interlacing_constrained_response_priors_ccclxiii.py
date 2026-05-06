"""Regression tests for PART CCCLXIII interlacing-constrained response priors."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXIII_INTERLACING_CONSTRAINED_RESPONSE_PRIORS.py'
def load_module():
    spec=importlib.util.spec_from_file_location('response_priors_ccclxiii',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_prior_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=7
def test_prior_penalties():
    mod=load_module(); p=mod.structural_prior_penalties(); assert p['operator_core']==0; assert p['free_channel']==max(p.values())
def test_operator_core_prior_wins_near_tie():
    mod=load_module(); cmp=mod.compare_with_priors(mod.packet_close_call(),mod.cov()); assert cmp['best_posterior']=='operator_core'
def test_refinement_can_win_when_strong():
    mod=load_module(); cmp=mod.compare_with_priors(mod.packet_minimal_bridge(),mod.cov()); assert cmp['best_posterior']=='minimal_bridge'; assert cmp['best_bic']=='minimal_bridge'
def test_result_payload_ccclxiii():
    mod=load_module(); r=mod.build_results(); assert 'structural_prior_penalties' in r; assert 'active structural priors' in r['architecture_upgrade']
