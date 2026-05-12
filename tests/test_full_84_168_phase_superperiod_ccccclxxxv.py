from math import gcd


def lcm(a, b):
    return a * b // gcd(a, b)


def test_coupled_phase_periods():
    local_transport_period = 12 // gcd(12, 3)
    face_decimal_period = 12 // gcd(12, 2)
    fano_period = 7
    assert local_transport_period == 4
    assert face_decimal_period == 6
    assert fano_period == 7
    assert lcm(lcm(local_transport_period, face_decimal_period), fano_period) == 84


def test_euler_drift_over_full_period():
    full_period = 84
    delta_chi = -2
    assert full_period * delta_chi == -168


def test_fano_automorphism_order_match():
    # |GL(3,2)|=(2^3-1)(2^3-2)(2^3-2^2)=7*6*4=168.
    assert (8 - 1) * (8 - 2) * (8 - 4) == 168


def test_phase_state_period_84():
    def state(h):
        return (3 * h % 12, -2 * h % 12, h % 7)
    assert state(0) == (0, 0, 0)
    assert state(84) == state(0)
    assert all(state(k) != state(0) for k in range(1, 84))


def test_relation_to_28_56_subperiod():
    transport_fano_period = 4 * 7
    assert transport_fano_period == 28
    assert -2 * transport_fano_period == -56
    assert 3 * transport_fano_period == 84
    assert 3 * 56 == 168
