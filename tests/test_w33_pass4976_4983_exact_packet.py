import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(n): return json.loads((ROOT/'data'/n).read_text())

def test_pass4976_shell_lock():
    x=load('PART_W33_PASS4976_SIGNED_SHELL_CORRELATIONS.json')
    assert x['H36_triangle_dual_shell']['weight3_span_rank']==324
    assert x['Pass4960_relaxation_witness']['realizable_character'] is False
    assert x['extremal_character_lock']['T3_minus_1080_forces']['4']==10530
    assert x['covering_radius']['proved_interval']==[134,173]

def test_pass4977_4978_outer_results():
    x=load('PART_W33_PASS4977_PGSP_OUTER_TWIST_DARK15.json')
    assert x['twist_result']['Hom_PSp_twisted_line15_to_point15_dimension']==0
    y=load('PART_W33_PASS4978_WITTING_QUADRATIC_OUTER_COMPENSATOR.json')
    assert y['compensated_module']['PGSp_even_dimension']==2
    assert y['compensated_module']['preferred_projective_channel_selected'] is False

def test_pass4979_40_plus_45_complete_reader():
    x=load('PART_W33_PASS4979_TRITANGENT_SPREAD_45_PORT_TRANSCEIVER.json')
    assert x['selector_incidence']['rank']==21
    assert x['complementary_40_plus_45_readout']['stacked_rank']==36
    assert x['complementary_40_plus_45_readout']['identity']=='18 I_36 = C C^T + M^T M - 22 J_36'

def test_pass4980_wreath_gauge():
    x=load('PART_W33_PASS4980_LOCAL_NINE_SPREAD_WREATH_GAUGE.json')
    assert x['induced_local_permutation_group_order']==1296
    assert x['kernel_on_nine_spreads_order']==1
    assert x['compiler_consequence']['raw_qutrit_coordinate_system_available_without_gauge_choice'] is False

def test_pass4981_bianchi_h2():
    x=load('PART_W33_PASS4981_Q43_TETRAHEDRAL_BIANCHI_H2.json')
    q=x['Q43_disjointness_clique_complex'];b=x['curvature_Bianchi']
    assert q['tetrahedra_K4']==9450
    assert q['rank_tetrahedron_to_triangle_boundary_F2']==2739
    assert q['H2_dimension_F2_after_filling_K4']==0
    assert b['nonabelian_S3_Bianchi_identity_verified_tetrahedra']==9450

def test_pass4982_affine_ambiguity():
    x=load('PART_W33_PASS4982_LOCAL_AG23_COMPLETION_OBSTRUCTION.json')
    assert x['AG23_completions']['count']==12
    assert x['AG23_completions']['completion_stabilizer_order']==108
    assert x['canonical_completion_exists'] is False

def test_pass4983_dual_spread_triangles():
    x=load('PART_W33_PASS4983_DUAL_TRIANGLES_AS_EMPTY_SPREAD_TRIPLES.json')
    assert x['spread_triple_intersection_census']=={'empty_common_W33_line':1080,'one_common_W33_line':120}
