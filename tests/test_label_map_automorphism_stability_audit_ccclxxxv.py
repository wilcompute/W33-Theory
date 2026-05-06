"""Regression tests for PART CCCLXXXV label-map automorphism stability audit."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXXXV_LABEL_MAP_AUTOMORPHISM_STABILITY_AUDIT.py'
def load_module():
    spec=importlib.util.spec_from_file_location('auto_stability_ccclxxxv',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_transvection_is_graph_automorphism():
    mod=load_module(); pts,adj=mod.build_graph(); perm=mod.transvection_perm(pts,0); assert sorted(perm)==list(range(40)); assert all(((perm[j] in adj[perm[i]])==(j in adj[i])) for i in range(40) for j in range(40) if i!=j)
def test_signature_audit_records_noninvariance():
    mod=load_module(); a=mod.audit(); assert a['changed_count_first_20']>0; assert a['edge_vertex_prefix_changed_count']==0
def test_payload():
    mod=load_module(); r=mod.build_results(); assert 'deterministic but not full-automorphism-invariant' in r['conclusion']
