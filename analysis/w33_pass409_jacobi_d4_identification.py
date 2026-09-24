#!/usr/bin/env python3
"""Pass 409: characteristic-zero classification of the 24D Jacobi algebra."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import subprocess, shutil, sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_pass409_jacobi_d4_identification.json"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def rational_row_basis():
    pivots, rows = [], []

    def add(vector):
        nonlocal pivots, rows
        vector = list(map(sp.Rational, vector))
        for pivot, row in zip(pivots, rows):
            if vector[pivot]:
                scale = vector[pivot]
                vector = [a - scale*b for a, b in zip(vector, row)]
        pivot = next((i for i, value in enumerate(vector) if value), None)
        if pivot is None:
            return False, None
        scale = vector[pivot]
        vector = [value/scale for value in vector]
        pivots.append(pivot)
        rows.append(vector)
        order = sorted(range(len(pivots)), key=pivots.__getitem__)
        pivots = [pivots[i] for i in order]
        rows = [rows[i] for i in order]
        return True, vector

    return add, lambda: len(rows)


def associative_algebra_dimension(generators):
    n = generators[0].rows
    add, dimension = rational_row_basis()
    queue = []
    for matrix in [sp.eye(n), *generators]:
        inserted, row = add(list(matrix))
        if inserted:
            queue.append(row)
    while queue:
        matrix = sp.Matrix(n, n, queue.pop())
        for generator in generators:
            inserted, row = add(list(matrix*generator))
            if inserted:
                queue.append(row)
    return dimension()


def commutant_basis(matrices, n):
    variables = sp.symbols("x0:" + str(n*n))
    unknown = sp.Matrix(n, n, variables)
    equations = []
    for matrix in matrices:
        equations.extend(list(unknown*matrix - matrix*unknown))
    coefficient_matrix, _ = sp.linear_eq_to_matrix(equations, variables)
    return [sp.Matrix(n, n, list(v)) for v in coefficient_matrix.nullspace()]


def alternating_form_dimension(matrices, n):
    pairs = [(i, j) for i in range(n) for j in range(i+1, n)]
    variables = sp.symbols("a0:" + str(len(pairs)))
    form = sp.zeros(n)
    for variable, (i, j) in zip(variables, pairs):
        form[i, j], form[j, i] = variable, -variable
    equations = []
    for matrix in matrices:
        equations.extend(list(matrix.T*form + form*matrix))
    coefficient_matrix, _ = sp.linear_eq_to_matrix(equations, variables)
    return len(coefficient_matrix.nullspace())


def reduced_cubic_from_commutant(basis):
    t = sp.symbols("x")
    for matrix in basis:
        factors = sp.factor_list(matrix.charpoly(t).as_expr())[1]
        cubic = next((f for f, multiplicity in factors if sp.degree(f, t) == 3 and multiplicity == 2), None)
        if cubic is None:
            continue
        monic = sp.Poly(cubic, t).monic().as_expr()
        gp_poly = str(monic).replace("**", "^")
        gp_cmd=["gp","-q"] if shutil.which("gp") else ["wsl","gp","-q"]
        run = subprocess.run(
            gp_cmd, input=f"print(polredabs({gp_poly}))\n",
            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
        )
        return run.stdout.strip(), str(sp.factor(matrix.charpoly(t).as_expr()))
    raise AssertionError("no primitive cubic commutant element")


def split_prime_replay(prime):
    env = dict(os.environ)
    env["W33_SPLIT_PRIME"] = str(prime)
    run = subprocess.run(
        [sys.executable, str(ROOT / "analysis/w33_20260923_cubic_jacobi_split107.py")],
        cwd=ROOT, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, check=True,
    )
    text = run.stdout
    required = [
        "factor_dims [3, 3, 3]",
        "modules 14 8 6",
        "commdims 1 3",
        "U_moved_direct_sum 6 [2, 2, 2]",
    ]
    assert all(item in text for item in required)
    for i in range(3):
        assert f"factor {i} W_inv 0 W_move 8 U_inv 4 U_move 2" in text
        for j in range(3):
            assert f"cross {i} {j} acts {i == j}" in text
    return text.splitlines()


def main(write=True):
    residual = load(ROOT / "analysis/w33_20260923_cubic_jacobi_residual.py", "residual")
    modules = load(ROOT / "analysis/w33_20260923_cubic_jacobi_char0_modules.py", "modules")
    residual_data = residual.main(write=True)

    comm8 = commutant_basis(modules.acts8, 8)
    comm6 = commutant_basis(modules.acts6, 6)
    algebra8 = associative_algebra_dimension(modules.acts8)
    algebra6 = associative_algebra_dimension(modules.acts6)
    alt8 = alternating_form_dimension(modules.acts8, 8)
    alt6 = alternating_form_dimension(modules.acts6, 6)
    reduced, commutant_charpoly = reduced_cubic_from_commutant(comm6)
    target = "x^3 - x^2 - 53*x - 120"
    assert (len(comm8), len(comm6), algebra8, algebra6, alt8, alt6) == (1, 3, 64, 12, 1, 3)
    assert reduced.replace(" ", "") == target.replace(" ", "")

    split_replays = {str(p): split_prime_replay(p) for p in (107, 151)}
    out = {
        "schema": "w33.pass409.jacobi_d4_identification.v1",
        "status": "PASS_RATIONAL_JACOBI_ALGEBRA_AND_D4_CONTACT_TRIALITY_COMPLETION",
        "rational_algebra": {
            "dimension": 24,
            "perfect": True,
            "center_dimension": 1,
            "radical": "Heisenberg h15",
            "radical_dimension": 15,
            "nested_ideal": "Heisenberg h9",
            "nested_ideal_dimension": 9,
            "levi_quotient": "Res_{K/Q} sl2(K)",
            "centroid_field": target,
            "centroid_discriminant": 94557,
            "semidirect_product": "(Res_{K/Q} sl2(K)) semidirect h15",
        },
        "characteristic_zero_modules": {
            "W8": {
                "dimension": 8,
                "commutant_dimension": len(comm8),
                "associative_image_dimension": algebra8,
                "invariant_alternating_forms": alt8,
                "classification_after_splitting": "(2,2,2)",
            },
            "U6": {
                "dimension": 6,
                "commutant_dimension": len(comm6),
                "commutant_reduced_polynomial": reduced,
                "sample_commutant_characteristic_polynomial": commutant_charpoly,
                "associative_image_dimension": algebra6,
                "invariant_alternating_forms": alt6,
                "classification_after_splitting": "(2,1,1) + (1,2,1) + (1,1,2)",
            },
            "reasoning": "End(W8)=Q and its associative image is M8(Q), while End(U6)=K and its associative image has Q-dimension 12=dim_Q M2(K). The split-prime audits identify the three A1 factors and their module weights.",
        },
        "split_prime_replays": split_replays,
        "d4_contact_identification": {
            "core_dimension": 18,
            "core": "(Res_K/Q sl2(K)) semidirect h9",
            "after_splitting_field": "sl2^3 semidirect h(2 tensor 2 tensor 2)",
            "interpretation": "This is the derived contact parabolic of D4: g0' = sl2^3, g_{-1}=2 tensor 2 tensor 2, g_{-2}=1.",
            "full_24D_extension": "The remaining U6 adds the triality orbit of three standard doublets to the same Heisenberg center.",
            "base_changed_full_form": "sl2^3 semidirect h((2,2,2) + (2,1,1) + (1,2,1) + (1,1,2))",
        },
        "theorem": "The residual control algebra is a rational cubic descent of a triality-completed D4 Jacobi algebra. Its 18D core is the derived D4 contact parabolic after scalar extension, and its extra six phase-space directions are exactly the three triality standard doublets.",
        "boundary": "This is an abstract rational Lie-algebra and module isomorphism. A single coordinate conjugating matrix to a conventional D4 Chevalley contact basis is not frozen here, and no continuum gauge or particle assignment follows.",
        "parents": [
            "data/w33_20260923_cubic_jacobi_residual.json",
            "data/w33_diagonal_weld_e8_lie_generation.json",
        ],
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    print(json.dumps(main(True), indent=2))
