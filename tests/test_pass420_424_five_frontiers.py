from pathlib import Path
import importlib.util,json,sys
ROOT=Path(__file__).resolve().parents[1];ANALYSIS=ROOT/'analysis';sys.path.insert(0,str(ANALYSIS))
def load(name):
 p=ANALYSIS/f'{name}.py';s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);assert s.loader;s.loader.exec_module(m);return m

def test_pass420_incidence_lift():
 p=load('w33_pass420_integral_conductor_gluing').build_payload();assert p['status']=='PASS'
 assert all(r['lifted_critical_p_exponents']==r['frozen_critical_p_exponents'] for r in p['exact_instances'])
 assert [r['q'] for r in p['extension_field_constraint_engine']]==[25,27]

def test_pass421_phase_portrait():
 p=load('w33_pass421_qutrit_phase_portrait').build_payload();assert p['status']=='PASS'
 assert len(p['fixed_points'])==31;assert sorted(x['size'] for x in p['clifford_orbits'])==[3,4,6,6,6,6]
 assert all(x['classification']=='repelling' for x in p['fixed_points'])

def test_pass422_coding():
 p=load('w33_pass422_telemetry_coding_theorem').build_payload();assert p['status']=='PASS'
 assert [c['protected_bits'] for c in p['protected_codes']]==[18,21]
 assert p['source_statistics']['unordered_average_bits']<4

def test_pass423_inverse_compiler():
 p,a=load('w33_pass423_hardware_inverse_compiler').build_payload();assert p['status']=='PASS'
 assert a['component_count']==387;assert all(t['exact_support'] for t in p['deterministic_trials'])

def test_pass424_model_checker():
 p=load('w33_pass424_custody_model_checker').build_payload();assert p['status']=='PASS'
 assert p['model']['attack_generators']==13;assert p['model']['unique_mutated_states']>=80
 assert all(x['v2_errors'] for x in p['single_attack_results'].values())

def test_frozen_current_certificates():
 names=['w33_pass420_integral_conductor_gluing.json','w33_pass421_qutrit_phase_portrait.json','w33_pass422_telemetry_coding_theorem.json','w33_pass423_hardware_inverse_compiler.json','w33_pass424_custody_model_checker.json']
 for name in names:
  p=json.loads((ROOT/'data'/name).read_text(encoding="utf-8"));assert p['status']=='PASS';assert all(p['checks'].values())
