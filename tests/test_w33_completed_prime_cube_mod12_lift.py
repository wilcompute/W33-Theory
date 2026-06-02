from analysis.w33_completed_prime_cube_mod12_lift import main


def test_completed_prime_cube_mod12_lift_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 27


def test_completed_prime_cube_mod12_lift_counts():
    r = main()
    assert r['counts']['completed_size'] == 27
    assert r['counts']['unit_residue_count'] == 25
    assert r['counts']['special_residue_count'] == 2
    assert r['counts']['mod12_profile'] == {7: 8, 5: 6, 11: 6, 1: 5, 2: 1, 3: 1}


def test_completed_prime_cube_mod12_lift_sets():
    r = main()
    assert r['sets']['special_primes_mod12'] == [2, 3]
    assert len(r['sets']['class_1_mod12']) == 5
    assert len(r['sets']['class_5_mod12']) == 6
    assert len(r['sets']['class_7_mod12']) == 8
    assert len(r['sets']['class_11_mod12']) == 6
