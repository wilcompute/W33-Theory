from analysis.w33_q4_rm13_bridge_min import main


def test_q4_rm13_bridge_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 13


def test_q4_rm13_bridge_core_counts():
    r = main()
    assert r['weight_enumerator'] == {0: 1, 4: 14, 8: 1}
    assert r['q4_quotient']['vertices'] == 16
    assert r['q4_quotient']['edges'] == 32
    assert r['q4_quotient']['axes'] == 8
    assert r['q4_quotient']['quotient_edges'] == 16
    assert r['q4_quotient']['is_K44'] is True


def test_q4_rm13_bridge_tomotope():
    r = main()
    assert (r['tomotope']['V'], r['tomotope']['E'], r['tomotope']['F'], r['tomotope']['C']) == (4, 12, 16, 8)
    assert r['tomotope']['sum'] == 40
