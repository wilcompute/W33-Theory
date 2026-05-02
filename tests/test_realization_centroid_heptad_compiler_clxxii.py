from PART_CLXXII_REALIZATION_CENTROID_HEPTAD_COMPILER import (
    Q,
    QP1,
    RANK_SEED,
    PHI3,
    PHI6,
    J,
    J_INV,
    TETRA_SEED,
    CS_COUNT,
    SZ_COUNT,
    HEPTAD_COUNT,
    GEOMETRIC_TOTAL_WITH_TETRA,
    CENTERED_SHELL_DIM,
    CS_CENTERED_RANK,
    SZ_CENTERED_RANK,
    FAMILY_SEPARATION_RANK,
    realization_centroid_heptad_audit,
)


def test_heptad_counts_and_carrier_completion():
    assert CS_COUNT == J == 5
    assert SZ_COUNT == Q - 1 == 2
    assert HEPTAD_COUNT == PHI6 == 7
    assert GEOMETRIC_TOTAL_WITH_TETRA == J_INV == 8


def test_centered_shell_dimensions():
    assert CENTERED_SHELL_DIM == RANK_SEED == 6
    assert CS_CENTERED_RANK == QP1 == 4
    assert SZ_CENTERED_RANK == 1
    assert FAMILY_SEPARATION_RANK == 1
    assert CS_CENTERED_RANK + SZ_CENTERED_RANK + FAMILY_SEPARATION_RANK == CENTERED_SHELL_DIM


def test_full_refinement_and_mean_line():
    assert 1 + CENTERED_SHELL_DIM == HEPTAD_COUNT
    assert CS_CENTERED_RANK + (SZ_CENTERED_RANK + FAMILY_SEPARATION_RANK + 1) == HEPTAD_COUNT


def test_threshold_carrier_inverse_and_step():
    assert (J * J_INV) % PHI3 == 1
    assert PHI6 + TETRA_SEED == J_INV


def test_audit_checks_all_true():
    audit = realization_centroid_heptad_audit()
    assert all(audit["checks"].values())
    assert audit["operator_heptad_dictionary"]["centered_rank_split"] == "4+1+1=6"
