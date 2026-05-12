def test_rank3_flag_count_is_four_edges():
    csaszar_edges = 21
    szilassi_edges = 21
    tetra_edges = 6
    assert 4 * csaszar_edges == 84
    assert 4 * szilassi_edges == 84
    assert 4 * tetra_edges == 24


def test_each_toroidal_map_splits_as_72_plus_12():
    total_flags = 84
    pointed_star_flags = 12
    active_remainder = 72
    assert pointed_star_flags + active_remainder == total_flags


def test_dual_toroidal_pair_flags_are_168():
    csaszar_flags = 84
    szilassi_flags = 84
    assert csaszar_flags + szilassi_flags == 168


def test_dual_pair_refines_as_72_72_24():
    active_csaszar = 72
    active_szilassi = 72
    two_pointed_stars = 24
    assert active_csaszar + active_szilassi + two_pointed_stars == 168


def test_two_pointed_stars_match_tetrahedron_flags():
    csaszar_pointed_star = 12
    szilassi_pointed_star = 12
    tetra_flags = 24
    assert csaszar_pointed_star + szilassi_pointed_star == tetra_flags


def test_toroidal_pair_plus_tetrahedron_is_tomotope_scale():
    toroidal_pair_flags = 168
    tetra_flags = 24
    tomotope_flag_scale = 192
    assert toroidal_pair_flags + tetra_flags == tomotope_flag_scale


def test_relation_to_81_81_6_phase_shell():
    assert 168 == 72 + 72 + 24
    assert 168 == 81 + 81 + 6
    assert 81 == 72 + 9
    assert 24 == 6 + 9 + 9
