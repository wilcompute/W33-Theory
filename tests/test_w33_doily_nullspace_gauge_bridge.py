from analysis.w33_doily_nullspace_gauge_bridge import main


def test_doily_nullspace_gauge_bridge_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 19


def test_doily_nullspace_gauge_bridge_ranks():
    r = main()
    assert r['ranks']['rank_D'] == 10
    assert r['ranks']['right_nullity'] == 5
    assert r['ranks']['left_nullity'] == 5
    assert r['ranks']['row_space_mutation_edge_dimension'] == 10


def test_doily_nullspace_gauge_bridge_spectra():
    r = main()
    assert r['spectra']['D_Dt'] == '9^1 + 4^9 + 0^5'
    assert r['spectra']['Dt_D'] == '9^1 + 4^9 + 0^5'
