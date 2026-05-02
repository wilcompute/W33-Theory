from PART_CLXVIII_FANO_EDGE_COLOR_LIFT import (
    Q,
    V,
    E,
    DIRECTED_EDGES,
    EDGE_COLORS,
    EDGES_PER_COLOR,
    DIRECTED_EDGES_PER_COLOR,
    RANK_SEED,
    Q2,
    direction_lifts,
    fano_edge_color_lift_audit,
)


def test_w33_edge_color_counts():
    assert E == 240
    assert DIRECTED_EDGES == 480
    assert EDGE_COLORS == Q == 3
    assert EDGES_PER_COLOR == 80
    assert DIRECTED_EDGES_PER_COLOR == 160


def test_each_fano_direction_lifts_to_one_color():
    for row in direction_lifts():
        assert row.seed_transitions == 2
        assert row.lift_vertices == V == 40
        assert row.lifted_edges == EDGES_PER_COLOR == 80
        assert row.lifted_directed_edges == DIRECTED_EDGES_PER_COLOR == 160


def test_three_directions_cover_all_edges():
    rows = direction_lifts()
    assert sum(r.lifted_edges for r in rows) == E
    assert sum(r.lifted_directed_edges for r in rows) == DIRECTED_EDGES


def test_direction_residues_are_q_axis():
    assert {r.direction_residue for r in direction_lifts()} == {Q, RANK_SEED, Q2} == {3, 6, 9}


def test_color_factorizations():
    assert EDGE_COLORS * 2 * V == E
    assert EDGE_COLORS * 2 * 2 * V == DIRECTED_EDGES
    assert EDGES_PER_COLOR == 2 * V
    assert DIRECTED_EDGES_PER_COLOR == 4 * V


def test_audit_checks_all_true():
    audit = fano_edge_color_lift_audit()
    assert all(audit["checks"].values())
    assert audit["lift_identity"]["three_directions"] == "3 * 2 * 40 = 240 edges"
