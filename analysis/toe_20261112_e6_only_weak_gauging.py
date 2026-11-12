"""Weak family gauging at the canonical rank-two E6-only trial fixed points."""

import json

import sympy as sp

import toe_20261112_canonical_uv_fixed_point as uv


OUT = 'data/toe_20261112_e6_only_weak_gauging.json'


def branch(omega):
    r, t, u, v = sp.symbols('r t u v', real=True)
    half = sp.Rational(1, 2)
    free = sp.Rational(2, 3)
    if omega:
        x, z = half-r/3, 3*half-2*r/3
        charged = [x+t, x-t, 1+2*r/3, z-t, z+t, r]
        splits = (t,)
        no_charged_free_through = sp.Rational(1, 6)
    else:
        mean = 1-r/2
        charged = [mean+u, mean+v, 1+2*r/3, mean-u, mean-v, r]
        splits = (u, v)
        no_charged_free_through = sp.Rational(1, 3)
    assert sp.expand(12 + 9*sum(q-1 for q in charged[:5]) + 12*(r-1)) == 0
    family_b = sp.expand(3*(3 + sp.Rational(27, 2)*sum(q-1 for q in charged[:5])
                            + sp.Rational(15, 2)*(free-1)))
    assert family_b == sp.Rational(3, 2)-54*r
    # The decoupled family vector adds a constant that cancels in Delta a.
    a = uv.trial_a(charged+[free])
    axis = dict.fromkeys(splits, 0)
    derivative = sp.diff(a.subs(axis), r)
    scale = -sp.diff(a, splits[0], 2).coeff(r)
    assert sp.diff(a, splits[0], 2) == -scale*r and scale > 0
    assert sp.expand(a-a.subs(axis)+scale*r*sum(w*w for w in splits)/2) == 0
    r0, upper_root = sorted(sp.solve(derivative, r), key=lambda value: value.evalf())
    curvature_limit = sp.solve(sp.diff(derivative, r), r)[0]
    assert 0 < r0 < curvature_limit < upper_root
    assert sp.diff(derivative, r).subs(r, r0) < 0
    assert sp.discriminant(derivative, r) > 0

    at_candidate = [sp.simplify(q.subs(axis).subs(r, r0)) for q in charged]
    assert all(0 < q < sp.Rational(5, 3) for q in at_candidate)
    assert r0 > sp.Rational(1, 3)
    if omega:
        assert min(at_candidate[:3]) > sp.Rational(2, 9)
        assert min(at_candidate[3:5]) > free
    else:
        assert min(at_candidate[:5]) > sp.Rational(1, 3)
    weak_b = sp.simplify(family_b.subs(r, r0))
    assert weak_b < 0
    delta_a = sp.simplify(a.subs(axis).subs(r, r0) - uv.trial_a([free]*7))
    assert delta_a < 0

    # The convex corrections imply that a candidate corrected maximum lies
    # in the negative-semidefinite region of the bare Hessian.
    ellipse = -r*sp.diff(derivative, r)/scale
    assert 0 < no_charged_free_through < curvature_limit/2
    max_split_squared = ellipse.subs(r, no_charged_free_through)
    if omega:
        assert x.subs(r, no_charged_free_through) - sp.sqrt(max_split_squared) > sp.Rational(2, 9)
        assert z.subs(r, no_charged_free_through) - sp.sqrt(max_split_squared) > free
    else:
        assert mean.subs(r, no_charged_free_through) - sp.sqrt(max_split_squared) > sp.Rational(1, 3)
    # No family-charged free composites would require r <= 1/36 for
    # marginal or relevant weak gauging. Only pure adjoints can decouple there.
    weak_cut = sp.Rational(1, 36)
    assert weak_cut < no_charged_free_through
    # Pure adjoints can be free only through r=1/3. Check the larger
    # interval so the result also tests every adjoint-only branch.
    corrected = uv.corrected_slopes(derivative, r, sp.Rational(1, 3))
    minimum_slope = min(sp.Rational(interval['minimum_slope']) for interval in corrected)
    assert minimum_slope > 0
    needed_correction = 18*no_charged_free_through-half
    return dict(alternating_cubic=omega, axis_derivative=str(sp.factor(derivative)),
                unique_uncorrected_local_max_R_A=str(r0),
                local_max_scalar_charges=list(map(str, at_candidate+[free])),
                weak_family_b_at_trial_max=str(weak_b),
                a_trial_minus_massless_gaussian=str(delta_a),
                max_R_A_in_bare_hessian_region=str(curvature_limit),
                no_charged_free_through_R_A=str(no_charged_free_through),
                required_charged_free_anomaly_correction_strictly_above=str(needed_correction),
                minimum_slope_with_all_adjoint_corrections_through_R_A_one_third=str(minimum_slope))


if __name__ == '__main__':
    result = json.dumps(dict(status='PASS', branches=[branch(True), branch(False)]), indent=2) + '\n'
    (uv.flat.ROOT / OUT).write_text(result, encoding='utf-8')
    print(result)
