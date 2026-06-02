from analysis.w33_clifford_octonion_g2_projection import main


def test_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 30


def test_core_ranks():
    r = main()
    assert r['ranks']['clifford_generators'] == 7
    assert r['ranks']['bivectors_so7'] == 21
    assert r['ranks']['g2_rank'] == 14
    assert r['ranks']['kernel_rank'] == 7
    assert r['ranks']['bracket_closure_rank'] == 14


def test_associator_counts():
    r = main()
    assert r['associator_geometry']['associative_count'] == 7
    assert r['associator_geometry']['nonassociative_count'] == 28
    assert r['associator_geometry']['total_imaginary_triples'] == 35
