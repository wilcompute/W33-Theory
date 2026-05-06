"""Regression tests for PART CCCLXIX incidence chain complex."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXIX_INCIDENCE_CHAIN_COMPLEX.py'
def load_module():
    spec=importlib.util.spec_from_file_location('chain_complex_ccclxix',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_chain_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=11
def test_beta1():
    mod=load_module(); r=mod.build_results(); ranks=r['gf2_ranks']; assert ranks['d1_edges_to_vertices']==39; assert ranks['d2_triangles_to_edges']==120; assert ranks['beta1_triangle_complex']==81
def test_boundary_behavior():
    mod=load_module(); pts,adj=mod.build_graph(); one,three=mod.classify_odd(adj); assert set(mod.boundary_of_edge_support(three,adj))=={()}; assert set(len(x) for x in mod.boundary_of_edge_support(one,adj))=={2}
def test_counts():
    mod=load_module(); r=mod.build_results(); c=r['chain_counts']; assert c['vertices']==40; assert c['edges']==240; assert c['triangles']==160; assert c['odd_triples']==4480
def test_payload_ccclxix():
    mod=load_module(); r=mod.build_results(); assert 'closed/open split' in r['architecture_upgrade']; assert r['boundary_behavior']['three_edge_triangle_support']=='cycle boundary zero over GF2'
