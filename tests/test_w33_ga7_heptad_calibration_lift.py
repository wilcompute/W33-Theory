from analysis.w33_ga7_heptad_calibration_lift import main


def test_ga7_heptad_calibration_lift_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 29


def test_ga7_heptad_calibration_lift_counts():
    r = main()
    assert r['counts']['toroidal_realizations'] == 7
    assert r['counts']['heptad_primary_overlays'] == 210
    assert r['counts']['heptad_signed_forms'] == 26880
    assert r['counts']['heptad_octonions'] == 3360
    assert r['counts']['heptad_pseudo'] == 23520


def test_ga7_heptad_calibration_lift_ratios():
    r = main()
    assert r['ratios']['heptad_signed_over_psl27'] == 160
    assert r['ratios']['heptad_oct_over_psl27'] == 20
    assert r['ratios']['heptad_pseudo_over_psl27'] == 140
    assert r['ratios']['heptad_signed_over_primary_overlays'] == 128
    assert r['ratios']['heptad_oct_over_primary_overlays'] == 16
    assert r['ratios']['heptad_pseudo_over_primary_overlays'] == 112
