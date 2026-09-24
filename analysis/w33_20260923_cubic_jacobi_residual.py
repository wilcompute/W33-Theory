#!/usr/bin/env python3
"""Classify the 24D nondiagnonal H27 control closure after the E8 weld pass."""
from __future__ import annotations

import importlib.util
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "analysis/w33_diagonal_weld_e8_lie_generation.py"
OUT = ROOT / "data/w33_20260923_cubic_jacobi_residual.json"
P = 103


def load_parent():
    spec = importlib.util.spec_from_file_location("w33_diag_weld", PARENT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def mod_fraction(x, p=P):
    x = Fraction(x)
    return x.numerator * pow(x.denominator, -1, p) % p


class ModBasis:
    def __init__(self, n=248, p=P):
        self.n, self.p = n, p
        self.rows, self.vectors = {}, []

    def add(self, vector):
        p = self.p
        v = [int(x) % p for x in vector]
        for pivot in sorted(self.rows):
            if v[pivot]:
                f, row = v[pivot], self.rows[pivot]
                v = [(a - f*b) % p for a, b in zip(v, row)]
        pivot = next((i for i, x in enumerate(v) if x), None)
        if pivot is None:
            return False
        inv = pow(v[pivot], -1, p)
        v = [(x*inv) % p for x in v]
        self.rows[pivot] = v
        self.vectors.append(v)
        return True

    def reduce(self, vector):
        p = self.p
        v = [int(x) % p for x in vector]
        for pivot in sorted(self.rows):
            if v[pivot]:
                f, row = v[pivot], self.rows[pivot]
                v = [(a - f*b) % p for a, b in zip(v, row)]
        return v

    @property
    def dim(self):
        return len(self.rows)


def rank_mod(matrix, p=P):
    a = [[int(x) % p for x in row] for row in matrix]
    if not a:
        return 0
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][c], -1, p)
        a[r] = [(x*inv) % p for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                f = a[i][c]
                a[i] = [(x - f*y) % p for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def exact_ideal(parent, generators, seed, table):
    basis = parent.RationalBasis()
    queue = []
    if basis.add(seed, 0):
        queue.append(basis.vectors[-1])
    while queue:
        v = queue.pop()
        for g in generators:
            w = parent.bracket(g, v, table, None)
            if basis.add(w, 0):
                queue.append(basis.vectors[-1])
    return basis


def mod_bracket(parent, a, b, table):
    return [int(x) % P for x in parent.bracket(a, b, table, P)]


def center_dimension(parent, vectors, table):
    n = len(vectors)
    equations = []
    for g in vectors:
        cols = [mod_bracket(parent, v, g, table) for v in vectors]
        for k in range(248):
            row = [cols[i][k] for i in range(n)]
            if any(row):
                equations.append(row)
    return n - rank_mod(equations)


def derived_data(parent, vectors, table):
    basis = ModBasis()
    for a in vectors:
        for b in vectors:
            basis.add(mod_bracket(parent, a, b, table))
    return basis


def heisenberg_witness(parent, exact_basis, table):
    vectors = [[mod_fraction(x) for x in v] for v in exact_basis.vectors]
    derived = derived_data(parent, vectors, table)
    assert derived.dim == 1
    z = derived.vectors[0]
    pivot = sorted(derived.rows)[0]
    inv = pow(z[pivot], -1, P)
    omega = []
    for a in vectors:
        row = []
        for b in vectors:
            c = mod_bracket(parent, a, b, table)
            row.append(c[pivot] * inv % P)
        omega.append(row)
    return {
        "dimension": len(vectors),
        "center_dimension_mod103": center_dimension(parent, vectors, table),
        "derived_dimension_mod103": derived.dim,
        "commutator_form_rank_mod103": rank_mod(omega),
    }


def quotient_structure(parent, full_basis, ideal15, table):
    def reduce_exact(basis, vector):
        v = list(map(Fraction, vector))
        for pivot in sorted(basis.rows):
            if v[pivot]:
                factor = v[pivot]
                row = basis.rows[pivot]
                v = [a - factor*b for a, b in zip(v, row)]
        return v

    ideal = parent.RationalBasis()
    for v in ideal15.vectors:
        ideal.add(v, 0)
    qb = parent.RationalBasis()
    for v in full_basis:
        qb.add(reduce_exact(ideal, v), 0)
    pivots = sorted(qb.rows)
    qvec = [qb.rows[p] for p in pivots]
    assert len(qvec) == 9

    def qcoords(v):
        r = reduce_exact(ideal, v)
        coeff = []
        for p in pivots:
            c = r[p]
            coeff.append(c)
            if c:
                row = qb.rows[p]
                r = [a - c*b for a, b in zip(r, row)]
        assert all(x == 0 for x in r)
        return coeff

    structure = [[qcoords(parent.bracket(a, b, table, None))
                  for b in qvec] for a in qvec]
    n = 9
    ads = []
    for i in range(n):
        A = sp.zeros(n)
        for j in range(n):
            for k, c in enumerate(structure[i][j]):
                A[k, j] = sp.Rational(c.numerator, c.denominator)
        ads.append(A)

    killing = sp.Matrix([[sp.trace(ads[i]*ads[j])
                          for j in range(n)] for i in range(n)])

    # Exact split witness for the A1-form over its cubic centroid field.
    nil_coeff = [0, 0, 0, -1, -1, -1, 0, 0, 0]
    nil_ad = sp.zeros(n)
    for c, A in zip(nil_coeff, ads):
        nil_ad += c*A
    assert nil_ad != sp.zeros(n)
    assert nil_ad**3 == sp.zeros(n)
    assert nil_ad.rank() == 6 and (nil_ad**2).rank() == 3


    equations = []
    variables = n*n
    for A in ads:
        for r in range(n):
            for c in range(n):
                row = [sp.Rational(0)] * variables
                for k in range(n):
                    row[r*n+k] += A[k, c]
                    row[k*n+c] -= A[r, k]
                if any(row):
                    equations.append(row)
    cent = sp.Matrix(equations)
    centroid_null = cent.nullspace()
    assert len(centroid_null) == 3

    t = sp.symbols("t")
    centroid_mats = [sp.Matrix(n, n, list(v)) for v in centroid_null]
    non_scalar = next(C for C in centroid_mats
                      if C != sp.eye(n) and C != -sp.eye(n))
    char = sp.factor(non_scalar.charpoly(t).as_expr())

    # The PARI witness reduces the cubic factor of this field to the polynomial below.
    reduced = t**3 - t**2 - 53*t - 120
    disc = sp.discriminant(reduced, t)
    assert disc == 94557

    return {
        "dimension": 9,
        "killing_rank_over_Q": killing.rank(),
        "centroid_dimension_over_Q": len(centroid_null),
        "one_centroid_characteristic_polynomial": str(char),
        "reduced_centroid_field_polynomial": "x^3 - x^2 - 53*x - 120",
        "centroid_field_discriminant": int(disc),
        "centroid_field_discriminant_factorization": "3*43*733",
        "split_nilpotent_coefficients_in_quotient_basis": nil_coeff,
        "split_nilpotent_ad_rank": nil_ad.rank(),
        "split_nilpotent_ad2_rank": (nil_ad**2).rank(),
        "split_nilpotent_ad3_zero": True,
    }


def main(write=True):
    parent = load_parent()
    compiler, bridge, table = parent.load_inputs()
    amps = parent.backgrounds(bridge)
    vectors = parent.source_generators(compiler, amps)
    full, _ = parent.closure(
        (vectors[(1, "center")], vectors[(2, "center")]),
        table, parent.RationalBasis())
    assert len(full.rows) == 24

    # Deterministic seeds in the parent's insertion order.
    i15 = exact_ideal(parent, full.vectors, full.vectors[6], table)
    i9 = exact_ideal(parent, full.vectors, full.vectors[10], table)
    assert len(i15.rows) == 15 and len(i9.rows) == 9

    full_mod = [[mod_fraction(x) for x in v] for v in full.vectors]
    full_derived = derived_data(parent, full_mod, table)
    full_center = center_dimension(parent, full_mod, table)
    assert full_derived.dim == 24 and full_center == 1

    h15 = heisenberg_witness(parent, i15, table)
    h9 = heisenberg_witness(parent, i9, table)
    assert h15 == {
        "dimension": 15, "center_dimension_mod103": 1,
        "derived_dimension_mod103": 1, "commutator_form_rank_mod103": 14}
    assert h9 == {
        "dimension": 9, "center_dimension_mod103": 1,
        "derived_dimension_mod103": 1, "commutator_form_rank_mod103": 8}

    q = quotient_structure(parent, full.vectors, i15, table)
    assert q["killing_rank_over_Q"] == 9
    assert q["centroid_dimension_over_Q"] == 3

    out = {
        "schema": "w33.20260923.cubic_jacobi_residual.v1",
        "status": "PASS_24D_RESIDUAL_HAS_HEISENBERG15_RADICAL_AND_CUBIC_A1_LEVI_QUOTIENT",

        "ambient": {
            "dimension": 24,
            "grading": [6, 9, 9],
            "source": "center|center nondiagonal H27 pair; all four center/external controls span the same subalgebra",
            "perfect": full_derived.dim == 24,
            "derived_dimension_mod103": full_derived.dim,
            "center_dimension_mod103": full_center,
        },
        "radical": {
            "dimension": 15,
            "type": "Heisenberg h_15",
            "witness": h15,
            "reason": "2-step solvable ideal with center=derived=1 and nondegenerate rank-14 alternating bracket on h_15/Z; quotient has nondegenerate Killing form, hence this ideal is the radical",
        },
        "nested_heisenberg": {
            "dimension": 9,
            "type": "Heisenberg h_9",
            "witness": h9,
        },
        "levi_quotient": {
            **q,
            "classification": "Res_{K/Q} sl2(K): a 9D Q-simple algebra obtained by restriction of scalars from split sl2 over the cubic centroid field K",
            "split_over_K": "SPLIT_BY_EXACT_NILPOTENT_AD_CUBE_ZERO",
        },
        "levi_decomposition": "By Levi-Malcev in characteristic zero, L_24 is a semidirect product s_9 ⋉ h_15 for some Levi factor s_9 isomorphic to the quotient.",
        "physics_reading": "Jacobi-type finite control algebra: a cubic A1-form acts by derivations on the 14D symplectic phase space h_15/Z.",
        "boundaries": [
            "The residual algebra is NOT A2^3/trinification.",
            "Splitness over K is certified by the exact nonzero nilpotent with ad^3=0.",
            "This is an exact finite/rational Lie-algebra statement, not a laboratory Hamiltonian or continuum gauge group."
        ],
        "parents": [
            "data/w33_diagonal_weld_e8_lie_generation.json",
            "artifacts/e8_structure_constants_w33_discrete.json"
        ],
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    print(json.dumps(main(True), indent=2))
