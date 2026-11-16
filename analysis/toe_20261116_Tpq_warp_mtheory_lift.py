"""Check the warped M-theory lift and neutral-base spin-two tower."""

import json
from pathlib import Path

import numpy as np
import sympy as sp
from numpy.polynomial.legendre import Legendre, leggauss
from scipy.linalg import eigh

from toe_20261116_Tpq_coupled_warp_branch import metric_response, numerical_branch, scalar_reduction


def exact_lift_checks():
    a, d, b, c = sp.symbols("A D B C")
    log_rho = c-5*a/3
    external = 2*a+2*log_rho/3
    torus = -4*log_rho/3
    first_sphere = 2*d-10*a/3+2*log_rho/3
    second_sphere = 2*b-10*a/3+2*log_rho/3
    measure = sp.expand(first_sphere+second_sphere+torus+3*external/2)
    assert measure == -16*a/3+2*d+2*b+c
    assert sp.expand(external-torus+measure) == -20*a/3+2*d+2*b+3*c
    assert sp.expand(external-first_sphere+measure) == 2*b+c
    horizontal_flux = sp.expand(-5*a+log_rho+2*d+2*b-20*a/3)
    assert horizontal_flux == -40*a/3+2*d+2*b+c

    momentum = sp.Symbol("lambda_T")
    mean_square = sp.Rational(1, 5)
    mean_second_warp = sp.Rational(28, 3)*mean_square
    mean_second_fiber = sp.Rational(20, 9)
    direct = momentum*(2*mean_second_fiber-4*mean_second_warp/3+8*mean_square)
    mixing = -(4*momentum/3)**2*mean_square/32
    shift = sp.expand(direct+mixing)
    assert shift == 32*momentum/9-momentum**2/90
    gap = sp.sqrt(sp.Rational(656, 9))-8
    assert gap > sp.Rational(1, 2)
    return {"spin_two_shift_per_quadrupole_amplitude_squared": str(shift),
            "homogeneous_BF_deficit_at_resonance": str(gap)}


def numerical_spin_two(result, momentum, count):
    x, weights = leggauss(100)
    profiles = np.array(result["even_legendre_profiles"])
    profile_basis = np.array([Legendre.basis(2*i)(x) for i in range(profiles.shape[1])])
    a, d, b, c = profiles @ profile_basis
    k1 = (32+result["lambda_minus_32"])/6
    basis = [Legendre.basis(2*i) for i in range(count)]
    values = np.array([poly(x) for poly in basis])
    slopes = np.array([poly.deriv()(x) for poly in basis])
    gradient = k1*(1-x*x)*np.exp(2*b+c)
    mass = np.exp(2*d+2*b+3*c-20*a/3)
    norm = np.exp(2*d+2*b+c-16*a/3)
    stiffness = ((slopes*(weights*gradient)) @ slopes.T
                 + momentum*(values*(weights*mass)) @ values.T)
    overlap = (values*(weights*norm)) @ values.T
    return float(eigh(stiffness, overlap, subset_by_index=[0, 0], eigvals_only=True)[0])


def examples():
    x, y = scalar_reduction()
    metric = metric_response(x, y)
    rows = []
    for p, q in ((7, 8), (8, 9), (38, 43)):
        warp = numerical_branch(p, q, metric, 8, include_profiles=True)
        amplitude = warp["quadrupole_amplitude"]
        for momentum in (0, 1, 4, 12):
            coarse = numerical_spin_two(warp, momentum, 6)
            fine = numerical_spin_two(warp, momentum, 10)
            assert abs(coarse-fine) < 5e-10
            if momentum == 0:
                assert abs(fine) < 5e-10
                continue
            # Restore the once-fixed Page charge, since lambda_T scales as L^4.
            fixed_page_momentum = momentum/(1+warp["page_integral_relative_shift"])
            mass = numerical_spin_two(warp, fixed_page_momentum, 10)
            predicted = amplitude**2*(32*momentum/9-momentum**2/90)
            relative_tolerance = 0.002 if abs(warp["lambda_minus_32"]) < 0.01 else 0.1
            assert abs((mass-momentum)/predicted-1) < relative_tolerance, (
                p, q, momentum, mass-momentum, predicted
            )
            rows.append({"chern_pair": [p, q], "unwarped_bare_torus_eigenvalue": momentum,
                         "fixed_Page_spin_two_shift": mass-momentum,
                         "numerical_over_second_order": (mass-momentum)/predicted})
    return rows


def main():
    data = exact_lift_checks()
    data["examples"] = examples()
    output = Path(__file__).resolve().parents[1]/"data"/"toe_20261116_Tpq_warp_mtheory_lift.json"
    output.write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    print("Verified the warped duality weights and the second-order spin-two shifts.")


if __name__ == "__main__":
    main()
