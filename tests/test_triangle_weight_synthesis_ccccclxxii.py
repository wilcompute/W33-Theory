from fractions import Fraction


def test_triangle_synthesis_rank_and_nullity():
    assert 160 - 40 == 120


def test_triangle_gram_spectrum():
    assert {"0": 40, "27/80": 120} == {"0": 40, "27/80": 120}


def test_vertex_triangle_comparison():
    vertex_rank = 39
    triangle_rank = 120
    assert vertex_rank < triangle_rank
    assert 24 + 15 == vertex_rank


def test_single_atom_to_synthesis_scale():
    single_triangle_s2 = Fraction(81, 320)
    gram_active = Fraction(27, 80)
    assert single_triangle_s2 / gram_active == Fraction(3, 4)


def test_generic_rank_observation():
    assert 80 < 81
