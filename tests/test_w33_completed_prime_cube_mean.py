from analysis.w33_completed_prime_cube_mean import main


def test_completed_prime_cube_mean_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 24


def test_completed_prime_cube_mean_counts():
    r = main()
    assert r['counts']['dense_shell_primes_to_47'] == 15
    assert r['counts']['transition_shell_primes_48_to_100'] == 10
    assert r['counts']['transition_substrate'] == 4
    assert r['counts']['transition_leak'] == 6
    assert r['counts']['outside_substrate'] == 2
    assert r['counts']['completed_cube_size'] == 27
    assert r['counts']['completed_cube_sum'] == 1350
    assert r['counts']['completed_cube_mean'] == 50


def test_completed_prime_cube_mean_sets():
    r = main()
    assert r['sets']['transition_leak'] == [53, 61, 73, 79, 83, 97]
    assert r['sets']['transition_substrate'] == [59, 67, 71, 89]
    assert r['sets']['outside_substrate'] == [127, 163]
