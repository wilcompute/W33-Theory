from __future__ import annotations
import importlib.util,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod

def test_full_noisy_base_filter_exact_counts_and_streaming_identity():
    m=load('analysis/bt3133_3140_certifying_adaptive_inference.py','bt3133')
    r=m.pass3133()
    assert r['hypotheses']==48826
    assert r['unique_immediately']==44848
    assert r['signature_classes']==46284
    assert r['largest_collision_class']==3
    assert r['batch_stream_max_abs_difference']<2e-14

def test_streaming_single_edit_relocks_within_three():
    m=load('analysis/bt3133_3140_certifying_adaptive_inference.py','bt3136')
    r=m.pass3136()
    assert r['single_edit_scenarios']==576
    assert r['received_symbols_to_relock_histogram']=={2:565,3:11}
    assert r['worst_received_symbols_to_relock']==3

def test_action_rate_distortion_frontier_and_contraction():
    m=load('analysis/bt3133_3140_certifying_adaptive_inference.py','bt3137')
    f=m.pass3137();c=m.pass3138()
    assert f['catalogue_points']==105 and f['pareto_points']==11
    assert f['lower_convex_frontier'][0]['sensor']=='stop'
    assert f['lower_convex_frontier'][-1]['sensor']=='full'
    moderate=c['profiles']['moderate']
    assert abs(moderate['dobrushin']-0.9969072164948454)<1e-12
    assert moderate['tv_memory_horizon']['1e-6']==4461

def test_recursive_context_and_collision_bridge_counts():
    m=load('analysis/bt3133_3140_certifying_adaptive_inference.py','bt3139')
    v=m.pass3139();b=m.pass3140()
    assert v['context_table'][-1]['saved_bits_independent']==32
    assert abs(b['reduction']-1/12)<1e-15
    assert abs(b['avoided_collision_exposures']['mean_program']-1.18129875)<1e-12

def test_rank3_certifier_rejects_negative_control(tmp_path):
    m=load('analysis/bt3134_rank3_code_certifier.py','bt3134')
    payload=json.loads((ROOT/'data/PART_BT3134_rank3_candidate_fixture.json').read_text())
    result=m.certify(payload['candidates'][0])
    assert result['generator_rank']==3
    assert result['projector_trace']==8.0
    assert not result['accepted']
    assert 'range is not contained in single-error complement' in result['reasons']
