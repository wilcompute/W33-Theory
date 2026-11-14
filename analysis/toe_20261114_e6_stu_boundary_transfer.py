"""Exact boundary and horizon tangent ranks for unequal electric STU charges."""

import json
from fractions import Fraction

import sympy as sp

from toe_20261114_e6_attractor_torus import DICTIONARY, OUT as TORUS, R

OUT = TORUS.with_name("toe_20261114_e6_stu_boundary_transfer.json")


def flatten_columns(matrices):
    return sp.Matrix.hstack(*(a.reshape(729, 1) for a in matrices))


def rank(matrix):
    return matrix.to_DM().rank()


def calculate():
    cert, cubic, _, _, _ = R.load()
    fixture = json.loads(DICTIONARY.read_text(encoding="utf-8"))
    torus = json.loads(TORUS.read_text(encoding="utf-8"))
    triad = torus["native_coordinates"]
    incidence = sp.Matrix([[int(i in term) for i in range(27)] for term in sorted(cubic)])
    diagonal_basis = sp.Matrix.hstack(*incidence.nullspace())
    projector = diagonal_basis * (diagonal_basis.T * diagonal_basis).inv() * diagonal_basis.T
    weights = projector[:, triad[:2]] * projector[triad[:2], triad[:2]].inv()

    algebra = []
    for records in cert["cubic_27"]["generators"]:
        generator = sp.zeros(27)
        for i, j, value in records:
            generator[i, j] = value
        algebra.append(generator)
    algebra_columns = flatten_columns(algebra)
    assert rank(algebra_columns) == 78
    st = sp.Matrix.hstack(*(sp.diag(*weights[:, j]).reshape(729, 1) for j in range(2)))
    assert rank(st) == 2

    rows = []
    for magnitudes, common, expected in [((1, 64, 4096), 64, 40),
                                         ((1, 1, 262144), 64, 36),
                                         ((1, 1, 1), 1, 28)]:
        charge = sp.zeros(27, 1)
        for i, x in zip(triad, magnitudes, strict=True):
            charge[i] = -x if i in fixture["coordinate_negative_sign_indices"] else x
        stabilizer = sp.Matrix.hstack(*(a*charge for a in algebra)).nullspace()
        assert len(stabilizer) == 52
        basis = [sp.Matrix(27, 27, algebra_columns*v) for v in stabilizer]

        factors = [Fraction(common, x) for x in magnitudes]
        assert factors[0]*factors[1]*factors[2] == 1
        diagonal = sp.diag(*(sp.Rational(factors[0])**u * sp.Rational(factors[1])**v
                             for u, v in weights.tolist()))
        assert all(abs((diagonal*charge)[i]) == common for i in triad)
        inverse = diagonal.inv()
        horizon_basis = [diagonal*a*inverse for a in basis]
        assert all(a*diagonal*charge == sp.zeros(27, 1) for a in horizon_basis)
        boundary = flatten_columns([a+a.T for a in basis])
        horizon = flatten_columns([a+a.T for a in horizon_basis])
        assert rank(boundary) == expected
        assert rank(horizon) == 28
        assert rank(boundary.col_join(horizon)) == expected
        assert rank(boundary.row_join(st)) == expected+2
        assert rank(horizon.row_join(st)) == 30
        rows.append(dict(charges=magnitudes, balanced_magnitude=common,
                         stabilizer_dimension=len(basis), boundary_stabilizer_rank=expected,
                         horizon_stabilizer_rank=28, augmented_boundary_rank=expected+2,
                         kernel_dimension_within_augmented_boundary=expected+2-28))
    return dict(status="PASS", cases=rows)


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result, flush=True)
