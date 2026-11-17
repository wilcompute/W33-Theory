"""Exact resonant cubic for the sphere-singlet hexagonal AdS modulation."""

import json
from collections import Counter
from itertools import product

import sympy as sp

from toe_20261117_11D_square_branch_BF_shift import certificate as square_BF_certificate


def fourier_moment(power):
    waves = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1))
    coefficients = Counter({(0, 0): sp.S.One})
    for _ in range(power):
        updated = Counter()
        for (a, b), coefficient in coefficients.items():
            for x, y in waves:
                updated[a+x, b+y] += coefficient/2
        coefficients = updated
    return coefficients[0, 0]


def equal_flux_quartic():
    lam = sp.Integer(20)
    w = sp.Matrix([0, 0, 0, 1])
    g = sp.Matrix([[20, 5, 0, 0], [5, 0, 0, 0],
                   [0, 0, -sp.Rational(36, 5), 0], [0, 0, 0, -4]])
    local = [(n, sp.Matrix(e)) for n, e in (
        (-20, (3, 2, 0, 0)), (12, (5, 2, -sp.Rational(18, 5), -2)),
        (12, (5, 2, -sp.Rational(18, 5), 2)), (-8, (5, 2, -sp.Rational(48, 5), 0)))]
    flux = [(2, sp.Matrix([-5, 2, sp.Rational(12, 5), sign*4])) for sign in (-1, 1)]
    m2, m4 = fourier_moment(2), fourier_moment(4)
    direct = sum(n*e.dot(w)**4 for n, e in local)*m4/24
    direct += sum(n*e.dot(w)**4 for n, e in flux)*(m4/24-m2*m2/4)
    relaxed = direct
    for norm2, coefficient in ((0, m2), (1, 1), (3, 1), (4, sp.Rational(1, 2))):
        norm = 1 if norm2 == 0 else m2
        overlap = norm*coefficient
        source = sum((n*e*e.dot(w)**2*overlap/2 for n, e in local+flux), sp.zeros(4, 1))
        source += 5*lam*(1-sp.Rational(norm2, 2))*w.dot(g*w)*overlap*sp.eye(4)[:, 0]
        if norm2 == 0:
            source -= sum((n*e*e.dot(w)**2*m2 for n, e in flux), sp.zeros(4, 1))
        assert source[3] == 0
        h = sum((n*e*e.T for n, e in local), sp.zeros(4))
        h += sum(((1 if norm2 else -1)*n*e*e.T for n, e in flux), sp.zeros(4))
        h += 2*lam*norm2*g
        complement = h[:3, :3]
        relaxed -= (source[:3, :].T*complement.inv()*source[:3, :])[0]/(2*norm)
    assert direct == -246
    assert relaxed == sp.Rational(5923, 9)
    return {"fourth_shell_moment": str(m4), "frozen_quartic": str(direct),
            "relaxed_quartic": str(relaxed),
            "lambda_shift_per_epsilon_squared": str(relaxed/3),
            "small_imbalance_linear_term_d_times_epsilon": 59,
            "predicted_fold_detuning_per_d_squared": str(-59**2/(4*(relaxed/3)))}


def certificate():
    lam, d = sp.symbols("Lambda d", real=True)
    mode = sp.Matrix([0, 16*d*(lam+32)/(lam*(lam+28)),
                      20*d/(3*(lam+28)), 1])
    local = [(weight, sp.Matrix(vector)) for weight, vector in (
        (-20, (3, 2, 0, 0)),
        (12+4*d, (5, 2, -sp.Rational(18, 5), -2)),
        (12-4*d, (5, 2, -sp.Rational(18, 5), 2)),
        (-8, (5, 2, -sp.Rational(48, 5), 0)),
    )]
    flux = [(2*(1+sign*d), sp.Matrix([-5, 2, sp.Rational(12, 5), 4*sign]))
            for sign in (1, -1)]
    g = sp.Matrix([[20, 5, 0, 0], [5, 0, 0, 0],
                   [0, 0, -sp.Rational(36, 5), 0], [0, 0, 0, -4]])
    relation = (lam**2+8*lam-560)/80

    def reduce(expression):
        numerator, denominator = sp.fraction(sp.factor(expression))
        assert not denominator.has(d)
        polynomial = sp.Poly(sp.expand(numerator), d)
        return sp.factor(sum(coefficient*d**(power % 2)*relation**(power//2)
                             for (power,), coefficient in polynomial.terms())/denominator)

    assert [fourier_moment(i) for i in (1, 2, 3)] == [0, sp.Rational(3, 2), sp.Rational(3, 2)]
    # The fixed-period inverse averages have a positive cubic sign when
    # the first harmonic has mean zero. The warp-gradient cubic vanishes
    # because the static kernel has A=0.
    cubic = reduce(sum(weight*vector.dot(mode)**3 for weight, vector in local+flux)/4)
    quadratic = reduce(sp.Rational(3, 2)*mode.dot(g*mode))
    slope = sp.factor(-3*cubic/(2*quadratic))
    assert sp.simplify(quadratic+12*(lam+4)/(lam+28)) == 0
    assert slope.subs(d, 0) == 0
    assert (slope/d).subs(lam, 20) == 59
    assert sp.Poly((lam**2+54*lam-64).subs(lam, sp.Symbol("t")+20), sp.Symbol("t")).all_coeffs() == [1, 94, 1416]
    return {"shell_field": "cos(x)+cos(y)+cos(x+y)",
            "moments_2_3": [str(fourier_moment(i)) for i in (2, 3)],
            "cubic_coefficient": str(cubic), "detuning_quadratic_coefficient": str(quadratic),
            "lambda_shift_per_signed_amplitude": str(slope),
            "kernel_fields_A_B_c_v": list(map(str, mode)),
            "equal_flux_limit": equal_flux_quartic(),
            "equal_flux_BF_mass_shift_per_epsilon_squared": str(
                fourier_moment(2)*sp.Rational(square_BF_certificate()[
                    "coefficient_of_epsilon_squared_in_m2_L2_plus_4"
                ])
            ),
            "equal_flux_numeric_control": convergence_check((68, 37, 37), slope, lam, d),
            "quantized_numeric_checks": [convergence_check(periods, slope, lam, d)
                                         for periods in ((127, 68, 51), (262, 140, 105))]}


def numerical_check(periods, slope, symbolic_lambda, symbolic_d, cutoff, grid):
    import numpy as np
    from scipy.optimize import root

    n0, n1, n2 = periods
    assert n1 == n2 or n1*3 == n2*4
    d = 0 if n1 == n2 else .6
    eta = (1+d)/2
    critical = -4+4*np.sqrt(36+5*d*d)
    area = 16*np.pi*n1/(n0*4*(2-eta)*np.sqrt(8*eta))
    lam = 8*np.pi*np.pi/(np.sqrt(3)*area)
    first_slope = float(slope.subs({symbolic_lambda: critical, symbolic_d: d}))
    eps = ((lam-critical)/first_slope if d else
           np.sqrt((lam-critical)/float(sp.Rational(5923, 27))))
    axis = 2*np.pi*np.arange(grid)/grid
    x, y = np.meshgrid(axis, axis, indexing="ij")

    def orbit(n, m):
        axes = set()
        for _ in range(6):
            axes.add(min((n, m), (-n, -m)))
            n, m = n-m, n
        return tuple(sorted(axes))

    orbits = sorted({orbit(n, m) for n, m in product(range(-cutoff, cutoff+1), repeat=2)
                     if n*n+m*m-n*m <= cutoff*cutoff},
                    key=lambda o: (o[0][0]**2+o[0][1]**2-o[0][0]*o[0][1], o))
    values = []
    for o in orbits:
        components = np.zeros((6, grid, grid))
        for n, m in o:
            phase = n*x+m*y
            co, si = np.cos(phase), np.sin(phase)
            components += np.array([co, -n*si, -m*si, -n*n*co, -m*m*co, -n*m*co])
        values.append(components)
    basis = np.moveaxis(np.array(values), 1, 0)
    norms = np.mean(basis[0]**2, axis=(1, 2))
    size = len(orbits)
    shell = orbits.index(orbit(1, 0))

    def inner(ax, ay, bx, by):
        return ax*bx+ay*by-(ax*by+ay*bx)/2

    def equations(coefficients, unprojected=False):
        fields = [np.einsum("i,dijk->djk", c, basis) for c in coefficients.reshape(4, size)]
        (a, ax, ay, axx, ayy, axy), (b, bx, by, bxx, byy, _), (
            c, cx, cy, cxx, cyy, cxy
        ), (v, vx, vy, vxx, vyy, vxy) = fields
        aa = inner(ax, ay, ax, ay)
        ab = inner(ax, ay, bx, by)
        da, db = axx+ayy-axy, bxx+byy-fields[1][5]
        dc, dv = cxx+cyy-cxy, vxx+vyy-vxy
        kinetic = 20*aa+10*ab-36*inner(cx, cy, cx, cy)/5-4*inner(vx, vy, vx, vy)
        reg, vol, war = np.exp(3*a+2*b), np.exp(5*a+2*b), np.exp(5*a)
        sp1 = (12+4*d)*np.exp(-18*c/5-2*v)
        sp2 = (12-4*d)*np.exp(-18*c/5+2*v)
        hor = 8*np.exp(-48*c/5)
        potential = -sp1-sp2+hor
        pc, pv = (18*(sp1+sp2)-48*hor)/5, 2*(sp1-sp2)
        xp, xm = np.exp(-5*a+2*b+12*c/5+4*v), np.exp(-5*a+2*b+12*c/5-4*v)
        ep, em = 2*(1+d)*xp/np.mean(xp)**2, 2*(1-d)*xm/np.mean(xm)**2
        eqs = [
            -60*reg-5*vol*potential-5*(ep+em)+lam*war*(5*kinetic-40*da-10*db-200*aa-50*ab),
            -40*reg-2*vol*potential+2*(ep+em)-10*lam*war*(da+5*aa),
            -vol*pc+12*(ep+em)/5+72*lam*war*(dc+5*inner(ax, ay, cx, cy))/5,
            -vol*pv+4*(ep-em)+8*lam*war*(dv+5*inner(ax, ay, vx, vy)),
        ]
        if unprojected:
            # Covariant trace-free tensor in the nonorthogonal lattice
            # coordinates, with q_ab proportional to [[1,1/2],[1/2,1]].
            tx = -5*(axx-2*ax*bx+inner(ax, ay, bx, by)*4/3+ax*ax)-36*cx*cx/5-4*vx*vx
            ty = -5*(ayy-2*ay*by+inner(ax, ay, bx, by)*4/3+ay*ay)-36*cy*cy/5-4*vy*vy
            txy = -5*(axy-bx*ay-by*ax+inner(ax, ay, bx, by)*2/3+ax*ay)-36*cx*cy/5-4*vx*vy
            trace = tx+ty-txy
            eqs += [tx-trace*2/3, ty-trace*2/3, txy-trace/3]
            return [float(np.max(np.abs(eq))) for eq in eqs]
        return np.concatenate([np.mean(eq*basis[0], axis=(1, 2))/norms for eq in eqs])

    start = np.zeros((4, size))
    start[:, shell] = eps*np.array([0, 16*d*(critical+32)/(critical*(critical+28)),
                                   20*d/(3*(critical+28)), 1])
    solved = root(equations, start.ravel(), tol=1e-10)
    amplitude = solved.x.reshape(4, size)[3, shell]
    residuals = equations(solved.x, True)
    assert abs(amplitude-eps) < abs(eps)/10
    if d == 0:
        assert abs((lam-critical)/amplitude**2-float(sp.Rational(5923, 27))) < .1
    assert max(residuals) < 1e-7, (amplitude, eps, residuals)
    return {"periods": list(periods), "asymmetry": d, "static_threshold": critical,
            "lambda": lam, "cutoff": cutoff, "grid": grid,
            "signed_amplitude": float(amplitude),
            "equation_and_tracefree_residuals": residuals}


def convergence_check(periods, slope, symbolic_lambda, symbolic_d):
    low = numerical_check(periods, slope, symbolic_lambda, symbolic_d, 4, 30)
    high = numerical_check(periods, slope, symbolic_lambda, symbolic_d, 6, 42)
    assert abs(low["signed_amplitude"]-high["signed_amplitude"]) < 1e-9
    return {"coarse": low, "fine": high}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2))
