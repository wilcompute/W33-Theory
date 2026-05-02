from PART_CLXXXVI_SPORADIC_MASTER_LADDER_INJECTION import (
    Q,
    Q2,
    Q4,
    V,
    K,
    LAM,
    MU,
    F,
    E,
    PHI3,
    PHI4,
    PHI6,
    PHI12,
    J,
    J_INV,
    E6_DIM,
    A2_DIM,
    G0_DIM,
    E8_DIM,
    TAU,
    ALPHA_INV,
    V_SUZ,
    K_SUZ,
    LAM_SUZ,
    MU_SUZ,
    F_SUZ,
    G_SUZ,
    CHI1_MONSTER,
    J_COEFF_1,
    J_CONSTANT,
    LEECH_KISSING,
    MONSTER_FIRST_SIX_EXPONENT_SUM,
    FI22_MIN_REP,
    TH_MIN_REP,
    CO1_I3_POWER_OF_TWO,
    sporadic_master_ladder_injection_audit,
)


def test_master_atoms_in_sporadic_layer():
    assert (PHI6, J_INV, Q ** 3, Q4, E6_DIM, E8_DIM) == (7, 8, 27, 81, 78, 248)


def test_tau_and_suzuki_injection():
    assert TAU == K * Q * PHI6 == 252
    assert V_SUZ == PHI6 * TAU + LAM * Q2 == 1782
    assert K_SUZ == Q * ALPHA_INV + (Q + 2) == 416
    assert LAM_SUZ == (Q + 2) ** LAM * MU == 100
    assert MU_SUZ == LAM * Q2 * MU + F == 96
    assert 1 + F_SUZ + G_SUZ == V_SUZ


def test_moonshine_injection():
    assert CHI1_MONSTER == (V + PHI6) * (V + K + PHI6) * (PHI12 - LAM) == 196883
    assert (V + PHI6, V + K + PHI6, PHI12 - LAM) == (47, 59, 71)
    assert J_COEFF_1 == TAU * (V * (V - 1) // 2) + 4 * Q4 == 196884
    assert J_COEFF_1 == CHI1_MONSTER + 1
    assert J_COEFF_1 - LEECH_KISSING == 4 * Q4 == 324
    assert J_CONSTANT == Q * E + F == 744


def test_g0_and_representation_hooks():
    assert MONSTER_FIRST_SIX_EXPONENT_SUM == G0_DIM == E6_DIM + A2_DIM == 86
    assert FI22_MIN_REP == E6_DIM == 78
    assert TH_MIN_REP == E8_DIM == 248
    assert CO1_I3_POWER_OF_TWO == 2 ** J_INV == 256


def test_threshold_carrier_relations():
    assert (J * J_INV) % PHI3 == 1
    assert PHI6 + 1 == J_INV


def test_audit_checks_all_true():
    audit = sporadic_master_ladder_injection_audit()
    assert all(audit["checks"].values())
    assert audit["careful_boundary"]["not_proved_here"] == "classification of sporadics from W33, causal derivation of Monster, or full Moonshine theorem"
