"""Regression tests for PART CCCLXXI explicit 81-cycle basis."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXXI_EXPLICIT_81_CYCLE_BASIS.py'
def load_module():
    spec=importlib.util.spec_from_file_location('cycle_basis_ccclxxi',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_cycle_basis_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=7
def test_counts_and_rank():
    mod=load_module(); pts,adj=mod.build_graph(); data=mod.quotient_h1_basis(adj); assert len(data['cycles'])==201; assert data['rank_tri']==120; assert len(data['h1_reps'])==81
def test_beta_identity():
    mod=load_module(); pts,adj=mod.build_graph(); data=mod.quotient_h1_basis(adj); assert len(data['cycles'])-data['rank_tri']==81
def test_payload_ccclxxi():
    mod=load_module(); r=mod.build_results(); assert r['counts']['h1_basis_size']==81; assert 'fundamental graph cycles' in r['theorem']
