from analysis.w33_s6_to_s5_branching_gauge import main


def test_s6_to_s5_branching_gauge_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 16


def test_s6_to_s5_branching_gauge_ranks():
    r = main()
    assert r['ranks']['F'] == 10
    assert r['ranks']['S6_P1_image'] == 1
    assert r['ranks']['S6_P5_image'] == 0
    assert r['ranks']['S6_P9_image'] == 9
    assert r['ranks']['Q4_block'] == 4
    assert r['ranks']['Q5_block'] == 5


def test_s6_to_s5_branching_gauge_spectra():
    r = main()
    assert r['spectra']['F_S6_P1_Ft'] == {'0': 9, '3/2': 1}
    assert r['spectra']['F_S6_P5_Ft'] == {'0': 10}
    assert r['spectra']['F_S6_P9_Ft'] == {'0': 1, '1': 5, '4': 4}
    assert r['spectra']['full_observable_quotient'] == {'1': 5, '3/2': 1, '4': 4}
