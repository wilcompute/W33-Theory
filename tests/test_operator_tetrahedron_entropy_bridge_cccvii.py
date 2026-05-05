from fractions import Fraction

from exploration.PART_CCCVII_OPERATOR_TETRAHEDRON_ENTROPY_BRIDGE import (
    q,
    V,
    K,
    r,
    s,
    E,
    DIRECTED,
    HASHIMOTO_BRANCH,
    Phi3,
    Phi4,
    Phi6,
    J,
    J_inv,
    EW,
    ALBERT,
    H1,
    ADJ_SPECTRUM,
    LAPLACIAN_SPECTRUM,
    SIGNLESS_SPECTRUM,
    DISTANCE_SPECTRUM,
    Q_TRACE,
    Q_SECOND_MOMENT,
    Q_ENERGY,
    D_TRACE,
    D_SECOND_MOMENT,
    DISTANCE_PERRON,
    WIENER_INDEX,
    TREE_EXP_2,
    TREE_EXP_5,
    NORMALIZED_Q2,
    NORMALIZED_D2,
    NORMALIZED_SECOND_MOMENT_SUM,
    NORMALIZED_SECOND_MOMENT_DIFF,
    operator_tetrahedron_entropy_audit,
)


def test_four_operator_spectra():
    assert ADJ_SPECTRUM == [(12, 1), (2, 24), (-4, 15)]
    assert LAPLACIAN_SPECTRUM == [(0, 1), (10, 24), (16, 15)]
    assert SIGNLESS_SPECTRUM == [(24, 1), (14, 24), (8, 15)]
    assert DISTANCE_SPECTRUM == [(66, 1), (-4, 24), (2, 15)]


def test_l_q_and_distance_affine_relations():
    for (lv, lm), (qv, qm) in zip(LAPLACIAN_SPECTRUM, SIGNLESS_SPECTRUM):
        assert lm == qm
        assert lv + qv == 2 * K
    assert -2 - r == s
    assert -2 - s == r
    assert DISTANCE_PERRON == K * (K - 1) // 2 == 66


def test_signless_moments_and_directed_carrier():
    assert DIRECTED == 2 * E == 480
    assert DIRECTED == 2 * q * (H1 - 1)
    assert Q_TRACE == DIRECTED
    assert Q_SECOND_MOMENT == DIRECTED * Phi3 == 6240
    assert Q_ENERGY == E // 2 == 120


def test_distance_moments_and_wiener():
    assert D_TRACE == 0
    assert D_SECOND_MOMENT == DIRECTED * Phi4 == 4800
    assert WIENER_INDEX == 1320
    assert WIENER_INDEX == HASHIMOTO_BRANCH * Q_ENERGY


def test_tree_exponent_recovery_from_second_moments():
    assert NORMALIZED_Q2 == Phi3 == 13
    assert NORMALIZED_D2 == Phi4 == 10
    assert NORMALIZED_SECOND_MOMENT_SUM == TREE_EXP_5 == 23
    assert NORMALIZED_SECOND_MOMENT_DIFF == q == 3
    assert (NORMALIZED_SECOND_MOMENT_SUM + NORMALIZED_SECOND_MOMENT_DIFF) / 2 == Phi3
    assert (NORMALIZED_SECOND_MOMENT_SUM - NORMALIZED_SECOND_MOMENT_DIFF) / 2 == Phi4


def test_matrix_tree_exponents():
    assert TREE_EXP_2 == H1 == q ** 4 == 81
    assert TREE_EXP_5 == ALBERT - EW == 23


def test_threshold_carrier_relations():
    assert (J * J_inv) % Phi3 == 1
    assert Phi6 + 1 == J_inv


def test_audit_checks_all_true():
    audit = operator_tetrahedron_entropy_audit()
    assert all(audit["checks"].values())
    assert audit["new_bridge_identities"]["tree_5_exponent_from_second_moments"] == "e5(tau)=23=(tr(Q^2)+tr(Delta^2))/(2E)=Phi3+Phi4"
