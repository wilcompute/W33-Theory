from analysis.w33_ag32_rm13_automorphism_bridge import main


def test_ag32_rm13_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 11


def test_ag32_rm13_group_orders():
    r = main()
    assert r['groups']['GL(3,2)'] == 168
    assert r['groups']['AGL(3,2)'] == 1344
    assert r['groups']['full_SQS8_automorphism_group'] == 1344


def test_ag32_rm13_affine_plane_counts():
    r = main()
    assert r['objects']['points'] == 8
    assert r['objects']['affine_planes'] == 14
    assert r['objects']['parallel_classes'] == 7
    assert r['objects']['sqs_triples'] == 56


def test_ag32_rm13_identity_factorizations():
    r = main()
    assert r['identities']['AGL=8*168'] == 1344
    assert r['identities']['AGL=7*192'] == 1344
    assert r['identities']['AGL=14*96'] == 1344
