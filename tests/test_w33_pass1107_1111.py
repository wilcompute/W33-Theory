from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())

def test_qontrol_second_vendor_boundary():
    x=load('data/w33_pass1107_qontrol_q8iv_transport.json')
    assert x['status']=='PASS_REFERENCE_TRANSPORT'
    assert x['vendor_profile']['vendor']=='Qontrol'
    assert x['schedule']=={'total':240,'voltage_limit_commands':40,'routing_voltage_commands':160,'telemetry_queries':40}
    assert x['reference_run']['emergency_zero_ports']==40

def test_qontrol_receipt_has_no_hardware_claim():
    x=load('hardware/w33_pass1107_qontrol_q8iv_receipt.json')
    assert x['physical_hardware_connected'] is False
    assert x['detector_triggered'] is False
    assert x['all_ports_zeroed'] is True

def test_a2_triple_extension_beats_pair_minimum():
    x=load('data/w33_pass1108_e8_a2_triple_carrier_extension.json')
    a=x['a2_triple_carrier']
    assert a['degree']==2240
    assert a['frame_visible_inner_products']['81_plus']==0
    assert a['frame_visible_inner_products']['81_minus']==3
    assert x['upstream_pass1104']['pair_universe_minimum']['degree']==3360

def test_all45_central_phase_extension():
    x=load('data/w33_pass1109_full_cubic_central_phase_extension.json')
    assert (len(x['cubic_triads']) if 'cubic_triads' in x else x['cubic_summary']['total'])==45
    assert x['central_phase_histogram']=={'0':25,'1':10,'2':10}
    assert sum(r['canonical_cubic_sign']==1 for r in x['hyperplane_fiber_transport'])==2
    assert sum(r['canonical_cubic_sign']==-1 for r in x['hyperplane_fiber_transport'])==7

def test_formal_extension_surface():
    x=load('data/w33_pass1110_formal_a2_phase_qontrol_lock.json')
    s=(ROOT/x['lean_module']).read_text()
    assert x['status'].startswith('PASS_SOURCE_READY')
    assert 'a2Triple_three_81Minus' in s
    assert 'centralPhaseHistogram' in s
    assert 'qontrolScheduleCounts' in s
    assert 'native_decide' not in s

def test_umbrella_imports_pass1110():
    assert 'import W33.Pass1110A2PhaseQontrolClosure' in (ROOT/'formal/W33.lean').read_text()

def test_runtime_closure_is_explicit():
    x=load('data/w33_pass1111_runtime_closure.json')
    assert x['status'] in {'PASS_LOCAL_RUNTIME_PENDING','PASS_OBSERVED_RUNTIME_CLOSURE'}
    assert x['local_exact_checks']['total']==72
    assert x['checks']['workflow_is_pull_request_visible']

def test_release_ledger():
    x=load('data/w33_pass1107_1111_release.json')
    assert x['local_exact_checks']==72
    assert x['pytest'].startswith('8 passed')
    assert x['passes']['1108']['result'].startswith('A2')
