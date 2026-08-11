import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load(p): return json.loads((ROOT/p).read_text())

def test_pass4849_4856_cross_certificates():
    e=load('data/PART_W33_PASS4849_4852_4854_4855_4856_E6_KERNEL_CODE.json')
    a=load('data/PART_W33_PASS4850_LEVI_MINIMUM_ORBITAL_WEDDERBURN.json')
    c=load('data/PART_W33_PASS4851_CODE399_FULL_AUTOMORPHISM.json')
    t=load('data/PART_W33_PASS4853_TERNARY_INCIDENCE_GOLAY_TWISTED_LIFT.json')
    old=load('data/PART_W33_PASS4842_4846_4847_4848_INCIDENCE_CODES.json')
    d6=load('data/PART_W33_PASS4659_INTERNAL_E6_27_36_45_TRIANGLE.json')
    aut=load('manuscripts/parts/PART_MCCCXCV_SPREAD_DOUBLE_SIX_AUTOMORPHISM_ORDER_results.json')

    assert old['F2_right_kernel']['parameters']=='[360,36,20]_2'
    assert e['kernel_code']['parameters']=='[360,36,20]_2'
    assert e['kernel_code']['minimum_shell_size']==36
    assert e['kernel_code']['minimum_shell_span_dimension']==35
    assert e['kernel_code']['dual']['parameters']=='[360,324,3]_2'
    assert e['kernel_code']['dual']['weight3_words']==1080
    assert e['extra_kernel_coset']['minimum_coset_weight']==120
    assert e['extra_kernel_coset']['complete_minimum_shell_size']==25920
    assert e['characteristic_two_extension']['splits_over_PSp'] is False
    assert e['characteristic_two_extension']['splits_over_PGSp'] is False
    assert e['minimum_carriers']['classical_identity'].startswith('the 36 cubic-surface double-sixes')
    assert d6['internal_carriers']['double_sixes36']==36
    assert aut['orbit_stabilizer']['automorphism_order']==e['kernel_code']['automorphism_group_order']==51840

    assert a['PSp']['orbital_dimension']==59 and a['PSp']['center_dimension']==15
    assert a['PGSp']['orbital_dimension']==49 and a['PGSp']['center_dimension']==13
    assert a['PSp']['rational_center']=='Q^9 x Q(sqrt(-3))^3'
    assert a['PGSp']['rational_center']=='Q^13'
    assert a['coarse_operator_embedding']['is_central'] is False

    assert c['sheet_kernel_is_genuine_full_code_symmetry'] is True
    assert c['class_quotient']['Aut_GQ_order']==51840
    assert 'S3^45' in c['full_coordinate_automorphism_group']

    assert t['projective_Levi_8_cycle_family']['span_dimension_F3']==64
    assert t['projective_K33_weight6_family']['span_dimension_F3']==54
    assert t['projective_K33_weight6_family']['codimension_in_Levi_H1']==10
    assert t['unweighted_cycle_K33_incidence']['rank_F3']==359
    assert t['unweighted_cycle_K33_incidence']['linear_factorization_to_K33_homology_after_any_projective_sign_choice'] is False
    assert t['twisted_lift']['rank']==54 and t['twisted_lift']['PGSp_equivariant'] is True
