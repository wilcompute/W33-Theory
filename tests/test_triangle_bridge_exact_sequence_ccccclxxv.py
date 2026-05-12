def test_first_exact_sequence_dimensions():
    line_sum_kernel = 40
    triangle_weights = 160
    active_bridge = 120
    assert triangle_weights - line_sum_kernel == active_bridge


def test_second_exact_sequence_dimensions():
    vertex_image = 39
    active_bridge = 120
    quotient = 81
    assert active_bridge - vertex_image == quotient


def test_compressed_quotient_identity():
    tri_mod_line = 160 - 40
    q = tri_mod_line - 39
    assert tri_mod_line == 120
    assert q == 81


def test_chain_complex_match():
    rank_d1 = 39
    h1 = 81
    boundary_sector = 120
    assert rank_d1 + h1 == boundary_sector


def test_named_spaces():
    spaces = {
        "L_40": 40,
        "Tri_160": 160,
        "Y_tri_120": 120,
        "Y_vert_39": 39,
        "Q_81": 81,
    }
    assert spaces["Tri_160"] - spaces["L_40"] == spaces["Y_tri_120"]
    assert spaces["Y_tri_120"] - spaces["Y_vert_39"] == spaces["Q_81"]
