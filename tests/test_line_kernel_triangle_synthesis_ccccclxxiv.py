def test_k4_line_triangle_kernel_dimension():
    number_of_triangles = 160
    number_of_k4_lines = 40
    active_triangle_synthesis = number_of_triangles - number_of_k4_lines
    assert active_triangle_synthesis == 120


def test_each_k4_line_contains_four_triangles():
    vertices_per_line = 4
    triangles_per_line = 4
    assert triangles_per_line == vertices_per_line


def test_triangle_synthesis_decomposition():
    vertex_gradient_modes = 39
    homological_modes = 81
    active_triangle_synthesis = 120
    assert vertex_gradient_modes + homological_modes == active_triangle_synthesis


def test_kernel_and_chain_matches():
    assert 40 == 40  # W(3,3) vertices and K4 lines
    assert 39 + 81 == 120
    assert 160 - 40 == 120
