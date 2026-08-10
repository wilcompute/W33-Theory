from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def J(name):return json.loads((ROOT/'data'/name).read_text())

def test_4616_explicit_45_intertwiner():
    d=J('PART_W33_PASS4616_EXPLICIT_45_E6_INTERTWINER.json')
    assert d['pass']==4616 and d['equivariant_bijection_size']==45
    assert d['PSp_order']==25920 and d['common_stabilizer_order']==576
    assert d['old_points_fixed_by_new_stabilizer']==1 and d['generator_equivariance_verified']

def test_4617_sentinel_transport():
    d=J('PART_W33_PASS4617_SENTINEL_MINIMUM_SHELL_TRANSPORT.json')
    assert d['pass']==4617 and d['T_shape']==[45,40] and d['T_rank_F2']==15
    assert d['point_line_incidence_rank_F2']==25 and d['TN_zero']
    assert d['sentinel']['parameters']=='[40,15,8]' and d['sentinel']['minimum_words']==45
    assert d['sentinel']['T_rows_are_all_minimum_words']
    assert sum(d['sentinel']['weight_enumerator'].values())==2**15

def test_4618_outer_u6_multiplicity():
    d=J('PART_W33_PASS4618_OUTER_CANONICAL_U6_FACTOR.json')
    assert d['pass']==4618 and d['PSp']['six_submodules']==3
    assert d['PSp']['commutant_dimension_F2']==4 and d['PSp']['commutant_units']==6
    assert d['PGSp_outer']['cycle_type']=='1+2' and d['PGSp_outer']['canonical_outer_stable_factor']
    assert d['PGSp_outer']['fixed_factor_outer_image_order']==51840

def test_4619_concrete_d4_lifts():
    d=J('PART_W33_PASS4619_CONCRETE_D4_TRIALITY_W33_LIFTS.json')
    assert d['pass']==4619 and d['half_spinor_PSp_orbits']==[27,36,36,36,135]
    assert d['transitive_135_family']['fixed_maximal_size8_partial_spreads']==3
    assert d['transitive_135_family']['line_orbits']==[8,8,8,16]
    assert d['other_family']['orbit27']['fixed_center_quad_E6_quotient_lines']==1
    assert all(x['fixed_W33_spreads']==1 for x in d['other_family']['orbit36'])
    assert d['partial_spread_census']['unextendable_maximal']==135

def test_4620_hermitian_rank_boundary_stays_open():
    d=J('PART_W33_PASS4620_QMINUS_HERMITIAN_BINARY_RANK_REFORMULATION.json')
    assert d['pass']==4620 and d['status'].startswith('OPEN:')
    assert 'q^4+q^2+1' in d['candidate_dimension']
    assert [a['q'] for a in d['exact_anchors']]==[3,5,7]
    assert [a['candidate_rank_N'] for a in d['exact_anchors']]==[91,651,2451]

def test_4621_sentinel_self_reconstruction():
    d=J('PART_W33_PASS4621_SENTINEL_MINIMUM_SHELL_SELF_RECONSTRUCTION.json')
    assert d['pass']==4621 and d['minimum_shell']['minimum_words']==45
    assert d['row_reconstruction']['intersection_profile']=={'0':270,'2':720}
    assert d['coordinate_reconstruction']['cooccurrence_profile']=={'1':540,'3':240}
    assert d['coordinate_reconstruction']['different_from_line_side_Astar']

def test_4622_partial_spread_packets():
    d=J('PART_W33_PASS4622_PARTIAL_SPREAD_STABILIZER_PACKETS.json')
    c=d['counts'];assert d['pass']==4622
    assert (c['partial_spreads'],c['spreads_per_packet'],c['stabilizer_packets'])==(135,3,45)
    assert (c['H_order'],c['normalizer_order'],c['normalizer_quotient_order'])==(192,576,3)

def test_4623_outer_extension_nonsplit():
    d=J('PART_W33_PASS4623_OUTER_NONSPLIT_U6_EXTENSION.json')
    assert d['pass']==4623 and d['splits_over_PSp'] and not d['splits_over_PGSp']
    assert d['PGSp_invariant_six_submodules']==1
    assert not d['PGSp_equivariant_projection_onto_fixed_U6']

def test_release_surfaces_and_namespace_hygiene():
    assert (ROOT/'analysis/PASS4616_4623_e6_sentinel_triality_rank_insert.tex').exists()
    assert (ROOT/'analysis/PASS4616_4623_e6_sentinel_triality_rank_index_insert.html').exists()
    assert (ROOT/'docs/protected-e6-sentinel-triality.html').exists()
    note=(ROOT/'analysis/PASS4592_4599_NAMESPACE_COLLISION.md').read_text()
    assert 'paired-axis/Golay owns 4592--4615' in note
    assert 'protected E6/sentinel/triality continuation owns 4616--4623' in note
    assert not (ROOT/'analysis/PASS4607_4614_RESERVATION.md').exists()
    assert not (ROOT/'analysis/PASS4592_4599_RESERVATION.md').exists()
