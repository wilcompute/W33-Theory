"""Exact scalar Hessian at the balanced five-dimensional E6 attractor."""

import json

import numpy as np
import sympy as sp

from toe_20261114_e6_attractor_torus import DICTIONARY, OUT as TORUS, P, R

OUT = TORUS.with_name("toe_20261114_e6_attractor_hessian.json")


def calculate():
    cert, cubic, _, _, _ = R.load()
    fixture = json.loads(DICTIONARY.read_text(encoding="utf-8"))
    torus = json.loads(TORUS.read_text(encoding="utf-8"))
    signs = [-1 if i in fixture["coordinate_negative_sign_indices"] else 1 for i in range(27)]
    charge = sp.zeros(27, 1)
    for i in torus["native_coordinates"]:
        charge[i] = signs[i]
    assert charge.dot(charge) == 3
    assert sum(v*charge[i]*charge[j]*charge[k] for (i, j, k), v in cubic.items()) == 1

    symmetric = set()
    for records in cert["cubic_27"]["generators"]:
        a = sp.zeros(27)
        for i, j, v in records:
            a[i, j] = v
        sym = a + a.T
        if sym:
            symmetric.add(tuple(sym))
    matrices = [sp.Matrix(27, 27, entries) for entries in sorted(symmetric)]
    assert len(matrices) == 42
    coordinates = sp.Matrix.hstack(*(a.reshape(729, 1) for a in matrices))
    gram = coordinates.T * coordinates
    response = sp.Matrix.hstack(*(a*charge for a in matrices))
    assert response.T*charge == sp.zeros(42, 1)
    pushed = 4*response*gram.inv()*response.T
    projection = 3*pushed/4
    assert projection.T == projection and projection**2 == projection
    assert sp.trace(projection) == 14

    paulis = np.array([signs[i]*P(fixture["coordinate_to_pauli_label"][str(i)]) for i in range(27)])
    x = np.einsum("i,ijk->jk", np.array(charge, dtype=int).ravel(), paulis)
    projector_times_four = x + np.eye(8, dtype=int)
    assert np.array_equal(projector_times_four @ projector_times_four, 4*projector_times_four)
    assert projector_times_four.trace() == 8
    for column in response.columnspace():
        change = np.einsum("i,ijk->jk", np.array(column, dtype=int).ravel(), paulis)
        assert not np.any(projector_times_four @ change)
        assert not np.any(change @ projector_times_four)
        assert change.trace() == 0

    # A check against the one-parameter exact Taylor expansion for
    # nonzero symmetric responses of arbitrary integer combinations.
    for v in (sp.ones(42, 1), sp.Matrix(range(-21, 21))):
        direction = sp.Matrix(27, 27, coordinates*v)
        assert (charge.T*direction**2*charge)[0] == (v.T*response.T*response*v)[0]

    return dict(status="PASS", normalization="Frobenius trace on the 27 representation",
                balanced_cubic=1, norm_squared=3, positive_eigenvalue_over_abs_N_two_thirds="4/3",
                positive_directions=14, flat_directions=28,
                image="traceless quaternionic Hermitian operators on the complementary three-plane")


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result, flush=True)
