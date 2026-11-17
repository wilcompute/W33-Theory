"""Leading BF eigenvalue shift on the balanced square AdS branch."""

import json

import sympy as sp

from toe_20261117_11D_square_modulated_branch import even_backreaction


def sideband():
    # Work for one of the two equivalent fundamental Fourier directions.
    # The homogeneous fluctuation is delta sigma=(1,-1,0) psi.
    lam, mass = sp.Integer(20), sp.Integer(-4)
    k = sp.sqrt(lam)
    u = sp.Matrix([1, -1, 0])
    f = sp.Matrix([2, 2])
    n = sp.Matrix([2, 2, 1])
    metric = sp.diag(4, 4, 2)+n*n.T/2
    zs = sp.Matrix([[-4, 0], [0, -4], [-2, -2]])
    v_terms = [(number, -n/2+sp.Matrix(exponent)) for number, exponent in
               ((-12, (-2, 0, 0)), (-12, (0, -2, 0)), (8, (-4, -4, 0)))]
    grad_v = sum((coeff*e for coeff, e in v_terms), sp.zeros(3, 1))
    hess_v = sum((coeff*e*e.T for coeff, e in v_terms), sp.zeros(3))
    flux_hess = zs*sp.diag(*[x*x/2 for x in f])*zs.T
    hessian = hess_v+flux_hess
    assert hessian*u == mass*metric*u and (grad_v.T*u)[0] == 0
    # d(Z f_background^2)/d epsilon is -Z_,A u^A f^2.
    d_hessian = sum(
        (coeff*(e.T*u)[0]*e*e.T for coeff, e in v_terms), sp.zeros(3)
    ) - zs*sp.diag(*[f[i]**2*(zs[:, i].T*u)[0]/2 for i in range(2)])*zs.T
    source = d_hessian*u
    a = sp.Matrix(sp.symbols("a1 a2"))
    s = sp.Matrix(sp.symbols("s1 s2 s3"))
    # A and B multiply g_mu_nu psi and nabla_mu nabla_nu psi in
    # the axial-gauge sideband metric. delta chi is a sin(kx) psi.
    warp = k*((f.T*a)[0]-8*k)/(4*(lam+3))
    longitudinal = 3*warp/lam
    trace = 5*warp+mass*longitudinal
    equations = ((mass-lam)*metric*s-hessian*s-k*zs*sp.diag(*f)*a-source).col_join(
        (mass-lam)*a-k*sp.diag(*f)*(zs.T*s+sp.ones(2, 1)*trace/2)
    )
    solution = sp.solve(list(equations), list(s)+list(a))
    s, a = s.subs(solution), a.subs(solution)
    warp, longitudinal, trace = (z.subs(solution) for z in (warp, longitudinal, trace))
    vs = (grad_v.T*s)[0]
    assert 2*(lam-mass+8)*warp == vs+(u.T*hess_v*u)[0]
    assert lam*trace/2 == k*(f.T*a)[0]-3*vs/4-88
    assert s[0] == s[1] and a[0] == a[1]
    return s, a, warp, longitudinal, trace


def density_projection(a0, b0, c0, cs, trace7, trace_internal, k_axion):
    """Project the divergence-form v equation before dividing by sqrt(g_7)."""
    eps, v = sp.symbols("epsilon C")

    def truncate(expr):
        return sp.Poly(sp.expand(expr), eps).rem(sp.Poly(eps**3, eps)).as_expr()

    def exp_jet(arg):
        return truncate(1+arg+arg**2/2)

    def mean(expr):
        p = sp.Poly(truncate(expr), v)
        assert p.degree() <= 2
        return p.nth(0)+p.nth(2)  # C=cos x+cos y has <C>=0 and <C^2>=1.

    warp, conformal, c, background_v = eps**2*a0, eps**2*b0, eps**2*c0, eps*v
    delta_c, h, ht = eps*cs*v, eps*trace7*v, eps*trace_internal*v
    volume = exp_jet(5*warp+2*conformal)
    delta_v_potential = -96*exp_jet(-18*c/5)*(1+2*background_v**2)
    delta_v_potential += sp.Rational(1728, 5)*background_v*delta_c
    background_v_potential = -96*background_v
    density_rhs = volume*(delta_v_potential+h*background_v_potential/2)
    for g in (-4, 4):
        inv_z = 12*c/5-g*background_v
        integral = mean(exp_jet(-5*warp+2*conformal+inv_z))
        inv_integral = exp_jet(-(integral-1))
        inv_square = exp_jet(-2*(integral-1))
        energy = truncate(2*exp_jet(-10*warp+inv_z)*inv_square)
        # The F_xy perturbation is k a cos along each wave; the
        # coefficient Z F e^(-4B) has no first-order Fourier dependence.
        field_mixed = 2*exp_jet(-5*warp-2*conformal)*inv_integral*eps*k_axion*v
        density_rhs += volume*g*(energy*(g-12*delta_c/5-ht+h/2)+field_mixed)
    rhs = sp.expand(mean(density_rhs))
    assert rhs.coeff(eps, 0) == -32 and 3*a0+2*b0 == 0
    return rhs.coeff(eps, 2)/8


def certificate():
    s, a, warp, longitudinal, trace6 = sideband()
    branch = even_backreaction()["even_backreaction_by_field"]
    a0, b0, c0 = [sp.Rational(branch[key][0]) for key in
                  ("warp_A", "torus_conformal_B", "sphere_mean_c")]
    cs = s[0]
    radius_y7 = s[2]+4*cs/5
    trace7 = trace6-radius_y7
    trace_internal7 = 3*radius_y7/2
    # Each wave carries norm squared 1/2 and the two waves are orthogonal.
    # The derivative-of-determinant term in delta Box averages to zero.
    laplacian_shift = 8*a0+10*trace7
    potential_shift = -96*(2-18*c0/5)+sp.Rational(1728, 5)*cs
    flux_shift = 64*(-4*b0-12*c0/5-8+12*cs/5+trace_internal7)
    shift = (potential_shift+flux_shift)/8-laplacian_shift
    independent = density_projection(
        a0, b0, c0, cs, trace7, trace_internal7, sp.sqrt(20)*a[0]
    )
    assert shift == independent == -sp.Rational(5880, 43)
    return {
        "first_order_axial_sideband_sigma": list(map(str, s)),
        "first_order_axial_sideband_axions_sine": list(map(str, a)),
        "first_order_axial_sideband_external_metric_A_B": list(map(str, (warp, longitudinal))),
        "mean_second_order_laplacian_shift": str(laplacian_shift),
        "mean_second_order_potential_shift": str(potential_shift),
        "mean_second_order_flux_shift": str(flux_shift),
        "coefficient_of_epsilon_squared_in_m2_L2_plus_4": str(shift),
        "independent_density_form_coefficient": str(independent),
    }


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2))
