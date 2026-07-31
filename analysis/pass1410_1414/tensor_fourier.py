from __future__ import annotations

import sympy as sp

import _selector_five_frontiers_impl as ff
from pass1370_1374 import core

from .common import capture, matrix_stats, sha


def multiplicity_coordinates(Cinv, vector, slices):
    coefficient = Cinv * sp.Matrix(vector)
    out = []
    for start, _stop, n, degree in slices:
        matrix = sp.Matrix(n, n, lambda i, j: sp.cancel(coefficient[start + i * n + j]))
        out.append({
            "matrix_size": n,
            "irreducible_degree": degree,
            "matrix": [[[int(sp.Rational(x).p), int(sp.Rational(x).q)] for x in matrix.row(i)] for i in range(n)],
            "sha256": matrix_stats(matrix)["sha256"],
        })
    return out


def row_selector(rows, width=120):
    matrix = sp.zeros(len(rows), width)
    for i, row in enumerate(rows):
        matrix[i, row] = 1
    return matrix


def analyze():
    _public, cap = capture()
    g = cap["g"]
    blocks = core.matrix_units_full(g, cap["full_records"])

    tensor_columns = []
    inverse_rows = []
    block_records = []
    matrix_unit_columns = []
    slices = []
    cursor = 0

    for block_index, block in enumerate(blocks):
        n = int(block["n"])
        degree = int(block["m"])
        units = block["E"]
        e00 = ff.orbital_matrix(g, units[0][0])
        primitive_pivots = list(e00.rref()[1])
        assert len(primitive_pivots) == degree
        primitive_basis = e00[:, primitive_pivots]
        copies = []
        for a in range(n):
            translated = ff.orbital_matrix(g, units[a][0]) * primitive_basis
            assert translated.rank() == degree
            copies.append(translated)
        Ublock = sp.Matrix.hstack(*copies)
        dimension = n * degree
        assert Ublock.rank() == dimension
        tensor_columns.append(Ublock)

        inverse_pivots = list(Ublock.T.rref()[1])
        assert len(inverse_pivots) == dimension
        pivot_square = Ublock[inverse_pivots, :]
        central_projector = ff.orbital_matrix(g, cap["full_records"][block_index]["z"])
        Qblock = (pivot_square.inv() * row_selector(inverse_pivots) * central_projector).applyfunc(sp.cancel)
        assert Qblock * Ublock == sp.eye(dimension)
        inverse_rows.append(Qblock)

        flat = [units[i][j] for i in range(n) for j in range(n)]
        matrix_unit_columns.extend(flat)
        slices.append((cursor, cursor + n * n, n, degree))
        cursor += n * n
        block_records.append({
            "block_index": block_index,
            "multiplicity_space_dimension": n,
            "irreducible_degree": degree,
            "isotypic_dimension": dimension,
            "primitive_copy_pivots": primitive_pivots,
            "inverse_pivot_rows": inverse_pivots,
            "tensor_basis_sha256": matrix_stats(Ublock)["sha256"],
            "tensor_inverse_block_sha256": matrix_stats(Qblock)["sha256"],
            "matrix_unit_action": "E_ab acts as e_ab tensor I_degree in multiplicity-major ordering",
        })

    assert cursor == 83
    U = sp.Matrix.hstack(*tensor_columns)
    Uinv = sp.Matrix.vstack(*inverse_rows)
    assert U.shape == (120, 120) and Uinv.shape == (120, 120)
    assert Uinv * U == sp.eye(120)

    matrix_unit_transition = sp.Matrix.hstack(*matrix_unit_columns)
    assert matrix_unit_transition.shape == (83, 83) and matrix_unit_transition.det() != 0
    transition_inverse = matrix_unit_transition.inv()

    orbital_actions = []
    for orbital_index in range(83):
        unit = sp.zeros(83, 1)
        unit[orbital_index] = 1
        orbital_actions.append({
            "orbital_index": orbital_index,
            "blocks": multiplicity_coordinates(transition_inverse, unit, slices),
        })

    Acoord = sp.Matrix([g["A"][i, j] for i, j in g["reps"]])
    Dcoord = sp.Matrix([g["D"][i, j] for i, j in g["reps"]])
    s2, s4 = core.splitters(g)
    named = {
        "A": multiplicity_coordinates(transition_inverse, Acoord, slices),
        "D": multiplicity_coordinates(transition_inverse, Dcoord, slices),
        "S": multiplicity_coordinates(transition_inverse, s2 + s4, slices),
    }

    for name, vector in (("A", Acoord), ("D", Dcoord), ("S", s2 + s4)):
        operator = ff.orbital_matrix(g, vector)
        for block_index, (record, Ublock) in enumerate(zip(block_records, tensor_columns)):
            n = record["multiplicity_space_dimension"]
            degree = record["irreducible_degree"]
            data = named[name][block_index]["matrix"]
            multiplicity_matrix = sp.Matrix([[sp.Rational(*data[i][j]) for j in range(n)] for i in range(n)])
            assert operator * Ublock == Ublock * sp.kronecker_product(multiplicity_matrix, sp.eye(degree))

    action_payload = [
        {"orbital_index": item["orbital_index"], "block_hashes": [block["sha256"] for block in item["blocks"]]}
        for item in orbital_actions
    ]
    result = {
        "theorem": "Pass 1411 Deterministic Tensor-Factor Selector Fourier Transform",
        "ordering": "Mackey blocks in frozen matrix-unit order; multiplicity index first, with deterministic primitive-copy column pivots and inverse row pivots",
        "blocks": block_records,
        "block_dimensions": [record["isotypic_dimension"] for record in block_records],
        "tensor_basis_U": matrix_stats(U),
        "tensor_inverse_Uinv": matrix_stats(Uinv),
        "exact_inverse_verified": True,
        "inverse_constructed_blockwise_from_central_projectors": True,
        "all_83_orbital_multiplicity_actions_sha256": sha(action_payload),
        "all_83_orbital_multiplicity_actions": orbital_actions,
        "named_multiplicity_actions": named,
        "conclusion": "Every orbital operator acts as a multiplicity-space matrix tensored with the identity on the irreducible factor; deterministic pivots fix the repeated-copy gauge.",
        "boundary": "The pivot rule is canonical relative to the frozen matrix units and selector coordinate order.",
    }
    result["sha256"] = sha(result)
    return result
