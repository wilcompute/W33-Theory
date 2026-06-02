from analysis.w33_ga7_calibration_class_counts import main


def test_ga7_calibration_class_counts_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 19


def test_ga7_calibration_distribution():
    r = main()
    assert r['counts'] == {'primaries': 30, 'signings_per_primary': 128, 'total': 3840}
    assert r['class_distribution'] == {'4': 192, '8': 192, '10': 512, '12': 928, '14': 1408, '16': 128, '28': 480}


def test_ga7_calibration_weighted_laws():
    r = main()
    assert r['weighted_laws']['all'] == 53760
    assert r['weighted_laws']['pseudo'] == 40320
    assert r['weighted_laws']['all_average'] == 14
    assert r['weighted_laws']['pseudo_average'] == 12
