"""Exact shared M/IIB coordinate extensions and the first-jet gauge image."""

import json
from itertools import combinations_with_replacement
from pathlib import Path

import numpy as np

import toe_20261113_E6_exft_generalized_closure_affine as exft
from toe_20261113_E6_exact_parabolic_stabilizer import rank_mod


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/toe_20261113_exft_common_four.json"
IDENTITY = np.eye(27, dtype=np.int64)


def complement(indices):
    return [i for i in range(27) if i not in indices]


def preserves(matrix, indices):
    return not matrix[np.ix_(complement(indices), indices)].any()


def jet_image(tensor, y_tensor, section):
    # D sends a section-supported Jacobian to its algebraic action on vectors.
    jets = np.array([
        y_tensor[:, s, :, l] - np.outer(IDENTITY[:, l], IDENTITY[s])
        for s in section for l in range(27)
    ])
    flat = jets.reshape(len(jets), -1)
    # G sends a covector Hessian to the Jacobian of its trivial parameter.
    exact_jets = []
    for i, j in combinations_with_replacement(range(len(section)), 2):
        for k in range(27):
            jacobian = np.zeros((len(section), 27), dtype=np.int64)
            jacobian[i] = tensor[:, section[j], k]
            jacobian[j] = tensor[:, section[i], k]
            exact_jets.append(jacobian.ravel())
    exact_jets = np.array(exact_jets)
    assert not (exact_jets @ flat).any()
    rank, trivial_rank = rank_mod(flat), rank_mod(exact_jets)
    # Finite-field ranks are lower bounds over R. Zero composition makes
    # their sum an upper bound of the same size, certifying both exactly.
    assert rank + trivial_rank == len(jets)
    assert all(preserves(j.T, section) for j in jets)
    anchor = np.array([j[np.ix_(section, section)].ravel() for j in jets])
    anchor_rank = rank_mod(anchor)
    assert anchor_rank == len(section)**2
    return jets, dict(gradient_parameters=len(jets), vertical_action_rank=rank,
                      exact_parameter_jacobian_rank=trivial_rank,
                      anchor_linear_action_rank=anchor_rank,
                      anchor_zero_vertical_action_rank=rank-anchor_rank,
                      effective_affine_operator_dimension=rank+len(section))


def calculate():
    tensor, y_tensor, iib, m = exft.setup()
    shared = tuple(sorted(set(iib) & set(m)))
    assert len(shared) == 4
    # Each contraction on a coordinate section is a signed partial permutation.
    # This makes the common annihilator a coordinate span for arbitrary vectors.
    for s in shared:
        nonzeros = tensor[s] != 0
        assert (nonzeros.sum(axis=0) <= 1).all()
        assert (nonzeros.sum(axis=1) <= 1).all()
    annihilator = tuple(i for i in range(27) if not tensor[i, shared, :].any())
    line = tuple(i for i in iib if i not in shared)
    plane = tuple(i for i in m if i not in shared)
    transverse = line + plane
    assert set(annihilator) == set(shared + transverse)
    terms = []
    for i, j in combinations_with_replacement(transverse, 2):
        for k in np.flatnonzero(tensor[i, j]):
            terms.append((i, j, int(k), int(tensor[i, j, k])))
    assert [(i, j) for i, j, _, _ in terms] == [(line[0], j) for j in plane]
    assert len({k for _, _, k, _ in terms}) == 2

    basis = np.load(ROOT / "artifacts/e6_27rep_basis_export/E6_basis_78.npy")
    assert not basis.imag.any() and np.array_equal(basis.real, basis.real.astype(int))
    basis = basis.real.astype(np.int64)
    # The stabilizer conditions pick individual root matrices. The
    # supports of distinct off-diagonal matrices are disjoint.
    assert ((basis != 0).sum(axis=0)[~np.eye(27, dtype=bool)] <= 1).all()
    stabilizer = [g for g in basis if preserves(g.T, shared)]
    joint = [g for g in basis if preserves(g.T, iib) and preserves(g.T, m)]
    assert len(stabilizer) == len(joint) == 49
    assert all(preserves(g.T, iib) and preserves(g.T, m) for g in stabilizer)
    ambient = stabilizer + [IDENTITY]
    flat_ambient = np.array(ambient).reshape(len(ambient), -1)
    assert rank_mod(flat_ambient) == 50

    for g in ambient:
        assert preserves(g.T, annihilator)
    quotient = [g.T[np.ix_(transverse, transverse)] for g in ambient]
    assert all(not a[0, 1:].any() and not a[1:, 0].any() for a in quotient)
    assert rank_mod([a.ravel() for a in quotient]) == 5

    controls = {}
    for name, section in (("one", shared[:1]), ("two", shared[:2]),
                          ("shared_four", shared), ("IIB", iib), ("M", m)):
        jets, controls[name] = jet_image(tensor, y_tensor, section)
        if name == "shared_four":
            for g in jets:
                assert preserves(g.T, annihilator)
                assert not g[np.ix_(transverse, transverse)].any()
            # Exact rational inclusion in the ambient algebra, not a
            # modular rank test for membership.
            import sympy as sp
            ambient_matrix = sp.Matrix(flat_ambient.T.tolist())
            _, independent_rows = ambient_matrix.T.rref()
            chart = ambient_matrix[list(independent_rows), :]
            flat_jets = sp.Matrix(jets.reshape(len(jets), -1).T.tolist())
            assert ambient_matrix * chart.inv() * flat_jets[list(independent_rows), :] == flat_jets

    # Constant affine parameters act only through the anchor. The image
    # of linear trivial potentials is the orthogonal complement of A.
    linear_potentials = np.concatenate([tensor[:, s, :] for s in shared], axis=1)
    assert not linear_potentials[list(annihilator), :].any()
    exact_constants = rank_mod(linear_potentials)
    assert exact_constants == 27-len(annihilator)
    invisible_constants = 27-len(shared)
    residual_constants = invisible_constants-exact_constants
    assert residual_constants == 3
    # For a nonzero Fourier covector, test the anchor and algebraic
    # parts of the differential-operator symbol at a coordinate covector.
    s = shared[0]
    symbol = np.array([
        np.r_[IDENTITY[s, l], (y_tensor[:, s, :, l]
                              - np.outer(IDENTITY[:, l], IDENTITY[s])).ravel()]
        for l in range(27)
    ])
    fourier_potential = tensor[:, s, :]
    assert not (fourier_potential.T @ symbol).any()
    fourier_rank, potential_rank = rank_mod(symbol), rank_mod(fourier_potential)
    assert (fourier_rank, potential_rank) == (17, 10)
    assert controls["shared_four"]["vertical_action_rank"] == 45
    return dict(status="PASS", shared=shared, annihilator=annihilator, iib_transverse=line,
                m_transverse=plane, mixed_cubic_terms=terms, joint_stabilizer_dimension=49,
                conformal_stabilizer_dimension=50, transverse_quotient_dimension=5,
                jets=controls, constant_parameter_cohomology=dict(
                    invisible_constants=invisible_constants, exact_constants=exact_constants,
                    dimension=residual_constants, representatives=transverse),
                nonzero_fourier_symbol=dict(operator_rank=fourier_rank, exact_rank=potential_rank),
                periodic_torus_invisible_parameter_cohomology=invisible_constants)


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)
