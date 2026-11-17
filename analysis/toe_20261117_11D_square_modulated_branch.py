"""Quartic normal form for the balanced, equal-flux square torus modulation."""

import json

import sympy as sp


def even_backreaction():
    x, y = sp.symbols("cx cy", real=True)
    a_vars = sp.symbols("a0 a20 a11", real=True)
    b_vars = sp.symbols("b0 b20 b11", real=True)
    c_vars = sp.symbols("c0 c20 c11", real=True)
    variables = a_vars+b_vars+c_vars
    odd = x+y
    even_modes = sp.Matrix([1, 2*(x*x+y*y)-2, x*y])
    a, b, c = (sp.Matrix(group).dot(even_modes) for group in (a_vars, b_vars, c_vars))

    def moment(power):
        return sp.binomial(power, power//2)/2**power if power % 2 == 0 else 0

    def average(expr):
        return sum(coefficient*moment(i)*moment(j) for (i, j), coefficient
                   in sp.Poly(expr, x, y).terms())

    def grad_square(left, right):
        return ((1-x*x)*sp.diff(left, x)*sp.diff(right, x)
                +(1-y*y)*sp.diff(left, y)*sp.diff(right, y))

    def exp_quartic(linear, quadratic):
        return average(quadratic**2/2+linear**2*quadratic/2+linear**4/24)

    def exp_quadratic(linear, quadratic):
        return average(quadratic+linear**2/2)

    assert average(odd**2) == average(grad_square(odd, odd)) == 1
    flux_exponent = -5*a+2*b+sp.Rational(12, 5)*c
    curvature = -20*exp_quartic(0, 3*a+2*b)
    sphere = 24*exp_quartic(2*odd, 5*a+2*b-sp.Rational(18, 5)*c)
    horizontal = -8*exp_quartic(0, 5*a+2*b-sp.Rational(48, 5)*c)
    flux = 4*(exp_quartic(4*odd, flux_exponent)
              -exp_quadratic(4*odd, flux_exponent)**2)
    gradients = 20*average(
        20*grad_square(a, a)+10*grad_square(a, b)
        -sp.Rational(36, 5)*grad_square(c, c)-20*a*grad_square(odd, odd)
    )
    quartic = sp.expand(curvature+sphere+horizontal+flux+gradients)
    hessian = sp.hessian(quartic, variables)
    forcing = sp.Matrix([sp.diff(quartic, v) for v in variables]).subs(dict.fromkeys(variables, 0))
    solved = -hessian.inv()*forcing
    solution = dict(zip(variables, solved, strict=True))
    assert all(sp.diff(quartic, v).subs(solution) == 0 for v in variables)
    quartic_on_shell = quartic.subs(solution)
    assert quartic_on_shell == sp.Rational(36736, 459)
    assert 3*solution[a_vars[0]]+2*solution[b_vars[0]] == 0
    return {
        "fourier_even_basis": ["1", "cos(2x)+cos(2y)", "cos(x)cos(y)"],
        "even_backreaction_by_field": {name: list(map(str, solved[3*i:3*i+3]))
                                       for i, name in enumerate(("warp_A", "torus_conformal_B",
                                                                 "sphere_mean_c"))},
        "constant_even_hessian_determinant": str(hessian.extract([0, 3, 6], [0, 3, 6]).det()),
        "fixed_background_quartic": str(quartic.subs(dict.fromkeys(variables, 0))),
        "relaxed_quartic": str(quartic_on_shell),
        "lambda_shift_coefficient": str(quartic_on_shell/2),
        "normalized_AdS_Newton_coefficient_shift_at_epsilon_fourth": str(quartic_on_shell/8),
    }


def numerical_branch(order, grid, normal, *, asymmetry=0, reference_lambda=None):
    import numpy as np
    from scipy.optimize import brentq, root

    # 17:8 is on the predicted side, and common integer rescaling leaves
    # the dimensionless equations unchanged.
    lam = 3*np.pi*17/8 if reference_lambda is None else reference_lambda
    d = asymmetry
    axis = 2*np.pi*np.arange(grid)/grid
    mode_pairs = [(m, n) for m in range(order+1) for n in range(m+1)]

    def basis(modes):
        spectral = np.array([[
            (m**dx*n**dy)*np.outer(np.cos(m*axis+dx*np.pi/2),
                                    np.cos(n*axis+dy*np.pi/2))
            + ((n**dx*m**dy)*np.outer(np.cos(n*axis+dx*np.pi/2),
                                      np.cos(m*axis+dy*np.pi/2)) if m != n else 0)
            for m, n in modes
        ] for dx, dy in ((0, 0), (1, 0), (0, 1), (2, 0), (0, 2), (1, 1))])
        squared_norms = np.mean(spectral[0]**2, axis=(1, 2))
        return spectral, squared_norms

    even_modes = [(m, n) for m, n in mode_pairs if d or (m+n) % 2 == 0]
    odd_modes = mode_pairs if d else [mn for mn in mode_pairs if mn not in even_modes]
    even, even_norms = basis(even_modes)
    odd, odd_norms = basis(odd_modes)
    size = len(even_modes)

    def equations(coefficients, project=True):
        parts = np.split(coefficients, (size, 2*size, 3*size))
        fields = [np.einsum("i,dijk->djk", c, b, optimize=False)
                  for c, b in zip(parts, (even, even, even, odd), strict=True)]
        (a, ax, ay, axx, ayy, axy), (b, bx, by, bxx, byy, _), (
            c, cx, cy, cxx, cyy, _
        ), (v, vx, vy, vxx, vyy, _) = fields
        reg = np.exp(3*a+2*b)
        vol = np.exp(5*a+2*b)
        war = np.exp(5*a)
        if d:
            sphere_plus = (12+4*d)*np.exp(-18*c/5-2*v)
            sphere_minus = (12-4*d)*np.exp(-18*c/5+2*v)
            horizontal = 8*np.exp(-48*c/5)
            vpot = -sphere_plus-sphere_minus+horizontal
            pot_c = (18*(sphere_plus+sphere_minus)-48*horizontal)/5
            pot_v = 2*(sphere_plus-sphere_minus)
        else:
            ac = np.exp(-18*c/5)
            hc = np.exp(-48*c/5)
            vpot = -24*ac*np.cosh(2*v)+8*hc
            pot_c = (432*ac*np.cosh(2*v)-384*hc)/5
            pot_v = -48*ac*np.sinh(2*v)
        xp, xm = (np.exp(-5*a+2*b+12*c/5+4*sign*v) for sign in (1, -1))
        ep, em = (2*(1+d)*xp/np.mean(xp)**2, 2*(1-d)*xm/np.mean(xm)**2)
        aa, ab = ax*ax+ay*ay, ax*bx+ay*by
        cc, vv = cx*cx+cy*cy, vx*vx+vy*vy
        da, db = axx+ayy, bxx+byy
        kinetic = 20*aa+10*ab-36*cc/5-4*vv
        eqs = np.array([
            -60*reg-5*vol*vpot-5*(ep+em)+lam*war*(5*kinetic-40*da-10*db-200*aa-50*ab),
            -40*reg-2*vol*vpot+2*(ep+em)-10*lam*war*(da+5*aa),
            -vol*pot_c+12*(ep+em)/5+72*lam*war*(cxx+cyy+5*(ax*cx+ay*cy))/5,
            -vol*pot_v+4*(ep-em)+8*lam*war*(vxx+vyy+5*(ax*vx+ay*vy)),
        ])
        if not project:
            tracefree = [
                -5*(axx-ayy-2*(ax*bx-ay*by)+ax*ax-ay*ay)-36*(cx*cx-cy*cy)/5-4*(vx*vx-vy*vy),
                -5*(axy-bx*ay-by*ax+ax*ay)-36*cx*cy/5-4*vx*vy,
            ]
            return [float(np.max(np.abs(m))) for m in (*eqs, *tracefree)]
        return np.concatenate([
            np.mean(eq*fourier[0], axis=(1, 2))/norm
            for eq, fourier, norm in zip(eqs, (even, even, even, odd),
                                         (even_norms, even_norms, even_norms, odd_norms), strict=True)
        ])

    critical = normal.get("static_threshold", 20)
    eps = normal.get("starting_amplitude")
    if eps is None:
        eps = np.sqrt((lam-critical)/float(sp.Rational(normal["lambda_shift_coefficient"])))
    linear_start = np.zeros(3*size+len(odd_modes))
    quadratic_start = np.zeros_like(linear_start)
    odd_start = 3*size+odd_modes.index((1, 0))
    linear_start[odd_start] = 1
    for i, coefficient in enumerate(normal.get("first_order_even_fields", ())):
        linear_start[i*size+even_modes.index((1, 0))] = float(coefficient)
    for i, coefficients in enumerate(normal["even_backreaction_by_field"].values()):
        for mn, coefficient in zip(((0, 0), (2, 0), (1, 1)), coefficients, strict=True):
            quadratic_start[i*size+even_modes.index(mn)] = float(sp.Rational(coefficient))
    if second_order_v := normal.get("second_order_v"):
        for mn, coefficient in zip(((0, 0), (2, 0), (1, 1)), second_order_v, strict=True):
            quadratic_start[3*size+odd_modes.index(mn)] = float(coefficient)

    def seed(amplitude):
        return amplitude*linear_start+amplitude**2*quadratic_start

    if bracket := normal.get("amplitude_bracket"):
        def solve_complement(amplitude):
            def unpack(values):
                return np.insert(values, odd_start, amplitude)

            def projected(values):
                return np.delete(equations(unpack(values)), odd_start)

            result = root(projected, np.delete(seed(amplitude), odd_start), tol=1e-11)
            assert np.max(np.abs(projected(result.x))) < 1e-9
            coefficients = unpack(result.x)
            return equations(coefficients)[odd_start], coefficients

        amplitude = brentq(lambda value: solve_complement(value)[0],
                           *bracket, xtol=1e-11)
        _, coefficients = solve_complement(amplitude)
    else:
        coefficients = root(equations, seed(eps), tol=1e-10).x
        assert abs(coefficients[odd_start]-eps) < eps/10
    assert np.max(np.abs(equations(coefficients))) < 1e-8
    c_newton = np.mean(np.exp(np.einsum(
        "i,ijk->jk", 3*coefficients[:size]+2*coefficients[size:2*size], even[0], optimize=False
    )))
    newton_predicted = normal.get("predicted_newton_shift")
    if newton_predicted is None:
        newton_predicted = eps**4*float(sp.Rational(
            normal["normalized_AdS_Newton_coefficient_shift_at_epsilon_fourth"]
        ))
        assert abs(c_newton-1-newton_predicted) < abs(newton_predicted)/30, (
            d, float(c_newton-1), float(newton_predicted), float(coefficients[odd_start]), float(eps)
        )
    return {
        "cutoff": order,
        "collocation_grid": grid,
        "lambda": float(lam),
        "leading_mode_amplitude": round(float(coefficients[odd_start]), 12),
        "normalized_AdS_Newton_coefficient_minus_one": float("%.8g" % (c_newton-1)),
        "predicted_leading_shift_at_same_lambda": float("%.8g" % newton_predicted),
        "max_residual_components_A_B_c_v_and_tracefree": [float("%.4g" % x)
                                                         for x in equations(coefficients, False)],
    }


def certificate():
    normal = even_backreaction()
    low, high = numerical_branch(4, 32, normal), numerical_branch(7, 48, normal)
    assert abs(high["leading_mode_amplitude"]-low["leading_mode_amplitude"]) < 1e-7
    assert max(high["max_residual_components_A_B_c_v_and_tracefree"]) < 1e-7
    return {"normal_form": normal, "quantized_flux_ratios_N0_N1_N2": [17, 8, 8],
            "numerical_controls": [low, high]}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2))
