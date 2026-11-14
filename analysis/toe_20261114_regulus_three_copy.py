"""Exact three-copy symmetric relaxation of the shortened F8 regulus."""

import json
from collections import Counter
from itertools import combinations, combinations_with_replacement, permutations, product
from pathlib import Path

import numpy as np
import sympy as sp

from toe_20261114_regulus_bell import STABILIZER, determinant, pairing, representative


OUT = Path(__file__).resolve().parents[1] / "data/toe_20261114_regulus_three_copy.json"


def logical_terms():
    centralizer = [v for v in range(4096) if not any(pairing(v, s) for s in STABILIZER)]
    labels = {representative(v) for v in centralizer}
    weights = Counter(representative(v) for v in centralizer if v and not determinant(v & 63, v >> 6))
    x_axes, z_axes = [], []
    while labels != {0}:
        x = min(labels - {0})
        z = min(v for v in labels if pairing(x, v))
        x_axes.append(x)
        z_axes.append(z)
        labels = {v for v in labels if not (pairing(x, v) or pairing(z, v))}
    assert len(x_axes) == 4

    def mask(v, axes):
        return sum(pairing(v, axis) << i for i, axis in enumerate(axes))

    return [(mask(v, z_axes), mask(v, x_axes), w) for v, w in weights.items()]


def calculate():
    terms = logical_terms()
    triples = [t for t in combinations_with_replacement(range(16), 3)
               if t[0] ^ t[1] ^ t[2] == 0]
    index = {t: i for i, t in enumerate(triples)}
    sizes = [len(set(permutations(t))) for t in triples]
    gram = np.zeros((len(triples), len(triples)), dtype=np.int64)
    for j, t in enumerate(triples):
        for source in set(permutations(t)):
            for a, b in combinations(range(3), 2):
                for x, z, weight in terms:
                    destination = list(source)
                    destination[a] ^= x
                    destination[b] ^= x
                    sign = (-1)**((z & (source[a] ^ source[b] ^ x)).bit_count())
                    gram[index[tuple(sorted(destination))], j] += weight*sign
    np.testing.assert_array_equal(gram, gram.T)
    assert len(triples) == 51 and len(triples)*16 == 816
    # These basis vectors are orbit sums, with squared norms sizes.
    metric = sp.diag(*sizes)
    multiple = metric.inv() * sp.Matrix(gram.tolist())
    characteristic = multiple.charpoly().as_poly()
    fac = sp.factor_list(characteristic)
    intervals = characteristic.intervals(eps=sp.Rational(1, 10**9))
    lower, upper = intervals[0][0]
    assert -16 < lower < upper < -15

    # Produce a short explicit rational negative witness as well.
    best = min((int(gram[i,i]+gram[j,j]-2*abs(gram[i,j])),
                i,j) for i,j in combinations(range(len(triples)),2))
    numerator, i, j = best
    assert numerator < 0
    marginal = pair_ppt_witness(terms, triples, index, sizes)
    return dict(status="PASS", symmetric_dimension=816, identical_blocks=16,
                reduced_dimension=len(triples),
                factors_for_three_times_objective=[[str(poly.as_expr()), power] for poly, power in fac[1]],
                relaxed_minimum_interval=[str(lower/3), str(upper/3)],
                approximate_minimum=float((lower+upper)/6),
                pair_marginal_ppt=marginal,
                two_term_witness=dict(triples=[triples[i], triples[j]],
                                      signs=[1, -int(np.sign(gram[i,j]))],
                                      objective=str(sp.Rational(numerator, 3*(sizes[i]+sizes[j])))))


def pair_ppt_witness(terms, triples, index, sizes):
    witness_path = OUT.with_name("toe_20261114_regulus_three_copy_ppt.json")
    witness = json.loads(witness_path.read_text(encoding="utf-8"))
    denominator = witness["denominator"]
    numerator = sp.zeros(len(triples))
    for (i, j), value in zip(combinations_with_replacement(range(len(triples)), 2),
                             witness["upper_triangle"], strict=True):
        numerator[i, j] = numerator[j, i] = value
    assert denominator > 0
    assert sum(numerator[i, i]*size for i, size in enumerate(sizes)) == denominator
    _, pivots = numerator.LDLdecomposition()
    assert all(pivot > 0 for pivot in pivots.diagonal())

    expectations = []
    for x, z in product(range(16), repeat=2):
        matrix = np.zeros((len(triples), len(triples)), dtype=np.int64)
        for j, t in enumerate(triples):
            for a, b, c in set(permutations(t)):
                target = tuple(sorted((a ^ x, b ^ x, c)))
                matrix[index[target], j] += (-1)**((z & (a ^ b ^ x)).bit_count())
        assert np.array_equal(matrix, matrix.T)
        expectations.append(sum(int(a)*b for a, b in zip(matrix.flat, numerator)))
    assert min(expectations) == 0
    assert sum(w*expectations[16*x+z] for x, z, w in terms) == 0
    return dict(objective=0, denominator=denominator,
                exact_positive_pivots=len(triples),
                zero_partial_transpose_eigenvalues=expectations.count(0))


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(result, flush=True)
