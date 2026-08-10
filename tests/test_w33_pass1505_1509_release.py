import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def cert(n):return json.loads((ROOT/'data'/n).read_text(encoding="utf-8"))

def test_all_frozen_certificates_pass():
 for name in ('w33_pass1505_exact_cover_census_frontier.json','w33_pass1506_bridge_local_arithmetic.json','w33_pass1507_joint_algebra_morita.json','w33_pass1508_contextuality_protocol.json','w33_pass1509_qutrit_hamming_m20_chart.json'):
  p=cert(name);assert p['status']=='PASS';assert all(p['checks'].values())

def test_cover_frontier_values():
 p=cert('w33_pass1505_exact_cover_census_frontier.json')
 assert p['distinct_full_orbits']==327
 assert p['certified_cover_lower_bound']==3547800
 assert p['stabilizer_type_histogram']=={'C2':228,'C2xC2':9,'C4':75,'C4xC2':6,'D8':9}

def test_bridge_smith_and_morita_values():
 p=cert('w33_pass1506_bridge_local_arithmetic.json')
 assert p['smith_forms']['C']=={'1':10,'3':5}
 assert p['smith_forms']['F']=={'1':10,'3':4,'6':1}
 q=cert('w33_pass1507_joint_algebra_morita.json')
 assert q['dimension_lower_bound']==301
 assert q['morita_context']['identities'][:4]==['e^2=e','q^2=q','xy=q','yx=e']

def test_contextuality_runner_self_tests_and_rejection():
 p=cert('w33_pass1508_contextuality_protocol.json')
 assert p['self_tests']['uniform']['contextual_fraction']==0
 assert p['self_tests']['pr']['contextual_fraction']==1
 m=load(ROOT/'analysis'/'w33_pass1508_contextual_fraction_falsifier.py','cf')
 try:m.contextual_fraction({'bad_contexts':4,'total_contexts':40})
 except ValueError:pass
 else:raise AssertionError('geometry-only deficit must be rejected')

def test_qutrit_hamming_m20_chart():
 p=cert('w33_pass1509_qutrit_hamming_m20_chart.json')
 assert p['chart_size']==243
 assert p['hamming_shells']=={'0':1,'1':10,'2':40,'3':80,'4':80,'5':32}
 assert p['stabilizer']['order']==960
 assert p['stabilizer']['structure']=='2^4:A5'
 assert p['stabilizer']['atlas_name']=='M20'

def test_compiled_census_sources_present():
 assert (ROOT/'analysis'/'cpp'/'w33_pass1505_exact_cover_prefix.cpp').exists()
 assert (ROOT/'analysis'/'cpp'/'w33_pass1505_orbit_reduce.cpp').exists()

def test_release_manifest_and_independent_cover_audit():
 p=cert('w33_pass1505_1509_release_manifest.json')
 assert p['status']=='PASS'
 assert p['validation']=={'certificate_checks':59,'cpp_sources_compile':True,'latex_insert_compiles':True,'pytest_tests':7}
 assert p['independent_cover_audit']['normalized_prefix_covers']==100000
 assert p['independent_cover_audit']['all_exact_partitions'] is True
