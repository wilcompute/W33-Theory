from exploration.PART_CCCXVII_IHARA_ZETA_TREE_ENTROPY_COMPILER import (
    q,
    K,
    V,
    Phi3,
    Phi4,
    Phi6,
    J,
    J_inv,
    H1,
    E,
    DIRECTED,
    HASHIMOTO_BRANCH,
    EDGE_EXCESS,
    ADJ_SPECTRUM,
    LAPLACIAN_SPECTRUM,
    IHARA_THETA_K_FACTOR_U1,
    IHARA_THETA_R_FACTOR_U1,
    IHARA_THETA_S_FACTOR_U1,
    IHARA_RESTRICTED_PRODUCT_U1,
    RESTRICTED_LAPLACIAN_PRODUCT,
    TREE_COUNT,
    E2_FROM_IHARA_TREE,
    E5_FROM_IHARA_TREE,
    TRIVIAL_FACTOR_RESIDUE_U1_ABS,
    SIGNED_REDUCED_IHARA_LIMIT,
    ABS_REDUCED_IHARA_LIMIT,
    HASHIMOTO_ROOT_DATA,
    LINE_SECOND_MOMENT,
    TR_A3,
    ihara_zeta_tree_entropy_audit,
)


def test_basic_spectra_and_atoms():
    assert (q, V, K, E, DIRECTED, HASHIMOTO_BRANCH) == (3, 40, 12, 240, 480, 11)
    assert EDGE_EXCESS == E - V == 200 == J * V
    assert ADJ_SPECTRUM == [(12, 1), (2, 24), (-4, 15)]
    assert LAPLACIAN_SPECTRUM == [(0, 1), (10, 24), (16, 15)]


def test_ihara_u1_restricted_factors_are_laplacian_eigenvalues():
    assert IHARA_THETA_K_FACTOR_U1 == 0
    assert (IHARA_THETA_R_FACTOR_U1, IHARA_THETA_S_FACTOR_U1) == (Phi4, (q + 1) ** 2) == (10, 16)
    assert IHARA_RESTRICTED_PRODUCT_U1 == RESTRICTED_LAPLACIAN_PRODUCT


def test_matrix_tree_factorization_from_ihara():
    assert RESTRICTED_LAPLACIAN_PRODUCT == V * TREE_COUNT
    assert TREE_COUNT == 2 ** 81 * 5 ** 23
    assert E2_FROM_IHARA_TREE == H1 == 81
    assert E5_FROM_IHARA_TREE == Phi3 + Phi4 == 23


def test_trivial_factor_residue_and_reduced_limit():
    assert TRIVIAL_FACTOR_RESIDUE_U1_ABS == K - 2 == Phi4 == 10
    assert SIGNED_REDUCED_IHARA_LIMIT == -(K - 2) * RESTRICTED_LAPLACIAN_PRODUCT
    assert ABS_REDUCED_IHARA_LIMIT == (K - 2) * V * TREE_COUNT == 400 * TREE_COUNT


def test_hashimoto_spectral_circle():
    assert HASHIMOTO_ROOT_DATA["theta_12"]["roots"] == [11, 1]
    assert HASHIMOTO_ROOT_DATA["theta_2"]["real"] ** 2 + HASHIMOTO_ROOT_DATA["theta_2"]["imag_sq"] == HASHIMOTO_BRANCH
    assert HASHIMOTO_ROOT_DATA["theta_minus4"]["real"] ** 2 + HASHIMOTO_ROOT_DATA["theta_minus4"]["imag_sq"] == HASHIMOTO_BRANCH


def test_companion_operator_counts():
    assert LINE_SECOND_MOMENT == DIRECTED * HASHIMOTO_BRANCH == 5280
    assert TR_A3 == 960


def test_threshold_relations():
    assert (J * J_inv) % Phi3 == 1
    assert Phi6 + 1 == J_inv


def test_audit_checks_all_true():
    audit = ihara_zeta_tree_entropy_audit()
    assert all(audit["checks"].values())
    assert audit["bridge_identities"]["tree_e2"] == "e2=24+4*15-v2(40)=81=q^4"
