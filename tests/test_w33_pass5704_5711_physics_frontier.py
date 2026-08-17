from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(name):return json.loads((ROOT/'data'/name).read_text())

def test_5704_wilson_and_face_selection():
 d=load('PART_W33_PASS5704_AFFINE_SU3_WILSON_FACE_SELECTION.json')
 assert d['face_support']['boundary_ranks_R']=={'line_triangles':12,'translation_plaquettes':24,'combined':28}
 assert d['tests']['nonabelian_commutator_distance_from_identity']>1e-6
 assert d['tests']['pure_gauge_triangle_holonomy_residual']<1e-8

def test_5705_group_bridge():
 d=load('PART_W33_PASS5705_DECK96_192_GROUP_FINGERPRINT.json')
 assert d['G96']['order']==96 and d['G96']['center_order']==2 and d['G96']['derived_order']==24
 assert d['projective_quotient']['order']==48
 assert d['D_extension']['order']==192 and d['D_extension']['exact_structure']=='G96 x C2'

def test_5706_deep_ramanujan():
 d=load('PART_W33_PASS5706_RAMANUJAN_LEVELS45_COLOR_GAUGE.json');ram=2*math.sqrt(3)
 assert d['new_levels']['1280_vertices']['ramanujan'] and d['new_levels']['2560_vertices']['ramanujan']
 assert all(x['nontrivial_radius']<ram for x in d['explicit_graph_levels'])

def test_5707_linfinity_correction():
 d=load('PART_W33_PASS5707_LINFINITY_L1_ZERO_NO_GO.json')
 assert d['repo_evidence']['builder_declares_l1_zero']
 assert d['repair_space_in_stated_model'].startswith('EMPTY')

def test_5708_generation_commutant():
 d=load('PART_W33_PASS5708_E8_27x3_GENERATION_COMMUTANT.json')
 assert d['commutant_dimensions']['E6_only']==9
 assert d['commutant_dimensions']['E6_x_center_Z3']==9
 assert d['commutant_dimensions']['E6_x_SU3_generated_by_T_and_C']==1

def test_5709_center_flux():
 d=load('PART_W33_PASS5709_Z3_CENTER_FLUX_SU3_ADJOINT_NOGO.json')
 assert d['affine_curvature']['histogram']=={'1':27,'2':27}
 assert d['adjoint_Wilson_trace']=={'0':8,'1':8,'2':8}

def test_5710_pfaffian_duality():
 d=load('PART_W33_PASS5710_DECK_DK_PFAFFIAN_TOPOLOGY.json')
 assert d['pfaffians']['same_sign_in_canonical_basis']
 assert d['DK_duality_residual']<1e-6
 assert d['D']['commutator_norm_with_H1']>1e-6 and d['D']['anticommutator_norm_with_H1']>1e-6

def test_5711_hierarchy_breaking():
 d=load('PART_W33_PASS5711_GENERATION_HIERARCHY_SYMMETRY_BREAKING.json')
 assert d['Hermitian_commutant_real_dimensions']=={'no_family_action':9,'center_Z3_only':9,'generic_torus':3,'full_SU3_generated':1}
 assert max(d['example_full_SU3_spectrum'])-min(d['example_full_SU3_spectrum'])<1e-12
