"""Regression tests for PART CCCLXVIII odd-triple 4320+160 factorization."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXVIII_ODD_TRIPLE_4320_160_FACTORIZATION.py'
def load_module():
    spec=importlib.util.spec_from_file_location('odd_factor_ccclxviii',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_factorization_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=11
def test_counts():
    mod=load_module(); pts,adj=mod.build_graph(); one,three=mod.classify_odd_triples(adj); assert len(one)==4320; assert len(three)==160; assert len(one)+len(three)==4480
def test_hashimoto_bridge_counts():
    mod=load_module(); pts,adj=mod.build_graph(); one,three=mod.classify_odd_triples(adj); assert 6*len(three)==960; assert len(one)==4320
def test_pair_coverage():
    mod=load_module(); pts,adj=mod.build_graph(); one,three=mod.classify_odd_triples(adj); oe,on,_,_=mod.edge_nonedge_pair_profiles(one,adj); te,tn,_,_=mod.edge_nonedge_pair_profiles(three,adj); assert oe==[18]; assert on==[16]; assert te==[2]; assert tn==[0]
def test_payload_ccclxviii():
    mod=load_module(); r=mod.build_results(); assert r['factorization']['one_edge_triples']==4320; assert r['factorization']['three_edge_triples']==160; assert r['pair_coverage']['combined']['gap']==4
