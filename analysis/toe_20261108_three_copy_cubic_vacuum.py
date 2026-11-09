"""A rank-three F- and D-flat point for a supplied three-copy potential."""

from collections import Counter
from itertools import combinations
import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as sp

import toe_20261108_exact_signed_cubic_stabilizer as cubic
import w33_e6_cubic_jacobian_rank_stratification as native

ROOT = Path(__file__).resolve().parents[1]
OUT = 'data/toe_20261108_three_copy_cubic_vacuum.json'


def exact_echelon(array):
    return cubic.echelon({j: int(value) for j, value in enumerate(row) if value} for row in array)


def rank(array):
    return len(exact_echelon(array))


def traceless_basis(dimension):
    for i in range(dimension):
        for j in range(dimension):
            if i != j:
                value = np.zeros((dimension, dimension), dtype=np.int64)
                value[i, j] = 1
                yield value
    for i in range(dimension - 1):
        value = np.zeros((dimension, dimension), dtype=np.int64)
        value[i, i], value[i + 1, i + 1] = 1, -1
        yield value


def gauge_generators(certificate):
    internal = []
    for entries in certificate['cubic_27']['generators']:
        matrix = np.zeros((27, 27), dtype=np.int64)
        for i, j, value in entries:
            matrix[i, j] = value
        internal.append(np.kron(matrix, np.eye(3, dtype=np.int64)))
    external = [np.kron(np.eye(27, dtype=np.int64), s) for s in traceless_basis(3)]
    return internal + external


def bracket(left, right, records):
    output = np.zeros(81, dtype=np.result_type(left, right))
    for a, b, c, sign in records:
        output[c] += sign * left[a] * right[b]
    return output


def commuting_supports(terms, records):
    """Enumerate disjoint all-plus triad triples in the declared chart."""
    supports = sorted(terms)
    lookup = {(a, b): (c, s) for a, b, c, s in records}
    assert len(lookup) == len(records)
    neighbors = [set() for _ in supports]
    for i, j in combinations(range(len(supports)), 2):
        left, right = supports[i], supports[j]
        if set(left) & set(right):
            continue
        output = Counter()
        for a in left:
            for b in right:
                if (a, b) in lookup:
                    c, sign = lookup[a, b]
                    output[c] += sign
        if not any(output.values()):
            neighbors[i].add(j)
            neighbors[j].add(i)
    triples = [(i, j, k) for i in range(len(supports)) for j in neighbors[i] if j > i
               for k in neighbors[i] & neighbors[j] if k > j]
    return [supports[i] for i in min(triples)], len(triples)


def stabilizer_type(generators, orbit):
    """Compute the exact Killing rank of the infinitesimal point stabilizer."""
    vectors = cubic.integer_kernel(exact_echelon(orbit.T), len(generators))
    stabilizer = [sum((value * generators[i] for i, value in v.items()),
                      np.zeros((81, 81), dtype=np.int64)) for v in vectors]
    flattened = sp.Matrix(np.array(stabilizer).reshape(len(stabilizer), -1).T.tolist())
    pivot_rows = list(flattened.T.rref()[1])
    inverse = flattened[pivot_rows, :].inv()
    adjoints = []
    for first in stabilizer:
        columns = []
        for second in stabilizer:
            commutator = sp.Matrix((first @ second - second @ first).ravel().tolist())
            coordinates = inverse * commutator[pivot_rows, :]
            assert flattened * coordinates == commutator
            columns.append(coordinates)
        adjoints.append(sp.Matrix.hstack(*columns))
    killing = sp.Matrix(len(stabilizer), len(stabilizer),
                        lambda i, j: sp.trace(adjoints[i] * adjoints[j]))
    return len(stabilizer), killing.rank(), vectors, stabilizer


def residual_branching(stabilizer):
    internal = [g[::3, ::3] for g in stabilizer]
    assert all(np.array_equal(g, np.kron(t, np.eye(3, dtype=np.int64)))
               for g, t in zip(stabilizer, internal))
    diagonals = [np.diag(t) for t in internal if not np.any(t - np.diag(np.diag(t)))]
    assert len(diagonals) == 2
    root_spaces = {}
    for t in internal:
        positions = [(i, j) for i, j in zip(*np.nonzero(t)) if i != j]
        if positions:
            roots = {tuple(int(h[i] - h[j]) for h in diagonals) for i, j in positions}
            assert len(roots) == 1
            root_spaces[roots.pop()] = t
    assert len(root_spaces) == 6
    positive = {r for r in root_spaces if next(v for v in r if v) > 0}
    simple = sorted(positive - {(a[0]+b[0],a[1]+b[1]) for a in positive for b in positive})
    assert len(simple) == 2
    raising = [root_spaces[r] for r in simple]
    h = [np.diag(e @ e.T - e.T @ e) for e in raising]
    cartan = []
    for d in h:
        row = []
        for e in raising:
            i, j = next(zip(*np.nonzero(e)))
            row.append(int(d[i] - d[j]))
        cartan.append(row)
    assert cartan == [[2,-1],[-1,2]]
    counts = Counter((int(a),int(b)) for a,b in zip(*h))
    expected = {(0,0):9,(1,0):3,(-1,1):3,(0,-1):3,(-1,0):3,(1,-1):3,(0,1):3}
    assert counts == expected
    return dict(type='A2 inside E6', simple_Cartan_matrix=cartan, external_continuous_factor_fully_broken=True,
                branching_27='9 singlets + 3 fundamental triplets + 3 conjugate triplets',
                exact_weight_census=[[*weight, count] for weight, count in sorted(counts.items())])


def tangent_ranks(X, generators, records):
    """Exact real and imaginary blocks of the sum-of-squares Hessian."""
    f_derivative = np.zeros((243, 243), dtype=np.int64)
    for pair, (a, b) in enumerate(combinations(range(3), 2)):
        for u, v, w, sign in records:
            f_derivative[81 * pair + w, 3 * u + a] += sign * X[v, b]
            f_derivative[81 * pair + w, 3 * v + b] += sign * X[u, a]
    coordinate_vectors = np.eye(243, dtype=np.int64).reshape(243, 81, 3)
    gram = np.array([X.T @ Y for Y in coordinate_vectors])
    gram_real = (gram + gram.transpose(0, 2, 1)).reshape(243, 9).T
    gram_imaginary = (gram - gram.transpose(0, 2, 1)).reshape(243, 9).T
    moment_real = np.array([((g + g.T) @ X).ravel() for g in generators])
    moment_imaginary = np.array([((g - g.T) @ X).ravel() for g in generators])
    constraint_real = np.vstack([f_derivative, gram_real, moment_real])
    constraint_imaginary = np.vstack([f_derivative, gram_imaginary, moment_imaginary])
    gauge_real, gauge_imaginary = moment_imaginary, moment_real
    species = [*traceless_basis(3), np.eye(3, dtype=np.int64)]
    species_real = np.array([(X @ (g - g.T)).ravel() for g in species])
    species_imaginary = np.array([(X @ (g + g.T)).ravel() for g in species])
    assert not np.any(constraint_real @ np.vstack([gauge_real, species_real]).T)
    assert not np.any(constraint_imaginary @ np.vstack([gauge_imaginary, species_imaginary]).T)
    re_rank = rank(constraint_real)
    im_rank = rank(constraint_imaginary)
    orbit_rank = rank(gauge_real) + rank(gauge_imaginary)
    together = rank(np.vstack([gauge_real, species_real])) + rank(np.vstack([gauge_imaginary, species_imaginary]))
    nullity = 486 - re_rank - im_rank
    assert (re_rank, im_rank, orbit_rank, together, nullity) == (204, 195, 78, 87, 87)
    return dict(complex_F_derivative_rank=rank(f_derivative), real_constraint_rank=re_rank,
                imaginary_constraint_rank=im_rank, Hessian_nullity=nullity,
                compact_gauge_orbit_dimension=orbit_rank, physical_Hessian_nullity=nullity-orbit_rank,
                gauge_plus_species_orbit_dimension=together, species_tangents_span_physical_kernel=True)


def calculate():
    certificate = cubic.calculate()
    terms = cubic.alternating_terms(cubic.signed_terms(cubic.CUBIC))
    records = native.build_records()
    assert Counter((tuple(sorted((a,b,c))), sign * cubic.parity((a,b,c)))
                   for a,b,c,sign in records) == Counter({(term, sign): 6 for term,sign in terms.items()})
    supports, count = commuting_supports(terms, records)
    X = np.zeros((81, 3), dtype=np.int64)
    for j, support in enumerate(supports):
        X[list(support), j] = 1
    assert np.array_equal(X.T @ X, 3*np.eye(3, dtype=np.int64))
    assert all(not np.any(bracket(X[:, a], X[:, b], records)) for a, b in combinations(range(3), 2))
    generators = gauge_generators(certificate)
    assert all(np.trace(X.T @ g @ X) == 0 for g in generators)
    orbit = np.array([(g @ X).ravel() for g in generators])
    dimension, killing_rank, stabilizer, matrices = stabilizer_type(generators, orbit)
    assert (dimension, killing_rank) == (8,8)
    branching = residual_branching(matrices)
    ranks = tangent_ranks(X, generators, records)
    paths = [cubic.CUBIC, cubic.ARCHIVE, 'analysis/toe_20261108_exact_signed_cubic_stabilizer.py',
             'analysis/toe_20261108_three_copy_cubic_vacuum.py', 'analysis/w33_e6_cubic_jacobian_rank_stratification.py']
    return dict(status='EXACT_THREE_COPY_F_D_GRAM_VACUUM_AND_PHYSICAL_FLAT_DIRECTIONS',
                commuting_disjoint_all_plus_triad_triples=count, chosen_supports=supports,
                Gram='3 I3 in supplied field units', F_zero=True, D_zero=True,
                unbroken_complex_Lie_dimension=dimension, unbroken_Killing_rank=killing_rank,
                unbroken_branching=branching,
                unbroken_Lie_basis_coefficients=[[[i, v] for i, v in sorted(row.items())] for row in stabilizer],
                tangent_ranks=ranks,
                action='Positive sum of squared F, D, and Gram residuals for three bosonic 81-component copies. W(X)=T(X1,X2,X3). The declared Gram term fixes X†X=3 I3.',
                flat_directions='Species U(3) rotations preserve the three norms in the action. Their nine independent tangent directions modulo gauge exhaust the physical Hessian kernel at this point. This is an actual symmetry orbit of minima.',
                scope='This is a classical supplied potential with specified canonical Hermitian metric. A supersymmetric realization of the extra Gram term, anomaly-canceling fermion inventory, isolated vacuum and radiative dynamics are additional problems.',
                raw_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths})


if __name__ == '__main__':
    result = calculate()
    (ROOT / OUT).write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('chosen_supports', 'unbroken_complex_Lie_dimension',
                                            'unbroken_Killing_rank', 'tangent_ranks')}))
