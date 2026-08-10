import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load(name):
    return json.loads((ROOT/'data'/name).read_text(encoding='utf-8'))

def test_4579_full_o8plus_lift_partition():
    c=load('PART_W33_PASS4579_W33_LIFT_O8PLUS255.json')
    assert c['protected_quotient']['nonzero_classes']==255
    assert c['lift_partition']['singular_from_apartments']==135
    assert c['lift_partition']['anisotropic_from_edges']==120
    assert c['projective_lines']=={'one_singular_two_anisotropic':3780,'three_anisotropic':5440,'three_singular':1575,'total':10795}

def test_4580_rank_law_remains_explicit_reduction():
    c=load('PART_W33_PASS4580_QMINUS_BINARY_RANK_REDUCTION.json')
    assert [a['q'] for a in c['exact_anchors']]==[3,5,7]
    assert all(a['dual_containing_verified_by_dimensions'] for a in c['exact_anchors'])
    assert 'remains open' in c['status']

def test_4581_three_by_four_fiber_symmetry():
    c=load('PART_W33_PASS4581_APARTMENT_FIBER_EQUIVARIANCE.json')
    assert c['fiber']['parts']==[4,4,4]
    assert c['fiber']['common_support_lines']==16
    assert c['singular_stabilizer']['order']==192
    assert c['singular_stabilizer']['part_action']=='S3'
    assert c['singular_stabilizer']['part_kernel']=='C2^4 (order 16)'

def test_4582_optimal_erasure_readouts():
    c=load('PART_W33_PASS4582_OPTIMAL_ERASURE_ROBUST_H10_READOUT.json')
    assert c['one_erasure']['exact_minimum_channels']==11
    assert c['one_erasure']['minimum_nonzero_functional_support']==2
    assert c['two_erasures']['exact_minimum_channels']==14
    assert c['two_erasures']['minimum_nonzero_functional_support']==3

def test_4583_alternating_square_exceptional_bridge():
    c=load('PART_W33_PASS4583_WEDGE2_EXCEPTIONAL_SIX_BRIDGE.json')
    assert c['alternating_square']['contraction_kernel_dimension']==27
    assert c['alternating_square']['core_dimension']==15
    assert c['alternating_square']['structure']=='U6 direct-sum U6'
    assert c['alternating_square']['six_submodules']==3
    assert c['U6_factor']['PSp_image_order']==25920
    assert c['U6_factor']['nonzero_orbits']==[27,36]
    assert c['bridge']['each_nonzero_U6_preimages']==240

def test_4584_cross_shell_code():
    c=load('PART_W33_PASS4584_CROSS_SHELL_INCIDENCE_CODE.json')
    assert c['incidence']['shape']==[135,120]
    assert c['binary']['rank']==9
    assert c['binary']['row_code']=='[120,9,56] self-orthogonal'
    assert c['binary']['RRt']=='zero' and c['binary']['RtR']=='all-ones J120'

def test_4585_support_line_quotient():
    c=load('PART_W33_PASS4585_FORTYFIVE_SINGULAR_SUPPORT_LINES.json')
    assert c['support_quotient']['singular_classes']==135
    assert c['support_quotient']['distinct_16_line_supports']==45
    assert c['support_quotient']['singular_classes_per_support']==3
    assert c['group']['support_stabilizer_order']==576
    assert c['group']['kernel_order']==192

def test_4586_nonselfdual_bridge():
    c=load('PART_W33_PASS4586_FORTYFIVE_BY_FORTY_POINT_DUALITY_BRIDGE.json')
    assert c['incidence']['shape']==[45,40]
    assert c['incidence']['binary_rank']==15
    assert c['row_gram']['graph']=='SRG(45,32,22,24)'
    assert c['column_gram']['exactly_point_graph'] is True
    assert c['column_gram']['different_from_protected_line_graph_Astar'] is True
    assert c['mod2']=={'RRt':'0','RtR':'J40'}

def test_public_and_manuscript_sources_exist():
    assert (ROOT/'analysis/PASS4579_4586_o8plus_rank_decoder_exceptional_insert.tex').is_file()
    assert (ROOT/'analysis/PASS4579_4586_o8plus_exceptional_bridge_index_insert.html').is_file()
    assert (ROOT/'docs/protected-o8plus-exceptional-bridge.html').is_file()
