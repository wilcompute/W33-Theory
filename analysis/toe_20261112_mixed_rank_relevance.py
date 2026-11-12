"""Flavor-current bounds on raising the rank of the W33 mixed adjoint term."""

import json

import sympy as sp

import toe_20261112_canonical_uv_fixed_point as uv


OUT = 'data/toe_20261112_mixed_rank_relevance.json'


def family_only(family, dims):
    r, p, t, z = sp.symbols('r p t z', real=True)
    two_thirds = sp.Rational(2, 3)

    def trace(charges, parameter):
        assert sp.expand((family*(sp.Matrix(charges)-sp.ones(7, 1)))[0]) == -3
        return sp.expand(sum(dim*(q-1)*sp.diff(q, parameter)**2 for dim, q in zip(dims, charges)))

    s = 6-18*z/5
    rank_zero = trace([two_thirds]*3+[z]*2+[two_thirds, s], z)
    assert rank_zero.coeff(z) < 0 and rank_zero.subs(z, 1) > 0

    result = []
    for omega, upper in [(True, -two_thirds), (False, -sp.Rational(13, 7))]:
        mean = 1-p/2 if omega else 1-r/2
        charges = [mean+t, mean-t, p, 2-r-mean-t, 2-r-mean+t, r,
                   (12+18*r-9*p)/5]
        bare = trace(charges, p)
        assert bare.coeff(p) > 0 and bare.coeff(r) > 0
        assert bare.subs({p: upper, r: two_thirds}) == 0
        assert 3*upper < two_thirds
        # One surviving SU(3) baryon of three uncoupled X fields suffices.
        corrected = sp.expand(bare + 9*(two_thirds-3*p))
        assert corrected.coeff(p) < 0 and corrected.coeff(r) > 0
        assert corrected.subs({p: upper, r: two_thirds}) > 0
        result.append(dict(alternating_cubic=omega, bare_trace=str(bare),
                           uncoupled_X_strict_upper_bound=str(upper),
                           trace_with_one_free_baryon=str(corrected)))
    return dict(rank_zero_with_alternating_cubic_trace=str(rank_zero),
                rank_two_baryon_tests=result)


def calculate():
    r, q, x, u, z = sp.symbols('r q x u z', real=True)
    dims = [81]*5 + [78, 10]
    reps = uv.flat.read(uv.THETA)['spin_witness']['representations']
    bifundamental, adjoint, _, spectator = (
        sp.Matrix(2, 1, entry['basic_trace_indices']) / 2 for entry in reps.values()
    )
    indices = sp.Matrix.hstack(*([bifundamental]*5+[adjoint, spectator]))
    e6, family = indices[0, :], indices[1, :]
    su2_x = sp.Matrix([0, 1, -1, 0, 0, 0, 0])
    su2_z = sp.Matrix([0, 0, 0, 1, -1, 0, 0])
    q_phase = sp.Matrix([1, -sp.Rational(1, 2), -sp.Rational(1, 2), -1, 1, 0, 0])
    paired_phase = sp.Matrix([1, 0, 0, -1, 0, 0, 0])
    r_phase = sp.Matrix([0, 0, 0, -1, -sp.Rational(1, 3), 1, sp.Rational(12, 5)])
    omega = sp.Matrix([[1, 1, 1, 0, 0, 0, 0]])
    mixed = sp.Matrix([[1, 0, 0, 1, 0, 1, 0]])
    missing = sp.Matrix([[0, 1, 0, 0, 1, 1, 0]])

    def check(charges, currents, rank, alternating):
        charges = sp.Matrix(charges)
        assert sp.expand((e6 * (charges-sp.ones(7, 1)))[0]) == -12
        assert not alternating or sp.expand((omega * charges)[0]) == 2
        assert not rank or sp.expand((mixed * charges)[0]) == 2
        for current in currents:
            assert (e6 * current)[0] == (family * current)[0] == 0
            assert not alternating or (omega * current)[0] == 0
            assert not rank or (mixed * current)[0] == 0
        anomaly = sp.diag(*(dim*(charge-1) for dim, charge in zip(dims, charges)))
        return (sp.expand((missing * charges)[0] - 2),
                [sp.expand((current.T * anomaly * current)[0]) for current in currents])

    # The basic strict bounds use flavor currents that leave S neutral.
    s = sp.Symbol('s')
    pair = [q, 1-q/2, 1-q/2, 2-r-q, 1-r/3+q, r, s]
    gap, anomalies = check(pair, [su2_x, q_phase, 2*r_phase+3*q_phase], 1, True)
    assert gap == q/2 + 2*r/3
    assert anomalies[:2] == [-81*q, sp.Rational(243, 4)*q-108*r]
    both_active = (3+12*r)/5
    polynomial = sp.Poly(-anomalies[2].subs(s, both_active), q, r)
    q_coeff, r_coeff = polynomial.coeff_monomial(q), polynomial.coeff_monomial(r)
    threshold = -polynomial.coeff_monomial(1)
    scale = max(2*q_coeff, sp.Rational(3, 2)*r_coeff)
    bound = threshold/scale
    assert threshold > 0 and scale > 0 and bound > sp.Rational(2, 5)
    rows = [dict(rank=1, alternating_cubic=True, missing_R_minus_two=str(gap),
                 flavor_anomaly_polynomials=list(map(str, anomalies)),
                 strict_gap_lower_bound='0',
                 strict_gap_lower_bound_both_gauges_active=str(bound))]

    pair = [q, u, u, 2-r-q, 3-r/3-2*u, r, s]
    gap, anomalies = check(pair, [su2_x, paired_phase], 1, False)
    assert gap == 1-u+2*r/3 and anomalies == [162*(u-1), -81*r]
    rows.append(dict(rank=1, alternating_cubic=False, missing_R_minus_two=str(gap),
                     flavor_anomaly_polynomials=list(map(str, anomalies)), strict_gap_lower_bound='0'))

    common_x = sp.Rational(2, 3)
    common_z = sp.Rational(3, 2)-2*r/3
    gap, anomalies = check([common_x]*3+[common_z]*2+[r, s], [su2_z], 0, True)
    assert gap == sp.Rational(1, 6)+r/3
    assert anomalies == [81-108*r]
    rows.append(dict(rank=0, alternating_cubic=True, missing_R_minus_two=str(gap),
                     flavor_anomaly_polynomials=list(map(str, anomalies)), strict_gap_lower_bound='5/12'))

    r_zero = (15-9*x-6*z)/4
    gap, anomalies = check([x]*3+[z]*2+[r_zero, s], [su2_x, su2_z], 0, False)
    assert gap == sp.Rational(7, 4)-5*x/4-z/2
    assert anomalies == [162*x-162, 162*z-162]
    rows.append(dict(rank=0, alternating_cubic=False, missing_R_minus_two=str(gap),
                     flavor_anomaly_polynomials=list(map(str, anomalies)), strict_gap_lower_bound='0'))
    return dict(status='PASS', interacting_E6_rank_relevance=rows,
                family_only_fixed_point_tests=family_only(family, dims))


if __name__ == '__main__':
    result = json.dumps(calculate(), indent=2) + '\n'
    (uv.flat.ROOT / OUT).write_text(result, encoding='utf-8')
    print(result)
