from analysis.w33_sp42_doily_s6_closure import main


def test_sp42_doily_s6_closure_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 18


def test_sp42_doily_s6_closure_orders():
    r = main()
    assert r['orders']['S6_duad_action'] == 720
    assert r['orders']['Sp(4,2)'] == 720
    assert r['orders']['GL(4,2)'] == 20160


def test_sp42_doily_s6_closure_line_split():
    r = main()
    assert r['line_split']['PG(3,2)_lines'] == 35
    assert r['line_split']['symplectic_doily_lines_onefactors'] == 15
    assert r['line_split']['nonisotropic_triangle_lines'] == 20
    assert r['doily']['points'] == 15
    assert r['doily']['lines'] == 15
    assert r['doily']['GQ_order'] == '(2,2)'
