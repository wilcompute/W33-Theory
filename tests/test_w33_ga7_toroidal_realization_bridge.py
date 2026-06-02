from analysis.w33_ga7_toroidal_realization_bridge import main


def test_ga7_toroidal_realization_bridge_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 20


def test_ga7_toroidal_realization_bridge_counts():
    r = main()
    assert r['counts']['realizations'] == 7
    assert r['counts']['csaszar'] == 5
    assert r['counts']['szilassi'] == 2
    assert r['counts']['edges_per_realization'] == 21
    assert r['counts']['fano_primaries'] == 30
    assert r['counts']['signed_landscape'] == 3840
    assert r['counts']['octonion_representations'] == 480


def test_ga7_toroidal_realization_bridge_buckets():
    r = main()
    assert sorted(len(v) for v in r['edge_completion_buckets'].values()) == [6, 6, 6, 6, 6]
    assert set(r['candidate_dictionary']['algebra_classes']) == {'O','P4','P8','P10','P12','P14','P16'}
