"""Regression tests for PART CCCLII computed W33 graph sector evidence."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLII_COMPUTED_W33_GRAPH_SECTOR_EVIDENCE.py'
def load_module():
    spec=importlib.util.spec_from_file_location('computed_w33_ccclii',MODULE_PATH); mod=importlib.util.module_from_spec(spec); assert spec.loader is not None; spec.loader.exec_module(mod); return mod
def test_all_computed_w33_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=11
def test_w33_counts():
    mod=load_module(); pts,adj=mod.build_graph(); assert len(pts)==40; assert len(mod.edges(adj))==240; assert len(mod.triangles(adj))==160
def test_srg_params():
    mod=load_module(); pts,adj=mod.build_graph(); p=mod.srg_params(adj); assert p['degree_set']==[12]; assert p['lambda_set']==[2]; assert p['mu_set']==[4]
def test_lines_and_turn_split():
    mod=load_module(); pts,adj=mod.build_graph(); assert len(mod.isotropic_lines(pts,adj))==40; stats=mod.nonbacktracking_turn_stats(adj); assert set(t for t,o in stats)=={2}; assert set(o for t,o in stats)=={9}
def test_result_payload_computed_w33_layer():
    mod=load_module(); r=mod.build_results(); assert r['counts']['directed_edges']==480; assert r['turn_split']['hashimoto_outdegree']==11; assert 'operator_core' in r['derived_sector_evidence']
