"""Regression tests for PART CCCLXX open-turn/two-edge triple isomorphism."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXX_OPEN_TURN_TWO_EDGE_TRIPLE_ISOMORPHISM.py'
def load_module():
    spec=importlib.util.spec_from_file_location('open_turn_ccclxx',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_open_turn_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=7
def test_bijection():
    mod=load_module(); pts,adj=mod.build_graph(); assert mod.mapped_open_turns(adj)==mod.all_open_turns(adj)
def test_counts():
    mod=load_module(); pts,adj=mod.build_graph(); by=mod.triples_by_edge_count(adj); assert len(by[2])==2160; assert len(mod.all_open_turns(adj))==4320; assert 2*len(by[2])==4320
def test_complement_dual():
    mod=load_module(); pts,adj=mod.build_graph(); by=mod.triples_by_edge_count(adj); assert all(mod.complement_edge_count(t,adj)==2 for t in by[1])
def test_payload_ccclxx():
    mod=load_module(); r=mod.build_results(); assert r['canonical_isomorphism']=='open Hashimoto turns <-> oriented two-edge triples'; assert 'complement-dual' in r['correction']
