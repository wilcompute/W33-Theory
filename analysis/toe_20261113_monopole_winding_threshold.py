"""Scan the near-threshold W33 Weyl matching and its incident overlap."""

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.interpolate import CubicSpline
from scipy.linalg import expm

import toe_20261113_monopole_winding_radial as radial


triplet = radial.triplet
OUT = triplet.flat.ROOT / "data/toe_20261113_monopole_winding_threshold.json"


CORE_MATCH_RADIUS = .14


def matching_index(grid):
    index = int(np.searchsorted(grid, CORE_MATCH_RADIUS))
    assert 0 < index < len(grid)-1 and grid[index] == CORE_MATCH_RADIUS
    return index


def prepare(count, sectors=None, profile_index=-1):
    model = radial.exchange.radial.mixing.higgs_model()
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
    mesh = meshes[profile_index]
    fields = np.array(mesh["state"])
    slopes = np.zeros(fields.shape[1])
    slopes[1] = fields[1, 1]/mesh["grid"][1]
    profile = CubicSpline(mesh["grid"], fields, bc_type=((1, slopes), "not-a-knot"))
    grid = np.r_[np.geomspace(1e-6, CORE_MATCH_RADIUS, count+1), np.geomspace(CORE_MATCH_RADIUS, 5., count+1)[1:]]
    for label, positive in (("Q/Uc", np.array(radial.exchange.QU[0])+alpha),
                            ("L", radial.exchange.LE[0]), ("Ec", np.array(radial.exchange.LE[1])+alpha)):
        if sectors is not None and label not in sectors:
            continue
        frames = radial.sector_frames(adjoint, weights, root, positive)
        evaluators = [triplet.mass_evaluator(*f, records, words, rules) for f in frames]
        flux, stable, incoming, outgoing, masses = radial.exterior_basis(evaluators, vacuum)
        _, outer = triplet.radial_hamiltonian(*masses, 0.)
        _, angular = triplet.radial_hamiltonian(*[np.zeros_like(m) for m in masses], 1.)
        regular = np.eye(len(flux), dtype=complex)[:, (-1j*flux @ angular).diagonal().real > 0]
        decay = -np.diag(stable.conj().T @ (-1j*flux @ outer) @ stable).real
        np.testing.assert_allclose(outer @ flux + flux @ outer, 0., atol=1e-11)
        base = []
        for r in (grid[:-1]+grid[1:])/2:
            state = profile(r)
            a, matter = triplet.profile_fields(state, embedding)
            local = [sum(evaluate(a, matter)) for evaluate in evaluators]
            _, potential = triplet.radial_hamiltonian(*local, state[0]/triplet.neutral.SQRT6/r)
            base.append(-1j*flux @ potential)
        yield label, grid, flux, regular, stable, incoming, outgoing, decay, np.array(base)


def match(system, energy, outer_radius=5.):
    _, grid, flux, regular, stable, incoming, outgoing, decay, base = system
    assert abs(energy) < min(decay)
    end = int(np.argmin(abs(grid-outer_radius)))
    # G(E)=G(0)+iE F. The F image pairs stable and unstable
    # eigenvectors, and the decaying branch has eigenvalue -sqrt(m^2-E^2).
    rate = np.sqrt(decay**2-energy**2)
    stable = stable - (flux @ stable)*(1j*energy/(decay+rate))
    stable = np.linalg.qr(stable)[0]
    allowed = np.column_stack((stable, outgoing, incoming))
    cols = incoming.shape[1]
    mid = matching_index(grid)
    assert end > mid
    transport = np.eye(cols, dtype=complex)
    generators = (base[:end]+1j*energy*flux)*np.diff(grid[:end+1])[:, None, None]
    for generator in generators[:mid]:
        regular = np.linalg.qr(expm(generator) @ regular)[0]
    for generator in generators[:mid-1:-1]:
        allowed, triangular = np.linalg.qr(expm(-generator) @ allowed)
        transport = triangular[-cols:, -cols:] @ transport
    a = np.column_stack((regular, -allowed[:, :-cols]))
    u, singular, vh = np.linalg.svd(a, full_matrices=False)
    forcing = allowed[:, -cols:] @ transport
    coefficients = u.conj().T @ forcing
    solution = vh.conj().T @ (coefficients/singular[:, None])
    local = regular @ solution[:regular.shape[1]]
    # Isolate the response of the weakest three singular directions.
    weak = vh[-3:, :regular.shape[1]].conj().T @ (coefficients[-3:]/singular[-3:, None])
    standing_flux = float(np.max(abs(local.conj().T @ flux @ local)))
    assert standing_flux < 1e-7
    heavy = np.linalg.svd(regular.conj().T @ allowed[:, :len(decay)], compute_uv=False)
    return dict(energy=energy, outer_radius=float(grid[end]),
                matching_singular_values=singular[-4:].tolist(),
                heavy_only_sine=float(np.sqrt(max(0., 1.-heavy[0]**2))),
                weakest_three_incident_overlap=float(np.linalg.norm(coefficients[-3:])),
                weakest_three_core_response=float(np.linalg.norm(weak)),
                matching_radius=float(grid[mid]), matching_radius_norm=float(np.linalg.norm(local)),
                standing_flux_error=standing_flux)


def calculate(count):
    rows = []
    for system in prepare(count):
        scale = min(.02, .2*min(system[7]))
        samples = [match(system, scale*f) for f in (-1., -.5, -.25, -.1, 0., .1, .25, .5, 1.)]
        cut = [match(system, 0., radius) for radius in (2., 3., 4.)]
        rows.append(dict(sector=system[0], smallest_exterior_mass=float(min(system[7])),
                         samples=samples, shorter_exteriors=cut))
        print(system[0], [(round(r["energy"], 6), round(r["matching_radius_norm"], 4))
                          for r in samples], flush=True)
    return dict(status="PASS", cells=2*count, scope="real core with constant exterior at the selected cut",
                sectors=rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, default=40)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    args.output.write_text(json.dumps(calculate(args.count), indent=2) + "\n", encoding="utf-8")
