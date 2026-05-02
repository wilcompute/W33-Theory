from PART_CLXXXIII_FIREWALL_JACOBIATOR_SUPPORT_BRIDGE import (
    Q,
    Q2,
    Q4,
    K,
    LAMBDA,
    PHI3,
    PHI6,
    J,
    J_INV,
    RANK_SEED,
    AFFINE_TRIADS,
    DELETED_FIBERS,
    CUBIC_TRIADS,
    ORIENTED_ROOTS,
    H1_CARRIER,
    E6_DIM,
    HASHIMOTO_BRANCH,
    DOOB_OPEN_TURNS,
    SOURCE_TOOLS,
    EXPECTED_TENSOR_ARTIFACTS,
    firewall_jacobiator_support_bridge_audit,
)


def test_support_dimensions():
    assert DELETED_FIBERS == Q2 == 9
    assert AFFINE_TRIADS == 36
    assert CUBIC_TRIADS == AFFINE_TRIADS + DELETED_FIBERS == 45
    assert ORIENTED_ROOTS == 2 * AFFINE_TRIADS == 72


def test_h1_and_e6_closures():
    assert H1_CARRIER == ORIENTED_ROOTS + DELETED_FIBERS == Q4 == 81
    assert E6_DIM == ORIENTED_ROOTS + RANK_SEED == 78
    assert RANK_SEED == 2 * Q == 6
    assert H1_CARRIER - E6_DIM == Q


def test_cct_echo_matches_firewall_sector():
    assert HASHIMOTO_BRANCH == K - 1 == 11
    assert DOOB_OPEN_TURNS == HASHIMOTO_BRANCH - LAMBDA == DELETED_FIBERS


def test_tool_and_artifact_registry():
    assert len(SOURCE_TOOLS) == 4
    assert "tools/compute_firewall_jacobiator_tensor.py" in SOURCE_TOOLS
    assert "tools/build_linfty_firewall_extension.py" in SOURCE_TOOLS
    assert len(EXPECTED_TENSOR_ARTIFACTS) == 6
    assert "artifacts/firewall_jacobiator_tensor.json" in EXPECTED_TENSOR_ARTIFACTS


def test_threshold_carrier_relations():
    assert PHI6 + 1 == J_INV
    assert (J * J_INV) % PHI3 == 1


def test_audit_checks_all_true():
    audit = firewall_jacobiator_support_bridge_audit()
    assert all(audit["checks"].values())
    assert audit["status"] == "structural audit; numerical tensor-rank artifact rerun still needed"
    assert audit["bridge_identities"]["l3_repair"] == "l3 is supported on the same 9 fiber triads and restores homotopy coherence"
