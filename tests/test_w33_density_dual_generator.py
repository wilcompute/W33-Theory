from analysis.w33_density_dual_generator import main


def test_density_dual_generator_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 20


def test_density_dual_generator_core_identities():
    r = main()
    assert r['counts']['f'] == 24
    assert r['counts']['mu'] == 28
    assert r['counts']['PSL27'] == 168
    assert r['counts']['F4_horizon'] == 52
    assert r['counts']['Aut_K44'] == 1152


def test_density_dual_generator_strings():
    r = main()
    assert r['identities']['dual_PSL'] == '24*7 = 28*6 = 168'
    assert r['identities']['F4_horizon'] == '24+28 = 52'
    assert r['identities']['Euler_gap'] == '28-24 = 4'
