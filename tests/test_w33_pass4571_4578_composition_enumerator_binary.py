from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load(name):return json.loads((ROOT/'data'/name).read_text())

def test_pass4571_composition_boundary():
    d=load('PART_W33_PASS4571_DUAL_MIDDLE_MODULE_COMPOSITION.json')
    assert d['S186']['composition_factors']=={'6':5,'8':1,'14':2,'40':3}
    assert d['S186']['composition_factor_dimension_check']==186
    assert d['S250_over_S186']['dimension']==64 and d['S250_over_S186']['irreducible']
    assert 'complete unlabeled Loewy lattice' in d['boundary']

def test_pass4572_real_enumerator_mass_but_full_open():
    d=load('PART_W33_PASS4572_SUPPORT89_ENUMERATOR.json')
    assert d['new_exact_labeled_subsets']==350343565
    assert d['support8']['subsets']==76904685 and d['support8']['minimum_weight']==528 and d['support8']['spectrum']['960']==1755
    assert d['support9']['subsets']==273438880 and d['support9']['minimum_weight']==582 and d['support9']['spectrum']['1026']==360
    assert d['status']=='EXACT_SUPPORT_8_9_COMPLETE_FULL_ENUMERATOR_OPEN'
    assert 'No 2^39 checksum' in d['boundary']

def test_pass4573_counterexample():
    d=load('PART_W33_PASS4573_GENERAL_GQ_C8_SELECTOR_OBSTRUCTION.json')
    assert d['universal_C8_coefficient_selector'] is False
    assert d['counterexample']['apartments']==90 and d['counterexample']['induced_K13_supports']==60
    assert d['counterexample']['primitive_C8_degree4_apartment_coefficient']==d['counterexample']['primitive_C8_degree4_K13_coefficient']==36

def test_pass4574_observed_q53_action():
    d=load('PART_W33_PASS4574_Q53_GLOBAL_PRISM_ACTION_OBSERVED.json')
    assert d['status']=='OBSERVED_EXACT_REPRODUCTION'
    assert d['generators']['full_projective_order']==13063680
    assert d['noncollinear_pair_action']['setwise_stabilizer_order']==2880
    assert d['noncollinear_pair_action']['unordered_3_subset_orbit_size']==120
    assert d['global_prism_action']=={'orbit_size':544320,'stabilizer_order':24,'transitive':True}

def test_pass4575_binary_cubic_code():
    d=load('PART_W33_PASS4575_CUBIC_INCIDENCE_BINARY_CODE.json')
    assert d['binary_rank']==6
    assert d['row_code']['parameters']=='[36,6,16]'
    assert d['column_code']['parameters']=='[27,6,12]'
    assert d['row_code']['dual_kernel']['A3']==120 and d['column_code']['dual_kernel']['A3']==45

def test_pass4576_quadratic_no_go():
    d=load('PART_W33_PASS4576_O8PLUS_O6MINUS_QUADRATIC_NO_GO.json')
    assert d['boolean_degree_le2']['V8_to_U6']=={'equation_rank':222,'solution_dimension':0,'unknown_coefficients':222}
    assert d['boolean_degree_le2']['U6_to_V8']=={'equation_rank':176,'solution_dimension':0,'unknown_coefficients':176}

def test_pass4577_fiber_polarity():
    d=load('PART_W33_PASS4577_APARTMENT_FIBER_O8PLUS_POLARITY.json')
    assert d['reconstructed_singular_polar_graph_srg']==[135,70,37,35]
    assert d['polar_reconstruction']['B1_pair_count']==4320 and d['polar_reconstruction']['B0_pair_count']==4725
    assert d['orthogonal_pair_n2_distribution']=={'0':1620,'2':810,'6':2160,'48':135}

def test_pass4578_reject_count_match():
    d=load('PART_W33_PASS4578_ANISOTROPIC120_DOUBLE_SIX_TRIPLES.json')
    assert d['double_six_triple_orbit_sizes']==[120,540,1080,2160,3240]
    assert d['protected_Gset']['suborbits']==[1,1,1,27,27,27,36]
    assert d['double_six_triple_Gset']['suborbits']==[1,2,27,36,54]
    assert d['equivariant_bijection'] is False
