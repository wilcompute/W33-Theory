"""Exact a-maximization obstruction for the canonical W33 cubic theory."""

import json

import sympy as sp

import toe_20261109_canonical_sm_flatness as flat


OUT = 'data/toe_20261112_canonical_uv_fixed_point.json'
THETA = 'data/toe_20261112_parent_theta_lattice.json'


def chiral_a(q):
    return sp.Rational(3, 32)*(3*(q-1)**3 - (q-1))


def trial_a(charges):
    dimensions = [81]*5 + [78, 10]
    return sp.expand(sp.Rational(3, 16)*86 + sum(d*chiral_a(q) for d, q in zip(dimensions, charges)))


def corrected_slopes(derivative, r, limit):
    """Include every possible free primitive adjoint generator."""
    degrees = [2, 5, 6, 8, 9, 12]
    bound = sp.Rational(2, 3)
    ends = sorted([sp.S.Zero, limit] + [bound/d for d in degrees])
    intervals = []
    for left, right in zip(ends, ends[1:]):
        active = [d for d in degrees if d*(left+right)/2 < bound]
        slope = sp.expand(derivative - sum(sp.diff(chiral_a(d*r), r) for d in active))
        witnesses = [left, right] + [v for v in sp.solve(sp.diff(slope, r), r) if left < v < right]
        minimum = min(slope.subs(r, v) for v in witnesses)
        assert minimum > 0
        intervals.append(dict(interval=list(map(str, (left, right))), free_degrees=active,
                              minimum_slope=str(minimum)))
    return intervals


def without_alternating_cubic(r, xm, s, c2, bifundamental, adjoint, spectator):
    """When Omega vanishes the two X-Z pair splittings are independent."""
    u, v = sp.symbols('u v', real=True)
    mean = 1 - r/2
    charges = [mean+u, mean+v, xm, mean-u, mean-v, r, s]
    ns = c2 + bifundamental*sum(q-1 for q in charges[:5]) + adjoint*(r-1) + spectator*(s-1)
    assert sp.simplify(ns) == sp.zeros(2, 1)
    a = trial_a(charges)
    axis = a.subs({u: 0, v: 0})
    scale = sp.Rational(2187, 16)
    assert sp.expand(a - axis + scale*r*(u*u + v*v)/2) == 0
    derivative = sp.diff(axis, r)
    limit = sp.solve(sp.diff(derivative, r), r)[0]
    ellipse = -r*sp.diff(derivative, r)/scale
    assert limit == sp.Rational(1684, 3329)
    assert sp.expand(ellipse - sp.Rational(3329, 1350)*r*(limit-r)) == 0
    # The Schur complement of the two splitting directions gives the disk
    # u^2+v^2 <= ellipse. All four paired matter charges exceed 2/5.
    lower_bound = sp.Poly((mean-sp.Rational(2, 5))**2 - ellipse, r)
    assert mean.subs(r, limit) > sp.Rational(2, 5)
    assert lower_bound.LC() > 0 and lower_bound.discriminant() < 0
    intervals = corrected_slopes(derivative, r, limit)
    return dict(trial_a=str(a), hessian_domain_max_R_A=str(limit),
                minimum_corrected_slopes=intervals)


def calculate():
    representations = flat.read(THETA)['spin_witness']['representations']
    bifundamental, adjoint, family_adjoint, spectator = (
        sp.Matrix(entry['basic_trace_indices']) / 2 for entry in representations.values()
    )
    c2 = adjoint + family_adjoint
    beta = 3*c2 - 5*bifundamental - adjoint - spectator
    assert list(beta) == [-21, -66]

    r, t = sp.symbols('r t', real=True)
    x = sp.Rational(1, 2) - r/3
    z = sp.Rational(3, 2) - 2*r/3
    xm = 1 + 2*r/3
    s = (3 + 12*r)/5
    charges = [x+t, x-t, xm, z-t, z+t, r, s]
    ns = c2 + bifundamental*sum(q-1 for q in charges[:5]) + adjoint*(r-1) + spectator*(s-1)
    assert sp.simplify(ns) == sp.zeros(2, 1)
    assert sp.simplify(sum(charges[:3])) == 2
    assert sp.simplify(charges[0] + charges[3] + r) == 2
    assert sp.simplify(charges[1] + charges[4] + r) == 2

    a = trial_a(charges)
    derivative = sp.diff(a, r).subs(t, 0)
    assert sp.discriminant(derivative, r) < 0 and derivative.subs(r, 0) > 0
    hessian = sp.hessian(a, (r, t))
    assert hessian[1, 1] == -sp.Rational(2187, 8)*r
    assert hessian[0, 1] == -sp.Rational(2187, 8)*t
    limit = sp.solve(hessian[0, 0], r)[0]
    assert 0 < limit < sp.Rational(2, 5)
    ellipse = sp.solve(hessian.det(), t**2)[0]
    assert sp.expand(ellipse - sp.Rational(776, 675)*r*(limit-r)) == 0
    assert ellipse.subs(r, limit/2) < sp.Rational(11, 50)**2
    x_bound = sp.Poly((x-sp.Rational(1, 5))**2 - ellipse, r)
    assert x_bound.LC() > 0 and x_bound.discriminant() < 0
    assert z.subs(r, limit) - sp.Rational(11, 50) > 1
    assert sp.Rational(3, 2) - 3*sp.Rational(11, 50) > sp.Rational(2, 3)

    # The only generators that can violate the bound inside the Hessian
    # region are the primitive E6 adjoint invariants.
    intervals = corrected_slopes(derivative, r, limit)
    assert min(sp.Rational(row['minimum_slope']) for row in intervals) == sp.Rational(6309, 1600)

    # The spectator quartic and mass sextic each enforce X+=X-.
    # The sextic cross contraction also enforces X2=X+.
    v_equals_m = charges[1] - xm
    solution = sp.solve([v_equals_m, charges[0] - charges[1]], (r, t))
    assert solution == {r: -sp.Rational(1, 2), t: 0}
    sextic = 2*s + 2*(2-r)
    assert sextic.subs(solution) == sp.Rational(19, 5)
    quartic_solution = sp.solve([v_equals_m, s+3*charges[1]-2], (r, t))
    assert quartic_solution[r] == -sp.Rational(4, 11)
    return dict(status='PASS', one_loop_b0=list(map(int, beta)),
                order=['X2', 'X+', 'X-', 'Z0', 'Z1', 'A', 'S'],
                trial_R=list(map(str, charges)), trial_a=str(a),
                hessian_domain_max_R_A=str(limit),
                hessian_domain_max_t_squared=str(ellipse.subs(r, limit/2)),
                minimum_corrected_slopes=intervals,
                without_alternating_cubic=without_alternating_cubic(
                    r, xm, s, c2, bifundamental, adjoint, spectator),
                spectator_sextic_forced_R=str(sextic.subs(solution)),
                spectator_odd_quartic_forced_R_A=str(quartic_solution[r]))


if __name__ == '__main__':
    result = json.dumps(calculate(), indent=2) + '\n'
    (flat.ROOT / OUT).write_text(result, encoding='utf-8')
    print(result)
