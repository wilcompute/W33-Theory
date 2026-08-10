import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def J(name):return json.loads((ROOT/'data'/name).read_text())

def test_pass4745_h1_characteristic_two_boundary():
    x=J('PART_W33_PASS4745_INVARIANT_H1_CHARACTER.json')
    assert x['graph']['H1_dimension']==5671
    assert x['ordinary_PSp']['dimension_check']==5671
    assert x['ordinary_PSp']['trivial_multiplicity']==0
    assert x['characteristic_two_boundary']['H1_F2_has_PGSp_fixed_deck_line'] is True
    assert x['characteristic_two_boundary']['deck_line_has_PGSp_invariant_integral_or_rational_lift'] is False

def test_pass4746_full_symmetry_but_triangle_rule_nonunique():
    x=J('PART_W33_PASS4746_S3_CONNECTION_CLASSIFICATION.json')
    assert x['base']['automorphism_group_order']==x['base']['explicit_PGSp_image_order']==51840
    assert x['base_automorphisms']['all_lift'] is True
    p=x['connection']['minimal_two_cycle_S3_presentation']
    assert p['orders']==[2,2] and p['product_order']==3
    f=x['triangle_constraint_falsifier']
    assert f['single_cotree_edge_distinct_deformation_found'] is True
    assert f['first_single_witness']['edge']==[1,12]
    assert f['first_single_witness']['triangle_order_census_after_deformation']=={'2':270}

def test_pass4747_radical_is_multiplicity_two_20():
    x=J('PART_W33_PASS4747_ROUTER_SPECTRAL_REPRESENTATION.json')
    r=x['irrational_sector']
    assert r['PSp_irrep']=='20' and r['multiplicity_in_vertex_module']==2
    assert r['adjacency_multiplicity_space_trace']==2
    assert r['adjacency_multiplicity_space_determinant']==-12
    assert r['minimal_polynomial']=='x^2-2x-12'
    assert x['exact_characteristic_factorization'].endswith('(x^2-2x-12)^20')

def test_pass4748_crossfiber_code_frontier():
    x=J('PART_W33_PASS4748_CROSSFIBER_ROUTER_CODE.json')
    assert x['cell_decomposition']['cells']==135
    assert x['cell_decomposition']['partition_all_2025_edges'] is True
    P=[(r['local_dimension'],r['weighted_distance']) for r in x['S3_invariant_local_subspaces']['Pareto']]
    assert P==[(1,15),(2,10),(3,7),(4,3),(5,2),(6,1)]
    assert x['comparison']['crossfiber_choice']=='[2025,405,7]_2'
    assert x['comparison']['K_times_d']>x['comparison']['baseline_K_times_d']

def test_pass4749_exact_adversarial_envelope():
    x=J('PART_W33_PASS4749_ADVERSARIAL_ROUTER_CAPACITY.json')
    e=x['exact_symbolic_global_cut']
    assert (e['cold_graph_edge_connectivity'],e['hot_Petersen_edge_connectivity'],e['quotient_edge_connectivity'])==(12,3,10)
    assert e['exact_global_min_cut']=='min(12+3 rho,120)' and e['breakpoint_rho']==36
    assert x['equal_capacity']['global_min_cut']==15
    assert x['one_shortcut_fiber_outage']['exact_global_min_cut_all_positive_rho']==12

def test_pass4750_chain_complex_and_no_go():
    x=J('PART_W33_PASS4750_RESIDUE_CIRCUIT_CHAIN_COMPLEX.json')
    assert x['dependency_circuit_shell']['circuit_word_span_rank']==240
    assert x['dependency_circuit_shell']['linear_relations_among_540_circuit_words']==300
    c=x['cold_triangle_chain_complex']
    assert (c['rank_d2'],c['rank_d1'],c['H1_dimension'])==(540,269,811)
    assert x['descent_no_go']['linear_map_from_span_of_dependency_circuit_words_sending_each_word_to_its_triangle_boundary_exists'] is False

def test_pass4751_corrected_s3_fourier_block():
    x=J('PART_W33_PASS4751_S3_FOURIER_VOLTAGE.json')
    f=x['selected135_fourier']
    assert f['standard_block_polynomial']=='x(x^2-36)'
    assert f['standard_spectrum']=={'6':15,'0':60,'-6':15}
    assert f['source_target_orientation_checked'] is True
    assert x['regular_S3_closure']['matches_Pass4719'] is True
    assert x['selected270_radical_test']['factor_x2_minus_2x_minus_12_present_in_any_S3_fourier_block'] is False

def test_pass4752_deck_is_normalizer_homogeneous_cover():
    x=J('PART_W33_PASS4752_DECK_NORMALIZER_TWIST_COMPARISON.json')
    assert x['global_cochain_descent']['deck_voltage_descends_after_flag_gauge'] is True
    d=x['descended_double_cover']
    assert (d['vertices'],d['edges'],d['degree'],d['diameter'])==(540,4320,16,4)
    assert d['PSp_image_order']==25920 and d['PSp_vertex_orbit']==540 and d['point_stabilizer_order']==48
    assert x['local_stabilizer']['kernels_equal_as_subgroups'] is True
    assert x['comparison']['same_global_homogeneous_cover'] is True
