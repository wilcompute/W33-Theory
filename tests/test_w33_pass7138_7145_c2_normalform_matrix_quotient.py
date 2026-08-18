import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'data'/'PART_W33_PASS7138_7145_C2_NORMALFORM_MATRIX_QUOTIENT.json'


def load(): return json.loads(CERT.read_text())


def test_exact_normal_form_and_anchor_reduction():
    d=load(); assert d['status']=='PASS'
    a=d['pass_7138_eigenspace_transversal_normal_form']
    assert a['q9_witness_orbits']=='1 fixed + 25 two-cycles'
    assert a['fixed_point']==80 and a['distinct_selected_transversals']==25
    g=d['pass_7139_52set_gram_gauge_reduction']
    assert g['number_anchor_types']==8 and g['normalized_row_state_space']==512
    assert g['continuous_field_variables_per_anchor_case']==144
    assert g['known_51_anchor_type']==[1,3,5] and g['known_witness_remaining_clique']==47
    assert g['target']=='48-clique among 512 row states after fixing four anchors'


def test_allq_involution_and_quotient_scope():
    d=load(); t=d['pass_7140_allq_involution_theorem']; q=d['pass_7141_c2_quotient_graph']
    assert t['fixed_projective_points']=='2(q+1)'
    assert t['eligible_nonfixed_pair_orbits']=='q(q^2-1)/2'
    assert q['q9']=={'nodes':380,'edges':14500,'degree_fixed':46,'degree_pair':78}
    assert q['q7']=={'nodes':184,'edges':4180,'degree_fixed':29,'degree_pair':47}
    assert q['spectrum_formula_status'].startswith('CONJECTURE')
    assert set(q['anchors'])=={'3','5','7','9'}


def test_switching_idempotent_and_hexad():
    d=load(); s=d['pass_7142_quadratic_character_switching']; m=d['pass_7143_rankone_idempotent_bridge']
    assert s['q9']['extended_switching_group']=='C2' and s['q9']['rank_Q']==51
    assert s['q7']['extended_plusminus_switching_group']=='C2' and s['q7']['rank_Q']==32
    assert m['q9_all_idempotents']==90 and m['q9_selected_distinct_idempotents']==25
    h=d['pass_7144_semilinear_D12_hexad']; c=d['pass_7145_hexad_binary_code']
    assert h['group_order']==12 and h['product_AF_order']==6 and h['orbit_of_witness_size']==6
    assert h['all_15_pair_intersections']==4 and h['union_size']==248 and h['triple_points']==[50,80]
    assert c['length_after_puncturing_to_union']==248 and c['dimension']==6 and c['minimum_distance']==51
    assert c['generator_gram_mod2']=='I_6'


def test_boundary_does_not_claim_q9_optimality():
    d=load(); b=d['boundary'].lower()
    assert 'no q=9 optimality' in b
    assert 'physics' in b
