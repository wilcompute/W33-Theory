"""Evaluate the cap's bifurcation when a spectator-circle mode reaches zero."""

import json
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import Legendre
from scipy.linalg import eigh, solve
from scipy.optimize import brentq
import sympy as sp

from toe_20261116_Tpq_M5_finite_stripe import area, volume
from toe_20261116_Tpq_M5_cap_geometric_threshold import meridian_quadrature


def reduced_quartic(row, mode_count, quadrature_count, *, include_response=False):
    alpha, bulge = row["alpha"], row["cap_bulge_radius"]
    c = 4/alpha
    r, weights, _, _, v, radial_speed, h, potential = meridian_quadrature(
        alpha, bulge, quadrature_count
    )
    weights /= np.sum(weights)
    basis = [Legendre.basis(i) for i in range(mode_count)]
    x = 2*(r/bulge)**2-1
    values = np.array([polynomial(x) for polynomial in basis])
    gradients = np.array([polynomial.deriv()(x)*4*r*radial_speed/bulge**2
                          for polynomial in basis])
    overlap = (values*weights) @ values.T
    radial_hessian = ((gradients*weights) @ gradients.T
                      - (values*(weights*potential)) @ values.T)
    eigenvalue, eigenvector = eigh(radial_hessian, overlap, subset_by_index=[0, 0])
    critical = -eigenvalue[0]
    psi = eigenvector[:, 0] @ values
    gradient = eigenvector[:, 0] @ gradients
    assert abs(weights @ (psi*psi)-1) < 1e-10

    meridian_curvature = c-4*h
    # Normal tube volume J=(1+meridian_curvature*f)*
    # (cosh(v*f)+(h/v)*sinh(v*f))^4.
    angular2 = 6*h*h+2*v*v
    angular3 = 4*h**3+(20/3)*h*v*v
    angular4 = h**4+8*h*h*v*v+(5/3)*v**4
    j2 = angular2+4*h*meridian_curvature
    j3 = angular3+meridian_curvature*angular2
    j4 = angular4+meridian_curvature*angular3
    assert np.max(abs(j2-c*c/2+potential/2)) < 1e-12
    potential3 = j3-c*j2/3
    potential4 = j4-c*j3/4
    gradient3 = (c-2*meridian_curvature)/2
    gradient4 = (j2-2*meridian_curvature*c+3*meridian_curvature**2)/2

    scale_direct = (3*potential4*psi**4/8
                    +3*gradient4*psi**2*gradient**2/8+j2*critical*psi**4/16
                    -(3*gradient**4+2*critical*psi**2*gradient**2
                      +3*critical**2*psi**4)/64)
    direct = float(weights @ scale_direct)

    source = 3*potential3*psi**2+gradient3*gradient**2
    derivative_source = 2*gradient3*psi*gradient
    spectator_source = c*critical*psi**2/2
    b0 = (values @ (weights*(source+spectator_source))
          + gradients @ (weights*derivative_source))/2
    b2 = (values @ (weights*(source+3*spectator_source))
          + gradients @ (weights*derivative_source))/4
    answer0 = solve(radial_hessian, b0, assume_a="sym")
    answer2 = solve((radial_hessian+4*critical*overlap)/2, b2, assume_a="pos")
    complement = -(b0 @ answer0+b2 @ answer2)/2
    if include_response:
        return {"critical": critical, "quartic": direct+complement, "pressure": c,
                "weights": weights, "speed": v, "angular_curvature": h,
                "meridian_curvature": meridian_curvature,
                "values": values, "gradients": gradients, "overlap": overlap,
                "radial_hessian": radial_hessian, "ground": eigenvector[:, 0],
                "second_order": (-answer0, -answer2)}
    return float(critical), direct, float(complement)


def track(row):
    coarse = reduced_quartic(row, 22, 350)
    fine = reduced_quartic(row, 34, 520)
    quartic = fine[1]+fine[2]
    change = abs(sum(coarse[1:])-quartic)
    assert abs(coarse[0]-fine[0]) < 1e-9
    assert change < 2e-4*abs(quartic), (row["alpha"], coarse, fine, change)
    assert abs(quartic) > 100*change
    return {"alpha": row["alpha"], "critical_wave_number_squared": fine[0],
            "direct_quartic": fine[1], "complementary_response_quartic": fine[2],
            "reduced_quartic": quartic, "quartic_change_under_resolution_check": change}


def flat_limit():
    # Unit Euclidean S^5 times a circle, with critical K=5 and pressure 5.
    c, critical = 5, 5
    j2, j3, j4 = 10, 10, 5
    potential3 = j3-sp.Rational(c*j2, 3)
    potential4 = j4-sp.Rational(c*j3, 4)
    direct = 3*potential4/8+sp.Rational(j2*critical, 16)-sp.Rational(3*critical**2, 64)
    b0 = (3*potential3+sp.Rational(c*critical, 2))/2
    b2 = (3*potential3+sp.Rational(3*c*critical, 2))/4
    complement = -(b0**2/(-5)+b2**2/sp.Rational(15, 2))/2
    assert direct+complement == -sp.Rational(35, 48)
    return str(direct+complement)


def find_zero(modes, quadrature):
    def coefficient(alpha):
        r0 = np.arctanh(alpha)
        bulge = brentq(lambda r: area(r)-4*volume(r)/alpha, r0, r0+3)
        _, direct, complementary = reduced_quartic(
            {"alpha": alpha, "cap_bulge_radius": bulge}, modes, quadrature
        )
        return direct+complementary

    return brentq(coefficient, 0.85, 0.95, xtol=2e-10)


def main():
    data_dir = Path(__file__).resolve().parents[1]/"data"
    input_path = data_dir/"toe_20261116_Tpq_M5_finite_stripe.json"
    parents = json.loads(input_path.read_text(encoding="utf-8"))
    zero = find_zero(34, 520)
    assert abs(zero-find_zero(22, 350)) < 2e-7
    result = {
        "control_families": [track(row) for row in parents["families"]],
        "actual_warped_backgrounds": [
            {"chern_pair": row["chern_pair"], **track(row)} for row in parents["actual_warped_backgrounds"]
        ],
        "critical_mode_normalization": "meridian weighted mean of psi squared equals one",
        "euclidean_limit_quartic_times_cap_radius_fourth": flat_limit(),
        "sampled_sign_change_in_alpha": zero,
    }
    assert all(row["reduced_quartic"] > 0 for row in result["actual_warped_backgrounds"])
    output = data_dir/"toe_20261116_Tpq_M5_cap_spectator_branch.json"
    output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print("Verified the spectator-mode bifurcation coefficients and complementary response.")


if __name__ == "__main__":
    main()
