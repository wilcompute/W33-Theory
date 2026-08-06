from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def read(name): return json.loads((ROOT/'data'/name).read_text())

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
