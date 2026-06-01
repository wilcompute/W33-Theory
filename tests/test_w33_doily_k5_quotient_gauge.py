from analysis.w33_doily_k5_quotient_gauge import main


def test_doily_k5_quotient_gauge_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 16


def test_doily_k5_quotient_gauge_ranks():
    r = main()
    assert r['objects']['K6_duads'] == 15
    assert r['objects']['vertex_gauge_dimension'] == 5
    assert r['objects']['K5_quotient_edges'] == 10
    assert r['ranks']['rank_D'] == 10
    assert r['ranks']['rank_vertex_gauge'] == 5
    assert r['ranks']['rank_F'] == 10
    assert r['ranks']['rank_rowspan_D_plus_F'] == 10


def test_doily_k5_quotient_gauge_symmetry():
    r = main()
    assert r['symmetry']['order'] == 120
    assert r['compression_identity'] == 'K6 duad space / vertex-potential gauge = 15 - 5 = 10 = K5 edge carrier'
