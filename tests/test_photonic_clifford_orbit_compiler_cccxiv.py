from exploration.PART_CCCXIV_PHOTONIC_CLIFFORD_ORBIT_COMPILER import (
    q,
    lam,
    mu,
    V,
    Phi3,
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
    QUTRIT_DIM,
    TWO_QUTRIT_PAULI_MONOMIALS,
    PROJECTIVE_OBSERVABLES,
    CLIFFORD_ORDER,
    PER_VERTEX_ORBIT,
    PER_EDGE_ORBIT,
    PER_DIRECTED_ORBIT,
    PER_TRIANGLE_TRACE_ORBIT,
    PER_TRIANGLE_ORBIT,
    FUSION_ATTEMPTS,
    KLM_ATTEMPTS_ALL_EDGES,
    STABILIZER_WEIGHT,
    STABILIZER_TOTAL_SUPPORT,
    photonic_clifford_orbit_compiler_audit,
)


def test_qutrit_phase_space_projectivizes_to_w33():
    assert QUTRIT_DIM == q == 3
    assert TWO_QUTRIT_PAULI_MONOMIALS == H1 == q ** 4 == 81
    assert PROJECTIVE_OBSERVABLES == (q ** 4 - 1) // (q - 1) == V == 40


def test_clifford_automorphism_order_and_vertex_resolution():
    assert CLIFFORD_ORDER == 51840
    assert CLIFFORD_ORDER == V * (EW ** 2) * H1
    assert PER_VERTEX_ORBIT == CLIFFORD_ORDER // V == EW ** 2 * H1 == 1296


def test_physical_resource_orbit_resolutions():
    assert PER_EDGE_ORBIT == CLIFFORD_ORDER // E == J_inv * ALBERT == 216
    assert PER_DIRECTED_ORBIT == CLIFFORD_ORDER // DIRECTED == mu * ALBERT == 108
    assert PER_TRIANGLE_TRACE_ORBIT == CLIFFORD_ORDER // TR_A3 == lam * ALBERT == 54
    assert PER_TRIANGLE_ORBIT == CLIFFORD_ORDER // TRIANGLES == mu * H1 == 324


def test_photonic_resources():
    assert FUSION_ATTEMPTS == DIRECTED == 480
    assert KLM_ATTEMPTS_ALL_EDGES == TR_A3 == 960
    assert STABILIZER_WEIGHT == Phi3 == 13
    assert STABILIZER_TOTAL_SUPPORT == V * Phi3 == 520


def test_edge_triangle_and_threshold_relations():
    assert E == q * (H1 - 1) == 240
    assert DIRECTED == 2 * E == 480
    assert TR_A3 == 960
    assert (J * J_inv) % Phi3 == 1
    assert Phi6 + 1 == J_inv


def test_audit_checks_all_true():
    audit = photonic_clifford_orbit_compiler_audit()
    assert all(audit["checks"].values())
    assert audit["bridge_identities"]["fusion_resolution"] == "|Sp|/480=mu q^3=108"
