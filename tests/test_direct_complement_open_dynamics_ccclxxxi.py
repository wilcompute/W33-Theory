"""Regression tests for PART CCCLXXXI direct vs complement open dynamics."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXXXI_DIRECT_COMPLEMENT_OPEN_DYNAMICS.py'
def load_module():
    spec=importlib.util.spec_from_file_location('direct_complement_ccclxxxi',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_open_dynamics_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=8
def test_counts():
    mod=load_module(); pts,G=mod.build_graph(); C=mod.complement(G); assert len(mod.open_turns(G))==4320; assert len(mod.open_turns(C))==8640
def test_profiles():
    mod=load_module(); pts,G=mod.build_graph(); C=mod.complement(G); assert set(mod.turn_middle_profile(mod.open_turns(G)).values())=={108}; assert set(mod.turn_middle_profile(mod.open_turns(C)).values())=={216}
def test_payload_ccclxxxi():
    mod=load_module(); r=mod.build_results(); assert r['direct_G']['open_turns']==4320; assert r['complement_G']['open_turns']==8640; assert 'complement-open dynamics' in r['theorem']
