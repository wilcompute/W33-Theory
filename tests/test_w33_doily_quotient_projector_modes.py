from analysis.w33_doily_quotient_projector_modes import main


def test_doily_quotient_projector_modes_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 16


def test_doily_quotient_projector_modes_ranks():
    r = main()
    assert r['mode_ranks'] == {'P1_uniform': 1, 'P4_vertex': 4, 'P5_petersen': 5}
    assert r['total_quotient_spectrum'] == {'0': 5, '4': 5, '16': 4, '27/2': 1}


def test_doily_quotient_projector_modes_spectra():
    r = main()
    assert r['mode_spectra']['P1_uniform'] == {'0': 14, '27/2': 1}
    assert r['mode_spectra']['P4_vertex'] == {'0': 11, '16': 4}
    assert r['mode_spectra']['P5_petersen'] == {'0': 10, '4': 5}
