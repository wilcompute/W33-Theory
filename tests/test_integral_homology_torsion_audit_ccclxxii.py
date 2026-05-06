"""Regression tests for PART CCCLXXII integral homology torsion audit."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXXII_INTEGRAL_HOMOLOGY_TORSION_AUDIT.py'
def load_module():
    spec=importlib.util.spec_from_file_location('integral_homology_ccclxxii',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_integral_homology_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=6
def test_rational_ranks_and_beta():
    mod=load_module(); r=mod.build_results(); ranks=r['rational_ranks']; assert ranks['rank_d1']==39; assert ranks['rank_d2']==120; assert ranks['beta1']==81
def test_boundary_composition():
    mod=load_module(); pts,adj=mod.build_graph(); E=mod.edges(adj); edge_index={e:i for i,e in enumerate(E)}; Tri=mod.triangles(adj); assert mod.compose_zero(mod.d1_matrix(E),mod.d2_matrix(Tri,edge_index))
def test_modular_rank_checks():
    mod=load_module(); r=mod.build_results(); assert all(v['rank_d1']==39 and v['rank_d2']==120 for v in r['modular_rank_checks'].values())
def test_payload_ccclxxii():
    mod=load_module(); r=mod.build_results(); assert 'Smith normal form' in r['honesty_boundary']; assert r['chain_counts']['edges']==240
