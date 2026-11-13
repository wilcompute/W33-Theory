"""Track the monopole triplet line shape against the finite matching boundary."""

import argparse
import json
from pathlib import Path

import numpy as np

import toe_20261113_monopole_triplet_line_shape as line


OUT = line.OUT.with_name("toe_20261113_monopole_triplet_cut.json")
ENERGIES = (0., .0016666666666666668, .0018333333333333333, .002, .002166666666666667, .004)


def truncate(system, requested):
    label, grid, *frames, base = system
    end = int(np.argmin(abs(grid-requested)))
    return label, grid[:end+1], *frames, base[:end]


def calculate(profile_index):
    poles = line.residues.poles
    frames = line.flavors.flavor_frames()
    prior = json.loads(line.flavors.OUT.read_text(encoding="utf-8"))["poles"]
    seed = complex(*prior["positive"]["energy"])
    system = next(poles.threshold.prepare(40, sectors=("L",), profile_index=profile_index))
    rows = []
    # Appending constant exterior at the same physical cut may change
    # only the common reflection phase, not any flavor probability.
    _, grid, flux, _, stable, _, _, decay, base = system
    unstable = flux @ stable
    exterior = (unstable*decay) @ unstable.conj().T - (stable*decay) @ stable.conj().T
    padding = 0.25
    extended = (system[0], np.r_[grid, grid[-1]+padding], *system[2:-1],
                np.concatenate((base, exterior[None])))
    energy = .002
    baseline = line.residues.matching(system, energy)
    padded = line.residues.matching(extended, energy)
    padding_error = float(np.linalg.norm(padded-np.exp(2j*energy*padding)*baseline))
    assert padding_error < 1e-8
    for requested in (5., 4., 3.):
        cut = truncate(system, requested)
        radius = float(cut[1][-1])
        center, pole = poles.pole(cut, seed, cut=radius)
        other, negative = poles.pole(cut, -center.conjugate(), cut=radius)
        assert abs(other + center.conjugate()) < 1e-9
        # Refitting uses the same finite boundary in the Evans matrix
        # and the amplitude matching used for the residue contour.
        locations = np.array([center, other])
        matrices = np.array([
            frames[1].conj().T @ line.residues.residue(cut, z, 4e-5, 8) @ frames[0]
            for z in locations
        ])
        projections = line.projectors(locations, matrices)
        samples = []
        for energy in ENERGIES:
            full = frames[1].conj().T @ line.residues.matching(cut, energy) @ frames[0]
            assert np.linalg.norm(full.conj().T @ full-np.eye(4)) < 1e-8
            principal = np.sum(matrices/(energy-locations)[:, None, None], axis=0)
            samples.append(dict(energy=energy, **line.decompose(full, principal)))
        row = dict(requested_cut=requested, radius=radius, cells=len(cut[1])-1,
                   poles=[pole, negative], projector_overlap=float(np.trace(projections[0] @ projections[1]).real),
                   samples=samples, minimum=min(samples, key=lambda r: r["total"]))
        rows.append(row)
        seed = center
        print(radius, center, row["minimum"], flush=True)
    reference = rows[0]["samples"]
    for row in rows:
        row["maximum_conversion_change"] = max(abs(a["total"]-b["total"])
                                               for a, b in zip(reference, row["samples"]))
    return dict(status="PASS", profile_index=profile_index, constant_exterior_padding_error=padding_error, cuts=rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile-index", type=int, default=-1)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    args.output.write_text(json.dumps(calculate(args.profile_index), indent=2)+"\n", encoding="utf-8")
