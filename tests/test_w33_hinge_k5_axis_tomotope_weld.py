from analysis.w33_hinge_k5_axis_tomotope_weld import main


def test_hinge_k5_axis_tomotope_weld_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 23


def test_hinge_k5_axis_tomotope_weld_q4_quotient():
    r = main()
    assert r['q4_quotient']['Q4_vertices'] == 16
    assert r['q4_quotient']['Q4_edges'] == 32
    assert r['q4_quotient']['antipodal_axes'] == 8
    assert r['q4_quotient']['quotient_edges'] == 16
    assert r['q4_quotient']['quotient_graph'] == 'K4,4'


def test_hinge_k5_axis_tomotope_weld_hinge_and_k5():
    r = main()
    assert r['hinge_split']['tomotope_f_vector'] == [4, 12, 16, 8]
    assert r['hinge_split']['sum'] == 40
    assert r['k5_axis_model']['K5_edges'] == 10
    assert r['k5_axis_model']['hinge_spokes'] == 4
    assert r['k5_axis_model']['adjacent_axis_pair_edges'] == 6
    assert r['axis_incidence']['rank'] == 7
