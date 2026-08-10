from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(n):return json.loads((ROOT/'data'/n).read_text())

def test_4664_two_s3s_are_transverse():
    d=load('PART_W33_PASS4664_TWO_S3S_JOINT_STRUCTURE.json')
    assert not d['separation']['same_ambient_S3']
    assert d['joint_group']['generated_structure']=='(C3 x C3):C2'
    assert d['joint_group']['generated_order']==18

def test_4665_full_aut_T():
    d=load('PART_W33_PASS4665_FULL_AUTOMORPHISM_T.json')
    assert d['incidence_graph']=={'vertices':85,'parts':[45,40],'degrees_by_part':[8,9],'side_swap_possible':False}
    assert d['full_automorphism_group']=='PGSp(4,3)' and d['full_automorphism_order']==51840

def test_4666_hermitian_stays_open():
    d=load('PART_W33_PASS4666_HERMITIAN_TWO_ADIC_EIGENLATTICE.json')
    assert d['two_adic_target']['equivalent_statement']=='L tensor Z_2 = K^perp_Z tensor Z_2'
    assert d['status'].startswith('OPEN:')
    assert all(x['v2_q2_plus_1']==1 for x in d['exact_anchors'])

def test_4667_one_bit_head_socle():
    d=load('PART_W33_PASS4667_SELECTED_SMITH_BIT_H10_HEAD_SOCLE.json')
    assert d['selected_torsion']['F2_dimension']==1
    assert d['equivariant_maps']['middle_V8_maps_to_or_from_bit']==0
    assert d['nilpotent']['rank']==1 and d['nilpotent']['square_zero']
    assert d['nilpotent']['image']=='<j>' and d['nilpotent']['kernel']=='V9'

def test_4668_f4_triality_plane_intertwiner():
    d=load('PART_W33_PASS4668_F4_MODULI_TO_TRIALITY_PLANES.json')
    assert d['PSp_equivariant_bijection']
    assert d['source_moduli']['count']==d['triality_moduli']['count']==40
    assert d['stabilizer_tower'].startswith('216')

def test_4669_orientation_double_cover():
    d=load('PART_W33_PASS4669_ORIENTED_F4_TRIALITY_DOUBLE_COVER.json')
    assert d['F4_cover']['oriented_objects']==d['triality_plane_cover']['oriented_objects']==80
    assert d['F4_cover']['base_objects']==d['triality_plane_cover']['base_planes']==40
    assert d['equivalence']['number_of_global_equivariant_orientation_matchings']==2

def test_4670_d4_reconstructs_T_h10_css():
    d=load('PART_W33_PASS4670_D4_LANE_RECONSTRUCTS_T_H10_CSS.json')
    assert d['reconstructed_cross_incidence']['shape']==[45,40]
    assert d['downstream']['CSS']=='[[40,10,4]]'
    assert d['downstream']['binary_middle_homology']=='H10 dimension 10'

def test_4671_local_s3_tower():
    d=load('PART_W33_PASS4671_LOCAL_F4_TRIALITY_S3_STABILIZER.json')
    assert [x['order'] for x in d['tower']]==[216,648,1296]
    assert d['quotients']=={'H1296_over_H216':'S3','H1296_over_H648':'C2','H648_over_H216':'C3=A3'}

def test_release_surfaces():
    needle='\\input{analysis/PASS4664_4671_s3_automorphism_eigenlattice_triality_insert}%'
    # Wrapper attachment can coexist with active 4656-4663 predecessor; once attached it must be present everywhere.
    present=[needle in (ROOT/n).read_text() for n in ('w33_paper.tex','photonic_holonet.tex','holonet_machine_blueprint.tex')]
    assert len(set(present))==1
    reg=json.loads((ROOT/'data/w33_public_frontier_extension_pass4461_4464.json').read_text())
    assert any(x['token']=='pass4664-4671-s3-automorphism-eigenlattice-triality' for x in reg['public_sections'])
    assert any(x['token']=='pass4664-4671-s3-automorphism-eigenlattice-triality-page' for x in reg['standalone_public_pages'])
