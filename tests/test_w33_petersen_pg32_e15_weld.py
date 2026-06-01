from analysis.w33_petersen_pg32_e15_weld import main


def test_petersen_pg32_e15_weld_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 17


def test_petersen_pg32_e15_weld_counts():
    r = main()
    assert r['counts']['petersen_disjoint_pair_states'] == 15
    assert r['counts']['pg32_points'] == 15
    assert r['counts']['pg32_lines'] == 35
    assert r['counts']['pg32_planes'] == 15
    assert r['counts']['E15_rank'] == 15
    assert r['counts']['packets_total'] == 2880


def test_petersen_pg32_e15_weld_incidence():
    r = main()
    assert r['pg32_incidence']['NNt'] == '4I+3J'
    assert r['pg32_incidence']['spectrum'] == {'49': 1, '4': 14}
    assert r['petersen_profiles'] == {'missing_k5_vertex_each': 3, 'k5_edge_use_each': 3}
