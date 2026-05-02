from PART_CLXVII_FANO_TRANSPORT_GRAMMAR import (
    Q,
    RANK_SEED,
    Q2,
    J,
    J_INV,
    PHI3,
    PHI6,
    FANO_LINES,
    DIRECTION_GROUPS,
    transport_lines,
    fano_transport_grammar_audit,
)


def _rows():
    return {r.name: r for r in transport_lines()}


def test_horizontal_lines_preserve_threshold_product():
    rows = _rows()
    assert [rows[n].affine_pair_product_mod13 for n in DIRECTION_GROUPS["threshold_horizontal_q"]] == [J, J]
    assert rows["horizontal_y0"].direction == rows["horizontal_y1"].direction == Q


def test_vertical_lines_are_additive_opposition():
    rows = _rows()
    assert [rows[n].affine_pair_sum_mod13 for n in DIRECTION_GROUPS["rank_vertical_2q"]] == [0, 0]
    assert rows["vertical_x0"].direction == rows["vertical_x1"].direction == RANK_SEED


def test_diagonal_lines_preserve_carrier_product():
    rows = _rows()
    assert [rows[n].affine_pair_product_mod13 for n in DIRECTION_GROUPS["carrier_diagonal_q2"]] == [J_INV, J_INV]
    assert rows["diagonal_main"].direction == rows["diagonal_shift"].direction == Q2


def test_line_at_infinity_closes_q_axis():
    rows = _rows()
    infinity = rows["line_at_infinity"]
    assert infinity.points == [Q, RANK_SEED, Q2]
    assert infinity.total_sum_mod13 == J
    assert infinity.total_product_mod13 == RANK_SEED


def test_transport_links_to_mixer_and_phi6():
    rows = _rows()
    assert (J * J_INV) % PHI3 == 1
    assert J + J_INV == PHI3
    assert abs(J_INV - J) == Q
    assert rows["diagonal_main"].total_product_mod13 == rows["diagonal_shift"].total_product_mod13 == PHI6


def test_audit_checks_all_true():
    audit = fano_transport_grammar_audit()
    assert all(audit["checks"].values())
    assert audit["direction_transports"][0]["value"] == "5"
    assert audit["direction_transports"][2]["value"] == "8"
