"""Regression tests for PART CCCLX Seidel/interlacing response-sector fusion."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCLX_SEIDEL_INTERLACING_RESPONSE_SECTOR_FUSION.py'
def load_module():
    spec=importlib.util.spec_from_file_location('fusion_ccclx',MODULE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def test_all_fusion_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=11
def test_interlacing_certificates():
    mod=load_module(); assert mod.hoffman_bound()==10; assert mod.fisher_clique_bound()==4; assert mod.neighborhood_certificate()['vertices']==12; assert mod.nonneighborhood_certificate()['vertices']==27
def test_two_graph_certificate():
    mod=load_module(); tg=mod.two_graph_certificate(); assert tg['odd_size']==4480; assert tg['edge_pair_count']==20; assert tg['nonedge_pair_count']==16; assert tg['edge_nonedge_difference']==4
def test_sector_certificates():
    mod=load_module(); certs=mod.sector_certificates(); assert certs['sector_0']['channels']==['mass','heat_trace','zeta']; assert certs['sector_1']['channels']==['gap','spinor_trace','resolvent_trace']
def test_result_payload_ccclx():
    mod=load_module(); r=mod.build_results(); assert 'two-graph' in r['architecture_upgrade']; assert 'interlacing' in r['architecture_upgrade']; assert r['preferred_sector_map']['mass']==0; assert r['preferred_sector_map']['gap']==1
