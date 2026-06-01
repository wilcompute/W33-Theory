from analysis.w33_symmetry_closure_gl42_a8_bridge import main


def test_symmetry_closure_gl42_a8_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 15


def test_symmetry_closure_gl42_a8_orders():
    r = main()
    assert r['orders']['S5_mutation_shell'] == 120
    assert r['orders']['GL(3,2)_Fano'] == 168
    assert r['orders']['product'] == 20160
    assert r['orders']['GL(4,2)'] == 20160
    assert r['orders']['A8'] == 20160
    assert r['orders']['AGL(3,2)_point_stabilizer'] == 1344


def test_symmetry_closure_gl42_a8_orbit_stabilizer():
    r = main()
    assert r['orbit_stabilizer']['nonzero_F2_4_points'] == 15
    assert r['orbit_stabilizer']['stabilizer'] == 1344
    assert r['orbit_stabilizer']['product'] == 20160
