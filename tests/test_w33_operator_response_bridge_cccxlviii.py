"""Regression tests for PART CCCXLVIII W33 operator-response bridge compiler."""
from __future__ import annotations
import importlib.util
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'exploration'/'PART_CCCXLVIII_W33_OPERATOR_RESPONSE_BRIDGE.py'
def load_module():
    spec=importlib.util.spec_from_file_location('w33_bridge_cccxlviii',MODULE_PATH); mod=importlib.util.module_from_spec(spec); assert spec.loader is not None; spec.loader.exec_module(mod); return mod
def test_all_w33_bridge_checks_pass():
    mod=load_module(); r=mod.build_results(); assert r['verified'] is True; assert r['checks_passed']==r['checks_total']; assert r['checks_total']>=10
def test_generator_identities():
    mod=load_module(); assert mod.M2==Fraction(5049,4); assert mod.tr(mod.G)==0; assert mod.det(mod.G)==-mod.M2; assert mod.mm(mod.G,mod.G)==mod.ms(mod.M2,mod.I)
def test_registry_has_all_channels():
    mod=load_module(); reg=mod.registry(); assert set(reg.keys())==set(mod.CHANNELS); assert reg['resolvent_trace']['candidate_internal_operator']=='finite Green resolvent'
def test_internal_packet_recovers_m2():
    mod=load_module(); scales=mod.anchor_free_scales(mod.response_from_internal()); assert max(abs(v-float(mod.M2)) for v in scales.values())<1e-9
def test_result_payload_bridge_layer():
    mod=load_module(); r=mod.build_results(); assert r['w33_atoms']['M2']=='5049/4'; assert 'operator_response_registry' in r; assert 'finite W33 operators' in r['architecture_upgrade']
