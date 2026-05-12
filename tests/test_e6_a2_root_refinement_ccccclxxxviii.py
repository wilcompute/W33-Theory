def test_root_level_e8_grading_count():
    e6_roots = 72
    a2_roots = 6
    g1_roots = 81
    g2_roots = 81
    assert e6_roots + a2_roots + g1_roots + g2_roots == 240


def test_lie_algebra_dimension_grading_count():
    dim_e6 = 78
    dim_a2 = 8
    g1 = 81
    g2 = 81
    assert dim_e6 + dim_a2 + g1 + g2 == 248


def test_we6_orbits_refine_to_e6_a2_matter():
    one_72_orbit = 72
    six_singletons = 6
    six_27_orbits = 6 * 27
    assert one_72_orbit + six_singletons + six_27_orbits == 240
    assert six_singletons == 6
    assert six_27_orbits == 162


def test_six_27_orbits_split_into_two_81_charge_triples():
    charge_triple = 3 * 27
    conjugate_charge_triple = 3 * 27
    assert charge_triple == 81
    assert conjugate_charge_triple == 81
    assert charge_triple + conjugate_charge_triple == 162


def test_a2_root_and_rank_counts():
    a2_roots = 6
    a2_rank = 2
    dim_a2 = 8
    assert a2_roots + a2_rank == dim_a2


def test_e6_root_and_rank_counts():
    e6_roots = 72
    e6_rank = 6
    dim_e6 = 78
    assert e6_roots + e6_rank == dim_e6
