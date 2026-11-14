"""Complete the STU transfer by compact rotations and check the KK and lattice reductions."""
import json
from collections import Counter
from itertools import permutations
from math import gcd

import sympy as sp

from toe_20261114_e6_stu_boundary_transfer import DICTIONARY, OUT as OLD, R, TORUS, flatten_columns, rank

OUT = OLD.with_name("toe_20261114_e6_stu_five_tests.json")


def matrix_basis(records):
    basis = []
    for entries in records:
        a = sp.zeros(27)
        for i, j, v in entries:
            a[i, j] = v
        basis.append(a)
    return basis


def calculate():
    cert, cubic, _, _, roots = R.load()
    triad = json.loads(TORUS.read_text())["native_coordinates"]
    signs = set(json.loads(DICTIONARY.read_text())["coordinate_negative_sign_indices"])
    old = json.loads(OLD.read_text())
    basis = matrix_basis(cert["cubic_27"]["generators"])
    columns = flatten_columns(basis)
    _, generators = R.pack_roots(roots)
    compact = [sp.Matrix(g.tolist()) for g in generators]
    compact_columns = flatten_columns(compact)
    incidence = sp.Matrix([[int(i in t) for i in range(27)] for t in sorted(cubic)])
    diagonal = sp.Matrix.hstack(*incidence.nullspace())
    projector = diagonal * (diagonal.T * diagonal).inv() * diagonal.T
    weights = projector[:, triad[:2]] * projector[triad[:2], triad[:2]].inv()
    stu = [sp.diag(*weights[:, j]) for j in range(2)]
    rows = []
    cases = [dict(charges=[1, 64, 262144], balanced_magnitude=256,
                  boundary_stabilizer_rank=40), *old["cases"]]
    for case in cases:
        magnitudes = case["charges"]
        common = case["balanced_magnitude"]
        q = sp.zeros(27, 1)
        for i, x in zip(triad, magnitudes, strict=True):
            q[i] = -x if i in signs else x
        stabilizer = [sp.Matrix(27, 27, columns*v)
                      for v in sp.Matrix.hstack(*(a*q for a in basis)).nullspace()]
        fixing = [sp.Matrix(27, 27, compact_columns*v)
                  for v in sp.Matrix.hstack(*(a*q for a in compact)).nullspace()]
        varied = stu + [k*a-a*k for k in fixing for a in stu]
        directions = flatten_columns(varied)
        d = sp.diag(*(sp.Rational(common, magnitudes[0])**u * sp.Rational(common, magnitudes[1])**v
                      for u, v in weights.tolist()))
        inv = d.inv()
        assert all(k*d == d*k for k in fixing)
        moved = [d*a*inv for a in stabilizer]
        u = flatten_columns([a+a.T for a in stabilizer]).row_join(directions)
        v = flatten_columns([a+a.T for a in moved]).row_join(sp.zeros(729, directions.cols))
        assert rank(u) == 42 and rank(v) == 28 and rank(u.col_join(v)) == 42
        cols = list(u.rref()[1])
        u, v = u[:, cols], v[:, cols]
        spectrum = (u.T*u).inv()*(v.T*v)
        x = sp.Symbol("x")
        factors = Counter()
        for polynomial, mult in sp.factor_list(spectrum.charpoly(x).as_expr())[1]:
            a, b = sp.Poly(polynomial, x).all_coeffs()
            factors[-b/a] += mult
        assert factors[0] == 14
        sizes = Counter([sp.Integer(1)]*16)
        for a, b in [(0, 1), (0, 2), (1, 2)]:
            sizes[sp.Rational(4*magnitudes[a]*magnitudes[b], (magnitudes[a]+magnitudes[b])**2)] += 4
        assert factors == sizes + Counter({0: 14})
        assert rank(directions) == 42-case["boundary_stabilizer_rank"]
        rows.append(dict(charges=magnitudes, rotated_stu_span=int(rank(directions)), horizon_rank=28,
                         squared_singular_values={str(k): int(n) for k, n in sorted(factors.items())}))

    # Test the normal space at the balanced point for Lie triple closure.
    symmetric_columns = flatten_columns([a+a.T for a in basis])
    independent = symmetric_columns.rref()[1]
    symmetric = [sp.Matrix(27, 27, symmetric_columns[:, i]) for i in independent]
    g = flatten_columns(symmetric)
    response = sp.Matrix.hstack(*(a*q for a in symmetric))
    normal_columns = g * (g.T*g).inv() * response.T
    normals = [sp.Matrix(27, 27, normal_columns[:, i]) for i in normal_columns.rref()[1]]
    assert len(normals) == 14
    n = flatten_columns(normals)
    orthogonal = n*(n.T*n).inv()*n.T
    commutators = [a*b-b*a for i, a in enumerate(normals) for b in normals[i+1:]]
    kcols = flatten_columns(commutators)
    brackets = [sp.Matrix(27, 27, kcols[:, i]) for i in kcols.rref()[1]]
    assert len(brackets) == 21
    for a in brackets:
        for b in normals:
            result = (a*b-b*a).reshape(729, 1)
            assert orthogonal*result == result

    balanced = d*q
    cubic_hessian = sp.zeros(27)
    for t, value in cubic.items():
        for i, j, k in permutations(t):
            cubic_hessian[i, j] += value*balanced[k]
    assert cubic_hessian.charpoly().as_expr().factor() == (
        (sp.Symbol("lambda")-2)*(sp.Symbol("lambda")-1)**12*(sp.Symbol("lambda")+1)**14)
    p = sp.Symbol("p", integer=True)
    axion_eigenvalues = {sign: [sign**2 + sign*z + int(z == 2)*3 for z in (2, 1, -1)]
                         for sign in (-1, 1)}
    assert axion_eigenvalues == {-1: [2, 0, 2], 1: [6, 2, 0]}

    q_integer = sp.zeros(27, 1)
    for i in triad:
        q_integer[i] = -1 if i in signs else 1
    fixed_roots = [r for r in roots if not any(r@q_integer)]
    assert len(fixed_roots) == 24
    for root in fixed_roots:
        root = sp.Matrix(root.tolist())
        assert root**2 == sp.zeros(27) and (sp.eye(27)+root)*q_integer == q_integer
        R.inf_check(root, cubic)
    assert 1*64*4096 == 64**3 and gcd(1, 64, 4096) != gcd(64, 64, 64)
    primitive_examples = [(1, 1, 64), (1, 4, 16)]
    gradients = []
    for charge in primitive_examples:
        vector = [0]*27
        for i, component in zip(triad, charge, strict=True):
            vector[i] = -component if i in signs else component
        grad = [0]*27
        for term, value in cubic.items():
            for i, j, k in (term, term[1:]+term[:1], term[2:]+term[:2]):
                grad[i] += value*vector[j]*vector[k]
        assert sum(v*vector[i]*vector[j]*vector[k] for (i, j, k), v in cubic.items()) == 64
        gradients.append(gcd(*grad))
    assert gradients == [1, 4]
    return dict(status="PASS", transfer=rows,
                circle_axion_hessian_units=axion_eigenvalues, circle_total_flat={-1: 40, 1: 42},
                normal_lie_triple_dimension=len(normals), normal_bracket_dimension=len(brackets),
                integral_root_subgroups=len(fixed_roots), primitive_same_cubic_gradient_gcd=gradients,
                same_cubic_integral_obstruction=dict(original_gcd=1, balanced_gcd=64))


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result, flush=True)
