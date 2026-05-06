"""Regression tests for PART CCCLV Hashimoto turn operator spectra."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLV_HASHIMOTO_TURN_OPERATOR_SPECTRA.py'
def load_module():
    spec=importlib.util.spec_from_file_location('hashimoto_turn_ccclv',MODULE_PATH); mod=importlib.util.module_from_spec(spec); assert spec.loader is not None; spec.loader.exec_module(mod); return mod
def test_all_hashimoto_turn_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=11
def test_row_sums_and_counts():
    mod=load_module(); pts,adj=mod.build_graph(); de,B,T,O=mod.build_turn_matrices(adj); assert len(de)==480; assert set(mod.row_sums(B))=={11}; assert set(mod.row_sums(T))=={2}; assert set(mod.row_sums(O))=={9}
def test_decomposition_disjoint():
    mod=load_module(); pts,adj=mod.build_graph(); de,B,T,O=mod.build_turn_matrices(adj); assert all(B[i]==T[i].union(O[i]) and T[i].isdisjoint(O[i]) for i in range(len(B)))
def test_commutator_nonzero():
    mod=load_module(); pts,adj=mod.build_graph(); de,B,T,O=mod.build_turn_matrices(adj); assert mod.commutator_frobenius_sq(T,O)>0
def test_result_payload_ccclv():
    mod=load_module(); r=mod.build_results(); assert r['carrier']['directed_edges']==480; assert r['carrier']['B_row_sum']==[11]; assert r['carrier']['T_row_sum']==[2]; assert r['carrier']['O_row_sum']==[9]
