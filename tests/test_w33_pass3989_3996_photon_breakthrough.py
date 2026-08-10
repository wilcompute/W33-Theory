from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def read(name): return json.loads((ROOT/'data'/name).read_text(encoding="utf-8"))

def test_maximum_code_orbits():
    x=read('PART_3991_MAXIMUM_CODE_ORBIT_CENSUS.json')
    assert x['status']=='PASS_EXACT_THREE_MAXIMUM_CODE_ORBITS'
    assert x['total_maximum_cliques']==945
    assert [r['orbit_size'] for r in x['maximum_code_orbits']]==[540,270,135]
    assert [r['parent_group_stabilizer_order'] for r in x['maximum_code_orbits']]==[96,192,384]
    assert x['semantic_sha256']=='852db084763db441845f0ef082a28b30c90a0f6eccd0aff32cc57fde7fa46757'

def test_photon_incidence_architecture():
    x=read('PART_3989_3990_3994_3996_PHOTON_INCIDENCE_ECHO_CLOCK.json')
    assert x['status']=='PASS_EXACT_SPARSE_COUPLER_ECHO_DARK_CLOCK_TOWER'
    c=x['pass3989_sparse_incidence_coupler']
    assert (c['total_modes'],c['incidence_edges'],c['degree'],c['girth'])==(80,160,4,8)
    assert c['bipartite_spectrum']=={'-4':1,'-sqrt(6)':24,'0':30,'sqrt(6)':24,'4':1}
    assert x['pass3994_dark_sector_memory']['total_dark_dimension']==30
    assert x['pass3995_exact_floquet_clock']['order']==4
    assert x['semantic_sha256']=='2223d77032d8b748cfeb32ec2ef6f2c68f43312a38b9b8c85b5e045d140404e9'

def test_central_fusion_summary():
    x=read('PART_3992_CENTRAL_FUSION_SUMMARY.json')
    assert x['all_set_partitions']==877
    assert x['inequivalent_central_fusions']==198
    assert x['primitive_simple_degrees']==[1,1,2,2,2,3,5]
    assert x['inequivalent_count_by_central_dimension']=={'1':1,'2':23,'3':68,'4':66,'5':31,'6':8,'7':1}

def test_wigner_smith_memory_and_information_delay():
    x=read('PART_3993_3996_WIGNER_SMITH_CAUSAL_MEMORY.json')
    assert x['status']=='PASS_EXACT_WIGNER_SMITH_MEMORY_WITH_DECLARED_CAUSAL_MODELS'
    q=x['wigner_smith_theorem']
    assert q['proper_delay_sectors_in_units_of_theta_prime']=={'0':1,'10':24,'16':15}
    assert q['mean_delay_in_units_of_theta_prime']==12
    assert q['delay_variance_in_units_of_theta_prime_squared']==12
    inv=x['self_similar_information_delay_invariant']
    assert inv['address_bits']=='m*log2(40)'
    assert inv['bits_per_mean_proper_delay']=='log2(40)/(12*theta_prime)'
    assert inv['relative_delay_standard_deviation']=='1/sqrt(12m)'
    assert x['semantic_sha256']=='5a666b410a874ac934ca60271f993ae74cc0c0605ef67c15834036baa3f7182d'

def test_combined_breakthrough_manifest():
    x=read('PART_3989_3996_PHOTON_BREAKTHROUGH_manifest.json')
    assert x['status']=='PASS_EXACT_FIVE_FRONT_THREE_BONKERS_MONSTER_WORDS_FOURIER_COEFFICIENT_FREEZE_AND_LAB_PENDING'
    assert x['fronts']['maximum_code_orbits']['result'].startswith('Exactly 945')
    assert x['bonkers']['wigner_smith_memory']['semantic_sha256']=='5a666b410a874ac934ca60271f993ae74cc0c0605ef67c15834036baa3f7182d'
    assert x['semantic_sha256']=='16397906a63553464abb18b0f65f839a7265afe9ef2fe712857c7e0efc977d27'
