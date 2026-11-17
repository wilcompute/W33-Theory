"""Interval sixth-order normal form at the two square-branch reversal ratios."""

import json
from itertools import product

import sympy as sp
from mpmath import iv

from toe_20261117_11D_square_modulated_branch import numerical_branch
from toe_20261117_11D_unequal_square_branch import normal_form


def rational(value):
    value = sp.Rational(value)
    return iv.mpf(int(value.p))/int(value.q)


def evaluate(expression, values):
    if expression.is_Rational:
        return rational(expression)
    if expression.is_Symbol:
        return values[expression]
    if expression.is_Add:
        return sum(evaluate(a, values) for a in expression.args)
    if expression.is_Mul:
        value = iv.mpf(1)
        for a in expression.args:
            value *= evaluate(a, values)
        return value
    if expression.is_Pow and expression.exp.is_Integer:
        return evaluate(expression.base, values)**int(expression.exp)
    raise ValueError(expression)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b, strict=True))


def wave(m, n, x, y):
    return iv.matrix([
        iv.cos(m*x)*iv.cos(n*y),
        -m*iv.sin(m*x)*iv.cos(n*y),
        -n*iv.cos(m*x)*iv.sin(n*y),
    ])


def square_wave(m, n, x, y):
    first = wave(m, n, x, y)
    return first if m == n else first+wave(n, m, x, y)


def interval_solve(matrix, rhs):
    dimension = len(rhs)
    a = [[matrix[i, j] for j in range(dimension)]+[rhs[i]]
         for i in range(dimension)]
    for col in range(dimension):
        pivot = next(i for i in range(col, dimension) if a[i][col] > 0 or a[i][col] < 0)
        a[col], a[pivot] = a[pivot], a[col]
        for row in range(col+1, dimension):
            scale = a[row][col]/a[col][col]
            for j in range(col+1, dimension+1):
                a[row][j] -= scale*a[col][j]
    solution = [iv.mpf(0)]*dimension
    for i in reversed(range(dimension)):
        solution[i] = (a[i][-1]-sum(a[i][j]*solution[j] for j in range(i+1, dimension)))/a[i][i]
    return solution


def sextic_at_root(lam, d, mode, responses, interval):
    left, right = interval
    # iv.mpf with two endpoints accepts scalar point intervals.
    mid = rational((left+right)/2)
    width = rational((right-left)/2)
    resonance = mid+iv.mpf([-1, 1])*width
    asymmetry = iv.sqrt((resonance**2+8*resonance-560)/80)
    values = {lam: resonance, d: asymmetry}
    w = iv.matrix([evaluate(v, values) for v in mode])
    q2 = {k: iv.matrix([evaluate(v, values) for v in response])
          for k, response in responses.items()}
    grad = iv.matrix([[20, 5, 0, 0], [5, 0, 0, 0],
                      [0, 0, rational("-36/5"), 0], [0, 0, 0, -4]])
    local = [(weight, iv.matrix(v)) for weight, v
             in ((-20, (3, 2, 0, 0)), (12+4*asymmetry, (5, 2, rational("-18/5"), -2)),
                 (12-4*asymmetry, (5, 2, rational("-18/5"), 2)),
                 (-8, (5, 2, rational("-48/5"), 0)))]
    flux = [(2*(1+sign*asymmetry), iv.matrix([-5, 2, rational("12/5"), 4*sign]))
            for sign in (1, -1)]
    flux_e2 = [(weight, v, dot(v, q2[0])+dot(v, w)**2/2) for weight, v in flux]
    gradient_w = grad*w
    harmonics = ((1, 0, 1), (3, 0, 1), (2, 1, rational("1/2")))
    forcing = [iv.zeros(4, 1) for _ in harmonics]
    direct = iv.mpf(0)
    flux_e4 = [iv.mpf(0), iv.mpf(0)]
    # The order-six integrands have Fourier degree at most six. The
    # uniform 12-point tensor rule computes their means exactly.
    axis = [2*iv.pi*i/12 for i in range(12)]
    for x, y in product(axis, repeat=2):
        c, cx, cy = square_wave(1, 0, x, y)
        p20, p20x, p20y = square_wave(2, 0, x, y)
        p11, p11x, p11y = square_wave(1, 1, x, y)
        profile = q2[0]+p20*q2[4]+p11*q2[2]
        px, py = p20x*q2[4]+p11x*q2[2], p20y*q2[4]+p11y*q2[2]
        qwarp = profile[0]
        n2 = (cx*cx+cy*cy)*dot(w, gradient_w)
        n3 = 2*dot(gradient_w, cx*px+cy*py)
        n4 = dot(px, grad*px)+dot(py, grad*py)
        direct += resonance*(5*qwarp*n4+25*qwarp**2*n2/2)
        local_force = iv.zeros(4, 1)
        for weight, v in local:
            l, q = dot(v, w)*c, dot(v, profile)
            direct += weight*(q**3/6+l*l*q*q/4+l**4*q/24+l**6/720)
            local_force += weight*(l*q+l**3/6)*v
        for index, (weight, v, e2) in enumerate(flux_e2):
            l, q = dot(v, w)*c, dot(v, profile)
            direct += weight*(q**3/6+l*l*q*q/4+l**4*q/24+l**6/720)
            flux_e4[index] += q*q/2+l*l*q/2+l**4/24
            local_force += weight*(l*q+l**3/6-2*e2*l)*v
        for index, (m, n, _) in enumerate(harmonics):
            p, dx, dy = square_wave(m, n, x, y)
            forcing[index] += p*local_force+10*resonance*qwarp*(cx*dx+cy*dy)*gradient_w
            forcing[index][0] += 5*resonance*p*n3
    direct /= 144
    for index, (weight, _, e2) in enumerate(flux_e2):
        direct += weight*(-2*e2*flux_e4[index]/144+e2**3)
    c6 = direct
    response_rows = []
    for index, (m, n, norm) in enumerate(harmonics):
        force = forcing[index]/144
        mass = 2*resonance*(m*m+n*n)*grad
        for weight, v in local+flux:
            mass += weight*v*v.T
        if index == 0:
            # Fix the amplitude by setting the v component of q3_10
            # to zero. At the root the omitted force is solvable.
            complement = iv.matrix([[mass[i, j] for j in range(3)] for i in range(3)])
            complement_force = iv.matrix([force[i] for i in range(3)])
        else:
            complement, complement_force = mass, force
        response = interval_solve(norm*complement, -complement_force)
        c6 += dot(complement_force, response)/2
        response_rows.append([str(a) for a in response])
    kinetic = dot(w, grad*w)
    detuning = -3*c6/kinetic
    return {"isolating_lambda_interval": list(map(str, interval)),
            "critical_abs_asymmetry_interval": str(asymmetry),
            "unrelaxed_sextic_interval": str(direct),
            "relaxed_sextic_interval": str(c6),
            "lambda_shift_per_epsilon_fourth_interval": str(detuning),
            "lambda_shift_per_epsilon_fourth_midpoint": float(detuning.mid),
            "third_order_relaxation_coordinates": response_rows,
            "detuning_sign": 1 if detuning > 0 else -1 if detuning < 0 else 0}


def quantized_two_solutions(lam, d, mode, quartic, responses, slope, critical_sextic):
    import numpy as np
    from scipy.optimize import brentq

    n0, n1, n2 = 6716, 3186, 2655
    eta = brentq(lambda e: n1*n1*(1-e)*(1+e)**2-n2*n2*e*(2-e)**2, 0, 1)
    imbalance = 2*eta-1
    critical = -4+4*np.sqrt(36+5*imbalance**2)
    area = 16*np.pi*n1/(n0*4*(2-eta)*np.sqrt(8*eta))
    reference = 4*np.pi*np.pi/area
    at = {lam: critical, d: imbalance}
    linear_slope = float(slope.subs(at))
    local_quartic = float(quartic.subs(at))
    local_sextic = critical_sextic*(-8*(critical+4)/(critical+28))/-3
    roots = np.roots([critical_sextic, linear_slope, critical-reference])
    assert all(np.isreal(roots)) and all(roots > 0)
    fold_seed = float(np.sqrt(-linear_slope/(2*critical_sextic)))
    q2 = [[float(responses[k][i].subs(at)) for k in (0, 4, 2)] for i in range(4)]
    found = []
    for index, amp2 in enumerate(sorted(roots)):
        initial = float(np.sqrt(amp2))
        bracket = ((initial*.65, fold_seed*.98) if index == 0
                   else (fold_seed*1.02, initial*1.25))
        normal = {"static_threshold": critical,
                  "lambda_shift_coefficient": linear_slope,
                  "starting_amplitude": initial,
                  "first_order_even_fields": [float(x) for x in mode[:3, :].subs(at)],
                  "even_backreaction_by_field": dict(enumerate(q2[:3])),
                  "second_order_v": q2[3],
                  "amplitude_bracket": bracket,
                  "predicted_newton_shift": float(
                      (local_quartic*amp2**2+2*local_sextic*amp2**3)/8
                  )}
        result = numerical_branch(7, 48, normal, asymmetry=imbalance, reference_lambda=reference)
        assert max(result["max_residual_components_A_B_c_v_and_tracefree"]) < 1e-7
        found.append(result)
    assert found[1]["leading_mode_amplitude"]-found[0]["leading_mode_amplitude"] > .005
    return {"periods_N0_N1_N2": [n0, n1, n2], "flux_asymmetry": imbalance,
            "static_lambda": critical, "detuning": reference-critical,
            "numerical_solutions": found}


def certificate():
    iv.dps = 40
    lam, d, mode, _, _, quartic, slope, responses = normal_form()
    numerator = sp.Poly(slope.as_numer_denom()[0], lam)
    intervals = [i for i, _ in numerator.intervals(eps=sp.Rational(1, 10**20))
                 if 20 <= i[0] <= i[1] <= 22]
    assert len(intervals) == 2
    cases = [sextic_at_root(lam, d, mode, responses, interval) for interval in intervals]
    assert all(case["detuning_sign"] == -1 for case in cases)
    check = quantized_two_solutions(
        lam, d, mode, quartic, responses, slope,
        cases[0]["lambda_shift_per_epsilon_fourth_midpoint"]
    )
    return {"critical_cases": cases, "fixed_integer_flux_two_solution_check": check}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2))
