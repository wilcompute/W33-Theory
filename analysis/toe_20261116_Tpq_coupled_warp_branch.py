"""Exact checks for the coupled quadrupole branch of the Type IIB equations."""

import json
from pathlib import Path

import numpy as np
import sympy as sp
from numpy.polynomial.legendre import Legendre, leggauss
from scipy.optimize import brentq, root


def scalar_reduction():
    warp = sp.Symbol("A")
    potential = 20*sp.exp(-16*warp/3)-8*sp.exp(-40*warp/3)
    kinetic = sp.Rational(80, 3)
    source = sp.diff(potential, warp)/kinetic
    assert sp.simplify(source-4*(sp.exp(-40*warp/3)-sp.exp(-16*warp/3))) == 0
    assert potential.subs(warp, 0) == 12 and source.subs(warp, 0) == 0
    assert sp.diff(source, warp).subs(warp, 0) == -32
    quadratic = sp.diff(source, warp, 2).subs(warp, 0)/2
    assert quadratic == sp.Rational(896, 3)

    x = sp.Symbol("x")
    y = sp.legendre(2, x)
    projection = sp.integrate(y**3, (x, -1, 1))/sp.integrate(y**2, (x, -1, 1))
    assert projection == sp.Rational(2, 7)
    assert quadratic*projection == sp.Rational(256, 3)
    return x, y


def metric_response(x, y):
    k1, k2 = sp.Rational(16, 3), sp.Rational(20, 3)
    b1, b2 = sp.Rational(8, 3), sp.Rational(16, 3)  # Squared curvatures.
    level = sp.Symbol("lambda")
    constant = sp.Matrix([[-2*k1+2*b1, 0, -b1],
                          [0, -2*k2+2*b2, -b2],
                          [-2*b1, -2*b2, b1+b2]])
    nonconstant = sp.Matrix([[level-2*k1, 2*b1+level, 2*b1+level/2],
                             [0, level-2*k2+2*b2, -b2],
                             [0, -2*(b1+b2), level-2*b1+b2]])
    assert constant.det() != 0
    assert sp.expand(nonconstant.det()-(level-2*k1)**2*(level+8)) == 0
    tensor_degree_two = -sp.Rational(1280, 9)*y*y
    first_trace = tensor_degree_two+sp.Rational(20, 3)*k1*(1-x*x)*sp.diff(y, x)**2

    def project(function, ell):
        return sp.Rational(2*ell+1, 2)*sp.integrate(
            function*sp.legendre(ell, x), (x, -1, 1))

    rows = []
    metric_functions = sp.zeros(3, 1)
    for ell in (0, 2, 4):
        matrix = constant if ell == 0 else nonconstant.subs(level, k1*ell*(ell+1))
        target = sp.Matrix([project(first_trace, ell), project(tensor_degree_two, ell),
                            project(tensor_degree_two, ell)])
        response = matrix.inv()*target
        metric_functions += response*sp.legendre(ell, x)
        rows.append({"harmonic": ell, "D_B_C": [str(value) for value in response]})
    # Independent traceless S2 Einstein check: common factors from Hessians
    # cancel, leaving 2 B'' + C'' + (40/3) (Y')^2 = 0.
    assert sp.expand(sp.diff(2*metric_functions[1]+metric_functions[2], x, 2)
                     +sp.Rational(40, 3)*sp.diff(y, x)**2) == 0
    return {"constant_metric_determinant": str(constant.det()),
            "nonconstant_metric_determinant": "(lambda-32/3)^2*(lambda+8)",
            "second_order_metric_response": rows,
            "independent_traceless_equation_passed": True}


def numerical_branch(p, q, metric, count, *, include_profiles=False):
    eta = brentq(lambda z: q*q*z*(2-z)**2-p*p*(1-z)*(1+z)**2, 0, 1)
    result = solve_shape(eta, metric, count)
    assert abs(result["relative_to_leading"]-1) < 0.1, (p, q, count, result)
    if not include_profiles:
        del result["even_legendre_profiles"]
    return {"chern_pair": [p, q], **result}


def solve_shape(eta, metric, count, *, initial_profiles=None):
    k1, k2 = 4*(1+eta), 4*(2-eta)
    b1, b2 = 8*eta, 8*(1-eta)
    expected = (32-6*k1)*3/256
    x, weights = leggauss(6*count)
    degrees = np.arange(0, 2*count, 2)
    basis = [Legendre.basis(int(ell)) for ell in degrees]
    values = np.array([poly(x) for poly in basis])
    slopes = np.array([poly.deriv()(x) for poly in basis])
    second_derivatives = np.array([poly.deriv(2)(x) for poly in basis])
    laplacian = -(degrees*(degrees+1))[:, None]*values
    projection = (2*degrees+1)[:, None]*values*weights/2
    scaling = np.array([expected, expected**2, expected**2, expected**2])[:, None]

    def equations(coefficients, project=True):
        scaled = coefficients.reshape(4, count)*scaling
        a, d, b, c = scaled @ values
        a_x, d_x, b_x, c_x = scaled @ slopes
        lap_a, lap_d, lap_b, lap_c = k1*np.exp(-2*d)*(scaled @ laplacian)
        norm = k1*np.exp(-2*d)*(1-x*x)
        flux_density = np.exp(2*d-2*b-3*c)
        flux_density /= np.dot(weights, flux_density)/2
        flux1 = b1*np.exp(2*c-4*d)*flux_density**2
        flux2 = b2*np.exp(2*c-4*b)
        source = 4*(np.expm1(-40*a/3)-np.expm1(-16*a/3))
        potential = (20*np.exp(-16*a/3)-8*np.exp(-40*a/3))/3
        scalar = lap_a+norm*(2*b_x+c_x)*a_x-source
        base1 = (k1*np.exp(-2*d)-lap_d-lap_b-norm*b_x*b_x
                 -(lap_c+norm*c_x*c_x+flux1)/2-potential-(20/3)*norm*a_x*a_x)
        base2 = k2*np.exp(-2*b)-lap_b-norm*b_x*(2*b_x+c_x)-flux2/2-potential
        fiber = -lap_c-norm*c_x*(2*b_x+c_x)+(flux1+flux2)/2-potential
        residual = np.array([scalar, base1, base2, fiber])
        if not project:
            _, _, b_xx, c_xx = scaled @ second_derivatives
            traceless = norm*(2*b_xx+c_xx-2*d_x*(2*b_x+c_x)
                              +2*b_x*b_x+c_x*c_x+(40/3)*a_x*a_x)
            return residual, traceless
        projected = (residual @ projection.T)/scaling
        projected[0, 1] /= expected
        return projected.ravel()

    initial = np.zeros((4, count))
    if initial_profiles is None:
        initial[0, 1] = 1
        for row in metric["second_order_metric_response"]:
            initial[1:, row["harmonic"]//2] = [float(sp.Rational(s)) for s in row["D_B_C"]]
    else:
        shared_count = min(count, len(initial_profiles[0]))
        initial[:, :shared_count] = np.array(initial_profiles)[:, :shared_count]/scaling
    fit = root(equations, initial.ravel(), tol=1e-9)
    projected_error = np.max(np.abs(equations(fit.x)))
    assert projected_error < 2e-6, (eta, count, projected_error, fit.message)
    amplitude = expected*fit.x[1]
    residual, traceless = equations(fit.x, project=False)
    error = float(np.max(np.abs(residual)))
    tracefree_error = float(np.max(np.abs(traceless)))
    assert error < 1e-9 and abs(amplitude) > abs(expected)/4, (eta, count, error, amplitude/expected)
    assert tracefree_error < 1e-9, (eta, count, tracefree_error)
    a, d, b, c = (fit.x.reshape(4, count)*scaling) @ values
    log_volume = 2*d+2*b+c
    graviton_integral_shift = float(np.dot(weights, np.expm1(log_volume-16*a/3))/2)
    page_integral_shift = float(np.dot(weights, np.expm1(log_volume-40*a/3))/2)
    assert abs(graviton_integral_shift-page_integral_shift) < 1e-13
    return {"lambda_minus_32": 6*k1-32,
            "quadrupole_amplitude": amplitude, "relative_to_leading": amplitude/expected,
            "maximum_retained_equation_residual": error,
            "maximum_traceless_equation_residual": tracefree_error, "even_harmonics": count,
            "graviton_integral_relative_shift": graviton_integral_shift,
            "page_integral_relative_shift": page_integral_shift,
            "even_legendre_profiles": (fit.x.reshape(4, count)*scaling).tolist()}


def main():
    x, y = scalar_reduction()
    metric = metric_response(x, y)
    numerical = []
    for p, q in ((7, 8), (8, 9)):
        coarse = numerical_branch(p, q, metric, 6)
        fine = numerical_branch(p, q, metric, 8)
        assert abs(coarse["quadrupole_amplitude"]-fine["quadrupole_amplitude"]) < 2e-9
        numerical.append(fine)
    data = {
        "rescaled_internal_einstein_scalar_metric": "g_internal = exp(-10 A / 3) h",
        "projected_quadratic_coefficient": "256/3",
        "leading_A_coefficient_per_32_minus_eigenvalue": "3/256",
        "metric": metric,
        "examples": numerical,
    }
    output = Path(__file__).resolve().parents[1]/"data"/"toe_20261116_Tpq_coupled_warp_branch.json"
    output.write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    print("Verified the coupled warp coefficient, metric invertibility, and all quadratic Einstein blocks.")


if __name__ == "__main__":
    main()
