"""Exact infinitesimal stabilizers of the committed signed cubic and 3-form."""

from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, combinations_with_replacement, permutations
import hashlib
import json
from math import gcd, lcm
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
CUBIC = 'artifacts/canonical_su3_gauge_and_cubic.json'
ARCHIVE = 'extracted_v13/W33-Theory-master/artifacts/canonical_su3_gauge_and_cubic.json'
OUT = 'data/toe_20261108_exact_signed_cubic_stabilizer.json'


def parity(word):
    return (-1) ** sum(i > j for i, j in combinations(word, 2))


def signed_terms(path):
    records = json.loads((ROOT / path).read_bytes())['solution']['d_triples']
    return {tuple(sorted(row['triple'])): int(row['sign']) for row in records}


def coefficient_rows(terms, dimension, alternating=False):
    """Rows of the derivative map, indexed by output monomials."""
    rows = defaultdict(Counter)
    for term, sign in terms.items():
        for position, source in enumerate(term):
            for target in range(dimension):
                word = term[:position] + (target,) + term[position + 1:]
                if alternating and len(set(word)) < 3:
                    continue
                coefficient = sign * (parity(word) if alternating else 1)
                rows[tuple(sorted(word))][source * dimension + target] += coefficient
    return list(rows.values())


def echelon(rows, prime=None):
    """Sparse echelon form over Q or a stated prime field."""
    pivots = {}
    for source in rows:
        row = {j: Fraction(value) if prime is None else int(value) % prime
               for j, value in source.items() if value}
        row = {j: value for j, value in row.items() if value}
        while row:
            column = min(row)
            value = row[column]
            if column not in pivots:
                inverse = 1 / value if prime is None else pow(value, -1, prime)
                pivots[column] = {j: v * inverse if prime is None else v * inverse % prime
                                  for j, v in row.items()}
                break
            for j, v in pivots[column].items():
                new = row.get(j, 0) - value * v
                if prime is not None:
                    new %= prime
                if new:
                    row[j] = new
                else:
                    row.pop(j, None)
    return pivots


def integer_kernel(pivots, dimension):
    basis = []
    for free in sorted(set(range(dimension)) - pivots.keys()):
        vector = {free: Fraction(1)}
        for pivot in sorted(pivots, reverse=True):
            value = -sum(v * vector.get(j, 0) for j, v in pivots[pivot].items() if j != pivot)
            if value:
                vector[pivot] = value
        denominator = lcm(*(v.denominator for v in vector.values()))
        integers = {j: int(v * denominator) for j, v in vector.items()}
        divisor = gcd(*integers.values())
        basis.append({j: v // divisor for j, v in integers.items()})
    return basis


def entries(vector, dimension):
    return [[*divmod(j, dimension), value] for j, value in sorted(vector.items())]


def matrix(vector, dimension):
    return sp.SparseMatrix(dimension, dimension, {divmod(j, dimension): v for j, v in vector.items()})


def vector(matrix):
    return {i * matrix.cols + j: int(v) for (i, j), v in matrix.todok().items()}


def verify_basis(rows, basis):
    assert all(sum(value * generator.get(j, 0) for j, value in row.items()) == 0
               for generator in basis for row in rows)


def root_certificate(basis):
    diagonal = [matrix(v, 27) for v in basis if all(j % 28 == 0 for j in v)]
    assert len(diagonal) == 6
    weights = [tuple(int(h[i, i]) for h in diagonal) for i in range(27)]
    assert len(set(weights)) == 27
    root_spaces = {}
    for v in basis:
        if all(j % 28 == 0 for j in v):
            continue
        characters = {tuple(a - b for a, b in zip(weights[i], weights[j]))
                      for i, j, _ in entries(v, 27)}
        assert len(characters) == 1
        root = characters.pop()
        assert any(root) and root not in root_spaces
        root_spaces[root] = matrix(v, 27)
    assert len(root_spaces) == 72
    for root, generator in root_spaces.items():
        opposite = root_spaces[tuple(-x for x in root)]
        assert generator.T == opposite or generator.T == -opposite
    positive = {r for r in root_spaces if next(x for x in r if x) > 0}
    sums = {tuple(a + b for a, b in zip(r, s)) for r in positive for s in positive}
    simple = sorted(positive - sums)
    assert len(simple) == 6
    raising = [root_spaces[r] for r in simple]
    coroots = [e * e.T - e.T * e for e in raising]
    cartan = sp.zeros(6)
    for i, h in enumerate(coroots):
        for j, e in enumerate(raising):
            u, v = next(iter(e.todok()))
            cartan[i, j] = h[u, u] - h[v, v]
            assert h * e - e * h == cartan[i, j] * e
    assert cartan.det() == 3 and cartan == cartan.T
    assert all(cartan[i, i] == 2 for i in range(6))
    assert all(cartan[i, j] in (0, -1) for i in range(6) for j in range(6) if i != j)
    reference = sp.Matrix([[2,-1,0,0,0,0],[-1,2,-1,0,0,0],[0,-1,2,-1,-1,0],
                           [0,0,-1,2,0,0],[0,0,-1,0,2,-1],[0,0,0,0,-1,2]])
    assert any(cartan.extract(order, order) == reference for order in permutations(range(6)))
    for i, e in enumerate(raising):
        for j, f in enumerate(raising):
            assert e * f.T - f.T * e == (coroots[i] if i == j else sp.zeros(27))
            if i != j:
                commutator = e * f - f * e
                if cartan[i, j] == -1:
                    assert commutator != sp.zeros(27)
                    commutator = e * commutator - commutator * e
                assert commutator == sp.zeros(27)
    assert sp.Matrix.hstack(*(h.reshape(729, 1) for h in coroots)).rank() == 6
    return weights, list(root_spaces.values()), dict(
        simple_root_weights=simple, cartan_matrix=[[int(x) for x in row] for row in cartan.tolist()],
        simple_raising=[entries(vector(e), 27) for e in raising],
        simple_coroots=[entries(vector(h), 27) for h in coroots],
        transpose_preserves_stabilizer=True, simple_serre_checks=True)


def cubic_invariant_rank(terms, root_matrices, alternating):
    """Restrict to Cartan weight zero and impose the remaining generators."""
    rows = []
    for generator in root_matrices:
        replacements = defaultdict(list)
        for (i, j), value in generator.todok().items():
            replacements[i].append((j, int(value)))
        block = defaultdict(Counter)
        for index, term in enumerate(terms):
            for position, i in enumerate(term):
                for j, value in replacements[i]:
                    word = term[:position] + (j,) + term[position + 1:]
                    if alternating and len(set(word)) < 3:
                        continue
                    block[tuple(sorted(word))][index] += value * (parity(word) if alternating else 1)
        rows.extend(block.values())
    return len(echelon(rows))


def alternating_terms(terms):
    return {tuple(3 * i + a for i, a in zip(term, phases)): sign * parity(phases)
            for term, sign in terms.items() for phases in permutations(range(3))}


@lru_cache(None)
def calculate():
    terms = signed_terms(CUBIC)
    assert terms == signed_terms(ARCHIVE) and len(terms) == 45
    rows27 = coefficient_rows(terms, 27)
    pivots = echelon(rows27)
    basis = integer_kernel(pivots, 729)
    assert len(pivots) == 651 and len(basis) == 78
    verify_basis(rows27, basis)
    weights, roots, structure = root_certificate(basis)
    terms81 = alternating_terms(terms)
    rows81 = coefficient_rows(terms81, 81, alternating=True)
    family = [sp.SparseMatrix(3, 3, {(i, j): 1}) for i in range(3) for j in range(3) if i != j]
    family.extend([sp.diag(1,-1,0), sp.diag(0,1,-1)])
    lift = [vector(sp.kronecker_product(matrix(v, 27), sp.eye(3))) for v in basis]
    lift.extend(vector(sp.kronecker_product(sp.eye(27), a)) for a in family)
    verify_basis(rows81, lift)
    assert len(echelon(lift, 101)) == 86
    rank81 = len(echelon(rows81, 101))
    assert rank81 == 6475
    zero_weight = [term for term in combinations_with_replacement(range(27), 3)
                   if all(sum(weights[i][j] for i in term) == 0 for j in range(6))]
    assert set(zero_weight) == set(terms)
    sym_rank = cubic_invariant_rank(zero_weight, roots, alternating=False)
    alt_rank = cubic_invariant_rank(zero_weight, roots, alternating=True)
    assert (sym_rank, alt_rank) == (44,45)
    assert all(sum(w[i]*w[j]*w[k] for w in weights) == 0
               for i, j, k in combinations_with_replacement(range(6),3))
    family_probe = sp.diag(1,1,-2)
    assert sp.trace(family_probe**3) == -6
    assert sp.trace(sp.kronecker_product(sp.eye(27),family_probe)**3) == -162
    paths = [CUBIC, ARCHIVE, str(Path(__file__).relative_to(ROOT)).replace('\\','/')]
    return dict(status='EXACT_SIGNED_CUBIC_AND_ALTERNATING_TENSOR_STABILIZERS',
        cubic_27=dict(terms=len(terms), equation_rows=len(rows27), rank_over_Q=len(pivots),
                      generators=[entries(v,27) for v in basis], root_structure=structure),
        alternating_81=dict(terms=len(terms81), equation_rows=len(rows81),
                            exact_rank=rank81, modular_prime=101, independent_exact_kernel_generators=len(lift),
                            lift='T tensor I3 plus I27 tensor S, with T from the serialized basis and traceless S.'),
        invariants=dict(zero_weight_terms=len(zero_weight), symmetric_27_cubic_rank=sym_rank,
                        alternating_27_cubic_rank=alt_rank, single_commuting_81_holomorphic_cubic_dimension=0,
                        three_species_alternating_81_coupling='T(X1,X2,X3) with independent fields.'),
        anomalies=dict(E6_cartan_cubic_trace_identically_zero=True, family_probe_diagonal=[1,1,-2],
                       fundamental_family_probe_trace=-6, chiral_81_family_probe_trace=-162,
                       normalized_external_SU3_anomaly=27, prior_owner='Pass11613 and October1 decuplet work.'),
        scope='Infinitesimal stabilizers over characteristic zero, their compact unitary forms and a perturbative chiral anomaly check. No matter vacuum or dynamical gauge action is specified.',
        raw_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths})


if __name__ == '__main__':
    result = calculate()
    (ROOT / OUT).write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k in ('alternating_81','invariants','anomalies')}))
