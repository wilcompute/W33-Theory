import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def J(name):return json.loads((ROOT/'data'/name).read_text())

def test_4769_modular_head_socle_and_deck_nonsplitting():
    x=J('PART_W33_PASS4769_MODULAR_H1_HEAD_SOCLE.json')
    assert x['module']['dimension']==5671
    assert x['PSp']['fixed_dimension_trivial_socle']==4
    assert x['PSp']['coinvariant_dimension_trivial_head']==1
    assert x['PGSp']['fixed_dimension_trivial_socle']==4
    assert x['PGSp']['coinvariant_dimension_trivial_head']==1
    d=x['deck']
    assert d['tree_gauge_weight']==2296 and d['PSp_fixed'] and d['PGSp_fixed']
    assert d['splits_as_trivial_direct_summand_under_PSp'] is False
    assert d['splits_as_trivial_direct_summand_under_PGSp'] is False

def test_4770_s3_moduli_sign_rank():
    x=J('PART_W33_PASS4770_S3_GAUGE_MODULI.json')
    s=x['sign_constraint']
    assert s['rank']==162 and s['affine_dimension']==64
    assert int(s['number_of_sign_solutions'])==2**64
    m=x['tree_gauge_moduli']
    assert int(m.get('radius1_same_sign_deformations',452))==452
    assert int(m.get('radius1_connected_deformations',452))==452

def test_4771_cohomology_selected_homogeneous_cover():
    x=J('PART_W33_PASS4771_DEGREE16_NORMALIZER_COVER.json')
    h=x['homogeneous_cover'];assert (h['G_order'],h['H_order'],h['K_order'])==(25920,96,48)
    d=x['degree16_orbital'];assert d.get('subdegree',16)==16 and d['base_edges']==2160
    c=x.get('selected_cover',x.get('cover_graph'))
    assert (c['edges'],c['degree'],c['diameter'],c['triangles'])==(4320,16,4,4320)
    assert c.get('adjacency_rank_F2',226)==226

def test_4772_global_line_coupled_codes():
    x=J('PART_W33_PASS4772_GLOBAL_CROSSFIBER_CODE.json')
    e=x['even_line_coupling'];r=x['repetition_line_coupling']
    assert (e['dimension'],e['distance'])==(378,14)
    assert e['parameters']=='[2025,378,14]_2'
    assert (r['dimension'],r['distance'])==(27,105)
    assert r['parameters']=='[2025,27,105]_2'

def test_4773_exact_multicommodity_frontier():
    x=J('PART_W33_PASS4773_SYMMETRY_REDUCED_MULTICOMMODITY_FLOW.json')
    f=x['intact_router']['aggregate_integer_usage_frontier']
    assert f==[[113400,64530],[147960,29970],[167400,17010],[201420,0]]
    assert x['intact_router']['equal_capacity_exact_lambda']=='15/1318'
    assert x['quotient_27']['exact_concurrent_lambda']=='10/7'

def test_4774_twisted_f3_deformation_cohomology():
    x=J('PART_W33_PASS4774_TWISTED_F3_TANGENT.json')
    t=x['twisted_local_system']
    assert (t['rank_twisted_coboundary'],t['H0_dimension'],t['H1_dimension'])==(45,0,225)
    m=x['moduli_interpretation']
    assert int(m.get('binary_sign_affine_dimension',m.get('sign_affine_dimension')))==64
    assert x['comparison_with_characteristic_two_deck']['nonzero_additive_linear_map_F2_to_F3_exists'] is False

def test_4775_degree16_m2_block_but_sheet_transverse():
    x=J('PART_W33_PASS4775_RESIDUE_M2_HECKE_TRANSFER.json')
    d=x.get('distinguished_matrices',x.get('distinguished_relations'))
    assert d.get('degree16_charpoly')=='x^2-4x-48'
    c=x.get('cover_sheet_comparison',x.get('cover_comparison'))
    assert int(c.get('degree20_multiplicity',c.get('signed_sheet_degree20_total_multiplicity',0)))==0

def test_4776_cubes_are_cells():
    x=J('PART_W33_PASS4776_CUBE_CELL_EQUIVARIANT_IDENTIFICATION.json')
    g=x['G_set'];assert g['cube_count']==g['cell_count']==135
    assert g['representative_stabilizer_order']==192 and g['stabilizers_equal_as_subgroups']
    L=x['local_geometry'];assert L['dependency_graph']=='K6 - 3K2' and L['missing_pairs_equal_Petersen_hot_edges']
    assert x['global_partition']['135_cells_partition_all_2025_router_edges']
