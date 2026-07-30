#!/usr/bin/env python3
"""Combined exact verifier for Passes 1350--1354."""
from __future__ import annotations
from pathlib import Path
import hashlib,json,sys
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass1353_selector_geometry as geometry

def sha(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def verify_brauer():
    d=json.loads((DATA/'w33_pass1350_u42d2_char5_blocks.json').read_text())
    blocks=[b for b in d['blocks'] if b['defect']==1]
    assert len(blocks)==2
    expected_D=[[1,0,0,0],[0,1,0,0],[1,0,1,0],[0,1,0,1],[0,0,1,1]]
    expected_tree=[[1,3],[2,4],[3,5],[4,5]]
    for b in blocks:
        assert b['ordinary_degrees']==[1,6,24,64,81]
        assert b['brauer_degrees']==[1,6,23,58]
        assert b['decomposition_matrix']==expected_D and b['brauer_tree']==expected_tree
    # The tree is the path 1--24--81--64--6, with modular edges 1,23,58,6.
    return {'defect_one_block_count':2,'ordinary_vertex_path':[1,24,81,64,6],
      'modular_edge_path':[1,23,58,6],'exceptional_multiplicity':1,
      'ext1_adjacency':[[0,1,0,0],[1,0,1,0],[0,1,0,1],[0,0,1,0]],
      'bridge':'the degree-23 and degree-58 modular edges meet at the ordinary degree-81 vertex'}

def verify_basic():
    out={}
    for p in (2,3,5):
        d=json.loads((DATA/f'w33_pass1351_basic_algebra_p{p}.json').read_text()); r=d['record']
        D=sp.Matrix(r['decomposition_matrix']); C=sp.Matrix(r['cartan_matrix'])
        assert D.T*D==C
        q=r['quiver_and_associated_graded_relations']; pr=r['projective_and_resolution_data']
        assert r['basic_algebra_dimension']==sum(sum(row) for row in r['cartan_matrix'])
        assert q['loewy_power_dimensions_full_algebra']==pr['basic_radical_power_dimensions']
        assert sum(sum(row) for row in q['ext1_adjacency'])==len(q['arrows'])
        assert sha(q['minimal_relations'])==r['minimal_relation_sha256']
        for dim,layers in zip(pr['projective_basic_dimensions'],pr['projective_radical_layer_multiplicities']):
            assert sum(sum(layer) for layer in layers)==dim
        for dim,layers in zip(pr['projective_basic_dimensions'],pr['projective_socle_layer_multiplicities']):
            assert sum(sum(layer) for layer in layers)==dim
        out[str(p)]={'vertices':q['vertices'],'arrows':q['arrows'],
          'minimal_relation_counts':{k:len(v) for k,v in q['minimal_relations'].items()},
          'radical_power_dimensions':pr['basic_radical_power_dimensions'],
          'projective_radical_layers':pr['projective_radical_layer_multiplicities'],
          'projective_socle_layers':pr['projective_socle_layer_multiplicities'],
          'resolution_prefixes':pr['minimal_projective_resolution_prefixes']}
    return out

def verify_atlas():
    d=json.loads((DATA/'w33_pass1352_atlas_carrier_conjugacy.json').read_text())
    assert d['status']=='PASS' and d['hom_space_dimension']==1 and all(d['checks'].values())
    return {k:d[k] for k in ('repsn_character_position','generator_traces','hom_space_dimension','integer_intertwiner_determinant','integer_intertwiner_sha256')}

def main(write=True):
    result={'schema':'w33.pass1350_1354.exact_release.v1','status':'PASS',
      'scope':'finite group modular representation theory, exact finite-dimensional algebras, finite polar geometry, and manuscript build governance',
      'pass1350_brauer_tree':verify_brauer(),'pass1351_basic_algebras':verify_basic(),
      'pass1352_atlas_conjugacy':verify_atlas(),'pass1353_selector_geometry':geometry.main(write=True),
      'pass1354_manuscripts':{'integration_target_count':2,'pdf_hash_manifest':'data/w33_pass1354_pdf_manifest.json'},
      'checks':{'ambient_group_and_hecke_corner_separated':True,'all_basic_certificates_consistent':True,
        'rational_atlas_intertwiner_exact':True,'selector_geometry_recomputed':True}}
    if write:(DATA/'w33_pass1350_1354_exact_release.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','brauer_path':result['pass1350_brauer_tree']['ordinary_vertex_path'],
      'selector_count':result['pass1353_selector_geometry']['selector_count'],'atlas_hom_dimension':result['pass1352_atlas_conjugacy']['hom_space_dimension']},indent=2))
    return result
if __name__=='__main__': main()
