from analysis.w33_toroidal_heptad_fano_orbit_bridge import main


def test_toroidal_heptad_fano_orbit_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 10


def test_toroidal_heptad_fano_orbit_counts():
    r = main()
    assert r['repo_edge_type_counts'] == [10, 9, 9, 8, 9, 12, 11]
    assert r['csaszar_counts'] == [10, 9, 9, 8, 9]
    assert r['szilassi_counts'] == [12, 11]


def test_toroidal_heptad_fano_orbit_partition():
    r = main()
    assert r['group_order_GL32'] == 168
    assert r['unique_multiset_labelings'] == 840
    assert r['orbit_count'] == 5
    assert r['orbit_size_profile'] == {168: 5}
    assert len(r['line_sum_profiles']) == 5
