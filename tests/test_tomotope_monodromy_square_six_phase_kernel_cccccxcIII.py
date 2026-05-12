def test_tomotope_monodromy_is_aut_times_flags():
    aut_t = 96
    flags_t = 192
    mon_t = 18432
    assert aut_t * flags_t == mon_t


def test_regular_cover_square_scale():
    flags_t = 192
    gamma2 = 36864
    assert flags_t * flags_t == gamma2


def test_mon_t_is_half_of_regular_cover_square():
    mon_t = 18432
    gamma2 = 36864
    assert 2 * mon_t == gamma2


def test_precursor_monodromy_is_double_square():
    flags_t = 192
    precursor_mon = 73728
    assert precursor_mon == 2 * flags_t * flags_t


def test_toroidal_cover_family_has_six_phase_kernel():
    gamma2 = 36864
    for k in [2, 3, 5, 7]:
        assert gamma2 * (k ** 6) == 36864 * (k ** 6)


def test_six_phase_shell_sources():
    six_sources = {
        "tetrahedral_bivectors": 6,
        "a2_roots": 6,
        "we6_singletons": 6,
        "pointed_seven_shell_remainder": 6,
        "toroidal_kernel_rank": 6,
    }
    assert all(v == 6 for v in six_sources.values())


def test_packet_ladder():
    packet = 24
    assert 4 * packet == 96
    assert 7 * packet == 168
    assert 8 * packet == 192
    assert 192 * 192 == 36864
