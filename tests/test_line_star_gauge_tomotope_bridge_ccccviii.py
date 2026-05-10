"""Regression tests for PART CCCCVIII line-star gauge / tomotope bridge."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCCVIII_LINE_STAR_GAUGE_TOMOTOPE_BRIDGE.py'
def load_module():
    spec=importlib.util.spec_from_file_location('line_star_gauge_ccccviii',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_line_star_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_line_star_counts_and_rank():
    mod=load_module(); r=mod.build_results(); pkt=r['line_star_packet']; assert pkt['k4_lines']==40; assert pkt['line_star_triples']==160; assert pkt['line_star_span_rank']==120; assert pkt['line_star_weight']==3
def test_rank_effect():
    mod=load_module(); r=mod.build_results(); eff=r['rank_effect']; assert eff['base_X_rank']==39; assert eff['Z_rank']==120; assert eff['X_plus_line_star_rank']==120; assert eff['line_star_mod_vertex_rank']==81; assert eff['if_added_as_stabilizers_k']==0
def test_tomotope_packet():
    mod=load_module(); r=mod.build_results(); tomo=r['tomotope_packet']; assert tomo['flags']==192; assert tomo['local_flags_per_edge']==16; assert 'Clifford chiralities' in tomo['local_decomposition']
def test_payload():
    mod=load_module(); r=mod.build_results(); assert 're-encoding' in r['architecture_upgrade']; assert 'agrees with CCCCIX' in r['honesty_boundary']
