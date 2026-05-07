"""Regression tests for PART CCCCXI tomotope Bacon-Shor packet code."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCCXI_TOMOTOPE_BACON_SHOR_PACKET_CODE.py'
def load_module():
    spec=importlib.util.spec_from_file_location('tomotope_bacon_shor_ccccxi',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_packet_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']
def test_packet_parameters():
    mod=load_module(); p=mod.packet_summary(); assert p['n']==16; assert p['k']==1; assert p['d']==4; assert p['d_X']==4; assert p['d_Z']==4; assert p['gauge_qubits']==9; assert p['rank_stabilizer_center']==6
def test_global_layer():
    mod=load_module(); g=mod.global_packet_layer(); c=mod.concatenated_target(); assert g['n']==1296 and g['k']==81 and g['d']==4; assert c['d_lower_bound']==12
def test_layout():
    mod=load_module(); layout=mod.packet_layout(); assert len(layout)==16; assert sorted({x['chart_vertex'] for x in layout})==[0,1,2,3]; assert sorted({x['orientation'] for x in layout})==[0,1]; assert sorted({x['chirality'] for x in layout})==[0,1]
def test_payload():
    mod=load_module(); r=mod.build_results(); assert '[[16,1,4]]' in r['architecture_upgrade']; assert 'global subsystem distance' in r['honesty_boundary']
