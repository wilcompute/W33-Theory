"""Regression tests for PART CCCXLIX W33-derived sector assignments."""
from __future__ import annotations
import importlib.util
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCXLIX_W33_DERIVED_SECTOR_ASSIGNMENTS.py'
def load_module():
    spec=importlib.util.spec_from_file_location('w33_sector_cccxlix',MODULE_PATH); mod=importlib.util.module_from_spec(spec); assert spec.loader is not None; spec.loader.exec_module(mod); return mod
def test_all_sector_assignment_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=11
def test_generator_identity():
    mod=load_module(); assert mod.M2==Fraction(5049,4); assert mod.mm(mod.G,mod.G)==mod.ms(mod.M2,mod.I)
def test_operator_core_map():
    mod=load_module(); maps=mod.derive_maps(); assert maps['operator_core']['assignment']=={'mass':0,'gap':1,'heat_trace':0,'spinor_trace':1,'resolvent_trace':1,'zeta':0}
def test_minimal_bridge_has_three_sectors():
    mod=load_module(); maps=mod.derive_maps(); assert mod.count_sectors(maps['minimal_bridge']['assignment'])==3
def test_internal_response_recovers_m2():
    mod=load_module(); scales=mod.anchor_free_scales(mod.response_packet_from_G()); assert max(abs(v-float(mod.M2)) for v in scales.values())<1e-9
def test_result_payload_sector_layer():
    mod=load_module(); r=mod.build_results(); assert r['recommended_next_sector_tests']==['operator_core','minimal_bridge','transform_class']; assert 'derived_sector_maps' in r
