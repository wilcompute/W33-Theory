from analysis.w33_frame_action_g2_weyl_quotient import main


def test_frame_action_g2_weyl_quotient_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 24


def test_frame_action_g2_weyl_quotient_groups():
    r = main()
    assert r['groups']['Aut_K44_order'] == 1152
    assert r['groups']['frame_action_order'] == 72
    assert r['groups']['kernel_order'] == 16
    assert r['groups']['kernel_structure'] == 'elementary abelian 2^4'
    assert r['groups']['frame_vertex_stabilizer_order'] == 12
    assert r['groups']['Weyl_G2_order'] == 12


def test_frame_action_g2_weyl_quotient_root_graph():
    r = main()
    assert r['root_graph']['edges'] == 9
    assert r['root_graph']['degree'] == 3
    assert r['root_graph']['graph'] == 'K3,3'
    assert r['root_graph']['reading'] == '3 short positive roots + 3 long positive roots'
    assert set(r['decompositions_of_1152'].values()) == {1152}
