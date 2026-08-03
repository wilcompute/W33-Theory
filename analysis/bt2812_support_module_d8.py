#!/usr/bin/env python3
from __future__ import annotations

from fractions import Fraction
import json

MASKS = tuple(range(1, 16))
INDEX = {m: i for i, m in enumerate(MASKS)}
TAU = (2, 3, 0, 1)
R = (1, 2, 3, 0)
S = (0, 3, 2, 1)


def compose(p, q):
    return tuple(p[q[i]] for i in range(4))


def power(p, n):
    out = tuple(range(4))
    for _ in range(n):
        out = compose(p, out)
    return out


def permute_mask(mask, p):
    out = 0
    for i in range(4):
        if mask & (1 << i):
            out |= 1 << p[i]
    return out


def matrix_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def matrix_add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def matrix_scale(c, a):
    return [[c * x for x in row] for row in a]


def identity(n):
    return [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def permutation_matrix(p):
    n = len(MASKS)
    out = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for m in MASKS:
        out[INDEX[permute_mask(m, p)]][INDEX[m]] = Fraction(1)
    return out


def nonzero_zero_sum_count(q, r):
    return ((q - 1) ** r + (q - 1) * ((-1) ** r)) // q


def q_entry(q, S, T):
    Sm = {i for i in range(4) if S & (1 << i)}
    Tm = {i for i in range(4) if T & (1 << i)}
    tauS = {TAU[i] for i in Sm}
    r = len(Tm & tauS)
    t = len(Tm)
    N = nonzero_zero_sum_count(q, r)
    numerator = (q - 1) ** (t - r) * N
    assert numerator % (q - 1) == 0
    return numerator // (q - 1) - int(S == T)


def quotient(q):
    return [[Fraction(q_entry(q, S, T)) for T in MASKS] for S in MASKS]


def projector(Q, lam, others):
    I = identity(len(Q))
    out = I
    den = Fraction(1)
    for mu in others:
        out = matrix_mul(out, matrix_add(Q, matrix_scale(-mu, I)))
        den *= lam - mu
    return matrix_scale(1 / den, out)


def d8_elements():
    elems = {}
    for i in range(4):
        ri = power(R, i)
        elems[f'r{i}'] = ri
        elems[f'r{i}s'] = compose(ri, S)
    assert len(set(elems.values())) == 8
    return elems


CLASSES = {
    '1': ['r0'],
    'r2': ['r2'],
    'r13': ['r1', 'r3'],
    's_even': ['r0s', 'r2s'],
    's_odd': ['r1s', 'r3s'],
}
IRREPS = {
    'A1': [1, 1, 1, 1, 1],
    'A2': [1, 1, 1, -1, -1],
    'B1': [1, 1, -1, 1, -1],
    'B2': [1, 1, -1, -1, 1],
    'E': [2, -2, 0, 0, 0],
}
CLASS_SIZES = [1, 1, 2, 2, 2]


def decompose(char):
    out = {}
    for name, irr in IRREPS.items():
        inner = sum(size * c * x for size, c, x in zip(CLASS_SIZES, char, irr)) // 8
        assert inner >= 0
        if inner:
            out[name] = inner
    return out


def char_on_projector(P, elem_matrices):
    values = []
    for cls, names in CLASSES.items():
        traces = [trace(matrix_mul(elem_matrices[name], P)) for name in names]
        assert len(set(traces)) == 1, (cls, traces)
        assert traces[0].denominator == 1
        values.append(int(traces[0]))
    return values


def main():
    elems = d8_elements()
    mats = {name: permutation_matrix(p) for name, p in elems.items()}
    rows = []
    expected = {
        'trivial': {'character': [1, 1, 1, 1, 1], 'decomposition': {'A1': 1}},
        'positive': {'character': [9, 1, 1, 3, 3], 'decomposition': {'A1': 3, 'B1': 1, 'B2': 1, 'E': 2}},
        'negative': {'character': [5, 1, -1, 3, -1], 'decomposition': {'A1': 1, 'B1': 2, 'E': 1}},
    }

    for q in (2, 3, 5, 7, 11):
        Q = quotient(q)
        k, rp, rm = q * (q + 1), q - 1, -(q + 1)
        commute = all(matrix_mul(M, Q) == matrix_mul(Q, M) for M in mats.values())
        projectors = {
            'trivial': projector(Q, k, (rp, rm)),
            'positive': projector(Q, rp, (k, rm)),
            'negative': projector(Q, rm, (k, rp)),
        }
        row = {'q': q, 'commutes_with_D8': commute, 'sectors': {}}
        for sector, P in projectors.items():
            char = char_on_projector(P, mats)
            dec = decompose(char)
            rank = trace(P)
            assert rank.denominator == 1
            row['sectors'][sector] = {
                'dimension': int(rank),
                'character': char,
                'decomposition': dec,
                'idempotent': matrix_mul(P, P) == P,
            }
            assert char == expected[sector]['character']
            assert dec == expected[sector]['decomposition']
        rows.append(row)

    checks = {
        'five_q_values_exact': len(rows) == 5,
        'all_D8_commute': all(r['commutes_with_D8'] for r in rows),
        'all_projectors_idempotent': all(s['idempotent'] for r in rows for s in r['sectors'].values()),
        'dimensions_1_9_5': all([s['dimension'] for s in r['sectors'].values()] == [1, 9, 5] for r in rows),
        'q_independent_characters': all(r['sectors'] == rows[0]['sectors'] for r in rows[1:]),
        'total_dimension_15': 5 + 3 + 1 + 2 * 3 == 15,
        'no_A2_sector': all('A2' not in s['decomposition'] for r in rows for s in r['sectors'].values()),
    }
    assert all(checks.values()), [k for k, v in checks.items() if not v]

    out = {
        'schema': 'w33.bt2812.support_module_d8.v1',
        'status': 'COMPLETE_EXACT',
        'group': 'D8 stabilizer of one perfect matching of four coordinates',
        'class_order': list(CLASSES),
        'sector_theorem': {
            'eigenvalue_q_qplus1': expected['trivial'],
            'eigenvalue_qminus1': expected['positive'],
            'eigenvalue_minus_qplus1': expected['negative'],
            'total_support_module': {'A1': 5, 'B1': 3, 'B2': 1, 'E': 3},
        },
        'q_rows': rows,
        'checks': checks,
        'check_count': len(checks),
        'reading': 'The 15-dimensional binary-support shell is a q-independent D8 module. Its W(3,q) quotient eigenspaces decompose as A1; 3A1+B1+B2+2E; and A1+2B1+E.',
        'boundary': 'This is a module for the matching stabilizer D8, not an invariant 15-dimensional module for the full symplectic group.',
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
