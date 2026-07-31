from __future__ import annotations

import numpy as np
import sympy as sp

import _selector_five_frontiers_impl as ff
from pass1370_1374 import core

from .common import capture, matrix_stats, sha


def multiplicity_coordinates(Cinv, vector, slices):
    coeff = Cinv * sp.Matrix(vector)
    out = []
    for start, stop, n, degree in slices:
        M = sp.Matrix(n, n, lambda i, j: sp.cancel(coeff[start + i * n + j]))
        out.append({
            "matrix_size": n,
            "irreducible_degree": degree,
            "matrix": [[[int(sp.Rational(x).p), int(sp.Rational(x).q)] for x in M.row(i)] for i in range(n)],
            "sha256": matrix_stats(M)["sha256"],
        })
    return out


def analyze():
    _public, cap = capture()
    g = cap["g"]
    blocks = core.matrix_units_full(g, cap["full_records"])

    tensor_columns = []
    block_records = []
    matrix_unit_columns = []
    slices = []
    cursor = 0

    for bi, block in enumerate(blocks):
        n = int(block["n"])
        degree = int(block["m"])
        E = block["E"]
        e00 = ff.orbital_matrix(g, E[0][0])
        pivots = list(e00.rref()[1])
        assert len(pivots) == degree
        W = e00[:, pivots]
        local = []
        for a in range(n):
            Ea0 = ff.orbital_matrix(g, E[a][0])
            translated = Ea0 * W
            assert translated.rank() == degree
            local.append(translated)
        Ublock = sp.Matrix.hstack(*local)
        assert Ublock.rank() == n * degree
        tensor_columns.append(Ublock)

        flat = [E[i][j] for i in range(n) for j in range(n)]
        matrix_unit_columns.extend(flat)
        slices.append((cursor, cursor + n * n, n, degree))
        cursor += n * n
        block_records.append({
            "block_index": bi,
            "multiplicity_space_dimension": n,
            "irreducible_degree": degree,
            "isotypic_dimension": n * degree,
            "primitive_copy_pivots": pivots,
            "tensor_basis_sha256": matrix_stats(Ublock)["sha256"],
            "matrix_unit_action": "E_ab acts as e_ab tensor I_degree in multiplicity-major ordering",
        })

    assert cursor == 83
    U = sp.Matrix.hstack(*tensor_columns)
    assert U.shape == (120, 120) and U.rank() == 120
    Uinv = U.inv()
    assert Uinv * U == sp.eye(120)

    C = sp.Matrix.hstack(*matrix_unit_columns)
    assert C.shape == (83, 83) and C.det() != 0
    Cinv = C.inv()

    orbital_actions = []
    for k in range(83):
        unit = sp.zeros(83, 1)
        unit[k] = 1
        orbital_actions.append({
            "orbital_index": k,
            "blocks": multiplicity_coordinates(Cinv, unit, slices),
        })

    Acoord = sp.Matrix([g["A"][i, j] for i, j in g["reps"]])
    Dcoord = sp.Matrix([g["D"][i, j] for i, j in g["reps"]])
    s2, s4 = core.splitters(g)
    named = {
        "A": multiplicity_coordinates(Cinv, Acoord, slices),
        "D": multiplicity_coordinates(Cinv, Dcoord, slices),
        "S": multiplicity_coordinates(Cinv, s2 + s4, slices),
    }

    # Independent exact check on the three named operators in the tensor basis.
    starts = np.cumsum([0] + [r["isotypic_dimension"] for r in block_records]).tolist()
    for name, vector in (("A", Acoord), ("D", Dcoord), ("S", s2 + s4)):
        F = (Uinv * ff.orbital_matrix(g, vector) * U).applyfunc(sp.cancel)
        for bi, rec in enumerate(block_records):
            lo, hi = starts[bi], starts[bi + 1]
            n = rec["multiplicity_space_dimension"]
            degree = rec["irreducible_degree"]
            block = F[lo:hi, lo:hi]
            Mdata = named[name][bi]["matrix"]
            M = sp.Matrix([[sp.Rational(*Mdata[i][j]) for j in range(n)] for i in range(n)])
            assert block == sp.kronecker_product(M, sp.eye(degree))
            assert F[lo:hi, :lo] == sp.zeros(hi - lo, lo)
            assert F[lo:hi, hi:] == sp.zeros(hi - lo, 120 - hi)

    action_payload = [{"orbital_index": x["orbital_index"], "block_hashes": [b["sha256"] for b in x["blocks"]]} for x in orbital_actions]
    result = {
        "theorem": "Pass 1411 Deterministic Tensor-Factor Selector Fourier Transform",
        "ordering": "Mackey blocks in frozen matrix-unit order; multiplicity index first, deterministic pivot basis inside the primitive irreducible copy",
        "blocks": block_records,
        "block_dimensions": [r["isotypic_dimension"] for r in block_records],
        "tensor_basis_U": matrix_stats(U),
        "tensor_inverse_Uinv": matrix_stats(Uinv),
        "exact_inverse_verified": True,
        "all_83_orbital_multiplicity_actions_sha256": sha(action_payload),
        "all_83_orbital_multiplicity_actions": orbital_actions,
        "named_multiplicity_actions": named,
        "conclusion": "The residual repeated-copy gauge is fixed deterministically. Every orbital operator acts blockwise as a multiplicity-space matrix tensored with the identity on the irreducible factor.",
        "boundary": "The pivot rule fixes a reproducible rational basis. It is canonical relative to the frozen matrix units and selector coordinate order, not invariant under arbitrary changes of those inputs.",
    }
    result["sha256"] = sha(result)
    return result
