from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/'data'/name).read_text())

def test_5683_ramanujan_lift():
    x=load('PART_W33_PASS5683_BALANCED_RAMANUJAN_LEVI_LIFTS.json')
    assert x['pass']==5683
    assert x['base']['vertices']==80 and x['base']['degree']==4
    assert x['explicit_first_lift']['negative_edges']==80
    assert x['explicit_first_lift']['negative_degree_at_every_vertex']==2
    assert x['explicit_first_lift']['signed_spectral_radius'] < 2*math.sqrt(3)
    assert x['explicit_first_lift']['connected'] is True

def test_5684_collision_firewall_weld():
    x=load('PART_W33_PASS5684_COLLISION_LINFINITY_SUPPORT_WELD.json')
    assert x['pass']==5684
    assert x['cubic_supports']=={'total':45,'horizontal':36,'vertical':9}
    assert 'C(T)/3' in x['exact_mask_identity']

def test_5685_flatbond_ratio2():
    x=load('PART_W33_PASS5685_DECK16_LOCAL_FLATBOND_RATIO2.json')
    assert x['starting_equivariant_Kodd_dimension']==4
    assert x['support_preserving_subspace_dimension']==2
    rays=x['projective_flat_bond_rays']
    assert len(rays)==2
    assert all(abs(r['ratio']-2)<1e-7 for r in rays)

def test_5686_asl_su3():
    x=load('PART_W33_PASS5686_ASL23_SU3_BRACKET.json')
    assert x['groups']['AGL(2,3)']==432 and x['groups']['ASL(2,3)']==216
    assert x['subgroup_enumeration']['Hom_AGL_Lambda2V8_to_V8']==0
    assert x['subgroup_enumeration']['Hom_ASL_Lambda2V8_to_V8']==1
    assert x['exact_checks']['ASL_equivariance'] is True
    assert x['exact_checks']['Jacobi'].startswith('zero')
    assert x['exact_checks']['Killing_on_V8']=='-54 I_8'
    assert 'su(3)' in x['lie_identification']

def test_5687_metric_clock_expander():
    x=load('PART_W33_PASS5687_METRIC_CLOCK_EXPANDER_NO_SPACETIME.json')
    assert x['ramanujan_network']['degree']==4
    assert x['ramanujan_network']['normalized_gap_lower']>0
    assert abs(x['d3_example']['after_3_levels']-.5)<1e-12

def test_5688_signing_comparison():
    x=load('PART_W33_PASS5688_BALANCED_SIGNING_SEARCH_VS_RANDOM.json')
    R=x['ramanujan_threshold']
    assert x['single_chord']['signed_radius']>R
    assert x['locally_balanced_2factor']['signed_radius']<R
    assert x['edge_balanced_spectral_witness']['signed_radius']<x['locally_balanced_2factor']['signed_radius']
    assert x['fixed_random_half_negative_baseline']['samples']==256

def test_5689_fermionic_boundary():
    x=load('PART_W33_PASS5689_FERMIONIC_EXTERIOR_COLLISION_BOUNDARY.json')
    c=x['counts']
    assert (c['horizontal_survive_full'],c['vertical_survive_full'])==(36,9)
    assert (c['horizontal_survive_base_hardcore'],c['vertical_survive_base_hardcore'])==(36,0)

def test_5690_synthetic_chern():
    x=load('PART_W33_PASS5690_DECK16_SYNTHETIC_BERRY_CHERN8.json')
    assert x['absolute_chern_number']==8
    assert x['first_chern_number_in_this_convention']==8
    assert abs(x['line_bundles']['numeric_c1_L_minus']-1)<2e-5
