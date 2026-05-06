"""Regression tests for PART CCCLXVII odd-triple nullspace basis certificate."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLXVII_ODD_TRIPLE_NULLSPACE_BASIS_CERTIFICATE.py'
def load_module():
    spec=importlib.util.spec_from_file_location('odd_null_ccclxvii',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_nullspace_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=6
def test_pivot_and_free_counts():
    mod=load_module(); pts,adj=mod.build_graph(); odd=mod.odd_triples(adj); piv=mod.pivot_columns(odd); assert len(piv)==40; assert len(odd)-len(piv)==4440
def test_sample_null_vectors_verify():
    mod=load_module(); pts,adj=mod.build_graph(); odd=mod.odd_triples(adj); piv=mod.pivot_columns(odd); Pinv=mod.invert_fraction_matrix(mod.pivot_matrix(odd,piv)); samples=mod.sample_basis_vectors(odd,piv,Pinv,2); assert all(s['verified'] for s in samples)
def test_payload_ccclxvii():
    mod=load_module(); r=mod.build_results(); assert r['nullity']==4440; assert 'basis_rule' in r
