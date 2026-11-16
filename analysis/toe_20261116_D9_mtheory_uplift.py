"""Verify the invariant torus uplift obstruction and the sibling's BF modes."""

import json
from fractions import Fraction as F
from math import pi, sqrt
from pathlib import Path

import sympy as sp


def verify_product_solution(eta):
    curvature = (4*(1+eta), 4*(2-eta), 0)
    flux_sq = (16, 8*eta, 8*(1-eta))
    u_sq, p_sq, q_sq = flux_sq
    total = sum(flux_sq)
    projected = (u_sq+p_sq, u_sq+q_sq, p_sq+q_sq)
    assert sp.expand(-total/6 + 4) == 0
    for expected, legs in zip(curvature, projected):
        assert sp.expand(legs/2-total/6-expected) == 0
    assert sum(curvature) == 12
    return curvature, flux_sq


def verify_homogeneous_radions(eta, curvature, flux_sq):
    ones = sp.ones(3, 1)
    kinetic = 4*sp.eye(3) + sp.Rational(8, 3)*ones*ones.T
    exponent = [sp.Matrix(column)-sp.Rational(4, 3)*ones for column in
                ((-2, 0, 0), (0, -2, 0), (-4, -4, 0), (-4, 0, -4), (0, -4, -4))]
    coefficients = [-2*curvature[0], -2*curvature[1], *[sp.sympify(value)/2 for value in flux_sq]]
    assert sum(coefficients) == -12
    tadpole = sum((a*v for a, v in zip(coefficients, exponent)), sp.zeros(3, 1))
    assert tadpole.applyfunc(sp.expand) == sp.zeros(3, 1)
    hessian = sum((a*v*v.T for a, v in zip(coefficients, exponent)), sp.zeros(3))
    mass_matrix = kinetic.inv()*hessian
    mass = sp.Symbol("m")
    characteristic = mass_matrix.charpoly(mass).as_expr()
    expected = (mass-32)*((mass-4)**2-64-320*(eta-sp.Rational(1, 2))**2)
    assert sp.expand(characteristic-expected) == 0
    equal = mass_matrix.subs(eta, sp.Rational(1, 2))
    exchange_odd = sp.Matrix([1, -1, 0])
    assert equal*exchange_odd == -4*exchange_odd
    assert set(equal.eigenvals()) == {-4, 12, 32}
    return {"characteristic_polynomial": str(expected),
            "equal_flux_squared_masses_ads_units": [-4, 12, 32],
            "bf_bound_ads_units": -4,
            "equal_flux_bf_eigenvector_in_log_radii": [1, -1, 0]}


def verify_equal_flux_band():
    t, phi, perturbation_sq, contraction = sp.symbols("t phi perturbation_sq contraction")
    # Expand the two Maxwell terms in the canonically normalized difference
    # field phi, with differentials dA_1, dA_2 = dA_bg +/- dA_-/sqrt(2).
    v = t*phi/sp.sqrt(8)
    kinetic_flux_terms = -(
        sp.exp(-4*v)*(8+sp.sqrt(2)*t*contraction+t*t*perturbation_sq/2)
        +sp.exp(4*v)*(8-sp.sqrt(2)*t*contraction+t*t*perturbation_sq/2)
    )/4
    lagrangian = 24*sp.cosh(2*v)+kinetic_flux_terms
    quadratic = sp.diff(lagrangian, t, 2).subs(t, 0)/2
    assert sp.simplify(quadratic - (2*phi*phi+phi*contraction-perturbation_sq/4)) == 0
    q, m = sp.symbols("q m")
    mass_block = sp.Matrix(((q*q-4, 4*q), (4*q, q*q)))
    characteristic = mass_block.charpoly(m).as_expr()
    lam = sp.Symbol("lam")
    assert sp.expand(characteristic.subs(q*q, lam)
                     - ((m-lam+2)**2-(4+16*lam))) == 0
    assert sp.factor(characteristic.subs(m, -4)) == q*q*(q*q-12)
    minimum_at = sp.Rational(15, 4)
    lower = lam-2-sp.sqrt(4+16*lam)
    assert lower.subs(lam, minimum_at) == -sp.Rational(25, 4)
    assert sp.diff(lower, lam).subs(lam, minimum_at) == 0
    return {"unstable_open_band_adimensional_torus_eigenvalue": [0, 12],
            "lowest_value_in_continuous_band_ads_units": "-25/4",
            "minimum_torus_eigenvalue_location": "15/4",
            "square_torus_flux_ratio_threshold": pi/4,
            "hexagonal_torus_flux_ratio_threshold": pi/(2*sqrt(3)),
            "sample_square_tori": [
                {"mixed_to_horizontal_flux_ratio": str(ratio),
                 "first_torus_eigenvalue_ads_units": 3*pi/float(ratio),
                 "unstable_in_this_sector": 0 < 3*pi/float(ratio) < 12}
                for ratio in (F(1, 2), F(4, 5), F(1), F(2))]}


def verify_quantization_and_probe(eta, curvature, flux_sq):
    # Use symbolic flux units, then set the universal 2pi factors explicitly.
    n0, n = sp.symbols("N0 N", positive=True)
    equal_l_cubed_over_lp = sp.pi*n0*36/8
    equal_area_over_l_sq = sp.simplify(2*sp.pi**2*n*6/(2*equal_l_cubed_over_lp))
    assert equal_area_over_l_sq == 4*sp.pi*n/(3*n0)
    square_momentum_sq = sp.simplify(4*sp.pi**2/equal_area_over_l_sq)
    assert square_momentum_sq == 3*sp.pi*n0/n
    ratio = sp.sqrt(eta/(1-eta))*(2-eta)/(1+eta)
    log_slope = 1/(2*eta*(1-eta))-1/(2-eta)-1/(1+eta)
    assert sp.simplify(sp.diff(ratio, eta)/ratio-log_slope) == 0
    assert sp.factor(log_slope*2*eta*(1-eta)*(2-eta)*(1+eta)) == 5*eta**2-5*eta+2
    # The dual magnetic form's comass is the largest block eigenvalue in
    # magnitude. Its torus block gives charge/tension one in the probe test.
    probe_squared = [sp.sympify(f)/16 for f in flux_sq]
    assert probe_squared == [1, eta/2, (1-eta)/2]
    return {"curvature_sum_in_ads_units": int(sum(curvature)),
            "equal_flux_torus_area_over_ads_radius_squared": str(equal_area_over_l_sq),
            "equal_flux_square_torus_first_eigenvalue": str(square_momentum_sq),
            "m5_probe_charge_to_tension_squared": list(map(str, probe_squared))}


def main():
    eta = sp.symbols("eta")
    curvature, flux_sq = verify_product_solution(eta)
    data = {"invariant_product": verify_quantization_and_probe(eta, curvature, flux_sq),
            "homogeneous_radius_sector": verify_homogeneous_radions(eta, curvature, flux_sq),
            "equal_flux_torus_momentum_sector": verify_equal_flux_band()}
    output = Path(__file__).resolve().parents[1] / "data" / "toe_20261116_D9_mtheory_uplift.json"
    output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("Verified the torus product, quantization, homogeneous BF violation, and equal-flux BF band.")


if __name__ == "__main__":
    main()
