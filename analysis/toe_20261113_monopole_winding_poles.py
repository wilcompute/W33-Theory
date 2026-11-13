"""Continue the W33 outgoing radial matching determinant into complex energy."""

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm
from scipy.optimize import root

import toe_20261113_monopole_winding_threshold as threshold


OUT = threshold.triplet.flat.ROOT / "data/toe_20261113_monopole_winding_poles.json"


def positive_qr(matrix):
    q, r = np.linalg.qr(matrix)
    diagonal = np.diag(r)
    return q * (diagonal / abs(diagonal))


def outgoing_match(system, energy, cut=5.):
    _, grid, flux, regular, stable, _, outgoing, decay, base = system
    end = int(np.argmin(abs(grid-cut)))
    mid = (len(grid)-1)//2
    rate = np.sqrt(decay**2-energy**2)
    decaying = stable - (flux @ stable)*(1j*energy/(decay+rate))
    exterior = positive_qr(np.column_stack((decaying, outgoing)))
    generators = (base[:end]+1j*energy*flux)*np.diff(grid[:end+1])[:, None, None]
    for generator in generators[:mid]:
        regular = positive_qr(expm(generator) @ regular)
    for generator in generators[:mid-1:-1]:
        exterior = positive_qr(expm(-generator) @ exterior)
    return np.column_stack((regular, -exterior))


def pole(system, seed, cut=5.):
    reference = outgoing_match(system, seed, cut)
    u, s, vh = np.linalg.svd(reference)
    det_reference = np.prod(s[:-1])
    def objective(coordinates):
        energy = complex(*coordinates)
        frame = outgoing_match(system, energy, cut)
        local = u.conj().T @ frame @ vh.conj().T
        value = np.linalg.det(local)/det_reference
        return [value.real, value.imag]

    answer = root(objective, [seed.real, seed.imag], tol=1e-9)
    energy = complex(*answer.x)
    matrix = outgoing_match(system, energy, cut)
    singular = np.linalg.svd(matrix, compute_uv=False)
    assert singular[-1] < 1e-9, (seed, energy, singular[-1], answer.message)
    assert energy.imag < 0
    return energy, dict(seed=[seed.real, seed.imag], energy=[energy.real, energy.imag],
                        cut=cut, smallest_singular_values=singular[-3:].tolist())


def contour(system, center, radius, samples, cut=5.):
    z = center + radius*np.exp(2j*np.pi*np.arange(samples)/samples)
    determinants, minima = [], []
    for energy in z:
        matrix = outgoing_match(system, energy, cut)
        determinants.append(np.linalg.slogdet(matrix)[0])
        minima.append(np.linalg.svd(matrix, compute_uv=False)[-1])
    determinants = np.array(determinants)
    increments = np.angle(np.roll(determinants, -1)/determinants)
    winding = np.sum(increments)/(2*np.pi)
    assert abs(winding-round(winding)) < 1e-10
    return dict(center=[center.real, center.imag], radius=radius, samples=samples,
                sampled_winding=int(round(winding)), max_phase_step=float(max(abs(increments))),
                sampled_minimum_singular_value=float(min(minima)))


def calculate(count, samples):
    rows = []
    for system in threshold.prepare(count):
        name = system[0]
        seeds = {"Q/Uc": [.00045-.0006j, .0017-.0009j],
                 "L": [.002-.00055j], "Ec": []}[name]
        roots = []
        for seed in seeds:
            try:
                energy, row = pole(system, seed)
            except AssertionError as error:
                print(name, "seed failed", error, flush=True)
                continue
            if any(abs(energy-complex(*known["energy"])) < 1e-8 for known in roots):
                continue
            print(name, row, flush=True)
            row["local_contour"] = contour(system, energy, 0.0001, samples)
            row["shorter_cut"] = pole(system, energy, cut=3.)[1]
            roots.append(row)
        broad = contour(system, -.0025j, .003, 2*samples)
        print(name, broad, flush=True)
        rows.append(dict(sector=name, poles=roots, broad_contour=broad))
    return dict(status="PASS", cells=2*count, sectors=rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, default=40)
    parser.add_argument("--samples", type=int, default=16)
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--roots-only", action="store_true", help="Replay the positive-real roots on a finer mesh")
    args = parser.parse_args()
    if args.roots_only:
        seeds = {"Q/Uc": [.000782-.000250j], "L": [.002-.00055j], "Ec": []}
        result = {system[0]: [pole(system, s)[1] for s in seeds[system[0]]]
                  for system in threshold.prepare(args.count)}
    else:
        result = calculate(args.count, args.samples)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
