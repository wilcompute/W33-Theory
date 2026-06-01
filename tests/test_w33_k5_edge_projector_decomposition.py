from analysis.w33_k5_edge_projector_decomposition import main


def test_k5_edge_projector_decomposition_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 17


def test_k5_edge_projector_decomposition_projectors():
    r = main()
    assert r['projectors']['traces'] == [1, 4, 5]
    assert r['projectors']['ranks'] == [1, 4, 5]
    assert r['symmetry']['S5_order'] == 120


def test_k5_edge_projector_decomposition_carrier():
    r = main()
    assert r['carrier'] == 'ten K5 quotient edges from the doily/K6 gauge quotient'
    assert '1+4+5' in r['interpretation']
