from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
def load(name):return json.loads((DATA/name).read_text())

def test_4960_degree7_moment_barrier():
    d=load('PART_W33_PASS4960_DEGREE7_MOMENT_RADIUS_BARRIER.json')
    assert d['covering_radius']=={'improved_here':False,'proved_interval_from_Pass4951':[134,173]}
    w=d['distance_173_relaxation_witness']
    assert w['delta']==173 and w['both_positive_definite']
    assert w['signed_shell_values']=={'3':-1080,'4':-1936,'5':75316,'6':830590,'7':-37193040}
    assert all(int(x)>0 for x in w['ordinary_moment_matrix_leading_minors'])
    assert all(int(x)>0 for x in w['one_sided_localizing_matrix_leading_minors'])

def test_4961_dark15_linear_hom_zero():
    d=load('PART_W33_PASS4961_DARK15_POINT_LINE_HOM_OBSTRUCTION.json')
    assert d['point_times_line_orbits']=={'count':2,'incident':160,'nonincident':1440}
    assert d['equivariant_matrix_space']['dimension']==2
    x=d['dark15_obstruction']
    assert x['Hom_PSp_V15line_to_V15point_dimension']==0
    assert x['Hom_PSp_V15point_to_V15line_dimension']==0
    assert x['signed_or_oriented_equivariant_incidence_can_evade'] is False

def test_4962_triangle_curvature_generates_s3():
    d=load('PART_W33_PASS4962_Q43_S3_CURVATURE_COHOMOLOGY.json')
    assert d['cell_counts']=={'edges':540,'triangles_as_2_cells':3240,'vertices':40}
    assert d['F2_cohomology']['graph_cycle_rank']==501
    assert d['F2_cohomology']['triangle_boundary_rank']==501
    assert d['F2_cohomology']['H1_dimension']==0
    assert d['sign_curvature']=={'flat_triangles':1080,'odd_reflection_triangles':2160}
    assert d['rooted_nonabelian_curvature']['all_three_transpositions_present']
    assert d['rooted_nonabelian_curvature']['generated_order']==6

def test_4963_corrected_witting_phase_law():
    d=load('PART_W33_PASS4963_WITTING_PANCHARATNAM_W33_REAUDIT.json')
    assert d['witting_carrier']['ambient']=='C^4 / CP^3'
    assert d['witting_carrier']['orthogonality_graph']=='isomorphic to standard W(3,3) point graph'
    assert not d['witting_carrier']['isomorphic_to_Q43_Steiner_line_graph']
    assert d['legacy_encoder_failure']=={'distinct_F3_tuples_from_40_rays':19,'projective_bijection':False,'zero_tuple_multiplicity':8}
    t=d['exact_pancharatnam_center_table']
    assert t['one_W33_common_center']=={'+pi/6':1440,'-pi/6':1440,'total':2880}
    assert t['four_W33_common_centers']=={'+pi/2':180,'-pi/2':180,'total':360}

def test_4964_unique_double_six_spread_bridge():
    d=load('PART_W33_PASS4964_DOUBLE_SIX_SPREAD_EQUIVARIANT_BRIDGE.json')
    assert d['group']['order']==51840
    assert d['carriers']=={'W33_spreads':36,'double_sixes':36,'point_stabilizer_order':1440}
    assert d['base_double_six_stabilizer_fixed_spreads']==1
    assert d['equivariant_bijection']=={'exists':True,'extends_across_outer_involution':True,'unique':True}
    assert d['pair_relation_transport']=={'double_six_intersection_4_to_spread_overlap_4':270,'double_six_intersection_6_to_spread_overlap_1':360}

def test_4965_local_nine_spread_chart():
    d=load('PART_W33_PASS4965_STEINER_LOCAL_NINE_SPREAD_CHART.json')
    assert (d['W33_lines'],d['spreads_through_each_line'])==(40,9)
    assert (d['Steiner_triangles'],d['Steiner_triangles_per_W33_line'])==(120,3)
    assert d['canonical_partition_per_line']=='9 spreads = 3 + 3 + 3'
    assert d['local_four_overlap_graph']=='K3,3,3'
    assert d['local_one_overlap_graph']=='3 disjoint K3'

def test_4966_witting_phase_outer_sign():
    d=load('PART_W33_PASS4966_WITTING_PHASE_OUTER_CHARACTER.json')
    assert d['PSp']=={'all_generators_preserve_oriented_phase':True,'generator_count':5,'order':25920}
    o=d['outer_similitude']
    assert o['matrix_mod3']=='diag(1,2,1,2)' and o['multiplier']==-1
    assert o['extended_group_order']==51840 and o['all_triples_phase_negated']
    assert d['oriented_nonorthogonal_triples']==3240

def test_4967_complete_point_double_six_readout():
    d=load('PART_W33_PASS4967_POINT_DOUBLE_SIX_COMPLETE_TRANSCEIVER.json')
    assert d['matrices']=={'C_double_six_by_line':[36,40],'Z_point_by_line':[40,40],'stacked':[76,40]}
    assert d['double_six_line_channel']['rank']==16
    assert d['point_line_channel']['rank']==25
    assert d['stacked_rank']==40
    assert d['exact_reconstruction_identity']=='18 I_40 = 3 Z^T Z + C^T C - 3 J_40'

def test_withdrawn_4882_cannot_regress():
    d=load('PART_W33_PASS4882_PANCHARATNAM_STEINER_COCYCLE.json')
    assert d['status']=='WITHDRAWN_SUPERSEDED_BY_PASS4963'
    legacy=(ROOT/'analysis/w33_pass4882_pancharatnam_steiner_f3_cocycle.py').read_text()
    assert 'WITHDRAWN_SUPERSEDED_BY_PASS4963' in legacy
    tool=(ROOT/'tools/pancharatnam_symplectic_invariants.py').read_text()
    assert 'w33_pass4963_witting_pancharatnam_w33_reaudit' in tool
    assert 'f3_point_from_ray' not in tool

def test_shared_manuscript_and_public_sources():
    manifest=(ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex').read_text()
    assert manifest.count('PASS4960_4967_moments_dark15_curvature_witting_spread_insert')==1
    insert=(ROOT/'analysis/PASS4960_4967_moments_dark15_curvature_witting_spread_insert.tex').read_text()
    assert 'WDDPassFourNineSixZeroPacketLoaded' in insert
    assert '18I_{40}=3Z^TZ+C^TC-3J_{40}' in insert
    for wrapper in ('w33_paper.tex','photonic_holonet.tex','holonet_machine_blueprint.tex'):
        assert 'W33_CURRENT_FRONTIER_MANIFEST' in (ROOT/wrapper).read_text()
    page=(ROOT/'docs/pass4960-4967-moments-witting-double-six.html').read_text()
    assert '36 double-sixes ↔ 36 spreads' in page and 'H¹(F₂)=0' in page
    card=(ROOT/'analysis/PASS4960_4967_index_insert.html').read_text()
    assert 'W33_PASS4960_4967_MOMENTS_WITTING_DOUBLE_SIX_CARD' in card
    materializer=(ROOT/'tools/integrate_pass4960_4967_public.py').read_text()
    assert "INDEXES=(ROOT/'docs/index.html',ROOT/'index.html')" in materializer
