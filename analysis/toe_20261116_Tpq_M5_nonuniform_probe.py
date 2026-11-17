"""Verify the subcritical wrapped M5 radial bifurcation."""

import json
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import root


def quartic_coefficients():
    q, u, a, b, dot = sp.symbols("q u a b dot", real=True)
    c1, c2, s1, s2 = sp.symbols("c1 c2 s1 s2", real=True)

    def average(polynomial):
        means = {(0, 0): 1, (2, 0): sp.Rational(1, 2), (0, 2): sp.Rational(1, 2),
                 (4, 0): sp.Rational(3, 8), (0, 4): sp.Rational(3, 8),
                 (2, 2): sp.Rational(1, 8)}
        total = 0
        for (i, j, k, ell), coefficient in sp.Poly(polynomial, c1, s1, c2, s2).terms():
            if not any(order % 2 for order in (i, j, k, ell)):
                total += coefficient*means[i, j]*means[k, ell]
        return sp.expand(total)

    f = a*c1+b*c2
    gradient_sq = a*a*s1*s1+b*b*s2*s2+2*dot*a*b*s1*s2
    # At the critical wave number the cubic variational source is
    # 4 q u f^2 - 8 q u |grad f|^2 on the critical eigenspace.
    forcing = 4*q*u*f*f-8*q*u*gradient_sq
    complement = -q*f*f
    direct = ((-112*q*q*u+40*u*u)*f**4/24
              +(16*q*q*u-4*u*u)*f*f*gradient_sq-2*u*u*gradient_sq**2)
    angular_result = average(direct+forcing*complement/2)
    assert sp.expand(angular_result+u*u*(5*a**4+(4+16*dot**2)*a*a*b*b+5*b**4)/8) == 0
    result = angular_result.subs(dot, 0)

    dk = sp.Symbol("sigma", positive=True)
    reduced = dk*(a*a+b*b)/4+result
    a_stripe_sq, a_square_sq = dk/(5*u*u), dk/(7*u*u)
    assert sp.simplify(reduced.subs(b, 0).subs(a*a, a_stripe_sq)) == dk**2/(40*u*u)
    assert sp.simplify(reduced.subs(b, a).expand().subs(a*a, a_square_sq)) == dk**2/(28*u*u)
    hessian = sp.hessian(reduced, (a, b))
    stripe = hessian.subs(b, 0).subs(a*a, a_stripe_sq)
    assert stripe == sp.diag(-dk, 3*dk/10)
    square = hessian.subs(b, a).subs(a*a, a_square_sq)
    assert sorted(square.eigenvals().keys(), key=lambda value: float(value.subs(dk, 1))) == [-dk, -3*dk/7]
    return {"quartic_at_square_threshold": str(result),
            "pairwise_quartic_for_angle_with_cosine_dot": str(angular_result),
            "stripe_squared_amplitude_per_detuning": "1/(5 u^2)",
            "equal_amplitude_square_squared_amplitude_per_detuning": "1/(7 u^2)",
            "stripe_and_equal_amplitude_square_action_excess_per_detuning_squared":
                ["1/(40 u^2)", "1/(28 u^2)"]}


def numerical_stripe(amplitude):
    radius = np.arcsinh(1.)
    q = np.sqrt(2.)
    u = 1.
    angles = 2*np.pi*(np.arange(192)+0.5)/192
    modes = np.arange(16)
    cosine = np.cos(modes[:, None]*angles)
    sine = np.sin(modes[:, None]*angles)
    retained = [0, *range(2, len(modes))]

    def fields(parameters):
        profile = np.zeros(len(modes))
        profile[1] = amplitude
        profile[retained] = parameters[:-1]*amplitude**2
        momentum = 4*u+parameters[-1]*amplitude**2
        return (radius+profile @ cosine, (-modes*profile) @ sine,
                (-modes**2*profile) @ cosine, momentum)

    def residual(parameters, project=True):
        r, velocity, acceleration, momentum = fields(parameters)
        metric = 1+momentum*velocity**2
        values = 4/np.tanh(r)/np.sqrt(metric)-4*q-momentum*acceleration/metric**1.5
        if not project:
            return values
        coefficients = (cosine @ values)/len(angles)/amplitude**2
        coefficients[1] /= amplitude
        return coefficients

    guess = np.zeros(len(modes))
    guess[:2] = -q/2
    guess[-1] = 5*u*u
    solution = root(residual, guess, tol=1e-10)
    residual_norm = float(np.max(np.abs(residual(solution.x, project=False))))
    shift = float(solution.x[-1])
    assert residual_norm < 5e-10 and abs(shift/5-1) < 0.03, (amplitude, residual_norm, shift)
    r, velocity, _, momentum = fields(solution.x)

    def density(radial, slope):
        volume = np.sinh(4*radial)/32-np.sinh(2*radial)/4+3*radial/8
        return np.sinh(radial)**4*np.sqrt(1+momentum*slope**2)-4*q*volume

    action_excess = float(np.mean(density(r, velocity)-density(radius, 0)))
    action_per_fourth = action_excess/amplitude**4
    assert abs(action_per_fourth/(5/8)-1) < 0.04, (amplitude, action_per_fourth)
    return {"radial_fourier_amplitude": amplitude,
            "wave_number_squared_detuning_per_amplitude_squared": shift,
            "round_action_excess_per_amplitude_fourth": action_per_fourth,
            "maximum_radial_equation_residual": residual_norm}


def main():
    data = quartic_coefficients()
    data["numerical_stripes_at_unit_sphere_radius"] = [
        numerical_stripe(amplitude) for amplitude in (0.025, 0.05, 0.10)
    ]
    output = Path(__file__).resolve().parents[1]/"data"/"toe_20261116_Tpq_M5_nonuniform_probe.json"
    output.write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    print("Verified the wrapped M5 radial quartic and full nonuniform stripe equation.")


if __name__ == "__main__":
    main()
