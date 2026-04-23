from scripts.w33_qutrit_operator_algebra import (
    build_two_qutrit_weyl_basis,
    summarize_canonical_projective_hamiltonian,
    verify_commutator_phase_matches_symplectic,
    verify_full_weyl_product_law,
    verify_selected_symplectic_generators,
)


def test_full_two_qutrit_weyl_basis_closes_exactly() -> None:
    basis = build_two_qutrit_weyl_basis()
    assert len(basis) == 81
    assert verify_full_weyl_product_law(basis) is True
    assert verify_commutator_phase_matches_symplectic() is True


def test_selected_symplectic_generators_preserve_projective_pauli_geometry() -> None:
    checks = verify_selected_symplectic_generators()
    assert tuple(checks.keys()) == ("S1", "T1", "S2", "T2", "SWAP")
    assert all(record["preserves_symplectic_form"] for record in checks.values())
    assert all(record["preserves_projective_points"] for record in checks.values())
    assert all(record["preserves_commutation_graph"] for record in checks.values())


def test_canonical_hamiltonian_matches_line_incidence_laplacian() -> None:
    summary = summarize_canonical_projective_hamiltonian()
    assert summary["point_count"] == 40
    assert summary["line_count"] == 40
    assert summary["line_size"] == 4
    assert summary["lines_per_point"] == 4
    assert summary["incidence_identity_holds"] is True
    assert summary["laplacian_matches_incidence_form"] is True
    assert summary["laplacian_eigenpairs"] == ((0, 1), (10, 24), (16, 15))
    assert summary["positive_semidefinite"] is True
    assert summary["kernel_dimension"] == 1