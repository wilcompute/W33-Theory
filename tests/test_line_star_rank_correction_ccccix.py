"""Regression tests for PART CCCCIX line-star rank correction."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCCIX_LINE_STAR_RANK_CORRECTION.py'
def load_module():
    spec=importlib.util.spec_from_file_location('line_star_rank_ccccix',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_rank_correction_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_rank_table():
    mod=load_module(); rt=mod.build_results()['rank_table']; assert rt['rank_X_vertex']==39; assert rt['rank_Z_triangle']==120; assert rt['base_k']==81; assert rt['rank_line_star_span']==120; assert rt['rank_X_plus_line_star']==120; assert rt['line_star_mod_vertex_rank']==81; assert rt['k_if_line_stars_are_stabilizers']==0
def test_line_star_counts():
    mod=load_module(); pkt=mod.build_results()['line_star_packet']; assert pkt['k4_lines']==40; assert pkt['line_star_triples']==160; assert pkt['line_star_weight']==3
def test_payload():
    mod=load_module(); r=mod.build_results(); assert 'span the full X-logical/matter sector' in r['architecture_upgrade']; assert 'supersedes the rank-effect statement' in r['honesty_boundary']
