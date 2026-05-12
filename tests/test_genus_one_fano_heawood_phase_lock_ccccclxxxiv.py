def test_genus_one_values():
    h = 1
    v = 4 + 3 * h
    e = 6 + 15 * h
    f = 4 + 10 * h
    assert (v, e, f) == (7, 21, 14)


def test_genus_one_fano_heawood_multiples():
    v, e, f = 7, 21, 14
    assert e == 3 * v
    assert f == 2 * v
    assert e == 21
    assert f == 14


def test_w33_hashimoto_split_in_genus_one_counts():
    e = 21
    f = 14
    assert e - 12 == 9
    assert f - 12 == 2
    assert 9 + 2 == 11


def test_phase_superperiod_28_56():
    local_phase_period = 12 // 3
    fano_colors = 7
    phase_superperiod = local_phase_period * fano_colors
    euler_drift = -2 * phase_superperiod
    assert local_phase_period == 4
    assert phase_superperiod == 28
    assert euler_drift == -56


def test_clifford_bivector_scale_hint():
    # dim so(8) = C(8,2) = 28.
    assert 8 * 7 // 2 == 28
    assert 2 * 28 == 56
