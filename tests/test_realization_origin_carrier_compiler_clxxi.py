from PART_CLXXI_REALIZATION_ORIGIN_CARRIER_COMPILER import (
    Q,
    PHI3,
    PHI6,
    J,
    J_INV,
    BINARY_DUALITY,
    TETRA_SEED,
    CSASZAR_REALIZATIONS,
    SZILASSI_REALIZATIONS,
    TOROIDAL_GEOMETRIC_REALIZATIONS,
    FULL_TRIAD_GEOMETRIC_COUNT,
    COMBINATORIAL_TYPE_COUNT,
    FANO_ORIGIN,
    DIRECTION_PAIRS,
    realization_origin_carrier_audit,
)


def test_realization_counts_generate_phi6_and_carrier():
    assert CSASZAR_REALIZATIONS == J == 5
    assert SZILASSI_REALIZATIONS == BINARY_DUALITY == Q - 1 == 2
    assert TOROIDAL_GEOMETRIC_REALIZATIONS == PHI6 == 7
    assert FULL_TRIAD_GEOMETRIC_COUNT == J_INV == 8


def test_combinatorial_vs_geometric_counts():
    assert COMBINATORIAL_TYPE_COUNT == PHI6 == 7
    assert FULL_TRIAD_GEOMETRIC_COUNT - COMBINATORIAL_TYPE_COUNT == 1
    assert TETRA_SEED + CSASZAR_REALIZATIONS + SZILASSI_REALIZATIONS == 8
    assert TETRA_SEED + CSASZAR_REALIZATIONS + 1 == 7


def test_carrier_transition_identities():
    assert J_INV == J + Q == 8
    assert J_INV == PHI6 + TETRA_SEED == 8
    assert PHI6 == J + (Q - 1) == 7
    assert (J * J_INV) % PHI3 == 1


def test_fano_origin_decomposition():
    all_pair_points = [p for _, pair, _ in DIRECTION_PAIRS for p in pair]
    assert FANO_ORIGIN == 1
    assert len(set(all_pair_points)) == 6
    assert FANO_ORIGIN not in all_pair_points
    assert len({FANO_ORIGIN, *all_pair_points}) == 7
    assert {tuple(pair) for _, pair, _ in DIRECTION_PAIRS} == {(5, 3), (12, 6), (8, 9)}


def test_audit_checks_all_true():
    audit = realization_origin_carrier_audit()
    assert all(audit["checks"].values())
    assert audit["bridge_identities"]["full_geometric_triad"] == "1+5+2=8=J^{-1}"
