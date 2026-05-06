"""Regression tests for PART CCCLXV odd-triple space operator."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXV_ODD_TRIPLE_SPACE_OPERATOR.py'
def load_module():
    spec=importlib.util.spec_from_file_location('odd_triple_space_ccclxv',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_odd_triple_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=9
def test_type_distribution():
    mod=load_module(); pts,adj=mod.build_graph(); odd=mod.odd_triples(adj); assert dict(mod.type_distribution(odd,adj))=={1:4320,3:160}
def test_intersection_profile():
    mod=load_module(); pts,adj=mod.build_graph(); odd=mod.odd_triples(adj); prof=mod.intersection_profile(odd); assert set(prof.keys())=={0,1,2}; assert sum(prof.values())==4480*4479//2
def test_spectrum_rank_nullity():
    mod=load_module(); r=mod.build_results(); assert r['rank']==40; assert r['nullity']==4440; assert r['nonzero_spectrum']=={'1008':1,'328':24,'304':15}
def test_result_payload_ccclxv():
    mod=load_module(); r=mod.build_results(); assert r['operator']=='K=M^T M on 4480 odd triples'; assert '4440-dimensional' in r['null_kernel']
