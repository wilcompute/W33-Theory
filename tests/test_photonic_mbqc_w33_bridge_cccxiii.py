from fractions import Fraction

from exploration.PART_CCCXIII_PHOTONIC_MBQC_W33_BRIDGE import (
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
    E,
    DIRECTED,
    HASHIMOTO_BRANCH,
    POLARIZATION_DIM,
    DUAL_RAIL_MODES,
    SU2_RANK_PLUS_ROOT,
    KLM_SIMPLE_SUCCESS,
    FUSION_SUCCESS,
    FUSION_ATTEMPTS_PER_EDGE,
    KLM_ATTEMPTS_PER_SIMPLE_CZ,
    CLUSTER_QUBITS,
    CLUSTER_EDGES,
    STABILIZER_WEIGHT,
    TOTAL_STABILIZER_SUPPORT,
    ORIENTED_STABILIZER_EDGE_INCIDENCES,
    EXPECTED_FUSION_ATTEMPTS_FULL_CLUSTER,
    EXPECTED_KLM_ATTEMPTS_FULL_EDGE_SET,
    SEIDEL_ENERGY,
    DIRAC_DEGREE,
    DIRAC_EXP_PRODUCT,
    TR_A3,
    TREE_EXP_2,
    TREE_EXP_5,
    photonic_mbqc_w33_bridge_audit,
)


def test_single_photon_qubit_dimensions():
    assert POLARIZATION_DIM == DUAL_RAIL_MODES == lam == 2
    assert SU2_RANK_PLUS_ROOT == q == 3


def test_klm_and_fusion_probabilities():
    assert KLM_SIMPLE_SUCCESS == Fraction(1, mu) == Fraction(1, 4)
    assert FUSION_SUCCESS == Fraction(lam, mu) == Fraction(1, 2)
    assert FUSION_ATTEMPTS_PER_EDGE == Fraction(mu, lam) == 2
    assert KLM_ATTEMPTS_PER_SIMPLE_CZ == mu == 4


def test_w33_cluster_resource_counts():
    assert CLUSTER_QUBITS == V == 40
    assert CLUSTER_EDGES == E == q * (H1 - 1) == 240
    assert STABILIZER_WEIGHT == K + 1 == Phi3 == 13
    assert TOTAL_STABILIZER_SUPPORT == V * Phi3 == 520
    assert ORIENTED_STABILIZER_EDGE_INCIDENCES == DIRECTED == 480


def test_photonic_attempts_match_operator_counts():
    assert EXPECTED_FUSION_ATTEMPTS_FULL_CLUSTER == DIRECTED == 480
    assert EXPECTED_KLM_ATTEMPTS_FULL_EDGE_SET == TR_A3 == 960
    assert SEIDEL_ENERGY == E == 240


def test_dirac_and_tree_companions():
    assert DIRAC_DEGREE == 32
    assert DIRAC_EXP_PRODUCT == TR_A3 == 960
    assert TREE_EXP_2 == H1 == 81
    assert TREE_EXP_5 == Phi3 + Phi4 == 23
    assert HASHIMOTO_BRANCH == K - 1 == 11


def test_threshold_relations():
    assert (J * J_inv) % Phi3 == 1
    assert Phi6 + 1 == J_inv


def test_audit_checks_all_true():
    audit = photonic_mbqc_w33_bridge_audit()
    assert all(audit["checks"].values())
    assert audit["bridge_identities"]["fusion_hashimoto"] == "expected attempts to create all W33 edges by p=1/2 fusion is 2E=480, the Hashimoto carrier"
