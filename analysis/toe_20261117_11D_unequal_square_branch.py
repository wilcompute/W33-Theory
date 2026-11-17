"""Exact quartic normal form of the unequal-flux square AdS branch."""

import json

import sympy as sp

from toe_20261117_11D_square_modulated_branch import numerical_branch


def normal_form():
    lam, d = sp.symbols("lambda d", real=True)
    d_squared = (lam**2+8*lam-560)/80
    laplace = sp.Matrix([[20, 5, 0, 0], [5, 0, 0, 0],
                         [0, 0, -sp.Rational(36, 5), 0], [0, 0, 0, -4]])
    local = [(coefficient, sp.Matrix(exponents)) for coefficient, exponents in
             ((-20, (3, 2, 0, 0)), (12+4*d, (5, 2, -sp.Rational(18, 5), -2)),
              (12-4*d, (5, 2, -sp.Rational(18, 5), 2)),
              (-8, (5, 2, -sp.Rational(48, 5), 0)))]
    flux = [(2*(1+sign*d), sp.Matrix([-5, 2, sp.Rational(12, 5), 4*sign]))
            for sign in (1, -1)]
    curvature = sum((n*v*v.T for n, v in local), sp.zeros(4))
    flux_curvature = sum((n*v*v.T for n, v in flux), sp.zeros(4))

    def hessian(norm2):
        return curvature+(-1 if norm2 == 0 else 1)*flux_curvature+2*lam*norm2*laplace

    def on_shell(expr):
        expression = sp.Poly(sp.expand(expr), d)
        return sp.Add(*(coefficient*d**(degree % 2)*d_squared**(degree//2)
                        for (degree,), coefficient in expression.terms()))

    def simplify_mod(expr):
        numerator, denominator = sp.fraction(sp.cancel(expr))
        numerator, denominator = on_shell(numerator), on_shell(denominator)
        if denominator.has(d):
            flip = denominator.subs(d, -d)
            numerator, denominator = on_shell(numerator*flip), on_shell(denominator*flip)
        return sp.factor(numerator/denominator)

    h1 = hessian(1)
    w = (-(h1[:3, :3].inv()*h1[:3, 3])).applyfunc(sp.factor).col_join(sp.ones(1, 1))
    assert (h1*w).applyfunc(simplify_mod) == sp.zeros(4, 1)
    mode_kinetic = simplify_mod(w.dot(laplace*w))
    direct_local = sum(n*v.dot(w)**4 for n, v in local)*sp.Rational(3, 32)
    direct_flux = -sp.Rational(5, 32)*sum(n*v.dot(w)**4 for n, v in flux)
    direct_gradient = sp.Rational(75, 8)*lam*w[0]**2*mode_kinetic
    direct = simplify_mod(direct_local+direct_flux+direct_gradient)
    local_forcing = sum((n*v.dot(w)**2*v/2 for n, v in local), sp.zeros(4, 1))
    flux_forcing = sum((n*v.dot(w)**2*v for n, v in flux), sp.zeros(4, 1))
    unit_a = sp.eye(4)[:, 0]
    relaxations = []
    responses = {}
    for length2, mode_norm, overlap in ((0, 1, 1), (2, sp.Rational(1, 4), sp.Rational(1, 2)),
                                         (4, 1, sp.Rational(1, 2))):
        source = overlap*(local_forcing+flux_forcing/2+5*lam*(
            (1-sp.Rational(length2, 2))*mode_kinetic*unit_a+length2*w[0]*laplace*w
        ))
        if length2 == 0:
            source -= flux_forcing
        source = source.applyfunc(simplify_mod)
        response = (-(mode_norm*hessian(length2)).inv()*source).applyfunc(simplify_mod)
        relaxations.append(simplify_mod(source.dot(response)/2))
        responses[length2] = response
    relaxed = sp.factor(direct+sum(relaxations))
    assert not relaxed.has(d)
    assert relaxed.subs(lam, 20) == sp.Rational(36736, 459)
    assert mode_kinetic.subs(lam, 20) == -4
    assert simplify_mod(3*responses[0][0]+2*responses[0][1]+2*w[1]**2) == 0
    shift = sp.factor(-2*relaxed/mode_kinetic)
    numerator, denominator = shift.as_numer_denom()
    denominator_polynomial = sp.Poly(denominator, lam)
    assert denominator_polynomial.eval(20) > 0 and denominator_polynomial.count_roots(20, 22) == 0
    return lam, d, w, mode_kinetic, direct, relaxed, shift, responses


def solve_quantized_scan(lam, d, mode, relaxed, shift, responses):
    import numpy as np
    from scipy.optimize import brentq

    samples = []
    for n0, n1, n2 in ((2306, 1068, 801), (134, 58, 29)):
        eta = brentq(lambda e: n1*n1*(1-e)*(1+e)**2-n2*n2*e*(2-e)**2, 0, 1)
        asymmetry = 2*eta-1
        critical = -4+4*np.sqrt(36+5*asymmetry**2)
        area = 16*np.pi*n1/(n0*4*(2-eta)*np.sqrt(8*eta))
        reference = 4*np.pi*np.pi/area
        at = {lam: critical, d: asymmetry}
        backreaction = [[float(responses[k][i].subs(at)) for k in (0, 4, 2)]
                        for i in range(4)]
        normal = {"static_threshold": critical,
                  "lambda_shift_coefficient": float(shift.subs(at)),
                  "first_order_even_fields": [float(x) for x in mode[:3, :].subs(at)],
                  "even_backreaction_by_field": dict(enumerate(backreaction[:3])),
                  "second_order_v": backreaction[3],
                  "normalized_AdS_Newton_coefficient_shift_at_epsilon_fourth":
                      float(relaxed.subs(at)/8)}
        assert (reference-critical)*normal["lambda_shift_coefficient"] > 0
        result = numerical_branch(7, 48, normal, asymmetry=asymmetry, reference_lambda=reference)
        assert max(result["max_residual_components_A_B_c_v_and_tracefree"]) < 1e-7
        samples.append({"periods_N0_N1_N2": [n0, n1, n2], "flux_asymmetry": asymmetry,
                        "static_threshold": critical, "detuning": reference-critical,
                        "slope_coefficient": normal["lambda_shift_coefficient"],
                        "numeric": result})
    return samples


def certificate():
    lam, d, mode, kinetic, direct, relaxed, shift, responses = normal_form()
    polynomial = sp.Poly(shift.as_numer_denom()[0], lam)
    root_intervals = [bound for bound, multiplicity in polynomial.intervals(eps=sp.Rational(1, 10**12))
                      if bound[0] >= 20 and bound[1] <= 22 and multiplicity == 1]
    assert len(root_intervals) == polynomial.count_roots(20, 22) == 2
    assert root_intervals[1][1] < -4+4*sp.sqrt(41)
    assert polynomial.eval(20) > 0 and polynomial.eval(
        sum(root_intervals[0][1:]+root_intervals[1][:1])/2
    ) < 0 and polynomial.eval(22) > 0
    # Integer periods make T=r^2+r^(-2) rational. Eliminate lambda from
    # the zero-quartic condition and the period ratio equation.
    t = sp.symbols("T")
    plus, minus = (1+d)*(3-d)**2, (1-d)*(3+d)**2
    relation = sp.Poly(sp.expand(t*plus*minus-plus**2-minus**2), d)
    assert all(power % 2 == 0 for (power,), _ in relation.terms())
    eliminated = sum(coefficient*((lam**2+8*lam-560)/80)**(power//2)
                     for (power,), coefficient in relation.terms())
    period_resultant = sp.Poly(sp.resultant(polynomial.as_expr(), eliminated, lam), t).primitive()[1]
    assert period_resultant.degree() > 0 and not period_resultant.ground_roots()
    return {
        "field_order_A_B_c_v": list(map(str, mode)),
        "static_lambda": "-4+4*sqrt(36+5*d^2)",
        "quadratic_detuning_coefficient": str(kinetic),
        "frozen_quartic": str(direct),
        "relaxed_quartic": str(relaxed),
        "lambda_shift_per_amplitude_squared": str(shift),
        "sample_shifts_at_d_0_and_1": [str(shift.subs(lam, 20)),
                                     str(sp.N(shift.subs(lam, -4+4*sp.sqrt(41)), 12))],
        "isolated_lambda_zeros_in_20_22": [[str(x) for x in bound] for bound in root_intervals],
        "approximate_asymmetries_at_zeros": [
            str(sp.N(sp.sqrt(((point := sum(bound)/2)**2+8*point-560)/80), 12))
            for bound in root_intervals
        ],
        "critical_period_ratio_resultant_for_T_r_squared_plus_inverse_squared":
            str(period_resultant.as_expr()),
        "critical_resultant_rational_roots": [],
        "quantized_unequal_samples": solve_quantized_scan(lam, d, mode, relaxed, shift, responses),
    }


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2))
