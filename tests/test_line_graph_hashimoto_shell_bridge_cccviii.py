from exploration.PART_CCCVIII_LINE_GRAPH_HASHIMOTO_SHELL_BRIDGE import (
    q,
    V,
    K,
    lam,
    E,
    DIRECTED,
    HASHIMOTO_BRANCH,
    Phi3,
    Phi4,
    Phi6,
    J,
    J_inv,
    H1,
    ALBERT,
    LINE_VERTICES,
    LINE_VALENCY,
    LINE_EDGES,
    LINE_SPECTRUM,
    LINE_TRACE,
    LINE_SECOND_MOMENT,
    LINE_NULLITY,
    LINE_NORMALIZED_SECOND,
    SIGNLESS_TRACE,
    SIGNLESS_ENERGY,
    WIENER_INDEX,
    Q_SECOND_MOMENT,
    D_SECOND_MOMENT,
    TREE_EXP_2,
    TREE_EXP_5,
    DISTANCE_PERRON,
    line_graph_hashimoto_shell_audit,
)


def test_edge_shell_and_directed_lift():
    assert LINE_VERTICES == E == q * (H1 - 1) == 240
    assert DIRECTED == 2 * LINE_VERTICES == 480
    assert SIGNLESS_TRACE == DIRECTED


def test_line_graph_branch_structure():
    assert HASHIMOTO_BRANCH == K - 1 == 11
    assert LINE_VALENCY == 2 * HASHIMOTO_BRANCH == 22
    assert LINE_EDGES == V * K * (K - 1) // 2 == 2640


def test_line_graph_spectrum_and_moments():
    assert LINE_SPECTRUM == [(22, 1), (12, 24), (6, 15), (-2, 200)]
    assert sum(mult for _, mult in LINE_SPECTRUM) == LINE_VERTICES
    assert LINE_TRACE == 0
    assert LINE_SECOND_MOMENT == 2 * LINE_EDGES == 5280
    assert LINE_SECOND_MOMENT == DIRECTED * HASHIMOTO_BRANCH
    assert LINE_NORMALIZED_SECOND == HASHIMOTO_BRANCH


def test_line_spectrum_special_values():
    assert LINE_NULLITY == E - V == J * V == 200
    assert LINE_SPECTRUM[0][0] == 2 * HASHIMOTO_BRANCH == 22
    assert LINE_SPECTRUM[1][0] == K == 12
    assert LINE_SPECTRUM[2][0] == lam * q == 6
    assert LINE_SPECTRUM[3][0] == -lam == -2


def test_distance_and_operator_tetrahedron_echoes():
    assert DISTANCE_PERRON == K * (K - 1) // 2 == 66
    assert WIENER_INDEX == HASHIMOTO_BRANCH * SIGNLESS_ENERGY == 1320
    assert (Q_SECOND_MOMENT + D_SECOND_MOMENT) // DIRECTED == TREE_EXP_5 == Phi3 + Phi4 == 23
    assert TREE_EXP_2 == H1 == 81
    assert TREE_EXP_5 == ALBERT - (q + 1) == 23


def test_threshold_carrier_relations():
    assert (J * J_inv) % Phi3 == 1
    assert Phi6 + 1 == J_inv


def test_audit_checks_all_true():
    audit = line_graph_hashimoto_shell_audit()
    assert all(audit["checks"].values())
    assert audit["bridge_identities"]["moment_branch_recovery"] == "tr(A_L^2)/480=11=K-1"
