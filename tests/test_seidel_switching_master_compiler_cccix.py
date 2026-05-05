from exploration.PART_CCCIX_SEIDEL_SWITCHING_MASTER_COMPILER import (
    q,
    V,
    K,
    lam,
    mu,
    E,
    DIRECTED,
    HASHIMOTO_BRANCH,
    Phi3,
    Phi4,
    Phi6,
    J_atom,
    J_inv,
    ALBERT,
    H1,
    QLE,
    Q_SECOND_MOMENT,
    D_SECOND_MOMENT,
    TREE_EXP_2,
    TREE_EXP_5,
    LINE_VALENCY,
    LINE_SECOND_MOMENT,
    SEIDEL_SPECTRUM,
    SIGMA0,
    SIGMA1,
    SIGMA2,
    SEIDEL_TRACE,
    SEIDEL_SECOND_MOMENT,
    SEIDEL_ENERGY,
    SEIDEL_POSITIVE_MASS,
    SEIDEL_NEGATIVE_MASS,
    SEIDEL_NORMALIZED_BY_QLE,
    seidel_switching_master_compiler_audit,
)


def test_seidel_spectrum_and_basic_moments():
    assert SEIDEL_SPECTRUM == [(15, 1), (-5, 24), (7, 15)]
    assert SEIDEL_TRACE == 0
    assert SEIDEL_SECOND_MOMENT == V * (V - 1) == 1560


def test_seidel_energy_is_edge_shell():
    assert SEIDEL_ENERGY == E == q * (H1 - 1) == 240
    assert DIRECTED == 2 * E == 480


def test_balanced_switching_masses():
    assert SEIDEL_POSITIVE_MASS == QLE == 120
    assert SEIDEL_NEGATIVE_MASS == QLE == 120
    assert SEIDEL_POSITIVE_MASS + SEIDEL_NEGATIVE_MASS == SEIDEL_ENERGY


def test_phi_recovery_from_switching_and_distance():
    assert SEIDEL_NORMALIZED_BY_QLE == Phi3 == 13
    assert D_SECOND_MOMENT // (4 * QLE) == Phi4 == 10
    assert SEIDEL_NORMALIZED_BY_QLE + D_SECOND_MOMENT // (4 * QLE) == TREE_EXP_5 == 23
    assert (Q_SECOND_MOMENT + D_SECOND_MOMENT) // DIRECTED == TREE_EXP_5


def test_seidel_gap_recoveries():
    assert SIGMA0 == 15
    assert SIGMA1 == -(mu + 1) == -5
    assert SIGMA2 == lam + mu + 1 == 7
    assert SIGMA0 + SIGMA2 == LINE_VALENCY == 2 * HASHIMOTO_BRANCH == 22
    assert SIGMA0 - abs(SIGMA1) == Phi4 == 10
    assert SIGMA2 - abs(SIGMA1) == lam == 2
    assert SIGMA0 - SIGMA2 == J_inv == 8


def test_line_and_hashimoto_recovery():
    assert LINE_SECOND_MOMENT == DIRECTED * HASHIMOTO_BRANCH == 5280
    assert LINE_SECOND_MOMENT // DIRECTED == HASHIMOTO_BRANCH == K - 1 == 11


def test_tree_exponents_and_threshold():
    assert TREE_EXP_2 == H1 == q ** 4 == 81
    assert TREE_EXP_5 == Phi3 + Phi4 == ALBERT - (q + 1) == 23
    assert (J_atom * J_inv) % Phi3 == 1
    assert Phi6 + 1 == J_inv


def test_audit_checks_all_true():
    audit = seidel_switching_master_compiler_audit()
    assert all(audit["checks"].values())
    assert audit["bridge_identities"]["tree_5_from_switching_distance"] == "e5(tau)=Phi3+Phi4=tr(S^2)/QLE + tr(Delta^2)/(4QLE)"
