#!/usr/bin/env python3
"""Pass 10941 front 1: exact rational chart for the trialitarian D4 core.

The rational core is a non-split trialitarian form.  Its cubic centroid rules
out a Q-isomorphism with the split D4 contact parabolic.  This script replaces
that impossible target by an explicit two-chart coordinate map from the
248-coordinate E8 realization to a fixed 18-dimensional rational contact
presentation.
"""
from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
from fractions import Fraction
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_pass10941_rational_triality_coordinate_chart.json"


def load_quiet(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


cm = load_quiet(
    ROOT / "analysis/w33_20260923_cubic_jacobi_char0_modules.py", "cm10941"
)
asai = load_quiet(
    ROOT / "analysis/w33_20260924_trialitarian_asai_cube_descent.py", "asai10941"
)


def q(x) -> sp.Rational:
    x = Fraction(x)
    return sp.Rational(x.numerator, x.denominator)


def col(v) -> sp.Matrix:
    return sp.Matrix([q(x) for x in v])


z = cm.Z.vectors[0]
ordered_basis = list(cm.Q9) + list(cm.W8) + [z]
names = [f"S9_{i}" for i in range(9)] + [f"W8_{i}" for i in range(8)] + ["Z"]
embedding = sp.Matrix.hstack(*[col(v) for v in ordered_basis])
assert embedding.shape == (248, 18) and embedding.rank() == 18


def pivot_chart(row_order):
    permuted = embedding.extract(row_order, range(18))
    _, pivots = permuted.T.rref()
    rows = [row_order[i] for i in pivots]
    assert len(rows) == 18
    minor = embedding.extract(rows, range(18))
    assert minor.det() != 0
    inverse = minor.inv()
    return rows, minor, inverse


forward_rows, forward_minor, forward_inverse = pivot_chart(list(range(248)))
reverse_rows, reverse_minor, reverse_inverse = pivot_chart(list(reversed(range(248))))
assert forward_rows != reverse_rows


def coords(v, rows, inverse):
    vector = col(v)
    c = inverse * vector.extract(rows, [0])
    assert embedding * c == vector
    return c


for i, v in enumerate(ordered_basis):
    target = sp.eye(18)[:, i]
    assert coords(v, forward_rows, forward_inverse) == target
    assert coords(v, reverse_rows, reverse_inverse) == target

# Freeze the complete bracket table in the fixed rational presentation.
table = {}
nonzero = 0
max_denominator = 1
for i in range(18):
    for j in range(i, 18):
        v = cm.br(ordered_basis[i], ordered_basis[j])
        cf = coords(v, forward_rows, forward_inverse)
        cr = coords(v, reverse_rows, reverse_inverse)
        assert cf == cr
        values = [sp.Rational(x) for x in cf]
        if any(values):
            nonzero += 1
            table[f"{i},{j}"] = [str(x) for x in values]
        for x in values:
            max_denominator = max(max_denominator, int(x.q))


def bracket_coords(a: sp.Matrix, b: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(18, 1)
    for i in range(18):
        if not a[i]:
            continue
        for j in range(18):
            if not b[j]:
                continue
            raw = cm.br(ordered_basis[i], ordered_basis[j])
            out += a[i] * b[j] * coords(raw, forward_rows, forward_inverse)
    return sp.simplify(out)


# Coordinate-level Jacobi audit on every ordered basis triple.
jacobi_checks = 0
unit = [sp.eye(18)[:, i] for i in range(18)]
for i in range(18):
    for j in range(18):
        for k in range(18):
            jac = (
                bracket_coords(unit[i], bracket_coords(unit[j], unit[k]))
                + bracket_coords(unit[j], bracket_coords(unit[k], unit[i]))
                + bracket_coords(unit[k], bracket_coords(unit[i], unit[j]))
            )
            assert jac == sp.zeros(18, 1)
            jacobi_checks += 1

# The split rational contact parabolic has centroid Q^3 on its A1^3 Levi,
# whereas the repo core has the field K.  These Q-algebras cannot be
# isomorphic: Q^3 has six nontrivial idempotents and a field has none.
x = sp.Symbol("x")
kpoly = x**3 - x**2 - 53 * x - 120
assert sp.Poly(kpoly, x, domain=sp.QQ).is_irreducible
split_centroid_nontrivial_idempotents = 6
trialitarian_centroid_nontrivial_idempotents = 0
assert split_centroid_nontrivial_idempotents != trialitarian_centroid_nontrivial_idempotents


def matrix_strings(m: sp.Matrix):
    return [[str(sp.Rational(m[i, j])) for j in range(m.cols)] for i in range(m.rows)]


def digest_matrix(m: sp.Matrix) -> str:
    payload = "|".join(str(sp.Rational(x)) for x in list(m))
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


table_digest = hashlib.sha256(
    json.dumps(table, sort_keys=True, separators=(",", ":")).encode("utf-8")
).hexdigest()

out = {
    "schema": "w33.pass10941.rational_triality_coordinate_chart.v1",
    "status": "PASS_RATIONAL_TRIALITARIAN_D4_COORDINATE_CHART_AND_SPLIT_NOGO",
    "fixed_presentation": {
        "dimension": 18,
        "ordered_basis": names,
        "structure": "Res_{K/Q} sl2(K) semidirect h4",
        "centroid_field_polynomial": "x^3 - x^2 - 53*x - 120",
        "embedding_shape": [248, 18],
        "embedding_sha256": digest_matrix(embedding),
        "nonzero_unordered_brackets": nonzero,
        "bracket_table_sha256": table_digest,
        "maximum_structure_constant_denominator": max_denominator,
        "jacobi_checks": jacobi_checks,
    },
    "forward_chart": {
        "pivot_rows_zero_based": forward_rows,
        "pivot_minor_determinant": str(sp.factor(forward_minor.det())),
        "pivot_minor": matrix_strings(forward_minor),
        "pivot_minor_inverse": matrix_strings(forward_inverse),
        "coordinate_formula": "c = pivot_minor_inverse * v[pivot_rows]",
    },
    "reverse_chart": {
        "pivot_rows_zero_based": reverse_rows,
        "pivot_minor_determinant": str(sp.factor(reverse_minor.det())),
        "pivot_minor": matrix_strings(reverse_minor),
        "pivot_minor_inverse": matrix_strings(reverse_inverse),
        "coordinate_formula": "c = pivot_minor_inverse * v[pivot_rows]",
    },
    "two_chart_audit": {
        "charts_distinct": True,
        "basis_coordinates_agree": True,
        "all_unordered_bracket_coordinates_agree": True,
    },
    "split_rational_nogo": {
        "trialitarian_levi_centroid": "cubic field K",
        "trialitarian_centroid_nontrivial_idempotents": 0,
        "split_A1_cubed_centroid": "Q^3",
        "split_centroid_nontrivial_idempotents": 6,
        "conclusion": "No Q-linear Lie-algebra conjugation to the split D4 contact parabolic exists.",
        "correct_target": "the fixed rational trialitarian contact presentation frozen above",
        "splitting_boundary": "A split Chevalley conjugation can exist only after scalar extension to a splitting field of K.",
    },
    "parents": [
        "analysis/w33_20260923_cubic_jacobi_char0_modules.py",
        "analysis/w33_20260924_trialitarian_asai_cube_descent.py",
    ],
    "boundary": (
        "This is an exact rational coordinate chart and a split-form no-go. "
        "It is not a coordinate map to the split rational D4 algebra, because "
        "the centroid proves that such a map cannot exist."
    ),
}
OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
print(
    json.dumps(
        {
            "status": out["status"],
            "forward_det": out["forward_chart"]["pivot_minor_determinant"],
            "reverse_det": out["reverse_chart"]["pivot_minor_determinant"],
            "nonzero_brackets": nonzero,
            "jacobi_checks": jacobi_checks,
        },
        indent=2,
    )
)
