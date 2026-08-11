import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def J(name):return json.loads((ROOT/'data'/name).read_text())

def test_4817_finite_moduli_modules():
    x=J('PART_W33_PASS4817_PGSP_S3_MODULI_MODULE.json')
    assert x['sign_cohomology']['dimension']==64
    assert x['selected_sign_sector']['PGSp_fixed'] and x['selected_sign_sector']['PGSp_stabilizer_order']==51840
    assert x['twisted_deformation']['dimension']==225 and x['twisted_deformation']['selected_projective_line_PGSp_stable']

def test_4818_brauer_semisimplification_closes_dimension():
    x=J('PART_W33_PASS4818_MODULAR_H1_BRAUER_LOEWY.json')
    assert x['ordinary_character_dimension']==5671
    assert sum(y['degree']*y['composition_multiplicity'] for y in x['Brauer_composition_factors'])==5671
    t=x['module_level_trivial_layers'];assert (t['trivial_socle_dimension'],t['trivial_head_dimension'])==(4,1)
    assert t['all_four_fixed_vectors_in_augmentation'] and t['deck_line_nonsplit']

def test_4819_complete_outer_preimage_family():
    x=J('PART_W33_PASS4819_OUTER_CODE_ALGEBRA.json')
    assert x['even_module']['uniserial_chain_dimensions']==[0,6,20,26]
    assert x['even_module']['successive_irreducible_dimensions']==[6,14,6]
    fam=[y['physical_parameters'] for y in x['physical_preimage_families']]
    assert fam==['[2025,378,14]_2','[2025,379,14]_2','[2025,384,14]_2','[2025,385,14]_2','[2025,398,14]_2','[2025,399,14]_2','[2025,404,8]_2','[2025,405,7]_2']
    assert x['max_dimension_retaining_distance14']==399

def test_4820_all_six_outage_optima():
    x=J('PART_W33_PASS4820_EXACT_OUTAGE_MULTICOMMODITY.json')['cases']
    expected={'one_hot':'67/5952','two_hot_adjacent':'665/59746','two_hot_nonadjacent':'133/11946','one_vertex_fiber_removed':'189/16538','two_vertex_adjacent_removed':'1767/153094','two_vertex_nonadjacent_removed':'351/30670'}
    assert {k:v['exact_lambda'] for k,v in x.items()}==expected
    assert all(v['rational_primal_dual_certificate'] for v in x.values())

def test_4821_sparse_decoder_schedule():
    x=J('PART_W33_PASS4821_GLOBAL_ROUTER_DECODER_SCHEDULE.json')
    h=x['parity_check'];assert (h['rows'],h['rank'],h['local_rows'],h['global_rows'])==(1647,1647,1620,27)
    assert x['schedule']['depth']==2 and x['schedule']['optimal']
    d=x['bounded_distance_decoder'];assert d['guaranteed_arbitrary_error_radius']==6 and d['worst_case_raw_candidate_bound']==8**6

def test_4822_binary_levi_homology_subcode():
    x=J('PART_W33_PASS4822_LEVI_BINARY_ROUTER_HOMOLOGY.json')
    assert (x['Levi']['vertices'],x['Levi']['edges'],x['Levi']['H1_dimension_F2'],x['Levi']['girth'])==(72,135,64,8)
    assert x['Pass4772_parity_checks']['rank']==27 and not x['Pass4772_parity_checks']['is_cycle_or_homology_check_space']
    assert x['binary_homology_subcode']['parameters']=='[2025,64,96]_2'

def test_4823_selected_connection_line_signature():
    x=J('PART_W33_PASS4823_SELECTED_CONNECTION_INVARIANT_LINE.json')
    assert x['PSp_fixed_dimension_in_twisted_H1']>=1
    assert x['selected_outer_scalar'] in (1,2)

def test_4824_no_linear_transfer_to_levi_h1():
    x=J('PART_W33_PASS4824_FLAG_H1_LEVI_TRANSFER_OBSTRUCTION.json')
    assert x['Levi_H1']['dimension']==64
    assert (x['Levi_H1']['fixed_dimension'],x['Levi_H1']['coinvariant_dimension'])==(0,0)
    assert not x['Hom_obstruction']['nonzero_transfer_from_flag_trivial_socle_to_Levi_H1']
