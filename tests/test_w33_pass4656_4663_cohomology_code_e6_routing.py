import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'
def load(name):return json.loads((DATA/name).read_text())

def test_4656_nonzero_duo_cohomology():
    d=load('PART_W33_PASS4656_APARTMENT_C2_VOLTAGE_COHOMOLOGY.json')
    assert d['canonical_base']['vertices']==810 and d['canonical_base']['labelled_edges']==4050 and d['canonical_base']['betti_1']==3241
    assert d['lift']['vertices']==1620 and d['lift']['deck_group']=='C2'
    assert d['explicit_monodromy_witness']['length']==6 and d['explicit_monodromy_witness']['voltage_evaluation']==1
    assert d['cohomology']['deck_class_nonzero'] is True

def test_4657_triality_intersection_structure():
    d=load('PART_W33_PASS4657_TRIALITY_INTERSECTION_GROUP.json')
    assert d['W33_point_stabilizer']['derived_series_orders']==[648,216,54,27,3,1]
    assert d['triality_pair_intersection']['structure']=='3^{1+2}:Q8'
    assert d['extraspecial_radical']['order']==27
    assert d['quotients']['intersection_mod_3radical']['element_order_census']=={'1':1,'2':1,'4':6}

def test_4658_code_dual_and_aut():
    d=load('PART_W33_PASS4658_SELECTED_CODE_DUAL_AUTOMORPHISM.json')
    assert d['dual']['parameters']=='[135,119,3]_2' and d['dual']['minimum_words']==270
    assert d['dual']['weight_enumerator']['3']==270 and d['dual']['weight_enumerator']['132']==45
    assert d['intrinsic_Jacobi_graph']['pair_class_sizes']==[270,360]
    assert d['automorphism_group']['order']==51840 and d['automorphism_group']['identification']=='Aut(C)=PGSp(4,3)'

def test_4659_internal_e6_triangle():
    d=load('PART_W33_PASS4659_INTERNAL_E6_27_36_45_TRIANGLE.json')
    assert d['internal_carriers']=={'lines27':27,'double_sixes36':36,'tritangents45':45}
    assert d['27x45']['tritangents_per_line']==5
    assert d['45x36']['triangle_double_six_line_intersection_census']=={'0':540,'2':1080}
    assert d['45x36']['identity']=='T^T R = 2 (J-D)'
    assert d['action_level_45_bridge']['fixed_protected_supports']==1

def test_4660_petersen_shortcut_router():
    d=load('PART_W33_PASS4660_TOPOLOGY_AWARE_HOLONET_OPTIMIZER.json')
    q=d['selected270_shortcut_layer']
    assert (q['high_load_edges'],q['low_load_edges'],q['high_load_components'])==(405,1620,27)
    assert q['component_graph']=='Petersen' and q['components_equal_internal_degree27_ten-line_carriers'] is True
    assert q['after_removing_high_orbit']=={'connected':True,'degree':12,'diameter':4,'edge_connectivity':12,'uniform_shell':'1,12,67,160,30'}

def test_4661_dual_120_scheme():
    d=load('PART_W33_PASS4661_ANISOTROPIC_120_SCHEME_DUALITY.json')
    assert d['anisotropic_planes']['PSp_orbits']==[40,1080]
    assert d['scheme']['valencies']==[1,2,36,27,54]
    assert d['scheme']['intersection_tensor_equals_Pass1355'] is True
    assert d['comparison_to_Pass1355']['PSp_equivariant_isomorphism'] is False

def test_4662_code_intrinsic_45():
    d=load('PART_W33_PASS4662_CODE_INTRINSIC_45_K4_TRIANGLE.json')
    c=d['code_intrinsic_chain']
    assert (c['minimum_words'],c['maximal_K4'],c['K4_anticompleteness_edges'])==(36,135,135)
    assert c['K4_anticompleteness_graph']=='45 C3' and c['union_supports']==45
    assert d['action_bridge']['stabilizer_order']==576 and d['action_bridge']['fixed_protected45_supports']==1

def test_4663_duo_spread_fail_closed():
    d=load('PART_W33_PASS4663_DUO_SPREAD_COUPLING_OBSTRUCTION.json')
    assert d['apartment_stabilizer']['spread_stabilizer_intersection_profile']=={'1':16,'4':16,'8':4}
    assert d['apartment_stabilizer']['fixed_spreads']==0
    assert d['transported_order8_relation']['quotient_incidence']=='135_4-36_15'
    assert d['comparison_to_code_spread_incidence']['rowwise_intersection']==0
    assert d['duo_sign_test']['result']=='FAIL_CLOSED'
