from analysis.w33_golden_d4_weyl_bridge import main


def test_golden_d4_weyl_bridge_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 25


def test_golden_d4_weyl_bridge_counts():
    r = main()
    assert r['counts']['ordered_failures'] == 864
    assert r['counts']['unique_failures'] == 108
    assert r['counts']['K2_2_edges'] == 4
    assert r['counts']['bridge_cube'] == 27
    assert r['counts']['D4_orientations'] == 8
    assert r['counts']['Q4_edges'] == 32
    assert r['counts']['Aut_K33'] == 72
    assert r['counts']['Weyl_G2'] == 12


def test_golden_d4_weyl_bridge_identities():
    r = main()
    assert '864 = 4*27*8' in r['identities']['golden_product']
    assert '864 = 27*32' in r['identities']['Q4_edge_lift']
    assert '864 = 72*12' in r['identities']['G2_Weyl_shell']
    assert '864 = 6*12^2' in r['identities']['root_sector_shell']
