"""Regression tests for PART CCCCXIII toroidal knight = Q4 hypercube packet."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCCXIII_TOROIDAL_KNIGHT_HYPERCUBE_PACKET.py'
def load_module():
    spec=importlib.util.spec_from_file_location('knight_hypercube_ccccxiii',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_hypercube_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_graph_is_q4():
    mod=load_module(); assert len(mod.knight_adj())==16; assert len(mod.knight_edges())==32; assert mod.mapped_edges()==mod.q4_edges()
def test_dimension_counts():
    mod=load_module(); assert mod.dimension_edge_counts()=={0:8,1:8,2:8,3:8}
def test_gray_cycle():
    mod=load_module(); assert mod.tour_is_gray_cycle(); assert mod.tour_flip_sequence()==[1,2,1,3,1,2,1,0,1,2,1,3,1,2,1,0]
def test_payload():
    mod=load_module(); r=mod.build_results(); assert 'true 4-bit hypercube packet' in r['architecture_upgrade']; assert 'global W33-to-packet subsystem distance' in r['honesty_boundary']
