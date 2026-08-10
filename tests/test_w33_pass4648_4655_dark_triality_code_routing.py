import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

def load(name):
    return json.loads((DATA/name).read_text(encoding='utf-8'))


def test_4648_dark_sheet_module():
    d=load('PART_W33_PASS4648_DARK_SHEET_MODULE.json')
    assert d['stacked_coupling']=={'shape':[27,108],'rank_Q':21,'kernel_dimension':87}
    assert d['dark_sector']['dimension']==72
    assert d['dark_sector']['tensor_model']=='Std_2(S3_sheet) tensor Q[36_spreads]'
    assert d['full_kernel_PSp']['multiplicities']=={'1':2,'20':2,'15':3}
    assert d['sheet_S3_kernel_character']=={'identity':87,'transposition':15,'three_cycle':-21}


def test_4649_full_triality_and_w33_reconstruction():
    d=load('PART_W33_PASS4649_FULL_TRIALITY_GROUP_INTERSECTIONS.json')
    t=d['triality_closure']
    assert t['type_preserving_group']=='Omega_8^+(2)'
    assert t['two_conjugates_generate_type_preserving_order']==174182400
    assert t['PSp_plus_order3_triality_order']==522547200
    assert t['full_group_order']==1045094400
    assert t['diagram_quotient']=='S3'
    i=d['PSp_intersections']
    assert i['pairwise_order']==216 and i['triple_order']==6 and i['triple_isomorphism']=='S3'
    a=d['anisotropic_plane_reconstruction']
    assert a['plane_orbit_size']==40
    assert a['partition_of_120_nonsingular_vectors']=='40 x 3'
    assert a['total_orthogonality_graph']=='SRG(40,12,2,4)'


def test_4650_global_d12_factorization():
    d=load('PART_W33_PASS4650_GLOBAL_D12_COVER_FACTORIZATION.json')
    s=d['subgroup_chain']
    assert [s[k]['order'] for k in ('core_C','apartment_K','flag_N_equals_NH_K','selected_line_H')]==[8,16,32,96]
    g=d['global_factorization']
    assert (g['apartments'],g['flags'],g['selected_lines'])==(1620,810,270)
    assert g['stage1_deck_group']=='C2' and g['stage2_monodromy']=='S3' and g['composite_monodromy']=='D12'


def test_4651_binary_code_and_critical_groups():
    d=load('PART_W33_PASS4651_SELECTED_BINARY_CODE_CRITICAL_GROUPS.json')
    c=d['binary_left_kernel_code']
    assert c['parameters']=='[135,16,30]_2'
    assert c['minimum_words']==36
    assert c['minimum_word_stabilizer_order']==720
    assert c['fixed_W33_spreads_per_minimum_stabilizer']==1
    assert c['weight_enumerator']['30']==36
    assert sum(c['weight_enumerator'].values())==65536
    k=d['critical_groups']
    assert k['selected_point_graph']['order_factorization']=='2^150 * 3^166 * 5^23'
    assert k['selected_line_graph']['order_factorization']=='2^284 * 3^436 * 5^23'
    assert k['line_over_point_order_ratio']=='2^134 * 3^270'


def test_4652_weighted_routing_pareto():
    d=load('PART_W33_PASS4652_WEIGHTED_HOLONET_ROUTING_PARETO.json')
    s=d['symbolic']
    assert s['normalized_delivery_order_for_0_eta_1']=='W33 > selected135 > selected270 > Levi160'
    assert s['aggregate_selected270_order']=='selected270 > W33, selected135, and Levi160 for every 0<eta<=1'
    assert 0<s['selected135_vs_Levi160_aggregate_crossover_eta']<1
    assert d['literature_component_benchmarks']['warning'].startswith('These components were not demonstrated')


def test_4653_characteristic3_sheet_fourier():
    d=load('PART_W33_PASS4653_CHARACTERISTIC3_SHEET_FOURIER_OBSTRUCTION.json')
    c=d['characteristic_3']
    assert c['J_rank']==1 and c['J_square']=='0'
    assert c['containment']=='T subset W'
    assert c['diagonal_bright_vector_is_dark'] is True
    assert c['top_extension_split'] is False and c['lower_extension_split'] is False
    assert c['filtration'].endswith('trivial | sign | trivial')


def test_4654_point_not_line_intertwiner():
    d=load('PART_W33_PASS4654_TRIALITY_PLANE_W33_POINT_INTERTWINER.json')
    assert d['base_plane_setwise_stabilizer_order']==648
    assert d['base_plane_pointwise_stabilizer_order']==216
    assert len(d['fixed_W33_points'])==1 and d['fixed_W33_lines']==[]
    assert d['orbit_size']==40 and d['target_carrier']=='W33 point carrier'
    assert d['not_target_carrier']=='W33 line carrier'


def test_4655_internal_schlafli_reconstruction():
    d=load('PART_W33_PASS4655_INTERNAL_SCHLAEFLI_FROM_SELECTED_CODE.json')
    assert d['internal_intersection_rule']['intersection_census']=={'0':432,'6':540}
    assert d['internal_intersection_rule']['incidence']=='intersection size 0'
    r=d['reconstructed_matrix']
    assert (r['shape'],r['row_sum'],r['column_sum'],r['rank_Q'])==([27,36],16,12,21)
    assert r['RRt']=='10 I27 + 2 A27 + 6 J27'
    assert r['RtR']=='6 I36 - 2 A36 + 6 J36'
    assert d['reconstructed_graphs']['A27']=='SRG(27,10,1,5) meeting graph'
    assert d['reconstructed_graphs']['A36']=='SRG(36,15,6,6) double-six graph'
