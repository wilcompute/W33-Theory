import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load(name):return json.loads((ROOT/'data'/name).read_text())

def test_pass4992_octahedral_shell():
    x=load('PART_W33_PASS4992_OCTAHEDRAL_SHELL_RADIUS_CORRELATIONS.json')
    assert x['octahedra']==270
    assert x['global_incidence']['A3_even_unique']==1080
    assert x['octahedral_subshells']=={
        'all_words_distinct_within_each_reported_subshell':True,
        'weight12_full_octahedra':270,'weight6_from_even_face_pairs':1620,
        'weight8_from_equator_pairs':810,'weight9_from_even_face_triples':1080}
    assert x['delta173_consequence']['restricted_weight12_sum_U12_at_least']==-106
    assert x['covering_radius']['proved_interval']==[134,173]
    assert not x['covering_radius']['improved_here']

def test_pass4993_exact_erasure_distance():
    x=load('PART_W33_PASS4993_EXACT_85_READER_ERASURE_DISTANCE.json')
    assert x['exact_erasure_distance']==8
    assert x['guaranteed_erasure_tolerance']==7
    assert x['minimum_failure_witnesses']['distinct_support8_witnesses']==135

def test_pass4994_residual_c3():
    x=load('PART_W33_PASS4994_RESIDUAL_C3_AFFINE_GAUGE.json')
    assert x['PSp_point_line_stabilizer']=={'image_on_residual_triple':'C3=A3','image_order':3,'kernel_order':54,'order':162,'transitive':True}
    assert x['full_PGSp_point_line_stabilizer']['image_on_residual_triple']=='S3'
    assert x['full_PGSp_point_line_stabilizer']['kernel_order']==54

def test_pass4995_filtration():
    x=load('PART_W33_PASS4995_OCTAHEDRAL_EQUATOR_CHAIN_COMPLEX.json')
    assert x['invariant_filtration']=={'cycle_mod_triangle_dimension':1,'full_cycle_space':325,'square_span':294,'triangle_dual_span_Kperp':324,'triangle_mod_square_dimension':30}
    assert x['residual_square_complex']['H1']==31
    assert x['sigma_even_triangle_complex']['H1']==1

def test_pass4996_firewall_frozen_pass():
    x=load('PART_W33_PASS4996_STALE_CLAIM_FIREWALL.json')
    assert x['status']=='PASS' and x['violations']==[]
    assert all(all(v.values()) for v in x['authoritative_replacements'].values())

def test_pass4997_shared_line_projection():
    x=load('PART_W33_PASS4997_SHARED_LINE_HOLOGRAPHY.json')
    assert x['triangle_image']['distinct_images']==1080
    assert x['triangle_image']['common_center_census']=={'0':1080}
    assert x['residual_square_image']['distinct_images']==270
    assert x['residual_square_image']['multiplicity_per_image']==3
    assert x['Q43_binary_adjacency_code']['square_image_equals_orthogonal_complement']
    assert x['induced_quotient']['source_dimension']==30
    assert x['induced_quotient']['target_dimension']==10
    assert x['induced_quotient']['kernel_dimension']==20

def test_pass4998_support8_2k4():
    x=load('PART_W33_PASS4998_CANONICAL_SUPPORT8_COCIRCUITS.json')
    assert x['K4_subgraphs']==135
    assert x['canonical_minimum_family']['size']==135
    assert x['canonical_minimum_family']['support_size']==8
    assert x['exhaustion_inside_mean_zero_V20']['all_disjoint_nonadjacent_K4_pairs']==135
    assert x['exhaustion_inside_mean_zero_V20']['equal_to_star_difference_family']

def test_pass4999_octahedral_edge_frame():
    x=load('PART_W33_PASS4999_OCTAHEDRAL_EDGE_FRAME.json')
    assert x['shape']==[270,360] and x['row_weight']==12 and x['column_weight']==9
    assert x['real_rank']==120 and x['GF2_rank']==90
    assert x['squared_singular_spectrum']=={'0':150,'18':84,'36':15,'54':20,'108':1}
    assert x['pair_intersections']=={'share_0_edges':31995,'share_3_edges':4320}
