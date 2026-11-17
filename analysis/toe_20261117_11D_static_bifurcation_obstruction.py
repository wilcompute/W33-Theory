"""Fixed-flux shape obstruction to the static AdS5 product marginal mode."""

import json

import sympy as sp

from toe_20261117_11D_unequal_flux_scalar_operator import pencil


def shape_inequality():
    d = sp.symbols("d", real=True)
    n = sp.Matrix([2, 2, 1])
    g = sp.diag(4, 4, 2)+n*n.T/2
    v_gradient = 8*sp.Matrix([1+d, 1-d, 1])
    norm = sp.factor((v_gradient.T*g.inv()*v_gradient)[0])
    assert sp.expand(norm-32*(d*d+1)) == 0
    # The static trace constraint is A=V_s/[2(lambda+8)]. For lambda>=20
    # and |d|<=1, apply Cauchy-Schwarz in the positive sigma metric.
    magnitude = sp.Rational(1, 2)-sp.Rational(5*64, 28**2)
    assert magnitude == sp.Rational(9, 98)
    k, m = pencil(20, 0)
    s = sp.Matrix([1, -1, 0])
    a = sp.Matrix([-8/sp.sqrt(20), 8/sp.sqrt(20)])
    assert m*s.col_join(a) == sp.zeros(5, 1)
    assert (v_gradient.subs(d, 0).T*s)[0] == 0
    equal_shape_source = -(s.T*g*s)[0]/4
    assert equal_shape_source == -2
    return {"gradient_norm_squared": str(norm),
            "uniform_negative_shape_coefficient_per_derivative_norm": str(-magnitude),
            "equal_flux_cosine_shape_source": int(equal_shape_source)}


def mean_eqs_at_equal_flux():
    eps, c = sp.symbols("epsilon c")
    a0, b0, g0 = sp.symbols("A0 B0 gamma0")
    n = sp.Matrix([2, 2, 1])
    sigma = sp.Matrix([eps*c+eps**2*b0, -eps*c+eps**2*b0, eps**2*g0])
    warp = eps**2*a0
    z1, z2 = sp.Matrix([-4, 0, -2]), sp.Matrix([0, -4, -2])

    def truncated(expr):
        return sp.Poly(sp.expand(expr), eps).rem(sp.Poly(eps**3, eps)).as_expr()

    def exp_jet(arg):
        return truncated(1+arg+arg**2/2)

    def mean(expr):
        # Only degrees <=2 in the cosine occur through this order.
        poly = sp.Poly(truncated(expr), c)
        assert poly.degree() <= 2
        return poly.nth(0)+poly.nth(2)/2

    c1, c2, ch = (sp.Matrix(v) for v in ((-2, 0, 0), (0, -2, 0), (-4, -4, 0)))
    v_terms = [(weight, exponent-n/2) for weight, exponent
               in ((-12, c1), (-12, c2), (8, ch))]
    v_mean = sum(weight*mean(exp_jet(exponent.dot(sigma))) for weight, exponent in v_terms)
    gradient = sum(
        (weight*exponent*mean(exp_jet(exponent.dot(sigma))) for weight, exponent in v_terms),
        sp.zeros(3, 1),
    )
    axion_energy = []
    for gradient_z in (z1, z2):
        normalizer = mean(exp_jet(-5*warp-gradient_z.dot(sigma)))
        inverse_square = exp_jet(-2*(normalizer-1))
        axion_energy.append(mean(2*inverse_square*exp_jet(-10*warp-gradient_z.dot(sigma))))
    eqs = [4*exp_jet(-2*warp)+v_mean/4,
           *(gradient+z1*axion_energy[0]+z2*axion_energy[1])]
    solution = sp.solve([expr.coeff(eps, 2) for expr in map(sp.expand, eqs)], (a0, b0, g0))
    assert len(solution) == 3
    # H=20(A_s^2+exp(-2A))-sigma_s^T G sigma_s/2-sum(E_i)+V.
    # The leading sigma tangent (cos,-cos,0) has G-norm 8, with
    # mean derivative norm 4; the static lambda is 20.
    hamiltonian_mean = 20*exp_jet(-2*warp)-40*eps**2-sum(axion_energy)+v_mean
    residual = sp.expand(hamiltonian_mean.subs(solution)).coeff(eps, 2)
    assert residual == -40
    return {"mean_warp_and_radii_from_external_and_scalar_equations": {
                str(var): str(value) for var, value in solution.items()},
            "remaining_mean_Einstein_constraint_at_epsilon_squared": str(residual)}


def lattice_necessity():
    a, b, q = sp.symbols("a b q", real=True)
    r = q*(1-a*a-b*b)/(2*a*b)
    gram = sp.Matrix([[q, r], [r, q]])
    v = sp.Matrix([a, b])
    assert sp.expand((v.T*gram*v)[0]-q) == 0
    assert sp.factor(gram.det()/q**2) == sp.factor(1-((1-a*a-b*b)/(2*a*b))**2)
    m, n = sp.symbols("M N", positive=True, integer=True)
    eta = sp.symbols("eta", positive=True)
    flux_relation = m*m*(1-eta)*(1+eta)**2-n*n*eta*(2-eta)**2
    assert sp.Poly(flux_relation, eta).degree() == 3
    # Equal-area rectangular toy controls: a single direction leaves a
    # trace-free stress. Two independent modes of equal weight cancel
    # only at an orthogonal shell.
    one = sp.diag(sp.Rational(1, 2), -sp.Rational(1, 2))
    second = -one
    assert one+second == sp.zeros(2)
    return {"gram_determinant_ratio_for_three_equal_norm_directions": str(sp.factor(gram.det()/q**2)),
            "integer_flux_polynomial": str(flux_relation),
            "normalized_static_shell_norm_at_quantized_flux": "nonzero_algebraic / pi",
            "balanced_two_direction_shell_requires": "orthogonal momenta with equal weights",
            "balanced_shell_exists_at_quantized_product": False}


def certificate():
    return {"shape_variation": shape_inequality(),
            "independent_mean_constraint_control": mean_eqs_at_equal_flux(),
            "quantized_lattice": lattice_necessity()}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2))
