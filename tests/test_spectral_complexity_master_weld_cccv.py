from fractions import Fraction

from exploration.PART_CCCV_SPECTRAL_COMPLEXITY_MASTER_WELD import (
    q,
    V,
    K,
    Phi3,
    Phi4,
    Phi6,
    J,
    J_inv,
    EW,
    ALBERT,
    H1,
    THETA_W,
    THETA_COMP,
    LP_ALPHA,
    LP_OMEGA,
    FIEDLER,
    LAPLACIAN_RADIUS,
    MULT_R,
    MULT_S,
    TREE_EXP_2,
    TREE_EXP_5,
    TREE_EXP_SUM,
    TREE_EXP_DIFF,
    KIRCHHOFF_INDEX,
    NORMALIZED_WEIGHTED_LOW,
    NORMALIZED_WEIGHTED_HIGH,
    krein,
    spectral_complexity_master_weld_audit,
)


def test_theta_delsarte_fiedler_lock():
    assert THETA_W == LP_ALPHA == FIEDLER == Phi4 == 10
    assert THETA_COMP == LP_OMEGA == EW == 4
    assert THETA_W * THETA_COMP == V == 40


def test_laplacian_pair_identities():
    assert LAPLACIAN_RADIUS == EW ** 2 == 16
    assert FIEDLER * LAPLACIAN_RADIUS == V * EW == 160
    assert FIEDLER + LAPLACIAN_RADIUS == 2 * Phi3 == 26
    assert LAPLACIAN_RADIUS - FIEDLER == 2 * q == 6


def test_normalized_laplacian_weighted_split():
    assert NORMALIZED_WEIGHTED_LOW == Fraction(MULT_R * FIEDLER, K) == 20
    assert NORMALIZED_WEIGHTED_HIGH == Fraction(MULT_S * LAPLACIAN_RADIUS, K) == 20
    assert NORMALIZED_WEIGHTED_LOW + NORMALIZED_WEIGHTED_HIGH == V


def test_spanning_tree_factorization_and_exponents():
    assert TREE_EXP_2 == H1 == q ** 4 == 81
    assert TREE_EXP_5 == ALBERT - EW == 23
    assert TREE_EXP_SUM == J_inv * Phi3 == 104
    assert TREE_EXP_DIFF == 2 * ALBERT + EW == 58
    assert (2 ** TREE_EXP_2) * (5 ** TREE_EXP_5) == (10 ** MULT_R) * (16 ** MULT_S) // V


def test_kirchhoff_index():
    assert KIRCHHOFF_INDEX == Fraction(V, 1) * (Fraction(MULT_R, FIEDLER) + Fraction(MULT_S, LAPLACIAN_RADIUS))
    assert KIRCHHOFF_INDEX == Fraction(267, 2)


def test_krein_dual_seed():
    assert 3 * krein["q2_11"] == V
    assert 3 * krein["q2_22"] == THETA_W
    assert 1 + krein["q0_11"] + krein["q0_22"] == V
    assert krein["q0_11"] - krein["q0_22"] == q ** 2
    assert 3 * (krein["q1_11"] + krein["q1_22"]) == J_inv ** 2 == EW ** 3


def test_threshold_carrier_relations():
    assert (J * J_inv) % Phi3 == 1
    assert Phi6 + 1 == J_inv


def test_audit_checks_all_true():
    audit = spectral_complexity_master_weld_audit()
    assert all(audit["checks"].values())
    assert audit["bridge_identities"]["tree_complexity"] == "tau(W)=10^24*16^15/40=2^81*5^23"
