from analysis.w33_s6_outer_automorphism_class_swap import main


def test_s6_outer_automorphism_class_swap_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 15


def test_s6_outer_automorphism_class_swap_groups():
    r = main()
    assert r['groups']['domain_S6'] == 720
    assert r['groups']['image_on_pentads'] == 720
    assert r['groups']['pentad_stabilizer'] == 120


def test_s6_outer_automorphism_class_swap_key_swap():
    r = main()
    assert r['key_class_swaps']['transpositions_to_triple_transpositions'] == 15
    assert r['key_class_swaps']['triple_transpositions_to_transpositions'] == 15
    assert 'outer automorphism' in r['interpretation']
