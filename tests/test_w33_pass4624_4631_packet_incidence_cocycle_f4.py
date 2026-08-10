from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/'data'/name).read_text())

def test_pass4624_packet_is_support_e6_45():
    d=load('PART_W33_PASS4624_PACKET45_SUPPORT_E6_INTERTWINER.json')
    assert d['pass']==4624 and d['source']['packet_count']==45
    assert d['representative']['complement_is_Pass4585_support']
    assert d['equivariance']['all_45_supports_hit']
    assert d['equivariance']['support_stabilizer_order']==576

def test_pass4625_intrinsic_three_carrier_and_snf():
    d=load('PART_W33_PASS4625_INTRINSIC_45X40_THREE_CARRIER.json')
    assert d['matrix']['smith_normal_form']=={'1':15,'2':10,'0':15}
    assert d['matrix']['rank_Q']==25 and d['matrix']['rank_F2']==15
    assert d['line_carrier']['minimum_words_are_exactly_W33_lines']
    assert d['binary_complex']['middle_homology_dimension']==10

def test_pass4626_outer_descent_cocycle():
    d=load('PART_W33_PASS4626_OUTER_U6_DESCENT_COCYCLE.json')
    assert d['PSp_splitting']['Hom_PSp_W_to_U_dimension']==1
    assert d['outer']['action_on_three_six_spaces']==[0,2,1]
    assert d['outer']['off_diagonal_B_rank']==6
    assert d['cocycle']['restriction_to_PSp']=='zero'

def test_pass4627_stays_open_until_two_saturation_proved():
    d=load('PART_W33_PASS4627_HERMITIAN_RANK_TWO_SATURATION_FRONTIER.json')
    assert d['rational_theorem']['rank_Q']=='q^4+q^2+1'
    assert d['status'].startswith('OPEN:')
    assert '2-saturated' in d['binary_equivalences_for_odd_q'][-1]

def test_pass4628_f4_choice_is_point_carrier():
    d=load('PART_W33_PASS4628_F4_CHOICE_IS_W33_POINT_CARRIER.json')
    assert d['compatible_F4_structures']['oriented_J']==80
    assert d['compatible_F4_structures']['unoriented_pairs']==40
    assert d['compatible_F4_structures']['centralizer_order']==648
    assert d['compatible_F4_structures']['normalizer_order']==1296
    assert d['W33_intertwiner']['carrier']=='point-side W33'
    assert len(d['W33_intertwiner']['normalizer_fixed_points'])==1
    assert d['W33_intertwiner']['normalizer_fixed_lines']==[]

def test_pass4629_full_outer_s3_fiber():
    d=load('PART_W33_PASS4629_FULL_OUTER_PACKET_S3_FIBER.json')
    assert d['PSp']['quotient']=='C3=A3'
    assert d['PGSp']['quotient']=='S3'
    assert d['PGSp']['support_stabilizer_order']==1152
    assert d['PGSp']['kernel_H_order']==192

def test_pass4630_bockstein_h10_css():
    d=load('PART_W33_PASS4630_T_BOCKSTEIN_H10_CSS.json')
    assert d['binary_complex']['middle_homology_dimension']==10
    assert d['integer_lift']['coker_2_primary_torsion']=='(Z/2)^10'
    assert d['bockstein']['isomorphism']
    assert d['CSS']['parameters']=='[[40,10,4]]'

def test_pass4631_f4_moduli_incidence():
    d=load('PART_W33_PASS4631_F4_MODULI_E6_INCIDENCE.json')
    assert d['moduli_points']['count']==40
    assert d['E6_rows']['count']==45
    assert d['minimal_even_tetrads']['count']==40
    assert d['minimal_even_tetrads']['identification']=='exactly the W33 lines'

def test_integration_surfaces():
    needle='\\input{analysis/PASS4624_4631_packet_incidence_cocycle_f4_insert}%'
    for name in ('w33_paper.tex','photonic_holonet.tex','holonet_machine_blueprint.tex'):
        assert needle in (ROOT/name).read_text()
    reg=json.loads((ROOT/'data/w33_public_frontier_extension_pass4461_4464.json').read_text())
    assert any(x['token']=='pass4624-4631-packet-incidence-f4-h10' for x in reg['public_sections'])
    assert any(x['token']=='pass4624-4631-packet-incidence-f4-h10-page' for x in reg['standalone_public_pages'])
