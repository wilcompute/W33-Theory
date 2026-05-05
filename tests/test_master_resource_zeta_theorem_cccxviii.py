from exploration.PART_CCCXVIII_MASTER_RESOURCE_ZETA_THEOREM import (
    q,
    lam,
    mu,
    V,
    K,
    Phi3,
    Phi4,
    Phi6,
    J,
    J_inv,
    H1,
    ALBERT,
    E,
    DIRECTED,
    TRIANGLES,
    TR_A3,
    HASHIMOTO_BRANCH,
    EDGE_EXCESS,
    QLE,
    Q_SECOND_MOMENT,
    D_SECOND_MOMENT,
    LINE_SECOND_MOMENT,
    WIENER_INDEX,
    S_SECOND_MOMENT,
    IHARA_RESTRICTED_FACTORS_U1,
    TREE_EXP_2,
    TREE_EXP_5,
    DIRAC_BASES,
    DIRAC_EXPS,
    DIRAC_DEGREE,
    DIRAC_EXP_PRODUCT,
    DIRAC_SIGNED_FIRST,
    DIRAC_SECOND,
    DIRAC_Z1_EXP,
    FUSION_P_NUM,
    FUSION_P_DEN,
    CRITICAL_EDGE_HALF,
    CRITICAL_EXPECTED_DEGREE,
    CRITICAL_STABILIZER_WEIGHT,
    RESOURCE_LADDER,
    CLIFFORD_ORDER,
    CLIFFORD_QUOTIENTS,
    CLIFFORD_QUOTIENT_FACTORS,
    master_resource_zeta_audit,
)


def test_w33_and_cyclotomic_atoms():
    assert (q, lam, mu, V, K, E, DIRECTED) == (3, 2, 4, 40, 12, 240, 480)
    assert (Phi3, Phi4, Phi6, J, J_inv, H1, ALBERT) == (13, 10, 7, 5, 8, 81, 27)


def test_operator_normalizers():
    assert HASHIMOTO_BRANCH == K - 1 == 11
    assert EDGE_EXCESS == J * V == 200
    assert LINE_SECOND_MOMENT == DIRECTED * HASHIMOTO_BRANCH == 5280
    assert WIENER_INDEX == HASHIMOTO_BRANCH * QLE == 1320
    assert (Q_SECOND_MOMENT // DIRECTED, D_SECOND_MOMENT // DIRECTED, LINE_SECOND_MOMENT // DIRECTED) == (Phi3, Phi4, HASHIMOTO_BRANCH)
    assert S_SECOND_MOMENT // QLE == Phi3


def test_ihara_matrix_tree_and_dirac():
    assert IHARA_RESTRICTED_FACTORS_U1 == (Phi4, mu ** 2) == (10, 16)
    assert TREE_EXP_2 == H1 == 81
    assert TREE_EXP_5 == Phi3 + Phi4 == 23
    assert DIRAC_BASES == [J, -1, -Phi6]
    assert DIRAC_EXPS == [Phi4, mu ** 2, 2 * q]
    assert DIRAC_DEGREE == 32
    assert DIRAC_EXP_PRODUCT == TR_A3 == 960
    assert DIRAC_SIGNED_FIRST == -J_inv
    assert DIRAC_SECOND == Phi6 * (H1 - 1)
    assert DIRAC_Z1_EXP == 2 * ALBERT


def test_photonic_critical_and_resource_ladder():
    assert (FUSION_P_NUM, FUSION_P_DEN) == (lam, mu) == (2, 4)
    assert CRITICAL_EDGE_HALF == QLE == 120
    assert CRITICAL_EXPECTED_DEGREE == 2 * q == 6
    assert CRITICAL_STABILIZER_WEIGHT == Phi6 == 7
    assert RESOURCE_LADDER == [120, 240, 480, 960]
    assert [RESOURCE_LADDER[i + 1] // RESOURCE_LADDER[i] for i in range(3)] == [2, 2, 2]


def test_clifford_resource_envelope():
    assert CLIFFORD_ORDER == 51840 == V * (mu ** 2) * H1
    assert CLIFFORD_QUOTIENTS == [432, 216, 108, 54]
    assert CLIFFORD_QUOTIENTS == CLIFFORD_QUOTIENT_FACTORS


def test_threshold_relations():
    assert (J * J_inv) % Phi3 == 1
    assert Phi6 + 1 == J_inv


def test_audit_checks_all_true():
    audit = master_resource_zeta_audit()
    assert all(audit["checks"].values())
    assert audit["master_equations"]["tree_exponents"] == "e2=q^4=81, e5=Phi3+Phi4=23"
