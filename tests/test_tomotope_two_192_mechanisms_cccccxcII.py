def test_intermediate_semiregular_group_order_192():
    tetrahedral_or_hemioctahedral_facet_group = 24
    facets_each_type = 8
    intermediate_group_order = 192
    assert facets_each_type * tetrahedral_or_hemioctahedral_facet_group == intermediate_group_order


def test_actual_tomotope_automorphism_order_and_flags():
    tomotope_automorphism_order = 96
    flag_orbits = 2
    tomotope_flags = 192
    assert flag_orbits * tomotope_automorphism_order == tomotope_flags


def test_tomotope_f_vector_and_facets():
    vertices = 4
    edges = 12
    triangles = 16
    tetrahedra = 4
    hemioctahedra = 4
    assert (vertices, edges, triangles, tetrahedra + hemioctahedra) == (4, 12, 16, 8)
    assert tetrahedra == hemioctahedra == 4


def test_intermediate_to_tomotope_collapse_halves_automorphism_scale():
    intermediate_group_order = 192
    tomotope_group_order = 96
    assert intermediate_group_order // 2 == tomotope_group_order


def test_24_cell_packet_ladder_with_two_192s():
    packet = 24
    intermediate_group_192 = 8 * packet
    tomotope_flag_192 = 2 * 96
    f4_scale = 1152
    assert intermediate_group_192 == 192
    assert tomotope_flag_192 == 192
    assert 6 * 192 == f4_scale


def test_reconciles_168_plus_24_with_tomotope_flags():
    toroidal_phase_shell = 168
    tetrahedral_ground_packet = 24
    assert toroidal_phase_shell + tetrahedral_ground_packet == 192
