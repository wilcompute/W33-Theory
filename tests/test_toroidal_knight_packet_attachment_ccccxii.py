"""Regression tests for PART CCCCXII toroidal knight packet attachment."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCCXII_TOROIDAL_KNIGHT_PACKET_ATTACHMENT.py'
def load_module():
    spec=importlib.util.spec_from_file_location('knight_packet_ccccxii',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_attachment_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_knight_board():
    mod=load_module(); assert len(mod.knight_adj())==16; assert sorted({len(v) for v in mod.knight_adj().values()})==[4]; assert len(mod.knight_edges())==32; assert mod.tour_valid()
def test_line_star_basis_and_attachment():
    mod=load_module(); sel=mod.select_81_line_star_basis(); assert len(sel['selected'])==81; assert sel['initial_rank']==39; assert sel['final_rank']==120; assert len(mod.attachment_map())==81
def test_replacement_weight():
    mod=load_module(); a=mod.attachment_map()[0]; assert len(a['edge_to_column'])==3; assert sum(len(x['packet_support']) for x in a['edge_to_column'])==12
def test_payload():
    mod=load_module(); r=mod.build_results(); assert 'closed toroidal knight tour' in r['architecture_upgrade']; assert 'full global subsystem stabilizer' in r['honesty_boundary']
