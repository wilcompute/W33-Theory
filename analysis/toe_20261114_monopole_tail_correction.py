"""First-order infinite-radius correction to the projected monopole reflection."""

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.linalg import expm
from scipy.special import exp1

import toe_20261113_monopole_far_tail as far

tail = far.tail
line = far.line
OUT = tail.OUT.with_name("toe_20261114_monopole_tail_correction.json")


def linear_response(reflection, generator_integral):
    size = len(reflection)
    return (np.hstack((np.eye(size), -reflection)) @ generator_integral
            @ np.vstack((reflection, np.eye(size))))


def exponential_integral(generators, rates, outer, endpoint, energy):
    """Linear Yukawa interaction integral in the phase frame based at endpoint."""
    velocities = np.array([1]*4 + [-1]*4)
    frequency = energy * (velocities[None, :] - velocities[:, None])
    integral = np.zeros((8, 8), dtype=complex)
    for generator, mass in zip(generators, rates, strict=True):
        argument = endpoint * (mass - 1j * frequency)
        integral += generator * np.exp(mass * outer - 1j*frequency*endpoint) * exp1(argument)
    return integral



def check_exponential_integral():
    endpoint, outer, rate, energy = 4608., 9., .001511, .002
    generator = np.zeros((8, 8), dtype=complex)
    generator[0, 4] = 1
    exact = exponential_integral([generator], [rate], outer, endpoint, energy)[0, 4]
    def integrand(offset):
        return np.exp(-rate*(endpoint+offset-outer)-2j*energy*offset)/(endpoint+offset)
    measured = complex(*(quad(f, 0., 50000., epsabs=1e-14)[0]
                         for f in (lambda s: integrand(s).real, lambda s: integrand(s).imag)))
    np.testing.assert_allclose(exact, measured, atol=1e-13, rtol=1e-10)


    rng = np.random.default_rng(20261114)
    hermitian = rng.normal(size=(8, 8)) + 1j*rng.normal(size=(8, 8))
    hermitian += hermitian.conj().T
    flow = -1j * np.diag([1]*4 + [-1]*4) @ hermitian
    reflection = np.diag(np.exp(1j * np.arange(4)))
    step = 1e-5

    def graph_at(time):
        graph = expm(time * flow) @ np.vstack((reflection, np.eye(4)))
        return np.linalg.solve(graph[4:].T, graph[:4].T).T

    np.testing.assert_allclose(linear_response(reflection, flow),
                               (graph_at(step) - graph_at(-step))/(2*step),
                               atol=1e-7, rtol=1e-7)

def derivatives(vacuum, directions, step):
    # Real perturbations preserve the native conjugate mass terms.
    count = 2*len(directions)
    grid = np.arange(1., count+2)
    displaced = [vacuum + sign * step * direction
                 for direction in directions for sign in (1, -1)]

    def profile(radius):
        return vacuum if radius < 1. else displaced[int(radius)-1]

    system = next(tail.threshold.prepare(1, sectors=("L",), outer_radius=1.,
                                         exterior_nodes=grid[1:], profile_override=profile))
    frame = np.column_stack((system[6], system[5]))
    projected = frame.conj().T @ system[-1][-count:] @ frame
    return (projected[::2] - projected[1::2]) / (2*step)


def calculate(outer, elements, cells):
    check_exponential_integral()
    solution = tail.solve_profile(outer, elements)
    _, vacuum, masses, modes, amplitudes, report = solution
    boundary, endpoint, final = 4*outer, 512*outer, 4096*outer
    nodes = np.r_[np.geomspace(boundary, endpoint, 7*cells+1),
                  np.geomspace(endpoint, final, 3*cells+1)[1:]]
    nodes[0], nodes[7*cells], nodes[-1] = boundary, endpoint, final
    system, _, _, _ = tail.prepare_tail(outer, elements, exterior_nodes=nodes[1:],
                                        solution=solution)
    _, grid, flux, _, _, incoming, outgoing, _, base = system
    frame = np.column_stack((outgoing, incoming))
    start = np.flatnonzero(grid == boundary)[0]
    projection = frame.conj().T @ base[start:] @ frame
    core = tail.split_transfers(tail.cut.truncate(system, boundary))
    energy = .002
    reflection = line.residues.matching(core, energy)
    at_cut = far.open_tail.extend(reflection, nodes[:7*cells+1], projection[:7*cells], energy)
    at_final = far.open_tail.extend(at_cut, nodes[7*cells:], projection[7*cells:], energy)
    # Remove the freely propagated common reflection phase.
    at_final *= np.exp(-2j * energy * (final-endpoint))
    change_in, change_out = line.flavors.flavor_frames()
    def conversion(reflection_matrix):
        return float(line.conversion(change_out.conj().T @ reflection_matrix @ change_in))

    positive = masses > 0
    # A mode contributes linearly with this exact radial profile coefficient.
    # High masses have numerically negligible E1 at the cutoff; skip them
    # in the diagnostics to avoid underflow and overlarge intermediate exp.
    keep = positive & (masses * endpoint < 220)
    rates = masses[keep]
    directions = np.column_stack((np.zeros(len(rates)), modes[keep]))
    coarse = derivatives(vacuum, directions, 1e-3)
    fine = derivatives(vacuum, directions, .5e-3)
    first = (4*fine-coarse)/3
    weighted = first * (outer*amplitudes[keep])[:, None, None]
    integral = exponential_integral(weighted, rates, outer, endpoint, energy)
    correction = linear_response(at_cut, integral)
    unitary_cut = change_out.conj().T @ at_cut @ change_in
    rotated_correction = change_out.conj().T @ correction @ change_in
    probability_change = float(2*np.vdot(unitary_cut[:3, 3], rotated_correction[:3, 3]).real)
    absolute_linear_integral = float(sum(np.linalg.norm(g, ord=2)*np.exp(m*outer)*exp1(m*endpoint)
                                         for g, m in zip(weighted, rates, strict=True)))
    actual_change = conversion(at_final) - conversion(at_cut)
    error = float(np.linalg.norm(at_final-at_cut-correction, ord=2))
    rows = dict(energy=energy, cutoff=endpoint, finite_control_radius=final, cells_per_octave=cells,
                probability_at_cutoff=conversion(at_cut), probability_at_control=conversion(at_final),
                first_order_infinite_probability_change=probability_change,
                direct_finite_probability_change=actual_change,
                direct_minus_linear_matrix_norm=error,
                linear_generator_integral_norm=float(np.linalg.norm(integral, ord=2)),
                absolute_linear_generator_integral_upper_diagnostic=absolute_linear_integral,
                riccati_linear_generator_quadratic_error_diagnostic=4*absolute_linear_integral**2,
                smallest_included_mass=float(min(rates)), largest_included_mass=float(max(rates)),
                minimum_omitted_mass=float(min(masses[positive & ~keep])),
                projected_jacobian_refinement_norm=float(np.linalg.norm(fine-coarse)),
                robin_profile=report)
    assert error < 1e-8
    assert abs(actual_change - probability_change) < 2e-9
    print({k: v for k, v in rows.items() if k != "robin_profile"}, flush=True)
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cells-per-octave", type=int, default=32)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    result = calculate(9., 120, args.cells_per_octave)
    args.output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
