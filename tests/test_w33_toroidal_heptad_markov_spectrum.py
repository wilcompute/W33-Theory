from analysis.w33_toroidal_heptad_markov_spectrum import main


def test_toroidal_heptad_markov_spectrum_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 15


def test_toroidal_heptad_markov_spectrum_values():
    r = main()
    assert r['transition_matrix'] == 'T = 504*(I_5 + J_5)'
    assert r['integer_spectrum'] == {'3024': 1, '504': 4}
    assert r['reduced_spectrum'] == {'18': 1, '3': 4}
    assert r['markov_spectrum'] == {'1': 1, '1/6': 4}
    assert r['spectral_gap'] == '5/6'


def test_toroidal_heptad_markov_minimal_polynomials():
    r = main()
    assert r['minimal_polynomials']['integer'] == '(x-3024)(x-504)'
    assert r['minimal_polynomials']['reduced'] == '(x-18)(x-3)'
    assert r['minimal_polynomials']['markov'] == '(x-1)(x-1/6)'
