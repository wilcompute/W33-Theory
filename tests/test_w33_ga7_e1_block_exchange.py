from analysis.w33_ga7_e1_block_exchange import main


def test_ga7_e1_block_exchange_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 25


def test_ga7_e1_block_exchange_counts():
    r = main()
    assert r['counts']['E1_blocks'] == 10
    assert r['counts']['primaries_per_block'] == 21
    assert r['counts']['signed_forms_per_block'] == 2688
    assert r['counts']['octonions_per_block'] == 336
    assert r['counts']['pseudo_per_block'] == 2352
    assert r['counts']['x_supports_per_block'] == 16


def test_ga7_e1_block_exchange_block_vector():
    r = main()
    assert r['block_vector'] == {
        'octonion_psl_copies': 2,
        'pseudo_psl_copies': 14,
        'total_psl_copies': 16,
    }
