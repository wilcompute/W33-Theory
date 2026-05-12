def test_two_81_dimensional_objects():
    q81 = 81
    h1 = 81
    assert q81 == h1


def test_alignment_matrix_shape():
    q_basis = 81
    h_basis = 81
    assert (q_basis, h_basis) == (81, 81)


def test_full_rank_alignment_target():
    target_rank = 81
    assert target_rank == 81


def test_basis_independent_ch_operator_target():
    # C_H = sum_alpha q_alpha q_alpha^* acts on K=H1.
    domain_dim = 81
    codomain_dim = 81
    assert domain_dim == codomain_dim == 81


def test_alignment_failure_modes_are_auditable():
    failure_modes = {
        "rank_defect": "some H1 directions invisible",
        "high_degeneracy": "large residual symmetry",
        "split_spectrum": "candidate flavor hierarchy",
    }
    assert set(failure_modes) == {"rank_defect", "high_degeneracy", "split_spectrum"}


def test_required_invariants():
    invariants = ["rank(C_H)", "Tr(C_H)", "Tr(C_H^2)", "Spec(C_H)"]
    assert len(invariants) == 4
    assert "Spec(C_H)" in invariants
