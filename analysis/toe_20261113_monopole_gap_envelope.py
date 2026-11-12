"""Bound the outgoing monopole boundary problem over a continuous coefficient hull."""

import argparse
import json
from math import comb, factorial
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.interpolate import CubicSpline
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import splu

import toe_20261113_monopole_phase_loop_shooting as loop


shooting = loop.shooting
OUT = shooting.phase.ROOT / 'data/toe_20261113_monopole_gap_envelope.json'
HOLDOUT = shooting.phase.ROOT / 'data/toe_20261113_monopole_gap_holdout.json'
DIMENSION = 8
ANGULAR = -1j * shooting.FLUX @ shooting.GAUGE
INNER = 5e-5
EPS = np.finfo(float).eps
PAD = 1e-10


def modulus(value):
    return np.abs(value.real) + np.abs(value.imag)


def induced(matrix):
    return np.max(np.sum(modulus(matrix), axis=-1), axis=-1)


def mass_generator(coeff):
    masses = np.zeros(coeff.shape[:-1] + (2, 2), dtype=complex)
    masses[..., 0, 0] = coeff[..., 0]
    masses[..., 0, 1] = coeff[..., 1]
    masses[..., 1, 0] = coeff[..., 2]
    average = (masses[..., 0, :, :] + masses[..., 1, :, :]) / 2
    difference = (masses[..., 1, :, :] - masses[..., 0, :, :]) / 2
    m = np.concatenate((np.concatenate((average, difference), axis=-1),
                        np.concatenate((difference, average), axis=-1)), axis=-2)
    v = np.zeros(m.shape[:-2] + (DIMENSION, DIMENSION), dtype=complex)
    v[..., 4:, :4] = m
    v[..., :4, 4:] = m.conj().swapaxes(-1, -2)
    return -1j * shooting.FLUX @ v


def outgoing_boundary(exterior):
    """Exact row constraints for the growing heavy and incoming light subspaces."""
    generator = 2*mass_generator(exterior)
    assert np.all(generator == np.rint(generator.real) + 1j*np.rint(generator.imag))
    exact = sp.Matrix([[int(z.real) + sp.I*int(z.imag) for z in row] for row in generator])/2
    assert exact.H == exact
    spectrum = list(exact.eigenvals())
    identity = sp.eye(DIMENSION)
    project = sp.zeros(DIMENSION)
    for eigenvalue in spectrum:
        if eigenvalue > 0:
            factor = identity
            for other in spectrum:
                if other != eigenvalue:
                    factor = factor * (exact-other*identity)/(eigenvalue-other)
            project += factor
    incoming = sp.Matrix([0, 0, 0, 0, 0, 1, 0, -1])
    assert exact * incoming == sp.zeros(DIMENSION, 1)
    project += incoming * incoming.T / 2
    assert project*project == project and project.H == project
    rows = project.T.rref()[1]
    assert len(rows) == 4
    boundary = project[list(rows), :]
    for z in boundary:
        for component in (sp.re(z), sp.im(z)):
            denominator = int(component.q)
            assert denominator & (denominator-1) == 0
            assert abs(int(component.p)) < 2**52
    return np.array(boundary, dtype=complex)


def centered_coefficients(knots, coefficients, left, right):
    """Power coefficients in t=(r-midpoint)/halfwidth and their arithmetic majorants."""
    half = (right-left)/2
    intervals = np.searchsorted(knots, left, side='right')-1
    assert np.all(left >= knots[intervals]) and np.all(right <= knots[intervals+1])
    shape = (-1,) + (1,)*(coefficients.ndim-2)
    offset = (left-knots[intervals]+half).reshape(shape)
    half = half.reshape(shape)
    c = coefficients[::-1, intervals]
    powers, majorants = [], []
    for j in range(4):
        terms = [comb(k, j) * c[k] * offset**(k-j) * half**j for k in range(j, 4)]
        powers.append(sum(terms))
        majorants.append(sum(modulus(term) for term in terms))
    return np.array(powers), np.array(majorants)


def radial_cells(knots):
    # The inner region uses log(r); outside it, the radial step is capped.
    nodes = np.unique(np.r_[INNER, .12, knots[knots >= INNER]])
    pieces = [np.linspace(a, b, max(1, int(np.ceil((b-a)/.012)))+1)[:-1]
              for a, b in zip(nodes[:-1], nodes[1:])]
    return np.r_[np.concatenate(pieces), nodes[-1]]


def numerator(k_spline, mass_knots, coefficients, left, right):
    """Polynomial coefficients of r times the generator on each radial cell."""
    k, k_major = centered_coefficients(k_spline.x, k_spline.c, left, right)
    mass, mass_major = centered_coefficients(mass_knots, coefficients, left, right)
    middle = ((left+right)/2)[None, :, None, None]
    half = ((right-left)/2)[None, :, None, None]
    result = np.zeros((5, len(left), DIMENSION, DIMENSION), dtype=complex)
    result[:4] = middle * mass + k[..., None, None] * ANGULAR
    result[1:] += half * mass
    bound = np.zeros(result.shape, dtype=float)
    bound[:4] = middle*mass_major + k_major[..., None, None]*modulus(ANGULAR)
    bound[1:] += half*mass_major
    return result, induced(bound.sum(axis=0))


def interval_scales(nodes):
    left, right = nodes[:-1], nodes[1:]
    middle = (left+right)/2
    logarithmic = right <= .12
    width = right-left
    # atanh series with a positive, geometrically bounded remainder.
    ratio = width/(right+left)
    log_width = 2*sum(ratio**(2*k+1)/(2*k+1) for k in range(9))
    log_remainder = 2*ratio**19/(19*(1-ratio**2))
    scale = np.where(logarithmic, log_width, width/middle)
    bound_scale = np.where(logarithmic, log_width+log_remainder, width/left)
    assert np.max(ratio[logarithmic]) < .04
    return scale, bound_scale, logarithmic, log_remainder


def constant_approximation(profile, nodes):
    left, right = nodes[:-1], nodes[1:]
    middle, half = (left+right)/2, (right-left)/2
    scale, bound_scale, logarithmic, log_remainder = interval_scales(nodes)
    reference, major = numerator(*profile, left, right)
    midpoint = reference[0].copy()
    center = scale[:, None, None]*midpoint
    reference[0] = 0
    reference[1, ~logarithmic] -= (half/middle)[~logarithmic, None, None] * midpoint[~logarithmic]
    error = bound_scale*induced(np.sum(modulus(reference), axis=0))
    error += np.where(logarithmic, log_remainder*induced(midpoint), 0.)
    return center, error+PAD*(1+bound_scale*major)


def enclose_intervals(profiles, nominal, nodes, origin_knots, extra):
    left, right = nodes[:-1], nodes[1:]
    _, bound_scale, _, _ = interval_scales(nodes)
    reference, reference_major = numerator(*nominal, left, right)
    magnitude = bound_scale*induced(np.sum(modulus(reference), axis=0))
    magnitude += PAD*(1+bound_scale*reference_major)
    delta = np.zeros(len(left))
    origin_bound = 0.
    for k, knots, mass in profiles:
        power, major = numerator(k, knots, mass, left, right)
        error = bound_scale * induced(np.sum(modulus(power-reference), axis=0))
        # Deliberately loose allowance for the short polynomial translations,
        # complex arithmetic, norm evaluation and the logarithm series.
        error += PAD*(1+bound_scale*(major+reference_major))
        delta = np.maximum(delta, error)
        mass_power, mass_major = centered_coefficients(knots, mass, origin_knots[:-1], origin_knots[1:])
        origin_mass = np.max(induced(np.sum(modulus(mass_power), axis=0))
                             + PAD*(1+induced(np.sum(mass_major, axis=0))))
        k0 = k.c[:, 0]
        assert k0[-1] == 1 and k0[-2] == 0 and k.x[1] >= INNER
        angular_remainder = (abs(k0[0])*INNER+abs(k0[1]))*INNER
        origin_bound = max(origin_bound, origin_mass + angular_remainder + extra)
    # An optional pointwise allowance on the physical generator, over and above
    # the entire convex coefficient hull.
    delta += extra * np.where(right <= .12, bound_scale*right, right-left)
    return magnitude, delta*(1+PAD)+PAD, origin_bound*(1+PAD)+PAD


def exp_upper(magnitude):
    assert max(magnitude) < 1.4
    return (1-magnitude/4)**-4*(1+PAD)


def exponential(center):
    power = np.broadcast_to(np.eye(DIMENSION), center.shape).astype(complex).copy()
    result = power.copy()
    for degree in range(1, 17):
        power = (power @ center)/degree
        result += power
    magnitude = induced(center)*(1+PAD)+PAD
    # exp(x) <= 1/(1-x/4)^4 for 0 <= x < 4.
    exponent = exp_upper(magnitude)
    defect = exponent*magnitude**17/factorial(17) + PAD*(1+exponent)
    return result, defect


def transfers(nominal, nodes, magnitude):
    count = len(nodes)-1
    subdivisions = 32
    sub = np.linspace(nodes[:-1], nodes[1:], subdivisions+1, axis=1)
    refined = np.r_[sub[:, :-1].ravel(), nodes[-1]]
    center, approximation = constant_approximation(nominal, refined)
    polynomial, rounding = exponential(center)
    polynomial = polynomial.reshape(count, subdivisions, DIMENSION, DIMENSION)
    result = np.broadcast_to(np.eye(DIMENSION), (count, DIMENSION, DIMENSION)).copy()
    for j in range(subdivisions):
        result = polynomial[:, j] @ result
    total_error = (approximation+rounding).reshape(count, subdivisions).sum(axis=1)
    defect = exp_upper(magnitude+2*total_error) * (total_error+PAD)
    return result, exp_upper(magnitude), defect


def weighted_inverse(transfer, right, weights):
    count = len(transfer)
    total = DIMENSION*(count+1)
    row, column, data = [], [], []

    def append(r, c, values):
        rr, cc = np.broadcast_arrays(r, c)
        row.extend(rr.ravel())
        column.extend(cc.ravel())
        data.extend(values.ravel())

    append(np.arange(4), np.array([2, 3, 6, 7]), np.ones(4))
    index = np.arange(DIMENSION)
    for j, transition in enumerate(transfer):
        base = 4+DIMENSION*j
        append(base+index[:, None], DIMENSION*j+index[None, :], -transition)
        append(base+index, DIMENSION*(j+1)+index, np.ones(DIMENSION))
    append(total-4+np.arange(4)[:, None], total-DIMENSION+index[None, :], right)
    matrix = coo_matrix((data, (row, column)), shape=(total, total)).tocsc()
    matrix.eliminate_zeros()
    absolute = matrix.copy()
    absolute.data = modulus(absolute.data)
    absolute = absolute.real
    factor = splu(matrix)
    inverse_sum = np.zeros(total)
    residual_sum = np.zeros(total)
    for start in range(0, total, 64):
        columns = np.arange(start, min(start+64, total))
        rhs = np.zeros((total, len(columns)), dtype=complex)
        rhs[columns, np.arange(len(columns))] = weights[columns]
        inverse = factor.solve(rhs)
        error = modulus(matrix @ inverse-rhs)
        inverse_size = modulus(inverse)
        rounding = 256*EPS*(absolute @ inverse_size+modulus(rhs))
        inverse_sum += np.sum(inverse_size, axis=1)
        residual_sum += np.sum(error+rounding, axis=1)/weights
    inverse_norm = float(max(inverse_sum)*(1+PAD)+PAD)
    rho = float(max(residual_sum)*(1+PAD)+PAD)
    assert rho < 1
    return inverse_norm/(1-rho)*(1+PAD)+PAD, rho


def spline_profile(grid, state, scalar_data, roots):
    _, knots, matrices = scalar_data
    k = CubicSpline(grid, state[:, 0].real/shooting.phase.neutral.SQRT6,
                    bc_type=((1, 0.), 'not-a-knot'))
    mass = CubicSpline(knots, np.array([shooting.coefficients(a, roots) for a in matrices]))
    return k, knots, mass_generator(mass.c)


def distance_from_chord(candidate, endpoints, fraction, nodes, origin_knots):
    left, right = nodes[:-1], nodes[1:]
    middle, middle_major = numerator(*candidate, left, right)
    lower, lower_major = numerator(*endpoints[0], left, right)
    upper, upper_major = numerator(*endpoints[1], left, right)
    diff = middle-(1-fraction)*lower-fraction*upper
    error = PAD*(middle_major+lower_major+upper_major)
    bound = (induced(np.sum(modulus(diff), axis=0))+error)/left + PAD

    def origin_mass(profile):
        _, knots, mass = profile
        return centered_coefficients(knots, mass, origin_knots[:-1], origin_knots[1:])

    m, mm = origin_mass(candidate)
    a, ma = origin_mass(endpoints[0])
    b, mb = origin_mass(endpoints[1])
    origin_diff = m-(1-fraction)*a-fraction*b
    origin = max(induced(np.sum(modulus(origin_diff)+PAD*(mm+ma+mb), axis=0)))
    k, k0, k1 = (profile[0].c[:, 0] for profile in (candidate, *endpoints))
    assert all(c[-1] == 1 and c[-2] == 0 for c in (k, k0, k1))
    angular_diff = np.abs(k[:2]-(1-fraction)*k0[:2]-fraction*k1[:2])
    angular_diff += PAD*(np.abs(k[:2])+np.abs(k0[:2])+np.abs(k1[:2]))
    origin += INNER*(angular_diff[1]+INNER*angular_diff[0])+PAD
    return float(max(max(bound), origin)*(1+PAD)+PAD)


def check_holdout(path, allowance):
    branch = json.loads(loop.nonlinear.OUT.read_text(encoding='utf-8'))
    holdout = json.loads(path.read_text(encoding='utf-8'))
    assert branch['grid'] == holdout['grid']
    check, = holdout['profiles']
    assert check['scaled_discrete_residual'] < 3e-7
    angles = [row['angle'] for row in branch['profiles']]
    position = int(np.searchsorted(angles, check['angle']))
    assert 0 < position < len(angles)
    start, stop = branch['profiles'][position-1:position+1]
    assert start['angle'] < check['angle'] < stop['angle']
    fraction = (check['angle']-start['angle'])/(stop['angle']-start['angle'])
    grid = np.array(branch['grid'])
    embedding, sectors = loop.context()
    states = [loop.nonlinear.unpack(np.array(row['state']))[:, :8] for row in (check, start, stop)]
    scalar = [shooting.interpolate_scalar(grid, state, embedding) for state in states]
    knots = scalar[0][1]
    nodes = radial_cells(knots)
    origin_knots = knots[knots <= INNER]
    results = []
    for weight, roots, _ in sectors:
        candidate, lower, upper = [spline_profile(grid, state, data, roots)
                                    for state, data in zip(states, scalar)]
        bound = distance_from_chord(candidate, (lower, upper), fraction, nodes, origin_knots)
        assert bound <= allowance
        results.append(dict(weight=weight.tolist(), generator_distance_upper=bound))
    direct = loop.scatter(grid, check['state'], check['angle'], (embedding, sectors))
    return dict(angle=check['angle'], neighboring_angles=[start['angle'], stop['angle']],
                scaled_discrete_residual=check['scaled_discrete_residual'], sectors=results,
                direct_matching=direct['sectors'])


def calculate(extra):
    assert np.array_equal(ANGULAR, np.diag([1, 1, -1, -1, 1, 1, -1, -1]))
    probe = np.array([[2+3j, 4-5j, 3+2j], [4+2j, 5-3j, 1-1j]])
    np.testing.assert_array_equal(mass_generator(probe),
                                  -1j * shooting.FLUX @ shooting.potential(0., probe, 1., 1.))
    branch = json.loads(loop.nonlinear.OUT.read_text(encoding='utf-8'))
    reference = json.loads(loop.nonlinear.MESH.read_text(encoding='utf-8'))[0]
    grid = np.array(branch['grid'])
    assert reference['grid'] == branch['grid'] and grid[1] == INNER
    embedding, sectors = loop.context()
    fields = [np.array(reference['state'])[:, :8]]
    fields += [loop.nonlinear.unpack(np.array(row['state']))[:, :8] for row in branch['profiles']]
    scalar = [shooting.interpolate_scalar(grid, state, embedding) for state in fields]
    fine = scalar[0][1]
    origin_knots = fine[fine <= INNER]
    assert origin_knots[0] == 0 and origin_knots[-1] == INNER
    nodes = radial_cells(fine)
    rows = []
    for weight, roots, exterior in sectors:
        assert all(np.array_equal(data[1], fine) for data in scalar)
        profiles = [spline_profile(grid, state, data, roots) for state, data in zip(fields, scalar)]
        sign = np.r_[np.ones(4), -np.ones(4)]
        conjugate = sign[:, None]*sign[None, :]
        first, last = profiles[0], profiles[-1]
        average_mass = (first[2]+last[2])/2
        nominal_mass = (average_mass+conjugate*average_mass.conj())/2
        nominal_k = CubicSpline(grid, (fields[0][:, 0].real+fields[-1][:, 0].real)
                                /(2*shooting.phase.neutral.SQRT6), bc_type=((1, 0.), 'not-a-knot'))
        nominal = (nominal_k, fine, nominal_mass)
        magnitude, delta, origin = enclose_intervals(profiles+[nominal], nominal, nodes, origin_knots, extra)
        assert INNER*origin < 1
        beta = INNER*origin/(3*(1-INNER*origin))
        transfer, exponent, defect = transfers(nominal, nodes, magnitude)
        weights = np.r_[np.full(4, beta*(1+PAD)+PAD),
                        (exponent*delta+defect)*(1+PAD)+PAD, np.full(4, 1e-7)]
        weights = np.r_[weights[:4], np.repeat(weights[4:-4], DIMENSION), weights[-4:]]
        inverse, residual = weighted_inverse(transfer, outgoing_boundary(exterior), weights)
        total = (inverse + float(max(delta)))*(1+PAD)+PAD
        result = dict(weight=weight.tolist(), radial_intervals=len(nodes)-1,
                      origin_graph_bound=float(beta), max_local_generator_defect=float(max(delta)),
                      accumulated_generator_defect=float(sum(delta)),
                      accumulated_reference_transfer_defect=float(sum(defect)),
                      weighted_inverse_upper=inverse, inverse_residual_upper=residual,
                      contraction_upper=total)
        print(result, flush=True)
        assert total < 1
        rows.append(result)
    return dict(status='PASS', coefficient_profiles=len(fields), physical_generator_allowance=extra,
                pi_endpoint_conjugation_symmetrized=True,
                certified_interpolant_adjoint_winding=3, sectors=rows)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--allowance', type=float, default=.02)
    parser.add_argument('--output', type=Path, default=OUT)
    parser.add_argument('--holdout', type=Path, nargs='?', const=HOLDOUT)
    args = parser.parse_args()
    if args.allowance < 0:
        parser.error('the pointwise allowance must be nonnegative')
    data = calculate(args.allowance)
    if args.holdout:
        data['stationary_holdout'] = check_holdout(args.holdout, args.allowance)
    result = json.dumps(data, indent=2)+'\n'
    args.output.write_text(result, encoding='utf-8')
