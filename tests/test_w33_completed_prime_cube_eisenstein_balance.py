from analysis.w33_completed_prime_cube_eisenstein_balance import main


def test_completed_prime_cube_eisenstein_balance_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 22


def test_completed_prime_cube_eisenstein_balance_counts():
    r = main()
    assert r['counts']['completed_size'] == 27
    assert r['counts']['split_mod_3'] == 13
    assert r['counts']['inert_mod_3'] == 13
    assert r['counts']['ramified_mod_3'] == 1
    assert r['counts']['substrate_profile'] == {2: 11, 1: 9, 0: 1}
    assert r['counts']['first_leak_profile'] == {1: 4, 2: 2}
    assert r['counts']['transition_profile'] == {1: 5, 2: 5}


def test_completed_prime_cube_eisenstein_balance_sets():
    r = main()
    assert r['sets']['ramified_mod_3_primes'] == [3]
    assert r['sets']['first_leak_split_primes'] == [61, 73, 79, 97]
    assert r['sets']['first_leak_inert_primes'] == [53, 83]
