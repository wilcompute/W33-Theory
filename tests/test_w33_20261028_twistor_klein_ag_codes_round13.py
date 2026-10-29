"""Independent exact Klein/twistor/AG/CSS tests."""
from w33_20261028_twistor_klein_ag_codes_round13 import certificate


def test_klein_plucker_incidence():
    c=certificate();q=c['quadric']
    assert (q['klein_quadric_points'],q['complement_points'])==(35,28)
    assert (q['finite_twistor_points'],q['finite_twistor_lines'])==(15,35)
    assert q['point_line_incidence_count']==105
    assert (q['intersecting_line_pairs'],q['disjoint_line_pairs'])==(315,280)


def test_conwell_eight_heptads_and_equivariant_A8():
    c=certificate()['conwell']
    assert c['heptads']==8 and c['heptad_size']==7
    assert c['exterior_projective_lines']==56
    assert len(c['point_to_heptad_pair'])==28
    a=c['canonical_GL4_F2_to_A8']
    assert a['heptad_action_order']==20160
    assert a['stabilizer_of_two_heptad_labels']==720
    assert a['orbit_of_28_pairs']==28
    assert a['point_to_heptad_pair_equivariance_verified']


def test_first_order_AG_weights_and_dual_puncturing():
    c=certificate()['codes']
    assert c['Klein']['1']['weight_enumerator']=={'0':1,'16':35,'20':28}
    assert c['off_quadric']['1']['weight_enumerator']=={'0':1,'12':28,'16':35}
    assert c['Klein']['1']['distance']==16
    assert c['off_quadric']['1']['distance']==12


def test_degree_two_exhaustive_2_to_the_20_and_21():
    c=certificate()['codes']
    assert (c['Klein']['2']['dimension'],c['Klein']['2']['distance'])==(20,6)
    assert (c['off_quadric']['2']['dimension'],c['off_quadric']['2']['distance'])==(21,4)
    assert c['Klein']['2']['weight_enumerator']['6']==280
    assert c['off_quadric']['2']['weight_enumerator']['4']==315


def test_degree_three_four_evaluation_hierarchy():
    c=certificate()['codes']
    assert [c['Klein'][str(i)]['dimension'] for i in (1,2,3,4)]==[6,20,34,35]
    assert [c['off_quadric'][str(i)]['dimension'] for i in (1,2,3,4)]==[6,21,27,28]


def test_nested_classical_AG_gives_commuting_CSS_codes():
    c=certificate()['codes']
    a=c['Klein']['CSS_from_nested_degree_1_and_2']
    b=c['off_quadric']['CSS_from_nested_degree_1_and_2']
    assert (a['length'],a['logical_qubits'],a['distance'])==(35,14,3)
    assert (b['length'],b['logical_qubits'],b['distance'])==(28,15,3)
    assert a['commutation_exact'] and b['commutation_exact']
    assert a['dual_degree2_distance']==7
    assert b['dual_degree2_distance']==12
    assert a['weight3_incidence_logical_witnesses']==105
    assert b['weight3_incidence_logical_witnesses']==56


def test_not_confusing_Klein_quartic_or_Hamming():
    c=certificate()['limits']
    assert c['no_AG_curve_Goppa_code_claim']
    assert c['no_SU22_real_structure_over_F2']
    assert 'simplex' in c['repo_historical_correction']


def test_native_four_term_shortcut_and_symmetry_selection_limits():
    c=certificate()['other_five_frontiers']
    assert c['smaller_than_six_gauge_repair']['four_term_common_e0_e1_activation_disproved']
    assert c['smaller_than_six_gauge_repair']['global_exceptional_polynomial_Q_zero']
    assert not c['smaller_than_six_gauge_repair']['stronger_2_to_5_term_general_no_go_proved']
    assert c['matter_selector']['GL4_F2_orbit_of_28_nondegenerate_forms']==28
    assert c['native_reflection']['finite_F2_fixes_4_off_quadric_points']
    assert not c['native_reflection']['Lorentzian_time_or_photon_helicities_derived']
