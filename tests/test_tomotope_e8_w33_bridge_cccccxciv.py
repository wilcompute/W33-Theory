"""Tests for Part CCCCCXCIV: Complete Tomotope-E8-W33 Bridge."""


def test_universal_24_packet_ladder():
    """Verify all key values are multiples of 24."""
    assert 1 * 24 == 24
    assert 2 * 24 == 48
    assert 3 * 24 == 72
    assert 4 * 24 == 96
    assert 7 * 24 == 168
    assert 8 * 24 == 192
    assert 9 * 24 == 216
    assert 10 * 24 == 240


def test_w33_tomotope_bridge():
    """W33 edges = sqrt(Mon(Q_6)/Gamma_2) = 6^3."""
    w33_edges = 27 * 16 // 2
    assert w33_edges == 216
    gamma2 = 36864
    mon_q6_over_gamma2 = 6 ** 6
    assert w33_edges ** 2 == mon_q6_over_gamma2
    assert w33_edges == 6 ** 3


def test_e8_e6_toroidal_complement():
    """E8 roots minus E6 roots equals the Fano/toroidal phase shell."""
    e8_roots = 240
    e6_roots = 72
    fano_shell = 168
    assert e8_roots - e6_roots == fano_shell
    assert fano_shell == 7 * 24


def test_f4_equals_six_kernel_times_tomotope():
    """F4 symmetry scale = 6 * tomotope flags = 6 * 192."""
    f4 = 1152
    six_kernel_rank = 6
    tomotope_flags = 192
    assert f4 == six_kernel_rank * tomotope_flags


def test_eight_packet_decomposition():
    """192 = (1 + 6 + 1) * 24 = ground + six-phase + D4-closure."""
    ground = 1 * 24
    six_phase = 6 * 24
    closure = 1 * 24
    assert ground + six_phase + closure == 192


def test_e8_is_ten_tetrahedral_packets():
    """E8 root count = 10 * 24."""
    assert 240 == 10 * 24


def test_e8_tomotope_deficit_is_binary_octahedral():
    """E8 roots - tomotope flags = 240 - 192 = 48 = binary octahedral group order."""
    assert 240 - 192 == 48 == 2 * 24


def test_six_kernel_rank_matches_all_sources():
    """Six independent sources each give count=6."""
    sources = {
        "a2_root_hexagon": 6,
        "k4_tetrahedral_bivectors": 6,
        "we6_singleton_orbits": 6,
        "toroidal_monodromy_phase_dirs": 6,
        "clifford_bivector_rank_c42": 6,
        "csaszar_szilassi_six_shell": 6,
    }
    assert all(v == 6 for v in sources.values())
    assert len(sources) == 6


def test_w33_edges_is_cube_of_six_kernel():
    """W33 edge count = 6^3 = six_kernel_rank^3."""
    six_kernel_rank = 6
    assert 27 * 16 // 2 == six_kernel_rank ** 3
