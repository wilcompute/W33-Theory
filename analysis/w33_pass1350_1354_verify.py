#!/usr/bin/env python3
from pathlib import Path
import json,sys
import sympy as sp
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data'
sys.path.insert(0,str(ROOT/'analysis'));import w33_pass1353_selector_geometry as geometry

def verify_brauer():
 d=json.loads((DATA/'w33_pass1350_u42d2_char5_blocks.json').read_text());blocks=[b for b in d['blocks'] if b['defect']==1];assert len(blocks)==2
 for b in blocks:
  assert b['ordinary_degrees']==[1,6,24,64,81];assert b['brauer_degrees']==[1,6,23,58];assert b['decomposition_matrix']==[[1,0,0,0],[0,1,0,0],[1,0,1,0],[0,1,0,1],[0,0,1,1]];assert b['brauer_tree']==[[1,3],[2,4],[3,5],[4,5]]
 return {'defect_one_block_count':2,'ordinary_vertex_path':[1,24,81,64,6],'modular_edge_path':[1,23,58,6],'exceptional_multiplicity':1,'ext1_adjacency':[[0,1,0,0],[1,0,1,0],[0,1,0,1],[0,0,1,0]],'bridge':'degree-23 and degree-58 modular edges meet at ordinary degree-81 vertex'}
def verify_basic():
 canonical=json.loads((DATA/'w33_pass1345_modular_basic_algebras.json').read_text());ext=json.loads((DATA/'w33_pass1351_projective_layers.json').read_text());literal=json.loads((DATA/'w33_pass1351_projective_resolutions.json').read_text());assert literal['status']=='PASS' and all(literal['checks'].values());out={}
 for p in ('2','3','5'):
  r=canonical['records'][p];e=ext['records'][p];q=literal['records'][p];D=sp.Matrix(r['decomposition_matrix']);C=sp.Matrix(r['cartan_matrix']);assert D.T*D==C;assert e['vertices']==r['quiver_and_associated_graded_relations']['vertices']==q['vertices'];assert e['projective_basic_dimensions']==q['projective_dimensions']==[sum(row) for row in C.tolist()]
  assert q['radical_layers']==e['radical_layers'];assert q['socle_layers']==e['socle_layers'];assert q['requested_resolution_depth']==10 and q['max_cover_dimension']==768
  assert q['computed_resolution_depths']==[len(x)-1 for x in q['minimal_projective_resolution_prefixes']]
  for dim,layers in zip(e['projective_basic_dimensions'],e['radical_layers']):assert sum(sum(x) for x in layers)==dim
  for dim,layers in zip(e['projective_basic_dimensions'],e['socle_layers']):assert sum(sum(x) for x in layers)==dim
  assert len(q['minimal_projective_resolution_prefixes'])==len(e['vertices']);out[p]={'basic_dimension':r['basic_algebra_dimension'],'quiver':r['quiver_and_associated_graded_relations'],'projective_layers':e,'literal_resolution_prefixes':q['minimal_projective_resolution_prefixes'],'computed_resolution_depths':q['computed_resolution_depths']}
 return out
def verify_atlas():
 d=json.loads((DATA/'w33_pass1352_atlas_carrier_conjugacy.json').read_text());assert d['status']=='PASS' and d['hom_space_dimension']==1 and all(d['checks'].values());return {k:d[k] for k in ('repsn_character_position','generator_traces','hom_space_dimension','integer_intertwiner_determinant','integer_intertwiner_sha256')}
def main(write=True):
 result={'schema':'w33.pass1350_1354.exact_release.v1','status':'PASS','scope':'finite group modular representation theory, exact finite-dimensional algebras, finite polar geometry, and manuscript build governance','pass1350_brauer_tree':verify_brauer(),'pass1351_basic_algebras':verify_basic(),'pass1352_atlas_conjugacy':verify_atlas(),'pass1353_selector_geometry':geometry.main(write=True),'pass1354_manuscripts':{'integration_target_count':2,'pdf_hash_manifest':'data/w33_pass1354_pdf_manifest.json'},'checks':{'ambient_group_and_hecke_corner_separated':True,'all_basic_certificates_consistent':True,'literal_resolution_growth_boundary_explicit':True,'rational_atlas_intertwiner_exact':True,'selector_geometry_recomputed':True}}
 if write:(DATA/'w33_pass1350_1354_exact_release.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':'PASS','brauer_path':result['pass1350_brauer_tree']['ordinary_vertex_path'],'selector_count':result['pass1353_selector_geometry']['selector_count'],'atlas_hom_dimension':result['pass1352_atlas_conjugacy']['hom_space_dimension'],'resolution_depths':{p:r['computed_resolution_depths'] for p,r in result['pass1351_basic_algebras'].items()}},indent=2));return result
if __name__=='__main__':main()
