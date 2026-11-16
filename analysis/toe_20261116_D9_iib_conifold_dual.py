"""Verify the IIB circle dual, its charge normalizations, and its planar D3 wall."""

import json
from math import gcd
from pathlib import Path

import sympy as sp
from sympy.matrices.normalforms import smith_normal_form


def verify_einstein_circle_and_normalizations():
    eta, n0, n1, gs = sp.symbols("eta N0 N1 gs", positive=True)
    k1, k2 = 4*(1+eta), 4*(2-eta)
    mixed_flux = sp.sqrt(8*eta)
    fiber_over_ads = 2*mixed_flux/(n1*k1)
    charge_ratio_sq = (1-eta)/eta*(k1/k2)**2
    twist_sq = ((fiber_over_ads*n1*k1/2)**2,
                (fiber_over_ads*n1*k2/2)**2*charge_ratio_sq)
    assert sp.simplify(twist_sq[0]-8*eta) == 0
    assert sp.simplify(twist_sq[1]-8*(1-eta)) == 0
    for curvature, twist in zip((k1, k2), twist_sq):
        assert sp.simplify(curvature-twist/2-4) == 0
    assert sp.simplify(sum(twist_sq)/2-4) == 0

    volume = 32*sp.pi**3*fiber_over_ads/(k1*k2)
    central_iib = sp.pi**3*n0*n0/(4*volume)
    l_cubed_over_lp = sp.pi*n0*k1*k2/8
    area_over_lp_sq = 2*sp.pi**2*n1*k1/(mixed_flux*l_cubed_over_lp**sp.Rational(1, 3))
    m_internal_volume_over_lp_six = (area_over_lp_sq*16*sp.pi**2
                                     * l_cubed_over_lp**sp.Rational(4, 3)/(k1*k2))
    central_m = sp.pi*l_cubed_over_lp*m_internal_volume_over_lp_six/(128*sp.pi**7)
    assert sp.simplify(central_iib-central_m) == 0

    # Classical (p,q) winding mass from the IIB tension times a circle length.
    # This is the momentum term, before the flux mixing in the BF calculation.
    string_length_ratio_to_alpha2 = 4*sp.pi**4*gs*n0/volume
    winding_scale_sq = fiber_over_ads**2*string_length_ratio_to_alpha2/gs
    m_torus_scale_sq = 4*sp.pi**2*l_cubed_over_lp**sp.Rational(2, 3)/area_over_lp_sq
    assert sp.simplify(winding_scale_sq-m_torus_scale_sq) == 0
    equal = {eta: sp.Rational(1, 2)}
    assert sp.simplify(volume.subs(equal)-16*sp.pi**3/(27*n1)) == 0
    assert sp.simplify(central_iib.subs(equal)-sp.Rational(27, 64)*n1*n0**2) == 0
    assert sp.simplify(winding_scale_sq.subs(equal)-3*sp.pi*n0/n1) == 0
    return {"equal_fiber_radius_over_ads_radius": "2/(3*N)",
            "equal_unit_ricci_volume": str(sp.factor(volume.subs(equal))),
            "equal_string_frame_ads_radius_to_fourth_over_alpha_prime_squared":
                str(sp.factor(string_length_ratio_to_alpha2.subs(equal))),
            "equal_leading_holographic_a_and_c": str(sp.factor(central_iib.subs(equal))),
            "equal_winding_mass_squared_ads_prefactor": str(sp.factor(winding_scale_sq.subs(equal)))}


def verify_radion_duality():
    # Log radii on the IIB side are (beta1+betaT/2, beta2+betaT/2, -3 betaT/2).
    half = sp.Rational(1, 2)
    jacobian = sp.Matrix(((1, 0, half), (0, 1, half), (0, 0, -3*half)))
    dims = sp.Matrix([2, 2, 1])
    ones = sp.ones(3, 1)
    kinetic_iib = 2*sp.diag(*dims) + sp.Rational(2, 3)*dims*dims.T
    kinetic_m = 4*sp.eye(3) + sp.Rational(8, 3)*ones*ones.T
    assert jacobian.T*kinetic_iib*jacobian == kinetic_m
    iib_exponents = ((-2, 0, 0), (0, -2, 0), (-4, 0, 2), (0, -4, 2), (-4, -4, -2))
    m_exponents = ((-2, 0, 0), (0, -2, 0), (-4, 0, -4), (0, -4, -4), (-4, -4, 0))
    for iib, m in zip(iib_exponents, m_exponents):
        assert jacobian.T*(sp.Matrix(iib)-sp.Rational(2, 3)*dims) == (
            sp.Matrix(m)-sp.Rational(4, 3)*ones)
    eta = sp.Symbol("eta")
    paper_lambda = 1/(1+eta)
    paper_discriminant = 16*(49-60/paper_lambda+20/paper_lambda**2)
    assert sp.expand(paper_discriminant-(64+320*(eta-half)**2)) == 0
    return {"log_radius_jacobian": [[str(value) for value in row] for row in jacobian.tolist()],
            "matching_radion_kinetic_and_all_five_potential_terms": True,
            "gubser_mitra_splitting_squared": str(sp.factor(paper_discriminant))}


def verify_discrete_groups_and_spin_lifts():
    rows = []
    for p, q in ((1, 1), (2, 2), (3, 3), (6, 10), (5, 0), (0, 7), (11, -13)):
        g = gcd(p, q)
        charges = sp.Matrix(((p, 0), (q, 0), (0, p), (0, q)))
        smith = smith_normal_form(charges, domain=sp.ZZ)
        assert abs(smith[0, 0]) == abs(smith[1, 1]) == g
        assert gcd(*tuple(abs(value) for value in charges)) == g
        rows.append({"chern_numbers": [p, q], "fiber_fundamental_group_order": g,
                     "torus_translation_smith_factors": [g, g]})
    preserved = []
    for g in range(1, 13):
        # Measure the total spin phase in units of 2*pi. An alternative
        # generator lift adds one half-turn and is allowed only at even g.
        lifts = (0, sp.Rational(1, 2)) if g % 2 == 0 else (0,)
        if any((sp.Rational(1, g)+lift).is_integer for lift in lifts):
            preserved.append(g)
    assert preserved == [1, 2]
    return {"charge_samples": rows, "equal_flux_supersymmetric_iib_quotient_orders_for_some_lift": preserved,
            "k2_requires_alternative_spin_lift": True}


def verify_planar_wall():
    r, radius, q_plus, q_minus = sp.symbols("r R Qplus Qminus", positive=True)
    outside = q_plus/r**4
    inside = q_minus/r**4+(q_plus-q_minus)/radius**4
    for branch, charge in ((outside, q_plus), (inside, q_minus)):
        assert sp.simplify(sp.diff(r**5*sp.diff(branch, r), r)) == 0
        assert sp.simplify(-r**5*sp.diff(branch, r)) == 4*charge
    assert sp.simplify((outside-inside).subs(r, radius)) == 0
    jump = sp.simplify(radius**5*sp.diff(outside-inside, r).subs(r, radius))
    assert sp.expand(jump+4*(q_plus-q_minus)) == 0

    # Five-dimensional Einstein action R-G(db)^2/2-V, fixed internal Page flux.
    b, magnetic_density = sp.symbols("b Q", real=True)
    w = 10*sp.exp(-8*b/3)-magnetic_density*sp.exp(-20*b/3)
    potential = -20*sp.exp(-16*b/3)+magnetic_density**2*sp.exp(-40*b/3)/2
    assert sp.simplify(sp.Rational(3, 160)*sp.diff(w, b)**2-w**2/3-potential) == 0
    assert sp.diff(w, b).subs({b: 0, magnetic_density: 4}) == 0
    assert sp.simplify(w.subs(magnetic_density, q_plus)-w.subs(magnetic_density, q_minus)
                       +(q_plus-q_minus)*sp.exp(-20*b/3)) == 0
    # Normalize the wall tension by 2*kappa_5^2. Its Israel metric junction
    # and scalar derivative junction follow from the same superpotential jump.
    delta_w = (w.subs(magnetic_density, q_plus)-w.subs(magnetic_density, q_minus))
    scaled_tension = (q_plus-q_minus)*sp.exp(-20*b/3)
    assert sp.simplify(delta_w/6+scaled_tension/6) == 0
    assert sp.simplify(-sp.Rational(3, 80)*sp.diff(delta_w, b)
                       -sp.Rational(3, 80)*sp.diff(scaled_tension, b)) == 0
    return {"radial_flux_jump": str(jump), "shell_position_is_free_in_classical_planar_solution": True,
            "breathing_gradient_flow_potential": str(potential), "breathing_superpotential": str(w),
            "simultaneous_planar_metric_and_scalar_junctions": True}


def main():
    result = {"metric_and_flux": verify_einstein_circle_and_normalizations(),
              "homogeneous_radions": verify_radion_duality(),
              "topology_and_spin": verify_discrete_groups_and_spin_lifts(),
              "planar_D3_shell": verify_planar_wall()}
    output = Path(__file__).resolve().parents[1] / "data" / "toe_20261116_D9_iib_conifold_dual.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Verified IIB topology, spectral and action matching, winding scales, and the planar wall.")


if __name__ == "__main__":
    main()
