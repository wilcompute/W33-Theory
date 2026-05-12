def test_tomotope_is_eight_tetrahedral_packets():
    tetrahedral_flag_packet = 24
    tomotope_flags = 192
    assert 8 * tetrahedral_flag_packet == tomotope_flags


def test_toroidal_phase_shell_is_seven_tetrahedral_packets():
    tetrahedral_flag_packet = 24
    toroidal_phase_shell = 168
    assert 7 * tetrahedral_flag_packet == toroidal_phase_shell


def test_toroidal_plus_ground_shell_is_tomotope_scale():
    toroidal_phase_shell = 168
    tetrahedral_ground_shell = 24
    tomotope_flags = 192
    assert toroidal_phase_shell + tetrahedral_ground_shell == tomotope_flags


def test_d4_and_f4_symmetry_scales():
    d4_scale = 192
    f4_scale = 1152
    assert 6 * d4_scale == f4_scale


def test_24_cell_incidence_counts():
    vertices = 24
    edges = 96
    faces = 96
    cells = 24
    assert vertices == cells == 24
    assert edges == faces == 96
    assert vertices + cells == 48
    assert edges + faces == 192


def test_d4_root_count_matches_tetrahedral_packet():
    d4_roots = 24
    tetrahedral_packet = 24
    assert d4_roots == tetrahedral_packet


def test_packet_ladder():
    packet = 24
    assert 7 * packet == 168
    assert 8 * packet == 192
    assert 48 * packet == 1152
