from PART_CLXIX_FANO_THREE_GENERATION_LIFT import (
    Q,
    V,
    E,
    DIRECTED_EDGES,
    EDGE_COLORS,
    EDGES_PER_COLOR,
    Q4_CARRIER,
    H1_DIM,
    GENERATION_DIM,
    GENERATIONS,
    RANK_SEED,
    Q2,
    generation_lifts,
    fano_three_generation_lift_audit,
)


def test_h1_generation_count():
    assert H1_DIM == Q4_CARRIER == 81
    assert GENERATION_DIM == Q ** 3 == 27
    assert GENERATIONS == Q == 3
    assert GENERATIONS * GENERATION_DIM == H1_DIM


def test_edge_color_completion_to_q4():
    assert EDGES_PER_COLOR == Q4_CARRIER - 1 == 80
    assert EDGES_PER_COLOR + 1 == Q4_CARRIER
    assert EDGE_COLORS * EDGES_PER_COLOR == E == 240
    assert DIRECTED_EDGES == 480


def test_generation_lifts_by_fano_direction():
    rows = generation_lifts()
    assert len(rows) == GENERATIONS
    assert {r.direction_residue for r in rows} == {Q, RANK_SEED, Q2} == {3, 6, 9}
    assert all(r.slice_dimension == 27 for r in rows)


def test_q4_slices_as_q_by_q3():
    assert Q4_CARRIER == Q * (Q ** 3) == 81


def test_audit_checks_all_true():
    audit = fano_three_generation_lift_audit()
    assert all(audit["checks"].values())
    assert audit["carrier_completion"]["generation_slicing"] == "q^4=q*q^3=3*27"
