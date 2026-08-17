from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(name):
    return json.loads((ROOT/'data'/name).read_text())

def test_5691_affine_gauge_complex():
    d=load('PART_W33_PASS5691_AFFINE_SU3_DISCRETE_YM_COMPLEX.json')
    c=d['affine_complex']
    assert c['cycle_space_dim_R']==28
    assert c['rank_translation_faces_R']==24
    assert c['H1_translation_complex_R']==4
    assert c['rank_translation_plus_line_faces_R']==28
    assert c['H1_with_line_faces_R']==0
    assert c['H1_with_line_faces_F3']==2

def test_5692_flatray_duality():
    d=load('PART_W33_PASS5692_DECK16_FLATRAY_DUALITY.json')
    assert d['centralizer_involution']['commutes_with_all_signed_stabilizer_elements']
    assert d['centralizer_involution']['group_order_after_adjoining_D']==192
    assert d['bond_sign_disagreements_up_to_global_sign']==12

def test_5693_explicit_ramanujan_depth():
    d=load('PART_W33_PASS5693_EXPLICIT_RAMANUJAN_LEVELS23.json')
    bound=2*math.sqrt(3)
    assert d['level1_to_level2_signing']['signed_radius']<bound
    assert d['level2_to_level3_signing']['signed_radius']<bound
    assert [x['vertices'] for x in d['explicit_levels']]==[80,160,320,640]
    assert all(x['nontrivial_radius']<bound+1e-7 for x in d['explicit_levels'])

def test_5694_jacobi_information_no_go():
    d=load('PART_W33_PASS5694_COLLISION_JACOBI_L3_NO_GO.json')
    assert d['collision_support']=={'horizontal_kept':36,'vertical_deleted':9,'deletion_mask':'C/3'}
    assert d['numerical_symbolic_identity_max_residual']<1e-10

def test_5695_tensor_separation():
    d=load('PART_W33_PASS5695_RAMANUJAN_DIRAC_TENSOR_SEPARATION.json')
    assert d['internal_capacities_first_levels']==[80,160,320,640,1280]
    assert d['numeric_probe']['kronecker_sum_spectrum_residual']<1e-7

def test_5696_full_affine_twist():
    d=load('PART_W33_PASS5696_AGL_ORIENTATION_TWISTED_SU3.json')
    assert d['groups']['AGL(2,3)']==432
    assert 'all 432' in d['exact_equivariance']

def test_5697_internal_adjoint_gap():
    d=load('PART_W33_PASS5697_RAMANUJAN_ADJOINT_LAPLACIAN_GAP.json')
    lower=4-2*math.sqrt(3)
    assert abs(d['universal_bound']['laplacian_gap_min']-lower)<1e-12
    assert all(x['scalar_laplacian_gap']>=lower-1e-7 for x in d['explicit_W33_levels'])

def test_5698_generation_falsifier():
    d=load('PART_W33_PASS5698_VERTICAL_Z3_GENERATION_FALSIFIER.json')
    assert d['joint_multiplicities']==[1,1,1,1,1,1]
    assert d['joint_commutant']=='C^6, complex dimension 6'

def test_packet_summary_boundary():
    d=load('PART_W33_PASS5691_5698_PHYSICS_YM_DUALITY_RAMANUJAN_FRONTIER_SUMMARY.json')
    assert d['pass_range']==[5691,5698]
    assert 'QCD/Yang-Mills derivation' in d['boundary']
