"""Regression tests for PART CCCCII W33 CSS topological code architecture."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCCII_W33_CSS_TOPOLOGICAL_CODE.py'
def load_module():
    spec=importlib.util.spec_from_file_location('w33_css_ccccii',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_css_parameters():
    mod=load_module(); r=mod.build_results(); params=r['css_parameters']; assert params['n_physical_edge_qubits']==240; assert params['rank_X_vertex_checks']==39; assert params['rank_Z_triangle_checks']==120; assert params['k_logical_qubits']==81
def test_commutation_and_weights():
    mod=load_module(); pts,adj=mod.build_graph(); E,T,Hx,Hz=mod.css_matrices(adj); assert mod.commute(Hx,Hz); assert mod.row_weight_set(Hx)==[12]; assert mod.row_weight_set(Hz)==[3]
def test_payload():
    mod=load_module(); r=mod.build_results(); assert r['css_parameters']['notation']=='[[240,81,d]] with d pending'; assert 'photonic topological quantum computer' in r['architecture_upgrade']
