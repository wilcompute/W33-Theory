from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def J(name):return json.loads((ROOT/'data'/name).read_text(encoding='utf-8'))

def test_4785_even_cycle_code():
    d=J('PART_W33_PASS4785_THICKENING_EVEN_CYCLE_CODE.json')
    assert d['pass']==4785 and d['implementation_alias']==4761
    assert d['thickening_edge_incidence']=={'all_rows_eulerian':True,'all_rows_even_weight':True,'binary_rank':200,'column_weight':189,'columns':240,'row_weight':28,'rows':1620}
    assert d['code']['parameters']=='[240,200,4]_2'
    assert d['code']['dual_parameters']=='[240,40,12]_2'

def test_4786_literal_protected45():
    d=J('PART_W33_PASS4786_THICKENING_PARTNER_ROOK45.json')
    assert d['partner_involution']['pairs']==810 and d['partner_involution']['partner_overlap']==8
    assert d['rook_quotient']['distinct_16_line_unions']==45
    assert d['rook_quotient']['partner_pairs_per_union']==18
    assert d['protected45_comparison']['literal_set_equality'] is True

def test_4787_srg45_incidence():
    d=J('PART_W33_PASS4787_SUPPORT12_RECONSTRUCTS_SRG45.json')
    assert d['support12_quotient']['pair_intersections']=={'4':270,'7':720}
    assert d['transport_graph']['parameters']=='SRG(45,32,22,24)'
    T=d['grid_line_incidence']
    assert (T['rank_Q'],T['rank_F2'],T['rank_F2_A45'],T['rank_F2_A_dual'])==(25,24,14,10)

def test_4788_rectangle_partner():
    d=J('PART_W33_PASS4788_ROOK36_RECTANGLE_PARTNER_ACTION.json')
    assert d['local_grid']['support12_minima_inside']==36
    assert d['local_grid']['coordinate_model']=='C(4,2) x C(4,2)'
    assert d['rectangle_rule']['partner']=='simultaneous complement of both 2-subsets'
    g=d['group_action']
    assert (g['PGSp_grid_stabilizer'],g['PSp_grid_stabilizer'])==(1152,576)
    assert g['partner_in_PGSp_image'] is False and g['partner_centralizes_PGSp_image'] is True

def test_4789_coordinate_gset_no_go():
    d=J('PART_W33_PASS4789_DUAL_EDGE_CODE_CSS_CARRIER_SEPARATION.json')
    assert d['carriers']['point_graph_edges']==d['carriers']['dual_line_graph_edges']==240
    assert d['line_edge_stabilizer']['fixed_point_edges']==0
    assert d['outer_twist']['repairs_equivariant_bijection'] is False

def test_4790_grid_code_point_edge_shell():
    d=J('PART_W33_PASS4790_GRID_CODE_POINT_EDGE_BRIDGE.json')
    assert d['grid_code']['parameters']=='[40,24,6]_2'
    assert d['grid_code']['weight_enumerator']['6']==240
    assert d['point_edge_bridge']['equals_complete_grid_code_minimum_shell'] is True
    assert d['dual']['parameters']=='[40,16,10]_2'
    assert d['dual']['minimum_shell']=={'kernel_degree_0_2_words':216,'spreads':36,'total':252}

def test_4791_golay_relation_matroid():
    d=J('PART_W33_PASS4791_LEECH_NEIGHBOR_GOLAY_PARITY_MATROID.json')
    assert d['neighbors']['count']==24 and d['neighbors']['sextet_stabilizer_order']==138240
    p=d['parity_characters']
    assert p['relation_space']=='extended binary Golay G24'
    assert (p['span_dimension'],p['relation_space_dimension'])==(12,12)
    assert (p['minimum_relation_weight'],p['minimum_relations'])==(8,759)
    assert d['sextet_relations']['two_tetrad_unions']==15

def test_4792_characteristic_two_boundary():
    d=J('PART_W33_PASS4792_DECK_VS_EVEN_CYCLE_PARITY_BOUNDARY.json')
    assert d['support12_parity_class']['PSp_vertex_stabilizer']==648
    assert d['apartment_deck_class']['PSp_vertex_stabilizer']==96
    assert d['equivariant_base_map_test']['40_to_270'] is False
    assert d['equivariant_base_map_test']['270_to_40'] is False
    assert d['comparison']['same_cohomology_object'] is False
