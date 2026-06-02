from analysis.w33_prime_cube_unit_convolution import main


def test_prime_cube_unit_convolution_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 23


def test_prime_cube_unit_convolution_completed():
    r = main()
    assert r['profiles']['completed_convolution'] == {1: 161, 5: 156, 7: 152, 11: 156}
    assert r['profiles']['completed_convolution'][1] == 160 + 1
    assert r['profiles']['completed_convolution'][7] == 152
    assert r['profiles']['completed_convolution'][5] == 12 * 13
    assert r['profiles']['completed_convolution'][11] == 12 * 13


def test_prime_cube_unit_convolution_leak():
    r = main()
    assert r['profiles']['first_leak_convolution'] == {1: 12, 5: 8, 7: 8, 11: 8}
    assert r['profiles']['transition_convolution'] == {1: 26, 5: 24, 7: 24, 11: 26}
