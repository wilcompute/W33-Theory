from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/'data'/name).read_text())

def test_pass4536_missing_bit_is_parity():
    c=load('PART_W33_PASS4536_MISSING_TENTH_PARITY_LINE_STAR.json')
    assert c['protected_dimension']==10 and c['edge_span_dimension']==9
    assert c['kernel_is_even'] is True
    assert c['minimal_missing_shell']=={'ambient_weight':12,'multiplicity':40,'objects':'the forty single-line stars A_* e_i'}
    assert c['protected_weight_enumerator_by_pi']['pi_0']=={'0':1,'16':135,'20':240,'24':135,'40':1}
    assert c['protected_weight_enumerator_by_pi']['pi_1']=={'12':40,'20':432,'28':40}

def test_pass4537_rank_frontier_stays_honest():
    c=load('PART_W33_PASS4537_Q5Q_BINARY_RANK_FRONTIER.json')
    assert [(r['q'],r['rank_N'],r['rank_NtN']) for r in c['exact_prime_field_anchors']]==[(3,91,70),(7,2451,2150)]
    assert 'remains unproved' in c['status']
    assert 'A^2=0' in c['general_odd_q_square_zero_theorem']['consequence']

def test_pass4538_global_large_order_bound():
    c=load('PART_W33_PASS4538_GLOBAL_LARGE_SPLITTING_CENSUS.json')
    assert c['large_class_orders']==[360,324,288,216,216,192,192]
    assert c['all_large_classes_nonsplit'] is True
    assert c['global_maximum_splitting_order']==162

def test_pass4539_exact_local_decoder():
    c=load('PART_W33_PASS4539_EXACT_LOCAL_H10_DECODER.json')
    assert c['sample_count']==10 and c['exhausted_protected_vectors']==1024
    assert c['sample_rows']==[0,1,2,3,4,5,7,8,10,11]
    assert c['decoder_total_xor_inputs']==45
    assert c['eight_state_boundary']['orbit_sizes']==[3,3,9,9,27,27,81,81]

def test_pass4540_cross_fusion():
    c=load('PART_W33_PASS4540_ZETA_PARITY_PRISM_CROSS_FUSION.json')
    assert c['w33_c6_degree2']['recovers_A_star_exactly'] is True
    assert c['dimensions']=={'H10':10,'V9_edge_span':9,'parity_quotient':1}
    assert '544320' in c['prism_exception']['Q53_t9']

def test_bonkers_4541_4543():
    c1=load('PART_W33_PASS4541_PARITY_FIXED_VECTOR_PAIRING.json')
    assert c1['edge_layer']=='V9=ker(pi)=1^perp'
    assert c1['fixed_vector_preimage_support']==[0,1,2,3]
    c2=load('PART_W33_PASS4542_ODD_SHELL_RECONSTRUCTS_W33.json')
    assert c2['pair_difference_histogram']=={'16':540,'20':240}
    assert 'SRG(40,12,2,4)' in c2['reconstructed_graph']
    c3=load('PART_W33_PASS4543_LOCAL_CELL_BASIS_MATROID.json')
    assert c3['full_local_H10_bases']==108
    assert c3['nine_neighbor_rank_by_omitted_triple']['triangle']=={'count':4,'count_formula':'4','rank':7}
    assert c3['nine_neighbor_rank_by_omitted_triple']['edge_plus_isolated']['rank']==8
    assert c3['nine_neighbor_rank_by_omitted_triple']['independent']=={'count':108,'count_formula':'C(4,3)*3^3','rank':9}
