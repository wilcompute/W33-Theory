from analysis.w33_petersen_k6_pg32_operation_weld import main


def test_petersen_k6_pg32_operation_weld_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 15


def test_petersen_k6_pg32_operation_weld_counts():
    r = main()
    assert r['counts']['petersen_edges'] == 15
    assert r['counts']['petersen_perfect_matchings'] == 6
    assert r['counts']['k6_edges'] == 15
    assert r['counts']['k6_triangles'] == 20
    assert r['counts']['k6_onefactors'] == 15
    assert r['counts']['sts_blocks'] == 35
    assert r['counts']['pg32_lines'] == 35


def test_petersen_k6_pg32_operation_weld_reading():
    r = main()
    assert 'operation-preserving' in r['reading']
    assert 'zero XOR sum' in r['reading']
