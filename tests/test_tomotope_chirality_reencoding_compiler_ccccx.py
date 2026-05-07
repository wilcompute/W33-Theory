"""Regression tests for PART CCCCX tomotope/chirality re-encoding compiler."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCCX_TOMOTOPE_CHIRALITY_REENCODING_COMPILER.py'
def load_module():
    spec=importlib.util.spec_from_file_location('tomotope_reencoding_ccccx',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_reencoding_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_packet_counts():
    mod=load_module(); assert mod.packet_count()==81; assert mod.physical_slots_total()==1296; assert mod.factorization_valid()
def test_reencoding_params():
    mod=load_module(); p=mod.sector_reencoding_params(3); c=mod.concatenated_target_params(3); assert p['n']==1296 and p['k']==81 and p['d_lower_bound']==3; assert c['d_lower_bound']==9
def test_constraints():
    mod=load_module(); constraints=mod.packet_constraints(); assert len(constraints)>=7; assert any('chirality' in x for x in constraints)
def test_payload():
    mod=load_module(); r=mod.build_results(); assert '1296 local packet slots' in r['architecture_upgrade']; assert 'not yet the final 16-slot packet code' in r['honesty_boundary']
