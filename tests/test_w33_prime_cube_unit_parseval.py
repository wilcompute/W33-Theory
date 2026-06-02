from analysis.w33_prime_cube_unit_parseval import main


def test_prime_cube_unit_parseval_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 21


def test_prime_cube_unit_parseval_energies():
    r = main()
    assert r['energies']['completed'] == 19
    assert r['energies']['substrate'] == 51
    assert r['energies']['first_leak'] == 12
    assert r['energies']['transition_substrate'] == 8
    assert r['energies']['transition_all'] == 4


def test_prime_cube_unit_parseval_profiles():
    r = main()
    assert r['profiles']['completed'] == {1: 5, 5: 6, 7: 8, 11: 6}
    assert r['unit_square_sums']['completed'] == 161
    assert r['moments']['completed'] == {'principal': 25, 'chi4': -3, 'chi3': 1, 'chi12': -3}
