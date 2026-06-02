from analysis.w33_completed_prime_cube_dirichlet_energy import main


def test_completed_prime_cube_dirichlet_energy_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 24


def test_completed_prime_cube_dirichlet_energy_moments():
    r = main()
    assert r['moments']['completed_units'] == {'principal': 25, 'chi4': -3, 'chi3': 1, 'chi12': -3}
    assert r['moments']['substrate_units'] == {'principal': 19, 'chi4': -5, 'chi3': -1, 'chi12': -5}
    assert r['moments']['first_leak_units'] == {'principal': 6, 'chi4': 2, 'chi3': 2, 'chi12': 2}


def test_completed_prime_cube_dirichlet_energy_values():
    r = main()
    assert r['energies']['completed_nontrivial_character_energy'] == 19
    assert r['energies']['substrate_nontrivial_character_energy'] == 51
    assert r['energies']['first_leak_nontrivial_character_energy'] == 12
    assert r['energies']['transition_all_energy'] == 4
    assert r['energies']['transition_cross_term'] == -8
