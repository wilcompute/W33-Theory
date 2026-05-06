"""Regression tests for PART CCCLXI two-graph incidence operator."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXI_TWO_GRAPH_INCIDENCE_OPERATOR.py'
def load_module():
    spec=importlib.util.spec_from_file_location('twograph_incidence_ccclxi',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_incidence_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=11
def test_triple_distribution():
    mod=load_module(); pts,adj=mod.build_graph(); assert mod.triple_distribution(adj)=={0:3240,1:4320,2:2160,3:160}; assert len(mod.odd_triples(adj))==4480
def test_gram_identity_and_adjacency_recovery():
    mod=load_module(); pts,adj=mod.build_graph(); odd=mod.odd_triples(adj); C,_=mod.incidence_gram(odd); assert mod.max_abs_diff(C,mod.expected_gram(adj))==0; assert mod.recover_adjacency(C)==mod.adjacency_matrix(adj)
def test_pair_counts():
    mod=load_module(); pts,adj=mod.build_graph(); C,_=mod.incidence_gram(mod.odd_triples(adj)); assert set(C[i][j] for i in range(40) for j in adj[i] if i<j)=={20}; assert set(C[i][j] for i in range(40) for j in range(i+1,40) if j not in adj[i])=={16}
def test_result_payload_ccclxi():
    mod=load_module(); r=mod.build_results(); assert r['gram_identity']=='M M^T = 320 I + 16 J + 4 A'; assert r['adjacency_recovery']=='A = (M M^T - 320 I - 16 J)/4'
