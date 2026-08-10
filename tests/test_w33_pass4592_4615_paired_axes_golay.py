import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/'data'/name).read_text())

def test_paired_simplex_hexacode_golay():
    c=load('PART_W33_PASS4592_PAIRED_AXES_SIMPLEX_HEXACODE_GOLAY.json')
    assert c['paired_axes']['same_message_concatenation']=='[63,6,32] binary simplex'
    assert c['paired_axes']['dual']=='[63,57,3] binary Hamming'
    assert c['hexacode']['parameters']=='[6,3,4]_4'
    assert c['hexacode']['binary_concatenation']=='[18,6,8]'
    assert c['golay_embedding']['word_for_word_verified'] is True
    assert c['golay_embedding']['zero_coordinates']==[17,18,19,20,21,22]

def test_support10_exact_mass():
    c=load('PART_W33_PASS4593_SUPPORT10_EXACT.json')
    assert c['subsets']==847660528
    assert c['distinct_weights']==147
    assert (c['minimum_weight'],c['minimum_count'])==(582,2160)
    assert (c['maximum_weight'],c['maximum_count'])==(1080,36)
    assert sum(map(int,c['spectrum'].values()))==847660528

def test_s186_series():
    c=load('PART_W33_PASS4601_S186_COMPOSITION_SERIES_SKELETON.json')
    assert c['composition_series_dimensions']==[0,14,54,60,74,80,120,126,134,140,146,186]
    assert c['ordered_simple_factor_dimensions']==[14,40,6,14,6,40,6,8,6,6,40]
    assert sum(c['ordered_simple_factor_dimensions'])==186

def test_c8_phase_boundary():
    c=load('PART_W33_PASS4602_C8_SELECTOR_PHASE_BOUNDARY.json')
    a=c['exact_anchors']
    assert a['GQ(2,2)']['C8_alone_selects_apartments'] is False
    assert a['GQ(2,4)']['C8_alone_selects_apartments'] is True
    assert a['GQ(2,4)']['coefficient60_supports']==a['GQ(2,4)']['apartments']==1080
    assert a['GQ(3,3)']['C8_alone_selects_apartments'] is True

def test_fiber_scheme_and_quotient():
    c=load('PART_W33_PASS4603_APARTMENT_FIBER_FIVE_CLASS_SCHEME.json')
    assert c['association_scheme_verified'] is True
    assert c['valencies']==[1,24,12,32,64,2]
    assert c['imprimitive_relation']['components']==45
    assert c['quotient45']['first_pattern_graph_srg']==[45,32,22,24]

def test_all_degree_unary_nogo():
    c=load('PART_W33_PASS4604_NO_UNARY_EQUIVARIANT_MAP_ANY_DEGREE.json')
    assert c['block_size5_possible'] is False
    assert c['protected_V8_orbits']==[1,135,120]
    assert c['cubic_U6_orbits']==[1,27,36]
    assert c['singular135_stabilizer_suborbits']==[1,1,1,12,12,12,32,32,32]

def test_sp6_and_periodic_css():
    s=load('PART_W33_PASS4605_PAIRED_AXIS_SP6_QUADRATIC_REFINEMENTS.json')
    assert s['uncolored_graph']['srg']==[63,32,16,16]
    assert s['quadratic_coloring']['index_in_Sp6']==28
    assert s['quadratic_refinements']['minus_type']==28 and s['quadratic_refinements']['plus_type']==36
    q=load('PART_W33_PASS4606_PAIRED_AXIS_PERIODIC_COMPLEX_QUANTUM_HAMMING.json')
    assert (q['periodic_complex']['H36_dimension'],q['periodic_complex']['H27_dimension'])==(24,15)
    assert q['axis_CSS']=={'C27':'[[27,15,3]]','C36':'[[36,24,3]]'}
    assert q['fused_CSS']['quantum_parameters']=='[[63,51,3]]'

def test_unique_mog_sextet():
    c=load('PART_W33_PASS4615_HEXACODE_SECTION_RECONSTRUCTS_MOG_SEXTET.json')
    assert c['sextet_completion']['matchings_tested']==720
    assert c['sextet_completion']['valid_matchings']==1
    assert c['sextet_completion']['all_pairwise_unions_are_Golay_octads'] is True
    assert len(c['sextet_completion']['six_tetrads'])==6
