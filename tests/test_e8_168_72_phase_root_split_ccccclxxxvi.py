def test_240_carrier_splits_into_168_and_72():
    w33_edges = 240
    fano_phase_curvature = 168
    e6_roots = 72
    assert fano_phase_curvature + e6_roots == w33_edges


def test_local_12_clock_sheet_counts():
    assert 168 // 12 == 14
    assert 72 // 12 == 6
    assert 240 // 12 == 20
    assert 14 + 6 == 20


def test_fano_automorphism_order():
    # |GL(3,2)|=(8-1)(8-2)(8-4)=168.
    assert (8 - 1) * (8 - 2) * (8 - 4) == 168


def test_e6_root_count_and_dimension():
    e6_roots = 72
    e6_rank = 6
    e6_dimension = 78
    assert e6_roots + e6_rank == e6_dimension


def test_phase_superperiod_numbers_align():
    full_period = 84
    euler_drift = -2 * full_period
    assert euler_drift == -168
    assert abs(euler_drift) + 72 == 240
