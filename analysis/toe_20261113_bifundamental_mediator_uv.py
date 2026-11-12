"""Conserved-current obstruction for the bifundamental W33 mediator."""

import json

import sympy as sp

import toe_20261112_canonical_uv_fixed_point as uv


OUT = 'data/toe_20261113_bifundamental_mediator_uv.json'


def calculate():
    p, q, r, u, dual = sp.symbols('p q r u dual', real=True)
    dims = [81]*7 + [78, 10]
    entries = uv.flat.read(uv.THETA)['spin_witness']['representations']
    bifundamental, adjoint, family_adjoint, spectator = (
        sp.Matrix(entry['basic_trace_indices'])/2 for entry in entries.values()
    )
    gauge = sp.Matrix.hstack(*([bifundamental]*7+[adjoint, spectator]))
    c2 = adjoint + family_adjoint
    su2 = sp.Matrix([0, 0, 1, -1, 0, 0, 0, 0, 0])
    cases = []
    for omega in (True, False):
        unpaired = 1-p/2 if omega else u
        d = 1+p+2*r/3 if omega else 3+2*r/3-2*u
        charges = sp.Matrix([p, q, unpaired, unpaired, 2-r-p, 2-r-q, d, r, (3+12*r)/5])
        assert sp.simplify(gauge*(charges-sp.ones(9, 1))+c2) == sp.zeros(2, 1)
        assert sp.expand(charges[0]+charges[4]+r) == 2
        assert sp.expand(charges[1]+charges[5]+r) == 2
        assert not omega or sp.expand(charges[0]+charges[2]+charges[3]) == 2
        anomaly = sp.diag(*(dim*(charge-1) for dim, charge in zip(dims, charges)))

        def trace(current, e6_only=False):
            assert (gauge*current)[0] == 0
            assert e6_only or (gauge*current)[1] == 0
            return sp.expand((current.T*anomaly*current)[0])

        assert trace(charges.diff(q)) == -81*r
        assert trace(su2) == (-81*p if omega else 162*u-162)
        missing_gap = sp.expand(d+unpaired-2)
        if omega:
            assert trace(charges.diff(p)) == sp.Rational(243, 4)*p-27*r
            current = charges.diff(p)+charges.diff(r)-charges.diff(q)/2
            forbidden = trace(current)
            assert sp.expand(forbidden+sp.Rational(3, 100)*(1275*p-733*r-4732)) == 0
            # p < 4r/9 from the p current makes the forbidden trace positive.
            assert forbidden.coeff(p) < 0
            lower = sp.expand(forbidden.subs(p, 4*r/9))
            assert lower.coeff(r) > 0 and lower.subs(r, 0) > 0
            # With the family coupling zero, omit the spectator phase.
            current[8] = 0
            e6_only_trace = trace(current, e6_only=True)
            e6_lower = sp.expand(e6_only_trace.subs(p, 4*r/9))
            r_bound = sp.solve(e6_lower, r)[0]
            assert r_bound == sp.Rational(660, 533)
            assert missing_gap == p/2+2*r/3
            # The second mass DU is also irrelevant. Use the Schur
            # complement of the q flavor direction for the E6-only r current.
            rq_current = charges.diff(r)
            rq_current[8] = 0
            q_current = charges.diff(q)
            cross = (rq_current.T*anomaly*q_current)[0]
            schur = trace(rq_current, e6_only=True)-cross**2/trace(q_current)
            x = sp.symbols('x', real=True)
            schur_x = sp.expand(schur.subs(q, 1-r/2+r*x/2))
            assert sp.expand(schur_x-sp.Rational(3, 4)*(4+r-60*p+27*r*x*x)) == 0
            p_floor = (4+r+27*r*x*x)/60
            mass_gap = sp.expand((d+q-2).subs(q, 1-r/2+r*x/2).subs(p, p_floor))
            completed_square = sp.Rational(1, 15)+r*(sp.Rational(2, 45)
                                                     +sp.Rational(9, 20)*(x+sp.Rational(5, 9))**2)
            assert sp.expand(mass_gap-completed_square) == 0
            extra = dict(E6_only_trace=str(e6_only_trace),
                         E6_only_strict_R_A_lower_bound=str(r_bound),
                         E6_only_strict_missing_mass_R_gap=str(2*r_bound/3),
                         E6_only_strict_DU_mass_R_gap=str(sp.Rational(1, 15)+2*r_bound/45))
        else:
            forbidden = trace(charges.diff(u))
            assert forbidden == 216*r-486*u+486
            assert missing_gap == 1-u+2*r/3
            extra = dict(E6_only_excluded=True)
        # With only family gauged, D is an independent trial variable.
        # A is then a gauge singlet and a surviving A primary has r >= 2/3.
        family_charges = charges.copy()
        family_charges[6] = dual
        family_charges[8] = (66-9*sum(family_charges[:7]))/5
        assert sp.expand((gauge*(family_charges-sp.ones(9, 1))+c2)[1]) == 0
        family_current = family_charges.diff(dual)
        assert (gauge*family_current)[1] == 0
        bare = sp.expand(sum(dim*(charge-1)*current**2 for dim, charge, current
                             in zip(dims, family_charges, family_current)))
        assert bare.coeff(dual) == sp.Rational(567, 25)
        edge = {r: sp.Rational(2, 3), p: 0, u: 1}
        assert bare.coeff(r) > 0
        assert (bare.coeff(p) > 0 if omega else bare.coeff(u) < 0)
        dual_limit = sp.solve(bare.subs(edge), dual)[0]
        assert dual_limit == -sp.Rational(13, 7)
        corrected = sp.expand(bare + 9*(sp.Rational(2, 3)-3*dual))
        assert corrected.coeff(dual) < 0 and corrected.subs(edge).subs(dual, dual_limit) > 0
        cases.append(dict(alternating_cubic=omega, active_gauges='E6 and family',
                          trial_scalar_charges=list(map(str, charges)),
                          positive_forbidden_flavor_trace=str(forbidden),
                          rank_changing_mass_R_minus_two=str(missing_gap),
                          family_only_D_strict_upper_R_bound=str(dual_limit),
                          family_only_trace_with_one_free_D_baryon=str(corrected), **extra))
    return dict(status='PASS', charge_order=['X+', 'U', 'X-', 'X2', 'Z1', 'Z0', 'D', 'A', 'S'],
                branches=cases)


if __name__ == '__main__':
    result = json.dumps(calculate(), indent=2) + '\n'
    (uv.flat.ROOT / OUT).write_text(result, encoding='utf-8')
    print(result)
