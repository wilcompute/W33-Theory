from scripts.tomotope_six_kernel_vertex_lift import build_vertex_lift


def test_vertex_lift_summary():
    payload = build_vertex_lift()
    summary = payload["summary"]

    assert summary["generator_count"] == 4
    assert summary["all_generators_lifted"] is True
    assert summary["all_lifts_verified_on_edges"] is True
    assert summary["vertex_group_order"] == 24


def test_all_lifts_are_permutations_of_four_vertices():
    payload = build_vertex_lift()
    lifts = payload["lifted_vertex_generators"]

    assert set(lifts.keys()) == {"p0", "p1", "p2", "p3"}
    for perm in lifts.values():
        assert len(perm) == 4
        assert set(perm) == {0, 1, 2, 3}


def test_tetrahedral_edge_generators_are_permutations_on_six_edges():
    payload = build_vertex_lift()
    edge_gens = payload["tetrahedral_edge_generators"]

    for perm in edge_gens.values():
        assert len(perm) == 6
        assert set(perm) == set(range(6))
