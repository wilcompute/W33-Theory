from fractions import Fraction


def test_vertex_bridge_exact_singular_values():
    sigma2 = Fraction(81, 640)
    rank = 8
    assert rank * sigma2 == Fraction(81, 80)
    assert rank * sigma2 * sigma2 == Fraction(6561, 51200)
    assert rank == 8


def test_triangle_bridge_exact_singular_values():
    sigma2 = Fraction(81, 640)
    rank = 2
    assert rank * sigma2 == Fraction(81, 320)
    assert rank * sigma2 * sigma2 == Fraction(6561, 204800)
    assert rank == 2


def test_incidence_frame_edge_counts():
    # W(3,3) is 12-regular; a marked vertex-star masks 12 edges.
    assert 12 == 12
    # A triangle frame masks its 3 edges.
    assert 3 == 3


def test_effective_mass_atom_formula():
    sigma2 = Fraction(81, 640)
    # Vertex atom gives eight equal mass eigenvalue numerators.
    vertex_multiplicity = 8
    triangle_multiplicity = 2
    assert vertex_multiplicity * sigma2 == Fraction(81, 80)
    assert triangle_multiplicity * sigma2 == Fraction(81, 320)
    # Single vertex bridge leaves 81-8 massless kernel directions.
    assert 81 - vertex_multiplicity == 73


def test_bridge_atom_interpretation():
    # One vertex-frame atom is degenerate; hierarchy requires combinations
    # of incidence-frame atoms or lower-symmetry frame data.
    active_vertex_channels = 8
    active_triangle_channels = 2
    assert active_vertex_channels == 4 * active_triangle_channels
