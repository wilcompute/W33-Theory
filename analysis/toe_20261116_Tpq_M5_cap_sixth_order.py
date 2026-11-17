"""Compute the reduced sixth-order action of the capped M5 spectator branch."""

import json
from math import factorial
from pathlib import Path

import numpy as np
from scipy.linalg import eigh
from scipy.optimize import brentq
import sympy as sp

from toe_20261116_Tpq_M5_cap_spectator_branch import reduced_quartic
from toe_20261116_Tpq_M5_finite_stripe import area, volume


ORDER = 6


def product(left, right):
    return np.stack([sum(left[i]*right[n-i] for i in range(n+1))
                     for n in range(ORDER+1)])


def polynomial(jet, coefficients):
    result = np.zeros_like(jet)
    for coefficient in reversed(coefficients):
        result = product(result, jet)
        result[0] += coefficient
    return result


def binomial(jet, exponent):
    coefficients = [1.]
    for n in range(1, ORDER+1):
        coefficients.append(coefficients[-1]*(exponent-n+1)/n)
    return polynomial(jet, coefficients)


def action_jets(fields, f, ds, dtheta):
    speed = fields["speed"][:, None]
    angular = fields["angular_curvature"][:, None]
    m = fields["meridian_curvature"][:, None]
    c, critical = fields["pressure"], fields["critical"]
    angular_coeffs = [speed**n/factorial(n) if n % 2 == 0
                      else angular*speed**(n-1)/factorial(n) for n in range(ORDER+1)]
    circular_tube = np.zeros_like(f)
    for n, coefficient in enumerate(angular_coeffs):
        circular_tube[n] = coefficient
    angular_sq = product(circular_tube, circular_tube)
    volume_tube = product(angular_sq, angular_sq)
    tube = volume_tube.copy()
    tube[1:] += m*volume_tube[:-1]
    constants = tube[:, :, :1]
    jacobian = polynomial(f, constants)
    jacobian_derivative = polynomial(f, [n*constants[n] for n in range(1, ORDER+1)])
    primitive = polynomial(f, [0, *(constants[n]/(n+1) for n in range(ORDER))])
    slope_metric = product(product(ds, ds), binomial(m*f, -2))
    gradient = slope_metric+critical*product(dtheta, dtheta)
    sqrt = binomial(gradient, .5)
    inverse_sqrt = binomial(gradient, -.5)

    energy = product(jacobian, sqrt)-c*primitive
    field_force = (product(jacobian_derivative, sqrt)-c*jacobian
                   -m*product(product(product(jacobian, slope_metric), binomial(m*f, -1)),
                              inverse_sqrt))
    force_s = product(product(product(jacobian, ds), binomial(m*f, -2)), inverse_sqrt)
    force_theta = critical*product(product(jacobian, dtheta), inverse_sqrt)
    return energy, (field_force, force_s, force_theta)


def graph(fields):
    theta = 2*np.pi*(np.arange(32)+0.5)/32
    f = np.zeros((ORDER+1, len(fields["weights"]), len(theta)))
    ds, dtheta = np.zeros_like(f), np.zeros_like(f)
    for order, spectrum in ((1, {1: fields["ground"]}),
                            (2, dict(zip((0, 2), fields["second_order"])))):
        for harmonic, coefficients in spectrum.items():
            wave = np.cos(harmonic*theta)
            profile = coefficients @ fields["values"]
            f[order] += profile[:, None]*wave
            ds[order] += (coefficients @ fields["gradients"])[:, None]*wave
            dtheta[order] -= profile[:, None]*harmonic*np.sin(harmonic*theta)
    return theta, (f, ds, dtheta)


def geometric_data(alpha):
    round_radius = np.arctanh(alpha)
    bulge = brentq(lambda r: area(r)-4*volume(r)/alpha, round_radius, round_radius+3)
    return {"alpha": alpha, "cap_bulge_radius": bulge}


def sixth_order(alpha, modes, quadrature, *, verify_corrected=False):
    fields = reduced_quartic(geometric_data(alpha), modes, quadrature, include_response=True)
    theta, profiles = graph(fields)
    energy, forces = action_jets(fields, *profiles)
    weights, values, gradients = [fields[key] for key in ("weights", "values", "gradients")]
    averaged = np.mean(energy, axis=2) @ weights
    assert abs(averaged[4]-fields["quartic"]) < 3e-12
    assert max(abs(averaged[i]) for i in (1, 2, 3, 5)) < 3e-12
    levels, basis = eigh(fields["radial_hessian"], fields["overlap"])
    correction = 0.
    projected_kernel = None
    third_order = {}
    for harmonic in (1, 3):
        cosine = np.cos(harmonic*theta)
        sine = np.sin(harmonic*theta)
        source = values @ (weights*np.mean(forces[0][3]*cosine
                                           -harmonic*forces[2][3]*sine, axis=1))
        source += gradients @ (weights*np.mean(forces[1][3]*cosine, axis=1))
        spectrum = basis.T @ source
        start = 1 if harmonic == 1 else 0
        if harmonic == 1:
            projected_kernel = float(fields["ground"] @ source)
        denominator = levels[start:]+harmonic**2*fields["critical"]
        correction -= np.sum(spectrum[start:]**2/denominator)
        if verify_corrected:
            third_order[harmonic] = -2*basis[:, start:] @ (spectrum[start:]/denominator)
    assert abs(projected_kernel-4*averaged[4]) < 3e-11
    result = {"alpha": alpha, "quartic": float(averaged[4]), "raw_sixth": float(averaged[6]),
            "third_order_response_correction": float(correction),
            "reduced_sixth": float(averaged[6]+correction),
            "projected_third_order_force": projected_kernel}
    if verify_corrected:
        f, ds, dtheta = profiles
        for harmonic, coefficients in third_order.items():
            wave = np.cos(harmonic*theta)
            profile = coefficients @ values
            f[3] += profile[:, None]*wave
            ds[3] += (coefficients @ gradients)[:, None]*wave
            dtheta[3] -= profile[:, None]*harmonic*np.sin(harmonic*theta)
        corrected, _ = action_jets(fields, f, ds, dtheta)
        independently_evaluated = float(np.mean(corrected[6], axis=1) @ weights)
        assert abs(independently_evaluated-result["reduced_sixth"]) < 3e-11
        result["sixth_from_direct_third_order_graph"] = independently_evaluated
    return result


def unfolding():
    z, sigma, quartic, sixth = sp.symbols("z sigma b d", real=True)
    action = sigma*z/4+quartic*z*z+sixth*z**3
    derivative = sp.diff(action, z)
    fold = {z: -quartic/(3*sixth), sigma: 4*quartic**2/(3*sixth)}
    equal_action = {z: -quartic/(2*sixth), sigma: quartic**2/sixth}
    assert sp.simplify(derivative.subs(fold)) == 0
    assert sp.simplify(sp.diff(derivative, z).subs(fold)) == 0
    assert sp.simplify(derivative.subs(equal_action)) == 0
    assert sp.simplify(action.subs(equal_action)) == 0
    return {"fold_detuning": "4*b^2/(3*d)", "equal_action_detuning": "b^2/d",
            "at_quartic_zero_amplitude_fourth_power": "-sigma/(12*d)"}


def main():
    data_dir = Path(__file__).resolve().parents[1]/"data"
    certificate = json.loads((data_dir/"toe_20261116_Tpq_M5_cap_spectator_branch.json").read_text())
    root = certificate["sampled_sign_change_in_alpha"]
    coarse = sixth_order(root, 22, 300)
    fine = sixth_order(root, 32, 460, verify_corrected=True)
    assert abs(fine["quartic"]) < 2e-10
    assert abs(fine["reduced_sixth"]-coarse["reduced_sixth"]) < 1e-8
    assert fine["reduced_sixth"] > 0.002
    result = {"crossing": fine, "coarse_at_crossing": coarse,
              "neighboring": [sixth_order(root+offset, 28, 390) for offset in (-.002, .002)],
              "leading_two_parameter_unfolding": unfolding()}
    path = data_dir/"toe_20261116_Tpq_M5_cap_sixth_order.json"
    path.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(f"Verified the reduced sixth-order coefficient: {fine['reduced_sixth']:.10g}")


if __name__ == "__main__":
    main()
