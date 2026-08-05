from __future__ import annotations
import base64
import importlib.util
import json
import lzma
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN=ROOT/'analysis/bt3628_3634_octad_borel_matrix_proof_tomography.py'
BATCH=ROOT/'analysis/bt3631_real_star_proof_batch.py'
RESULT=ROOT/'data/PART_BT3628_BT3634_OCTAD_BOREL_MATRIX_PROOF_TOMOGRAPHY_results.json'
PROOFS=ROOT/'data/PART_BT3631_REAL_STAR_PROOF_BATCH.parts'

def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path)
 mod=importlib.util.module_from_spec(spec);assert spec.loader is not None;spec.loader.exec_module(mod);return mod

def test_seven_front_certificate_matches_frozen():
 mod=load(MAIN,'bt3628_3634')
 got=mod.build_result();old=json.loads(RESULT.read_text())
 assert got==old
 assert got['semantic_sha256']=='58b7e205ee0a1409230d50df6efc3abe8d67caf3125b9eaa654dd6600b7b1d25'

def test_abstract_octad_census_is_69():
 mod=load(MAIN,'bt3628_octad')
 x=mod.abstract_octad_pattern_census()
 assert x['orbit_counts_by_nontrivial_blocks']=={'1':6,'2':10,'3':10,'4':13,'5':14,'6':8,'7':6,'8':1}
 assert x['total_S8_orbits']==69
 assert x['maximum_triple_coincidence_excess']==56

def test_borel_core_bridge_decomposition():
 mod=load(MAIN,'bt3629_borel')
 x=mod.borel_core_bridge_presolve()
 assert x['shared_binary_core']=={'regular_internal':1530,'regular_regular':26163,'small_regular':3078}
 assert x['shared_core_variables']==30771
 assert x['P19']['residual_variables']==30771
 assert x['P57']['residual_variables']==30789
 assert x['P57_extension_rank']==18

def test_perkel_units_and_positive_form():
 mod=load(MAIN,'bt3630_perkel')
 x=mod.perkel_matrix_units_and_positive_form()
 assert x['matrix_units']==x['field_matrix_units']==9
 assert x['matrix_unit_digest']=='e9d441ac71aeaffe498936989909f7d1170d84826e8a4c2485a6ecf03cdfd98a'
 assert x['two_by_two_principal_minor']=='15/19'
 assert x['H_determinant']=='7/19'

def test_all_frozen_proof_DAGs_independently_verify():
 mod=load(BATCH,'bt3631_proofs')
 packed=''.join(p.read_text().strip() for p in sorted(PROOFS.glob('part*.b85')));batch=json.loads(lzma.decompress(base64.b85decode(packed)).decode())
 assert batch['instances']==16
 leaves=[]
 for row in batch['rows']:
  adj=[int(x,16) for x in row['adjacency_hex']]
  assert len(adj)==row['compatibility_vertices']
  assert mod.verify(adj,(1<<len(adj))-1,row['maximum_clique'],row['upper_proof'])
  assert all((adj[u]>>v)&1 for i,u in enumerate(row['witness']) for v in row['witness'][i+1:])
  assert mod.digest(row['upper_proof'])==row['proof_sha256']
  payload=dict(row);record=payload.pop('record_sha256')
  assert mod.digest(payload)==record
  leaves.append(record)
 assert mod.merkle(leaves)==batch['merkle_root']=='c176539c7b944274fb64965275ce3f900852fe4b26f67923b2ca6a2f06e256a4'
 assert batch['maximum_clique_histogram']=={'8':1,'9':1,'10':1,'11':3,'12':1,'13':2,'16':2,'31':5}

def test_minimum_marker_rank_three():
 mod=load(MAIN,'bt3632_marker')
 x=mod.marked_resolvent_tomography()
 assert x['minimum_marker_size']==3
 assert 'triangle-free' in x['rank3_separator']
 assert 'unique K4 line' in x['line_decoder']
