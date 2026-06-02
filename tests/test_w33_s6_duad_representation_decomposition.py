from analysis.w33_s6_duad_representation_decomposition import main


def test_s6_duad_representation_decomposition_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 21


def test_s6_duad_representation_decomposition_projectors():
    r = main()
    assert r['S6_split'] == '15 = 1 + 5 + 9'
    assert r['projectors']['ranks'] == [1, 5, 9]
    assert r['mode_ranks_after_D'] == {'P1_uniform': 1, 'P5_gauge': 0, 'P9_observable': 9}


def test_s6_duad_representation_decomposition_branching():
    r = main()
    assert '4+5' in r['link_to_S5_quotient']
    assert '9P1 + 4P9' in r['incidence_formula']
