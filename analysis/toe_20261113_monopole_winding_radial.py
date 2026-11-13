"""Flux-normalized threshold Weyl profiles in the W33 winding sectors."""

import json
from pathlib import Path

import numpy as np
from scipy.interpolate import CubicSpline
from scipy.linalg import expm, solve_triangular

import toe_20261113_monopole_yukawa_exchange as exchange


triplet = exchange.triplet
OUT = triplet.flat.ROOT / "data/toe_20261113_monopole_winding_radial.json"


def sector_frames(adjoint, weights, root, positive):
    def frame(weight):
        mask = (weights == weight).all(axis=1)
        chiral = triplet.normalize_chiral(triplet.directions(np.flatnonzero(mask), adjoint))
        roots = adjoint[mask[405:]]
        if len(roots):
            roots = triplet.normalize_rows(roots.reshape(-1, 729)).reshape(-1, 27, 27)
        return chiral, roots

    left, gl = frame(-np.array(positive))
    right, gr = frame(np.array(positive))
    return ((left, right, gl, gr),
            (triplet.chiral_action(-root, left), triplet.chiral_action(root.T, right),
             triplet.adjoint_action(-root, gl), triplet.adjoint_action(root.T, gr)))


def exterior_basis(evaluators, vacuum):
    masses = [sum(evaluate(*vacuum)) for evaluate in evaluators]
    flux, potential = triplet.radial_hamiltonian(*masses, 0.)
    generator = -1j*flux @ potential
    np.testing.assert_allclose(generator, generator.conj().T, atol=1e-11)
    values, basis = np.linalg.eigh(generator)
    stable = basis[:, values < -1e-8]
    zero = basis[:, abs(values) < 1e-8]
    velocities, rotation = np.linalg.eigh(zero.conj().T @ flux @ zero)
    np.testing.assert_allclose(abs(velocities), 1., atol=1e-11)
    modes = zero @ rotation
    incoming, outgoing = modes[:, velocities < 0], modes[:, velocities > 0]
    assert incoming.shape == outgoing.shape
    return flux, stable, incoming, outgoing, masses


def radial_match(grid, profile, embedding, evaluators, vacuum):
    flux, stable, incoming, outgoing, masses = exterior_basis(evaluators, vacuum)
    _, angular = triplet.radial_hamiltonian(*[np.zeros_like(m) for m in masses], 1.)
    origin = -1j*flux @ angular
    regular = np.eye(len(flux), dtype=complex)[:, origin.diagonal().real > 0]
    midpoint = (len(grid)-1)//2
    left_bases, left_r = [regular], []
    right_bases, right_r = {}, {}
    allowed = np.column_stack((stable, outgoing, incoming))
    right_bases[len(grid)-1] = allowed
    for j in range(len(grid)-1):
        i = j if j < midpoint else len(grid)-2+midpoint-j
        radius = (grid[i]+grid[i+1])/2
        a, matter = triplet.profile_fields(profile(radius), embedding)
        local = [sum(evaluate(a, matter)) for evaluate in evaluators]
        _, potential = triplet.radial_hamiltonian(*local, profile(radius)[0]/triplet.neutral.SQRT6/radius)
        delta = grid[i+1]-grid[i]
        generator = (-1j*flux @ potential)*delta
        if j < midpoint:
            regular, factor = np.linalg.qr(expm(generator) @ regular)
            left_bases.append(regular)
            left_r.append(factor)
        else:
            allowed, right_r[i] = np.linalg.qr(expm(-generator) @ allowed)
            right_bases[i] = allowed

    # Pull the fixed incoming amplitudes back to the matching radius.
    cols = incoming.shape[1]
    transport = np.eye(allowed.shape[1], dtype=complex)
    for i in range(len(grid)-2, midpoint-1, -1):
        # Only needed up to the block that preserves the incoming quotient.
        transport[-cols:, -cols:] = right_r[i][-cols:, -cols:] @ transport[-cols:, -cols:]
    forcing = allowed[:, -cols:] @ transport[-cols:, -cols:]
    matching = np.column_stack((regular, -allowed[:, :-cols]))
    amplitudes = np.linalg.solve(matching, forcing)
    left_coeff = amplitudes[:regular.shape[1]]
    right_coeff = np.vstack((amplitudes[regular.shape[1]:], transport[-cols:, -cols:]))
    states = {midpoint: regular @ left_coeff}
    for i in range(midpoint-1, -1, -1):
        left_coeff = solve_triangular(left_r[i], left_coeff)
        states[i] = left_bases[i] @ left_coeff
    for i in range(midpoint, len(grid)-1):
        right_coeff = solve_triangular(right_r[i], right_coeff)
        states[i+1] = right_bases[i+1] @ right_coeff
    reflection = right_coeff[-2*cols:-cols]
    np.testing.assert_allclose(right_coeff[-cols:], np.eye(cols), atol=1e-10)
    unitarity = np.linalg.norm(reflection.conj().T @ reflection-np.eye(cols))
    assert unitarity < 1e-6
    profile_values = np.array([states[i] for i in range(len(grid))])
    norm = np.linalg.norm(profile_values, axis=(1, 2))
    flux_error = np.max(np.abs(profile_values.conj().transpose(0, 2, 1) @ flux @ profile_values))
    assert flux_error < 1e-6
    return dict(light_channels=cols, heavy_channels=stable.shape[1],
                matching_sigma_min=float(np.linalg.svd(matching, compute_uv=False)[-1]),
                reflection_unitarity_error=float(unitarity), standing_flux_error=float(flux_error),
                radial_norm_samples=np.interp([.01, .03, .06, .1, .2, .4, 1., 3., 5.], grid, norm).tolist(),
                reflection_real=reflection.real.tolist(), reflection_imag=reflection.imag.tolist())


def calculate():
    model = exchange.radial.mixing.higgs_model()
    gauge, adjoint, _, _, _, _, embedding, _, meshes, _, native = model
    _, _, cartan, color, weak, y = triplet.flat.compact_chart()
    core = triplet.adjoint_phase.core
    five = core.topology.representation_check(adjoint.astype(int), cartan, weak, y)["fundamental5_chart"]
    root, _ = core.monopole_root(adjoint.astype(int), five)
    records, words, rules = native
    x, z, _, fundamental, _, (_, _, weights) = triplet.flavor.projected_space(
        gauge.astype(int), adjoint.astype(int), color, weak, y, records)
    alpha = fundamental[five[0]]-fundamental[five[3]]
    vacuum = np.diag(y).astype(float), np.concatenate((x, z)).reshape(5, 27, 3).astype(float)
    source = meshes[-1]
    fields = np.array(source["state"])
    slopes = np.zeros(fields.shape[1])
    slopes[1] = fields[1, 1]/source["grid"][1]
    profile = CubicSpline(source["grid"], fields, bc_type=((1, slopes), "not-a-knot"))
    results = []
    for name, weight, sign in zip(("Q", "Uc", "L", "Ec"), (*exchange.QU, *exchange.LE), (-1, 1, 1, -1)):
        positive = np.array(weight) + (alpha if sign < 0 else 0)
        frames = sector_frames(adjoint, weights, root, positive)
        evaluators = [triplet.mass_evaluator(*frame, records, words, rules) for frame in frames]
        for count in (40, 72):
            grid = np.r_[np.geomspace(1e-6, .14, count+1), np.geomspace(.14, source["grid"][-1], count+1)[1:]]
            row = radial_match(grid, profile, embedding, evaluators, vacuum)
            results.append(dict(slot=name, cells=2*count, **row))
            print(name, count, row["light_channels"], row["matching_sigma_min"], row["radial_norm_samples"], flush=True)
    return dict(status="PASS", sampled_radii=[.01, .03, .06, .1, .2, .4, 1., 3., 5.], results=results)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    args.output.write_text(json.dumps(calculate(), indent=2) + "\n", encoding="utf-8")
