"""Propagate a variational monopole with its light scalar exterior."""

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.interpolate import CubicSpline

import toe_20261113_monopole_triplet_cut as cut


line = cut.line
threshold = line.residues.poles.threshold
OUT = line.OUT.with_name("toe_20261113_monopole_triplet_tail.json")


def solve_profile(outer, elements):
    core = threshold.triplet.neutral
    vacuum, _, _, residual, generators = core.model()
    stored = json.loads(threshold.triplet.flat.ROOT.joinpath(
        "data/toe_20261113_monopole_adjoint_shooting_mesh.json").read_text(encoding="utf-8"))[-1]
    directions = np.eye(len(vacuum))[1:]
    jacobian = np.column_stack([
        residual(vacuum[None] + 1e-24j*direction)[0].imag/1e-24 for direction in directions
    ])
    _, masses, right = np.linalg.svd(jacobian, full_matrices=False)
    masses[masses < 1e-8] = 0.
    assert np.count_nonzero(masses == 0) == 4
    endpoints = np.r_[0., np.geomspace(1e-4, outer, elements)]
    grid = np.empty(2*elements+1)
    grid[::2] = endpoints
    grid[1::2] = (endpoints[1:]+endpoints[:-1])/2
    initial = CubicSpline(stored["grid"], stored["state"])(np.minimum(grid, 5.))
    initial[0, :2] = [core.SQRT6, 0.]
    initial[-1, 0] = 0.
    boundary = np.sqrt(outer+outer**2*masses)[:, None]*right
    state, report = core.minimize(residual, grid, initial, (vacuum[1:], boundary))
    print("profile", outer, report, flush=True)
    amplitudes = right @ (state[-1, 1:]-vacuum[1:])
    spline = CubicSpline(grid, state)
    tangent = generators(vacuum[None])[0, :, 1:].T
    tangent, _ = np.linalg.qr(tangent)
    gauge_amplitude = float(np.linalg.norm(tangent.T @ (state[-1, 1:]-vacuum[1:])))
    report.update(outer_radius=outer, boundary_scalar_deviation=float(np.linalg.norm(amplitudes)),
                  boundary_linear_gauge_tangent=gauge_amplitude)
    return spline, vacuum, masses, right, amplitudes, report


def split_transfers(system, maximum_step=.06):
    label, grid, *frames, base = system
    pieces = np.maximum(1, np.ceil(np.diff(grid)/maximum_step).astype(int))
    refined = np.r_[grid[0], np.concatenate([
        np.linspace(a, b, count+1)[1:] for a, b, count in zip(grid[:-1], grid[1:], pieces)
    ])]
    return label, refined, *frames, np.repeat(base, pieces, axis=0)


def calculate(outer, elements):
    spline, vacuum, masses, right, amplitudes, report = solve_profile(outer, elements)

    def profile(radius):
        if radius <= outer:
            return spline(radius)
        state = vacuum.copy()
        state[1:] += (amplitudes*(outer/radius)*np.exp(-masses*(radius-outer))) @ right
        return state

    change_in, change_out = line.flavors.flavor_frames()
    pole_solver = line.residues.poles
    seed = complex(*json.loads(line.flavors.OUT.read_text(encoding="utf-8"))["poles"]["positive"]["energy"])
    system = next(threshold.prepare(48, sectors=("L",), profile_override=profile,
                                    outer_radius=4*outer))
    rows = []
    for requested in sorted({5., outer, 2*outer, 4*outer}):
        finite = cut.truncate(system, requested)
        radius = float(finite[1][-1])
        finite = split_transfers(finite)
        center, pole = pole_solver.pole(finite, seed, cut=radius)
        conversion = []
        for energy in cut.ENERGIES:
            reflection = change_out.conj().T @ line.residues.matching(finite, energy) @ change_in
            assert np.linalg.norm(reflection.conj().T @ reflection-np.eye(4)) < 1e-8
            conversion.append(dict(energy=energy, total=float(line.conversion(reflection))))
        rows.append(dict(radius=radius, pole=pole, samples=conversion,
                         minimum=min(conversion, key=lambda row: row["total"]),
                         background_deviation=float(np.linalg.norm(profile(radius)-vacuum))))
        print("cut", radius, center, rows[-1]["minimum"], flush=True)
        seed = center
    threshold_mass = float(min(system[-2]))
    return dict(status="PASS", profile=report, cuts=rows,
                lowest_exterior_fermion_mass=threshold_mass,
                final_pole_over_threshold=[x/threshold_mass for x in rows[-1]["pole"]["energy"]])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outer", type=float, default=9.)
    parser.add_argument("--elements", type=int, default=120)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    args.output.write_text(json.dumps(calculate(args.outer, args.elements), indent=2)+"\n",
                           encoding="utf-8")
