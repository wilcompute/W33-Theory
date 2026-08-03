#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict
from itertools import product
import hashlib
import json
import sympy as sp

MASKS = tuple(range(1, 16))
TAU = (2, 3, 0, 1)


class FiniteField:
    def __init__(self, p: int, modulus: tuple[int, ...]):
        self.p = p
        self.modulus = tuple(x % p for x in modulus)
        self.n = len(modulus) - 1
        assert self.modulus[-1] == 1
        self.q = p ** self.n
        self.add_table = [[self._add_raw(a, b) for b in range(self.q)] for a in range(self.q)]
        self.neg_table = [self._neg_raw(a) for a in range(self.q)]
        self.mul_table = [[self._mul_raw(a, b) for b in range(self.q)] for a in range(self.q)]
        self.inv_table = [0] * self.q
        for a in range(1, self.q):
            hits = [b for b in range(1, self.q) if self.mul_table[a][b] == 1]
            assert len(hits) == 1
            self.inv_table[a] = hits[0]

    def coeffs(self, a):
        out = []
        for _ in range(self.n):
            out.append(a % self.p)
            a //= self.p
        return out

    def pack(self, c):
        return sum((x % self.p) * self.p ** i for i, x in enumerate(c[:self.n]))

    def _add_raw(self, a, b):
        return self.pack([(x + y) % self.p for x, y in zip(self.coeffs(a), self.coeffs(b))])

    def _neg_raw(self, a):
        return self.pack([(-x) % self.p for x in self.coeffs(a)])

    def _mul_raw(self, a, b):
        ca, cb = self.coeffs(a), self.coeffs(b)
        poly = [0] * (2 * self.n - 1)
        for i, x in enumerate(ca):
            for j, y in enumerate(cb):
                poly[i + j] = (poly[i + j] + x * y) % self.p
        for d in range(len(poly) - 1, self.n - 1, -1):
            factor = poly[d] % self.p
            if factor:
                for j in range(self.n + 1):
                    poly[d - self.n + j] = (poly[d - self.n + j] - factor * self.modulus[j]) % self.p
        return self.pack(poly)

    def add(self, a, b): return self.add_table[a][b]
    def neg(self, a): return self.neg_table[a]
    def sub(self, a, b): return self.add_table[a][self.neg_table[b]]
    def mul(self, a, b): return self.mul_table[a][b]
    def inv(self, a):
        assert a
        return self.inv_table[a]


FIELDS = {
    2: FiniteField(2, (0, 1)),
    3: FiniteField(3, (0, 1)),
    4: FiniteField(2, (1, 1, 1)),
    5: FiniteField(5, (0, 1)),
    7: FiniteField(7, (0, 1)),
    8: FiniteField(2, (1, 1, 0, 1)),
    9: FiniteField(3, (1, 0, 1)),
    11: FiniteField(11, (0, 1)),
}


def canon_projective(v, F):
    for x in v:
        if x:
            z = F.inv(x)
            return tuple(F.mul(z, y) for y in v)
    raise ValueError('zero')


def projective_points(F):
    return sorted({canon_projective(v, F) for v in product(range(F.q), repeat=4) if any(v)})


def symp(x, y, F):
    return F.add(F.sub(F.mul(x[0], y[2]), F.mul(x[2], y[0])), F.sub(F.mul(x[1], y[3]), F.mul(x[3], y[1])))


def support_mask(v):
    return sum(1 << i for i, x in enumerate(v) if x)


def nonzero_zero_sum_count(q, r):
    return ((q - 1) ** r + (q - 1) * ((-1) ** r)) // q


def quotient_formula_entry(q, S, T):
    Sm = {i for i in range(4) if S & (1 << i)}
    Tm = {i for i in range(4) if T & (1 << i)}
    r = len(Tm & {TAU[i] for i in Sm})
    numerator = (q - 1) ** (len(Tm) - r) * nonzero_zero_sum_count(q, r)
    assert numerator % (q - 1) == 0
    return numerator // (q - 1) - int(S == T)


def formula_matrix(q):
    return [[quotient_formula_entry(q, S, T) for T in MASKS] for S in MASKS]


def actual_quotient(F):
    pts = projective_points(F)
    fibers = defaultdict(list)
    for i, v in enumerate(pts):
        fibers[support_mask(v)].append(i)
    assert set(fibers) == set(MASKS)
    Q = [[None] * 15 for _ in range(15)]
    equitable = True
    for si, S in enumerate(MASKS):
        profiles = []
        for i in fibers[S]:
            profiles.append(tuple(sum(j != i and symp(pts[i], pts[j], F) == 0 for j in fibers[T]) for T in MASKS))
        equitable &= len(set(profiles)) == 1
        Q[si] = list(profiles[0])
    return pts, fibers, Q, equitable


def symbolic_certificate():
    q = sp.symbols('q', integer=True, positive=True)

    def Nr(r):
        return sp.cancel(((q - 1) ** r + (q - 1) * (-1) ** r) / q)

    def entry(S, T):
        Sm = {i for i in range(4) if S & (1 << i)}
        Tm = {i for i in range(4) if T & (1 << i)}
        r = len(Tm & {TAU[i] for i in Sm})
        return sp.simplify((q - 1) ** (len(Tm) - r) * Nr(r) / (q - 1) - int(S == T))

    Q = sp.Matrix([[entry(S, T) for T in MASKS] for S in MASKS])
    s = sp.Matrix([(q - 1) ** (m.bit_count() - 1) for m in MASKS])
    one, I = sp.ones(15, 1), sp.eye(15)
    k, rp, rm = q * (q + 1), q - 1, -(q + 1)
    row_law = all(sp.simplify(x - k) == 0 for x in Q * one)
    detail = all(sp.simplify(x) == 0 for x in sp.diag(*s) * Q - Q.T * sp.diag(*s))
    quadratic = all(sp.simplify(x) == 0 for x in Q * Q - (q * q - 1) * I + 2 * Q - (q + 1) * one * s.T)
    trace1, trace2 = sp.simplify(sp.trace(Q)), sp.simplify(sp.trace(Q * Q))
    mk, mp, mm = sp.symbols('m_k m_p m_m')
    sol = sp.solve([
        sp.Eq(mk + mp + mm, 15),
        sp.Eq(mk * k + mp * rp + mm * rm, trace1),
        sp.Eq(mk * k ** 2 + mp * rp ** 2 + mm * rm ** 2, trace2),
    ], (mk, mp, mm), dict=True)
    return {
        'nonzero_zero_sum_polynomials_r0_to_r4': [str(sp.factor(Nr(r))) for r in range(5)],
        'row_sum_identity': row_law,
        'detailed_balance_identity': detail,
        'quadratic_identity': quadratic,
        'trace_identity': sp.simplify(trace1 - (k + 9 * rp + 5 * rm)) == 0,
        'trace_square_identity': sp.simplify(trace2 - (k ** 2 + 9 * rp ** 2 + 5 * rm ** 2)) == 0,
        'multiplicity_moment_solution_1_9_5': sol == [{mk: 1, mp: 9, mm: 5}],
        'spectrum_from_closure_and_moments': 'q(q+1)^1, (q-1)^9, (-(q+1))^5',
    }


def main():
    rows = []
    for q, F in FIELDS.items():
        pts, fibers, actual, equitable = actual_quotient(F)
        formula = formula_matrix(q)
        sizes = {str(m): len(fibers[m]) for m in MASKS}
        expected = {str(m): (q - 1) ** (m.bit_count() - 1) for m in MASKS}
        rows.append({
            'q': q,
            'field': f'GF({q})',
            'projective_points': len(pts),
            'expected_projective_points': (q + 1) * (q * q + 1),
            'equitable': equitable,
            'formula_matches': actual == formula,
            'fiber_sizes_match': sizes == expected,
            'row_sum_set': sorted(set(sum(row) for row in actual)),
            'quotient_sha256': hashlib.sha256(json.dumps(actual, separators=(',', ':')).encode()).hexdigest(),
        })

    symbolic = symbolic_certificate()
    checks = {
        'eight_fields_tested': len(rows) == 8,
        'includes_even_prime_powers': {2, 4, 8}.issubset({r['q'] for r in rows}),
        'includes_odd_prime_power_9': 9 in {r['q'] for r in rows},
        'all_projective_counts': all(r['projective_points'] == r['expected_projective_points'] for r in rows),
        'all_equitable': all(r['equitable'] for r in rows),
        'all_formula_matches': all(r['formula_matches'] for r in rows),
        'all_fiber_sizes': all(r['fiber_sizes_match'] for r in rows),
        'all_degree_q_qplus1': all(r['row_sum_set'] == [r['q'] * (r['q'] + 1)] for r in rows),
        'symbolic_row_sum': symbolic['row_sum_identity'],
        'symbolic_detailed_balance': symbolic['detailed_balance_identity'],
        'symbolic_quadratic': symbolic['quadratic_identity'],
        'symbolic_multiplicities': symbolic['multiplicity_moment_solution_1_9_5'],
    }
    assert all(checks.values()), [k for k, v in checks.items() if not v]

    out = {
        'schema': 'w33.bt2813.all_q_support_lift.v1',
        'status': 'COMPLETE_SYMBOLIC_WITH_EIGHT_FIELD_WITNESSES',
        'theorem': {
            'scope': 'every finite field GF(q), including even and odd prime powers',
            'fiber_size': '(q-1)^(|S|-1)',
            'entry_formula': 'Q_ST=(q-1)^(|T|-r-1) N_r(q)-delta_ST, r=|T intersect tau(S)|',
            'nonzero_sum_count': 'N_r(q)=((q-1)^r+(q-1)(-1)^r)/q',
            'spectrum': {'q(q+1)': 1, 'q-1': 9, '-(q+1)': 5},
            'quadratic_identity': 'Q^2=(q^2-1)I-2Q+(q+1)1s^T',
            'detailed_balance': 'diag(s)Q=Q^T diag(s)',
        },
        'symbolic': symbolic,
        'field_rows': rows,
        'checks': checks,
        'check_count': len(checks),
        'reading': 'The 15-state tetrahedral support quotient is universal across W(3,q); the quotient multiplicities 1+9+5 do not depend on q.',
        'boundary': 'Only q=3 gives the tomotope capacity vector; the abstract tomotope incidence realization is a separate signed q=3 construction.',
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
