"""Regression tests for PART CCCCXIV integrated Q4 packet subsystem matrix."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCCXIV_INTEGRATED_Q4_PACKET_SUBSYSTEM_MATRIX.py'
def load_module():
    spec=importlib.util.spec_from_file_location('integrated_q4_packet_ccccxiv',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_integrated_packet_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_global_subsystem_parameters():
    mod=load_module(); r=mod.build_results(); g=r['global_packet_subsystem']; assert g['n']==1296; assert g['k']==81; assert g['d_packet_layer']==4; assert g['gauge_qubits']==729; assert g['center_rank']==486
def test_matrix_counts():
    mod=load_module(); c=mod.build_results()['matrix_counts']; assert c['X_gauge_rows']==972; assert c['Z_gauge_rows']==972; assert c['X_center_rows']==243; assert c['Z_center_rows']==243; assert c['X_center_rank']==243; assert c['Z_center_rank']==243
def test_attachment_summary():
    mod=load_module(); s=mod.build_results()['attachment_summary']; assert s['selected_line_star_reps']==81; assert s['attachments']==81; assert s['replacement_weight_target']==12
def test_payload():
    mod=load_module(); r=mod.build_results(); assert '[[1296,81,4]] packet layer' in r['architecture_upgrade']; assert 'dressed-logical verifier' in r['honesty_boundary']
