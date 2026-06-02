from analysis.w33_k44_factorization_g2_root_selector import main


def test_k44_factorization_g2_root_selector_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 23


def test_k44_factorization_g2_root_selector_groups():
    r = main()
    assert r['groups']['Aut_K44_order'] == 1152
    assert r['groups']['affine_hinge_group_order'] == 192
    assert r['groups']['stabilizer_of_canonical_factorization'] == 192
    assert r['groups']['orbit_size'] == 6
    assert r['groups']['index'] == 6


def test_k44_factorization_g2_root_selector_factorization_orbit():
    r = main()
    assert r['factorization_orbit']['one_factorizations'] == 6
    assert r['factorization_orbit']['perfect_matchings_total'] == 24
    assert r['factorization_orbit']['oriented_root_sectors'] == 12
    assert set(r['decompositions_of_1152'].values()) == {1152}
