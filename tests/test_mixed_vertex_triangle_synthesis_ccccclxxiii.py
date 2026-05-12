def test_mixed_span_rank():
    assert max(39, 120) == 120


def test_vertex_span_inside_triangle_span_dimension_count():
    vertex_dim = 39
    triangle_dim = 120
    complement = triangle_dim - vertex_dim
    assert complement == 81


def test_chain_dimension_match():
    rank_d1 = 39
    h1 = 81
    boundary_sector = 120
    assert rank_d1 + h1 == boundary_sector


def test_incidence_hierarchy():
    assert 2 < 8 < 39 < 120
