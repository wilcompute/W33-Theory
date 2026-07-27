from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path: str):
    return json.loads((ROOT / path).read_text())

def test_pass1112_qontrol_boundary():
    x = load('data/w33_pass1112_qontrol_q8iv_transport.json')
    assert x['status'] == 'PASS_REFERENCE_TRANSPORT'
    assert x['schedule'] == {'total':240,'voltage_limit_commands':40,'routing_voltage_commands':160,'telemetry_queries':40}
    assert x['reference_run']['emergency_zero_ports'] == 40
    assert x['check_count'] == 16 and all(x['checks'].values())

def test_pass1113_a2_carrier():
    x = load('data/w33_pass1113_e8_a2_triple_carrier_extension.json')
    a = x['a2_triple_carrier']
    assert x['status'] == 'PASS'
    assert a['degree'] == 2240
    assert a['frame_visible_inner_products']['81_plus'] == 0
    assert a['frame_visible_inner_products']['81_minus'] == 3
    assert x['check_count'] == 14 and all(x['checks'].values())

def test_pass1114_cubic_phase():
    x = load('data/w33_pass1114_full_cubic_central_phase_extension.json')
    assert x['cubic_summary'] == {'total':45,'affine':36,'fiber':9}
    assert x['central_phase_histogram'] == {'0':25,'1':10,'2':10}
    assert x['jacobiator_support']['support_size'] == 9
    assert x['check_count'] == 20 and all(x['checks'].values())

def test_pass1115_formal_source_lock():
    x = load('data/w33_pass1115_formal_a2_phase_qontrol_lock.json')
    assert x['status'].startswith('PASS_SOURCE_READY')
    assert x['check_count'] == 10 and all(x['checks'].values())
    assert 'Pass1115A2PhaseQontrolClosure' in (ROOT/'formal/W33.lean').read_text()

def test_pass1121_equivariant_cubic_lifts():
    x = load('data/w33_pass1121_e8_a2_cubic_incidence.json')
    assert x['status'] == 'PASS'
    assert x['counts'] == {
        'a2_triples':2240,
        'cubic_supports':45,
        'firewall_supports':9,
        'positive_cubic_lifts':270,
        'negative_cubic_lifts':270,
        'total_cubic_lifts':540,
    }
    assert x['per_cubic_lifts']['positive_histogram'] == {'6':45}
    assert x['per_cubic_lifts']['negative_histogram'] == {'6':45}
    assert x['per_cubic_lifts']['total_histogram'] == {'12':45}
    assert all(a['root_projection'] and a['cubic_lifts'] for a in x['equivariance_by_simple_generator'])

def test_pass1121_ranks_and_firewall():
    x = load('data/w33_pass1121_e8_a2_cubic_incidence.json')
    r = x['matrix_ranks']
    assert r['lift_total_2240x45']['rank_Q_certified_mod_1000003'] == 45
    assert r['firewall_9x27']['rank_Q_certified_mod_1000003'] == 9
    assert x['firewall']['lift_histogram'] == {'12':9}
    assert x['check_count'] == 16 and all(x['checks'].values())

def test_pass1116_runtime_state_is_fail_closed():
    x = load('data/w33_pass1116_runtime_closure.json')
    assert x['status'] in {'PASS_LOCAL_RUNTIME_PENDING','PASS_OBSERVED_RUNTIME_CLOSURE'}
    assert x['check_count'] == 13 and all(x['checks'].values())

def test_local_check_total_before_observed_runtime():
    paths = [
        'data/w33_pass1112_qontrol_q8iv_transport.json',
        'data/w33_pass1113_e8_a2_triple_carrier_extension.json',
        'data/w33_pass1114_full_cubic_central_phase_extension.json',
        'data/w33_pass1115_formal_a2_phase_qontrol_lock.json',
        'data/w33_pass1116_runtime_closure.json',
        'data/w33_pass1121_e8_a2_cubic_incidence.json',
    ]
    assert sum(load(p)['check_count'] for p in paths) == 89
