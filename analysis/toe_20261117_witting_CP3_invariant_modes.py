"""Exact Witting invariant-mode test for the CP3 compactification.

Reuse the ray construction in exploration/w33_witting_srg_bridge.py.
The physics interpretation is conditional on Martin-Reall's KK spectrum;
an invariant subsector is not by itself a complete orbifold vacuum.
"""
import json
from collections import Counter, deque
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path

import numpy as np
import sympy as sp

W = sp.Symbol('w')
POLY = sp.Poly(W**2+W+1, W)
PAIRS = list(combinations(range(4), 2))


def red(value):
    return sp.rem(sp.Poly(sp.expand(value), W), POLY).as_expr()


def clean(matrix):
    return matrix.applyfunc(red)


def exterior(matrix):
    return clean(sp.Matrix(6, 6, lambda i, j: matrix.extract(PAIRS[i], PAIRS[j]).det()))


def exact_rays():
    rays = [sp.eye(4)[:, i] for i in range(4)]
    for a, b in product(range(3), repeat=2):
        rays += [sp.Matrix(v) for v in ((0, 1, -W**a, W**b),
                 (1, 0, -W**a, -W**b), (1, -W**a, 0, W**b), (1, W**a, W**b, 0))]
    return rays


def generators():
    vectors = [sp.eye(4)[:, i] for i in range(4)]
    vectors += [sp.Matrix(v) for v in ((0, 1, -1, 1), (1, 0, -1, -1),
                                      (1, -1, 0, 1), (1, 1, 1, 0))]
    result = []
    for v in vectors:
        reflection = sp.eye(4)+(W-1)*v*v.T/(v.T*v)[0]
        # det R=w. Multiplication by w^2 gives det U=w^9=1.
        u = clean(W**2*reflection)
        assert red(u.det()) == 1 and clean(u**3) == sp.eye(4)
        conjugate = u.applyfunc(lambda x: red(x.subs(W, W**2)))
        assert clean(conjugate.T*u) == sp.eye(4)
        result.append(u)
    return result


def wedge_pairing():
    j = sp.zeros(6)
    for i, (a, b) in enumerate(PAIRS):
        for k, (c, d) in enumerate(PAIRS):
            if len({a, b, c, d}) == 4:
                sequence = (a, b, c, d)
                inversions = sum(sequence[s] > sequence[t] for s in range(4) for t in range(s+1, 4))
                j[i, k] = (-1)**inversions
    assert j*j == sp.eye(6)
    return j


def symmetric_basis():
    pairs = [(i, j) for i in range(6) for j in range(i, 6)]
    basis = []
    for i, j in pairs:
        s = sp.zeros(6)
        s[i, j] = s[j, i] = 1
        basis.append(s)
    return pairs, basis


def modular(matrix, prime=7, root=2):
    assert (root*root+root+1) % prime == 0
    def entry(x):
        numerator, denominator = sp.fraction(sp.cancel(x.subs(W, root)))
        return int(numerator) * pow(int(denominator), -1, prime) % prime
    return np.array(matrix.applyfunc(entry).tolist(), dtype=np.int64)


def rank_mod(matrix, prime=7):
    a = np.array(matrix, dtype=np.int64) % prime
    row = 0
    for col in range(a.shape[1]):
        candidates = np.flatnonzero(a[row:, col])
        if not len(candidates):
            continue
        chosen = row+int(candidates[0])
        a[[row, chosen]] = a[[chosen, row]]
        a[row] = a[row]*pow(int(a[row, col]), -1, prime) % prime
        factors = a[row+1:, col].copy()
        a[row+1:] = (a[row+1:]-factors[:, None]*a[row]) % prime
        row += 1
        if row == min(a.shape):
            break
    return row


def invariant_calculation():
    group = generators()
    j = wedge_pairing()
    pairs, basis = symmetric_basis()
    constraints = []
    for u in group:
        g = exterior(u)
        assert clean(g.T*j*g) == j
        assert clean(g*j*g.T) == j
        columns = []
        for s in basis:
            image = clean(g*s*g.T-s)
            columns.append(sp.Matrix([image[a, b] for a, b in pairs]))
        constraints.append(sp.Matrix.hstack(*columns))
    stacked = sp.Matrix.vstack(*constraints)
    # Lower bound from a good finite-field specialization, upper bound from
    # the explicit invariant J. Together these prove exact characteristic-zero rank.
    rank = rank_mod(modular(stacked))
    assert rank == 20
    invariant = sp.Matrix([j[a, b] for a, b in pairs])
    assert clean(stacked*invariant) == sp.zeros(stacked.rows, 1)
    assert sp.trace(j*j) == 6

    # Construct the traceless symmetric 20 and adjoint 15 representations.
    keep20 = [pair for pair in pairs if pair != (2, 3)]
    basis20 = []
    for pair in keep20:
        s = basis[pairs.index(pair)].copy()
        if pair == (0, 5):
            s[2, 3] = s[3, 2] = -1
        elif pair == (1, 4):
            s[2, 3] = s[3, 2] = 1
        assert sp.trace(j*s) == 0
        basis20.append(s)
    keep15 = [(a, b) for a in range(4) for b in range(4) if (a, b) != (3, 3)]
    basis15 = []
    for a, b in keep15:
        s = sp.zeros(4)
        s[a, b] = 1
        if a == b:
            s[3, 3] = -1
        basis15.append(s)
    hom_constraints = []
    adjoint_constraints = []
    for u in group:
        g = exterior(u)
        image20 = [clean(g*s*g.T) for s in basis20]
        b20 = sp.Matrix(20, 20, lambda a, b: image20[b][keep20[a]])
        image15 = [clean(u*s*u**2) for s in basis15]
        a15 = sp.Matrix(15, 15, lambda a, b: image15[b][keep15[a]])
        aa, bb = modular(a15), modular(b20)
        adjoint_constraints.append(aa-np.eye(15, dtype=np.int64))
        hom_constraints.append(np.kron(bb, np.eye(15, dtype=np.int64))
                               -np.kron(np.eye(20, dtype=np.int64), aa.T))
    adjoint_rank = rank_mod(np.vstack(adjoint_constraints))
    hom_rank = rank_mod(np.vstack(hom_constraints))
    assert adjoint_rank == 15 and hom_rank == 300
    return dict(symmetric_21_constraint_rank=rank, invariant_21_dimension=1,
                invariant_tensor=[[int(x) for x in row] for row in j.tolist()], traceless_20_invariants=0,
                adjoint_15_constraint_rank=adjoint_rank,
                adjoint_15_invariants=15-adjoint_rank,
                Hom_15_to_20_constraint_rank=hom_rank,
                Hom_15_to_20_invariant_dimension_upper_bound=300-hom_rank,
                prime=7, omega_mod_prime=2,
                exact_scope='Full modular column rank proves absence in characteristic zero; '
                            'rank20 plus explicit invariant proves the symmetric21 fixed-space dimension.')


def ray_action_check():
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from exploration.w33_witting_srg_bridge import construct_witting_rays
    rays = np.array(construct_witting_rays())
    omega = np.exp(2j*np.pi/3)
    permutations = []
    reference_rays = exact_rays()
    def canonical(v):
        v = clean(v)
        pivot = next(x for x in v if x != 0)
        inverse = sp.invert(sp.Poly(pivot, W), POLY).as_expr()
        return tuple(red(x*inverse) for x in v)
    ray_index = {canonical(v): i for i, v in enumerate(reference_rays)}
    assert len(ray_index) == 40
    maximum = 0.
    for u in generators():
        matrix = np.array(u.subs(W, omega), complex)
        image = (matrix@rays.T).T
        overlaps = abs(image.conj()@rays.T)**2
        permutation = np.argmax(overlaps, axis=1)
        maximum = max(maximum, float(max(abs(overlaps[np.arange(40), permutation]-1))))
        assert len(set(permutation)) == 40 and maximum < 1e-12
        exact_permutation = [ray_index[canonical(u*v)] for v in reference_rays]
        assert exact_permutation == permutation.tolist()
        permutations.append(exact_permutation)
    seen = {tuple(range(40))}
    queue = deque(seen)
    while queue:
        current = queue.popleft()
        for generator in permutations:
            following = tuple(generator[i] for i in current)
            if following not in seen:
                seen.add(following)
                queue.append(following)
    assert len(seen) == 25920
    assert len({permutation[0] for permutation in seen}) == 40
    return dict(permutations=permutations, max_squared_overlap_error=maximum,
                exact_projective_permutation_group_order=len(seen),
                scope='Exact cyclotomic ray permutations and projective closure; '
                      'independent floating-point ordering check against existing rays.')


@lru_cache(None)
def schur_weights(partition):
    """Integral GL(n) character via multiplicity-free interlacing branching."""
    if len(partition) == 1:
        return Counter({partition: 1})
    result = Counter()
    for smaller in product(*(range(partition[i+1], partition[i]+1)
                             for i in range(len(partition)-1))):
        power = sum(partition)-sum(smaller)
        for weight, multiplicity in schur_weights(smaller).items():
            result[weight+(power,)] += multiplicity
    return result


def tensor_product_check():
    left = Counter()
    for a, x in schur_weights((2, 1, 1, 0)).items():
        for b, y in schur_weights((2, 2, 0, 0)).items():
            left[tuple(u+v for u, v in zip(a, b))] += x*y
    parts = ((4, 3, 1, 0), (4, 2, 1, 1), (3, 3, 2, 0),
             (3, 3, 1, 1), (3, 2, 2, 1))
    right = sum((schur_weights(part) for part in parts), Counter())
    assert left == right
    dimensions = [sum(schur_weights(part).values()) for part in parts]
    assert dimensions == [175, 45, 45, 20, 15]
    return dict(identity='15 tensor 20prime = 175+45+45bar+20prime+15',
                summand_dimensions=dimensions,
                method='Exact equality of GL4 weight multiplicities including determinant shifts.',
                massless_175_invariants=0,
                deduction='Hom(15,20prime) has no fixed vectors. Since the adjoint is self-dual, '
                          'the tensor product has no invariant; hence none of its summands do.')


def orbifold_branch_bookkeeping():
    rays = exact_rays()
    incidence = np.zeros((40, 40), dtype=np.int64)
    for a, v in enumerate(rays):
        conjugate = v.applyfunc(lambda x: red(x.subs(W, W**2)))
        for b, u in enumerate(rays):
            incidence[a, b] = int(red((conjugate.T*u)[0]) == 0)
    assert np.all(incidence.sum(axis=1) == 12)
    assert np.array_equal(incidence@incidence,
                          8*np.eye(40, dtype=np.int64)-2*incidence+4*np.ones((40, 40), dtype=np.int64))
    degrees = (12, 18, 24, 30)  # Established G32 invariant degrees, reused.
    weights = (2, 3, 4, 5)
    assert sum(d-1 for d in degrees) == 80 == 40*(3-1)
    # pi^*O_weighted(1)=O_CP3(6); branch discriminant pulls back to
    # three times the forty mirror hyperplanes, hence weighted degree20.
    branch_degree = sp.Rational(3*40, 6)
    log_canonical = -sum(weights)+sp.Rational(2, 3)*branch_degree
    assert branch_degree == 20 and log_canonical == -sp.Rational(2, 3)
    assert 6*log_canonical == -4
    weighted_intersection = sp.Rational(1, 2*3*4*5)
    assert 25920*weighted_intersection == 6**3
    assert (-log_canonical)**3*weighted_intersection == sp.Rational(4**3, 25920)
    return dict(coarse_quotient='P(2,3,4,5)', mirrors=40, generic_mirror_stabilizer_order=3,
                Witting_points_on_each_mirror=12, mirror_incidence=incidence.tolist(),
                G32_invariant_degrees=list(degrees), Jacobian_degree=80,
                branch_discriminant_weighted_degree=20,
                coarse_canonical_class='-14 H', branch_coefficient='2/3',
                orbifold_log_canonical_class='-(2/3) H', pullback_of_H='6 h',
                canonical_pullback_check='6[-14+(2/3)*20]h=-4h=K_CP3',
                log_anticanonical_cubic='1/405=64/25920',
                coordinate_reflection_fixed_loci=['CP2: z0=0', 'point: [1,0,0,0]'],
                scope='Coarse quotient identification uses the established G32 invariant-ring theorem. '
                      'Its branch divisor and quotient metric cannot be replaced by an unmarked weighted space.')


def same_coarse_space_control():
    """S5 in its standard 4D representation has the same coarse quotient.

    SU4 lifts of odd permutations need a scalar phase. The 20prime
    character therefore includes det(R)^(-1), while degree8 Schur431
    has det(R)^(-2)=1. Ignoring this twist gives a false comparison.
    """
    classes = (((1, 1, 1, 1, 1), 1), ((2, 1, 1, 1), 10), ((2, 2, 1), 15),
               ((3, 1, 1), 20), ((3, 2), 20), ((4, 1), 30), ((5,), 24))
    rows = []
    for cycles, count in classes:
        powers = {r: sum(d for d in cycles if r % d == 0)-1 for r in range(1, 8)}
        sign = (-1)**(5-len(cycles))
        chi6 = sp.Rational(powers[1]**2-powers[2], 2)
        chi6_square = sp.Rational(powers[2]**2-powers[4], 2)
        chi20 = sign*(chi6**2+chi6_square)/2-1
        chi15 = powers[1]**2-1
        complete = {0:sp.S.One}
        for n in range(1, 8):
            complete[n] = sum(powers[k]*complete[n-k] for k in range(1, n+1))/n
        partition = (4, 3, 1, 0)
        chi175 = sp.Matrix(4, 4, lambda a, b: complete.get(partition[a]-a+b, 0)).det()
        assert all(sp.sympify(value).is_Integer for value in (chi15, chi20, chi175))
        rows.append(dict(cycle_type=list(cycles), count=count,
                         char15=int(chi15), char20prime=int(chi20), char175=int(chi175)))
    fixed = {str(d): sum(row['count']*row['char'+('20prime' if d == 20 else str(d))]
                        for row in rows)//120 for d in (15, 20, 175)}
    for d in (15, 20, 175):
        key = 'char'+('20prime' if d == 20 else str(d))
        assert sum(row['count']*row[key] for row in rows) % 120 == 0
    assert fixed == {'15':0, '20':0, '175':1}
    return dict(group='S5, standard four-dimensional projective action',
                coarse_quotient='P(2,3,4,5)', irreducible_multiplet_fixed_dimensions=fixed,
                characters=rows, branch_weighted_degree=20, generic_branch_order=2,
                log_canonical_class='-14H+(1/2)*20H=-4H', pullback_of_H='h',
                quotient_volume_ratio_Witting_to_S5='120/25920=1/216',
                scope='Same coarse variety, different marked branch data and quotient metric. '
                      'No equality of physical compactifications follows.')


if __name__ == '__main__':
    result = dict(status='PASS', invariant_modes=invariant_calculation(),
                  ray_action=ray_action_check(),
                  tensor_product=tensor_product_check(),
                  orbifold_branch=orbifold_branch_bookkeeping(),
                  same_coarse_space_control=same_coarse_space_control(),
                  caveat='CP3 quotient has fixed loci. No localized-sector spectrum or '
                         'nonperturbative stability established.')
    output = Path(__file__).resolve().parents[1]/'data/toe_20261117_witting_CP3_invariant_modes.json'
    output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result['invariant_modes'], default=str))
