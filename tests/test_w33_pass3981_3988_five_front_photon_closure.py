from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(path): return json.loads((ROOT/path).read_text(encoding='utf-8'))

def test_global_mesh_bound():
    x=load('data/PART_3982_GLOBAL_MESH_BOUND.json')
    h=x['universal_half_cut_rank_lower_bounds']
    assert 2*sum(h[:-1])+h[-1]==229
    assert x['base_bound']==sum(x['base_cut_ranks'])==253
    assert x['best_bound']==sum(x['best_cut_ranks'])==251
    assert sorted(x['base_order'])==sorted(x['best_order'])==list(range(36))

def test_photon_nuisance_design():
    x=load('data/PART_3984_PHOTON_NUISANCE_TOMOGRAPHY.json')
    assert x['design_rank']==x['parameters']==16
    assert x['cells']==48
    assert x['omitted_bias_removed']
    assert abs(x['full_model_gamma_estimate'])<1e-15
    assert x['omitted_variable_gamma_estimate']>1e-9

def test_exact_global_reflection_identity():
    # W33 SRG relation A^2=8I-2A+4J.
    # U=-(I+A)/3+2J/15; verify coefficients of U^2 in I,A,J.
    # (I+A)^2 = I+2A+A^2 = 9I+4J.
    # J(I+A)=(1+12)J=13J and J^2=40J.
    i=Fraction(9,9)
    a=Fraction(0)
    j=Fraction(4,9)-2*Fraction(2,45)*13+Fraction(4,225)*40
    assert (i,a,j)==(1,0,0)
    x=load('data/PART_3986_3988_PHOTON_CHAINED_CONSTRUCTIONS.json')
    assert x['pass3988_exact_global_reflection']['row_multiplicities']=={'nonneighbor':27,'point_or_neighbor':13}
    assert x['pass3986_spectral_metrology']['localized_qfi']==48.0
    assert x['pass3987_dual_geometry_echo']['full_space_optimal_qfi']==400

def test_rank48_and_publication_reachability():
    tensor=load('data/PART_3973_3980_EXTREMAL_MESH_PHOTON_TENSOR_manifest.json')['rank48_tensor']
    assert tensor['relations']==48
    assert tensor['nonzero_intersection_constants']==904
    manifest=(ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex').read_text(encoding='utf-8')
    needle=r'\input{analysis/BT3981_BT3988_five_front_three_photon_closure_insert}%'
    assert manifest.count(needle)==1
    assert (ROOT/'docs/five-front-photon-closure.html').is_file()
    assert (ROOT/'analysis/BT3981_BT3988_five_front_three_photon_closure_index_insert.html').is_file()

def test_external_gates_remain_fail_closed():
    registry=load('data/w33_pass_namespace_registry_v2.d/3981-3988.json')
    assert registry['status']=='completed_with_fail_closed_external_gates'
    assert any('Monster' in item for item in registry['pending'])
    assert (ROOT/'analysis/w33_pass3985_monster_class_fusion_sieve.g').is_file()
    assert (ROOT/'analysis/w33_mmgroup_u42_candidate_harness.py').is_file()
