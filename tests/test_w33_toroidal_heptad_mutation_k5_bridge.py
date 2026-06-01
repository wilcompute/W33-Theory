from analysis.w33_toroidal_heptad_mutation_k5_bridge import main


def test_toroidal_heptad_mutation_k5_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 13


def test_toroidal_heptad_mutation_k5_graph():
    r = main()
    assert r['mutation_graph']['vertices'] == 5
    assert r['mutation_graph']['nonself_edges'] == 10
    assert r['mutation_graph']['type'] == 'complete graph K5'


def test_toroidal_heptad_mutation_k5_weights():
    r = main()
    assert r['weights']['directed_offdiag'] == 504
    assert r['weights']['undirected_offdiag'] == 1008
    assert r['weights']['loop'] == 1008
    assert r['weights']['directed_total_per_orbit'] == 3024
    assert r['local_transition_profile_per_assignment'] == {'self': 6, 'to_each_other_orbit': 3, 'total_nontrivial_swaps': 18}
