from PART_CLXXXIV_HEPTAD_PROJECTOR_CAYLEY_SIGN_BRIDGE import (
    Q,
    Q3,
    PHI3,
    PHI6,
    J,
    J_INV,
    K,
    RANK_SEED,
    CSASZAR_PROJECTORS,
    SZILASSI_PROJECTORS,
    PROJECTOR_HEPTAD,
    MEAN_LINE,
    CENTERED_SHELL,
    CSASZAR_CENTERED,
    SZILASSI_CENTERED,
    FAMILY_SEPARATION,
    BIVECTOR_DIM_4,
    ORIENTATION_DOUBLE,
    CAYLEY_CARRIER,
    FANO_PAIRS,
    FANO_LINES,
    ALBERT_DIM,
    HEPTAD_RESIDUES,
    FANO_LINES_RESIDUES,
    SOURCE_TOOLS,
    EXPECTED_PROJECTOR_ARTIFACTS,
    heptad_projector_cayley_sign_bridge_audit,
)


def test_projector_heptad_family_split():
    assert CSASZAR_PROJECTORS == J == 5
    assert SZILASSI_PROJECTORS == Q - 1 == 2
    assert PROJECTOR_HEPTAD == CSASZAR_PROJECTORS + SZILASSI_PROJECTORS == PHI6 == 7


def test_centered_and_full_refinements():
    assert CENTERED_SHELL == PROJECTOR_HEPTAD - MEAN_LINE == RANK_SEED == 6
    assert CSASZAR_CENTERED + SZILASSI_CENTERED + FAMILY_SEPARATION == CENTERED_SHELL
    assert CSASZAR_CENTERED + (SZILASSI_CENTERED + FAMILY_SEPARATION + MEAN_LINE) == PROJECTOR_HEPTAD


def test_bivector_orientation_and_cayley_completion():
    assert BIVECTOR_DIM_4 == CENTERED_SHELL == 6
    assert ORIENTATION_DOUBLE == 2 * CENTERED_SHELL == K == 12
    assert CAYLEY_CARRIER == 1 + PROJECTOR_HEPTAD == J_INV == 8
    assert ALBERT_DIM == 3 + 3 * CAYLEY_CARRIER == Q3 == 27


def test_fano_pair_coverage():
    assert len(HEPTAD_RESIDUES) == 7
    assert len(FANO_LINES_RESIDUES) == FANO_LINES == 7
    pairs = set()
    for a, b, c in FANO_LINES_RESIDUES:
        pairs.update({tuple(sorted((a, b))), tuple(sorted((a, c))), tuple(sorted((b, c)))})
    assert len(pairs) == FANO_PAIRS == 21


def test_tool_and_artifact_registry():
    assert len(SOURCE_TOOLS) == 3
    assert "exploration/w33_toroidal_heptad_projector_bridge.py" in SOURCE_TOOLS
    assert EXPECTED_PROJECTOR_ARTIFACTS == ["data/w33_toroidal_heptad_projector_bridge_summary.json"]


def test_threshold_carrier_inverse():
    assert (J * J_INV) % PHI3 == 1


def test_audit_checks_all_true():
    audit = heptad_projector_cayley_sign_bridge_audit()
    assert all(audit["checks"].values())
    assert audit["status"] == "structural sign-capacity audit; projector Gram/sign extraction artifact rerun still needed"
    assert audit["bridge_identities"]["orientation_to_signs"] == "2*6=12 gives the oriented sign/phase double cover needed for Cayley multiplication"
