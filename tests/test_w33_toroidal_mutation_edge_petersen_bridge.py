from analysis.w33_toroidal_mutation_edge_petersen_bridge import main


def test_toroidal_mutation_edge_petersen_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 16


def test_toroidal_mutation_edge_petersen_pair_split():
    r = main()
    assert r['pair_split']['incident_pairs_T5'] == 30
    assert r['pair_split']['disjoint_pairs_Petersen'] == 15
    assert r['pair_split']['total_pairs_on_10_edges'] == 45
    assert r['pair_split']['csaszar_edge_type_sum'] == 45


def test_toroidal_mutation_edge_petersen_srg_spectra():
    r = main()
    assert r['srg_parameters']['T5'] == [10, 6, 3, 4]
    assert r['srg_parameters']['Petersen'] == [10, 3, 0, 1]
    assert r['spectra']['T5'] == {'6': 1, '1': 4, '-2': 5}
    assert r['spectra']['Petersen'] == {'3': 1, '1': 5, '-2': 4}
