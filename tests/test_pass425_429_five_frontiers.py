from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

def load(name):
    p=json.loads((ROOT/'data'/name).read_text(encoding="utf-8"))
    assert p['status']=='PASS'
    assert all(p['checks'].values())
    return p

def test_pass425_exact_extension_smith():
    p=load('w33_pass425_exact_extension_smith.json')
    assert p['instances']['25']['critical_group_exact_valuations']=={'1':3200,'2':6976,'3':2800,'4':800,'6':623}
    assert p['instances']['27']['critical_group_exact_valuations']=={'1':1920,'2':3678,'3':6812,'4':3354,'5':1596,'6':595,'9':727}

def test_pass426_mixed_phase_portrait():
    p=load('w33_pass426_mixed_qutrit_phase_portrait.json')
    assert p['basin_summary']['mixed_attractor_count']==135
    assert p['basin_summary']['boundary_purifying_count']==6
    assert p['basin_summary']['exceptional_clifford_orbit']==[8,9,16,17,27,28]
    assert p['exceptional_ray_scan']['outcome_transitions']>=3

def test_pass427_adaptive_telemetry():
    p=load('w33_pass427_adaptive_telemetry_channel.json')
    assert p['average_lengths']['unordered_protected']<6.82
    assert p['average_lengths']['ordered_protected']<10.64
    assert max(x['protected_bits'] for x in p['frame_classes'])==21

def test_pass428_bayesian_diagnosis():
    p=load('w33_pass428_bayesian_hardware_diagnosis.json')
    assert sum(x['top1_correct'] for x in p['noise_scenarios'])>=149
    assert sum(x['top5_correct'] for x in p['noise_scenarios'])==150
    assert p['delay_vs_trim']['shared_delay_log_bayes_factor_range'][0]>0
    assert p['delay_vs_trim']['independent_trims_log_bayes_factor_range'][1]<0

def test_pass429_inductive_custody():
    p=load('w33_pass429_inductive_custody_verification.json')
    assert len(p['induction_cases'])==24
    assert all(x['preserved'] for x in p['induction_cases'])
    assert all(x['breaks_invariant'] for x in p['guard_counterexamples'].values())
    assert (ROOT/'specs'/'W33Pass429CustodyInductive.tla').exists()

def test_cross_pass_closure():
    p425=load('w33_pass425_exact_extension_smith.json')
    p426=load('w33_pass426_mixed_qutrit_phase_portrait.json')
    p427=load('w33_pass427_adaptive_telemetry_channel.json')
    p428=load('w33_pass428_bayesian_hardware_diagnosis.json')
    p429=load('w33_pass429_inductive_custody_verification.json')
    assert p425['instances']['25']['critical_group_p_valuation']==32490
    assert abs(p426['maximally_mixed']['acceptance_probability']-1/81)<1e-6
    assert p427['average_lengths']['unordered_protected']<p427['average_lengths']['unordered_fixed']
    assert p428['priors']['null']+sum(p428['priors']['families'].values())==1
    assert p429['checks']['proof_is_not_bounded_attack_enumeration']
