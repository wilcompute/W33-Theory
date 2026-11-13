"""Test a two-pole scattering model on the extended Robin monopole."""

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm, logm

import toe_20261113_monopole_triplet_tail as tail


line = tail.line
OUT = tail.OUT.with_name("toe_20261113_monopole_triplet_tail_interference.json")


def product(energy, locations, projectors):
    result = np.eye(4, dtype=complex)
    for location, projection in zip(locations, projectors):
        result = line.factor(energy, location, projection) @ result
    return result


def calculate(outer, elements):
    system, _, _, report = tail.prepare_tail(outer, elements)
    system = tail.split_transfers(system)
    fixture = tail.OUT if outer == 9. else tail.OUT.with_name(
        "toe_20261113_monopole_triplet_tail_robin5.json")
    seed = complex(*json.loads(fixture.read_text(encoding="utf-8"))["cuts"][-1]["pole"]["energy"])
    radius = float(system[1][-1])
    positive, _ = line.residues.poles.pole(system, seed, cut=radius)
    negative, _ = line.residues.poles.pole(system, -positive.conjugate(), cut=radius)
    assert abs(positive+negative.conjugate()) < 1e-9
    locations = (positive, negative)
    incoming, outgoing = line.flavors.flavor_frames()

    def reflection(energy):
        return outgoing.conj().T @ line.residues.matching(system, energy) @ incoming

    def residue(z, width, samples):
        offsets = width*np.exp(2j*np.pi*np.arange(samples)/samples)
        return sum(offset*reflection(z+offset) for offset in offsets)/samples

    amplitudes = []
    residue_errors = []
    for z in locations:
        a = residue(z, 8e-5, 8)
        b = residue(z, 4e-5, 8)
        error = float(np.linalg.norm(a-b)/np.linalg.norm(b))
        assert error < 1e-6
        residue_errors.append(error)
        amplitudes.append(b)
        print("residue", z, error, flush=True)
    amplitudes = np.array(amplitudes)
    projectors = line.projectors(locations, amplitudes)
    energies = sorted(set(np.linspace(-.004, .004, 17)) | {-positive.real, positive.real})
    models, rows = {}, []
    for energy in energies:
        full = reflection(energy)
        assert np.linalg.norm(full.conj().T @ full-np.eye(4)) < 1e-8
        pole_sum = np.sum(amplitudes/(energy-np.array(locations))[:, None, None], axis=0)
        factors = product(energy, locations, projectors)
        models[energy] = (full @ factors.conj().T, factors)
        rows.append(dict(energy=float(energy), **line.decompose(full, pole_sum)))
    center = models[0.][0]
    step = .001
    slope = logm(models[step][0] @ models[-step][0].conj().T)/(2*step)
    slope = (slope-slope.conj().T)/2
    for row in rows:
        energy = row["energy"]
        _, factors = models[energy]
        row["constant_background"] = float(line.conversion(center @ factors))
        row["linear_unitary_background"] = float(line.conversion(expm(energy*slope) @ center @ factors))
    holdout = [r for r in rows if r["energy"] not in (-step, 0., step)]
    errors = {key: max(abs(r[key]-r["total"]) for r in holdout)
              for key in ("constant_background", "linear_unitary_background")}
    return dict(status="PASS", radius=radius, profile=report,
                poles=[[z.real, z.imag] for z in locations], residue_errors=residue_errors,
                projector_overlap=float(np.trace(projectors[0] @ projectors[1]).real),
                holdout_maximum_errors=errors, sampled_minimum=min(rows, key=lambda r: r["total"]),
                rows=rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outer", type=float, default=9.)
    parser.add_argument("--elements", type=int, default=120)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    result = calculate(args.outer, args.elements)
    args.output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(result["sampled_minimum"], result["holdout_maximum_errors"], flush=True)
