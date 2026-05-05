from exploration.PART_CCCXII_DIRAC_DETERMINANT_OPERATOR_COMPILER import (
    q,
    lam,
    K,
    Phi3,
    Phi4,
    Phi6,
    J,
    J_inv,
    EW,
    H1,
    ALBERT,
    E,
    DIRECTED,
    TRIANGLES,
    TR_A3,
    FIEDLER,
    LAPLACIAN_RADIUS,
    LAPLACIAN_GAP,
    HASHIMOTO_BRANCH,
    DIRAC_BASES,
    DIRAC_MULTS,
    DIRAC_DEGREE,
    DIRAC_EXP_PRODUCT,
    DIRAC_SIGNED_FIRST,
    DIRAC_SECOND,
    DIRAC_ABS_ENDPOINT_SUM,
    DIRAC_ABS_ENDPOINT_DIFF,
    Z_AT_1_EXP,
    TREE_EXP_2,
    TREE_EXP_5,
    MARKOV_POS,
    MARKOV_NEG,
    KREIN_FIREWALL,
    KREIN_CARRIER_SQUARE,
    SEIDEL_ENERGY,
    LINE_SECOND_MOMENT,
    dirac_determinant_operator_compiler_audit,
)


def test_paper_determinant_data():
    assert DIRAC_BASES == [5, -1, -7]
    assert DIRAC_MULTS == [10, 16, 6]


def test_dirac_bases_from_j_phi6_and_center():
    assert DIRAC_BASES[0] == J == (K - lam) // 2 == 5
    assert DIRAC_BASES[2] == -Phi6 == -((K + lam) // 2) == -7
    assert DIRAC_BASES[0] == -1 + 2 * q
    assert DIRAC_BASES[2] == -1 - 2 * q
    assert DIRAC_ABS_ENDPOINT_SUM == K == 12
    assert DIRAC_ABS_ENDPOINT_DIFF == lam == 2


def test_dirac_multiplicities_are_laplacian_pair_gap():
    assert DIRAC_MULTS == [FIEDLER, LAPLACIAN_RADIUS, LAPLACIAN_GAP] == [Phi4, EW ** 2, 2 * q]
    assert DIRAC_DEGREE == 2 ** (q + lam) == 32
    assert DIRAC_DEGREE == Phi4 + EW ** 2 + 2 * q


def test_triangle_trace_and_dirac_moments():
    assert TRIANGLES == 160
    assert TR_A3 == 6 * TRIANGLES == 960
    assert DIRAC_EXP_PRODUCT == TR_A3
    assert DIRAC_SIGNED_FIRST == -J_inv == -8
    assert DIRAC_SECOND == Phi6 * (H1 - 1) == 560


def test_z_at_one_and_global_entropy():
    assert Z_AT_1_EXP == 2 * ALBERT == 54
    assert TREE_EXP_2 == H1 == 81
    assert TREE_EXP_5 == Phi3 + Phi4 == 23


def test_links_to_recent_operator_stack():
    assert MARKOV_POS == (1, 2 * q)
    assert MARKOV_NEG == (-1, q)
    assert KREIN_FIREWALL == q ** 2 == 9
    assert KREIN_CARRIER_SQUARE == J_inv ** 2 == 64
    assert SEIDEL_ENERGY == E == q * (H1 - 1) == 240
    assert LINE_SECOND_MOMENT == DIRECTED * HASHIMOTO_BRANCH == 5280


def test_threshold_carrier_relations():
    assert (J * J_inv) % Phi3 == 1
    assert Phi6 + 1 == J_inv


def test_audit_checks_all_true():
    audit = dirac_determinant_operator_compiler_audit()
    assert all(audit["checks"].values())
    assert audit["bridge_identities"]["exponents"] == "{10,16,6}={Phi4,(q+1)^2,2q} = Laplacian Fiedler/radius/gap"
