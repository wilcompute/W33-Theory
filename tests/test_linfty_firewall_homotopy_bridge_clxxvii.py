from PART_CLXXVII_LINFTY_FIREWALL_HOMOTOPY_BRIDGE import (
    Q,
    Q2,
    Q3,
    Q4,
    PHI3,
    PHI6,
    J,
    J_INV,
    RANK_SEED,
    TRIPLE_ALBERT,
    ROOT_SECTOR,
    FIREWALL_SECTOR,
    E6_RANK,
    E6_DIM,
    G0_DIM,
    E8_DIM,
    AFFINE_TRIADS,
    ORIENTED_AFFINE_TRIADS,
    FIBER_TRIADS,
    CUBIC_TRIADS,
    linfty_firewall_homotopy_audit,
)


def test_filtered_root_and_firewall_completion():
    assert ROOT_SECTOR == ORIENTED_AFFINE_TRIADS == 72
    assert FIREWALL_SECTOR == FIBER_TRIADS == Q2 == 9
    assert TRIPLE_ALBERT == ROOT_SECTOR + FIREWALL_SECTOR == Q4 == 81


def test_cubic_triads_and_orientation():
    assert AFFINE_TRIADS == 36
    assert FIBER_TRIADS == 9
    assert CUBIC_TRIADS == AFFINE_TRIADS + FIBER_TRIADS == 45
    assert 2 * AFFINE_TRIADS == ROOT_SECTOR


def test_e6_and_h1_closures_share_root_sector():
    assert ROOT_SECTOR + FIREWALL_SECTOR == 81
    assert ROOT_SECTOR + E6_RANK == E6_DIM == 78
    assert E6_RANK == RANK_SEED == 2 * Q == 6
    assert FIREWALL_SECTOR - E6_RANK == Q


def test_e8_z3_dimensions():
    assert G0_DIM == E6_DIM + J_INV == 86
    assert E8_DIM == G0_DIM + TRIPLE_ALBERT + TRIPLE_ALBERT == 248


def test_threshold_carrier_relations():
    assert (J * J_INV) % PHI3 == 1
    assert PHI6 + 1 == J_INV


def test_audit_checks_all_true():
    audit = linfty_firewall_homotopy_audit()
    assert all(audit["checks"].values())
    assert audit["bridge_identities"]["homotopy_repair"] == "l3 supplies the q^2=9 missing diagonal/fiber completion up to homotopy"
