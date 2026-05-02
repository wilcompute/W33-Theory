from PART_CLXXIV_FANO_CAYLEY_ALBERT_E6_ALGEBRA import (
    Q,
    PHI3,
    PHI6,
    J,
    J_INV,
    RANK_SEED,
    HEPTAD_RESIDUES,
    RESIDUE_TO_INDEX,
    FANO_LINES_RESIDUES,
    ORIENTED_INDEX_LINES,
    basis_mul,
    add,
    mul,
    conjugate,
    norm_squared,
    associator,
    _basis,
    fano_cayley_albert_audit,
)


def test_heptad_and_carrier_dimensions():
    assert len(HEPTAD_RESIDUES) == PHI6 == 7
    assert 1 + PHI6 == J_INV == 8
    assert len(RESIDUE_TO_INDEX) == 7


def test_fano_lines_match_heptad_structure():
    assert len(FANO_LINES_RESIDUES) == 7
    assert len(ORIENTED_INDEX_LINES) == 7
    assert all(len(set(line)) == 3 for line in FANO_LINES_RESIDUES)


def test_imaginary_units_square_and_anticommute():
    for i in range(1, 8):
        assert basis_mul(i, i) == {0: -1}
    for i in range(1, 8):
        for j in range(1, 8):
            if i != j:
                assert add(basis_mul(i, j), basis_mul(j, i)) == {}


def test_basis_alternativity():
    basis = [_basis(i) for i in range(8)]
    for x in basis:
        for y in basis:
            assert associator(x, x, y) == {}
            assert associator(y, x, x) == {}


def test_sample_norm_multiplicativity():
    samples = [
        _basis(0),
        _basis(1),
        add(_basis(0), _basis(1)),
        add(_basis(2), _basis(3)),
        add(add(_basis(4), _basis(5)), _basis(0)),
        add(add(_basis(6), _basis(7)), _basis(1)),
    ]
    for x in samples:
        assert mul(x, conjugate(x)) == {0: norm_squared(x)}
        for y in samples:
            assert norm_squared(mul(x, y)) == norm_squared(x) * norm_squared(y)


def test_albert_and_e6_dimensions():
    assert 3 + 3 * (1 + PHI6) == Q ** 3 == 27
    assert Q ** 3 - 1 == 26
    assert 52 + (Q ** 3 - 1) == 78
    assert RANK_SEED + 72 == 78


def test_threshold_carrier_inverse():
    assert PHI6 + 1 == J_INV
    assert (J * J_INV) % PHI3 == 1


def test_audit_checks_all_true():
    audit = fano_cayley_albert_audit()
    assert all(audit["checks"].values())
    assert audit["algebra_layers"][2]["dimension"] == 27
    assert audit["algebra_layers"][5]["dimension"] == 78
