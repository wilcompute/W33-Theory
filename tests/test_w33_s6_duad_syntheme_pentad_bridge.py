from analysis.w33_s6_duad_syntheme_pentad_bridge import main


def test_s6_duad_syntheme_pentad_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 20


def test_s6_duad_syntheme_pentad_counts():
    r = main()
    assert r['counts']['duads'] == 15
    assert r['counts']['synthemes'] == 15
    assert r['counts']['pentads'] == 6
    assert r['counts']['duad_syntheme_incidences'] == 45
    assert r['counts']['syntheme_pentad_incidences'] == 30


def test_s6_duad_syntheme_pentad_group_orders():
    r = main()
    assert r['groups']['S6'] == 720
    assert r['groups']['duad_stabilizer'] == 48
    assert r['groups']['syntheme_stabilizer'] == 48
    assert r['groups']['pentad_stabilizer'] == 120
