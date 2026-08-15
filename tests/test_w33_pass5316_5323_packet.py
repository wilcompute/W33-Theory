from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load(name):return json.loads((ROOT/'data'/name).read_text())

def test_pass5316_affine_latin_split():
    d=load('PART_W33_PASS5316_LATIN_KNIGHT_Q4_AFFINE_DERIVATIVE_CENSUS.json')
    assert d['latin_squares']==576
    assert d['klein_V4_class']['count']==144
    assert d['klein_V4_class']['constant_q4_derivatives']==4
    assert d['cyclic_C4_class']['constant_derivative_split']=={'0':240,'1':192}
    assert d['cyclic_C4_class']['one_constant_direction_masks']=={'1':48,'2':48,'4':48,'8':48}

def test_pass5317_triality_refinement():
    d=load('PART_W33_PASS5317_HOFFMAN_FOURCELL_TRIALITY_REFINEMENT.json')
    assert (d['H_orbits'],d['WD4_orbits'])==(10,22)
    assert (d['unsplit_H_orbits'],d['triality_triple_H_orbits'])==(4,6)
    assert d['WD4_orbits_by_span_rank']=={'33':2,'35':4,'38':4,'39':3,'40':9}

def test_pass5318_spread_triality():
    d=load('PART_W33_PASS5318_LATIN_SPREAD_TRIALITY_ACTION.json')
    assert d['latin_even_group_order']==288
    assert d['characteristic_tomotope_kernel_order']==96
    assert d['quotient']=='C3'
    assert d['outer_triality_representative']['spread_permutation']==[1,2,0,3,4]

def test_pass5319_natural_tomotope_action():
    d=load('PART_W33_PASS5319_D4_TESSERACT_FACEPAIRS_TOMOTOPE_ACTION.json')
    assert d['tesseract_square_faces']==24 and d['antipodal_square_face_pairs']==12
    assert d['WD4_order']==192 and d['WD4_center_order']==2 and d['induced_action_order']==96
    assert d['explicit_degree12_conjugator']==[0,1,4,5,8,9,11,10,7,6,3,2]

def test_pass5320_orbital_fusion():
    d=load('PART_W33_PASS5320_TESSERACT_ROTATION_VS_D4_FACEPAIR_ORBITAL_FUSION.json')
    assert d['WD4_tomotope_action']['orbital_rank']==5
    assert d['rotation_action']['orbital_rank']==4
    assert d['common_uncolored_small_relation']['graph']=='3 K4'

def test_pass5321_semidirect_geometry():
    d=load('PART_W33_PASS5321_TOMOTOPE_3K4_COORDINATE_PARTITION_SEMIDIRECT.json')
    assert d['coordinate_partition_labels']==[[[0,1],[2,3]],[[0,2],[1,3]],[[0,3],[1,2]]]
    assert d['component_action']['image']=='S3' and d['component_action']['image_order']==6
    assert d['kernel']['order']==16 and d['kernel']['structure']=='(C2)^4'

def test_manifest_promotes_insert():
    m=(ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex').read_text()
    assert r'\input{analysis/PASS5316_5321_latin_q4_d4_facepair_insert}%' in m
    assert (ROOT/'analysis/PASS5316_5321_latin_q4_d4_facepair_insert.tex').exists()

def test_consolidated_firewalls():
    d=load('PART_W33_PASS5316_5323_RESULTS.json')
    assert d['range']==[5316,5323]
    assert d['frontier']['hoffman_shortened_distance'].startswith('OPEN')
    assert d['frontier']['q11_footprint_distance'].startswith('OPEN')
    assert d['frontier']['all_odd_rank'].startswith('OPEN')
