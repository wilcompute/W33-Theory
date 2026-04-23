from scripts.w3q_scaling_family import (
    q_values_with_edge_count,
    w3q_canonical_hamiltonian_spectrum,
    w3q_parameters,
    w3q_record,
)


def test_q3_record_matches_w33_kernel_data() -> None:
    record = w3q_record(3)
    assert record["srg_parameters"] == (40, 12, 2, 4)
    assert record["edge_count"] == 240
    assert record["line_count"] == 40
    assert record["line_size"] == 4
    assert record["lines_per_point"] == 4
    assert record["local_shell_sizes"] == {"neighbors": 12, "nonneighbors": 27}
    assert record["complement_degree"] == 27
    assert record["hoffman_bounds"] == {"clique_bound": 4, "coclique_bound": 10}
    assert record["adjacency_eigenvalues"] == (2, -4)
    assert record["adjacency_multiplicities"] == (24, 15)
    assert record["canonical_hamiltonian_eigenpairs"] == ((0, 1), (10, 24), (16, 15))


def test_first_family_members_match_known_parameters() -> None:
    expected = {
        2: (15, 6, 1, 3),
        3: (40, 12, 2, 4),
        4: (85, 20, 3, 5),
        5: (156, 30, 4, 6),
        7: (400, 56, 6, 8),
    }
    for q_value, parameters in expected.items():
        assert w3q_parameters(q_value) == parameters


def test_canonical_hamiltonian_generalizes_along_the_family() -> None:
    assert w3q_canonical_hamiltonian_spectrum(2) == ((0, 1), (5, 9), (9, 5))
    assert w3q_canonical_hamiltonian_spectrum(3) == ((0, 1), (10, 24), (16, 15))
    assert w3q_canonical_hamiltonian_spectrum(5) == ((0, 1), (26, 90), (36, 65))


def test_only_q3_has_edge_count_240_in_small_scan() -> None:
    assert q_values_with_edge_count(240, 2, 29) == (3,)