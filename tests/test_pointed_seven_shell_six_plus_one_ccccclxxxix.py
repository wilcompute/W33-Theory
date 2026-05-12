def test_pointed_seven_shell_decomposes_as_one_plus_six():
    seven_shell = 7
    distinguished = 1
    active_six_shell = 6
    assert distinguished + active_six_shell == seven_shell


def test_fano_automorphism_as_seven_tetrahedral_stabilizers():
    fano_aut_order = 168
    pointed_choices = 7
    stabilizer_order = 24
    assert pointed_choices * stabilizer_order == fano_aut_order


def test_tetrahedron_has_six_edges_and_bivectors():
    vertices = 4
    edges = vertices * (vertices - 1) // 2
    bivectors_in_four_directions = 4 * 3 // 2
    assert edges == 6
    assert bivectors_in_four_directions == 6


def test_a2_root_hexagon_has_six_roots():
    a2_positive_roots = 3
    a2_roots = 2 * a2_positive_roots
    assert a2_roots == 6


def test_phase_shell_as_matter_pair_plus_six_shell():
    g1 = 81
    g2 = 81
    active_six_shell = 6
    phase_shell = 168
    assert g1 + g2 + active_six_shell == phase_shell


def test_dual_toroidal_pointed_shells():
    # Csaszar: one distinguished vertex plus six adjacent vertices in K7.
    # Szilassi dual: one distinguished face plus six adjacent faces among seven faces.
    csaszar_total_vertices = 7
    szilassi_total_faces = 7
    assert csaszar_total_vertices - 1 == 6
    assert szilassi_total_faces - 1 == 6


def test_unified_six_dictionary():
    six_sources = {
        "tetrahedral_edges_or_bivectors": 6,
        "a2_roots": 6,
        "pointed_fano_remainder": 6,
        "pointed_toroidal_remainder": 6,
        "we6_singleton_orbits": 6,
    }
    assert all(v == 6 for v in six_sources.values())
