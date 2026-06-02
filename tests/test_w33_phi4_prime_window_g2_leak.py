from analysis.w33_phi4_prime_window_g2_leak import main


def test_phi4_prime_window_g2_leak_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 15


def test_phi4_prime_window_g2_leak_counts():
    r = main()
    assert r['counts']['window'] == 100
    assert r['counts']['all_primes_to_window'] == 25
    assert r['counts']['substrate_primes_in_window'] == 19
    assert r['counts']['leak_primes_in_window'] == 6
    assert r['counts']['substrate_primes_total'] == 21
    assert r['counts']['substrate_plus_first_leak'] == 27


def test_phi4_prime_window_g2_leak_sets():
    r = main()
    assert r['sets']['leak_primes_in_window'] == [53, 61, 73, 79, 83, 97]
    assert r['sets']['substrate_primes_outside_window'] == [127, 163]
