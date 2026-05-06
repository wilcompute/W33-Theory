"""Regression tests for PART CCCLXXIV complement-duality open turns."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXXIV_COMPLEMENT_DUALITY_OPEN_TURNS.py'
def load_module():
    spec=importlib.util.spec_from_file_location('complement_turns_ccclxxiv',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_complement_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=6
def test_distribution_reversal():
    mod=load_module(); pts,adj=mod.build_graph(); comp=mod.complement(adj); assert {k:len(v) for k,v in mod.triples_by_edge_count(comp).items()}=={0:160,1:2160,2:4320,3:3240}
def test_mapped_turns():
    mod=load_module(); pts,adj=mod.build_graph(); comp=mod.complement(adj); assert mod.mapped_complement_open_turns_from_one_edge_G(adj)==mod.all_open_turns(comp)
def test_payload_ccclxxiv():
    mod=load_module(); r=mod.build_results(); assert r['complement_open_turns']==8640; assert 'complement-dual' in r['architecture_upgrade']
